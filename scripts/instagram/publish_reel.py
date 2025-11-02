#!/usr/bin/env python3
"""
Template: Publicar Reel no Instagram

Uso:
    python3 scripts/instagram/publish_reel.py --video "video.mp4" --caption "Meu Reel!"
    python3 scripts/instagram/publish_reel.py --video "video.mp4" --caption "Reel" --cover "capa.jpg"
    python3 scripts/instagram/publish_reel.py --video "video.mp4" --no-feed --audio "Nome da Música"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.publish_instagram_reel import InstagramReelPublisher


def publish_reel(video: str, caption: str = "", share_to_feed: bool = True,
                 cover: str = None, audio_name: str = None,
                 no_rate_check: bool = False, no_status_check: bool = False):
    """
    Publica Reel no Instagram

    Args:
        video: Caminho local ou URL do vídeo (MP4/MOV, 3-90s, max 200MB)
        caption: Legenda do Reel (opcional)
        share_to_feed: Compartilhar no feed principal (padrão: True)
        cover: Imagem de capa personalizada (opcional)
        audio_name: Nome do áudio/música (opcional)
        no_rate_check: Pula verificação de rate limit
        no_status_check: Pula verificação de status do container

    Returns:
        bool: True se publicou com sucesso
    """

    # Inicializa publisher
    publisher = InstagramReelPublisher()

    # Configura flags
    if no_rate_check:
        publisher.config["RATE_LIMITS"]["check_before_post"] = False
    if no_status_check:
        publisher.config["VALIDATION_CONFIG"]["check_container_status"] = False

    # Publica Reel
    success = publisher.publish_reel(video, caption, share_to_feed, cover, audio_name)

    return success


def main():
    parser = argparse.ArgumentParser(description='Publicar Reel no Instagram')
    parser.add_argument('--video', '-v', required=True, help='Caminho ou URL do vídeo (MP4/MOV)')
    parser.add_argument('--caption', '-c', default="", help='Legenda do Reel (opcional)')
    parser.add_argument('--cover', help='Imagem de capa personalizada (opcional)')
    parser.add_argument('--no-feed', action='store_true', help='Não compartilhar no feed principal')
    parser.add_argument('--audio', '-a', help='Nome do áudio/música (opcional)')
    parser.add_argument('--no-rate-check', action='store_true', help='Pular verificação de rate limit')
    parser.add_argument('--no-status-check', action='store_true', help='Pular verificação de status')

    args = parser.parse_args()

    share_to_feed = not args.no_feed

    print(f"🎬 Publicando Reel no Instagram...")

    try:
        success = publish_reel(
            args.video,
            args.caption,
            share_to_feed,
            args.cover,
            args.audio,
            args.no_rate_check,
            args.no_status_check
        )

        if success:
            print(f"✅ Reel publicado com sucesso!")
        else:
            print(f"❌ Falha ao publicar Reel")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
