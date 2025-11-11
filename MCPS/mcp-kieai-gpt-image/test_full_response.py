#!/usr/bin/env python3
"""
Mostra resposta completa da API
"""
import requests
import json
import time

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

print("📤 Criando task...")
create_response = requests.post(
    f"{API_BASE_URL}/gpt4o-image/generate",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "prompt": "A cute cat",
        "size": "1:1",
        "nVariants": 1,
        "enableFallback": True,
        "fallbackModel": "GPT_IMAGE_1"
    }
)

result = create_response.json()
print(f"✅ Resposta de criação:")
print(json.dumps(result, indent=2))

if result.get("code") == 200:
    task_id = result["data"]["taskId"]
    print(f"\nTask ID: {task_id}")

    # Aguarda um pouco e checa status
    print("\n⏳ Aguardando 5s...")
    time.sleep(5)

    print(f"\n📡 Checando status...")
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(
        f"{API_BASE_URL}/gpt4o-image/record-info",
        headers=headers,
        params={"taskId": task_id}
    )

    print(f"\nStatus HTTP: {response.status_code}")
    print(f"\nResposta completa do status:")
    print(json.dumps(response.json(), indent=2))
