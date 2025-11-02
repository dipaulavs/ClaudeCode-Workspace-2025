#!/usr/bin/env python3
"""
Template: Obter informações da instância WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/instance_info.py
    python3 scripts/whatsapp/instance_info.py --qrcode
    python3 scripts/whatsapp/instance_info.py --verbose
"""

import sys
import argparse
from pathlib import Path
import json

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def get_instance_info(show_qrcode: bool = False, verbose: bool = False):
    """Obtém informações da instância WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Obtém status da instância
    status = api.get_instance_status()

    result = {
        'status': status
    }

    # Se solicitado e instância desconectada, tenta obter QR code
    if show_qrcode:
        try:
            qrcode_response = api.get_qrcode()
            result['qrcode'] = qrcode_response
        except Exception as e:
            result['qrcode_error'] = str(e)

    return result, verbose


def main():
    parser = argparse.ArgumentParser(
        description='Obter informações da instância WhatsApp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scripts/whatsapp/instance_info.py
  python3 scripts/whatsapp/instance_info.py --qrcode
  python3 scripts/whatsapp/instance_info.py --verbose
        """
    )
    parser.add_argument('--qrcode', '-q', action='store_true',
                       help='Mostrar QR code se disponível')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mostrar informações detalhadas')

    args = parser.parse_args()

    print(f"📱 Obtendo informações da instância '{EVOLUTION_INSTANCE_NAME}'...")
    print()

    try:
        result, verbose = get_instance_info(args.qrcode, args.verbose)

        # Exibe status da conexão
        status = result.get('status', {})
        # O estado pode estar em 'state' ou 'instance.state'
        state = status.get('state')
        if state is None and 'instance' in status:
            state = status['instance'].get('state', 'unknown')
        if state is None:
            state = 'unknown'

        if state == 'open':
            print("✅ Instância CONECTADA")
        elif state == 'close':
            print("❌ Instância DESCONECTADA")
        else:
            print(f"⚠️  Status: {state}")

        print()

        # Informações detalhadas do status
        if verbose or args.verbose:
            print("📊 Detalhes da Conexão:")
            print(json.dumps(status, indent=2, ensure_ascii=False))
            print()

        # Exibe QR code se disponível
        if 'qrcode' in result:
            qrcode_data = result['qrcode']
            if 'code' in qrcode_data:
                print("📱 QR Code disponível:")
                print(f"   Code: {qrcode_data.get('code', 'N/A')[:50]}...")
                if 'base64' in qrcode_data:
                    print(f"   Base64: disponível ({len(qrcode_data['base64'])} caracteres)")
            else:
                print("⚠️  QR code não disponível (instância pode estar conectada)")
            print()
        elif 'qrcode_error' in result:
            print(f"⚠️  Erro ao obter QR code: {result['qrcode_error']}")
            print()

        # Resumo
        print("=" * 60)
        print(f"Instância: {EVOLUTION_INSTANCE_NAME}")
        print(f"Estado: {state}")

        # Informações adicionais se disponíveis
        if 'instance' in status:
            instance_info = status['instance']
            if 'owner' in instance_info:
                print(f"Número: {instance_info.get('owner', 'N/A')}")
            if 'profileName' in instance_info:
                print(f"Nome: {instance_info.get('profileName', 'N/A')}")

        print("=" * 60)

        return result

    except Exception as e:
        print(f"❌ Erro ao obter informações da instância: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
