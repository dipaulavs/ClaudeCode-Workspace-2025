#!/usr/bin/env python3
"""
Instagram Scraper via Apify API

Extrai dados públicos do Instagram: posts, comentários, perfis, hashtags e localizações.

Uso:
    # Scrape posts de usuário
    python3 apify_instagram.py --user "natgeo" --results-type posts --limit 50

    # Scrape comentários de post
    python3 apify_instagram.py --url "https://instagram.com/p/ABC123/" --results-type comments

    # Scrape posts de hashtag
    python3 apify_instagram.py --hashtag "endgame" --results-type posts --limit 100

    # Scrape detalhes de perfil
    python3 apify_instagram.py --user "avengers" --results-type details

    # Scrape posts de localização
    python3 apify_instagram.py --place "Niagara Falls" --results-type posts --limit 50

Autor: Claude Code
Data: 2025-11-02
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configurações
from config.apify_config import (
    APIFY_API_KEY,
    INSTAGRAM_SCRAPER_ACTOR_ID,
    INSTAGRAM_DEFAULTS,
    INSTAGRAM_SEARCH_TYPES,
    INSTAGRAM_RESULTS_TYPES,
    DEFAULT_TIMEOUT,
    EXPORT_DIR
)

try:
    from apify_client import ApifyClient
except ImportError:
    print("❌ Erro: Biblioteca 'apify-client' não instalada")
    print("📦 Instale com: pip3 install apify-client")
    sys.exit(1)


class InstagramScraper:
    """Cliente para Instagram Scraper da Apify"""

    def __init__(self, api_key=None):
        """
        Inicializa o cliente

        Args:
            api_key: API key da Apify (opcional, usa variável de ambiente se não fornecido)
        """
        self.api_key = api_key or APIFY_API_KEY
        if not self.api_key:
            raise ValueError("❌ APIFY_API_KEY não configurada")

        self.client = ApifyClient(self.api_key)
        self.actor = self.client.actor(INSTAGRAM_SCRAPER_ACTOR_ID)

    def scrape(
        self,
        user=None,
        hashtag=None,
        place=None,
        url=None,
        results_type="posts",
        results_limit=50,
        search_limit=10,
        newer_than=None,
        older_than=None,
        timeout=None,
        output_file=None
    ):
        """
        Executa scraping do Instagram

        Args:
            user: Username do Instagram (sem @)
            hashtag: Hashtag (sem #)
            place: Nome da localização
            url: URL direta de post (para scrape de comentários)
            results_type: Tipo de resultado ("posts", "comments", "details")
            results_limit: Limite de resultados (posts/comentários)
            search_limit: Limite de resultados de busca (hashtags/places)
            newer_than: Data ISO 8601 - apenas posts mais novos que (ex: "2024-01-01")
            older_than: Data ISO 8601 - apenas posts mais antigos que
            timeout: Timeout em segundos
            output_file: Caminho para salvar resultado (JSON)

        Returns:
            dict: Resultado do scraping
        """
        # Validações
        if not any([user, hashtag, place, url]):
            raise ValueError("❌ Forneça pelo menos um: user, hashtag, place ou url")

        if results_type not in INSTAGRAM_RESULTS_TYPES.values():
            raise ValueError(f"❌ results_type inválido. Use: {list(INSTAGRAM_RESULTS_TYPES.values())}")

        # Montar input
        run_input = {
            "resultsType": results_type,
            "resultsLimit": results_limit,
            "searchLimit": search_limit,
            **INSTAGRAM_DEFAULTS
        }

        # Adicionar filtros de data
        if newer_than:
            run_input["onlyPostsNewerThan"] = newer_than
        if older_than:
            run_input["onlyPostsOlderThan"] = older_than

        # Adicionar tipo de busca
        if url:
            # URL direta (geralmente para comentários)
            run_input["directUrls"] = [url] if isinstance(url, str) else url
        elif user:
            run_input["search"] = user
            run_input["searchType"] = INSTAGRAM_SEARCH_TYPES["user"]
        elif hashtag:
            # Remover # se fornecido
            hashtag = hashtag.lstrip('#')
            run_input["search"] = hashtag
            run_input["searchType"] = INSTAGRAM_SEARCH_TYPES["hashtag"]
        elif place:
            run_input["search"] = place
            run_input["searchType"] = INSTAGRAM_SEARCH_TYPES["place"]

        # Executar
        print(f"🚀 Iniciando scraping do Instagram...")
        print(f"📋 Configuração:")
        if user:
            print(f"   👤 Usuário: @{user}")
        if hashtag:
            print(f"   #️⃣ Hashtag: #{hashtag}")
        if place:
            print(f"   📍 Localização: {place}")
        if url:
            print(f"   🔗 URL: {url}")
        print(f"   📊 Tipo: {results_type}")
        print(f"   🔢 Limite: {results_limit}")

        try:
            # Executar actor
            run = self.actor.call(
                run_input=run_input,
                timeout_secs=timeout or DEFAULT_TIMEOUT
            )

            # Buscar resultados
            print(f"\n⏳ Aguardando resultados...")
            dataset = self.client.dataset(run["defaultDatasetId"])
            items = list(dataset.iterate_items())

            result = {
                "success": True,
                "run_id": run["id"],
                "status": run["status"],
                "items_count": len(items),
                "items": items,
                "stats": {
                    "started_at": run.get("startedAt"),
                    "finished_at": run.get("finishedAt"),
                    "compute_units": run.get("stats", {}).get("computeUnits", 0)
                }
            }

            # Salvar em arquivo se solicitado
            if output_file:
                output_path = os.path.expanduser(output_file)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"\n✅ Resultados salvos em: {output_path}")

            # Resumo
            print(f"\n✅ Scraping concluído!")
            print(f"📊 Total de itens: {len(items)}")
            print(f"⚡ Compute units: {result['stats']['compute_units']:.4f}")

            return result

        except Exception as e:
            print(f"\n❌ Erro no scraping: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "items": []
            }

    def scrape_user_posts(self, username, limit=50, output_file=None):
        """
        Atalho: Scrape posts de usuário

        Args:
            username: Username (sem @)
            limit: Limite de posts
            output_file: Caminho para salvar resultado

        Returns:
            dict: Resultado do scraping
        """
        return self.scrape(
            user=username,
            results_type="posts",
            results_limit=limit,
            output_file=output_file
        )

    def scrape_hashtag_posts(self, hashtag, limit=50, output_file=None):
        """
        Atalho: Scrape posts de hashtag

        Args:
            hashtag: Hashtag (sem #)
            limit: Limite de posts
            output_file: Caminho para salvar resultado

        Returns:
            dict: Resultado do scraping
        """
        return self.scrape(
            hashtag=hashtag,
            results_type="posts",
            results_limit=limit,
            output_file=output_file
        )

    def scrape_post_comments(self, post_url, limit=50, output_file=None):
        """
        Atalho: Scrape comentários de post

        Args:
            post_url: URL do post
            limit: Limite de comentários
            output_file: Caminho para salvar resultado

        Returns:
            dict: Resultado do scraping
        """
        return self.scrape(
            url=post_url,
            results_type="comments",
            results_limit=limit,
            output_file=output_file
        )

    def scrape_user_profile(self, username, output_file=None):
        """
        Atalho: Scrape detalhes de perfil

        Args:
            username: Username (sem @)
            output_file: Caminho para salvar resultado

        Returns:
            dict: Resultado do scraping
        """
        return self.scrape(
            user=username,
            results_type="details",
            output_file=output_file
        )


def main():
    """Função principal para CLI"""
    parser = argparse.ArgumentParser(
        description="Instagram Scraper via Apify API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Scrape posts de usuário
  python3 apify_instagram.py --user "natgeo" --results-type posts --limit 50

  # Scrape comentários de post
  python3 apify_instagram.py --url "https://instagram.com/p/ABC123/" --results-type comments

  # Scrape posts de hashtag
  python3 apify_instagram.py --hashtag "travel" --results-type posts --limit 100

  # Scrape detalhes de perfil
  python3 apify_instagram.py --user "avengers" --results-type details

  # Scrape posts de localização
  python3 apify_instagram.py --place "Niagara Falls" --results-type posts --limit 50

  # Filtrar por data (apenas posts após 2024-01-01)
  python3 apify_instagram.py --user "natgeo" --newer-than "2024-01-01" --limit 50

Tipos de resultado:
  - posts: Retorna posts (imagens/vídeos/carrosseis)
  - comments: Retorna comentários (requer URL de post)
  - details: Retorna detalhes (perfil/hashtag/localização)
        """
    )

    # Argumentos principais
    parser.add_argument('--user', help='Username do Instagram (sem @)')
    parser.add_argument('--hashtag', help='Hashtag (sem #)')
    parser.add_argument('--place', help='Nome da localização')
    parser.add_argument('--url', help='URL direta de post (para comentários)')

    # Configurações
    parser.add_argument(
        '--results-type',
        choices=['posts', 'comments', 'details'],
        default='posts',
        help='Tipo de resultado (padrão: posts)'
    )
    parser.add_argument('--limit', type=int, default=50, help='Limite de resultados (padrão: 50)')
    parser.add_argument('--search-limit', type=int, default=10, help='Limite de busca (padrão: 10)')

    # Filtros de data
    parser.add_argument('--newer-than', help='Apenas posts mais novos que (ISO 8601: 2024-01-01)')
    parser.add_argument('--older-than', help='Apenas posts mais antigos que (ISO 8601: 2024-01-01)')

    # Output
    parser.add_argument(
        '--output',
        help='Arquivo de saída (padrão: ~/Downloads/instagram_TIMESTAMP.json)'
    )
    parser.add_argument('--timeout', type=int, help='Timeout em segundos')

    # Outros
    parser.add_argument('--api-key', help='API Key da Apify (opcional)')

    args = parser.parse_args()

    # Validações
    if not any([args.user, args.hashtag, args.place, args.url]):
        parser.error("❌ Forneça pelo menos um: --user, --hashtag, --place ou --url")

    # Gerar nome de arquivo se não fornecido
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source = args.user or args.hashtag or args.place or "post"
        filename = f"instagram_{source}_{args.results_type}_{timestamp}.json"
        args.output = os.path.join(EXPORT_DIR, filename)

    # Executar scraping
    scraper = InstagramScraper(api_key=args.api_key)

    result = scraper.scrape(
        user=args.user,
        hashtag=args.hashtag,
        place=args.place,
        url=args.url,
        results_type=args.results_type,
        results_limit=args.limit,
        search_limit=args.search_limit,
        newer_than=args.newer_than,
        older_than=args.older_than,
        timeout=args.timeout,
        output_file=args.output
    )

    # Exit code
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
