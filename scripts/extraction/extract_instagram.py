#!/usr/bin/env python3
"""
Template: Extração de Posts do Instagram
Baixa imagens, vídeos e legendas de posts/carrosséis do Instagram via Apify

Uso:
    python3 scripts/extraction/extract_instagram.py "URL_OU_USERNAME"
    python3 scripts/extraction/extract_instagram.py "natgeo" --limit 10
"""

import sys
import os
from pathlib import Path

# Adiciona tools/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

try:
    from extract_instagram import extract_content
except ImportError:
    print("❌ Erro: Não foi possível importar extract_instagram.py")
    print("Verifique se o arquivo existe em: tools/extract_instagram.py")
    sys.exit(1)

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Extrai imagens e legendas de posts do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Extrair um post específico
  python3 scripts/extraction/extract_instagram.py "https://www.instagram.com/p/ABC123/"

  # Extrair posts de um perfil (últimos 30)
  python3 scripts/extraction/extract_instagram.py "natgeo"

  # Extrair com limite personalizado
  python3 scripts/extraction/extract_instagram.py "natgeo" --limit 10

  # Extrair carrossel completo
  python3 scripts/extraction/extract_instagram.py "https://www.instagram.com/p/XYZ789/"

Notas:
  • Extrai imagens em alta qualidade
  • Baixa todas as imagens de carrosséis
  • Salva legendas completas
  • Inclui metadados (likes, comentários, autor)
  • Arquivos salvos em: ~/Downloads/instagram_extract_TIMESTAMP/
        """
    )

    parser.add_argument(
        "url",
        help="URL do Instagram (post, perfil) ou username"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Limite de posts a extrair (padrão: 30)"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("📸 EXTRAÇÃO DE POSTS DO INSTAGRAM")
    print("=" * 70 + "\n")

    # Extrai conteúdo
    output_dir = extract_content(args.url, args.limit)

    if output_dir:
        print(f"\n{'=' * 70}")
        print("✅ Extração concluída com sucesso!")
        print(f"{'=' * 70}")
    else:
        print("\n❌ Falha na extração. Verifique a URL e tente novamente.")
        sys.exit(1)


if __name__ == "__main__":
    main()
