#!/usr/bin/env python3
"""
EvansMathibe Agency - Stripe Payment Integration
Handles payment processing for services
"""

import os
import json
from datetime import datetime
from pathlib import Path

try:
    import stripe

    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    print("Warning: Stripe not installed. Install with: pip install stripe")

AGENCY_ROOT = Path("/home/ev/EvansMathibe_Agency")
CONFIG_FILE = AGENCY_ROOT / "config" / "stripe_config.json"

SERVICES_PRICING = {
    "photography": {
        "name": "Photography Session",
        "description": "Professional photography for events, products, portraits",
        "prices": {"basic": 5000, "standard": 12000, "premium": 25000},
    },
    "film": {
        "name": "Film Production",
        "description": "Commercials, documentaries, corporate videos",
        "prices": {"basic": 15000, "standard": 45000, "premium": 100000},
    },
    "advertising": {
        "name": "Advertising Campaign",
        "description": "Digital and traditional media campaigns",
        "prices": {"basic": 10000, "standard": 30000, "premium": 75000},
    },
    "brand_management": {
        "name": "Brand Management",
        "description": "Brand strategy, positioning, identity",
        "prices": {"basic": 8000, "standard": 20000, "premium": 50000},
    },
    "event_management": {
        "name": "Event Design & Management",
        "description": "Full-service event planning and production",
        "prices": {"basic": 15000, "standard": 40000, "premium": 100000},
    },
    "creative": {
        "name": "Creative Services",
        "description": "Creative direction, concept development",
        "prices": {"basic": 5000, "standard": 15000, "premium": 35000},
    },
    "design": {
        "name": "Design Services",
        "description": "Graphic design, UI/UX, visual communication",
        "prices": {"basic": 3000, "standard": 8000, "premium": 20000},
    },
    "pr": {
        "name": "Public Relations",
        "description": "PR strategies, media relations",
        "prices": {"basic": 7000, "standard": 18000, "premium": 45000},
    },
    "ai_automation": {
        "name": "AI Brand Automation",
        "description": "AI-powered marketing automation",
        "prices": {"basic": 10000, "standard": 25000, "premium": 60000},
    },
}


class StripePaymentHandler:
    def __init__(self, api_key: str = None):
        if not STRIPE_AVAILABLE:
            raise RuntimeError("Stripe package not installed")

        self.api_key = api_key or os.environ.get("STRIPE_API_KEY")
        if not self.api_key:
            print("No Stripe API key provided. Using test mode.")
            self.stripe = None
        else:
            stripe.api_key = self.api_key
            self.stripe = stripe

    def create_checkout_session(
        self,
        service: str,
        tier: str = "standard",
        success_url: str = None,
        cancel_url: str = None,
    ):
        if not self.stripe:
            return self._create_mock_session(service, tier)

        service_info = SERVICES_PRICING.get(service.lower())
        if not service_info:
            raise ValueError(f"Unknown service: {service}")

        price = service_info["prices"].get(
            tier.lower(), service_info["prices"]["standard"]
        )

        try:
            session = self.stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "zar",
                            "product_data": {
                                "name": f"{service_info['name']} - {tier.title()}",
                                "description": service_info["description"],
                            },
                            "unit_amount": price * 100,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url
                or "https://evansxm.github.io/evansmathibe-agency/success.html",
                cancel_url=cancel_url
                or "https://evansxm.github.io/evansmathibe-agency/cancel.html",
            )
            return {"url": session.url, "session_id": session.id, "amount": price}
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def _create_mock_session(self, service: str, tier: str):
        service_info = SERVICES_PRICING.get(service.lower(), {})
        price = service_info.get("prices", {}).get(tier.lower(), 0)
        return {
            "mock": True,
            "service": service,
            "tier": tier,
            "amount": price,
            "currency": "ZAR",
            "note": "Stripe not configured - mock payment session",
        }

    def create_payment_link(self, service: str, tier: str = "standard"):
        service_info = SERVICES_PRICING.get(service.lower())
        if not service_info:
            return None

        price = service_info["prices"].get(tier.lower())

        if self.stripe:
            try:
                product = self.stripe.Product.create(
                    name=f"{service_info['name']} - {tier.title()}",
                    description=service_info["description"],
                )
                price_obj = self.stripe.Price.create(
                    unit_amount=price * 100, currency="zar", product=product.id
                )
                link = self.stripe.PaymentLink.create(
                    line_items=[{"price": price_obj.id, "quantity": 1}]
                )
                return {"url": link.url, "price": price}
            except stripe.error.StripeError as e:
                return {"error": str(e)}

        return {"amount": price, "note": "Stripe not configured"}


def get_payment_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"mode": "test", "currency": "zar", "webhook_secret": None, "api_key": None}


def main():
    import sys

    handler = StripePaymentHandler()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "services":
            print("\nServices with Pricing (in ZAR):")
            print("=" * 50)
            for key, service in SERVICES_PRICING.items():
                print(f"\n{service['name']}:")
                for tier, price in service["prices"].items():
                    print(f"  {tier.title()}: R{price:,}")

        elif command == "create" and len(sys.argv) > 2:
            service = sys.argv[2]
            tier = sys.argv[3] if len(sys.argv) > 3 else "standard"
            result = handler.create_checkout_session(service, tier)
            print(json.dumps(result, indent=2))

        elif command == "link" and len(sys.argv) > 2:
            service = sys.argv[2]
            tier = sys.argv[3] if len(sys.argv) > 3 else "standard"
            result = handler.create_payment_link(service, tier)
            print(json.dumps(result, indent=2))
    else:
        print("EvansMathibe Stripe Payment System")
        print("=" * 40)
        print("Commands:")
        print(
            "  python payment.py services              - List all services and prices"
        )
        print("  python payment.py create <service> [tier] - Create checkout session")
        print("  python payment.py link <service> [tier]   - Create payment link")
        print("\nNote: Set STRIPE_API_KEY env var for live payments")


if __name__ == "__main__":
    main()
