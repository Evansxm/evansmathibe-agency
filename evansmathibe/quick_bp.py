#!/usr/bin/env python3
"""
Quick Business Profile Updater - Minimal version
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def main():
    opts = Options()
    opts.add_argument("--profile-directory=Default")
    opts.add_argument("--no-sandbox")

    print("🔧 Starting...")
    driver = webdriver.Chrome(options=opts)

    try:
        driver.get("https://business.google.com")
        time.sleep(4)

        if "signin" not in driver.current_url:
            print("✅ Logged in!")
            driver.save_screenshot("/home/ev/evansmathibe/bp_final_check.png")

            # Try to click first business link
            try:
                links = driver.find_elements(By.TAG_NAME, "a")
                for l in links[:10]:
                    href = l.get_attribute("href") or ""
                    if "/w/" in href:
                        print(f"Clicking: {l.text[:30]}")
                        l.click()
                        time.sleep(3)
                        break
            except:
                pass

            driver.save_screenshot("/home/ev/evansmathibe/bp_after_click.png")

            # Try Edit
            try:
                edit = driver.find_element(
                    By.XPATH, "//button[contains(text(),'Edit')]"
                )
                edit.click()
                time.sleep(2)
                driver.save_screenshot("/home/ev/evansmathibe/bp_edit_mode.png")
                print("✅ Entered edit mode!")
            except:
                print("⚠️ Could not enter edit mode")

            print(f"\n📍 {driver.current_url}")
            print("Check screenshots!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        time.sleep(30)
        driver.quit()


if __name__ == "__main__":
    main()
