#!/usr/bin/env python3
"""
Template: Enviar áudio PTT (Push To Talk) via WhatsApp

Uso:
    python3 scripts/whatsapp/send_audio.py --phone 5531980160822 --audio https://example.com/audio.ogg
    python3 scripts/whatsapp/send_audio.py --phone 5531980160822 --audio /path/to/audio.ogg
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_audio(phone: str, audio_url: str):
    """Envia áudio PTT via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia áudio
    response = api.send_audio(number=phone, audio_url=audio_url)

    return response


def main():
    parser = argparse.ArgumentParser(description='Enviar áudio PTT WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI (ex: 5531980160822)')
    parser.add_argument('--audio', '-a', required=True, help='URL do áudio ou caminho local')

    args = parser.parse_args()

    print(f"🎵 Enviando áudio para {args.phone}...")

    try:
        response = send_audio(args.phone, args.audio)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Áudio enviado com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar áudio: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
