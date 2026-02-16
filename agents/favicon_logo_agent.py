#!/usr/bin/env python3
"""
AGENT: Favicon & Logo Manager
=============================
Brief: Manages and fixes all favicon and logo issues for the website

RESPONSIBILITIES:
1. Ensure favicon displays correctly in browser tabs
2. Ensure logo displays correctly on website header
3. Optimize logo/favicon sizes for web
4. Fix broken image references in HTML
5. Verify logo appears on all pages

TROUBLESHOOTING:
- If favicon not showing: Check file path in HTML <link rel="icon">
- If logo broken: Verify logo.png exists in website folder
- Clear browser cache after changes (Ctrl+Shift+R)
- GitHub Pages may take 1-2 minutes to update

FILES:
- Source: /home/ev/Documents/Evans Mathibe/Evans mathibe Images and Videos and logo/Evans mathibe Logo.jpeg
- Output: /home/ev/EvansMathibe_Agency/website/logo.png
- Favicon: /home/ev/EvansMathibe_Agency/website/favicon.png

CHECKLIST:
□ favicon.png exists in website folder
□ logo.png exists in website folder
□ HTML has <link rel="icon" href="favicon.png">
□ HTML has <img src="logo.png"> for header logo
□ Browser cache cleared
□ GitHub Pages updated (wait 2 mins)
"""

import os
import json
from pathlib import Path
from PIL import Image

SOURCE_LOGO = "/home/ev/Documents/Evans Mathibe/Evans mathibe Images and Videos and logo/Evans mathibe Logo.jpeg"
WEBSITE_DIR = Path(__file__).parent.parent / "website"


def check_status():
    """Check logo/favicon status"""
    results = {
        "logo_png_exists": (WEBSITE_DIR / "logo.png").exists(),
        "favicon_png_exists": (WEBSITE_DIR / "favicon.png").exists(),
        "source_exists": os.path.exists(SOURCE_LOGO),
    }

    if results["logo_png_exists"]:
        img = Image.open(WEBSITE_DIR / "logo.png")
        results["logo_size"] = img.size

    if results["favicon_png_exists"]:
        img = Image.open(WEBSITE_DIR / "favicon.png")
        results["favicon_size"] = img.size

    return results


def fix_favicon():
    """Ensure favicon is properly set up"""
    issues = []

    # Check favicon exists
    if not (WEBSITE_DIR / "favicon.png").exists():
        issues.append("favicon.png missing")

    # Check HTML reference
    html_file = WEBSITE_DIR / "index.html"
    with open(html_file) as f:
        content = f.read()

    if 'href="favicon.png"' not in content:
        issues.append("HTML missing favicon reference")

    if 'src="logo.png"' not in content:
        issues.append("HTML missing logo reference")

    return issues


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print(json.dumps(check_status(), indent=2))
        elif sys.argv[1] == "fix":
            issues = fix_favicon()
            if issues:
                print("Issues found:", issues)
            else:
                print("All checks passed!")
    else:
        print(json.dumps(check_status(), indent=2))
