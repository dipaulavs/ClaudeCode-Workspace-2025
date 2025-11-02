#!/usr/bin/env python3
"""
Template: Google Maps Scraper - Busca Básica
=============================================

Busca simples por termo + localização.
Uso rápido para extrair empresas/lugares do Google Maps.

Uso:
    python3 scripts/scraping/google_maps_basic.py "restaurantes" "São Paulo, Brasil"
    python3 scripts/scraping/google_maps_basic.py "hotéis" "Lisboa, Portugal" --max 50
"""

import sys
import os
import argparse

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from tools.apify_google_maps import GoogleMapsScraper


def main():
    parser = argparse.ArgumentParser(
        description="Google Maps Scraper - Busca Básica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  # Restaurantes em São Paulo (20 resultados)
  python3 scripts/scraping/google_maps_basic.py "restaurantes" "São Paulo, Brasil"

  # Hotéis no Rio (50 resultados)
  python3 scripts/scraping/google_maps_basic.py "hotéis" "Rio de Janeiro" --max 50

  # Cafeterias em Lisboa (export CSV)
  python3 scripts/scraping/google_maps_basic.py "cafeterias" "Lisboa, Portugal" --csv

  # Academias em BH com reviews
  python3 scripts/scraping/google_maps_basic.py "academias" "Belo Horizonte" --reviews
        """
    )

    parser.add_argument('search', type=str, help='Termo de busca (ex: "restaurantes")')
    parser.add_argument('location', type=str, help='Localização (ex: "São Paulo, Brasil")')
    parser.add_argument('--max', type=int, default=20, help='Máximo de resultados (padrão: 20)')
    parser.add_argument('--csv', action='store_true', help='Exportar em CSV (padrão: JSON)')
    parser.add_argument('--reviews', action='store_true', help='Incluir reviews (5 por lugar)')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída')

    args = parser.parse_args()

    print("=" * 80)
    print("🗺️  GOOGLE MAPS SCRAPER - BUSCA BÁSICA")
    print("=" * 80)

    # Inicializa scraper
    scraper = GoogleMapsScraper()

    # Executa scraping
    results = scraper.scrape_by_search(
        search_query=args.search,
        location=args.location,
        max_results=args.max,
        include_reviews=args.reviews,
        max_reviews=5 if args.reviews else 0
    )

    # Salva resultados
    if results["success"]:
        output_format = "csv" if args.csv else "json"
        scraper.save_results(results, format=output_format, filename=args.output)
        print("=" * 80)
        print("✅ Scraping concluído!")
        print("=" * 80)
    else:
        print(f"❌ Erro: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
