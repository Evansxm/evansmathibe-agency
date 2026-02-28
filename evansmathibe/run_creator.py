#!/usr/bin/env python3
"""
Google Sites Creator - Fully Automated with Credentials
Usage:
  Set credentials in config or pass as arguments
  python3 run_creator.py --email "your@email" --password "yourpass"
"""

import os
import sys
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class GoogleSitesCreator:
    def __init__(self, email, password, headless=True):
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = None
        self.site_url = None
        self.chrome_path = (
            "/home/ev/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
        )

    def setup(self):
        """Setup browser"""
        print("🔧 Setting up browser...")

        opts = Options()
        opts.binary_location = self.chrome_path
        if self.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(10)
        print("✅ Browser ready!")
        return True

    def wait(self, secs=2):
        time.sleep(secs)

    def find_click(self, by, value):
        """Find and click"""
        try:
            elem = self.driver.find_element(by, value)
            elem.click()
            return True
        except:
            return False

    def find_type(self, by, value, text):
        """Find and type"""
        try:
            elem = self.driver.find_element(by, value)
            elem.clear()
            elem.send_keys(text)
            return True
        except:
            return False

    def run(self):
        """Run full automation"""
        if not self.setup():
            return False

        try:
            # Step 1: Go to Google
            print("\n📍 Step 1: Going to Google...")
            self.driver.get("https://www.google.com")
            self.wait(2)

            # Step 2: Login
            print(f"\n🔐 Step 2: Logging in as {self.email}...")
            self.driver.get("https://accounts.google.com")
            self.wait(3)

            # Enter email
            self.find_type(By.NAME, "identifier", self.email)
            self.find_click(By.ID, "identifierNext")
            self.wait(3)

            # Enter password
            self.find_type(By.NAME, "Passwd", self.password)
            self.find_click(By.ID, "passwordNext")
            self.wait(5)
            print("   ✅ Logged in!")

            # Step 3: Go to Google Sites
            print("\n🏗️ Step 3: Creating site...")
            self.driver.get("https://sites.google.com")
            self.wait(4)

            # Click Create
            self.find_click(By.XPATH, "//button[contains(text(),'Create')]")
            self.wait(3)

            # Enter site name
            self.find_type(
                By.XPATH, "//input[@placeholder='Enter a site name']", "Evans Mathibe"
            )
            self.wait(1)

            # Click Create
            self.find_click(By.XPATH, "//button[contains(text(),'Create')]")
            self.wait(5)

            print("   ✅ Site created!")

            # Get editor URL
            editor_url = self.driver.current_url
            print(f"   📝 Editor: {editor_url}")

            # Save state
            with open("/home/ev/evansmathibe/site_state.json", "w") as f:
                import json

                json.dump(
                    {
                        "status": "created",
                        "editor_url": editor_url,
                        "email": self.email,
                    },
                    f,
                )

            print(f"\n✅ SUCCESS! Site created.")
            print(f"   Editor URL: {editor_url}")

            # Keep browser open for user to complete
            print("\n⏸️ Browser open for manual completion...")
            print("Complete the remaining steps in the browser, then close.")
            input("Press Enter to close...")

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Create Google Site")
    parser.add_argument("--email", required=True, help="Google email")
    parser.add_argument("--password", required=True, help="Google password")
    parser.add_argument(
        "--visible", action="store_true", help="Show browser (not headless)"
    )

    args = parser.parse_args()

    creator = GoogleSitesCreator(args.email, args.password, headless=not args.visible)
    creator.run()


if __name__ == "__main__":
    main()
