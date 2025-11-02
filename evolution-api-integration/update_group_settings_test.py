#!/usr/bin/env python3
"""
Script para atualizar configurações do grupo criado
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def update_group_settings(api: EvolutionAPI, group_id: str, setting: str) -> dict:
    """Atualiza configurações do grupo"""
    endpoint = f"/group/updateSetting/{api.instance_name}?groupJid={group_id}"
    data = {"action": setting}
    return api._make_request('POST', endpoint, data)


def main():
    # ID do grupo criado anteriormente
    group_id = "120363423739033485@g.us"

    print("🔄 Inicializando Evolution API...")
    api = EvolutionAPI(
        base_url=EVOLUTION_API_URL,
        api_key=EVOLUTION_API_KEY,
        instance_name=EVOLUTION_INSTANCE_NAME
    )

    print(f"\n⚙️ Configurando grupo {group_id} para apenas admins enviarem mensagens...")
    try:
        response = update_group_settings(
            api=api,
            group_id=group_id,
            setting="announcement"
        )
        print(f"✅ Configurações do grupo atualizadas com sucesso!")
        print(f"   Response: {response}")
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
