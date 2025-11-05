#!/usr/bin/env python3
"""
Teste direto da API KIE.AI para entender os endpoints
"""
import requests
import json
import time

API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
API_BASE_URL = "https://api.kie.ai/api/v1"

def test_create_task():
    """Testa criar uma task"""
    url = f"{API_BASE_URL}/jobs/createTask"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "google/nano-banana",
        "input": {
            "prompt": "A cute cat",
            "output_format": "png",
            "image_size": "1:1"
        }
    }

    print("📤 Criando task...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    response = requests.post(url, headers=headers, json=payload)

    print(f"\n📥 Resposta:")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}\n")

    if response.status_code == 200:
        data = response.json()
        task_id = data.get("data", {}).get("taskId")
        record_id = data.get("data", {}).get("recordId")
        print(f"✅ Task criada: {task_id}")
        print(f"   Record ID: {record_id}")
        return task_id, record_id
    else:
        print(f"❌ Erro ao criar task")
        return None, None


def test_query_task(task_id):
    """Testa diferentes endpoints de query"""
    endpoints = [
        f"{API_BASE_URL}/jobs/queryTask",
        f"{API_BASE_URL}/jobs/query",
        f"{API_BASE_URL}/jobs/status",
        f"{API_BASE_URL}/jobs/getTask",
        f"{API_BASE_URL}/jobs/get",
        f"{API_BASE_URL}/jobs/{task_id}",
        f"{API_BASE_URL}/tasks/{task_id}",
        f"{API_BASE_URL}/task/query",
        f"{API_BASE_URL}/task/{task_id}",
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    for endpoint in endpoints:
        print(f"\n🔍 Testando endpoint: {endpoint}")

        # Tenta POST
        print("   Método: POST")
        try:
            response = requests.post(endpoint, headers=headers, json={"taskId": task_id}, timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code != 404:
                print(f"   ✅ Resposta: {response.text[:200]}")
                return endpoint, "POST"
        except Exception as e:
            print(f"   ❌ Erro: {e}")

        # Tenta GET
        print("   Método: GET")
        try:
            response = requests.get(f"{endpoint}?taskId={task_id}", headers=headers, timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code != 404:
                print(f"   ✅ Resposta: {response.text[:200]}")
                return endpoint, "GET"
        except Exception as e:
            print(f"   ❌ Erro: {e}")

    return None, None


if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTE DIRETO DA API KIE.AI")
    print("="*60)

    # Cria uma task
    task_id, record_id = test_create_task()

    if task_id:
        print("\n" + "="*60)
        print("🔍 BUSCANDO ENDPOINT DE QUERY CORRETO")
        print("="*60)

        time.sleep(5)  # Aguarda um pouco

        # Tenta com taskId
        print("\n📍 Testando com taskId...")
        endpoint, method = test_query_task(task_id)

        if not endpoint and record_id != task_id:
            # Tenta com recordId
            print("\n📍 Testando com recordId...")
            endpoint, method = test_query_task(record_id)

        if endpoint:
            print(f"\n✅ Endpoint correto encontrado!")
            print(f"   URL: {endpoint}")
            print(f"   Método: {method}")
        else:
            print(f"\n❌ Nenhum endpoint funcionou")
            print(f"\n💡 Aguarde mais tempo e tente novamente...")
            print(f"   A task pode demorar para ficar disponível no sistema")
