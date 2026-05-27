#!/usr/bin/env python3
"""Submit all site URLs to IndexNow (Bing, Yandex, Naver, Seznam)."""

import requests
import sys

BASE = "https://evansxm.github.io/evansmathibe-agency"
KEY = "93c56b1a6f1f4b1f8a2d3e4c5b6a7d8c"

URLS = [
    f"{BASE}/",
    f"{BASE}/solutions/",
    f"{BASE}/solutions/sandton-marketing/",
    f"{BASE}/solutions/cape-town-media/",
    f"{BASE}/solutions/durban-media/",
    f"{BASE}/solutions/rosebank-creative-corridor/",
    f"{BASE}/solutions/johannesburg-northern-suburbs/",
    f"{BASE}/solutions/illovo-melrose-arch/",
    f"{BASE}/solutions/centurion-media-hub/",
    f"{BASE}/solutions/pretoria-creative-districts/",
    f"{BASE}/solutions/midrand-media/",
    f"{BASE}/solutions/stellenbosch-digital/",
    f"{BASE}/solutions/gqeberha-digital/",
    f"{BASE}/solutions/bloemfontein-digital/",
    f"{BASE}/solutions/george-garden-route/",
    f"{BASE}/solutions/nelspruit-digital/",
]

PAYLOAD = {
    "host": "evansxm.github.io",
    "key": KEY,
    "keyLocation": f"{BASE}/{KEY}.txt",
    "urlList": URLS,
}

ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
    # "https://www.seznamsz.cz/indexnow",
]

success = True
for ep in ENDPOINTS:
    try:
        r = requests.post(ep, json=PAYLOAD, timeout=15)
        print(f"[{r.status_code}] {ep}")
        if r.status_code not in (200, 202):
            print(f"  Body: {r.text[:200]}")
            success = False
    except Exception as e:
        print(f"[ERR] {ep}: {e}")
        success = False

sys.exit(0 if success else 1)
