#!/usr/bin/env python3
"""
Evans Mathibe Agency - Business Verification Automation
Monitors Gmail for verification codes from Google, Bing, and industry directories.
"""

import imaplib
import email
import re
import time

# === CONFIGURE GMAIL ===
GMAIL_EMAIL = "evansmathibe82@gmail.com"
GMAIL_APP_PASSWORD = "Bonolo14$"

def connect_to_gmail():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        return mail
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def extract_code(text):
    # Common verification code patterns (5-6 digits)
    patterns = [
        r"code is (\d{5,6})",
        r"verification code: (\d{5,6})",
        r"PIN: (\d{5,6})",
        r"(\d{6})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def check_for_verification_emails():
    mail = connect_to_gmail()
    if not mail:
        return

    mail.select("inbox")
    # Search for emails from Google Business, Bing Places, etc.
    status, messages = mail.search(None, '(OR (FROM "google.com") (FROM "microsoft.com"))')
    
    if status != "OK" or not messages[0]:
        print("No verification emails found.")
        return

    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        if status != "OK":
            continue

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject = msg["Subject"]
        
        # Get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        code = extract_code(body)
        if code:
            print(f"FOUND CODE: {code} (Subject: {subject})")
            # In a real scenario, we might POST this code to a verification API
        else:
            print(f"Found email from {msg['From']} but no code extracted.")

    mail.logout()

if __name__ == "__main__":
    print("=== MONITORING BUSINESS VERIFICATIONS ===")
    check_for_verification_emails()
