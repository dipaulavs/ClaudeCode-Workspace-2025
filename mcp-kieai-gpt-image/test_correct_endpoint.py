#!/usr/bin/env python3
"""
Testa com o endpoint correto: /gpt4o-image/record-info
"""
import requests
import json
import time

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

print("📤 Criando 2 tasks em paralelo...")
print("=" * 60)

prompts = [
    "A professional photo of a modern workspace",
    "A serene mountain landscape"
]

tasks = []

# Cria as 2 tasks
for i, prompt in enumerate(prompts, 1):
    print(f"\n{i}. Criando: {prompt}")
    create_response = requests.post(
        f"{API_BASE_URL}/gpt4o-image/generate",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "prompt": prompt,
            "size": "1:1",
            "nVariants": 1,
            "enableFallback": True,
            "fallbackModel": "GPT_IMAGE_1"
        }
    )

    result = create_response.json()
    if result.get("code") == 200:
        task_id = result["data"]["taskId"]
        print(f"   ✅ Task ID: {task_id}")
        tasks.append({"id": task_id, "prompt": prompt})
    else:
        print(f"   ❌ Erro: {result}")

print(f"\n\n⏳ Aguardando conclusão de {len(tasks)} tasks...")
print("=" * 60)

headers = {"Authorization": f"Bearer {API_KEY}"}

# Aguarda conclusão de todas
max_wait = 90
waited = 0
completed = []

while waited < max_wait and len(completed) < len(tasks):
    time.sleep(2)
    waited += 2

    print(f"\n[{waited}s] Checando status...")

    for task in tasks:
        if task["id"] in [c["id"] for c in completed]:
            continue

        # Testa o endpoint correto
        response = requests.get(
            f"{API_BASE_URL}/gpt4o-image/record-info",
            headers=headers,
            params={"taskId": task["id"]}
        )

        status_result = response.json()

        if status_result.get("code") == 200:
            data = status_result.get("data")
            if data:
                state = data.get("state", "unknown")
                print(f"   Task {task['id'][:8]}... : {state}")

                if state == "success":
                    result_json = data.get("resultJson", {})
                    if isinstance(result_json, str):
                        result_json = json.loads(result_json)

                    images = result_json.get("images", [])
                    print(f"      ✅ Imagens: {len(images)}")
                    for img_url in images:
                        print(f"         {img_url}")

                    completed.append({
                        "id": task["id"],
                        "prompt": task["prompt"],
                        "images": images
                    })
                elif state == "fail":
                    print(f"      ❌ Falhou")
                    completed.append({
                        "id": task["id"],
                        "prompt": task["prompt"],
                        "status": "failed"
                    })
            else:
                print(f"   Task {task['id'][:8]}... : Aguardando...")
        else:
            print(f"   Task {task['id'][:8]}... : Erro - {status_result.get('msg')}")

if len(completed) == len(tasks):
    print(f"\n✅ SUCESSO! Todas as {len(completed)} imagens foram geradas!")
else:
    print(f"\n⏰ Timeout - {len(completed)}/{len(tasks)} concluídas")

print("\n" + "=" * 60)
print("Resumo Final:")
for i, task in enumerate(completed, 1):
    print(f"{i}. {task['prompt']}")
    if 'images' in task:
        print(f"   🖼️  {len(task['images'])} imagem(ns)")
