#!/usr/bin/env python3
"""
Teste direto da API GPT-4o Image (sem MCP)
"""
import requests
import time
import json

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

def create_task(prompt, size="1:1", n_variants=1):
    """Cria task de geração"""
    url = f"{API_BASE_URL}/gpt4o-image/generate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "prompt": prompt,
        "size": size,
        "nVariants": n_variants,
        "enableFallback": True,
        "fallbackModel": "GPT_IMAGE_1"
    }

    print(f"📤 Enviando: {prompt}")
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def check_status(task_id):
    """Checa status da task"""
    url = f"{API_BASE_URL}/jobs/recordInfo"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"taskId": task_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def wait_task(task_id, max_wait=60):
    """Aguarda conclusão"""
    waited = 0
    while waited < max_wait:
        result = check_status(task_id)

        if result.get("code") != 200:
            return result

        data = result.get("data", {})
        state = data.get("state")

        if state == "success":
            return result
        elif state == "fail":
            return result

        time.sleep(2)
        waited += 2

    return {"code": 408, "message": "Timeout"}

# Teste 1: Criar 2 imagens
print("🧪 Teste 1: Criar 2 imagens")
print("=" * 60)

prompts = [
    "A professional photo of a modern workspace with laptop",
    "A serene mountain landscape at golden hour"
]

results = []
for i, prompt in enumerate(prompts, 1):
    print(f"\n{i}. {prompt}")

    # Cria task
    task_result = create_task(prompt, size="1:1", n_variants=1)
    print(f"   Response: {json.dumps(task_result, indent=2)}")

    if task_result.get("code") == 200:
        task_id = task_result["data"]["taskId"]
        print(f"   Task ID: {task_id}")

        # Aguarda
        print(f"   ⏳ Aguardando...")
        final_result = wait_task(task_id)

        if final_result.get("code") == 200:
            data = final_result["data"]
            state = data.get("state")
            print(f"   ✅ Status: {state}")

            if state == "success":
                result_json = data.get("resultJson", {})
                if isinstance(result_json, str):
                    result_json = json.loads(result_json)

                images = result_json.get("images", [])
                print(f"   🖼️  Imagens: {len(images)}")
                for img_url in images:
                    print(f"      {img_url}")

                results.append({
                    "prompt": prompt,
                    "status": "success",
                    "images": images
                })
        else:
            print(f"   ❌ Erro: {final_result}")
            results.append({"prompt": prompt, "status": "error"})
    else:
        print(f"   ❌ Erro ao criar task: {task_result}")
        results.append({"prompt": prompt, "status": "error"})

print("\n" + "=" * 60)
print(f"✅ Teste concluído! {len([r for r in results if r.get('status') == 'success'])}/{len(results)} sucesso")
