#!/usr/bin/env python3
"""
EvansMathibe Automation System
=============================
Master automation script that runs all tasks automatically

CRON SETUP:
-----------
# Add to crontab (run: crontab -e)

# Daily at 9 AM - Check and send analytics
0 9 * * * cd /home/ev/EvansMathibe_Agency && python3 scripts/auto_run.py analytics

# Weekly on Monday at 8 AM - Full system check
0 8 * * 1 cd /home/ev/EvansMathibe_Agency && python3 scripts/auto_run.py full-check

# Monthly on 1st at 9 AM - Backup and deploy
0 9 1 * * cd /home/ev/EvansMathibe_Agency && python3 scripts/auto_run.py backup

USAGE:
------
python3 scripts/auto_run.py [command]

COMMANDS:
---------
analytics    - Send analytics report (if 3+ days since last)
full-check   - Run all fix agents, check statuses
backup       - Backup data, commit to git, deploy
deploy       - Quick deploy to GitHub Pages
status       - Show all system statuses
"""
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def log(message):
    """Log with timestamp"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {message}")

def run_command(cmd, cwd=None):
    """Run shell command"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60,
            cwd=cwd or BASE_DIR
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def run_analytics():
    """Run analytics and send notification if due"""
    log("Running analytics...")
    
    # Check last notification
    analytics_file = DATA_DIR / "website_analytics.json"
    if analytics_file.exists():
        with open(analytics_file) as f:
            data = json.load(f)
            notifications = data.get("notifications", [])
            
            if notifications:
                last = datetime.fromisoformat(notifications[-1]["timestamp"])
                if (datetime.now() - last).days < 3:
                    log(f"Analytics notification sent { (datetime.now() - last).days } days ago. Skipping.")
                    return
    
    # Run analytics agent
    success, output = run_command("python3 agents/analytics_agent.py notify")
    if success:
        log("Analytics notification sent!")
    else:
        log(f"Analytics: {output}")

def run_full_check():
    """Run full system check"""
    log("Running full system check...")
    
    checks = {
        "git_status": False,
        "website_exists": False,
        "data_exists": False,
        "agents_exist": False
    }
    
    # Check git
    success, _ = run_command("git status")
    checks["git_status"] = success
    
    # Check website
    checks["website_exists"] = (BASE_DIR / "website" / "index.html").exists()
    
    # Check data
    checks["data_exists"] = (DATA_DIR / "agency_data.json").exists()
    
    # Check agents
    checks["agents_exist"] = (BASE_DIR / "agents").exists()
    
    log(f"Status: {json.dumps(checks, indent=2)}")
    
    # Try deploying if on main branch
    success, output = run_command("git branch --show-current")
    if success and "main" in output or "deploy" in output:
        log("Deploying to GitHub Pages...")
        run_command("git add -A")
        run_command('git commit -m "Auto-update: ' + datetime.now().strftime('%Y-%m-%d') + '"')
        run_command("git push origin main")
        log("Deployed!")

def run_backup():
    """Backup data and deploy"""
    log("Running backup and deploy...")
    
    # Create backup
    backup_file = DATA_DIR / f"backup_{datetime.now().strftime('%Y%m%d')}.json"
    
    # Copy data
    import shutil
    if (DATA_DIR / "agency_data.json").exists():
        shutil.copy(DATA_DIR / "agency_data.json", backup_file)
        log(f"Backup created: {backup_file}")
    
    # Deploy
    log("Deploying to GitHub...")
    run_command("git add -A")
    run_command(f'git commit -m "Auto backup: {datetime.now().strftime(\'%Y-%m-%d\')}"')
    run_command("git push origin deploy-gh-pages")
    log("Backup and deploy complete!")

def run_deploy():
    """Quick deploy"""
    log("Deploying to GitHub Pages...")
    run_command("git add -A")
    run_command(f'git commit -m "Update: {datetime.now().strftime(\'%Y-%m-%d %H:%M\')}"')
    success, out = run_command("git push origin deploy-gh-pages")
    if success:
        log("Deployed successfully!")
    else:
        log(f"Deploy failed: {out}")

def show_status():
    """Show all statuses"""
    log("Checking system status...")
    
    # Git status
    success, output = run_command("git status --short")
    git_status = output if success else "Error"
    
    # Files
    files = {
        "website": (BASE_DIR / "website" / "index.html").exists(),
        "data": (DATA_DIR / "agency_data.json").exists(),
        "analytics": (DATA_DIR / "website_analytics.json").exists(),
        "agents": len(list((BASE_DIR / "agents").glob("*.py"))) if (BASE_DIR / "agents").exists() else 0
    }
    
    print(f"""
========================================
EVANSMATHIBE SYSTEM STATUS
========================================
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Git Status:
{git_status}

Files:
{json.dumps(files, indent=2)}

Website: https://evansxm.github.io/evansmathibe-agency/
GitHub:  https://github.com/Evansxm/evansmathibe-agency
========================================
""")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "analytics":
            run_analytics()
        elif cmd == "full-check":
            run_full_check()
        elif cmd == "backup":
            run_backup()
        elif cmd == "deploy":
            run_deploy()
        elif cmd == "status":
            show_status()
        else:
            print(__doc__)
    else:
        show_status()
