#!/usr/bin/env python3
"""
Template: Ver perfil WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/get_profile.py                    # Ver perfil próprio
    python3 scripts/whatsapp/get_profile.py --phone 5531980160822  # Ver perfil de outro número
"""

import sys
import argparse
import json
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def get_profile(phone: str = None):
    """
    Obtém informações do perfil WhatsApp

    Args:
        phone: Número do telefone (opcional - se não fornecido, retorna perfil próprio)

    Returns:
        Dicionário com informações do perfil
    """
    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Obtém perfil
    response = api.get_profile(phone)

    return response


def main():
    parser = argparse.ArgumentParser(description='Ver perfil WhatsApp')
    parser.add_argument('--phone', '-p', help='Número do telefone (opcional - sem esse parâmetro, mostra perfil próprio)')

    args = parser.parse_args()

    if args.phone:
        print(f"👤 Buscando perfil de {args.phone}...")
    else:
        print(f"👤 Buscando perfil próprio...")

    try:
        profile = get_profile(args.phone)

        print(f"\n✅ Perfil obtido com sucesso!")
        print(f"\n📋 Informações do perfil:")
        print(json.dumps(profile, indent=2, ensure_ascii=False))

        # Mostra informações formatadas se disponíveis
        if isinstance(profile, list) and len(profile) > 0:
            profile_data = profile[0]
            print(f"\n📌 Resumo:")
            if 'name' in profile_data:
                print(f"   Nome: {profile_data['name']}")
            if 'status' in profile_data:
                print(f"   Status: {profile_data['status']}")
            if 'picture' in profile_data:
                print(f"   Foto: {profile_data['picture']}")

        return profile
    except Exception as e:
        print(f"❌ Erro ao obter perfil: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
