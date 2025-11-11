#!/usr/bin/env python3
import requests

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"

url = f"https://graph.facebook.com/{API_VERSION}/{AD_ACCOUNT_ID}/campaigns"
params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'id,name,status,effective_status,objective',
    'limit': 100
}

response = requests.get(url, params=params)
campaigns = response.json().get('data', [])

print(f"\n📊 CAMPANHAS NA CONTA CA - 01 DIP ({len(campaigns)} total):\n")
print("=" * 100)

for idx, c in enumerate(campaigns, 1):
    status_icon = "🟢" if c.get('effective_status') == 'ACTIVE' else "⏸️"
    print(f"\n{idx}. {status_icon} {c['name']}")
    print(f"   ID: {c['id']}")
    print(f"   Status: {c.get('effective_status')}")
    print(f"   Objetivo: {c.get('objective')}")

print("\n" + "=" * 100 + "\n")
