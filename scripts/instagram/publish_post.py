#!/usr/bin/env python3
"""
Template: Publicar post no Instagram

Uso:
    python3 scripts/instagram/publish_post.py --image "path/to/image.jpg" --caption "Meu post!"
    python3 scripts/instagram/publish_post.py --image "https://url.com/image.jpg" --caption "Post!"
    python3 scripts/instagram/publish_post.py --image "foto.jpg" --caption "Post" --no-rate-check
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.publish_instagram_post import InstagramPublisher


def publish_post(image: str, caption: str = "", no_rate_check: bool = False, no_status_check: bool = False):
    """
    Publica post no Instagram

    Args:
        image: Caminho local ou URL da imagem
        caption: Legenda do post (opcional)
        no_rate_check: Pula verificação de rate limit
        no_status_check: Pula verificação de status do container

    Returns:
        bool: True se publicou com sucesso
    """

    # Inicializa publisher
    publisher = InstagramPublisher()

    # Configura flags
    if no_rate_check:
        publisher.config["RATE_LIMITS"]["check_before_post"] = False
    if no_status_check:
        publisher.config["VALIDATION_CONFIG"]["check_container_status"] = False

    # Publica post
    success = publisher.publish_post(image, caption)

    return success


def main():
    parser = argparse.ArgumentParser(description='Publicar post no Instagram')
    parser.add_argument('--image', '-i', required=True, help='Caminho ou URL da imagem')
    parser.add_argument('--caption', '-c', default="", help='Legenda do post (opcional)')
    parser.add_argument('--no-rate-check', action='store_true', help='Pular verificação de rate limit')
    parser.add_argument('--no-status-check', action='store_true', help='Pular verificação de status')

    args = parser.parse_args()

    print(f"📸 Publicando post no Instagram...")

    try:
        success = publish_post(
            args.image,
            args.caption,
            args.no_rate_check,
            args.no_status_check
        )

        if success:
            print(f"✅ Post publicado com sucesso!")
        else:
            print(f"❌ Falha ao publicar post")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
