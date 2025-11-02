#!/usr/bin/env python3
"""
Template: Reagir a mensagem via WhatsApp

Uso:
    python3 scripts/whatsapp/send_reaction.py --phone 5531980160822 --message-id "ABC123XYZ" --emoji "👍"
    python3 scripts/whatsapp/send_reaction.py --phone 5531980160822 --message-id "ABC123XYZ" --emoji "❤️"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_reaction(phone: str, message_id: str, emoji: str):
    """Reage a uma mensagem via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia reação
    response = api.send_reaction(number=phone, key=message_id, reaction=emoji)

    return response


def main():
    parser = argparse.ArgumentParser(description='Reagir a mensagem WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI (ex: 5531980160822)')
    parser.add_argument('--message-id', '-m', required=True, help='ID da mensagem a reagir')
    parser.add_argument('--emoji', '-e', required=True, help='Emoji da reação (ex: 👍, ❤️, 😂)')

    args = parser.parse_args()

    print(f"👍 Enviando reação para {args.phone}...")
    print(f"   Message ID: {args.message_id}")
    print(f"   Emoji: {args.emoji}")

    try:
        response = send_reaction(args.phone, args.message_id, args.emoji)
        print(f"✅ Reação enviada com sucesso!")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar reação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
