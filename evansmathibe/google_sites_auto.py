#!/usr/bin/env python3
"""
Google Sites Creator - Automated Browser Script
Creates a complete Google Sites website for Evans Mathibe

Usage: python3 google_sites_auto.py
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class GoogleSitesCreator:
    def __init__(self):
        self.driver = None
        self.base_url = "https://sites.google.com"

    def setup_driver(self):
        """Setup Chrome driver with options"""
        print("Setting up Chrome driver...")
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Error setting up driver: {e}")
            print("Trying with system chrome...")
            self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(10)
        print("Driver ready!")

    def wait_and_click(self, by, value, timeout=20):
        """Wait for element and click"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return element

    def wait_for_element(self, by, value, timeout=20):
        """Wait for element to be present"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def login_to_google(self, email, password):
        """Login to Google account"""
        print("\n=== LOGGING IN TO GOOGLE ===")
        self.driver.get("https://accounts.google.com/signin")
        time.sleep(3)

        # Enter email
        print("Entering email...")
        email_input = self.wait_for_element(By.NAME, "identifier")
        email_input.send_keys(email)
        self.wait_and_click(By.ID, "identifierNext")
        time.sleep(3)

        # Enter password
        print("Entering password...")
        password_input = self.wait_for_element(By.NAME, "Passwd")
        password_input.send_keys(password)
        self.wait_and_click(By.ID, "passwordNext")
        time.sleep(5)
        print("Logged in successfully!")

    def create_new_site(self, site_name="Evans Mathibe Portfolio"):
        """Create a new Google Site"""
        print("\n=== CREATING NEW SITE ===")
        self.driver.get(self.base_url)
        time.sleep(3)

        # Click create new site
        try:
            create_btn = self.wait_and_click(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
        except:
            # Try alternative
            create_btn = self.wait_and_click(
                By.XPATH, "//a[contains(text(),'New site')]"
            )

        time.sleep(3)

        # Enter site name
        print(f"Setting site name: {site_name}")
        try:
            name_input = self.wait_for_element(
                By.XPATH, "//input[@placeholder='Enter a site name']"
            )
            name_input.send_keys(site_name)
        except:
            print("Could not find name input, site might have been created differently")

        time.sleep(2)

    def add_page(self, page_name, content=""):
        """Add a new page to the site"""
        print(f"\n--- Adding page: {page_name} ---")
        try:
            # Click add page button
            add_page_btn = self.wait_and_click(
                By.XPATH,
                "//button[contains(@aria-label,'Add page')] | //div[contains(text(),'Add page')]",
            )
            time.sleep(2)

            # Enter page name
            page_input = self.wait_for_element(
                By.XPATH, "//input[@placeholder='Page name']"
            )
            page_input.send_keys(page_name)
            time.sleep(1)

            # Click create
            create_btn = self.wait_and_click(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            time.sleep(3)

            print(f"Page '{page_name}' created!")
        except Exception as e:
            print(f"Error creating page: {e}")

    def add_text_content(self, content):
        """Add text content to current page"""
        try:
            # Click edit button or text tool
            edit_btn = self.wait_and_click(
                By.XPATH,
                "//button[contains(@aria-label,'Text')] | //div[contains(text(),'Text')]",
            )
            time.sleep(2)

            # Enter content
            content_box = self.wait_for_element(
                By.XPATH, "//div[@contenteditable='true']"
            )
            content_box.send_keys(content)
            time.sleep(1)
        except Exception as e:
            print(f"Could not add text: {e}")

    def add_section(self, section_type="text"):
        """Add a section to current page"""
        try:
            add_btn = self.wait_and_click(
                By.XPATH,
                "//button[contains(@aria-label,'Add section')] | //div[contains(text(),'Add')]",
            )
            time.sleep(2)

            # Select section type
            if section_type == "text":
                section_btn = self.wait_and_click(
                    By.XPATH, "//div[contains(text(),'Text')]"
                )
            elif section_type == "image":
                section_btn = self.wait_and_click(
                    By.XPATH, "//div[contains(text(),'Image')]"
                )
            elif section_type == "embed":
                section_btn = self.wait_and_click(
                    By.XPATH, "//div[contains(text(),'Embed')]"
                )

            time.sleep(2)
        except Exception as e:
            print(f"Could not add section: {e}")

    def publish_site(self):
        """Publish the site"""
        print("\n=== PUBLISHING SITE ===")
        try:
            # Click publish button
            publish_btn = self.wait_and_click(
                By.XPATH,
                "//button[contains(text(),'Publish')] | //button[contains(@aria-label,'Publish')]",
            )
            time.sleep(2)

            # Confirm publish
            confirm_btn = self.wait_and_click(
                By.XPATH, "//button[contains(text(),'Publish')]"
            )
            time.sleep(5)

            print("Site published!")

            # Get the published URL
            try:
                url_elem = self.driver.find_element(
                    By.XPATH, "//span[contains(@class,'published-url')]"
                )
                print(f"Published URL: {url_elem.text}")
            except:
                print("Could not get published URL")

        except Exception as e:
            print(f"Error publishing: {e}")

    def close(self):
        """Close the browser"""
        if self.driver:
            input("Press Enter to close browser...")
            self.driver.quit()


def main():
    print("=" * 60)
    print("GOOGLE SITES CREATOR - Evans Mathibe Portfolio")
    print("=" * 60)

    # Get credentials
    print("\nIMPORTANT: You need to be logged into Google!")
    print("The script will open Chrome. Please log in if not already.")
    input("Press Enter after logging in to continue...")

    creator = GoogleSitesCreator()
    creator.setup_driver()

    try:
        # Navigate to Google Sites
        print("\n=== NAVIGATING TO GOOGLE SITES ===")
        creator.driver.get("https://sites.google.com")
        time.sleep(3)

        input("""
Step 1: In the opened browser, go to sites.google.com
Step 2: Click "Create" to start a new site
Step 3: Choose a template (Blank is fine)
Step 4: Name your site: "Evans Mathibe"

Press Enter when you've created the site and are in the editor...
        """)

        # Add pages
        pages = [
            (
                "Home",
                "Hi, I'm Evans Mathibe\n\nProfessional | Visionary | Leader\n\nBuilding the future through innovation and dedication",
            ),
            (
                "About",
                "About Me\n\nEvans Mathibe is a dedicated professional with a passion for excellence and innovation. With years of experience in his field, he continues to push boundaries and deliver exceptional results.\n\nStats:\n• 10+ Years Experience\n• 50+ Projects Completed\n• 30+ Happy Clients",
            ),
            (
                "Services",
                "Services\n\n1. Consulting - Expert advice and strategic planning\n2. Project Management - End-to-end project delivery\n3. Business Development - Growth and partnerships\n4. Training & Coaching - Professional development\n5. Financial Analysis - Analysis and reporting\n6. Operations - Efficiency improvement",
            ),
            (
                "Experience",
                "Experience Timeline\n\n2024 - Present: COO, Evans Mathibe Group\nLeading operational strategy and business development\n\n2020 - 2024: Senior Management\nStrategic planning and team leadership\n\n2015 - 2020: Professional Growth\nBuilding expertise and establishing foundation",
            ),
            (
                "Contact",
                "Contact Information\n\nEmail: evansmathibe@email.com\nPhone: +27 XX XXX XXXX\nLocation: Gauteng, South Africa\n\nLet's connect and create something amazing together!",
            ),
        ]

        for page_name, content in pages:
            input(f"\nPress Enter to add page: {page_name}...")
            creator.add_page(page_name, content)

        input("\nPress Enter to publish the site...")
        creator.publish_site()

        print("\n" + "=" * 60)
        print("SETUP COMPLETE!")
        print("=" * 60)
        print("""
Next steps:
1. Customize your site theme in the editor
2. Add images from the assets folder
3. Set custom URL in Site Settings > Publishing
4. Add Google Forms for contact
        """)

    finally:
        creator.close()


if __name__ == "__main__":
    main()
