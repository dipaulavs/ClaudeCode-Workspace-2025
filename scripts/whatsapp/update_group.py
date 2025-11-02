#!/usr/bin/env python3
"""
Template: Atualizar informações do grupo WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/update_group.py --group 120363404863351747@g.us --name "Novo Nome"
    python3 scripts/whatsapp/update_group.py --group 120363404863351747@g.us --description "Nova descrição"
    python3 scripts/whatsapp/update_group.py --group 120363404863351747@g.us --picture "https://exemplo.com/imagem.jpg"
    python3 scripts/whatsapp/update_group.py --group 120363404863351747@g.us --name "Grupo Atualizado" --description "Descrição nova"
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def update_group(group_id: str, name: str = None, description: str = None, picture: str = None):
    """
    Atualiza informações do grupo WhatsApp

    Args:
        group_id: ID do grupo
        name: Novo nome (opcional)
        description: Nova descrição (opcional)
        picture: URL ou caminho da nova foto (opcional)

    Returns:
        Respostas das atualizações realizadas
    """

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    results = {}

    # Atualiza nome se fornecido
    if name:
        response = api.update_group_name(group_id=group_id, subject=name)
        results['name'] = response

    # Atualiza descrição se fornecida
    if description:
        response = api.update_group_description(group_id=group_id, description=description)
        results['description'] = response

    # Atualiza foto se fornecida
    if picture:
        response = api.update_group_picture(group_id=group_id, image_url=picture)
        results['picture'] = response

    return results


def main():
    parser = argparse.ArgumentParser(description='Atualizar informações do grupo WhatsApp')
    parser.add_argument('--group', '-g', required=True, help='ID do grupo (ex: 120363404863351747@g.us)')
    parser.add_argument('--name', '-n', help='Novo nome do grupo')
    parser.add_argument('--description', '-d', help='Nova descrição do grupo')
    parser.add_argument('--picture', '-p', help='URL ou caminho da nova foto do grupo')

    args = parser.parse_args()

    # Valida que pelo menos uma atualização foi solicitada
    if not any([args.name, args.description, args.picture]):
        print("❌ Erro: Você deve fornecer pelo menos uma atualização (--name, --description ou --picture)")
        sys.exit(1)

    print(f"🔄 Atualizando grupo {args.group}...")

    try:
        results = update_group(args.group, args.name, args.description, args.picture)

        print(f"✅ Grupo atualizado com sucesso!")

        if 'name' in results:
            print(f"   📝 Nome atualizado")
        if 'description' in results:
            print(f"   📄 Descrição atualizada")
        if 'picture' in results:
            print(f"   🖼️ Foto atualizada")

        return results
    except Exception as e:
        print(f"❌ Erro ao atualizar grupo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
