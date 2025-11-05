#!/usr/bin/env python3
"""
Teste completo do fluxo GPT-4o Image
"""
import requests
import json
import time

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

def create_task(prompt):
    response = requests.post(
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
    return response.json()

def check_status(task_id):
    response = requests.get(
        f"{API_BASE_URL}/gpt4o-image/record-info",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"taskId": task_id}
    )
    return response.json()

def wait_for_completion(task_id, max_wait=120):
    waited = 0
    while waited < max_wait:
        result = check_status(task_id)

        if result.get("code") == 200:
            data = result.get("data", {})
            status = data.get("status", "UNKNOWN")
            progress = data.get("progress", "0")

            print(f"   [{waited}s] Status: {status} | Progresso: {progress}%", flush=True)

            if status == "SUCCESS":
                response_data = data.get("response")
                if response_data:
                    if isinstance(response_data, str):
                        response_data = json.loads(response_data)

                    images = response_data.get("images", [])
                    return {"status": "success", "images": images}

            elif status in ["FAILED", "FAIL"]:
                error_msg = data.get("errorMessage", "Unknown error")
                return {"status": "failed", "error": error_msg}

        time.sleep(3)
        waited += 3

    return {"status": "timeout"}

# Teste: Criar 2 imagens em paralelo
print("🧪 Teste: Criar 2 imagens GPT-4o em paralelo")
print("=" * 60)

prompts = [
    "A modern minimalist office workspace",
    "A beautiful sunset over mountains"
]

tasks = []

# Cria tasks
for i, prompt in enumerate(prompts, 1):
    print(f"\n{i}. Criando: {prompt}")
    result = create_task(prompt)

    if result.get("code") == 200:
        task_id = result["data"]["taskId"]
        print(f"   ✅ Task ID: {task_id}")
        tasks.append({"id": task_id, "prompt": prompt})
    else:
        print(f"   ❌ Erro: {result}")

print(f"\n\n⏳ Aguardando conclusão...")
print("=" * 60)

# Aguarda todas
completed = []
for i, task in enumerate(tasks, 1):
    print(f"\n{i}. {task['prompt']}")
    result = wait_for_completion(task["id"])

    if result["status"] == "success":
        print(f"   ✅ SUCESSO! {len(result['images'])} imagem(ns)")
        for img_url in result['images']:
            print(f"      {img_url}")
        completed.append(result)
    else:
        print(f"   ❌ {result['status'].upper()}: {result.get('error', 'No error message')}")

print("\n" + "=" * 60)
print(f"🎉 Concluído! {len(completed)}/{len(tasks)} imagens geradas com sucesso")
