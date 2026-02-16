#!/usr/bin/env python3
"""
EvansMathibe Context Manager
A contingency system to remember important context between sessions.
"""

import json
import os
from datetime import datetime
from pathlib import Path

CONTEXT_FILE = Path(__file__).parent / "data" / "user_context.json"


def load_context():
    """Load existing context from JSON file"""
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_context(data):
    """Save context to JSON file (compressed)"""
    with open(CONTEXT_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_reminder(reminder_text):
    """Add a reminder to the context"""
    context = load_context()
    if "reminders" not in context:
        context["reminders"] = []
    context["reminders"].append(
        {"text": reminder_text, "created": datetime.now().isoformat()}
    )
    save_context(context)


def get_important_info():
    """Quick access to most important info"""
    context = load_context()
    return {
        "github": context.get("user_info", {}).get("github_username"),
        "repo": context.get("current_project", {}).get("github_url"),
        "website": context.get("current_project", {}).get("live_url"),
        "email": context.get("user_info", {}).get("email"),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "info":
            info = get_important_info()
            print(json.dumps(info, indent=2))
        elif sys.argv[1] == "remind" and len(sys.argv) > 2:
            add_reminder(" ".join(sys.argv[2:]))
            print("Reminder added!")
        else:
            context = load_context()
            print(json.dumps(context, indent=2))
    else:
        print("Usage: context_manager.py [info|remind <text>]")
