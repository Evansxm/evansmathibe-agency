#!/usr/bin/env python3
"""
Non-interactive Google Sites Creator
Saves result to file
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

EMAIL = "evansmathibe82@gmail.com"
PASSWORD = "Bonolo14$"


def create_site():
    opts = Options()
    opts.add_argument("--profile-directory=Default")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(20)

    result = {"status": "starting", "url": None, "error": None}

    try:
        # Login
        print("🔐 Logging in...")
        driver.get("https://accounts.google.com")
        time.sleep(2)

        try:
            email = driver.find_element(By.NAME, "identifier")
            email.send_keys(EMAIL)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(3)

            pwd = driver.find_element(By.NAME, "Passwd")
            pwd.send_keys(PASSWORD)
            driver.find_element(By.ID, "passwordNext").click()
            time.sleep(4)
            print("   ✅ Logged in")
        except Exception as e:
            result["error"] = f"Login failed: {e}"
            print(f"   ❌ {result['error']}")
            return result

        # Go to Sites
        print("📍 Creating site...")
        driver.get("https://sites.google.com")
        time.sleep(3)

        # Click Create
        try:
            create_btn = driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            time.sleep(2)
        except:
            pass

        # Enter name
        try:
            name_input = driver.find_element(
                By.XPATH, "//input[@placeholder='Enter a site name']"
            )
            name_input.send_keys("Evans Mathibe")
            time.sleep(1)

            create_btn = driver.find_element(
                By.XPATH, "//button[contains(text(),'Create')]"
            )
            create_btn.click()
            time.sleep(4)
        except Exception as e:
            result["error"] = f"Could not create site: {e}"

        result["status"] = "created"
        result["url"] = driver.current_url
        print(f"   ✅ Site created: {result['url']}")

    except Exception as e:
        result["error"] = str(e)
        print(f"   ❌ Error: {e}")
    finally:
        # Save result
        with open("/home/ev/evansmathibe/creation_result.json", "w") as f:
            json.dump(result, f, indent=2)

        print("\n⏳ Browser will close in 10 seconds...")
        time.sleep(10)
        driver.quit()

    return result


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Google Sites Creator")
    print("=" * 50)
    result = create_site()
    print(f"\nResult: {result}")
