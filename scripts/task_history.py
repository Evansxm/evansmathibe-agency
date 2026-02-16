#!/usr/bin/env python3
"""
EvansMathibe Agency - Task History & Data Cache System
Tracks all tasks and allows recalling information
"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("/home/ev/EvansMathibe_Agency/data/agency_data.json")


class TaskHistory:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        if DATA_FILE.exists():
            with open(DATA_FILE) as f:
                return json.load(f)
        return {
            "task_history": [],
            "agency_info": {},
            "created_at": datetime.now().isoformat(),
        }

    def _save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_task(self, task: str, details: str = ""):
        task_entry = {
            "id": len(self.data.get("task_history", [])) + 1,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "task": task,
            "details": details,
        }
        if "task_history" not in self.data:
            self.data["task_history"] = []
        self.data["task_history"].append(task_entry)
        self.data["updated_at"] = datetime.now().isoformat()
        self._save_data()
        return task_entry

    def get_tasks(self, limit: int = 10):
        tasks = self.data.get("task_history", [])
        return tasks[-limit:] if limit else tasks

    def search_tasks(self, query: str):
        query = query.lower()
        tasks = self.data.get("task_history", [])
        return [
            t
            for t in tasks
            if query in t.get("task", "").lower()
            or query in t.get("details", "").lower()
        ]

    def get_agency_info(self):
        return self.data.get("agency_info", {})

    def update_agency_info(self, **kwargs):
        if "agency_info" not in self.data:
            self.data["agency_info"] = {}
        self.data["agency_info"].update(kwargs)
        self.data["updated_at"] = datetime.now().isoformat()
        self._save_data()

    def get_service_areas(self):
        return self.data.get("service_areas", {})

    def get_projects(self):
        return self.data.get("projects", [])

    def get_services(self):
        return self.data.get("services", [])

    def get_payment_info(self):
        return self.data.get("payment_info", {})


def main():
    import sys

    tracker = TaskHistory()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "add":
            task = sys.argv[2] if len(sys.argv) > 2 else "New task"
            details = sys.argv[3] if len(sys.argv) > 3 else ""
            result = tracker.add_task(task, details)
            print(f"Task added: {result}")

        elif command == "list":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            tasks = tracker.get_tasks(limit)
            print("\n=== Task History ===")
            for t in reversed(tasks):
                print(f"[{t['date']}] {t['task']}")
                if t.get("details"):
                    print(f"   {t['details']}")
                print()

        elif command == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            results = tracker.search_tasks(query)
            print(f"Found {len(results)} tasks:")
            for t in results:
                print(f"[{t['date']}] {t['task']}")

        elif command == "info":
            info = tracker.get_agency_info()
            print(json.dumps(info, indent=2))

        elif command == "projects":
            projects = tracker.get_projects()
            print(json.dumps(projects, indent=2))

        elif command == "services":
            services = tracker.get_services()
            print(json.dumps(services, indent=2))

        else:
            print("Commands:")
            print("  python task_history.py add <task> [details]")
            print("  python task_history.py list [limit]")
            print("  python task_history.py search <query>")
            print("  python task_history.py info")
            print("  python task_history.py projects")
            print("  python task_history.py services")
    else:
        tasks = tracker.get_tasks(5)
        print("=== Recent Tasks ===")
        for t in reversed(tasks):
            print(f"[{t['date']}] {t['task']}")


if __name__ == "__main__":
    main()
