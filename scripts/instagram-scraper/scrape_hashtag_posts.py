#!/usr/bin/env python3
"""
Template: Scrape Posts de Hashtag do Instagram

Extrai posts de uma hashtag do Instagram.

Uso:
    python3 scrape_hashtag_posts.py "travel"
    python3 scrape_hashtag_posts.py "endgame" --limit 100
    python3 scrape_hashtag_posts.py "fitness" --newer-than "2024-01-01"

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
        description="Scrape posts de hashtag do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scrape_hashtag_posts.py "travel"
  python3 scrape_hashtag_posts.py "endgame" --limit 100
  python3 scrape_hashtag_posts.py "fitness" --newer-than "2024-01-01"
        """
    )

    parser.add_argument('hashtag', help='Hashtag (sem #)')
    parser.add_argument('--limit', type=int, default=50, help='Limite de posts (padrão: 50)')
    parser.add_argument('--newer-than', help='Apenas posts após data (ISO: 2024-01-01)')
    parser.add_argument('--older-than', help='Apenas posts antes de data (ISO: 2024-01-01)')
    parser.add_argument('--output', help='Arquivo de saída (JSON)')

    args = parser.parse_args()

    # Remover # se fornecido
    hashtag = args.hashtag.lstrip('#')

    # Executar
    scraper = InstagramScraper()

    result = scraper.scrape_hashtag_posts(
        hashtag=hashtag,
        limit=args.limit,
        output_file=args.output
    )

    # Mostrar preview dos posts
    if result.get("success") and result.get("items"):
        print(f"\n#️⃣ Posts da hashtag #{hashtag}:")
        for i, post in enumerate(result["items"][:5], 1):
            print(f"\n{i}. {post.get('type', 'Unknown')}")
            print(f"   👤 Por: @{post.get('ownerUsername', 'N/A')}")
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
