#!/usr/bin/env python3
"""
Configura webhook na Evolution API para receber mensagens
"""

import requests
import sys

# Configurações da Evolution
EVOLUTION_API_URL = "https://evolution.loop9.com.br"
EVOLUTION_API_KEY = "178e43e1c4f459527e7008e57e378e1c"
EVOLUTION_INSTANCE_NAME = "lfimoveis"

def configurar_webhook(webhook_url):
    """
    Configura webhook na instância Evolution

    Args:
        webhook_url: URL pública do webhook (ex: https://seu-ngrok.ngrok-free.app/webhook)
    """

    url = f"{EVOLUTION_API_URL}/webhook/set/{EVOLUTION_INSTANCE_NAME}"

    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "webhook": {
            "enabled": True,
            "url": webhook_url,
            "webhookByEvents": True,
            "webhookBase64": True,  # IMPORTANTE: Envia base64 de mídias (áudio descriptografado)
            "events": [
                "MESSAGES_UPSERT",  # Mensagens recebidas
                "MESSAGES_UPDATE",  # Atualizações de mensagens
                "MESSAGES_DELETE",  # Mensagens deletadas
                "SEND_MESSAGE",     # Mensagens enviadas
                "CONNECTION_UPDATE" # Status de conexão
            ]
        }
    }

    try:
        print(f"🔧 Configurando webhook...")
        print(f"📍 URL: {webhook_url}")
        print(f"📱 Instância: {EVOLUTION_INSTANCE_NAME}\n")

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        resultado = response.json()

        print("✅ Webhook configurado com sucesso!")
        print(f"\n📊 Resposta da API:")
        print(resultado)

        return resultado

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao configurar webhook: {e}")
        if hasattr(e.response, 'text'):
            print(f"📄 Detalhes: {e.response.text}")
        sys.exit(1)

def verificar_webhook():
    """Verifica configuração atual do webhook"""

    url = f"{EVOLUTION_API_URL}/webhook/find/{EVOLUTION_INSTANCE_NAME}"

    headers = {
        "apikey": EVOLUTION_API_KEY
    }

    try:
        print("🔍 Verificando configuração atual do webhook...\n")

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        resultado = response.json()

        if resultado.get('enabled'):
            print("✅ Webhook ATIVO")
            print(f"📍 URL: {resultado.get('url')}")
            print(f"📋 Eventos: {', '.join(resultado.get('events', []))}")
        else:
            print("⚠️  Webhook DESATIVADO")

        print(f"\n📊 Configuração completa:")
        print(resultado)

        return resultado

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao verificar webhook: {e}")
        if hasattr(e.response, 'text'):
            print(f"📄 Detalhes: {e.response.text}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("🌐 CONFIGURAÇÃO DE WEBHOOK - Evolution API")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        if sys.argv[1] == "verificar":
            verificar_webhook()
        else:
            webhook_url = sys.argv[1]
            configurar_webhook(webhook_url)
    else:
        print("📝 USO:")
        print()
        print("  Configurar webhook:")
        print("  python3 configurar_webhook.py https://seu-ngrok.ngrok-free.app/webhook")
        print()
        print("  Verificar configuração atual:")
        print("  python3 configurar_webhook.py verificar")
        print()
        sys.exit(1)
