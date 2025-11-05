#!/usr/bin/env python3
"""
Testa criação de imagens esperando mais tempo
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
        "prompt": "A beautiful red rose",
        "size": "1:1",
        "nVariants": 1,
        "enableFallback": True,
        "fallbackModel": "GPT_IMAGE_1"
    }
)

result = create_response.json()
print(f"✅ Task criada: {json.dumps(result, indent=2)}\n")

if result.get("code") == 200:
    task_id = result["data"]["taskId"]
    print(f"Task ID: {task_id}")
    print("⏳ Aguardando processamento...\n")

    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Tenta por 90 segundos
    for attempt in range(45):  # 45 x 2s = 90s
        time.sleep(2)

        response = requests.get(
            f"{API_BASE_URL}/jobs/recordInfo",
            headers=headers,
            params={"taskId": task_id}
        )

        status_result = response.json()

        print(f"[{(attempt + 1) * 2}s] ", end="", flush=True)

        if status_result.get("code") == 200:
            data = status_result.get("data")
            if data:
                state = data.get("state", "unknown")
                print(f"Estado: {state}")

                if state == "success":
                    print(f"\n✅ SUCESSO!")
                    print(f"Resultado completo:")
                    print(json.dumps(data, indent=2))

                    result_json = data.get("resultJson", {})
                    if isinstance(result_json, str):
                        result_json = json.loads(result_json)

                    images = result_json.get("images", [])
                    print(f"\n🖼️  Imagens geradas: {len(images)}")
                    for i, img_url in enumerate(images, 1):
                        print(f"   {i}. {img_url}")
                    break
                elif state == "fail":
                    print(f"\n❌ FALHOU!")
                    print(json.dumps(data, indent=2))
                    break
                else:
                    print(f"Processando...")
            else:
                print("Sem dados ainda (recordInfo null)")
        else:
            print(f"Erro: {status_result.get('msg')}")

    else:
        print(f"\n⏰ Timeout após 90 segundos")
else:
    print(f"❌ Erro ao criar task: {result}")
