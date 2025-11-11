#!/usr/bin/env python3
"""
Testa diferentes endpoints de status para GPT-4o Image
"""
import requests
import json

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

# Primeiro cria uma task
print("📤 Criando task de teste...")
create_response = requests.post(
    f"{API_BASE_URL}/gpt4o-image/generate",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "prompt": "A cute cat",
        "size": "1:1",
        "nVariants": 1
    }
)

result = create_response.json()
print(f"Resposta criação: {json.dumps(result, indent=2)}\n")

if result.get("code") == 200:
    task_id = result["data"]["taskId"]
    print(f"Task ID: {task_id}\n")

    # Testa diferentes endpoints de status
    endpoints_to_test = [
        "/jobs/recordInfo",
        "/gpt4o-image/recordInfo",
        "/gpt4o-image/status",
        "/gpt4o-image/task",
        "/image/recordInfo",
    ]

    headers = {"Authorization": f"Bearer {API_KEY}"}

    for endpoint in endpoints_to_test:
        print(f"🧪 Testando: {endpoint}")
        url = f"{API_BASE_URL}{endpoint}"

        try:
            # Testa GET com taskId como parâmetro
            response = requests.get(url, headers=headers, params={"taskId": task_id})
            print(f"   GET (taskId): {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ SUCESSO: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"   ❌ {response.json()}")

        except Exception as e:
            print(f"   ❌ Erro: {e}")

        print()

else:
    print(f"❌ Erro ao criar task: {result}")
