#!/usr/bin/env python3
"""
EvansMathibe Content Agent
Handles all contact, email, and inquiry content generation
"""

from datetime import datetime

CONTENT_TEMPLATES = {
    "inquiry": {
        "subject": "New Service Inquiry - EvansMathibe Agency",
        "body": """Dear EvansMathibe Team,

I am interested in the following services:
{services}

Please provide me with more information about pricing and next steps.

Thank you for your time.

Best regards,
{name}
{email}
{phone}""",
    },
    "notification": {
        "subject": "Project Interest Notification",
        "body": """Dear EvansMathibe Team,

I am interested in learning more about:
{project}

Please contact me with updates.

Contact Details:
Email: {email}
Phone: {phone}

Thank you.""",
    },
    "general": {
        "subject": "General Inquiry - EvansMathibe Agency",
        "body": """Dear EvansMathibe Team,

{name} has reached out via the website contact form.

Email: {email}
Phone: {phone}

Message:
{message}

Please respond at your earliest convenience.""",
    },
}


def generate_inquiry_email(name, email, phone, services):
    """Generate inquiry email content"""
    services_text = "\n".join([f"- {s}" for s in services])
    return CONTENT_TEMPLATES["inquiry"]["body"].format(
        name=name, email=email, phone=phone or "Not provided", services=services_text
    )


def generate_mailto_link(inquiry_type, **kwargs):
    """Generate mailto link for given inquiry type"""
    template = CONTENT_TEMPLATES.get(inquiry_type, CONTENT_TEMPLATES["general"])
    body = template["body"].format(**kwargs)
    subject = template["subject"]
    return f"mailto:evans.mathibe@mail.com?subject={subject}&body={body}"


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        if sys.argv[1] == "generate":
            inquiry_type = sys.argv[2] if len(sys.argv) > 2 else "general"
            data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
            link = generate_mailto_link(inquiry_type, **data)
            print(link)
        else:
            print(json.dumps(CONTENT_TEMPLATES, indent=2))
    else:
        print("Usage: content_agent.py generate <inquiry_type> <json_data>")
