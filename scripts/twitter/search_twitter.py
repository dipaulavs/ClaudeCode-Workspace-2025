#!/usr/bin/env python3
"""
Template: Busca no Twitter/X com filtros avançados

Exemplos de uso:
    # Busca simples
    python3 search_twitter.py "inteligência artificial"

    # Busca com hashtag
    python3 search_twitter.py "#ai #machinelearning"

    # Busca com filtros
    python3 search_twitter.py "python" --lang pt --verified --min-likes 100

    # Busca com período
    python3 search_twitter.py "ChatGPT" --since 2024-01-01 --until 2024-12-31

    # Busca avançada (operadores)
    python3 search_twitter.py "(python OR javascript) tutorial -filter:retweets"

    # Múltiplas buscas
    python3 search_twitter.py "AI" "machine learning" "deep learning"
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tools.apify_twitter import ApifyTwitterScraper


def main():
    parser = argparse.ArgumentParser(
        description="Busca tweets no Twitter/X com filtros avançados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de busca avançada:

  Operadores básicos:
    "python OR javascript"          - Qualquer um dos termos
    "python javascript"             - Ambos os termos
    '"machine learning"'            - Frase exata
    "python -javascript"            - python mas não javascript

  Filtros de mídia:
    "gato filter:media"             - Com qualquer mídia
    "gato filter:images"            - Apenas com imagens
    "gato filter:videos"            - Apenas com vídeos
    "gato -filter:images"           - Sem imagens

  Filtros de tipo:
    "ai -filter:retweets"           - Sem retweets
    "ai filter:replies"             - Apenas replies
    "ai filter:quote"               - Apenas quotes

  Filtros de usuário:
    "from:elonmusk"                 - Tweets de @elonmusk
    "to:elonmusk"                   - Replies para @elonmusk
    "@elonmusk"                     - Menciona @elonmusk

  Filtros de engajamento:
    "ai min_faves:100"              - Mínimo 100 likes
    "ai min_retweets:50"            - Mínimo 50 RTs
    "ai min_replies:10"             - Mínimo 10 replies

  Filtros de data:
    "ai since:2024-01-01"           - A partir de 01/01/2024
    "ai until:2024-12-31"           - Até 31/12/2024
    "ai since:2024-01-01 until:2024-01-31" - Janeiro de 2024

  Filtros de localização:
    "terremoto near:Tokyo"          - Próximo a Tokyo
    "terremoto near:Tokyo within:15km" - Raio de 15km

  Combinações:
    "(python OR javascript) tutorial -filter:retweets min_faves:50"
    "from:NASA filter:images min_retweets:100"
        """
    )

    # Argumentos principais
    parser.add_argument(
        "terms",
        nargs="+",
        help="Termo(s) de busca (pode ser múltiplos)"
    )

    # Limites
    parser.add_argument(
        "--max-items",
        type=int,
        help="Número máximo de tweets (padrão: ilimitado)"
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
        help="Nome do arquivo de saída (padrão: busca_twitter_TIMESTAMP.json)"
    )

    args = parser.parse_args()

    # Monta as queries
    search_terms = []
    for term in args.terms:
        query = term

        # Adiciona filtros à query se não houver operadores avançados
        # (se já tem operadores, deixa o usuário controlar)
        if "since:" not in query.lower() and args.since:
            query += f" since:{args.since}"
        if "until:" not in query.lower() and args.until:
            query += f" until:{args.until}"

        search_terms.append(query)

    print(f"🔍 Buscando tweets...")
    print(f"📝 Queries: {search_terms}")

    # Executa busca
    scraper = ApifyTwitterScraper()

    try:
        result = scraper.scrape(
            search_terms=search_terms,
            max_items=args.max_items,
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
            include_search_terms=True  # Útil para saber qual query retornou cada tweet
        )

        # Nome do arquivo
        if args.output:
            filename = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Sanitiza o primeiro termo para usar no nome
            safe_term = "".join(c for c in args.terms[0] if c.isalnum() or c in (" ", "_", "-"))
            safe_term = safe_term.replace(" ", "_")[:30]
            filename = f"busca_twitter_{safe_term}_{timestamp}.json"

        # Salva resultados
        output_path = os.path.expanduser(f"~/Downloads/{filename}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Busca concluída!")
        print(f"💾 Resultados salvos em: {output_path}")
        print(f"\n📊 Estatísticas:")
        print(f"   Total de tweets: {result['total_items']}")

        if result.get("stats"):
            stats = result["stats"]
            print(f"   Total de retweets: {stats.get('total_retweets', 0):,}")
            print(f"   Total de likes: {stats.get('total_likes', 0):,}")
            print(f"   Total de replies: {stats.get('total_replies', 0):,}")

            # Top 5 autores
            if stats.get("authors"):
                print(f"\n👥 Top 5 autores:")
                top_authors = sorted(
                    stats["authors"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                for author, count in top_authors:
                    print(f"   @{author}: {count} tweet(s)")

            # Idiomas
            if stats.get("languages"):
                print(f"\n🌍 Idiomas:")
                for lang, count in stats["languages"].items():
                    print(f"   {lang}: {count} tweet(s)")

        # Mostra preview dos primeiros tweets
        if result["items"]:
            print(f"\n📄 Preview dos primeiros 3 tweets:")
            for i, tweet in enumerate(result["items"][:3], 1):
                print(f"\n   Tweet {i}:")
                print(f"   Autor: @{tweet.get('author', {}).get('userName', 'N/A')}")
                print(f"   Texto: {tweet.get('text', '')[:100]}...")
                print(f"   ❤️  {tweet.get('likeCount', 0)} | 🔁 {tweet.get('retweetCount', 0)} | 💬 {tweet.get('replyCount', 0)}")
                print(f"   URL: {tweet.get('url', 'N/A')}")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
