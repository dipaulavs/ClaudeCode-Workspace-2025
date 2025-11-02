#!/usr/bin/env python3
"""
Template: Listar contatos e chats WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/get_contacts.py                    # Lista contatos e chats
    python3 scripts/whatsapp/get_contacts.py --type contacts    # Somente contatos
    python3 scripts/whatsapp/get_contacts.py --type chats       # Somente chats
    python3 scripts/whatsapp/get_contacts.py --verbose          # Mostrar detalhes completos
    python3 scripts/whatsapp/get_contacts.py --limit 10         # Limitar quantidade
"""

import sys
import argparse
import json
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def get_contacts_and_chats(type: str = "both", verbose: bool = False, limit: int = None):
    """
    Lista contatos e chats do WhatsApp

    Args:
        type: Tipo de listagem (contacts/chats/both)
        verbose: Se True, mostra todos os detalhes
        limit: Limite de itens a mostrar (opcional)

    Returns:
        Dicionário com contatos e/ou chats
    """
    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    results = {}

    # Lista contatos
    if type in ["contacts", "both"]:
        print(f"📇 Buscando contatos...")
        contacts = api.get_all_contacts()
        results['contacts'] = contacts

    # Lista chats
    if type in ["chats", "both"]:
        print(f"💬 Buscando chats...")
        chats = api.get_all_chats()
        results['chats'] = chats

    return results


def main():
    parser = argparse.ArgumentParser(description='Listar contatos e chats WhatsApp')
    parser.add_argument('--type', '-t', choices=['contacts', 'chats', 'both'], default='both',
                        help='Tipo de listagem (contacts/chats/both)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Mostrar todos os detalhes')
    parser.add_argument('--limit', '-l', type=int,
                        help='Limitar quantidade de itens mostrados')

    args = parser.parse_args()

    print(f"📋 Listando {args.type}...\n")

    try:
        results = get_contacts_and_chats(args.type, args.verbose, args.limit)

        print(f"\n✅ Dados obtidos com sucesso!\n")

        # Mostra contatos
        if 'contacts' in results:
            contacts = results['contacts']
            total_contacts = len(contacts) if isinstance(contacts, list) else 0
            print(f"📇 Total de contatos: {total_contacts}")

            if total_contacts > 0:
                display_contacts = contacts[:args.limit] if args.limit else contacts

                if args.verbose:
                    print(json.dumps(display_contacts, indent=2, ensure_ascii=False))
                else:
                    print(f"\n📌 Primeiros {len(display_contacts)} contatos:")
                    for i, contact in enumerate(display_contacts, 1):
                        name = contact.get('name', contact.get('pushName', 'Sem nome'))
                        number = contact.get('id', 'N/A').split('@')[0]
                        print(f"   {i}. {name} ({number})")

        # Mostra chats
        if 'chats' in results:
            chats = results['chats']
            total_chats = len(chats) if isinstance(chats, list) else 0
            print(f"\n💬 Total de chats: {total_chats}")

            if total_chats > 0:
                display_chats = chats[:args.limit] if args.limit else chats

                if args.verbose:
                    print(json.dumps(display_chats, indent=2, ensure_ascii=False))
                else:
                    print(f"\n📌 Primeiros {len(display_chats)} chats:")
                    for i, chat in enumerate(display_chats, 1):
                        name = chat.get('name', 'Sem nome')
                        chat_id = chat.get('id', 'N/A')
                        unread = chat.get('unreadCount', 0)
                        print(f"   {i}. {name} (ID: {chat_id.split('@')[0]}, Não lidas: {unread})")

        if args.verbose:
            print(f"\n📄 JSON completo:")
            print(json.dumps(results, indent=2, ensure_ascii=False))

        return results
    except Exception as e:
        print(f"❌ Erro ao obter dados: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
