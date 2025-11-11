"""
Script para enviar status de texto (tentativa corrigida)
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
import requests

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

print("=" * 60)
print("ENVIANDO STATUS DE TEXTO")
print("=" * 60)

try:
    # Preparar a requisição direta
    url = f"{api.base_url}/message/sendStatus/{api.instance_name}"

    payload = {
        "type": "text",
        "content": "Testando status via Evolution API! 🚀",
        "backgroundColor": "#FF5733",  # Laranja
        "font": 2,  # NORICAN_REGULAR
        "allContacts": True,  # Enviar para todos os contatos
        "statusJidList": []
    }

    headers = {
        "apikey": api.api_key,
        "Content-Type": "application/json"
    }

    print(f"\nURL: {url}")
    print(f"Payload: {payload}")
    print("\nEnviando status...")

    response = requests.post(url, json=payload, headers=headers)

    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 201 or response.status_code == 200:
        result = response.json()
        print("\n✅ STATUS PUBLICADO COM SUCESSO!")
        print(f"\nResposta completa:")
        print(result)
    else:
        print(f"\n❌ ERRO: {response.status_code}")
        print(f"Resposta: {response.text}")
        response.raise_for_status()

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
