#!/usr/bin/env python3
"""
Template: Postar status/story via WhatsApp

Uso:
    python3 scripts/whatsapp/send_status.py --content "Olá! Este é meu status!" --type text --bgcolor "#008000"
    python3 scripts/whatsapp/send_status.py --content "https://example.com/image.jpg" --type image --caption "Minha foto"
    python3 scripts/whatsapp/send_status.py --content "Bom dia!" --type text --bgcolor "#FF0000" --caption "Status do dia"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_status(content: str, type: str = "text", background_color: str = "#000000", caption: str = ""):
    """Posta status/story via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia status
    response = api.send_status(
        content=content,
        type=type,
        background_color=background_color,
        font=1,
        all_contacts=True,
        caption=caption
    )

    return response


def main():
    parser = argparse.ArgumentParser(description='Postar status/story WhatsApp')
    parser.add_argument('--content', '-c', required=True, help='Conteúdo (texto ou URL da mídia)')
    parser.add_argument('--type', '-t', default="text", choices=['text', 'image', 'video', 'audio'], help='Tipo do status (padrão: text)')
    parser.add_argument('--bgcolor', '-b', default="#000000", help='Cor de fundo para texto (ex: #008000)')
    parser.add_argument('--caption', '-p', default="", help='Legenda para imagem/vídeo')

    args = parser.parse_args()

    print(f"📱 Postando status...")
    print(f"   Tipo: {args.type}")
    if args.type == "text":
        print(f"   Texto: {args.content}")
        print(f"   Cor de fundo: {args.bgcolor}")
    else:
        print(f"   Mídia: {args.content}")
        if args.caption:
            print(f"   Legenda: {args.caption}")

    try:
        response = send_status(args.content, args.type, args.bgcolor, args.caption)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Status postado com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao postar status: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
