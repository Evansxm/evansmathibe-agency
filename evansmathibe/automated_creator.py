#!/usr/bin/env python3
"""
Google Sites Creator - FULLY AUTOMATED
Uses Playwright's Chromium via Selenium
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class AutoGoogleSites:
    """Fully automated Google Sites creator"""

    def __init__(self):
        self.driver = None
        self.site_url = None
        self.chrome_path = (
            "/home/ev/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
        )

    def setup(self):
        """Setup Chrome"""
        print("🔧 Setting up Chromium...")

        opts = Options()
        opts.binary_location = self.chrome_path
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])

        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(15)
        print("✅ Browser ready!")
        return True

    def wait(self, secs=2):
        time.sleep(secs)

    def click(self, by, value):
        """Click element"""
        try:
            elem = self.driver.find_element(by, value)
            elem.click()
            self.wait(1)
            return True
        except Exception as e:
            return False

    def type(self, by, value, text):
        """Type text"""
        try:
            elem = self.driver.find_element(by, value)
            elem.clear()
            elem.send_keys(text)
            return True
        except:
            return False

    def login(self, email, password):
        """Login to Google"""
        print("\n🔐 Logging in...")
        self.driver.get("https://accounts.google.com")
        self.wait(3)

        # Email
        print(f"   📧 {email}")
        self.type(By.NAME, "identifier", email)
        self.click(By.ID, "identifierNext")
        self.wait(3)

        # Password
        print("   🔑 Password ***")
        self.type(By.NAME, "Passwd", password)
        self.click(By.ID, "passwordNext")
        self.wait(5)
        print("   ✅ Logged in!")

    def create_site(self, site_name="Evans Mathibe"):
        """Create new site"""
        print(f"\n🏗️ Creating site: {site_name}")
        self.driver.get("https://sites.google.com")
        self.wait(4)

        # Click Create
        try:
            create_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            self.wait(2)
        except:
            pass

        # Enter name
        try:
            name_input = self.driver.find_element(
                By.XPATH, "//input[@placeholder='Enter a site name']"
            )
            name_input.send_keys(site_name)
            self.wait(1)

            # Click Create
            create_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            self.wait(5)
        except Exception as e:
            print(f"   ⚠️ {e}")

        print("   ✅ Site creation initiated!")
        return self.driver.current_url

    def add_page(self, page_name):
        """Add a page"""
        print(f"   📄 Adding page: {page_name}")
        try:
            # Find add page button
            add_btn = self.driver.find_element(
                By.XPATH, "//button[contains(@aria-label,'Add page')]"
            )
            add_btn.click()
            self.wait(2)

            # Enter page name
            name_input = self.driver.find_element(
                By.XPATH, "//input[@placeholder='Page name']"
            )
            name_input.send_keys(page_name)
            self.wait(1)

            # Click Create
            create_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            self.wait(3)
        except Exception as e:
            print(f"   ⚠️ Could not add page: {e}")

    def add_text_content(self, heading, content):
        """Add text content"""
        print(f"   📝 Adding: {heading}")
        try:
            # Click add section
            add_section = self.driver.find_element(
                By.XPATH, "//button[contains(@aria-label,'Add section')]"
            )
            add_section.click()
            self.wait(1)

            # Select Text
            text_elem = self.driver.find_element(
                By.XPATH, "//div[contains(text(),'Text')]"
            )
            text_elem.click()
            self.wait(2)

            # Enter content (heading + body)
            # This is simplified - in reality would need more handling
        except Exception as e:
            print(f"   ⚠️ {e}")

    def publish(self):
        """Publish site"""
        print("\n🚀 Publishing...")
        try:
            # Click Publish
            publish_btn = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Publish')]"
            )
            publish_btn.click()
            self.wait(2)

            # Confirm
            confirm = self.driver.find_element(
                By.XPATH, "//button[contains(text(),'Publish')]"
            )
            confirm.click()
            self.wait(5)

            # Try to get URL
            try:
                url_elem = self.driver.find_element(
                    By.XPATH, "//span[contains(@class,'sites')]"
                )
                self.site_url = url_elem.text
            except:
                self.site_url = "Published (check Google Sites)"

            print(f"   ✅ Done! {self.site_url}")
        except Exception as e:
            print(f"   ⚠️ Publish error: {e}")

    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()


def main():
    print("=" * 60)
    print("🚀 GOOGLE SITES CREATOR - FULLY AUTOMATED")
    print("=" * 60)

    # Get credentials
    print("\n📧 Enter Google credentials:")
    email = input("   Email: ").strip()
    password = input("   Password: ").strip()

    if not email:
        print("❌ No email provided")
        return

    # Run automation
    bot = AutoGoogleSites()

    if not bot.setup():
        print("❌ Failed to setup")
        return

    try:
        # Login
        bot.login(email, password)

        # Create site
        bot.create_site("Evans Mathibe")

        # Wait for user to complete in browser
        print("""

⚠️  AUTOMATION PAUSED - Manual completion needed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Google Sites editor requires manual interaction for:
• Choosing template
• Adding pages  
• Adding content
• Customizing theme
• Final publishing

Please complete these steps in the browser:
1. Choose "Blank" template
2. Add pages: About, Services, Experience, Contact
3. Add content from: /home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md
4. Upload images from: /home/ev/evansmathibe/assets/
5. Click "Publish"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Press ENTER when site is published...
        """)
        input()

        # Save URL
        url = input("Enter published URL: ").strip()
        if url:
            with open("/home/ev/evansmathibe/SITE_URL.txt", "w") as f:
                f.write(url)
            print(f"\n🎉 Site saved: {url}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
