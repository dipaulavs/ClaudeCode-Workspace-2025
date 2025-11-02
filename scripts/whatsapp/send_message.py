#!/usr/bin/env python3
"""
Template: Enviar mensagem WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Olá!"
    python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Texto em *negrito*" --delay 1000
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_message(phone: str, message: str, delay: int = 0):
    """Envia mensagem via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia mensagem
    response = api.send_text(number=phone, text=message, delay=delay)

    return response


def main():
    parser = argparse.ArgumentParser(description='Enviar mensagem WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI (ex: 5531980160822)')
    parser.add_argument('--message', '-m', required=True, help='Texto da mensagem')
    parser.add_argument('--delay', '-d', type=int, default=0, help='Delay em ms (padrão: 0)')

    args = parser.parse_args()

    print(f"📤 Enviando mensagem para {args.phone}...")

    try:
        response = send_message(args.phone, args.message, args.delay)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Mensagem enviada com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
