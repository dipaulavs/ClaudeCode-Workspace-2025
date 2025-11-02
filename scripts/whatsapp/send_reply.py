#!/usr/bin/env python3
"""
Template: Responder mensagem via WhatsApp

Uso:
    python3 scripts/whatsapp/send_reply.py --phone 5531980160822 --message-id "ABC123XYZ" --text "Esta é minha resposta!"
    python3 scripts/whatsapp/send_reply.py --phone 5531980160822 --message-id "ABC123XYZ" --text "Obrigado pela mensagem!"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_reply(phone: str, message_id: str, text: str):
    """Responde uma mensagem via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia resposta
    response = api.send_reply(number=phone, text=text, message_id=message_id)

    return response


def main():
    parser = argparse.ArgumentParser(description='Responder mensagem WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI (ex: 5531980160822)')
    parser.add_argument('--message-id', '-m', required=True, help='ID da mensagem a responder')
    parser.add_argument('--text', '-t', required=True, help='Texto da resposta')

    args = parser.parse_args()

    print(f"💬 Respondendo mensagem para {args.phone}...")
    print(f"   Message ID: {args.message_id}")
    print(f"   Resposta: {args.text}")

    try:
        response = send_reply(args.phone, args.message_id, args.text)
        reply_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Resposta enviada com sucesso!")
        print(f"   Reply ID: {reply_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar resposta: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
