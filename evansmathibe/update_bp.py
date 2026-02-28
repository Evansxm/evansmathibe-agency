#!/usr/bin/env python3
"""
Google Business Profile Updater - GitHub Actions Compatible
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load credentials from environment variables
EMAIL = os.environ.get("GOOGLE_EMAIL")
PASSWORD = os.environ.get("GOOGLE_PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("GOOGLE_EMAIL and GOOGLE_PASSWORD environment variables must be set.")


def update_business_profile():
    opts = Options()
    # Headless mode for CI/CD
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    
    # User agent to avoid detection
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(60)

    result = {"status": "starting", "steps": [], "error": None}
    
    # Ensure output directory exists
    output_dir = "bp_artifacts"
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Go to Google Login first if not logged in (simplified flow, might need cookies in real CI)
        print("📍 Step 1: Going to Google Business Profile...")
        driver.get("https://business.google.com")
        time.sleep(5)
        
        # Check if login is required
        if "signin" in driver.current_url or "accounts.google.com" in driver.current_url:
            print("   Login required...")
            try:
                email_field = driver.find_element(By.ID, "identifierId")
                email_field.send_keys(EMAIL)
                driver.find_element(By.ID, "identifierNext").click()
                time.sleep(5)
                
                pass_field = driver.find_element(By.NAME, "Passwd")
                pass_field.send_keys(PASSWORD)
                driver.find_element(By.ID, "passwordNext").click()
                time.sleep(5)
                result["steps"].append("Performed login")
            except Exception as e:
                result["steps"].append(f"Login failed: {e}")
                driver.save_screenshot(f"{output_dir}/login_error.png")
                raise e

        result["steps"].append(f"Opened: {driver.current_url}")

        # Try to find business
        print("   Looking for business list...")
        time.sleep(5)

        # Save screenshot
        driver.save_screenshot(f"{output_dir}/bp_step1.png")

        # Try clicking on a business
        try:
            # Look for any clickable business name
            businesses = driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'business')] | //a[contains(@href,'/w/')]",
            )
            if businesses:
                print(f"   Found {len(businesses)} businesses")
                businesses[0].click()
                time.sleep(5)
                driver.save_screenshot(f"{output_dir}/bp_business.png")
            else:
                 print("   No business list found, might be directly on profile or empty.")
        except Exception as e:
            result["steps"].append(f"No business found: {e}")

        # Try Edit mode
        print("   Trying to enter edit mode...")
        try:
            edit_buttons = driver.find_elements(
                By.XPATH,
                "//button[contains(text(),'Edit')] | //button[contains(@aria-label,'Edit')]",
            )
            for btn in edit_buttons:
                try:
                    btn.click()
                    time.sleep(3)
                    driver.save_screenshot(f"{output_dir}/bp_edit.png")
                    result["steps"].append("Entered edit mode")
                    break
                except:
                    continue
        except Exception as e:
            result["steps"].append(f"Edit error: {e}")

        # Try to find and update business name
        print("   Attempting to update business name...")
        try:
            name_field = driver.find_element(
                By.XPATH, "//input[@name='name'] | //input[@aria-label='Business name']"
            )
            name_field.clear()
            name_field.send_keys("Evans Mathibe")
            result["steps"].append("Updated business name")
            time.sleep(1)
        except:
            pass

        # Try description
        try:
            desc_field = driver.find_element(
                By.XPATH, "//textarea[@name='description'] | //textarea"
            )
            desc_field.clear()
            desc = """Evans Mathibe - Premier South African Agency offering AI Automation Services, Project Management, Brand Design & Management, Creative Services, Advertising, Event Design & Management, Film Production, Photography, and Mentorship.

Serving: Johannesburg, Cape Town, Durban, Pretoria, and all major South African cities and business districts including Sandton, Rosebank, Midrand, Centurion, Menlyn, Cape Town CBD, Durban CBD."""
            desc_field.send_keys(desc)
            result["steps"].append("Updated description")
        except Exception as e:
            result["steps"].append(f"Description error: {e}")

        # Save screenshot
        driver.save_screenshot(f"{output_dir}/bp_updated.png")

        result["status"] = "success"
        result["url"] = driver.current_url

    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Error: {e}")
        driver.save_screenshot(f"{output_dir}/error_state.png")
    finally:
        # Save result
        with open(f"{output_dir}/bp_result.json", "w") as f:
            json.dump(result, f, indent=2)

        driver.quit()

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Google Business Profile Updater - CI/CD Mode")
    print("=" * 60)
    result = update_business_profile()
    print(f"\nResult: {json.dumps(result, indent=2)}")
