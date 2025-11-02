#!/usr/bin/env python3
"""
Template: Ações em mensagens WhatsApp

Uso:
    # Marcar mensagem como lida
    python3 scripts/whatsapp/message_actions.py --action read --phone 5531980160822 --message-id ID_DA_MENSAGEM

    # Deletar mensagem (apenas para você)
    python3 scripts/whatsapp/message_actions.py --action delete --phone 5531980160822 --message-id ID_DA_MENSAGEM

    # Deletar mensagem para todos
    python3 scripts/whatsapp/message_actions.py --action delete --phone 5531980160822 --message-id ID_DA_MENSAGEM --for-everyone
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def mark_as_read(phone: str, message_id: str):
    """Marca mensagem como lida"""
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)
    # Formata número com @s.whatsapp.net se necessário
    formatted_phone = f"{phone}@s.whatsapp.net" if '@' not in phone else phone
    return api.mark_message_as_read(formatted_phone, message_id)


def delete_message(phone: str, message_id: str, for_everyone: bool = False):
    """Deleta mensagem"""
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)
    # Formata número com @s.whatsapp.net se necessário
    formatted_phone = f"{phone}@s.whatsapp.net" if '@' not in phone else phone
    return api.delete_message(formatted_phone, message_id, for_everyone)


def main():
    parser = argparse.ArgumentParser(
        description='Ações em mensagens WhatsApp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Marcar mensagem como lida
  python3 scripts/whatsapp/message_actions.py --action read --phone 5531980160822 --message-id 3EB0123456789ABCDEF

  # Deletar mensagem (apenas para você)
  python3 scripts/whatsapp/message_actions.py --action delete --phone 5531980160822 --message-id 3EB0123456789ABCDEF

  # Deletar mensagem para todos
  python3 scripts/whatsapp/message_actions.py --action delete --phone 5531980160822 --message-id 3EB0123456789ABCDEF --for-everyone
        """
    )

    parser.add_argument('--action', '-a', required=True,
                       choices=['read', 'delete'],
                       help='Ação a executar (read: marcar como lida, delete: deletar mensagem)')
    parser.add_argument('--phone', '-p', required=True,
                       help='Número do destinatário com DDI (ex: 5531980160822)')
    parser.add_argument('--message-id', '-m', required=True,
                       help='ID da mensagem retornado ao enviar')
    parser.add_argument('--for-everyone', action='store_true',
                       help='Deletar mensagem para todos (apenas para action=delete)')

    args = parser.parse_args()

    try:
        if args.action == 'read':
            print(f"📖 Marcando mensagem como lida...")
            print(f"   Número: {args.phone}")
            print(f"   Message ID: {args.message_id}")

            response = mark_as_read(args.phone, args.message_id)
            print(f"\n✅ Mensagem marcada como lida com sucesso!")
            print(f"   Resposta: {response}")

        elif args.action == 'delete':
            for_everyone_text = "para todos" if args.for_everyone else "apenas para você"
            print(f"🗑️  Deletando mensagem {for_everyone_text}...")
            print(f"   Número: {args.phone}")
            print(f"   Message ID: {args.message_id}")

            response = delete_message(args.phone, args.message_id, args.for_everyone)
            print(f"\n✅ Mensagem deletada com sucesso!")
            print(f"   Resposta: {response}")

    except Exception as e:
        print(f"\n❌ Erro ao executar ação '{args.action}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
