#!/usr/bin/env python3
"""
Checa o formato da resposta quando SUCCESS
"""
import requests
import json
import time

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

# Cria task
print("📤 Criando task...")
result = requests.post(
    f"{API_BASE_URL}/gpt4o-image/generate",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "prompt": "A cute dog",
        "size": "1:1",
        "nVariants": 1
    }
).json()

if result.get("code") == 200:
    task_id = result["data"]["taskId"]
    print(f"✅ Task ID: {task_id}\n")

    # Aguarda SUCCESS
    print("⏳ Aguardando SUCCESS...")
    max_wait = 120
    waited = 0

    while waited < max_wait:
        status_result = requests.get(
            f"{API_BASE_URL}/gpt4o-image/record-info",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={"taskId": task_id}
        ).json()

        if status_result.get("code") == 200:
            data = status_result.get("data", {})
            status = data.get("status", "UNKNOWN")
            progress = data.get("progress", "0")

            print(f"[{waited}s] {status} - {progress}%")

            if status == "SUCCESS":
                print("\n✅ SUCCESS! Resposta completa:")
                print("=" * 60)
                print(json.dumps(data, indent=2))
                break

        time.sleep(3)
        waited += 3

    if waited >= max_wait:
        print("\n⏰ Timeout")
