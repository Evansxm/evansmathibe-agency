#!/usr/bin/env python3
"""
Analytics Notification Scheduler
Runs every day to check if 3-day notification is due
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.analytics_agent import WebsiteAnalytics


def check_and_notify():
    """Check if notification is due and send"""
    analytics = WebsiteAnalytics()

    if analytics.should_notify():
        print(
            f"📊 Sending analytics notification ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        )

        # Get stats
        stats = analytics.get_stats(days=3)

        # Generate email
        subject, body = analytics.send_notification()

        # Open email client
        encoded_subject = __import__("urllib.parse").quote(subject)
        encoded_body = __import__("urllib.parse").quote(body)
        mailto = f"mailto:evans.mathibe@mail.com?subject={encoded_subject}&body={encoded_body}"

        try:
            subprocess.run(["xdg-open", mailto], timeout=10)
            print("✅ Notification sent!")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            # Print the email content instead
            print("\n" + "=" * 50)
            print("EMAIL CONTENT:")
            print("=" * 50)
            print(f"To: evans.mathibe@mail.com")
            print(f"Subject: {subject}")
            print("\nBody:")
            print(body)
            return False
    else:
        days_since = (
            datetime.now()
            - datetime.fromisoformat(
                analytics.data.get("notifications", [{}])[-1].get(
                    "timestamp", datetime.now().isoformat()
                )
            )
        ).days
        print(f"⏳ Next notification in {3 - days_since} days")
        return False


def setup_cron():
    """Setup cron job for daily check"""
    cron_entry = (
        f"0 9 * * * cd {Path(__file__).parent} && python3 {Path(__file__).name} run\n"
    )

    print("To enable daily notifications, add this to your crontab:")
    print(f"  {cron_entry}")
    print("\nTo add, run: crontab -e")
    print("And add the line above.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        check_and_notify()
    elif len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_cron()
    else:
        print("Usage:")
        print("  python3 scheduler.py run        - Check and send notification")
        print("  python3 scheduler.py setup       - Show cron setup instructions")
        print("\nFor automatic scheduling, run: python3 scheduler.py setup")
