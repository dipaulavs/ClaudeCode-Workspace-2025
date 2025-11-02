#!/usr/bin/env python3
"""
Template: Google Maps Scraper - Busca Avançada
===============================================

Busca avançada com geolocalização customizada, múltiplas categorias e filtros.
Para casos de uso complexos que requerem precisão geográfica.

Uso:
    python3 scripts/scraping/google_maps_advanced.py --search "restaurantes" --location "São Paulo" --categories "Chinese restaurant,Japanese restaurant"
    python3 scripts/scraping/google_maps_advanced.py --circle -46.6333 -23.5505 --radius 5 --search "academias"
"""

import sys
import os
import argparse
import json

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from tools.apify_google_maps import GoogleMapsScraper


def main():
    parser = argparse.ArgumentParser(
        description="Google Maps Scraper - Busca Avançada",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  # Busca com múltiplas categorias
  python3 scripts/scraping/google_maps_advanced.py \\
    --search "restaurantes" \\
    --location "São Paulo" \\
    --categories "Chinese restaurant,Japanese restaurant,Italian restaurant"

  # Busca em círculo (raio de 5km)
  python3 scripts/scraping/google_maps_advanced.py \\
    --circle -46.6333 -23.5505 --radius 5 \\
    --search "academias" --max 100

  # Busca em polígono customizado (área específica)
  python3 scripts/scraping/google_maps_advanced.py \\
    --polygon "[[[-46.6,-23.5],[-46.7,-23.5],[-46.7,-23.6],[-46.6,-23.6],[-46.6,-23.5]]]" \\
    --search "cafeterias"

  # Busca com reviews detalhados
  python3 scripts/scraping/google_maps_advanced.py \\
    --search "hotéis" --location "Rio de Janeiro" \\
    --reviews --max-reviews 20 --csv
        """
    )

    # Tipo de busca
    search_group = parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument('--search', type=str, help='Termo de busca')
    search_group.add_argument('--url', type=str, help='URL direta do Google Maps')

    # Geolocalização
    geo_group = parser.add_mutually_exclusive_group()
    geo_group.add_argument('--location', type=str, help='Localização textual (ex: "São Paulo, Brasil")')
    geo_group.add_argument('--circle', nargs=2, type=float, metavar=('LNG', 'LAT'), help='Círculo: longitude latitude')
    geo_group.add_argument('--polygon', type=str, help='Polígono em formato GeoJSON')

    # Opções de círculo
    parser.add_argument('--radius', type=float, default=10, help='Raio do círculo em km (padrão: 10)')

    # Filtros e configurações
    parser.add_argument('--categories', type=str, help='Categorias separadas por vírgula')
    parser.add_argument('--max', type=int, default=20, help='Máximo de resultados (padrão: 20)')
    parser.add_argument('--reviews', action='store_true', help='Incluir reviews')
    parser.add_argument('--max-reviews', type=int, default=5, help='Máximo de reviews por lugar (padrão: 5)')

    # Export
    parser.add_argument('--csv', action='store_true', help='Exportar em CSV (padrão: JSON)')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída')

    args = parser.parse_args()

    # Valida argumentos
    if args.search and not (args.location or args.circle or args.polygon):
        print("❌ Erro: --search requer --location, --circle ou --polygon")
        sys.exit(1)

    print("=" * 80)
    print("🗺️  GOOGLE MAPS SCRAPER - BUSCA AVANÇADA")
    print("=" * 80)

    # Inicializa scraper
    scraper = GoogleMapsScraper()

    # Processa categorias
    categories = args.categories.split(',') if args.categories else None

    # Executa scraping baseado no tipo
    if args.url:
        # URL direta
        results = scraper.scrape_by_url(
            url=args.url,
            include_reviews=args.reviews,
            max_reviews=args.max_reviews
        )

    elif args.circle:
        # Busca com círculo
        lng, lat = args.circle
        geolocation = {
            "type": "Point",
            "coordinates": [lng, lat],
            "radiusKm": args.radius
        }

        results = scraper.scrape_with_geolocation(
            search_query=args.search,
            geolocation=geolocation,
            max_results=args.max,
            custom_config={
                "categoryFilterList": categories,
                "maxReviews": args.max_reviews if args.reviews else 0,
                "scrapeReviewerName": args.reviews,
                "scrapeReviewId": args.reviews,
                "scrapeReviewUrl": args.reviews,
            }
        )

    elif args.polygon:
        # Busca com polígono
        try:
            coordinates = json.loads(args.polygon)
            geolocation = {
                "type": "Polygon",
                "coordinates": coordinates
            }

            results = scraper.scrape_with_geolocation(
                search_query=args.search,
                geolocation=geolocation,
                max_results=args.max,
                custom_config={
                    "categoryFilterList": categories,
                    "maxReviews": args.max_reviews if args.reviews else 0,
                    "scrapeReviewerName": args.reviews,
                    "scrapeReviewId": args.reviews,
                    "scrapeReviewUrl": args.reviews,
                }
            )
        except json.JSONDecodeError:
            print("❌ Erro: --polygon deve ser um GeoJSON válido")
            sys.exit(1)

    else:
        # Busca normal com localização textual
        results = scraper.scrape_by_search(
            search_query=args.search,
            location=args.location,
            max_results=args.max,
            categories=categories,
            include_reviews=args.reviews,
            max_reviews=args.max_reviews
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
