#!/usr/bin/env python3
"""
Template: Criar grupo WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/create_group.py --name "Meu Grupo" --phones 5531980160822,5511999999999
    python3 scripts/whatsapp/create_group.py --name "Vendas" --phones 5531980160822 --description "Grupo de vendas" --admins-only
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def create_group(name: str, participants: list, description: str = "", admins_only: bool = False):
    """Cria grupo no WhatsApp"""

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Cria o grupo
    response = api.create_group(
        subject=name,
        participants=participants,
        description=description
    )

    group_id = response.get('id')

    # Se admins_only, configura o grupo
    if admins_only and group_id:
        api.update_group_settings(group_id=group_id, setting="announcement")

    return response


def main():
    parser = argparse.ArgumentParser(description='Criar grupo WhatsApp')
    parser.add_argument('--name', '-n', required=True, help='Nome do grupo')
    parser.add_argument('--phones', '-p', required=True, help='Números separados por vírgula (ex: 5531980160822,5511999999999)')
    parser.add_argument('--description', '-d', default='', help='Descrição do grupo')
    parser.add_argument('--admins-only', '-a', action='store_true', help='Apenas admins podem enviar mensagens')

    args = parser.parse_args()

    # Converte string de telefones em lista
    participants = [p.strip() for p in args.phones.split(',')]

    print(f"👥 Criando grupo '{args.name}' com {len(participants)} participante(s)...")

    try:
        response = create_group(args.name, participants, args.description, args.admins_only)
        group_id = response.get('id', 'N/A')
        print(f"✅ Grupo criado com sucesso!")
        print(f"   Nome: {args.name}")
        print(f"   Group ID: {group_id}")
        print(f"   Participantes: {len(participants)}")

        if args.admins_only:
            print(f"   ⚙️ Configurado para apenas admins enviarem mensagens")

        return response
    except Exception as e:
        print(f"❌ Erro ao criar grupo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
