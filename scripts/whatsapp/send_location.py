#!/usr/bin/env python3
"""
Template: Enviar localização via WhatsApp

Uso:
    python3 scripts/whatsapp/send_location.py --phone 5531980160822 --lat -19.9167 --lon -43.9345 --name "Praça da Liberdade" --address "Belo Horizonte, MG"
    python3 scripts/whatsapp/send_location.py --phone 5531980160822 --lat -23.5505 --lon -46.6333
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_location(phone: str, latitude: float, longitude: float, name: str = "", address: str = ""):
    """Envia localização via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia localização
    response = api.send_location(
        number=phone,
        latitude=latitude,
        longitude=longitude,
        name=name,
        address=address
    )

    return response


def main():
    parser = argparse.ArgumentParser(description='Enviar localização WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI (ex: 5531980160822)')
    parser.add_argument('--lat', required=True, type=float, help='Latitude')
    parser.add_argument('--lon', required=True, type=float, help='Longitude')
    parser.add_argument('--name', '-n', default="", help='Nome do local')
    parser.add_argument('--address', '-a', default="", help='Endereço do local')

    args = parser.parse_args()

    print(f"📍 Enviando localização para {args.phone}...")
    if args.name:
        print(f"   Local: {args.name}")
    print(f"   Coordenadas: {args.lat}, {args.lon}")

    try:
        response = send_location(args.phone, args.lat, args.lon, args.name, args.address)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Localização enviada com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar localização: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
