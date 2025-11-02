#!/usr/bin/env python3
"""
Script de teste de agendamento - Envia mensagem via WhatsApp
Criado pelo Claude Code para testar agendamento local
"""

import sys
import os

# Adicionar o diretório evolution-api-integration ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'evolution-api-integration'))

from whatsapp_helper import whatsapp

def send_test_message():
    """Envia mensagem de teste humanizada"""

    # Número do destinatário
    phone_number = "5531980160822"

    # Mensagem descontraída e humanizada
    message = """E aí mano! 😎

Esse aqui é um teste de agendamento programado pelo Claude Code local via terminal.

Se você tá lendo isso agora, significa que o bagulho funcionou! 🚀

Bora automatizar tudo! 💪"""

    try:
        print(f"📱 Enviando mensagem para {phone_number}...")
        result = whatsapp.send_message(phone_number, message)
        print(f"✅ Mensagem enviada com sucesso!")
        print(f"📊 Resultado: {result}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Claude Code - Teste de Agendamento WhatsApp")
    print("=" * 50)
    send_test_message()
