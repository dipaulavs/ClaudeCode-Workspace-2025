#!/usr/bin/env python3
"""
Template: Gerenciar DMs do Instagram

Uso:
    # Listar conversas
    python3 scripts/instagram/manage_dms.py --list

    # Ver mensagens de uma conversa
    python3 scripts/instagram/manage_dms.py --read CONVERSATION_ID

    # Responder mensagem
    python3 scripts/instagram/manage_dms.py --reply CONVERSATION_ID --text "Sua resposta"

    # Marcar como lida
    python3 scripts/instagram/manage_dms.py --mark-read CONVERSATION_ID
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.manage_instagram_dms import InstagramDMManager


def main():
    parser = argparse.ArgumentParser(description='Gerenciar DMs do Instagram')

    # Ações mutuamente exclusivas
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='Listar conversas')
    group.add_argument('--read', metavar='CONV_ID', help='Ler mensagens de uma conversa')
    group.add_argument('--reply', metavar='CONV_ID', help='Responder mensagem')
    group.add_argument('--mark-read', metavar='CONV_ID', help='Marcar conversa como lida')

    # Argumentos opcionais
    parser.add_argument('--text', '-t', help='Texto da resposta (necessário para --reply)')
    parser.add_argument('--limit', '-l', type=int, default=25, help='Limite de resultados (padrão: 25)')

    args = parser.parse_args()

    # Inicializa manager
    manager = InstagramDMManager()

    try:
        if args.list:
            print("💬 Listando conversas...\n")
            manager.list_conversations(limit=args.limit)

        elif args.read:
            print(f"📖 Lendo mensagens da conversa {args.read}...\n")
            manager.read_messages(args.read, limit=args.limit)

        elif args.reply:
            if not args.text:
                print("❌ Erro: --text é necessário para responder mensagem")
                sys.exit(1)
            print(f"✉️ Respondendo conversa {args.reply}...\n")
            manager.reply_message(args.reply, args.text)

        elif args.mark_read:
            print(f"✅ Marcando conversa {args.mark_read} como lida...\n")
            manager.mark_as_read(args.mark_read)

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
