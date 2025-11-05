#!/usr/bin/env python3
"""
🚀 SETUP COMPLETO - LF Imóveis
Automatiza: Criação inbox Chatwoot + Conexão Evolution + Config
"""

import requests
import json
import sys
from pathlib import Path

# ============= CREDENCIAIS (mesmas do Automaia) =============
CHATWOOT_URL = "https://chatwoot.loop9.com.br"
CHATWOOT_TOKEN = "xp1AcWvf6F2p2ZypabNWHfW6"
ACCOUNT_ID = "1"

EVOLUTION_URL = "https://evolution.loop9.com.br"
EVOLUTION_API_KEY = "178e43e1c4f459527e7008e57e378e1c"
INSTANCE_NAME = "lfimoveis"

INBOX_NAME = "LF Imoveis"
CONFIG_FILE = Path(__file__).parent / "chatwoot_config_imobili-ria-premium.json"


def verificar_instancia_evolution():
    """Verifica se instância lfimoveis existe na Evolution"""
    print("\n🔍 Verificando instância 'lfimoveis' na Evolution...")

    url = f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE_NAME}"
    headers = {"apikey": EVOLUTION_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            state = data.get('instance', {}).get('state')
            print(f"✅ Instância encontrada! Status: {state}")
            return True
        else:
            print(f"⚠️  Instância não encontrada (status: {response.status_code})")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao verificar instância: {e}")
        return False


def criar_inbox_chatwoot():
    """Cria inbox 'LF Imoveis' no Chatwoot"""
    print(f"\n📥 Criando inbox '{INBOX_NAME}' no Chatwoot...")

    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes"

    headers = {
        "api_access_token": CHATWOOT_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "name": INBOX_NAME,
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
            webhook_url = data.get('webhook_url', '')
            print(f"✅ Inbox criada com sucesso!")
            print(f"   Inbox ID: {inbox_id}")
            print(f"   Webhook URL: {webhook_url}")
            return inbox_id, webhook_url
        else:
            print(f"❌ Erro ao criar inbox: {response.status_code}")
            print(f"   Resposta: {response.text}")

            # Tentar buscar inbox existente
            print(f"\n🔍 Verificando se inbox já existe...")
            return buscar_inbox_existente()

    except Exception as e:
        print(f"❌ Erro: {e}")
        return None, None


def buscar_inbox_existente():
    """Busca inbox existente pelo nome"""
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes"
    headers = {"api_access_token": CHATWOOT_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            inboxes = response.json().get('payload', [])

            for inbox in inboxes:
                if inbox.get('name') == INBOX_NAME:
                    inbox_id = inbox.get('id')
                    webhook_url = inbox.get('webhook_url', '')
                    print(f"✅ Inbox '{INBOX_NAME}' já existe!")
                    print(f"   Inbox ID: {inbox_id}")
                    return inbox_id, webhook_url

        print(f"⚠️  Inbox '{INBOX_NAME}' não encontrada")
        return None, None

    except Exception as e:
        print(f"❌ Erro ao buscar inbox: {e}")
        return None, None


def configurar_webhook_evolution(webhook_url):
    """Configura webhook da Evolution para enviar para Chatwoot"""
    print(f"\n🔗 Configurando webhook Evolution → Chatwoot...")

    url = f"{EVOLUTION_URL}/webhook/set/{INSTANCE_NAME}"
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "url": webhook_url,
        "webhook_by_events": False,
        "webhook_base64": False,
        "events": [
            "QRCODE_UPDATED",
            "MESSAGES_UPSERT",
            "MESSAGES_UPDATE",
            "SEND_MESSAGE",
            "CONNECTION_UPDATE"
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code in [200, 201]:
            print(f"✅ Webhook configurado!")
            return True
        else:
            print(f"⚠️  Webhook não configurado (status: {response.status_code})")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao configurar webhook: {e}")
        return False


def atualizar_config(inbox_id):
    """Atualiza chatwoot_config_imobili-ria-premium.json"""
    print(f"\n📝 Atualizando configuração...")

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        config['chatwoot']['token'] = CHATWOOT_TOKEN
        config['chatwoot']['inbox_id'] = str(inbox_id)
        config['evolution']['api_key'] = EVOLUTION_API_KEY
        config['evolution']['instance'] = INSTANCE_NAME

        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"✅ Config atualizado: {CONFIG_FILE.name}")
        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar config: {e}")
        return False


def main():
    print("=" * 70)
    print("🚀 SETUP COMPLETO - LF IMÓVEIS")
    print("=" * 70)
    print()
    print("📋 Configurações:")
    print(f"   Chatwoot: {CHATWOOT_URL}")
    print(f"   Evolution: {EVOLUTION_URL}")
    print(f"   Instância: {INSTANCE_NAME}")
    print(f"   Inbox: {INBOX_NAME}")
    print()

    # 1. Verificar instância Evolution
    if not verificar_instancia_evolution():
        print("\n⚠️  ATENÇÃO: Instância 'lfimoveis' não encontrada na Evolution!")
        print("   Você pode continuar, mas precisará criar/conectar a instância depois.")
        resp = input("\n   Continuar mesmo assim? (s/n): ").strip().lower()
        if resp != 's':
            sys.exit(0)

    # 2. Criar inbox Chatwoot
    inbox_id, webhook_url = criar_inbox_chatwoot()

    if not inbox_id:
        print("\n❌ Não foi possível criar/encontrar inbox no Chatwoot")
        sys.exit(1)

    # 3. Configurar webhook Evolution (se instância existe)
    if webhook_url:
        configurar_webhook_evolution(webhook_url)

    # 4. Atualizar config
    if not atualizar_config(inbox_id):
        print("\n❌ Falha ao atualizar configuração")
        sys.exit(1)

    # Resumo final
    print()
    print("=" * 70)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print()
    print("📋 RESUMO:")
    print(f"   ✅ Inbox Chatwoot: {INBOX_NAME} (ID: {inbox_id})")
    print(f"   ✅ Instância Evolution: {INSTANCE_NAME}")
    print(f"   ✅ Config atualizado: {CONFIG_FILE.name}")
    print()
    print("🔗 PRÓXIMOS PASSOS:")
    print()
    print("1️⃣  Se instância 'lfimoveis' não existe na Evolution:")
    print("   - Acesse: https://evolution.loop9.com.br")
    print("   - Crie instância 'lfimoveis'")
    print("   - Conecte QR Code do WhatsApp")
    print()
    print("2️⃣  Criar agenda Google Sheets:")
    print("   cd whatsapp-chatbot-imobili-ria-premium")
    print("   python3 componentes/escalonamento/autenticar_google.py")
    print("   python3 componentes/escalonamento/criar_agenda_publica_oauth.py")
    print()
    print("3️⃣  Adicionar imóveis:")
    print("   - Criar pastas em imoveis/")
    print("   - Preencher arquivos .txt")
    print()
    print("4️⃣  Iniciar bot:")
    print("   ./INICIAR_COM_NGROK.sh")
    print()
    print("=" * 70)


if __name__ == '__main__':
    main()
