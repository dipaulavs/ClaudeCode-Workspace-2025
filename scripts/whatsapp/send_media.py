#!/usr/bin/env python3
"""
Template: Enviar mídia WhatsApp via Evolution API

Uso:
    python3 scripts/whatsapp/send_media.py --phone 5531980160822 --url "https://exemplo.com/imagem.jpg" --type image --caption "Veja isso!"
    python3 scripts/whatsapp/send_media.py --phone 5531980160822 --file "/path/to/video.mp4" --type video
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_media(phone: str, media_source: str, media_type: str, caption: str = "", filename: str = None):
    """Envia mídia via WhatsApp"""

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    response = api.send_media(
        number=phone,
        media_url=media_source,
        caption=caption,
        media_type=media_type,
        filename=filename
    )

    return response


def main():
    parser = argparse.ArgumentParser(description='Enviar mídia WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI')

    # Mídia pode ser URL ou arquivo local
    media_group = parser.add_mutually_exclusive_group(required=True)
    media_group.add_argument('--url', help='URL da mídia')
    media_group.add_argument('--file', help='Caminho do arquivo local')

    parser.add_argument('--type', '-t', required=True,
                       choices=['image', 'video', 'document', 'audio'],
                       help='Tipo de mídia')
    parser.add_argument('--caption', '-c', default='', help='Legenda da mídia')
    parser.add_argument('--filename', '-f', help='Nome do arquivo (para documentos)')

    args = parser.parse_args()

    media_source = args.url or args.file

    print(f"📤 Enviando {args.type} para {args.phone}...")

    try:
        response = send_media(args.phone, media_source, args.type, args.caption, args.filename)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Mídia enviada com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar mídia: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
