#!/usr/bin/env python3
"""
Secure Governance Layer - Tool allow-lists, permission checks, task isolation
Inspired by KiloClaw enterprise security for secure always-on agents
"""

import os
import re
import sqlite3
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class AuditLogger:
    """Audit logging for compliance"""

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "audit.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER,
                tool TEXT,
                command TEXT,
                user TEXT,
                result TEXT,
                isolated INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def log(
        self,
        tool: str,
        command: str,
        user: str = "agent",
        result: str = "success",
        isolated: bool = False,
    ):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO audit_log (timestamp, tool, command, user, result, isolated) VALUES (?, ?, ?, ?, ?, ?)",
            (int(time.time()), tool, command[:200], user, result, int(isolated)),
        )

        conn.commit()
        conn.close()

    def get_recent(self, limit: int = 10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT timestamp, tool, command, user, result FROM audit_log ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )

        results = []
        for row in cursor.fetchall():
            results.append(
                {
                    "timestamp": datetime.fromtimestamp(row[0]).isoformat(),
                    "tool": row[1],
                    "command": row[2][:50],
                    "user": row[3],
                    "result": row[4],
                }
            )

        conn.close()
        return results


class ToolAllowList:
    """Controls which tools can be executed"""

    def __init__(self):
        self.safe_tools = {
            "read",
            "grep",
            "glob",
            "websearch",
            "webfetch",
            "codesearch",
        }
        self.restricted_tools = {"edit", "write", "bash"}
        self.blocked_tools = {"ssh", "docker", "rm", "delete", "exec"}

        self.dangerous_patterns = [
            r"rm\s+-rf",
            r"dd\s+if=",
            r"curl.*\|\s*sh",
            r"wget.*\|\s*sh",
            r">\s*/dev/",
            r"chmod\s+777",
            r"chown\s+-R",
        ]

    def is_allowed(self, tool: str, command: str = "") -> Dict:
        """Check if tool/command is allowed"""
        if tool in self.blocked_tools:
            return {
                "allowed": False,
                "reason": f"Tool {tool} is blocked",
                "requires_approval": True,
            }

        if tool in self.restricted_tools:
            if any(
                re.search(p, command, re.IGNORECASE) for p in self.dangerous_patterns
            ):
                return {
                    "allowed": False,
                    "reason": "Dangerous pattern detected",
                    "requires_approval": True,
                }
            return {
                "allowed": True,
                "warning": f"Tool {tool} requires attention",
                "requires_approval": False,
            }

        if tool in self.safe_tools:
            return {"allowed": True, "requires_approval": False}

        return {"allowed": False, "reason": "Unknown tool", "requires_approval": True}

    def add_allowed(self, tool: str):
        self.safe_tools.add(tool)

    def block_tool(self, tool: str):
        self.blocked_tools.add(tool)
        if tool in self.safe_tools:
            self.safe_tools.remove(tool)
        if tool in self.restricted_tools:
            self.restricted_tools.remove(tool)


class TaskIsolator:
    """Provides sandboxed execution environment"""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or "/tmp/kairos-sandbox"
        os.makedirs(self.base_dir, exist_ok=True)

    def create_workspace(self, task_id: str) -> str:
        workspace = os.path.join(self.base_dir, f"task_{task_id}")
        os.makedirs(workspace, exist_ok=True)
        return workspace

    def cleanup(self, task_id: str):
        import shutil

        workspace = os.path.join(self.base_dir, f"task_{task_id}")
        if os.path.exists(workspace):
            shutil.rmtree(workspace)

    def is_path_safe(self, path: str) -> bool:
        """Check if path is within allowed directories"""
        protected = ["/etc", "/root", "/home", "/var"]

        abs_path = os.path.abspath(path)
        for p in protected:
            if abs_path.startswith(p):
                return False
        return True


class SecureGovernor:
    """Main secure governance controller"""

    def __init__(self):
        self.allow_list = ToolAllowList()
        self.isolator = TaskIsolator()
        self.audit = AuditLogger()

    def check_permission(
        self, tool: str, command: str = "", isolated: bool = False
    ) -> Dict:
        """Check if operation is allowed"""
        result = self.allow_list.is_allowed(tool, command)

        if not result.get("allowed"):
            self.audit.log(tool, command, result="blocked", isolated=isolated)
        else:
            self.audit.log(tool, command, result="allowed", isolated=isolated)

        return result

    def execute_with_check(
        self, tool: str, command: str = "", isolated: bool = False
    ) -> Dict:
        """Execute with permission check"""
        permission = self.check_permission(tool, command, isolated)

        if not permission["allowed"]:
            return {
                "success": False,
                "message": permission["reason"],
                "requires_approval": permission.get("requires_approval", False),
            }

        return {
            "success": True,
            "message": "Proceed",
            "warning": permission.get("warning"),
        }

    def get_policy(self) -> Dict:
        """Get current security policy"""
        return {
            "safe_tools": list(self.allow_list.safe_tools),
            "restricted_tools": list(self.allow_list.restricted_tools),
            "blocked_tools": list(self.allow_list.blocked_tools),
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Secure Governance CLI")
    parser.add_argument("command", choices=["check", "allowlist", "audit", "policy"])
    parser.add_argument("args", nargs="*")

    gov = SecureGovernor()

    args = parser.parse_args()

    if args.command == "check":
        tool = args.args[0] if len(args.args) > 0 else "bash"
        cmd = " ".join(args.args[1:]) if len(args.args) > 1 else ""
        result = gov.execute_with_check(tool, cmd)
        print(json.dumps(result, indent=2))

    elif args.command == "allowlist":
        action = args.args[0] if len(args.args) > 0 else ""
        tool = args.args[1] if len(args.args) > 1 else ""

        if action == "add" and tool:
            gov.allow_list.add_allowed(tool)
            print(f"Added {tool} to allow list")
        elif action == "block" and tool:
            gov.allow_list.block_tool(tool)
            print(f"Blocked {tool}")

    elif args.command == "audit":
        limit = int(args.args[0]) if args.args and args.args[0].isdigit() else 10
        logs = gov.audit.get_recent(limit)
        for log in logs:
            print(
                f"[{log['timestamp']}] {log['tool']}: {log['command']} -> {log['result']}"
            )

    elif args.command == "policy":
        print(json.dumps(gov.get_policy(), indent=2))


if __name__ == "__main__":
    main()
