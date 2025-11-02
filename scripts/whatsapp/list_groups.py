#!/usr/bin/env python3
"""
Template: Listar grupos WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/list_groups.py
    python3 scripts/whatsapp/list_groups.py --verbose
    python3 scripts/whatsapp/list_groups.py --filter "Teste"
    python3 scripts/whatsapp/list_groups.py --verbose --filter "Template"
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def list_groups(verbose: bool = False, filter_name: str = None):
    """
    Lista todos os grupos do WhatsApp

    Args:
        verbose: Se True, mostra detalhes completos
        filter_name: Filtra grupos por nome (opcional)

    Returns:
        Lista de grupos
    """

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Obtém todos os grupos
    response = api.get_all_groups()

    # Extrai lista de grupos
    groups = response if isinstance(response, list) else response.get('groups', [])

    # Aplica filtro se fornecido
    if filter_name:
        groups = [g for g in groups if filter_name.lower() in g.get('subject', '').lower()]

    return groups, verbose


def main():
    parser = argparse.ArgumentParser(description='Listar grupos WhatsApp')
    parser.add_argument('--verbose', '-v', action='store_true', help='Mostrar detalhes completos dos grupos')
    parser.add_argument('--filter', '-f', help='Filtrar grupos por nome')

    args = parser.parse_args()

    print(f"📋 Listando grupos...")
    if args.filter:
        print(f"   Filtro: {args.filter}")

    try:
        groups, verbose = list_groups(args.verbose, args.filter)

        print(f"\n✅ Total de grupos encontrados: {len(groups)}\n")

        if len(groups) == 0:
            print("   Nenhum grupo encontrado.")
            return []

        # Lista grupos
        for i, group in enumerate(groups, 1):
            print(f"{i}. {group.get('subject', 'Sem nome')}")
            print(f"   ID: {group.get('id', 'N/A')}")

            if verbose:
                # Informações detalhadas
                participants = group.get('participants', [])
                print(f"   Participantes: {len(participants)}")

                # Conta admins
                admins = [p for p in participants if p.get('admin') in ['admin', 'superadmin']]
                print(f"   Administradores: {len(admins)}")

                # Descrição
                description = group.get('desc', '') or group.get('description', '')
                if description:
                    print(f"   Descrição: {description[:100]}...")

                # Criação
                creation = group.get('creation')
                if creation:
                    print(f"   Criado em: {creation}")

                print()

        return groups
    except Exception as e:
        print(f"❌ Erro ao listar grupos: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
