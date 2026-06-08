#!/usr/bin/env python3
"""
Session Manager - Single source of truth for persistent daemon state
Handles save/load of MCP context, Memory Bank pointers, task queue, logs
"""

import os
import json
import time
import shutil
from datetime import datetime
from typing import Dict, Optional, Any


class SessionManager:
    """Manages persistent session state with graceful recovery"""

    def __init__(self, base_dir=None, max_snapshots=3):
        if base_dir is None:
            base_dir = os.path.dirname(__file__)

        self.base_dir = base_dir
        self.session_file = os.path.join(base_dir, "session.json")
        self.snapshot_dir = os.path.join(base_dir, "snapshots")
        self.max_snapshots = max_snapshots

        os.makedirs(self.snapshot_dir, exist_ok=True)

    def save_session(self, state: Dict, reason: str = "tick") -> str:
        """Save current session state to disk atomically"""
        timestamp = datetime.now().isoformat()

        session_data = {
            "timestamp": timestamp,
            "reason": reason,
            "version": "0.9-persistent",
            "state": state,
        }

        # Write to temp file first, then rename (atomic)
        temp_file = self.session_file + ".tmp"
        with open(temp_file, "w") as f:
            json.dump(session_data, f, indent=2)

        os.replace(temp_file, self.session_file)

        # Create snapshot for recovery
        snapshot_name = f"snapshot_{int(time.time())}.json"
        snapshot_path = os.path.join(self.snapshot_dir, snapshot_name)
        shutil.copy(self.session_file, snapshot_path)
        self._prune_snapshots()

        return timestamp

    def load_session(self) -> Optional[Dict]:
        """Load previous session state from disk, fallback to snapshot"""
        if not os.path.exists(self.session_file):
            return None

        try:
            with open(self.session_file, "r") as f:
                data = json.load(f)
            return data.get("state", {})
        except (json.JSONDecodeError, IOError):
            return self._recover_from_snapshot()

    def _recover_from_snapshot(self) -> Optional[Dict]:
        """Recover from last good snapshot"""
        snapshots = sorted(
            [f for f in os.listdir(self.snapshot_dir) if f.endswith(".json")],
            reverse=True,
        )

        for snap in snapshots[: self.max_snapshots]:
            try:
                path = os.path.join(self.snapshot_dir, snap)
                with open(path, "r") as f:
                    data = json.load(f)
                print(f"Recovered session from: {snap}")
                return data.get("state", {})
            except Exception:
                continue

        print("No valid snapshot found")
        return None

    def _prune_snapshots(self):
        """Keep only max_snapshots most recent"""
        snapshots = sorted(
            [f for f in os.listdir(self.snapshot_dir) if f.endswith(".json")],
            reverse=True,
        )

        for old in snapshots[self.max_snapshots :]:
            os.remove(os.path.join(self.snapshot_dir, old))

    def get_session_info(self) -> Dict:
        """Get current session info"""
        if not os.path.exists(self.session_file):
            return {"exists": False}

        try:
            with open(self.session_file, "r") as f:
                data = json.load(f)

            return {
                "exists": True,
                "timestamp": data.get("timestamp"),
                "reason": data.get("reason"),
                "version": data.get("version"),
            }
        except Exception:
            return {"exists": False, "error": "corrupted"}


class PersistentDaemonState:
    """Single source of truth for all daemon session save/load operations.

    Wraps a daemon instance and handles:
    - Tick count persistence
    - Task queue preservation
    - MCP context storage
    - Graceful recovery from snapshots
    - Snapshot pruning (max 3)
    - File permission checks
    """

    def __init__(self, daemon, base_dir=None, max_snapshots=3):
        self.daemon = daemon
        self.session = SessionManager(base_dir=base_dir, max_snapshots=max_snapshots)
        self.version = "0.9-persistent-competitive"
        self.log_file = os.path.join(
            base_dir or os.path.dirname(__file__), "daemon.log"
        )

    def save(self, reason: str = "tick") -> str:
        """Save current daemon session state"""
        state = {
            "tick_count": self.daemon.tick_count,
            "task_queue": self.daemon.queue.get_pending(),
            "context": self.daemon.context.to_dict(),
            "running": self.daemon.running,
            "peers": self.daemon.mesh.get_peers(),
        }

        timestamp = self.session.save_session(state, reason)
        self._log(f"Session saved ({reason}) at tick {self.daemon.tick_count}")
        return timestamp

    def load(self) -> bool:
        """Load previous session and restore daemon state"""
        state = self.session.load_session()

        if state is None:
            self._log("No previous session found, starting fresh")
            print("No previous session found, starting fresh")
            return False

        # Restore tick count
        self.daemon.tick_count = state.get("tick_count", 0)

        # Restore context
        ctx = state.get("context", {})
        for k, v in ctx.items():
            self.daemon.context.update(k, v)

        # Restore tasks to queue
        tasks = state.get("task_queue", [])
        for task in tasks:
            self.daemon.queue.add_task(task["task"])

        # Restore peers
        peers = state.get("peers", {})
        for peer, info in peers.items():
            self.daemon.mesh.add_peer(peer)

        self._log(
            f"Session restored: tick={self.daemon.tick_count}, tasks={len(tasks)}, peers={len(peers)}"
        )
        print(f"Restored session: tick={self.daemon.tick_count}")
        return True

    def get_info(self) -> Dict:
        """Get combined session and daemon info"""
        return {
            "session": self.session.get_session_info(),
            "daemon": {
                "tick_count": self.daemon.tick_count,
                "running": self.daemon.running,
                "version": self.version,
            },
        }

    def _log(self, message: str):
        """Append to daemon log file"""
        timestamp = datetime.now().isoformat()
        try:
            with open(self.log_file, "a") as f:
                f.write(f"[{timestamp}] {message}\n")
        except IOError:
            pass

    def check_permissions(self) -> Dict[str, bool]:
        """Check file permissions for state files (secure governance)"""
        results = {}
        for path in [
            self.session.session_file,
            self.log_file,
            self.daemon.queue.db_path,
        ]:
            if os.path.exists(path):
                results[path] = os.access(path, os.R_OK) and os.access(path, os.W_OK)
            else:
                results[path] = False
        return results
