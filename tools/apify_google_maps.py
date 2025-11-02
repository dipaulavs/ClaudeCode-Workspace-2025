#!/usr/bin/env python3
"""
Apify Google Maps Scraper - Extração de dados de empresas do Google Maps

Este script usa o Apify para fazer scraping do Google Maps e extrair informações
de empresas como nome, endereço, telefone, website, avaliações, etc.

Uso:
    python3 tools/apify_google_maps.py --search "restaurantes" --location "São Paulo, Brasil"
    python3 tools/apify_google_maps.py --url "https://www.google.com/maps/place/..."
    python3 tools/apify_google_maps.py --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4"
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Adiciona o diretório pai ao path para importar a config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from apify_client import ApifyClient
except ImportError:
    print("❌ Erro: apify-client não está instalado")
    print("Execute: pip3 install apify-client")
    sys.exit(1)

from config.apify_config import (
    APIFY_API_TOKEN,
    GOOGLE_MAPS_SCRAPER_ACTOR_ID,
    GOOGLE_MAPS_DEFAULTS,
    EXPORT_DIR,
    DEFAULT_TIMEOUT
)


class GoogleMapsScraper:
    """Classe para realizar scraping do Google Maps usando Apify"""

    def __init__(self, api_token: str = APIFY_API_TOKEN):
        """
        Inicializa o cliente Apify

        Args:
            api_token: Token da API do Apify
        """
        self.client = ApifyClient(api_token)
        self.actor_id = GOOGLE_MAPS_SCRAPER_ACTOR_ID

    def scrape_by_search(
        self,
        search_query: str,
        location: str,
        max_results: int = 20,
        categories: Optional[List[str]] = None,
        include_reviews: bool = False,
        max_reviews: int = 0,
        custom_config: Optional[Dict] = None
    ) -> Dict:
        """
        Scraping por termo de busca + localização

        Args:
            search_query: Termo de busca (ex: "restaurantes", "hotéis")
            location: Localização (ex: "São Paulo, Brasil", "New York, USA")
            max_results: Número máximo de resultados
            categories: Lista de categorias para filtrar
            include_reviews: Se deve incluir reviews
            max_reviews: Número máximo de reviews por lugar
            custom_config: Configurações customizadas adicionais

        Returns:
            dict com resultados do scraping
        """
        print(f"\n🔍 Buscando: {search_query}")
        print(f"📍 Localização: {location}")
        print(f"📊 Máximo de resultados: {max_results}")
        if categories:
            print(f"🏷️  Categorias: {', '.join(categories)}")
        print()

        # Configuração base
        config = GOOGLE_MAPS_DEFAULTS.copy()
        config.update({
            "searchStringsArray": [search_query],
            "locationQuery": location,
            "maxCrawledPlaces": max_results,
            "maxCrawledPlacesPerSearch": max_results,
        })

        # Configurações de reviews
        if include_reviews:
            config["maxReviews"] = max_reviews if max_reviews > 0 else 5
            config["scrapeReviewerName"] = True
            config["scrapeReviewId"] = True
            config["scrapeReviewUrl"] = True

        # Adiciona categorias
        if categories:
            config["categoryFilterList"] = categories

        # Merge com configurações customizadas
        if custom_config:
            config.update(custom_config)

        return self._execute_scraping(config)

    def scrape_by_url(
        self,
        url: str,
        include_reviews: bool = False,
        max_reviews: int = 0,
        custom_config: Optional[Dict] = None
    ) -> Dict:
        """
        Scraping por URL direta do Google Maps

        Args:
            url: URL do Google Maps
            include_reviews: Se deve incluir reviews
            max_reviews: Número máximo de reviews
            custom_config: Configurações customizadas adicionais

        Returns:
            dict com resultados do scraping
        """
        print(f"\n🔗 URL: {url}")
        print()

        # Configuração base
        config = GOOGLE_MAPS_DEFAULTS.copy()
        config.update({
            "startUrls": [url],
        })

        # Configurações de reviews
        if include_reviews:
            config["maxReviews"] = max_reviews if max_reviews > 0 else 5
            config["scrapeReviewerName"] = True
            config["scrapeReviewId"] = True
            config["scrapeReviewUrl"] = True

        # Merge com configurações customizadas
        if custom_config:
            config.update(custom_config)

        return self._execute_scraping(config)

    def scrape_by_place_id(
        self,
        place_id: str,
        include_reviews: bool = False,
        max_reviews: int = 0,
        custom_config: Optional[Dict] = None
    ) -> Dict:
        """
        Scraping por Place ID do Google

        Args:
            place_id: Place ID do Google (ex: ChIJN1t_tDeuEmsRUsoyG83frY4)
            include_reviews: Se deve incluir reviews
            max_reviews: Número máximo de reviews
            custom_config: Configurações customizadas adicionais

        Returns:
            dict com resultados do scraping
        """
        print(f"\n🆔 Place ID: {place_id}")
        print()

        # Configuração base
        config = GOOGLE_MAPS_DEFAULTS.copy()
        config.update({
            "startUrls": [f"https://www.google.com/maps/search/?api=1&query=&query_place_id={place_id}"],
        })

        # Configurações de reviews
        if include_reviews:
            config["maxReviews"] = max_reviews if max_reviews > 0 else 5
            config["scrapeReviewerName"] = True
            config["scrapeReviewId"] = True
            config["scrapeReviewUrl"] = True

        # Merge com configurações customizadas
        if custom_config:
            config.update(custom_config)

        return self._execute_scraping(config)

    def scrape_with_geolocation(
        self,
        search_query: str,
        geolocation: Dict,
        max_results: int = 20,
        custom_config: Optional[Dict] = None
    ) -> Dict:
        """
        Scraping com geolocalização customizada (polígono, círculo, etc)

        Args:
            search_query: Termo de busca
            geolocation: Objeto GeoJSON (Polygon, Point, MultiPolygon)
            max_results: Número máximo de resultados
            custom_config: Configurações customizadas adicionais

        Returns:
            dict com resultados do scraping
        """
        print(f"\n🔍 Buscando: {search_query}")
        print(f"🗺️  Geolocalização customizada: {geolocation.get('type', 'N/A')}")
        print(f"📊 Máximo de resultados: {max_results}")
        print()

        # Configuração base
        config = GOOGLE_MAPS_DEFAULTS.copy()
        config.update({
            "searchStringsArray": [search_query],
            "customGeolocation": geolocation,
            "maxCrawledPlaces": max_results,
            "maxCrawledPlacesPerSearch": max_results,
        })

        # Merge com configurações customizadas
        if custom_config:
            config.update(custom_config)

        return self._execute_scraping(config)

    def _execute_scraping(self, config: Dict) -> Dict:
        """
        Executa o scraping com a configuração fornecida

        Args:
            config: Configuração do Actor

        Returns:
            dict com resultados do scraping
        """
        try:
            print("⏳ Executando scraping...\n")

            # Executa o Actor
            run = self.client.actor(self.actor_id).call(
                run_input=config,
                timeout_secs=DEFAULT_TIMEOUT
            )

            print(f"✅ Scraping concluído!")
            print(f"🆔 Run ID: {run['id']}\n")

            # Busca todos os resultados
            print("📥 Baixando resultados...\n")
            dataset_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

            return {
                "success": True,
                "run_id": run["id"],
                "dataset_id": run["defaultDatasetId"],
                "num_places": len(dataset_items),
                "places": dataset_items
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def save_results(
        self,
        results: Dict,
        format: str = "json",
        filename: Optional[str] = None
    ) -> str:
        """
        Salva resultados em arquivo

        Args:
            results: Resultados do scraping
            format: Formato de saída (json, csv)
            filename: Nome do arquivo (sem extensão)

        Returns:
            Caminho do arquivo salvo
        """
        if not results["success"]:
            print(f"❌ Erro: {results['error']}")
            return None

        # Define nome do arquivo
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"google_maps_scrape_{timestamp}"

        # Cria pasta de destino
        output_dir = Path(EXPORT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        places = results["places"]

        if format == "json":
            output_path = output_dir / f"{filename}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(places, f, indent=2, ensure_ascii=False)

        elif format == "csv":
            import csv
            output_path = output_dir / f"{filename}.csv"

            if not places:
                print("⚠️  Nenhum resultado para salvar")
                return None

            # Identifica todos os campos possíveis
            all_keys = set()
            for place in places:
                all_keys.update(self._flatten_dict(place).keys())

            # Escreve CSV
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                writer.writeheader()
                for place in places:
                    writer.writerow(self._flatten_dict(place))

        else:
            print(f"❌ Formato '{format}' não suportado. Use 'json' ou 'csv'")
            return None

        print(f"\n✅ Resultados salvos com sucesso!")
        print(f"📁 Arquivo: {output_path}")
        print(f"📊 Total de lugares: {len(places)}\n")

        # Mostra resumo dos primeiros resultados
        if places:
            print("📋 Primeiros resultados:")
            for idx, place in enumerate(places[:3], 1):
                title = place.get('title', 'N/A')
                address = place.get('address', 'N/A')
                rating = place.get('totalScore', 'N/A')
                reviews = place.get('reviewsCount', 0)
                print(f"  {idx}. {title}")
                print(f"     📍 {address}")
                print(f"     ⭐️ {rating} ({reviews} reviews)")
                print()

            if len(places) > 3:
                print(f"  ... e mais {len(places) - 3} lugares\n")

        return str(output_path)

    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """
        Achata dicionário aninhado para CSV

        Args:
            d: Dicionário para achatar
            parent_key: Chave pai (para recursão)
            sep: Separador de níveis

        Returns:
            Dicionário achatado
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Converte listas em strings
                items.append((new_key, json.dumps(v, ensure_ascii=False)))
            else:
                items.append((new_key, v))

        return dict(items)


def main():
    """Função principal para uso via linha de comando"""
    parser = argparse.ArgumentParser(
        description="Apify Google Maps Scraper - Extração de dados de empresas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Busca simples
  python3 tools/apify_google_maps.py --search "restaurantes" --location "São Paulo, Brasil"

  # Busca com limite de resultados
  python3 tools/apify_google_maps.py --search "hotéis" --location "Rio de Janeiro" --max-results 50

  # Busca com reviews
  python3 tools/apify_google_maps.py --search "cafeterias" --location "Lisboa, Portugal" --reviews --max-reviews 10

  # URL direta
  python3 tools/apify_google_maps.py --url "https://www.google.com/maps/place/..."

  # Place ID
  python3 tools/apify_google_maps.py --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" --reviews

  # Export em CSV
  python3 tools/apify_google_maps.py --search "academias" --location "Belo Horizonte" --format csv
        """
    )

    # Argumentos de busca
    search_group = parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument('--search', type=str, help='Termo de busca (ex: "restaurantes")')
    search_group.add_argument('--url', type=str, help='URL direta do Google Maps')
    search_group.add_argument('--place-id', type=str, help='Place ID do Google Maps')

    # Argumentos opcionais
    parser.add_argument('--location', type=str, help='Localização (ex: "São Paulo, Brasil")')
    parser.add_argument('--max-results', type=int, default=20, help='Número máximo de resultados (padrão: 20)')
    parser.add_argument('--categories', type=str, help='Categorias separadas por vírgula')
    parser.add_argument('--reviews', action='store_true', help='Incluir reviews')
    parser.add_argument('--max-reviews', type=int, default=5, help='Número máximo de reviews por lugar (padrão: 5)')
    parser.add_argument('--format', type=str, choices=['json', 'csv'], default='json', help='Formato de saída (padrão: json)')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída (sem extensão)')

    args = parser.parse_args()

    # Valida argumentos
    if args.search and not args.location:
        print("❌ Erro: --location é obrigatório quando usar --search")
        sys.exit(1)

    print("=" * 80)
    print("🗺️  APIFY GOOGLE MAPS SCRAPER")
    print("=" * 80)

    # Inicializa scraper
    scraper = GoogleMapsScraper()

    # Executa scraping baseado no tipo de busca
    if args.search:
        categories = args.categories.split(',') if args.categories else None
        results = scraper.scrape_by_search(
            search_query=args.search,
            location=args.location,
            max_results=args.max_results,
            categories=categories,
            include_reviews=args.reviews,
            max_reviews=args.max_reviews
        )
    elif args.url:
        results = scraper.scrape_by_url(
            url=args.url,
            include_reviews=args.reviews,
            max_reviews=args.max_reviews
        )
    elif args.place_id:
        results = scraper.scrape_by_place_id(
            place_id=args.place_id,
            include_reviews=args.reviews,
            max_reviews=args.max_reviews
        )

    # Salva resultados
    if results["success"]:
        scraper.save_results(results, format=args.format, filename=args.output)
        print("=" * 80)
        print("✅ Scraping concluído com sucesso!")
        print("=" * 80)
    else:
        print(f"❌ Erro no scraping: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
