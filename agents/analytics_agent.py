#!/usr/bin/env python3
"""
EvansMathibe Analytics Agent
Runs locally to collect and analyze website analytics
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

DATA_DIR = Path(__file__).parent / "data"
ANALYTICS_FILE = DATA_DIR / "website_analytics.json"


class WebsiteAnalytics:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """Load existing analytics data"""
        if ANALYTICS_FILE.exists():
            with open(ANALYTICS_FILE, "r") as f:
                return json.load(f)
        return {"visits": [], "pages": {}, "devices": [], "notifications": []}

    def save_data(self):
        """Save analytics data"""
        with open(ANALYTICS_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def record_visit(self, visit_data):
        """Record a new visit from website"""
        visit = {
            "timestamp": datetime.now().isoformat(),
            "page": visit_data.get("page", "unknown"),
            "referrer": visit_data.get("referrer", "direct"),
            "device": visit_data.get("device", "unknown"),
            "browser": visit_data.get("browser", "unknown"),
            "duration": visit_data.get("duration", 0),
            "country": visit_data.get("country", "unknown"),
            "city": visit_data.get("city", "unknown"),
        }
        self.data["visits"].append(visit)

        # Track page views
        page = visit["page"]
        if page not in self.data["pages"]:
            self.data["pages"][page] = {"views": 0, "total_duration": 0, "visits": []}
        self.data["pages"][page]["views"] += 1
        self.data["pages"][page]["total_duration"] += visit["duration"]

        # Track devices
        self.data["devices"].append(visit["device"])

        self.save_data()
        return visit

    def get_stats(self, days=7):
        """Get statistics for last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_visits = [
            v
            for v in self.data["visits"]
            if datetime.fromisoformat(v["timestamp"]) > cutoff
        ]

        if not recent_visits:
            return {
                "total_visits": 0,
                "message": "No visits in the last {} days".format(days),
            }

        # Calculate stats
        total_visits = len(recent_visits)
        unique_visitors = len(set([v.get("session", "unknown") for v in recent_visits]))

        # Pages
        page_counts = Counter([v["page"] for v in recent_visits])

        # Devices
        device_counts = Counter([v["device"] for v in recent_visits])

        # Average duration
        durations = [v["duration"] for v in recent_visits if v["duration"] > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_visits": total_visits,
            "unique_visitors": unique_visitors,
            "top_pages": dict(page_counts.most_common(5)),
            "devices": dict(device_counts),
            "avg_duration_seconds": round(avg_duration, 1),
            "period_days": days,
        }

    def should_notify(self):
        """Check if notification should be sent (every 3 days)"""
        notifications = self.data.get("notifications", [])

        if not notifications:
            return True

        last_notification = datetime.fromisoformat(notifications[-1]["timestamp"])
        days_since = (datetime.now() - last_notification).days

        return days_since >= 3

    def send_notification(self):
        """Generate notification email"""
        stats = self.get_stats(days=3)

        # Generate email content
        subject = (
            f"📊 EvansMathibe Website Analytics - {datetime.now().strftime('%Y-%m-%d')}"
        )

        body = f"""📊 Website Analytics Report - Last 3 Days
========================================

Total Visits: {stats.get("total_visits", 0)}
Unique Visitors: {stats.get("unique_visitors", 0)}
Average Time on Site: {stats.get("avg_duration_seconds", 0)} seconds

📍 Top Pages:
"""
        for page, count in stats.get("top_pages", {}).items():
            body += f"  - {page}: {count} views\n"

        body += "\n📱 Devices:\n"
        for device, count in stats.get("devices", {}).items():
            body += f"  - {device}: {count}\n"

        body += f"""
🌐 View Full Dashboard:
https://evansxm.github.io/evansmathibe-agency/

---
Automated from EvansMathibe Analytics System
"""

        # Record notification
        self.data.setdefault("notifications", []).append(
            {"timestamp": datetime.now().isoformat(), "stats": stats}
        )
        self.save_data()

        return subject, body

    def generate_dashboard_link(self):
        """Generate mailto link for notification"""
        subject, body = self.send_notification()
        encoded_subject = __import__("urllib.parse").quote(subject)
        encoded_body = __import__("urllib.parse").quote(body)
        return f"mailto:evans.mathibe@mail.com?subject={encoded_subject}&body={encoded_body}"


if __name__ == "__main__":
    import sys

    analytics = WebsiteAnalytics()

    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            print(json.dumps(analytics.get_stats(days), indent=2))
        elif sys.argv[1] == "notify":
            if analytics.should_notify():
                link = analytics.generate_dashboard_link()
                print("Notification ready! Mailto link:")
                print(link)
            else:
                print(
                    "Notification already sent recently. Next notification in 3 days."
                )
        elif sys.argv[1] == "record" and len(sys.argv) > 2:
            data = json.loads(sys.argv[2])
            analytics.record_visit(data)
            print("Visit recorded!")
        else:
            print("Usage: analytics_agent.py [stats [days]|notify|record <json_data>]")
    else:
        print(json.dumps(analytics.get_stats(7), indent=2))
