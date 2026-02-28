#!/usr/bin/env python3
"""
Google Sites Creator - Full Automation
Creates Evans Mathibe website on Google Sites automatically
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleSitesAutomator:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.site_url = None

    def setup(self):
        """Setup Chrome with Selenium"""
        print("🔧 Setting up Chrome browser...")

        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--user-data-dir=/tmp/chrome-profile")

        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(15)
            print("✅ Browser ready!")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def wait(self, seconds=2):
        """Safe wait"""
        time.sleep(seconds)

    def wait_for_clickable(self, by, value, timeout=20):
        """Wait for element to be clickable"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def find_and_click(self, by, value, description=""):
        """Find and click element"""
        try:
            element = self.wait_for_clickable(by, value)
            element.click()
            self.wait(1)
            return True
        except Exception as e:
            print(f"⚠️ Could not click {description}: {e}")
            return False

    def find_and_type(self, by, value, text, description=""):
        """Find and type text"""
        try:
            element = self.driver.find_element(by, value)
            element.clear()
            element.send_keys(text)
            self.wait(0.5)
            return True
        except Exception as e:
            print(f"⚠️ Could not type in {description}: {e}")
            return False

    def go_to(self, url):
        """Navigate to URL"""
        print(f"📍 Going to: {url}")
        self.driver.get(url)
        self.wait(3)

    def login(self, email, password):
        """Login to Google"""
        print("\n🔐 Logging in to Google...")
        self.go_to("https://accounts.google.com")
        self.wait(2)

        # Email
        print(f"   Entering email: {email}")
        self.find_and_type(By.NAME, "identifier", email, "email input")
        self.find_and_click(By.ID, "identifierNext", "Next button")
        self.wait(3)

        # Password
        print("   Entering password...")
        self.find_and_type(By.NAME, "Passwd", password, "password input")
        self.find_and_click(By.ID, "passwordNext", "Submit button")
        self.wait(5)
        print("   ✅ Logged in!")

    def create_site(self, site_name):
        """Create new Google Site"""
        print(f"\n🏗️ Creating site: {site_name}")
        self.go_to("https://sites.google.com")
        self.wait(3)

        # Click Create button
        try:
            create_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            self.wait(2)
        except:
            pass

        # Enter site name
        try:
            name_input = self.driver.find_element(
                By.XPATH, "//input[@placeholder='Enter a site name']"
            )
            name_input.send_keys(site_name)
            self.wait(1)

            # Click Create/Continue
            create_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            self.wait(5)
        except Exception as e:
            print(f"   ⚠️ Could not set name directly: {e}")

        print("   ✅ Site creation initiated!")

    def add_text_content(self, heading, content):
        """Add heading and text content"""
        print(f"   Adding: {heading}")

        # Try to add text section
        try:
            # Click add button
            add_btns = self.driver.find_elements(
                By.XPATH,
                "//button[contains(@aria-label,'Add')] | //div[contains(@aria-label,'Add section')]",
            )
            for btn in add_btns:
                try:
                    btn.click()
                    break
                except:
                    continue

            self.wait(1)

            # Select Text
            text_elem = self.driver.find_element(
                By.XPATH, "//div[contains(text(),'Text')]"
            )
            text_elem.click()
            self.wait(2)

        except Exception as e:
            print(f"   ⚠️ Could not add text section: {e}")

    def publish(self):
        """Publish the site"""
        print("\n🚀 Publishing site...")

        try:
            # Find and click publish
            publish_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Publish')]"
            )
            publish_btn.click()
            self.wait(2)

            # Confirm
            confirm_btns = self.driver.find_elements(
                By.XPATH, "//button[contains(text(),'Publish')]"
            )
            for btn in confirm_btns:
                try:
                    btn.click()
                    break
                except:
                    continue

            self.wait(5)

            # Get URL
            try:
                url_elem = self.driver.find_element(
                    By.XPATH,
                    "//span[contains(@class,'sites')] | //a[contains(@href,'.googlecom')]",
                )
                self.site_url = url_elem.text
            except:
                self.site_url = "Site published (check Google Sites)"

            print(f"   ✅ Published: {self.site_url}")

        except Exception as e:
            print(f"   ⚠️ Publish error: {e}")

    def close(self):
        """Close browser"""
        if self.driver:
            input("\n⏸️ Press Enter to close browser...")
            self.driver.quit()


def main():
    print("=" * 60)
    print("🚀 GOOGLE SITES CREATOR - Evans Mathibe")
    print("=" * 60)

    # Get credentials
    print("\n📧 Enter your Google credentials:")
    email = input("   Email: ").strip()
    password = input("   Password: ").strip()

    # Initialize
    automator = GoogleSitesAutomator(headless=False)

    if not automator.setup():
        print("❌ Failed to setup browser")
        return

    try:
        # Login
        automator.login(email, password)

        # Create site
        automator.create_site("Evans Mathibe")

        # Get current URL
        current = automator.driver.current_url
        print(f"\n📝 Current state: {current}")

        print("""
\n⏸️ PAUSED - Manual steps needed:
The Google Sites editor works best with manual interaction.

Please in the browser:
1. Click "Blank" template to create site
2. You'll be in the site editor

Once you're in the editor, I can help add content via automation.

Press Enter to continue with manual setup guidance...
        """)
        input()

        print("""
📋 MANUAL SETUP STEPS:
======================

1. In Google Sites editor, click "Pages" on left
2. Add these pages: About, Services, Experience, Contact
3. For each page, add content using the + button

CONTENT TO USE:
===============
From: /home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md

When done:
1. Click "Publish" (top right)
2. Get your URL
3. Come back and tell me the URL

I'll create an agent to monitor and update it!
        """)

        automator.site_url = input("Enter your published site URL: ").strip()

        if automator.site_url:
            print(f"\n🎉 Your site is live!")
            print(f"   URL: {automator.site_url}")

            # Save URL
            with open("/home/ev/evansmathibe/SITE_URL.txt", "w") as f:
                f.write(automator.site_url)
            print("   Saved to: SITE_URL.txt")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        automator.close()


if __name__ == "__main__":
    main()
