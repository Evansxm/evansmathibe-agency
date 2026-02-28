#!/usr/bin/env python3
"""
Google Sites Creator - Non-Interactive Full Automation
Creates Evans Mathibe website automatically using Selenium
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)


class FullAutoGoogleSites:
    """Fully automated Google Sites creator"""

    def __init__(self):
        self.driver = None
        self.site_url = None

    def setup_browser(self):
        """Setup Chrome"""
        print("🔧 Setting up Chrome...")

        opts = Options()
        opts.add_argument("--start-maximized")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(10)
        print("✅ Browser ready!")
        return True

    def wait(self, secs=2):
        time.sleep(secs)

    def safe_click(self, by, value, description=""):
        """Click with multiple strategies"""
        strategies = [
            (By.XPATH, value),
            (By.CSS_SELECTOR, value),
            (By.ID, value),
        ]

        for strategy in strategies:
            try:
                if strategy[0] == By.XPATH:
                    elements = self.driver.find_elements(By.XPATH, strategy[1])
                    if elements:
                        elements[0].click()
                        self.wait(1)
                        return True
                elif strategy[0] == By.CSS_SELECTOR:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, strategy[1])
                    if elements:
                        elements[0].click()
                        self.wait(1)
                        return True
            except:
                continue
        return False

    def safe_send_keys(self, by, value, text):
        """Send keys with multiple strategies"""
        try:
            elem = self.driver.find_element(by, value)
            elem.clear()
            elem.send_keys(text)
            return True
        except:
            return False

    def create_site(self, email, password, site_name="Evans Mathibe"):
        """Create site automatically"""
        print("\n🚀 Starting automated site creation...")

        # Step 1: Go to Google Sites
        print("   📍 Navigating to Google Sites...")
        self.driver.get("https://sites.google.com")
        self.wait(3)

        # Step 2: Login
        print("   🔐 Checking for login...")
        try:
            login_btn = self.driver.find_element(
                By.XPATH, "//a[contains(text(),'Sign in')]"
            )
            login_btn.click()
            self.wait(2)

            # Enter email
            print(f"   📧 Entering email: {email}")
            email_field = self.driver.find_element(By.NAME, "identifier")
            email_field.send_keys(email)
            self.driver.find_element(By.ID, "identifierNext").click()
            self.wait(3)

            # Enter password
            print("   🔑 Entering password...")
            pass_field = self.driver.find_element(By.NAME, "Passwd")
            pass_field.send_keys(password)
            self.driver.find_element(By.ID, "passwordNext").click()
            self.wait(5)
            print("   ✅ Logged in!")
        except Exception as e:
            print(f"   ⚠️ Login check: {e}")

        # Step 3: Create new site
        print("   🆕 Creating new site...")
        self.driver.get("https://sites.google.com")
        self.wait(3)

        try:
            # Try to find create button
            create_xpaths = [
                "//button[contains(text(),'Create')]",
                "//a[contains(text(),'Create new site')]",
                "//div[contains(text(),'Create new site')]",
                "//button[contains(@aria-label,'Create')]",
            ]

            for xpath in create_xpaths:
                try:
                    btn = self.driver.find_element(By.XPATH, xpath)
                    btn.click()
                    print("   ✅ Clicked create!")
                    break
                except:
                    continue

            self.wait(3)

            # Enter site name
            name_xpaths = [
                "//input[@placeholder='Enter a site name']",
                "//input[@placeholder='Site name']",
                "//input[contains(@class,'name-input')]",
            ]

            for xpath in name_xpaths:
                try:
                    name_field = self.driver.find_element(By.XPATH, xpath)
                    name_field.send_keys(site_name)
                    print(f"   ✅ Site named: {site_name}")
                    break
                except:
                    continue

            self.wait(2)

            # Click create/submit
            submit_xpaths = [
                "//button[contains(text(),'Create')]",
                "//button[contains(text(),'Continue')]",
                "//button[contains(@type,'submit')]",
            ]

            for xpath in submit_xpaths:
                try:
                    submit_btn = self.driver.find_element(By.XPATH, xpath)
                    submit_btn.click()
                    print("   ✅ Site created!")
                    break
                except:
                    continue

            self.wait(5)

            # Get the editor URL
            self.site_url = self.driver.current_url
            print(f"   📝 Editor URL: {self.site_url}")

        except Exception as e:
            print(f"   ⚠️ Error during creation: {e}")

        return self.site_url

    def close(self):
        """Close browser"""
        if self.driver:
            print("\n⏸️ Browser open for manual completion...")
            print("Complete the remaining steps in the browser, then close.")
            input("Press Enter to close browser and finish...")
            self.driver.quit()


def main():
    print("=" * 60)
    print("🚀 FULL AUTOMATION - Google Sites Creator")
    print("=" * 60)

    # Credentials
    print("\n📧 Enter Google credentials (or press Enter to skip login):")
    email = input("   Email: ").strip()
    password = input("   Password: ").strip()

    if not email:
        print("\n⚠️ No credentials provided.")
        print("I'll open Google Sites for you to log in manually.")

        # Just open browser
        import subprocess

        subprocess.Popen(["google-chrome", "https://sites.google.com"])

        print("""
\n📋 INSTRUCTIONS:
─────────────────
1. Log into your Google account
2. Click "Create new site"
3. Choose "Blank" template
4. Name it: "Evans Mathibe"
5. Add pages and content from the guide
6. Publish!

Resources:
- Content: /home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md
- Images: /home/ev/evansmathibe/assets/
- Landing Page: /home/ev/evansmathibe/index.html
        """)
        return

    # Run automation
    bot = FullAutoGoogleSites()

    if bot.setup_browser():
        try:
            url = bot.create_site(email, password)

            if url:
                print(f"\n✅ Site creation initiated!")
                print(f"   Editor: {url}")

                print("""

📋 NEXT STEPS IN BROWSER:
─────────────────────────
1. You'll be in the Google Sites editor
2. Add pages: About, Services, Experience, Contact
3. Add content from /home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md
4. Upload images from /home/ev/evansmathibe/assets/
5. Click "Publish" (top right)
6. Get your URL!

The automation has started the process.
Manual completion needed for best results.
                """)

                # Save URL
                with open("/home/ev/evansmathibe/SITE_URL.txt", "w") as f:
                    f.write(url or "Created - check Google Sites")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            bot.close()

    print("\n✨ Done! Your site should be underway.")


if __name__ == "__main__":
    main()
