#!/usr/bin/env python3
"""
Template: Scrape Posts de Usuário do Instagram

Extrai posts de um perfil do Instagram (imagens, vídeos, carrosseis).

Uso:
    python3 scrape_user_posts.py "natgeo"
    python3 scrape_user_posts.py "avengers" --limit 100
    python3 scrape_user_posts.py "humansofny" --newer-than "2024-01-01"

Autor: Claude Code
Data: 2025-11-02
"""

import sys
import os
import argparse

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.apify_instagram import InstagramScraper


def main():
    parser = argparse.ArgumentParser(
        description="Scrape posts de usuário do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scrape_user_posts.py "natgeo"
  python3 scrape_user_posts.py "avengers" --limit 100
  python3 scrape_user_posts.py "humansofny" --newer-than "2024-01-01"
        """
    )

    parser.add_argument('username', help='Username do Instagram (sem @)')
    parser.add_argument('--limit', type=int, default=50, help='Limite de posts (padrão: 50)')
    parser.add_argument('--newer-than', help='Apenas posts após data (ISO: 2024-01-01)')
    parser.add_argument('--older-than', help='Apenas posts antes de data (ISO: 2024-01-01)')
    parser.add_argument('--output', help='Arquivo de saída (JSON)')

    args = parser.parse_args()

    # Executar
    scraper = InstagramScraper()

    result = scraper.scrape_user_posts(
        username=args.username,
        limit=args.limit,
        output_file=args.output
    )

    # Mostrar preview dos posts
    if result.get("success") and result.get("items"):
        print("\n📸 Preview dos posts:")
        for i, post in enumerate(result["items"][:5], 1):
            print(f"\n{i}. {post.get('type', 'Unknown')}")
            print(f"   URL: {post.get('url', 'N/A')}")
            print(f"   ❤️ Likes: {post.get('likesCount', 0)}")
            print(f"   💬 Comentários: {post.get('commentsCount', 0)}")
            caption = post.get('caption', '')
            if caption:
                preview = caption[:100] + '...' if len(caption) > 100 else caption
                print(f"   📝 Legenda: {preview}")

        if len(result["items"]) > 5:
            print(f"\n... e mais {len(result['items']) - 5} posts")

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
