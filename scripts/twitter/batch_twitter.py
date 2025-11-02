#!/usr/bin/env python3
"""
Template: Scraping em batch de múltiplos perfis/termos do Twitter/X

Útil para coletar dados de vários perfis ou termos de busca em uma única execução.

Exemplos de uso:
    # Múltiplos perfis
    python3 batch_twitter.py --handles elonmusk NASA Space python3 batch_twitter.py --handles elonmusk NASA SpaceX --max-items 100

    # Múltiplos termos de busca
    python3 batch_twitter.py --search "ai" "machine learning" "deep learning" --max-items 200

    # Mix de perfis e buscas
    python3 batch_twitter.py --handles NASA SpaceX --search "space exploration" --max-items 500

    # Com filtros
    python3 batch_twitter.py --handles tech_influencer1 tech_influencer2 --verified --images

    # De arquivo
    python3 batch_twitter.py --handles-file handles.txt --max-items 1000
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tools.apify_twitter import ApifyTwitterScraper


def read_lines_from_file(filepath: str) -> list:
    """Lê linhas de um arquivo (uma por linha)"""
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignora linhas vazias e comentários
                lines.append(line)
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Scraping em batch de múltiplos perfis/termos do Twitter/X",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  Múltiplos perfis:
    python3 batch_twitter.py --handles elonmusk NASA SpaceX

  Múltiplos termos:
    python3 batch_twitter.py --search "ai" "machine learning" "python"

  Mix:
    python3 batch_twitter.py --handles NASA --search "space exploration"

  De arquivo:
    python3 batch_twitter.py --handles-file handles.txt

Formato do arquivo (handles.txt):
  elonmusk
  NASA
  SpaceX
  # Comentários são ignorados
  python

Formato do arquivo (searches.txt):
  inteligência artificial
  machine learning
  # Comentários são ignorados
  deep learning
        """
    )

    # Argumentos principais
    parser.add_argument(
        "--handles",
        nargs="+",
        help="Lista de handles (sem @)"
    )

    parser.add_argument(
        "--handles-file",
        help="Arquivo com handles (um por linha)"
    )

    parser.add_argument(
        "--search",
        nargs="+",
        help="Lista de termos de busca"
    )

    parser.add_argument(
        "--search-file",
        help="Arquivo com termos de busca (um por linha)"
    )

    # Limites
    parser.add_argument(
        "--max-items",
        type=int,
        help="Número máximo de tweets TOTAL (dividido entre todas as queries)"
    )

    parser.add_argument(
        "--max-per-query",
        type=int,
        help="Número máximo de tweets POR query"
    )

    # Filtros básicos
    parser.add_argument(
        "--lang",
        help="Idioma dos tweets (pt, en, es, etc)"
    )

    parser.add_argument(
        "--verified",
        action="store_true",
        help="Apenas usuários verificados"
    )

    parser.add_argument(
        "--blue",
        action="store_true",
        help="Apenas Twitter Blue"
    )

    parser.add_argument(
        "--images",
        action="store_true",
        help="Apenas tweets com imagens"
    )

    parser.add_argument(
        "--videos",
        action="store_true",
        help="Apenas tweets com vídeos"
    )

    parser.add_argument(
        "--quotes",
        action="store_true",
        help="Apenas quote tweets"
    )

    # Filtros de engajamento
    parser.add_argument(
        "--min-retweets",
        type=int,
        help="Número mínimo de retweets"
    )

    parser.add_argument(
        "--min-likes",
        type=int,
        help="Número mínimo de likes"
    )

    parser.add_argument(
        "--min-replies",
        type=int,
        help="Número mínimo de replies"
    )

    # Filtros de data
    parser.add_argument(
        "--since",
        help="Data inicial (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--until",
        help="Data final (YYYY-MM-DD)"
    )

    # Ordenação
    parser.add_argument(
        "--sort",
        choices=["Latest", "Top", "Relevance"],
        default="Latest",
        help="Ordenação dos resultados (padrão: Latest)"
    )

    # Output
    parser.add_argument(
        "--output",
        help="Nome do arquivo de saída (padrão: batch_twitter_TIMESTAMP.json)"
    )

    parser.add_argument(
        "--separate-files",
        action="store_true",
        help="Salvar resultados em arquivos separados por query"
    )

    args = parser.parse_args()

    # Coleta handles
    handles = []
    if args.handles:
        handles.extend(args.handles)

    if args.handles_file:
        if not os.path.exists(args.handles_file):
            print(f"❌ Arquivo não encontrado: {args.handles_file}")
            sys.exit(1)
        file_handles = read_lines_from_file(args.handles_file)
        handles.extend(file_handles)
        print(f"📄 {len(file_handles)} handle(s) carregados de {args.handles_file}")

    # Coleta termos de busca
    search_terms = []
    if args.search:
        search_terms.extend(args.search)

    if args.search_file:
        if not os.path.exists(args.search_file):
            print(f"❌ Arquivo não encontrado: {args.search_file}")
            sys.exit(1)
        file_searches = read_lines_from_file(args.search_file)
        search_terms.extend(file_searches)
        print(f"📄 {len(file_searches)} termo(s) de busca carregados de {args.search_file}")

    # Valida
    if not handles and not search_terms:
        parser.error("Informe pelo menos --handles, --search, --handles-file ou --search-file")

    # Remove @ dos handles se presente
    handles = [h.lstrip("@") for h in handles]

    # Converte handles em queries
    handle_queries = []
    for handle in handles:
        query = f"from:{handle}"
        if args.since:
            query += f" since:{args.since}"
        if args.until:
            query += f" until:{args.until}"
        handle_queries.append(query)

    # Combina com search terms
    all_queries = handle_queries + search_terms

    # Remove duplicatas
    all_queries = list(set(all_queries))

    print(f"🐦 Scraping em batch do Twitter...")
    print(f"📊 Estatísticas:")
    if handles:
        print(f"   👤 Perfis: {len(handles)}")
    if search_terms:
        print(f"   🔍 Buscas: {len(search_terms)}")
    print(f"   📝 Total de queries: {len(all_queries)}")

    if args.max_items:
        print(f"   📈 Max items total: {args.max_items}")
    if args.max_per_query:
        print(f"   📈 Max items por query: {args.max_per_query}")

    # Calcula limite por query se necessário
    max_items_param = args.max_items
    if args.max_per_query:
        # Não podemos limitar por query no Apify diretamente
        # Vamos fazer um scraping único e depois processar
        print(f"⚠️  Nota: --max-per-query será aplicado no pós-processamento")

    # Executa scraping
    scraper = ApifyTwitterScraper()

    try:
        result = scraper.scrape(
            search_terms=all_queries,
            max_items=max_items_param,
            tweet_language=args.lang,
            only_verified_users=args.verified,
            only_twitter_blue=args.blue,
            only_image=args.images,
            only_video=args.videos,
            only_quote=args.quotes,
            minimum_retweets=args.min_retweets,
            minimum_favorites=args.min_likes,
            minimum_replies=args.min_replies,
            sort=args.sort,
            include_search_terms=True  # Para saber qual query retornou cada tweet
        )

        # Pós-processamento: dividir por query se necessário
        if args.separate_files or args.max_per_query:
            # Agrupa tweets por query
            tweets_by_query = {}
            for tweet in result["items"]:
                query = tweet.get("searchTerm", "unknown")
                if query not in tweets_by_query:
                    tweets_by_query[query] = []
                tweets_by_query[query].append(tweet)

            # Aplica limite por query se necessário
            if args.max_per_query:
                for query in tweets_by_query:
                    tweets_by_query[query] = tweets_by_query[query][:args.max_per_query]

            # Salva em arquivos separados se solicitado
            if args.separate_files:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                for query, tweets in tweets_by_query.items():
                    # Sanitiza o nome da query
                    safe_query = "".join(c for c in query if c.isalnum() or c in (" ", "_", "-"))
                    safe_query = safe_query.replace(" ", "_")[:30]

                    filename = f"batch_twitter_{safe_query}_{timestamp}.json"
                    output_path = os.path.expanduser(f"~/Downloads/{filename}")

                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump({
                            "query": query,
                            "total_items": len(tweets),
                            "items": tweets
                        }, f, ensure_ascii=False, indent=2)

                    print(f"💾 {query}: {len(tweets)} tweets → {output_path}")

                print(f"\n✅ Scraping concluído!")
                print(f"📁 {len(tweets_by_query)} arquivo(s) salvos em ~/Downloads/")
                return

            # Reconstrói resultado com limite por query
            result["items"] = []
            for tweets in tweets_by_query.values():
                result["items"].extend(tweets)
            result["total_items"] = len(result["items"])

        # Nome do arquivo
        if args.output:
            filename = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_twitter_{timestamp}.json"

        # Salva resultados
        output_path = os.path.expanduser(f"~/Downloads/{filename}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Scraping concluído!")
        print(f"💾 Resultados salvos em: {output_path}")
        print(f"\n📊 Estatísticas gerais:")
        print(f"   Total de tweets: {result['total_items']}")

        if result.get("stats"):
            stats = result["stats"]
            print(f"   Total de retweets: {stats.get('total_retweets', 0):,}")
            print(f"   Total de likes: {stats.get('total_likes', 0):,}")
            print(f"   Total de replies: {stats.get('total_replies', 0):,}")

            # Top autores
            if stats.get("authors"):
                print(f"\n👥 Top 10 autores:")
                top_authors = sorted(
                    stats["authors"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
                for author, count in top_authors:
                    print(f"   @{author}: {count} tweet(s)")

            # Idiomas
            if stats.get("languages"):
                print(f"\n🌍 Idiomas:")
                for lang, count in sorted(
                    stats["languages"].items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    print(f"   {lang}: {count} tweet(s)")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
