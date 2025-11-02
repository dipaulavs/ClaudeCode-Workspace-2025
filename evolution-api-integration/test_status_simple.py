"""
Teste simples de status com timeout longo
"""

import requests
import json

url = "https://evolution.loop9.com.br/message/sendStatus/lfimoveis"

payload = {
    "type": "text",
    "content": "Teste via Evolution API! 🚀",
    "backgroundColor": "#008000",
    "font": 1,
    "allContacts": False,
    "statusJidList": ["5531980160822"]
}

headers = {
    "apikey": "178e43e1c4f459527e7008e57e378e1c",
    "Content-Type": "application/json"
}

print("Enviando status de texto...")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    # Timeout de 30 segundos
    response = requests.post(url, json=payload, headers=headers, timeout=30)

    print(f"\n✅ Status Code: {response.status_code}")

    if response.status_code in [200, 201]:
        print("✅ STATUS ENVIADO COM SUCESSO!")
        print(f"\nResposta: {response.json()}")
    else:
        print(f"❌ Erro: {response.text}")

except requests.exceptions.Timeout:
    print("\n❌ TIMEOUT: A API demorou mais de 30 segundos para responder")
    print("Isso indica que o servidor está com problemas no endpoint de status")

except Exception as e:
    print(f"\n❌ Erro: {e}")
