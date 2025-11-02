"""
Script para configurar grupo para apenas admins enviarem mensagens
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
import requests

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# ID do grupo
group_id = "120363406126089260@g.us"

print("=" * 60)
print("CONFIGURANDO GRUPO PARA APENAS ADMINS")
print("=" * 60)
print(f"\nGrupo ID: {group_id}")

try:
    # Configurar para apenas admins enviarem mensagens
    print("\nConfigurando para apenas admins enviarem mensagens...")

    url = f"{api.base_url}/group/updateSetting/{api.instance_name}?groupJid={group_id}"

    payload = {
        "action": "announcement"  # announcement = apenas admins
    }

    headers = {
        "apikey": api.api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()

    print("\n✅ GRUPO CONFIGURADO COM SUCESSO!")
    print(f"\nResposta: {result}")

    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO COMPLETA")
    print("=" * 60)
    print(f"\nAgora apenas administradores podem enviar mensagens no grupo!")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
