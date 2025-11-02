#!/usr/bin/env python3
"""
Template: Publicar Story no Instagram

✨ Novo: Conversão automática PNG → JPG

Uso:
    python3 scripts/instagram/publish_story.py --media "imagem.jpg"
    python3 scripts/instagram/publish_story.py --media "imagem.png"  # Auto-convertido
    python3 scripts/instagram/publish_story.py --media "video.mp4"
    python3 scripts/instagram/publish_story.py --media "https://url.com/image.jpg"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.publish_instagram_story import InstagramStoryPublisher


def publish_story(media: str, no_rate_check: bool = False):
    """
    Publica Story no Instagram

    Args:
        media: Caminho local ou URL da imagem/vídeo
        no_rate_check: Pula verificação de rate limit

    Returns:
        bool: True se publicou com sucesso
    """

    # Inicializa publisher
    publisher = InstagramStoryPublisher()

    # Configura flags
    if no_rate_check:
        publisher.config["RATE_LIMITS"]["check_before_post"] = False

    # Publica Story
    success = publisher.publish_story(media)

    return success


def main():
    parser = argparse.ArgumentParser(description='Publicar Story no Instagram')
    parser.add_argument('--media', '-m', required=True, help='Caminho ou URL da imagem/vídeo')
    parser.add_argument('--no-rate-check', action='store_true', help='Pular verificação de rate limit')

    args = parser.parse_args()

    print(f"📱 Publicando Story no Instagram...")

    try:
        success = publish_story(args.media, args.no_rate_check)

        if success:
            print(f"✅ Story publicado com sucesso!")
            print(f"   ⏰ Durará 24 horas")
        else:
            print(f"❌ Falha ao publicar Story")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
