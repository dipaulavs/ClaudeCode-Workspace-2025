#!/usr/bin/env python3
"""
Lista TODAS as campanhas (ativas, pausadas, rascunhos)
"""

import requests

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"

params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'id,name,status,effective_status,objective,created_time',
    'limit': 100
}

response = requests.get(url, params=params)
data = response.json()

campaigns = data.get('data', [])

print(f"\n📊 TODAS AS CAMPANHAS ({len(campaigns)} total):\n")
print("=" * 100)

for idx, c in enumerate(campaigns, 1):
    print(f"\n{idx}. {c['name']}")
    print(f"   ID: {c['id']}")
    print(f"   Status: {c.get('status')} | Effective: {c.get('effective_status')}")
    print(f"   Objetivo: {c.get('objective')}")
    print(f"   Criada: {c.get('created_time', '')[:10]}")

print("\n" + "=" * 100)
