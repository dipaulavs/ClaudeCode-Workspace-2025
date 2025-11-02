#!/usr/bin/env python3
"""
Template: Enviar enquete WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/send_poll.py --phone 5531980160822 --question "Melhor dia?" --options "Segunda,Terça,Quarta"
    python3 scripts/whatsapp/send_poll.py --group 120363423739033485@g.us --question "Pizza ou Hamburguer?" --options "Pizza,Hamburguer" --multiple
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_poll(number: str, question: str, options: list, selectable_count: int = 1):
    """Envia enquete via WhatsApp"""

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    response = api.send_poll(
        number=number,
        name=question,
        options=options,
        selectable_count=selectable_count
    )

    return response


def main():
    parser = argparse.ArgumentParser(description='Enviar enquete WhatsApp')

    # Número ou grupo
    number_group = parser.add_mutually_exclusive_group(required=True)
    number_group.add_argument('--phone', '-p', help='Número com DDI')
    number_group.add_argument('--group', '-g', help='ID do grupo (ex: 120363123456789@g.us)')

    parser.add_argument('--question', '-q', required=True, help='Pergunta da enquete')
    parser.add_argument('--options', '-o', required=True, help='Opções separadas por vírgula (ex: "Opção 1,Opção 2,Opção 3")')
    parser.add_argument('--multiple', '-m', action='store_true', help='Permitir seleção múltipla')

    args = parser.parse_args()

    number = args.phone or args.group
    options = [opt.strip() for opt in args.options.split(',')]
    selectable_count = len(options) if args.multiple else 1

    print(f"📊 Enviando enquete para {number}...")
    print(f"   Pergunta: {args.question}")
    print(f"   Opções: {', '.join(options)}")

    try:
        response = send_poll(number, args.question, options, selectable_count)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Enquete enviada com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar enquete: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
