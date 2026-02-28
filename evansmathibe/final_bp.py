#!/usr/bin/env python3
"""
Google Business Profile - Using System Chrome with your profile
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

EMAIL = "evansmathibe82@gmail.com"
PASSWORD = "Bonolo14$"


def run():
    print("🔧 Starting with system Chrome...")

    opts = Options()
    opts.add_argument("--profile-directory=Default")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(30)

    result = {"steps": []}

    try:
        # Go directly to Business Profile
        print("📍 Going to Business Profile...")
        driver.get("https://business.google.com/manage/")
        time.sleep(5)

        result["steps"].append(f"URL: {driver.current_url}")
        result["steps"].append(f"Title: {driver.title}")

        # Check if logged in
        if "signin" in driver.current_url:
            print("🔐 Need to login...")

            # Email
            email = driver.find_element(By.NAME, "identifier")
            email.send_keys(EMAIL)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(3)

            # Password
            pwd = driver.find_element(By.NAME, "Passwd")
            pwd.send_keys(PASSWORD)
            driver.find_element(By.ID, "passwordNext").click()
            time.sleep(5)

            result["steps"].append("Logged in")

        # Save initial screenshot
        driver.save_screenshot("/home/ev/evansmathibe/bp1.png")

        # Try to find business listing
        print("🔍 Looking for business...")
        time.sleep(3)

        # Click on first business link
        try:
            links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/w/']")
            for link in links[:3]:
                try:
                    txt = link.text
                    if txt and len(txt) > 2:
                        print(f"   Clicking: {txt[:30]}")
                        link.click()
                        time.sleep(4)
                        break
                except:
                    continue
        except Exception as e:
            result["steps"].append(f"Click error: {e}")

        driver.save_screenshot("/home/ev/evansmathibe/bp2.png")

        # Try Edit button
        print("✏️ Looking for Edit button...")
        try:
            edit = driver.find_element(By.XPATH, "//button[contains(text(),'Edit')]")
            edit.click()
            time.sleep(3)
            result["steps"].append("Clicked Edit")
        except:
            result["steps"].append("No Edit button found")

        driver.save_screenshot("/home/ev/evansmathibe/bp3.png")

        # Try to fill name
        print("📝 Trying to fill name...")
        try:
            # Find name input
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs[:10]:
                try:
                    name = inp.get_attribute("name") or ""
                    aria = inp.get_attribute("aria-label") or ""
                    if "name" in name.lower() or "business" in aria.lower():
                        inp.clear()
                        inp.send_keys("Evans Mathibe | Mone | TYC")
                        result["steps"].append("Name updated!")
                        break
                except:
                    continue
        except Exception as e:
            result["steps"].append(f"Name error: {e}")

        driver.save_screenshot("/home/ev/evansmathibe/bp4.png")

        result["success"] = True
        result["url"] = driver.current_url

    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Error: {e}")
    finally:
        with open("/home/ev/evansmathibe/bp_result_final.json", "w") as f:
            json.dump(result, f, indent=2)

        print(f"\n📍 URL: {driver.current_url}")
        print("\n⏳ Browser open for 60s...")
        time.sleep(60)
        driver.quit()

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Google Business Profile Updater")
    print("=" * 60)
    run()
