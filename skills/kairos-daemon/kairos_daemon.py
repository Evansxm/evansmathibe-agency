#!/usr/bin/env python3
"""
KAIROS Daemon v0.13 - Persistent background daemon with Secure Credentials
Uses PersistentDaemonState for session state, GovernanceGuard for task assessment,
MultiLLMRouter for model selection, and CredentialVault for encrypted secrets.
"""

import os
import sys
import time
import json
import sqlite3
import signal
import atexit
import subprocess
from datetime import datetime
from typing import List, Dict, Optional

from session_manager import PersistentDaemonState

# Add internal skills to path
daemon_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(daemon_dir, "..", "secure-governance"))
sys.path.insert(0, os.path.join(daemon_dir, "..", "multi-llm-router"))
sys.path.insert(0, os.path.join(daemon_dir, "..", "secure-credentials"))
sys.path.insert(0, os.path.join(daemon_dir, "..", "yts-manager"))

from governance_guard import GovernanceGuard
from router import MultiLLMRouter
from credential_vault import CredentialVault
from mesh_manager import MeshManager
from yts_notifier import YTSNotifier
from yts_tray import YTSManagerTray

class SharedContext:
    """Shared context for session state"""

    def __init__(self):
        self.state = {}
    def update(self, key, value):
        self.state[key] = value
    def get(self, key, default=None):
        return self.state.get(key, default)
    def to_dict(self):
        return dict(self.state)

class DaemonTaskQueue:
    """Append-only task queue backed by SQLite"""
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(daemon_dir, "daemon_tasks.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, task TEXT, status TEXT, created_at INTEGER, completed_at INTEGER, routed_model TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tick_logs (
            id INTEGER PRIMARY KEY, tick_number INTEGER, timestamp INTEGER, action TEXT, result TEXT)""")
        conn.commit()
        conn.close()

    def add_task(self, task: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task, status, created_at) VALUES (?, ?, ?)",
            (task, "pending", int(time.time())),
        )
        conn.commit()
        conn.close()

    def get_pending(self) -> List[dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, task FROM tasks WHERE status = ? ORDER BY created_at",
            ("pending",),
        )
        tasks = [{"id": r[0], "task": r[1]} for r in cursor.fetchall()]
        conn.close()
        return tasks

    def complete(self, task_id: int, status="completed", model: str = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN routed_model TEXT")
        except sqlite3.OperationalError:
            pass
        cursor.execute(
            "UPDATE tasks SET status = ?, completed_at = ?, routed_model = ? WHERE id = ?",
            (status, int(time.time()), model, task_id),
        )
        conn.commit()
        conn.close()

    def log_tick(self, tick_num: int, action: str, result: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tick_logs (tick_number, timestamp, action, result) VALUES (?, ?, ?, ?)",
            (tick_num, int(time.time()), action, result),
        )
        conn.commit()
        conn.close()

    def get_recent_logs(self, limit=20):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tick_number, timestamp, action, result FROM tick_logs ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        logs = [{"tick": r[0], "time": r[1], "action": r[2], "result": r[3]} for r in cursor.fetchall()]
        conn.close()
        return logs

class KAIROSDaemon:
    """Persistent background daemon with Secure Credentials and isolation"""

    def __init__(self, tick_interval=30, action_budget=15):
        self.tick_interval = tick_interval
        self.action_budget = action_budget
        self.running = False
        self.tick_count = 0
        self.queue = DaemonTaskQueue()
        self.context = SharedContext()
        self.version = "0.13-secure-credentials"
        self.daemon_dir = daemon_dir

        # Initialize core systems
        self.guard = GovernanceGuard(daemon_log=os.path.join(self.daemon_dir, "daemon.log"))
        self.vault = CredentialVault()
        self.router = MultiLLMRouter(vault=self.vault)
        self.mesh = MeshManager(self, port=int(os.getenv("KAIROS_MESH_PORT", 5000)))
        self.yts_notifier = YTSNotifier(check_interval=3600)
        self.yts_tray = YTSManagerTray(self)

        # Unified session state
        self.state = PersistentDaemonState(self)
        self.state.load()

        signal.signal(signal.SIGINT, lambda s, f: self._shutdown())
        signal.signal(signal.SIGTERM, lambda s, f: self._shutdown())
        atexit.register(self._cleanup)

    def _log(self, message: str):
        ts = datetime.now().isoformat()
        try:
            with open(os.path.join(self.daemon_dir, "daemon.log"), "a") as f:
                f.write(f"[{ts}] {message}\n")
        except IOError: pass

    def _shutdown(self):
        self._log("Shutdown initiated")
        self.running = False
        self.mesh.stop()
        self.yts_notifier.stop_monitor()
        self.yts_tray.stop_tray()
        self.state.save("shutdown")

    def _cleanup(self):
        self.state.save("exit")
        self.mesh.stop()
        self.yts_notifier.stop_monitor()
        self.yts_tray.stop_tray()
        self.running = False

    def _execute_task_isolated(self, task: str, tick_num: int) -> Dict:
        """Execute a task in an isolated subprocess with just-in-time secret injection."""
        assessment = self.guard.check_task(task)
        if not assessment["allowed"]:
            self._log(f"BLOCKED by governance: {task[:80]}")
            return {"success": False, "reason": assessment["reason"]}

        route = self.router.route_task(task, assessment["risk_level"], assessment["complexity_level"])
        self._log(f"ROUTING: {route['model']} ({route['tier']})")

        # Prepare environment with just-in-time secrets via router
        env = os.environ.copy()
        auth_env = self.router.get_auth_env(route["provider"])
        if auth_env:
            env.update(auth_env)
            for key in auth_env:
                # Log that a secret was injected (but not the value!)
                self._log(f"INJECTION: {key} provided to worker")

        tick_script = os.path.join(self.daemon_dir, "tick_worker.py")
        try:
            proc = subprocess.run(
                [sys.executable, tick_script, task, route["model"]],
                capture_output=True, text=True, timeout=self.action_budget, cwd=self.daemon_dir,
                env=env
            )
            if proc.returncode == 0:
                self._log(f"Task completed: {task[:50]}")
                return {"success": True, "output": proc.stdout.strip(), "model": route["model"]}
            else:
                return {"success": False, "error": proc.stderr.strip(), "model": route["model"]}
        except Exception as e:
            return {"success": False, "error": str(e), "model": route["model"]}

    def _run_tick(self):
        self.tick_count += 1
        pending = self.queue.get_pending()
        if pending:
            task = pending[0]
            exec_result = self._execute_task_isolated(task["task"], self.tick_count)
            self.queue.complete(task["id"], status="completed" if exec_result["success"] else "failed", model=exec_result.get("model"))
        
        if self.tick_count % 5 == 0:
            self.state.save("periodic")
        return {"tick": self.tick_count}

    def start(self):
        self.running = True
        self.mesh.start()
        self.yts_notifier.run_monitor()
        self.yts_tray.run_tray()
        print(f"KAIROS Daemon v{self.version} with Secure Credentials")
        while self.running:
            res = self._run_tick()
            time.sleep(self.tick_interval)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["start", "stop", "queue", "logs", "info", "guard", "router", "benchmark", "credential", "mesh"])
    parser.add_argument("args", nargs="*")
    args = parser.parse_args()

    daemon = KAIROSDaemon()

    if args.cmd == "start": daemon.start()
    elif args.cmd == "queue" and args.args:
        task = " ".join(args.args)
        daemon.queue.add_task(task)
        daemon.mesh.push_task_to_peers(task)
        print(f"Task queued and broadcast: {task}")
    elif args.cmd == "logs":
        for log in daemon.queue.get_recent_logs(10):
            print(f"[Tick {log['tick']}] {log['action']} - {log['result']}")
    elif args.cmd == "info":
        print(f"Version: {daemon.version}\nTick: {daemon.tick_count}\nNode: {daemon.mesh.node_id}")
    elif args.cmd == "guard":
        print(f"Governance Policy: {json.dumps(daemon.guard.get_policy(), indent=2)}")
    elif args.cmd == "router":
        print(f"Router Config: {json.dumps(daemon.router.get_config(), indent=2)}")
    elif args.cmd == "credential":
        if not args.args:
            print("Usage: credential {set,list,delete} [key] [value]")
            return
        sub = args.args[0]
        if sub == "set":
            if len(args.args) < 3:
                print("Usage: credential set <key> <value>")
            else:
                daemon.vault.set_secret(args.args[1], args.args[2])
                print(f"Secret '{args.args[1]}' encrypted and stored.")
        elif sub == "list":
            secrets = daemon.vault.list_secrets()
            if not secrets:
                print("No secrets stored in vault.")
            else:
                print("Stored secrets:")
                for s in sorted(secrets):
                    print(f"  - {s}")
        elif sub == "delete":
            if len(args.args) < 2:
                print("Usage: credential delete <key>")
            else:
                daemon.vault.delete_secret(args.args[1])
                print(f"Secret '{args.args[1]}' deleted.")
        else:
            print(f"Unknown credential command: {sub}")
    elif args.cmd == "mesh":
        if not args.args:
            print("Usage: mesh {join,list,sync} [args]")
            return
        sub = args.args[0]
        if sub == "join" and len(args.args) > 1:
            peer_addr = args.args[1]
            # Try to tell the running daemon first
            try:
                import urllib.request
                import json
                local_port = int(os.getenv("KAIROS_MESH_PORT", 5000))
                url = f"http://127.0.0.1:{local_port}/mesh/admin/add_peer"
                data = json.dumps({"peer": peer_addr}).encode('utf-8')
                req = urllib.request.Request(url, data=data, method="POST")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    res = json.loads(resp.read().decode())
                    print(f"Success: {res.get('message')}")
            except Exception as e:
                # Fallback to local memory update (for non-running daemon or startup)
                daemon.mesh.add_peer(peer_addr)
                daemon.state.save("mesh_join_fallback")
                print(f"Joining mesh node (offline mode): {peer_addr}")
        elif sub == "list":
            # Try to get list from running daemon
            peers = {}
            local_node = daemon.mesh.node_id
            try:
                import urllib.request
                import json
                local_port = int(os.getenv("KAIROS_MESH_PORT", 5000))
                url = f"http://127.0.0.1:{local_port}/mesh/admin/list_peers"
                req = urllib.request.Request(url, method="POST", data=b'{}')
                with urllib.request.urlopen(req, timeout=2) as resp:
                    res = json.loads(resp.read().decode())
                    peers = res.get("peers", {})
            except:
                peers = daemon.mesh.get_peers()
            
            print(f"Local Node: {local_node}")
            print("Mesh Peers:")
            if not peers:
                print("  (No peers discovered)")
            for p, info in peers.items():
                print(f"  - {p} ({info['status']})")
        elif sub == "sync":
            for p in daemon.mesh.get_peers():
                daemon.mesh._sync_tasks_with_peer(p)
            print("Mesh sync triggered.")
    elif args.cmd == "benchmark":
        sys.path.insert(0, os.path.join(daemon.daemon_dir, "..", "tenant-isolation-benchmark"))
        from benchmark import TenantBenchmark
        bench = TenantBenchmark()
        bench.run_routing_benchmark(); bench.run_concurrency_benchmark()
        print(f"Benchmark complete: {bench.generate_report()}")

if __name__ == "__main__":
    main()
