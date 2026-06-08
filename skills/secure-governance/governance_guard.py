#!/usr/bin/env python3
"""
Governance Guard v0.11 - Pre-execution policy enforcement & task assessment
Enforces tool allow-lists, checks for dangerous patterns, and assesses task complexity.
"""

import os
import re
import json
import time
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional


class GovernanceGuard:
    """Pre-execution guard that checks every task before it runs.

    Enforces:
    - Tool allow-lists (safe, restricted, blocked)
    - Dangerous pattern detection in task descriptions
    - Complexity assessment for Multi-LLM Routing
    - Audit logging to both daemon.log and internal SQLite
    """

    DANGEROUS_PATTERNS = [
        r"rm\s+-rf\s+/",
        r"dd\s+if=",
        r"curl.*\|\s*(ba)?sh",
        r"wget.*\|\s*(ba)?sh",
        r">\s*/dev/sd",
        r"chmod\s+777\s+/",
        r"chown\s+-R\s+/",
        r"mkfs",
        r"fdisk",
        r"sudo\s+rm",
        r"sudo\s+apt",
        r"sudo\s+systemctl",
        r":\(\)\{\s*:\|:\s*&\s*\};:",
        r"kill\s+-9\s+1",
        r"format\s+[a-z]:",
        r"shred",
        r"wipe",
        r"parted",
        r"wipefs",
        r"os\.environ",
        r"os\.getenv",
        r"print\s*\(.*environ",
        r"echo\s+\$[A-Z0-9_]+",
        r"cat\s+.*\.env",
        r"\bprintenv\b",
    ]

    SAFE_TASK_PREFIXES = [
        "confirm",
        "check",
        "verify",
        "list",
        "show",
        "report",
        "analyze",
        "summarize",
        "review",
        "audit",
        "scan",
        "explain",
        "describe",
    ]

    COMPLEXITY_KEYWORDS = [
        "refactor",
        "implement",
        "architect",
        "debug",
        "fix",
        "optimize",
        "rewrite",
        "compare",
        "analyze",
        "design",
    ]

    def __init__(self, base_dir=None, daemon_log=None):
        if base_dir is None:
            base_dir = os.path.dirname(__file__)
        self.base_dir = base_dir
        self.audit_db = os.path.join(base_dir, "governance_audit.db")
        self.daemon_log = daemon_log or os.path.join(
            os.path.dirname(base_dir), "kairos-daemon", "daemon.log"
        )
        self._init_db()

        self.safe_tools = {
            "read_file",
            "grep_search",
            "glob",
            "web_fetch",
            "google_web_search",
            "list_directory",
            "ask_user",
        }
        self.restricted_tools = {"replace", "write_file", "run_shell_command"}
        self.blocked_tools = {"ssh", "docker", "exec", "sudo", "git push", "npm install"}

    def _init_db(self):
        conn = sqlite3.connect(self.audit_db)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS governance_log (
            id INTEGER PRIMARY KEY,
            timestamp INTEGER,
            task TEXT,
            decision TEXT,
            reason TEXT,
            risk_level TEXT,
            complexity_level TEXT
        )""")
        conn.commit()
        conn.close()

    def check_task(self, task: str) -> Dict:
        """Evaluate a task description and return decision + assessment."""
        risk = self._assess_risk(task)
        complexity = self._assess_complexity(task)
        decision = self._make_decision(risk)

        self._audit_log(task, decision, complexity)
        return {
            "allowed": decision["allowed"],
            "risk_level": risk["level"],
            "complexity_level": complexity,
            "reason": decision["reason"],
            "requires_approval": decision.get("requires_approval", False),
        }

    def _assess_risk(self, task: str) -> Dict:
        """Assess risk level of a task description."""
        task_lower = task.lower()

        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, task_lower, re.IGNORECASE):
                return {"level": "critical", "matched_pattern": pattern}

        for tool in self.blocked_tools:
            if tool in task_lower:
                return {"level": "high", "matched_tool": tool}

        for prefix in self.SAFE_TASK_PREFIXES:
            if task_lower.startswith(prefix):
                return {"level": "low", "reason": "safe prefix"}

        return {"level": "medium", "reason": "unknown task type"}

    def _assess_complexity(self, task: str) -> str:
        """Assess complexity level of a task description."""
        task_lower = task.lower()
        
        # High complexity markers
        for kw in self.COMPLEXITY_KEYWORDS:
            if kw in task_lower:
                return "high"
        
        # Medium complexity markers (tool usage)
        for tool in self.restricted_tools:
            if tool in task_lower:
                return "medium"
                
        # Low complexity (basic queries/checks)
        # Refined: tasks with fewer than 5 words AND no complex keywords are low complexity
        if len(task.split()) <= 5:
            return "low"
            
        return "medium"

    def _make_decision(self, risk: Dict) -> Dict:
        """Make allow/block decision based on risk assessment."""
        level = risk["level"]

        if level == "critical":
            return {
                "allowed": False,
                "reason": f"Critical risk: {risk.get('matched_pattern', 'blocked pattern')}",
                "requires_approval": True,
            }

        if level == "high":
            return {
                "allowed": False,
                "reason": f"High risk: blocked tool '{risk.get('matched_tool')}' detected",
                "requires_approval": True,
            }

        if level == "medium":
            return {
                "allowed": True,
                "reason": "Medium risk - allowed with audit logging",
                "requires_approval": False,
            }

        return {
            "allowed": True,
            "reason": "Low risk - safe task",
            "requires_approval": False,
        }

    def _audit_log(self, task: str, decision: Dict, complexity: str):
        """Log governance decision to SQLite and daemon log."""
        timestamp = int(time.time())
        risk = "blocked" if not decision["allowed"] else "allowed"
        reason = decision["reason"]

        conn = sqlite3.connect(self.audit_db)
        cursor = conn.cursor()
        
        # Ensure column exists for complexity_level if table already existed
        try:
            cursor.execute("ALTER TABLE governance_log ADD COLUMN complexity_level TEXT")
        except sqlite3.OperationalError:
            pass # Already exists
            
        cursor.execute(
            "INSERT INTO governance_log (timestamp, task, decision, reason, risk_level, complexity_level) VALUES (?, ?, ?, ?, ?, ?)",
            (
                timestamp,
                task[:200],
                risk,
                reason[:200],
                decision.get("risk_level", "unknown"),
                complexity
            ),
        )
        conn.commit()
        conn.close()

        ts = datetime.now().isoformat()
        try:
            with open(self.daemon_log, "a") as f:
                f.write(f"[{ts}] GOVERNANCE: {risk} - {task[:80]} (Risk: {decision.get('risk_level', 'unknown')}, Complexity: {complexity})\n")
        except IOError:
            pass

    def get_recent_decisions(self, limit: int = 10) -> List[Dict]:
        """Get recent governance decisions."""
        conn = sqlite3.connect(self.audit_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, task, decision, reason, risk_level, complexity_level FROM governance_log ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        results = [
            {
                "timestamp": datetime.fromtimestamp(r[0]).isoformat(),
                "task": r[1],
                "decision": r[2],
                "reason": r[3],
                "risk_level": r[4],
                "complexity_level": r[5]
            }
            for r in cursor.fetchall()
        ]
        conn.close()
        return results

    def get_policy(self) -> Dict:
        """Return current governance policy."""
        return {
            "safe_tools": sorted(self.safe_tools),
            "restricted_tools": sorted(self.restricted_tools),
            "blocked_tools": sorted(self.blocked_tools),
            "dangerous_patterns_count": len(self.DANGEROUS_PATTERNS),
            "complexity_keywords": len(self.COMPLEXITY_KEYWORDS)
        }
