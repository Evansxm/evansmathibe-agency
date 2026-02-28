#!/usr/bin/env python3
"""
Evans Mathibe Google Sites Agent
Runs as a service to help manage the website
"""

import os
import json
import subprocess
import time

STATE_FILE = "/home/ev/evansmathibe/site_state.json"


class EvansSitesAgent:
    def __init__(self):
        self.state = self.load_state()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                return json.load(f)
        return {"status": "new", "site_url": None, "pages": []}

    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def open(self):
        """Open all resources"""
        print("🌐 Opening Google Sites and resources...")
        subprocess.Popen(["google-chrome", "https://sites.google.com"])
        time.sleep(1)
        subprocess.Popen(
            ["google-chrome", "/home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md"]
        )
        time.sleep(1)
        subprocess.Popen(["google-chrome", "/home/ev/evansmathibe/index.html"])

    def set_url(self, url):
        """Save the published URL"""
        self.state["site_url"] = url
        self.state["status"] = "published"
        self.save_state()
        print(f"✅ Saved site URL: {url}")

    def show_status(self):
        """Show current status"""
        print("\n📊 Evans Mathibe Website Status")
        print("=" * 40)
        print(f"Status: {self.state['status']}")
        print(f"URL: {self.state.get('site_url', 'Not published')}")
        print(f"Pages: {', '.join(self.state.get('pages', [])) or 'None'}")

    def run(self):
        """Main menu"""
        while True:
            print("""
╔═══════════════════════════════════════╗
║  EVANS MATHIBE - GOOGLE SITES AGENT   ║
╠═══════════════════════════════════════╣
║  1. Open Google Sites Editor          ║
║  2. View Content Guide                ║
║  3. Preview Landing Page              ║
║  4. Open Assets Folder                ║
║  5. Save Published URL                ║
║  6. Show Status                       ║
║  7. Exit                              ║
╚═══════════════════════════════════════╝
            """)

            choice = input("Select: ").strip()

            if choice == "1":
                self.open()
            elif choice == "2":
                subprocess.Popen(
                    ["google-chrome", "/home/ev/evansmathibe/GOOGLE_SITES_GUIDE.md"]
                )
            elif choice == "3":
                subprocess.Popen(["google-chrome", "/home/ev/evansmathibe/index.html"])
            elif choice == "4":
                subprocess.Popen(["xdg-open", "/home/ev/evansmathibe/assets"])
            elif choice == "5":
                url = input("Enter published URL: ").strip()
                self.set_url(url)
            elif choice == "6":
                self.show_status()
            elif choice == "7":
                print("👋 Goodbye!")
                break


if __name__ == "__main__":
    agent = EvansSitesAgent()

    # Check for command line args
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "open":
            agent.open()
        elif sys.argv[1] == "status":
            agent.show_status()
        elif sys.argv[1] == "set" and len(sys.argv) > 2:
            agent.set_url(sys.argv[2])
    else:
        agent.run()
