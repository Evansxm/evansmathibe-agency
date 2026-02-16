#!/usr/bin/env python3
"""
EvansMathibe Logo Agent
Handles logo optimization, sizing, and deployment
"""

import os
import json
from pathlib import Path
from PIL import Image

SOURCE_LOGO = "/home/ev/Documents/Evans Mathibe/Evans mathibe Images and Videos and logo/Evans mathibe Logo.jpeg"
TARGET_DIR = Path(__file__).parent.parent / "website"

LOGO_SIZES = {"favicon": (32, 32), "logo": (150, 150), "social": (200, 200)}


def get_logo():
    """Get current logo path"""
    return TARGET_DIR / "logo.png"


def optimize_logo(source=SOURCE_LOGO):
    """Optimize logo for web"""
    if not os.path.exists(source):
        print(f"Source logo not found: {source}")
        return False

    try:
        img = Image.open(source)
        if img.mode == "RGBA":
            pass  # Keep transparency
        elif img.mode == "P":
            img = img.convert("RGBA")

        # Save main logo
        img.thumbnail(LOGO_SIZES["logo"], Image.LANCZOS)
        img.save(TARGET_DIR / "logo.png", "PNG", optimize=True)
        print(f"Logo saved: {TARGET_DIR / 'logo.png'}")

        # Save favicon
        favicon = Image.open(source)
        if favicon.mode != "RGBA":
            favicon = favicon.convert("RGBA")
        favicon.thumbnail(LOGO_SIZES["favicon"], Image.LANCZOS)
        favicon.save(TARGET_DIR / "favicon.png", "PNG", optimize=True)
        print(f"Favicon saved: {TARGET_DIR / 'favicon.png'}")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def check_logo_status():
    """Check if logos exist and their status"""
    logo = get_logo()
    favicon = TARGET_DIR / "favicon.png"

    status = {
        "logo_exists": logo.exists(),
        "favicon_exists": favicon.exists(),
        "logo_path": str(logo),
        "source_path": SOURCE_LOGO,
    }

    if logo.exists():
        img = Image.open(logo)
        status["logo_size"] = img.size

    return status


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print(json.dumps(check_logo_status(), indent=2))
        elif sys.argv[1] == "optimize":
            optimize_logo()
        else:
            print("Usage: logo_agent.py [status|optimize]")
    else:
        print(json.dumps(check_logo_status(), indent=2))
