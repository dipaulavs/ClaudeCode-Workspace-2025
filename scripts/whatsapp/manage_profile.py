#!/usr/bin/env python3
"""
Template: Gerenciar perfil WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/manage_profile.py --name "Meu Nome"
    python3 scripts/whatsapp/manage_profile.py --status "Disponível"
    python3 scripts/whatsapp/manage_profile.py --picture "https://example.com/image.jpg"
    python3 scripts/whatsapp/manage_profile.py --name "Nome" --status "Status" --picture "caminho/para/imagem.jpg"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def manage_profile(name: str = None, status: str = None, picture: str = None):
    """
    Gerencia o perfil do WhatsApp

    Args:
        name: Novo nome do perfil (opcional)
        status: Novo status do perfil (opcional)
        picture: URL ou caminho para nova foto do perfil (opcional)

    Returns:
        Dicionário com os resultados das operações
    """
    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    results = {}

    # Atualiza nome se fornecido
    if name:
        print(f"📝 Atualizando nome do perfil para: {name}")
        response = api.update_profile_name(name)
        results['name'] = response
        print(f"✅ Nome atualizado!")

    # Atualiza status se fornecido
    if status:
        print(f"💬 Atualizando status do perfil para: {status}")
        response = api.update_profile_status(status)
        results['status'] = response
        print(f"✅ Status atualizado!")

    # Atualiza foto se fornecida
    if picture:
        print(f"📸 Atualizando foto do perfil...")
        response = api.update_profile_picture(picture)
        results['picture'] = response
        print(f"✅ Foto atualizada!")

    return results


def main():
    parser = argparse.ArgumentParser(description='Gerenciar perfil WhatsApp')
    parser.add_argument('--name', '-n', help='Novo nome do perfil')
    parser.add_argument('--status', '-s', help='Novo status do perfil')
    parser.add_argument('--picture', '-p', help='URL ou caminho para nova foto do perfil')

    args = parser.parse_args()

    # Verifica se pelo menos um parâmetro foi fornecido
    if not (args.name or args.status or args.picture):
        print("❌ Erro: Forneça pelo menos um parâmetro (--name, --status ou --picture)")
        parser.print_help()
        sys.exit(1)

    print(f"🔧 Gerenciando perfil WhatsApp...")

    try:
        results = manage_profile(
            name=args.name,
            status=args.status,
            picture=args.picture
        )
        print(f"\n✅ Perfil atualizado com sucesso!")
        return results
    except Exception as e:
        print(f"❌ Erro ao atualizar perfil: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
