#!/usr/bin/env python3
"""
Configura webhook Chatwoot para receber APENAS mensagens do cliente
"""
import requests
import json

# Credenciais
CHATWOOT_URL = "https://chatwoot.loop9.com.br"
API_TOKEN = "YpNPyzfzCiTH75EwL18AXZUy"
ACCOUNT_ID = 2

headers = {
    "api_access_token": API_TOKEN,
    "Content-Type": "application/json"
}

def listar_inboxes():
    """Lista todas as inboxes"""
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/inboxes"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        inboxes = response.json()
        print("\n📥 INBOXES DISPONÍVEIS:")
        print("=" * 60)
        for inbox in inboxes.get('payload', []):
            print(f"ID: {inbox['id']}")
            print(f"Nome: {inbox['name']}")
            print(f"Tipo: {inbox['channel_type']}")
            print("-" * 60)
        return inboxes.get('payload', [])
    else:
        print(f"❌ Erro ao listar inboxes: {response.status_code}")
        print(response.text)
        return []

def listar_webhooks():
    """Lista webhooks configurados"""
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/webhooks"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        webhooks = data if isinstance(data, list) else data.get('payload', [])
        print("\n🔗 WEBHOOKS CONFIGURADOS:")
        print("=" * 60)
        if webhooks:
            for webhook in webhooks:
                if isinstance(webhook, dict):
                    print(f"ID: {webhook.get('id', 'N/A')}")
                    print(f"URL: {webhook.get('url', 'N/A')}")
                    print(f"Eventos: {webhook.get('subscriptions', [])}")
                    print("-" * 60)
        else:
            print("Nenhum webhook configurado")
            print("-" * 60)
        return webhooks
    else:
        print(f"❌ Erro ao listar webhooks: {response.status_code}")
        print(response.text)
        return []

def configurar_webhook(webhook_url):
    """Configura webhook para receber apenas message_created"""
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/webhooks"

    payload = {
        "url": webhook_url,
        "subscriptions": ["message_created"]  # Apenas mensagens criadas
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print("\n✅ Webhook configurado com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print(f"❌ Erro ao configurar webhook: {response.status_code}")
        print(response.text)
        return None

def atualizar_webhook(webhook_id, webhook_url):
    """Atualiza webhook existente"""
    url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/webhooks/{webhook_id}"

    payload = {
        "url": webhook_url,
        "subscriptions": ["message_created"]
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("\n✅ Webhook atualizado com sucesso!")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print(f"❌ Erro ao atualizar webhook: {response.status_code}")
        print(response.text)
        return None

def main():
    print("🔧 CONFIGURADOR DE WEBHOOK CHATWOOT")
    print("=" * 60)

    # Lista inboxes
    inboxes = listar_inboxes()

    # Procura inbox "chatbot"
    inbox_chatbot = None
    for inbox in inboxes:
        if 'chatbot' in inbox['name'].lower():
            inbox_chatbot = inbox
            print(f"\n✅ Inbox 'chatbot' encontrada: ID {inbox['id']}")
            break

    if not inbox_chatbot:
        print("\n⚠️ Inbox 'chatbot' não encontrada")

    # Lista webhooks existentes
    webhooks = listar_webhooks()

    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO NECESSÁRIA:")
    print("=" * 60)
    print("Para filtrar apenas mensagens do CLIENTE, você precisa:")
    print("1. Configurar webhook para evento 'message_created'")
    print("2. Adicionar filtro no N8N: sender.type === 'contact'")
    print("\nMotivo: Chatwoot não diferencia cliente/agente no webhook.")
    print("A API envia TODAS as mensagens no evento message_created.")
    print("O filtro deve ser feito no N8N após receber o webhook.")

    print("\n" + "=" * 60)
    webhook_url = input("\n Digite a URL do seu webhook N8N (ou ENTER para pular): ").strip()

    if webhook_url:
        if webhooks:
            print(f"\nWebhook existente encontrado (ID: {webhooks[0]['id']})")
            atualizar = input("Deseja atualizar? (s/n): ").strip().lower()
            if atualizar == 's':
                atualizar_webhook(webhooks[0]['id'], webhook_url)
        else:
            configurar_webhook(webhook_url)

if __name__ == "__main__":
    main()
