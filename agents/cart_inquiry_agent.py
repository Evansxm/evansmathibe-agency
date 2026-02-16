#!/usr/bin/env python3
"""
AGENT: Cart & Inquiry Flow Manager
==================================
Brief: Manages the service cart and inquiry submission flow

RESPONSIBILITIES:
1. Add services to cart when user clicks "Add to Inquiry"
2. Display cart contents in cart section
3. When user clicks "Send Inquiry":
   - Collect all selected services
   - Open email client with pre-filled message
   - Include user's contact details
   - Clear cart after submission
4. Show appropriate toasts/notifications

CART WORKFLOW:
1. User clicks "Add to Inquiry" on any service
2. Service added to cart array (no duplicates)
3. Cart section shows list of selected services
4. Each service has "X" button to remove
5. "Send Inquiry" button opens email with all services
6. After sending, cart clears

EMAIL FORMAT:
To: evans.mathibe@mail.com
Subject: New Service Inquiry - EvansMathibe Agency

Body:
Hello EvansMathibe,

I am interested in the following services:
- Photography
- Film Production
- AI Brand Automation

Please provide me with pricing and next steps.

Thank you

CONTACT INFO COLLECTED:
- Name (required)
- Email (required)
- Phone (optional)
- Service interested in (dropdown)
- Message (textarea)

FILES:
- Website: /home/ev/EvansMathibe_Agency/website/index.html
- Cart logic: JavaScript cart functions in index.html
"""

import json


def get_cart_workflow():
    """Return cart workflow documentation"""
    return {
        "workflow": [
            {
                "step": 1,
                "action": "User clicks 'Add to Inquiry' button",
                "result": "Service added to cart array",
            },
            {
                "step": 2,
                "action": "User adds more services",
                "result": "More items added to cart",
            },
            {
                "step": 3,
                "action": "User views cart section",
                "result": "Shows all selected services with remove buttons",
            },
            {
                "step": 4,
                "action": "User clicks 'Send Inquiry'",
                "result": "Email client opens with pre-filled inquiry",
            },
            {
                "step": 5,
                "action": "User sends email",
                "result": "Cart clears, success toast shown",
            },
        ],
        "button_labels": {
            "add": "Add to Inquiry",
            "remove": "X (remove from cart)",
            "submit": "Send Inquiry",
        },
        "email_recipient": "evans.mathibe@mail.com",
        "email_subject": "New Service Inquiry - EvansMathibe Agency",
    }


def check_inquiry_flow():
    """Verify inquiry flow is working"""
    from pathlib import Path

    html_file = Path(__file__).parent.parent / "website" / "index.html"
    content = html_file.read_text()

    checks = {
        "has_add_to_cart": "addToCart(" in content,
        "has_cart_display": "updateCart()" in content,
        "has_send_inquiry": "submitInquiry()" in content,
        "has_mailto": "mailto:evans.mathibe@mail.com" in content,
        "has_cart_section": 'id="cartItems"' in content,
    }

    return checks


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "workflow":
            print(json.dumps(get_cart_workflow(), indent=2))
        elif sys.argv[1] == "check":
            print(json.dumps(check_inquiry_flow(), indent=2))
    else:
        print(json.dumps(get_cart_workflow(), indent=2))
