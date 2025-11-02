#!/usr/bin/env python3
"""
Template: Google Maps Scraper - Busca em Lote (Batch)
======================================================

Executa múltiplas buscas em paralelo e combina os resultados.
Útil para extrair dados de várias localizações ou termos de busca simultaneamente.

Uso:
    python3 scripts/scraping/google_maps_batch.py --searches "restaurantes,hotéis,cafeterias" --location "São Paulo"
    python3 scripts/scraping/google_maps_batch.py --search "academias" --locations "São Paulo,Rio de Janeiro,Belo Horizonte"
"""

import sys
import os
import argparse
import json
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from tools.apify_google_maps import GoogleMapsScraper
from config.apify_config import EXPORT_DIR


def scrape_single(scraper, search_query, location, max_results, include_reviews, max_reviews):
    """Executa um único scraping"""
    try:
        print(f"  🔄 Iniciando: {search_query} em {location}")
        result = scraper.scrape_by_search(
            search_query=search_query,
            location=location,
            max_results=max_results,
            include_reviews=include_reviews,
            max_reviews=max_reviews
        )
        if result["success"]:
            print(f"  ✅ Concluído: {search_query} em {location} ({result['num_places']} lugares)")
        else:
            print(f"  ❌ Erro: {search_query} em {location} - {result.get('error', 'Erro desconhecido')}")
        return result
    except Exception as e:
        print(f"  ❌ Exceção: {search_query} em {location} - {str(e)}")
        return {"success": False, "error": str(e), "places": []}


def main():
    parser = argparse.ArgumentParser(
        description="Google Maps Scraper - Busca em Lote (Batch)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  # Múltiplas buscas na mesma localização
  python3 scripts/scraping/google_maps_batch.py \\
    --searches "restaurantes,hotéis,cafeterias,academias" \\
    --location "São Paulo, Brasil"

  # Mesma busca em múltiplas localizações
  python3 scripts/scraping/google_maps_batch.py \\
    --search "academias" \\
    --locations "São Paulo,Rio de Janeiro,Belo Horizonte,Curitiba"

  # Combinação de buscas e localizações (produto cartesiano)
  python3 scripts/scraping/google_maps_batch.py \\
    --searches "restaurantes,cafeterias" \\
    --locations "São Paulo,Rio de Janeiro" \\
    --max 30

  # Com reviews e export CSV
  python3 scripts/scraping/google_maps_batch.py \\
    --search "hotéis" \\
    --locations "Lisboa,Porto,Faro" \\
    --reviews --csv
        """
    )

    # Argumentos de busca
    parser.add_argument('--search', type=str, help='Termo de busca único')
    parser.add_argument('--searches', type=str, help='Múltiplos termos de busca (separados por vírgula)')
    parser.add_argument('--location', type=str, help='Localização única')
    parser.add_argument('--locations', type=str, help='Múltiplas localizações (separadas por vírgula)')

    # Configurações
    parser.add_argument('--max', type=int, default=20, help='Máximo de resultados por busca (padrão: 20)')
    parser.add_argument('--reviews', action='store_true', help='Incluir reviews')
    parser.add_argument('--max-reviews', type=int, default=5, help='Máximo de reviews por lugar (padrão: 5)')
    parser.add_argument('--workers', type=int, default=3, help='Número de buscas paralelas (padrão: 3)')

    # Export
    parser.add_argument('--csv', action='store_true', help='Exportar em CSV (padrão: JSON)')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída')
    parser.add_argument('--separate', action='store_true', help='Salvar cada busca em arquivo separado')

    args = parser.parse_args()

    # Valida argumentos
    if not (args.search or args.searches):
        print("❌ Erro: --search ou --searches é obrigatório")
        sys.exit(1)

    if not (args.location or args.locations):
        print("❌ Erro: --location ou --locations é obrigatório")
        sys.exit(1)

    # Processa listas
    search_queries = []
    if args.searches:
        search_queries = [s.strip() for s in args.searches.split(',')]
    elif args.search:
        search_queries = [args.search.strip()]

    locations = []
    if args.locations:
        locations = [l.strip() for l in args.locations.split(',')]
    elif args.location:
        locations = [args.location.strip()]

    # Cria lista de tarefas (produto cartesiano)
    tasks = []
    for search in search_queries:
        for location in locations:
            tasks.append((search, location))

    print("=" * 80)
    print("🗺️  GOOGLE MAPS SCRAPER - BUSCA EM LOTE")
    print("=" * 80)
    print(f"\n📊 Total de buscas: {len(tasks)}")
    print(f"👷 Workers paralelos: {args.workers}")
    print(f"📍 Localizações: {', '.join(locations)}")
    print(f"🔍 Buscas: {', '.join(search_queries)}")
    print()

    # Inicializa scraper
    scraper = GoogleMapsScraper()

    # Executa buscas em paralelo
    all_results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for search, location in tasks:
            future = executor.submit(
                scrape_single,
                scraper,
                search,
                location,
                args.max,
                args.reviews,
                args.max_reviews
            )
            futures[future] = (search, location)

        # Aguarda conclusão
        for future in as_completed(futures):
            search, location = futures[future]
            result = future.result()
            all_results.append({
                "search": search,
                "location": location,
                "result": result
            })

    # Processa resultados
    successful = [r for r in all_results if r["result"]["success"]]
    failed = [r for r in all_results if not r["result"]["success"]]

    print("\n" + "=" * 80)
    print(f"📊 RESUMO")
    print("=" * 80)
    print(f"✅ Buscas bem-sucedidas: {len(successful)}")
    print(f"❌ Buscas com erro: {len(failed)}")

    if failed:
        print("\n⚠️  Buscas que falharam:")
        for item in failed:
            print(f"  - {item['search']} em {item['location']}: {item['result'].get('error', 'Erro desconhecido')}")

    # Salva resultados
    if successful:
        output_format = "csv" if args.csv else "json"

        if args.separate:
            # Salva cada busca em arquivo separado
            print(f"\n💾 Salvando resultados separados...")
            for item in successful:
                search = item["search"]
                location = item["location"]
                result = item["result"]

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"gmaps_{search.replace(' ', '_')}_{location.replace(' ', '_').replace(',', '')}_{timestamp}"

                scraper.save_results(result, format=output_format, filename=filename)

        else:
            # Combina todos os resultados em um único arquivo
            print(f"\n💾 Salvando resultados combinados...")

            all_places = []
            for item in successful:
                places = item["result"]["places"]
                # Adiciona metadados de busca a cada lugar
                for place in places:
                    place["_search_query"] = item["search"]
                    place["_search_location"] = item["location"]
                all_places.extend(places)

            # Cria resultado combinado
            combined_result = {
                "success": True,
                "num_places": len(all_places),
                "places": all_places
            }

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = args.output or f"gmaps_batch_{timestamp}"

            scraper.save_results(combined_result, format=output_format, filename=filename)

    print("\n" + "=" * 80)
    print("✅ Batch scraping concluído!")
    print("=" * 80)


if __name__ == "__main__":
    main()
