#!/usr/bin/env python3
"""
Google Sites Creator - Semi-Automated Version
Opens browser and guides you through creation step by step
"""

import subprocess
import time
import os


def open_google_sites():
    """Open Google Sites in browser"""
    print("=" * 60)
    print("GOOGLE SITES CREATION - Evans Mathibe Portfolio")
    print("=" * 60)

    # Open Google Sites
    print("\nOpening Google Sites in your browser...")
    subprocess.Popen(["google-chrome", "https://sites.google.com"])
    time.sleep(2)

    print("""
INSTRUCTIONS - Follow these steps:

STEP 1: CREATE NEW SITE
-------------------------
• Click the + button or "Create new site"
• Choose "Blank" template (or any you like)
• Site name: "Evans Mathibe" or "Evans Mathibe Portfolio"

STEP 2: EDIT HOME PAGE
------------------------
In the editor:
1. Click "Edit" (pencil icon)
2. Change header to: "Hi, I'm Evans Mathibe"
3. Add subtitle: "Professional | Visionary | Leader"
4. Add a text box with: "Building the future through innovation and dedication"
5. Add 2 buttons: "Get In Touch" and "Learn More"

STEP 3: ADD PAGES
------------------
Click "Pages" (left sidebar) > "+ Add page"

Create these pages:
• About - Full bio + stats
• Services - 6 service cards  
• Experience - Timeline
• Testimonials - Client quotes
• Gallery - Images
• Contact - Contact info + form

STEP 4: ADD CONTENT
--------------------
Use content from: /home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md

STEP 5: CUSTOMIZE
------------------
• Click "Themes" (paintbrush icon)
• Choose a professional theme
• Colors: Dark blue (#1a1a2e), accent red (#e94560)

STEP 6: PUBLISH
----------------
• Click "Publish" (top right)
• Set custom URL: evansmathibe.site

STEP 7: ADD GOOGLE FORMS
--------------------------
• Go to forms.google.com
• Create contact form
• Embed in Contact page: Insert > Embed > Embed code

STEP 8: ADD MAP
---------------
• Insert > Maps
• Search: Gauteng, South Africa

""")

    input("\nPress ENTER when you've completed all steps...")

    print("\n" + "=" * 60)
    print("WEBSITE CREATION COMPLETE!")
    print("=" * 60)
    print("""
Your site is now live at: evansmathibe.site

Don't forget to:
• Upload images to site (from evansmathibe/assets/)
• Test mobile view
• Add SEO description in Site Settings
• Share on social media
    """)


if __name__ == "__main__":
    open_google_sites()
