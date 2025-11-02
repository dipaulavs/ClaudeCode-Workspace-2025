#!/usr/bin/env python3
"""
Template: Transcrição de Vídeos
Transcreve vídeos de YouTube, TikTok, Instagram, LinkedIn, X/Twitter, Vimeo

Uso:
    python3 scripts/extraction/transcribe_video.py "URL_DO_VIDEO"
    python3 scripts/extraction/transcribe_video.py "URL_DO_VIDEO" --lang pt
"""

import sys
import os
from pathlib import Path

# Adiciona tools/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

try:
    from transcribe_universal import transcribe_video, save_transcription
except ImportError:
    print("❌ Erro: Não foi possível importar transcribe_universal.py")
    print("Verifique se o arquivo existe em: tools/transcribe_universal.py")
    sys.exit(1)

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Transcreve vídeos de múltiplas plataformas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Plataformas suportadas:
  • YouTube (youtube.com, youtu.be)
  • TikTok (tiktok.com)
  • Instagram (instagram.com)
  • LinkedIn (linkedin.com)
  • X/Twitter (x.com, twitter.com)
  • Vimeo (vimeo.com)

Exemplos:
  # YouTube em português
  python3 scripts/extraction/transcribe_video.py "https://youtu.be/VIDEO_ID" --lang pt

  # TikTok em inglês (padrão)
  python3 scripts/extraction/transcribe_video.py "https://tiktok.com/@user/video/123"

  # Instagram em espanhol
  python3 scripts/extraction/transcribe_video.py "https://instagram.com/reel/ABC/" --lang es

Idiomas suportados:
  pt (português), en (inglês), es (espanhol), fr (francês), de (alemão),
  it (italiano), ja (japonês), ko (coreano), zh (chinês), ru (russo)
        """
    )

    parser.add_argument(
        "url",
        help="URL do vídeo (YouTube, TikTok, Instagram, etc)"
    )

    parser.add_argument(
        "--lang",
        default="en",
        help="Código do idioma (padrão: en). Exemplos: pt, es, fr"
    )

    parser.add_argument(
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Tarefa: transcribe (padrão) ou translate (traduz para inglês)"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("🎬 TRANSCRIÇÃO DE VÍDEO")
    print("=" * 70 + "\n")

    # Valida URL
    if not args.url.startswith('http'):
        print("❌ Erro: Forneça uma URL válida começando com http:// ou https://")
        sys.exit(1)

    # Transcreve
    result = transcribe_video(args.url, args.lang, args.task)

    # Salva resultado
    if result:
        output_dir = save_transcription(args.url, result, args.lang)
        print(f"\n{'=' * 70}")
        print("✅ Transcrição concluída com sucesso!")
        print(f"{'=' * 70}")
    else:
        print("\n❌ Falha na transcrição. Verifique a URL e tente novamente.")
        sys.exit(1)


if __name__ == "__main__":
    main()
