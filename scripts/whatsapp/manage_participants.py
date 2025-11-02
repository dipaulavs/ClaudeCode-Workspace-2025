#!/usr/bin/env python3
"""
Template: Gerenciar participantes de grupo WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/manage_participants.py --group 120363404863351747@g.us --action add --phones 5511999999999
    python3 scripts/whatsapp/manage_participants.py --group 120363404863351747@g.us --action remove --phones 5511999999999,5511888888888
    python3 scripts/whatsapp/manage_participants.py --group 120363404863351747@g.us --action promote --phones 5531980160822
    python3 scripts/whatsapp/manage_participants.py --group 120363404863351747@g.us --action demote --phones 5531980160822
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def manage_participants(group_id: str, action: str, participants: list):
    """
    Gerencia participantes do grupo WhatsApp

    Args:
        group_id: ID do grupo
        action: Ação a executar (add, remove, promote, demote)
        participants: Lista de números dos participantes

    Returns:
        Resposta da API
    """

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Executa ação correspondente
    if action == 'add':
        response = api.add_participant(group_id=group_id, participants=participants)
    elif action == 'remove':
        response = api.remove_participant(group_id=group_id, participants=participants)
    elif action == 'promote':
        response = api.promote_participant(group_id=group_id, participants=participants)
    elif action == 'demote':
        response = api.demote_participant(group_id=group_id, participants=participants)
    else:
        raise ValueError(f"Ação inválida: {action}")

    return response


def main():
    parser = argparse.ArgumentParser(description='Gerenciar participantes do grupo WhatsApp')
    parser.add_argument('--group', '-g', required=True, help='ID do grupo (ex: 120363404863351747@g.us)')
    parser.add_argument('--action', '-a', required=True,
                        choices=['add', 'remove', 'promote', 'demote'],
                        help='Ação: add (adicionar), remove (remover), promote (tornar admin), demote (remover admin)')
    parser.add_argument('--phones', '-p', required=True,
                        help='Números separados por vírgula (ex: 5511999999999,5511888888888)')

    args = parser.parse_args()

    # Converte string de telefones em lista
    participants = [p.strip() for p in args.phones.split(',')]

    # Mensagens amigáveis por ação
    action_messages = {
        'add': 'Adicionando',
        'remove': 'Removendo',
        'promote': 'Promovendo a admin',
        'demote': 'Removendo admin de'
    }

    print(f"👥 {action_messages[args.action]} {len(participants)} participante(s)...")

    try:
        response = manage_participants(args.group, args.action, participants)

        print(f"✅ Operação realizada com sucesso!")
        print(f"   Grupo: {args.group}")
        print(f"   Ação: {args.action}")
        print(f"   Participantes: {len(participants)}")

        return response
    except Exception as e:
        print(f"❌ Erro ao gerenciar participantes: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
