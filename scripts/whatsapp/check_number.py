#!/usr/bin/env python3
"""
Template: Verificar números no WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/check_number.py --phones 5531980160822
    python3 scripts/whatsapp/check_number.py --phones 5531980160822,5511999999999,123456789
"""

import sys
import argparse
import json
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def check_numbers(phones: list):
    """
    Verifica se números existem no WhatsApp

    Args:
        phones: Lista de números a verificar

    Returns:
        Dicionário com status dos números
    """
    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Verifica números
    response = api.check_number_exists(phones)

    return response


def main():
    parser = argparse.ArgumentParser(description='Verificar números no WhatsApp')
    parser.add_argument('--phones', '-p', required=True,
                        help='Números separados por vírgula (ex: 5531980160822,5511999999999)')

    args = parser.parse_args()

    # Converte string para lista
    phone_list = [phone.strip() for phone in args.phones.split(',')]

    print(f"🔍 Verificando {len(phone_list)} número(s) no WhatsApp...\n")

    try:
        results = check_numbers(phone_list)

        print(f"✅ Verificação concluída!\n")

        # Mostra JSON completo
        print(f"📋 Resultados:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

        # Mostra resumo formatado
        if isinstance(results, list):
            print(f"\n📌 Resumo:")
            for result in results:
                number = result.get('jid', result.get('number', 'N/A')).split('@')[0]
                exists = result.get('exists', False)
                status = "✅ Existe no WhatsApp" if exists else "❌ NÃO existe no WhatsApp"
                print(f"   {number}: {status}")

        return results
    except Exception as e:
        print(f"❌ Erro ao verificar números: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
