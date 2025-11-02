#!/usr/bin/env python3
"""
Template: Scrape Posts de Localização do Instagram

Extrai posts de uma localização específica do Instagram.

Uso:
    python3 scrape_place_posts.py "Niagara Falls"
    python3 scrape_place_posts.py "Eiffel Tower" --limit 100
    python3 scrape_place_posts.py "Times Square" --newer-than "2024-01-01"

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
        description="Scrape posts de localização do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scrape_place_posts.py "Niagara Falls"
  python3 scrape_place_posts.py "Eiffel Tower" --limit 100
  python3 scrape_place_posts.py "Times Square" --newer-than "2024-01-01"
        """
    )

    parser.add_argument('place', help='Nome da localização')
    parser.add_argument('--limit', type=int, default=50, help='Limite de posts (padrão: 50)')
    parser.add_argument('--newer-than', help='Apenas posts após data (ISO: 2024-01-01)')
    parser.add_argument('--older-than', help='Apenas posts antes de data (ISO: 2024-01-01)')
    parser.add_argument('--output', help='Arquivo de saída (JSON)')

    args = parser.parse_args()

    # Executar
    scraper = InstagramScraper()

    result = scraper.scrape(
        place=args.place,
        results_type="posts",
        results_limit=args.limit,
        newer_than=args.newer_than,
        older_than=args.older_than,
        output_file=args.output
    )

    # Mostrar preview dos posts
    if result.get("success") and result.get("items"):
        print(f"\n📍 Posts da localização '{args.place}':")
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
