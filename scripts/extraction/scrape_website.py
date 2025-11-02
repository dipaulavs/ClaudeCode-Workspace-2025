#!/usr/bin/env python3
"""
Template: Web Scraping de Sites
Extrai conteúdo de websites completos e salva em Markdown via Apify

Uso:
    python3 scripts/extraction/scrape_website.py "URL_DO_SITE"
    python3 scripts/extraction/scrape_website.py "https://docs.site.com" --max-pages 100
"""

import sys
import os
from pathlib import Path

# Adiciona tools/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

try:
    from apify_scraper import ApifyScraper
except ImportError:
    print("❌ Erro: Não foi possível importar apify_scraper.py")
    print("Verifique se o arquivo existe em: tools/apify_scraper.py")
    sys.exit(1)

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Faz scraping de websites completos e salva em Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Scraping básico (ilimitado)
  python3 scripts/extraction/scrape_website.py "https://docs.example.com"

  # Limitar quantidade de páginas
  python3 scripts/extraction/scrape_website.py "https://docs.site.com" --max-pages 50

  # Controlar profundidade de crawling
  python3 scripts/extraction/scrape_website.py "https://site.com" --max-depth 3

  # Combinar limites
  python3 scripts/extraction/scrape_website.py "https://site.com" --max-pages 100 --max-depth 5

Recursos:
  • Preview automático antes de executar
  • Segue links internos automaticamente
  • Converte tudo para Markdown
  • Salva páginas individuais + conteúdo completo
  • Inclui metadata (títulos, URLs, timestamps)
  • Arquivos salvos em: ~/Downloads/apify_scrape_DOMAIN_TIMESTAMP/

Notas:
  • Ideal para documentações técnicas
  • Respeita estrutura de links do site
  • Ignora recursos externos (imagens, CSS, JS)
        """
    )

    parser.add_argument(
        "url",
        help="URL do site para fazer scraping"
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Limite máximo de páginas (padrão: ilimitado)"
    )

    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Profundidade máxima de crawl (padrão: config padrão)"
    )

    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Pular preview e executar direto"
    )

    args = parser.parse_args()

    # Valida URL
    if not args.url.startswith(('http://', 'https://')):
        print("❌ Erro: URL deve começar com http:// ou https://")
        sys.exit(1)

    print("=" * 80)
    print("🌐 WEB SCRAPING")
    print("=" * 80)

    # Inicializa scraper
    scraper = ApifyScraper()

    # Preview (se não pulado)
    if not args.no_preview:
        preview = scraper.preview_scrape(args.url, max_preview_pages=50)

        if not preview["success"]:
            print(f"❌ Erro no preview: {preview['error']}")
            sys.exit(1)

        num_pages = preview["num_pages"]
        print(f"📊 Páginas encontradas (preview): {num_pages}")

        if preview["reached_limit"]:
            print(f"⚠️  O site pode ter MAIS de {num_pages} páginas")

        # Mostra amostra
        print(f"\n📝 Exemplos de páginas:")
        for idx, url in enumerate(preview["sample_urls"][:5], 1):
            print(f"   {idx}. {url}")

        # Confirmação
        print(f"\n{'=' * 80}")
        try:
            response = input("Continuar com scraping completo? (s/n): ").strip().lower()
        except KeyboardInterrupt:
            print("\n\n❌ Cancelado pelo usuário.")
            sys.exit(0)

        if response != 's':
            print("❌ Operação cancelada.")
            sys.exit(0)

        print(f"\n{'=' * 80}")

    # Scraping completo
    results = scraper.scrape(args.url, max_pages=args.max_pages, max_depth=args.max_depth)

    if results["success"]:
        # Salva resultados
        output_path = scraper.save_results(args.url, results)
        print("=" * 80)
        print("✅ Scraping concluído com sucesso!")
        print("=" * 80)
    else:
        print(f"❌ Erro no scraping: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
