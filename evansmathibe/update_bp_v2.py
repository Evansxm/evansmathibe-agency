#!/usr/bin/env python3
"""
Google Business Profile Updater - JavaScript Injection Method
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui

EMAIL = "evansmathibe82@gmail.com"
PASSWORD = "Bonolo14$"


def update_bp():
    opts = Options()
    opts.add_argument("--profile-directory=Default")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(25)

    result = {"steps": [], "success": False}

    try:
        # Go to Business Profile
        print("📍 Opening Google Business Profile...")
        driver.get(
            "https://business.google.com/locations?gmbsrc=all-en-z-z-z-gmb-l-z-d"
        )
        time.sleep(5)

        # Wait for page to load
        try:
            ui.WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except:
            pass

        result["steps"].append(f"Page title: {driver.title}")

        # Try JavaScript to find and click elements
        print("🔍 Looking for business...")

        # Try to find the business link using JavaScript
        businesses = driver.find_elements(By.CSS_SELECTOR, "a[href*='/w/']")

        # Try clicking first business
        try:
            # Find all clickable elements that might be businesses
            links = driver.find_elements(By.XPATH, "//a[contains(@href, '/w/')]")
            for link in links[:5]:
                try:
                    text = link.text
                    if text and len(text) > 2:
                        print(f"   Found: {text[:50]}")
                except:
                    pass
        except Exception as e:
            print(f"   Scan error: {e}")

        # Try direct navigation to profile manager
        print("📝 Trying direct edit URL...")
        driver.get("https://business.google.com/manage/?gmbsrc=all-en-z-z-z-gmb-l-z-d")
        time.sleep(5)

        # Look for edit buttons
        edit_buttons = driver.find_elements(
            By.XPATH, "//button[contains(text(),'Edit')]"
        )
        print(f"   Found {len(edit_buttons)} Edit buttons")

        # Try JavaScript click on first edit
        if edit_buttons:
            try:
                driver.execute_script("arguments[0].click();", edit_buttons[0])
                time.sleep(3)
                result["steps"].append("Clicked Edit button")
            except Exception as e:
                result["steps"].append(f"Edit click failed: {e}")

        # Try to find name input via JavaScript
        print("📝 Attempting to update business name...")

        # JavaScript injection to find and fill fields
        js_script = """
        // Try to find business name input
        var inputs = document.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {
            var name = inputs[i].name || inputs[i].id || '';
            var aria = inputs[i].getAttribute('aria-label') || '';
            if (name.includes('name') || aria.includes('name') || aria.includes('Business')) {
                inputs[i].value = 'Evans Mathibe | Mone | TYC';
                inputs[i].dispatchEvent(new Event('input', {bubbles: true}));
                return 'Updated: ' + name;
            }
        }
        return 'Name field not found';
        """

        try:
            result_js = driver.execute_script(js_script)
            result["steps"].append(result_js)
            print(f"   {result_js}")
        except Exception as e:
            result["steps"].append(f"JS error: {e}")

        # Try description
        desc_js = """
        var textareas = document.querySelectorAll('textarea');
        for (var i = 0; i < textareas.length; i++) {
            var aria = textareas[i].getAttribute('aria-label') || '';
            var name = textareas[i].name || '';
            if (aria.includes('description') || name.includes('description') || aria.includes('About')) {
                textareas[i].value = 'Evans Mathibe - Premier South African Agency offering AI Automation Services, Project Management, Brand Design & Management, Creative Services, Advertising, Event Design & Management, Film Production, Photography, and Mentorship. Serving: Johannesburg, Cape Town, Durban, Pretoria, and all major South African cities.';
                textareas[i].dispatchEvent(new Event('input', {bubbles: true}));
                return 'Description updated';
            }
        }
        return 'Description field not found';
        """

        try:
            result_desc = driver.execute_script(desc_js)
            result["steps"].append(result_desc)
            print(f"   {result_desc}")
        except Exception as e:
            result["steps"].append(f"Desc JS error: {e}")

        # Save screenshot
        driver.save_screenshot("/home/ev/evansmathibe/bp_final.png")

        result["success"] = True
        result["url"] = driver.current_url

    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Error: {e}")
    finally:
        with open("/home/ev/evansmathibe/bp_update_result.json", "w") as f:
            json.dump(result, f, indent=2)

        print("\n⏳ Browser open for 30 seconds - complete manually if needed...")
        time.sleep(30)
        driver.quit()

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Google Business Profile Updater v2")
    print("=" * 60)
    result = update_bp()
    print(f"\nResult: {json.dumps(result, indent=2)}")
