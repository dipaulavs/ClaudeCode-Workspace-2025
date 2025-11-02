#!/usr/bin/env python3
"""
Template: Publicar carrossel no Instagram

Uso:
    python3 scripts/instagram/publish_carousel.py --images "img1.jpg,img2.jpg,img3.jpg" --caption "Meu carrossel!"
    python3 scripts/instagram/publish_carousel.py --images "img1.jpg,img2.jpg" --caption "Carrossel de 2 fotos"
    python3 scripts/instagram/publish_carousel.py --images "img1.jpg,img2.jpg,img3.jpg" --no-rate-check
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.publish_instagram_carousel import InstagramCarouselPublisher


def publish_carousel(images: list, caption: str = "", no_rate_check: bool = False, no_status_check: bool = False):
    """
    Publica carrossel no Instagram

    Args:
        images: Lista de 2-10 imagens (caminhos locais ou URLs)
        caption: Legenda do carrossel (opcional)
        no_rate_check: Pula verificação de rate limit
        no_status_check: Pula verificação de status do container

    Returns:
        bool: True se publicou com sucesso
    """

    # Valida quantidade de imagens
    if len(images) < 2:
        raise ValueError("Carrossel precisa de pelo menos 2 imagens")
    if len(images) > 10:
        raise ValueError("Carrossel suporta no máximo 10 imagens")

    # Inicializa publisher
    publisher = InstagramCarouselPublisher()

    # Configura flags
    if no_rate_check:
        publisher.config["RATE_LIMITS"]["check_before_post"] = False
    if no_status_check:
        publisher.config["VALIDATION_CONFIG"]["check_container_status"] = False

    # Publica carrossel
    success = publisher.publish_carousel(images, caption)

    return success


def main():
    parser = argparse.ArgumentParser(description='Publicar carrossel no Instagram')
    parser.add_argument('--images', '-i', required=True, help='Lista de 2-10 imagens separadas por vírgula (ex: img1.jpg,img2.jpg)')
    parser.add_argument('--caption', '-c', default="", help='Legenda do carrossel (opcional)')
    parser.add_argument('--no-rate-check', action='store_true', help='Pular verificação de rate limit')
    parser.add_argument('--no-status-check', action='store_true', help='Pular verificação de status')

    args = parser.parse_args()

    # Converte string de imagens para lista
    images = [img.strip() for img in args.images.split(',')]

    print(f"🎠 Publicando carrossel com {len(images)} imagens no Instagram...")

    try:
        success = publish_carousel(
            images,
            args.caption,
            args.no_rate_check,
            args.no_status_check
        )

        if success:
            print(f"✅ Carrossel publicado com sucesso!")
        else:
            print(f"❌ Falha ao publicar carrossel")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
