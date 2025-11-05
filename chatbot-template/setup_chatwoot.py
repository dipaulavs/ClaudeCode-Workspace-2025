#!/usr/bin/env python3
"""
🔧 SETUP CHATWOOT - Criar Inbox Automaia
Cria inbox API no Chatwoot para o bot Automaia
"""

import requests
import json
import sys
from pathlib import Path

def criar_inbox_chatwoot(chatwoot_url, access_token, account_id, inbox_name):
    """Cria nova inbox no Chatwoot"""

    print(f"\n📥 Criando inbox '{inbox_name}'...")

    url = f"{chatwoot_url}/api/v1/accounts/{account_id}/inboxes"

    headers = {
        "api_access_token": access_token,
        "Content-Type": "application/json"
    }

    payload = {
        "name": inbox_name,
        "channel": {
            "type": "api",
            "webhook_url": ""
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code in [200, 201]:
            data = response.json()
            inbox_id = data.get('id')
            print(f"✅ Inbox criada com sucesso!")
            print(f"📍 Inbox ID: {inbox_id}")
            return inbox_id
        else:
            print(f"❌ Erro ao criar inbox: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def atualizar_config(chatwoot_token, inbox_id):
    """Atualiza chatwoot_config_automaia.json"""

    config_file = Path(__file__).parent / "chatwoot_config_automaia.json"

    with open(config_file, 'r') as f:
        config = json.load(f)

    config['chatwoot']['token'] = chatwoot_token
    config['chatwoot']['inbox_id'] = str(inbox_id)

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Arquivo atualizado: {config_file}")

def main():
    print("=" * 70)
    print("🔧 SETUP CHATWOOT - CRIAR INBOX AUTOMAIA")
    print("=" * 70)

    # Solicita dados
    print("\n📝 Para criar a inbox, preciso de:")
    print()

    chatwoot_url = input("1️⃣  URL do Chatwoot (ex: https://chatwoot.loop9.com.br): ").strip()
    if not chatwoot_url:
        chatwoot_url = "https://chatwoot.loop9.com.br"
        print(f"   Usando: {chatwoot_url}")

    print()
    print("2️⃣  Access Token do Chatwoot:")
    print("    Como pegar:")
    print("    - Faça login no Chatwoot")
    print("    - Clique no seu avatar (canto inferior esquerdo)")
    print("    - Profile Settings")
    print("    - Copie o 'Access Token'")
    print()
    access_token = input("    Cole o token aqui: ").strip()

    if not access_token:
        print("\n❌ Token é obrigatório!")
        sys.exit(1)

    print()
    account_id = input("3️⃣  Account ID (normalmente é '1'): ").strip()
    if not account_id:
        account_id = "1"
        print(f"   Usando: {account_id}")

    print()
    inbox_name = input("4️⃣  Nome da inbox (default: 'Automaia - Seminovos'): ").strip()
    if not inbox_name:
        inbox_name = "Automaia - Seminovos"
        print(f"   Usando: {inbox_name}")

    # Cria inbox
    inbox_id = criar_inbox_chatwoot(chatwoot_url, access_token, account_id, inbox_name)

    if not inbox_id:
        print("\n❌ Falha ao criar inbox")
        sys.exit(1)

    # Atualiza config
    atualizar_config(access_token, inbox_id)

    print()
    print("=" * 70)
    print("✅ SETUP CONCLUÍDO!")
    print("=" * 70)
    print()
    print("📋 Próximos passos:")
    print()
    print("1. Configurar webhook no Chatwoot:")
    print(f"   Inbox → {inbox_name} → Settings → Webhook")
    print("   URL: http://SEU_SERVIDOR:5004/webhook/chatwoot")
    print()
    print("2. Iniciar o bot:")
    print("   ./INICIAR_BOT_AUTOMAIA.sh")
    print()
    print("=" * 70)

if __name__ == '__main__':
    main()
