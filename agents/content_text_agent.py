#!/usr/bin/env python3
"""
AGENT: Content Text Manager
===========================
Brief: Manages and removes unwanted text from the website

RESPONSIBILITIES:
1. Remove "Premier Creative Agency" from all pages
2. Remove any tagline that says "Premier"
3. Ensure hero section has clean, minimal text
4. Update meta descriptions for SEO
5. Check all text content for unwanted phrases

UNWANTED PHRASES TO REMOVE:
- "Premier Creative Agency"
- "Premier Creative Agency South Africa"
- Any variation with "Premier"

REPLACEMENT OPTIONS:
- "Leading Creative Agency"
- "Top Creative Agency"
- "South Africa's Leading Creative Agency"
- Just remove entirely

FILES:
- Main: /home/ev/EvansMathibe_Agency/website/index.html
- Check: grep -r "Premier" website/

CHECKLIST:
□ Search entire website for "Premier"
□ Replace with appropriate alternative or remove
□ Update hero badge text
□ Update footer text
□ Update meta description if needed
□ Test all pages after changes
"""

import json
import re
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent.parent / "website"


def find_premier_text():
    """Find all instances of Premier text"""
    html_file = WEBSITE_DIR / "index.html"
    content = html_file.read_text()

    matches = []
    for i, line in enumerate(content.split("\n"), 1):
        if "premier" in line.lower():
            matches.append({"line": i, "text": line.strip()[:100]})

    return matches


def remove_premier():
    """Remove premier text from website"""
    html_file = WEBSITE_DIR / "index.html"
    content = html_file.read_text()

    # Replace variations
    replacements = [
        ("Premier Creative Agency South Africa", "Leading Creative Agency"),
        ("Premier Creative Agency", "Leading Creative Agency"),
        ("premier creative agency", "leading creative agency"),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    # Write back
    html_file.write_text(content)

    return f"Replaced {len(replacements)} patterns"


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "find":
            print(json.dumps(find_premier_text(), indent=2))
        elif sys.argv[1] == "remove":
            result = remove_premier()
            print(result)
        elif sys.argv[1] == "check":
            matches = find_premier_text()
            if matches:
                print(f"Found {len(matches)} instances:")
                print(json.dumps(matches, indent=2))
            else:
                print("No 'Premier' text found - clean!")
    else:
        print(json.dumps(find_premier_text(), indent=2))
