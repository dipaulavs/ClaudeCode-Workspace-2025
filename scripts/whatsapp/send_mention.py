#!/usr/bin/env python3
"""
Template: Mencionar pessoas em grupo via WhatsApp

Uso:
    python3 scripts/whatsapp/send_mention.py --group "120363123456789012@g.us" --text "Olá @5531980160822 e @5511999999999!" --mentions "5531980160822,5511999999999"
    python3 scripts/whatsapp/send_mention.py --group "120363123456789012@g.us" --text "@5531980160822 atenção!" --mentions "5531980160822"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_mention(group_id: str, text: str, mentions: list):
    """Envia mensagem com menções em grupo via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia mensagem com menções
    response = api.send_mention(group_id=group_id, text=text, mentions=mentions)

    return response


def main():
    parser = argparse.ArgumentParser(description='Mencionar pessoas em grupo WhatsApp')
    parser.add_argument('--group', '-g', required=True, help='ID do grupo (ex: 120363123456789012@g.us)')
    parser.add_argument('--text', '-t', required=True, help='Texto da mensagem (use @numero para mencionar)')
    parser.add_argument('--mentions', '-m', required=True, help='Números a mencionar separados por vírgula (ex: 5531980160822,5511999999999)')

    args = parser.parse_args()

    # Converte string de mentions para lista
    mentions_list = [m.strip() for m in args.mentions.split(',')]

    print(f"📢 Enviando menção para grupo {args.group}...")
    print(f"   Mencionando: {', '.join(mentions_list)}")
    print(f"   Texto: {args.text}")

    try:
        response = send_mention(args.group, args.text, mentions_list)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Mensagem com menções enviada com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar menção: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
