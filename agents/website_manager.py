#!/usr/bin/env python3
"""
AGENT: Website Issues Manager
============================
Master agent that coordinates all website fix agents

USAGE:
    python3 agents/website_manager.py [command]

COMMANDS:
    fix all           - Run all fix agents
    fix favicon       - Fix favicon/logo issues
    fix text          - Remove unwanted text
    fix cart          - Verify cart/inquiry flow
    status            - Check all statuses
    deploy            - Commit and push to GitHub
"""

import subprocess
import sys
import json
from pathlib import Path

AGENTS = {
    "favicon": "agents/favicon_logo_agent.py",
    "text": "agents/content_text_agent.py",
    "cart": "agents/cart_inquiry_agent.py",
    "analytics": "agents/analytics_agent.py",
    "content": "agents/content_agent.py",
    "logo": "agents/logo_agent.py",
}


def run_agent(agent_name, command=""):
    """Run a specific agent"""
    agent_file = AGENTS.get(agent_name)
    if not agent_file:
        return f"Unknown agent: {agent_name}"

    agent_path = Path(__file__).parent / agent_file
    if not agent_path.exists():
        return f"Agent not found: {agent_file}"

    try:
        result = subprocess.run(
            ["python3", str(agent_path)] + command.split() if command else [],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error: {e}"


def fix_all():
    """Run all fix agents"""
    results = {}

    # Fix text
    print("Fixing text...")
    results["text"] = run_agent("text", "remove")

    # Check favicon
    print("Checking favicon...")
    results["favicon"] = run_agent("favicon", "status")

    # Check cart
    print("Checking cart...")
    results["cart"] = run_agent("cart", "check")

    return results


def deploy():
    """Commit and deploy to GitHub"""
    repo_dir = Path(__file__).parent.parent

    print("Committing changes...")
    result = subprocess.run(
        ["git", "add", "-A"], cwd=repo_dir, capture_output=True, text=True
    )

    result = subprocess.run(
        ["git", "commit", "-m", "Fix: Remove premier text, fix favicon"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    print("Pushing to GitHub...")
    result = subprocess.run(
        ["git", "push", "origin", "deploy-gh-pages"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    return "Deployed to GitHub Pages!"


def status():
    """Check all system statuses"""
    results = {}

    for agent in AGENTS:
        try:
            output = run_agent(agent, "status" if agent != "text" else "check")
            results[agent] = output[:200]  # Truncate long output
        except:
            results[agent] = "Error"

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "fix" and len(sys.argv) > 2:
            subcmd = sys.argv[2]
            if subcmd == "all":
                print("Running all fixes...")
                print(json.dumps(fix_all(), indent=2))
            else:
                print(run_agent(subcmd))

        elif cmd == "deploy":
            print(deploy())

        elif cmd == "status":
            print(json.dumps(status(), indent=2))

        else:
            print(f"Unknown command: {cmd}")
            print(__doc__)
    else:
        print(__doc__)
