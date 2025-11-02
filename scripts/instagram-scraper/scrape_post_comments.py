#!/usr/bin/env python3
"""
Template: Scrape Comentários de Post do Instagram

Extrai comentários de um post específico do Instagram.

Uso:
    python3 scrape_post_comments.py "https://instagram.com/p/ABC123/"
    python3 scrape_post_comments.py "https://instagram.com/p/ABC123/" --limit 200

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
        description="Scrape comentários de post do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scrape_post_comments.py "https://instagram.com/p/ABC123/"
  python3 scrape_post_comments.py "https://instagram.com/p/ABC123/" --limit 200
        """
    )

    parser.add_argument('url', help='URL do post do Instagram')
    parser.add_argument('--limit', type=int, default=50, help='Limite de comentários (padrão: 50)')
    parser.add_argument('--output', help='Arquivo de saída (JSON)')

    args = parser.parse_args()

    # Executar
    scraper = InstagramScraper()

    result = scraper.scrape_post_comments(
        post_url=args.url,
        limit=args.limit,
        output_file=args.output
    )

    # Mostrar preview dos comentários
    if result.get("success") and result.get("items"):
        print("\n💬 Preview dos comentários:")
        for i, comment in enumerate(result["items"][:10], 1):
            print(f"\n{i}. @{comment.get('ownerUsername', 'N/A')}")
            verified = "✅" if comment.get('ownerIsVerified') else ""
            print(f"   {verified}")
            text = comment.get('text', '')
            preview = text[:150] + '...' if len(text) > 150 else text
            print(f"   💬 {preview}")
            print(f"   📅 {comment.get('timestamp', 'N/A')}")

        if len(result["items"]) > 10:
            print(f"\n... e mais {len(result['items']) - 10} comentários")

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
