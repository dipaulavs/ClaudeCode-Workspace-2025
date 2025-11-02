#!/usr/bin/env python3
"""
🤖 SETUP AUTOMÁTICO - CHATWOOT + EVOLUTION API
Configura integração híbrida: Bot automático + Atendimento humano
"""

import requests
import json
import sys

# ========== CONFIGURAÇÕES ==========
CHATWOOT_URL = "https://chatwoot.loop9.com.br"
CHATWOOT_TOKEN = "xp1AcWvf6F2p2ZypabNWHfW6"
ACCOUNT_ID = 1

EVOLUTION_URL = "https://evolution.loop9.com.br"
EVOLUTION_API_KEY = "178e43e1c4f459527e7008e57e378e1c"
EVOLUTION_INSTANCE = "lfimoveis"

# URL pública do webhook (você vai configurar com ngrok depois)
WEBHOOK_URL_BASE = "https://SEU-NGROK-URL-AQUI.ngrok-free.app"  # Alterar depois

# ===================================

def criar_inbox_whatsapp():
    """
    Cria inbox WhatsApp no Chatwoot conectado à Evolution API
    """
    print("\n" + "="*70)
    print("📥 PASSO 1: Criando Inbox WhatsApp no Chatwoot")
    print("="*70)

    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes"

    headers = {
        "api_access_token": CHATWOOT_TOKEN,
        "Content-Type": "application/json"
    }

    # Dados do inbox
    # Chatwoot suporta diferentes tipos de inbox WhatsApp
    # Vamos usar "api" channel que permite integração customizada
    payload = {
        "name": "WhatsApp - LF Imóveis",
        "channel": {
            "type": "api",
            "webhook_url": "",  # Será configurado depois
            "additional_attributes": {
                "provider": "evolution_api",
                "provider_url": EVOLUTION_URL,
                "instance_name": EVOLUTION_INSTANCE
            }
        }
    }

    try:
        print(f"📤 Enviando requisição para criar inbox...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print(f"📊 Status Code: {response.status_code}")

        if response.status_code in [200, 201]:
            inbox = response.json()
            print(f"✅ Inbox criado com sucesso!")
            print(f"📋 ID: {inbox.get('id')}")
            print(f"📋 Nome: {inbox.get('name')}")
            print(f"📋 Channel ID: {inbox.get('channel_id')}")

            # Salva configuração em arquivo
            config = {
                "inbox_id": inbox.get('id'),
                "inbox_name": inbox.get('name'),
                "channel_id": inbox.get('channel_id'),
                "channel_type": inbox.get('channel_type'),
                "webhook_url": inbox.get('webhook_url', '')
            }

            with open('chatwoot_config.json', 'w') as f:
                json.dump(config, f, indent=2)

            print(f"💾 Configuração salva em: chatwoot_config.json")

            return inbox
        else:
            print(f"❌ Erro ao criar inbox!")
            print(f"📄 Resposta: {response.text}")

            # Talvez o inbox já existe? Vamos listar
            print("\n🔍 Verificando inboxes existentes...")
            listar_inboxes()

            return None

    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        import traceback
        traceback.print_exc()
        return None

def listar_inboxes():
    """Lista todos os inboxes existentes"""
    print("\n" + "="*70)
    print("📋 Listando Inboxes Existentes")
    print("="*70)

    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes"

    headers = {
        "api_access_token": CHATWOOT_TOKEN
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        inboxes = response.json().get('payload', [])

        if not inboxes:
            print("⚠️  Nenhum inbox encontrado.")
            return []

        print(f"✅ {len(inboxes)} inbox(es) encontrado(s):\n")

        for inbox in inboxes:
            print(f"📥 ID: {inbox.get('id')}")
            print(f"   Nome: {inbox.get('name')}")
            print(f"   Tipo: {inbox.get('channel_type')}")
            print(f"   Webhook: {inbox.get('webhook_url', 'N/A')}")
            print()

        return inboxes

    except Exception as e:
        print(f"❌ Erro ao listar inboxes: {e}")
        return []

def atualizar_webhook_chatwoot(inbox_id, webhook_url):
    """
    Atualiza URL do webhook no inbox do Chatwoot
    """
    print("\n" + "="*70)
    print("🔄 PASSO 2: Atualizando Webhook do Inbox")
    print("="*70)

    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes/{inbox_id}"

    headers = {
        "api_access_token": CHATWOOT_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "channel": {
            "webhook_url": webhook_url
        }
    }

    try:
        print(f"📤 Atualizando webhook para: {webhook_url}")
        response = requests.patch(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            print(f"✅ Webhook atualizado com sucesso!")
            return True
        else:
            print(f"⚠️  Resposta: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao atualizar webhook: {e}")
        return False

def configurar_webhook_evolution():
    """
    Configura webhook na Evolution API para enviar mensagens ao Chatwoot
    """
    print("\n" + "="*70)
    print("🔄 PASSO 3: Configurando Webhook na Evolution API")
    print("="*70)

    # Primeiro, precisamos do inbox_id do Chatwoot
    try:
        with open('chatwoot_config.json', 'r') as f:
            config = json.load(f)
            inbox_id = config['inbox_id']
    except:
        print("⚠️  Arquivo chatwoot_config.json não encontrado!")
        print("Execute primeiro a criação do inbox.")
        return False

    # Webhook da Evolution vai enviar para o Chatwoot
    webhook_url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes/{inbox_id}/webhooks"

    url = f"{EVOLUTION_URL}/webhook/set/{EVOLUTION_INSTANCE}"

    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "webhook": {
            "enabled": True,
            "url": f"{WEBHOOK_URL_BASE}/webhook/chatwoot",  # Nosso middleware
            "webhookByEvents": True,
            "webhookBase64": True,
            "events": [
                "MESSAGES_UPSERT",
                "MESSAGES_UPDATE",
                "CONNECTION_UPDATE"
            ]
        }
    }

    try:
        print(f"📤 Configurando webhook na Evolution...")
        print(f"📍 URL: {payload['webhook']['url']}")

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            print(f"✅ Webhook Evolution configurado!")
            return True
        else:
            print(f"⚠️  Resposta: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao configurar webhook Evolution: {e}")
        return False

def testar_conexao():
    """Testa conexão com APIs"""
    print("\n" + "="*70)
    print("🔍 Testando Conexões")
    print("="*70)

    # Testa Chatwoot
    print("\n1️⃣ Testando Chatwoot...")
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}"
    headers = {"api_access_token": CHATWOOT_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            account = response.json()
            print(f"✅ Chatwoot OK!")
            print(f"   Conta: {account.get('name', 'N/A')}")
        else:
            print(f"❌ Chatwoot erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Chatwoot erro: {e}")

    # Testa Evolution
    print("\n2️⃣ Testando Evolution API...")
    url = f"{EVOLUTION_URL}/instance/fetchInstances"
    headers = {"apikey": EVOLUTION_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Evolution API OK!")
        else:
            print(f"❌ Evolution erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Evolution erro: {e}")

def menu_principal():
    """Menu interativo"""
    print("\n" + "="*80)
    print("🤖 SETUP CHATWOOT + EVOLUTION API - INTEGRAÇÃO HÍBRIDA")
    print("="*80)
    print("\nO que deseja fazer?\n")
    print("1️⃣  - Testar conexões (recomendado primeiro)")
    print("2️⃣  - Listar inboxes existentes")
    print("3️⃣  - Criar novo inbox WhatsApp")
    print("4️⃣  - Configurar webhook Evolution → Chatwoot")
    print("5️⃣  - Setup completo (faz tudo)")
    print("0️⃣  - Sair")
    print()

    escolha = input("Digite sua escolha: ").strip()

    if escolha == "1":
        testar_conexao()
    elif escolha == "2":
        listar_inboxes()
    elif escolha == "3":
        criar_inbox_whatsapp()
    elif escolha == "4":
        configurar_webhook_evolution()
    elif escolha == "5":
        print("\n🚀 Iniciando setup completo...")
        testar_conexao()
        input("\n⏸️  Pressione ENTER para continuar...")
        criar_inbox_whatsapp()
        input("\n⏸️  Pressione ENTER para continuar...")
        configurar_webhook_evolution()
        print("\n✅ Setup completo finalizado!")
    elif escolha == "0":
        print("👋 Até logo!")
        sys.exit(0)
    else:
        print("❌ Opção inválida!")

    input("\n⏸️  Pressione ENTER para voltar ao menu...")
    menu_principal()

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário. Até logo!")
        sys.exit(0)
