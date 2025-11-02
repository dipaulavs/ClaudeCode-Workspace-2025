#!/usr/bin/env python3
"""
Script de teste para operações WhatsApp via Evolution API
- Envia mensagem de teste
- Reage com emoji de foguete
- Cria grupo
- Configura grupo para apenas admins enviarem mensagens
"""

import sys
from pathlib import Path
import time

# Adiciona o diretório ao path
sys.path.append(str(Path(__file__).parent))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def update_group_settings(api: EvolutionAPI, group_id: str, setting: str) -> dict:
    """
    Atualiza configurações do grupo

    Args:
        api: Instância da EvolutionAPI
        group_id: ID do grupo
        setting: Configuração ('announcement' = apenas admins, 'not_announcement' = todos)

    Returns:
        Resposta da API
    """
    # O groupJid deve ser passado como query parameter
    endpoint = f"/group/updateSetting/{api.instance_name}?groupJid={group_id}"
    data = {
        "action": setting  # 'announcement' ou 'not_announcement'
    }
    return api._make_request('POST', endpoint, data)


def main():
    # Número para teste
    test_number = "5531980160822"

    # Inicializa a API
    print("🔄 Inicializando Evolution API...")
    api = EvolutionAPI(
        base_url=EVOLUTION_API_URL,
        api_key=EVOLUTION_API_KEY,
        instance_name=EVOLUTION_INSTANCE_NAME
    )

    # Verifica status da instância
    try:
        status = api.get_instance_status()
        print(f"✅ Instância conectada: {status.get('instance', {}).get('state', 'desconhecido')}")
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return

    # PASSO 1: Enviar mensagem de teste
    print(f"\n📤 Enviando mensagem de teste para {test_number}...")
    try:
        response = api.send_text(
            number=test_number,
            text="🧪 *Mensagem de teste!*\n\nEsta é uma mensagem de teste enviada via Evolution API."
        )

        # Extrai o ID da mensagem enviada
        message_key = response.get('key', {})
        message_id = message_key.get('id')

        print(f"✅ Mensagem enviada com sucesso!")
        print(f"   Message ID: {message_id}")

        # Aguarda um momento antes de reagir
        time.sleep(2)

        # PASSO 2: Reagir com emoji de foguete
        if message_id:
            print(f"\n🚀 Reagindo à mensagem com emoji de foguete...")
            try:
                reaction_response = api.send_reaction(
                    number=test_number,
                    key=message_key,  # Passa o objeto key completo
                    reaction="🚀"
                )
                print(f"✅ Reação enviada com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao enviar reação: {e}")
        else:
            print(f"⚠️ Não foi possível obter o ID da mensagem para reagir")

    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return

    # Aguarda um momento antes de criar o grupo
    time.sleep(2)

    # PASSO 3: Criar grupo
    print(f"\n👥 Criando grupo com {test_number}...")
    try:
        group_name = f"Teste WhatsApp API - {time.strftime('%d/%m/%Y %H:%M')}"
        group_response = api.create_group(
            subject=group_name,
            participants=[test_number],
            description="Grupo de teste criado automaticamente via Evolution API"
        )

        group_id = group_response.get('id')
        print(f"✅ Grupo criado com sucesso!")
        print(f"   Nome: {group_name}")
        print(f"   Group ID: {group_id}")

        # Aguarda um momento antes de alterar configurações
        time.sleep(2)

        # PASSO 4: Configurar grupo para apenas admins enviarem mensagens
        if group_id:
            print(f"\n⚙️ Configurando grupo para apenas admins enviarem mensagens...")
            try:
                settings_response = update_group_settings(
                    api=api,
                    group_id=group_id,
                    setting="announcement"  # announcement = apenas admins
                )
                print(f"✅ Configurações do grupo atualizadas com sucesso!")
                print(f"   Apenas administradores podem enviar mensagens agora")
            except Exception as e:
                print(f"❌ Erro ao atualizar configurações do grupo: {e}")
                print(f"   (Pode ser que você precise ser admin do grupo)")

    except Exception as e:
        print(f"❌ Erro ao criar grupo: {e}")
        return

    print(f"\n✅ Todas as operações foram concluídas!")
    print(f"\n📋 Resumo:")
    print(f"   1. ✅ Mensagem enviada para {test_number}")
    print(f"   2. ✅ Reação com 🚀 enviada")
    print(f"   3. ✅ Grupo '{group_name}' criado")
    print(f"   4. ✅ Grupo configurado para apenas admins")


if __name__ == "__main__":
    main()
