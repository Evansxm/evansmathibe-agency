#!/usr/bin/env python3
"""
Evans Mathibe Agency - Business Verification Automation
Monitors Gmail for verification codes from Google, Bing, and industry directories.

Usage:
  export GMAIL_EMAIL="your.email@gmail.com"
  export GMAIL_APP_PASSWORD="your-app-password"
  python3 verify_business.py
"""

import imaplib
import email
import re
import time
import os

# === CONFIGURE GMAIL (via environment variables) ===
GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

def connect_to_gmail():
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("ERROR: Set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables.")
        return None
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        return mail
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def extract_code(text):
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
        else:
            print(f"Found email from {msg['From']} but no code extracted.")

    mail.logout()

if __name__ == "__main__":
    print("=== MONITORING BUSINESS VERIFICATIONS ===")
    check_for_verification_emails()
