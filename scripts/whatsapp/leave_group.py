#!/usr/bin/env python3
"""
Template: Sair de grupo WhatsApp via Evolution API

ATENÇÃO: Esta ação é IRREVERSÍVEL! Você precisará ser adicionado novamente para retornar ao grupo.

Uso:
    python3 scripts/whatsapp/leave_group.py --group 120363404863351747@g.us --confirm
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def leave_group(group_id: str):
    """
    Sai do grupo WhatsApp

    Args:
        group_id: ID do grupo

    Returns:
        Resposta da API
    """

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Sai do grupo
    response = api.leave_group(group_id=group_id)

    return response


def main():
    parser = argparse.ArgumentParser(description='Sair de grupo WhatsApp')
    parser.add_argument('--group', '-g', required=True, help='ID do grupo (ex: 120363404863351747@g.us)')
    parser.add_argument('--confirm', '-c', action='store_true',
                        help='Confirmação obrigatória para executar a ação')

    args = parser.parse_args()

    # Validação de segurança
    if not args.confirm:
        print("❌ ERRO: Esta ação requer confirmação!")
        print("   Use --confirm ou -c para confirmar que deseja sair do grupo")
        print("   ATENÇÃO: Esta ação é IRREVERSÍVEL!")
        sys.exit(1)

    # Solicita confirmação adicional
    print("⚠️  ATENÇÃO: Você está prestes a SAIR do grupo!")
    print(f"   Grupo: {args.group}")
    print("   Esta ação é IRREVERSÍVEL!")
    print()
    confirmation = input("   Digite 'SAIR' para confirmar: ")

    if confirmation != 'SAIR':
        print("❌ Operação cancelada pelo usuário.")
        sys.exit(0)

    print(f"\n🚪 Saindo do grupo {args.group}...")

    try:
        response = leave_group(args.group)

        print(f"✅ Você saiu do grupo com sucesso!")
        print(f"   Você precisará ser adicionado novamente para retornar ao grupo.")

        return response
    except Exception as e:
        print(f"❌ Erro ao sair do grupo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
