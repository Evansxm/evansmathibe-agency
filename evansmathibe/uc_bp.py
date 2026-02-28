#!/usr/bin/env python3
"""
Google Business Profile - Full Automation with undetected-chromedriver
"""

import time
import json
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By

EMAIL = "evansmathibe82@gmail.com"
PASSWORD = "Bonolo14$"


def run():
    print("🔧 Starting Chrome...")

    import undetected_chromedriver as uc

    driver = uc.Chrome(headless=False, version_main=None)
    driver.set_page_load_timeout(45)

    result = {"steps": []}

    try:
        # Step 1: Go to Business Profile
        print("📍 Step 1: Going to Google Business Profile...")
        driver.get("https://business.google.com")
        time.sleep(5)
        result["steps"].append(f"Opened: {driver.title}")

        # Step 2: Wait for login if needed
        if "signin" in driver.current_url:
            print("🔐 Step 2: Logging in...")

            # Email
            email_input = ui.WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.NAME, "identifier")
            )
            email_input.send_keys(EMAIL)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(4)

            # Password
            pass_input = ui.WebDriverWait(driver, 20).until(
                lambda d: d.find_element(By.NAME, "Passwd")
            )
            pass_input.send_keys(PASSWORD)
            driver.find_element(By.ID, "passwordNext").click()
            time.sleep(6)

            result["steps"].append("Logged in")

        # Step 3: Go to Business Profile again
        print("📍 Step 3: Going to Business Profile Manager...")
        driver.get("https://business.google.com/manage/?gmbsrc=all-en-z-z-z-gmb-l-z-d")
        time.sleep(6)

        # Step 4: Find and click the business
        print("🔍 Step 4: Looking for business...")
        try:
            # Look for any link to click
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links[:10]:
                try:
                    href = link.get_attribute("href") or ""
                    text = link.text or ""
                    if "w/" in href and len(text) > 2:
                        print(f"   Clicking: {text[:30]}")
                        link.click()
                        time.sleep(4)
                        break
                except:
                    continue
        except Exception as e:
            result["steps"].append(f"Link click: {e}")

        # Step 5: Try to edit
        print("✏️ Step 5: Trying to edit...")
        try:
            # Find edit button
            edit_btns = driver.find_elements(
                By.XPATH, "//button[contains(text(),'Edit')]"
            )
            if edit_btns:
                edit_btns[0].click()
                time.sleep(3)
                result["steps"].append("Clicked Edit")
        except Exception as e:
            result["steps"].append(f"Edit: {e}")

        # Save screenshot
        driver.save_screenshot("/home/ev/evansmathibe/undetected_bp.png")

        # Step 6: Try to update name via JS
        print("📝 Step 6: Updating business name...")
        js_name = """
        var inputs = document.querySelectorAll('input');
        for(var i=0; i<inputs.length; i++) {
            if(inputs[i].name.includes('name') || inputs[i].getAttribute('aria-label')?.includes('name')) {
                inputs[i].value = 'Evans Mathibe | Mone | TYC';
                return 'Name updated';
            }
        }
        return 'Name field not found';
        """
        name_result = driver.execute_script(js_name)
        result["steps"].append(name_result)

        # Save final screenshot
        driver.save_screenshot("/home/ev/evansmathibe/undetected_final.png")

        result["success"] = True
        result["url"] = driver.current_url

    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Error: {e}")
    finally:
        with open("/home/ev/evansmathibe/uc_result.json", "w") as f:
            json.dump(result, f, indent=2)

        print(f"\n📍 Final URL: {driver.current_url}")
        print("\n⏳ Browser open for 60 seconds...")
        time.sleep(60)
        driver.quit()

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Google Business Profile - Undetected Chrome")
    print("=" * 60)
    run()
