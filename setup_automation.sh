#!/bin/bash
# EvansMathibe Automation Setup
# Run this to set up automatic tasks

echo "Setting up EvansMathibe automation..."

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create cron entries
CRON_ENTRIES="
# EvansMathibe Analytics - Daily at 9 AM
0 9 * * * cd $PROJECT_DIR && python3 scripts/auto_run.py analytics

# EvansMathibe Full Check - Weekly on Monday at 8 AM
0 8 * * 1 cd $PROJECT_DIR && python3 scripts/auto_run.py full-check

# EvansMathibe Backup - Monthly on 1st at 9 AM
0 9 1 * * cd $PROJECT_DIR && python3 scripts/auto_run.py backup
"

# Check if cron exists
if command -v crontab &> /dev/null; then
    echo "$CRON_ENTRIES" | crontab -
    echo "Cron jobs installed!"
    echo ""
    echo "Your scheduled tasks:"
    crontab -l | grep EvansMathibe
else
    echo "Crontab not found. To set up manually, add these lines to your crontab:"
    echo "$CRON_ENTRIES"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Quick commands:"
echo "  python3 scripts/auto_run.py status      - Check system status"
echo "  python3 scripts/auto_run.py deploy      - Deploy to GitHub"
echo "  python3 scripts/auto_run.py analytics   - Send analytics"
echo "  python3 scripts/auto_run.py full-check  - Run all checks"
