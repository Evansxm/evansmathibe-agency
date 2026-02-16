#!/usr/bin/env python3
"""
AGENT: Google Business Profile Manager
=====================================
Brief: Manages and syncs Google Business Profile for EvansMathibe Agency

RESPONSIBILITIES:
1. Track Google Business Profile URL and status
2. Sync business info (name, address, phone, hours, photos)
3. Add new photos/posts to GBP
4. Monitor reviews and respond
5. Update business info when website changes

GBP PROFILE INFO:
- Name: EvansMathibe Agency
- URL: https://business.google.com/locations (managed account)
- Email: evans.mathibe@mail.com
- Phone: +27 72 416 5061
- Location: South Africa (Gauteng)

UPDATES NEEDED ON GBP:
□ Website URL: https://evansxm.github.io/evansmathibe-agency/
□ Services: Photography, Film, Advertising, AI Brand Automation, etc.
□ Photos: Add latest work gallery images
□ Description: Update to reflect current services
□ Hours: Update business hours
□ TYC Project: Add as upcoming project/post

HOW TO UPDATE GBP MANUALLY:
1. Go to: https://business.google.com/locations
2. Sign in with: evansmathibe82@gmail.com
3. Select EvansMathibe Agency
4. Edit each section:
   - Info: Name, address, phone, website
   - Photos: Upload new gallery images
   - Posts: Add updates about TYC project
   - Services: List all 12 services

AUTOMATION OPTIONS:
- Use Google My Business API (requires verification)
- Use third-party tools like Birdeye, Podium
- Manual updates recommended for accuracy

FILES:
- Data: /home/ev/EvansMathibe_Agency/data/agency_data.json
- Website: /home/ev/EvansMathibe_Agency/website/index.html

CHECKLIST:
□ Verify GBP account access
□ Update website URL to new GitHub Pages link
□ Add all 12 services to GBP
□ Upload portfolio photos
□ Add TYC project as post
□ Enable messaging feature
□ Set business hours
"""

import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent.parent / "data" / "agency_data.json"


def load_data():
    """Load agency data"""
    with open(DATA_FILE) as f:
        return json.load(f)


def get_gbp_info():
    """Get current GBP info"""
    data = load_data()
    return {
        "name": data["agency_info"]["name"],
        "email": data["agency_info"]["email"],
        "phone": data["agency_info"]["phone"],
        "whatsapp": data["agency_info"]["whatsapp"],
        "google_business": data["agency_info"]["google_business"],
        "website": data["agency_info"]["website"],
    }


def check_updates_needed():
    """Check what needs updating on GBP"""
    data = load_data()
    issues = []

    # Check website URL
    if (
        data["agency_info"]["website"]
        != "https://evansxm.github.io/evansmathibe-agency/"
    ):
        issues.append("Website URL needs update")

    # Check social media
    social = data["agency_info"]["social_media"]
    if not any(social.values()):
        issues.append("No social media links set")

    return {
        "issues": issues,
        "gbp_url": data["agency_info"]["google_business"],
        "last_updated": data.get("updated_at", "Unknown"),
    }


def generate_update_report():
    """Generate report of what to update on GBP"""
    services = load_data()["services"]

    report = f"""
GBP UPDATE REPORT - {datetime.now().strftime("%Y-%m-%d")}
{"=" * 50}

PROFILE INFO:
- Business Name: EvansMathibe Agency
- Phone: +27 72 416 5061
- Email: evans.mathibe@mail.com
- Website: https://evansxm.github.io/evansmathibe-agency/

SERVICES TO ADD (12 total):
"""
    for s in services:
        report += f"  - {s['name']}\n"

    report += """
POSTS TO ADD:
  1. TYC Project announcement
  2. New service offerings
  3. Portfolio highlights

PHOTOS TO UPLOAD:
  - Use images from /home/ev/EvansMathibe_Agency/website/images/

LINKS:
  - GBP Dashboard: https://business.google.com/locations
  - Direct Link: https://business.google.com/en-all/business-profile/?ppsrc=GPDA2
"""
    return report


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "info":
            print(json.dumps(get_gbp_info(), indent=2))
        elif sys.argv[1] == "check":
            print(json.dumps(check_updates_needed(), indent=2))
        elif sys.argv[1] == "report":
            print(generate_update_report())
    else:
        print(json.dumps(get_gbp_info(), indent=2))
