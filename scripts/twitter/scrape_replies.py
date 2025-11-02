#!/usr/bin/env python3
"""
Template: Scraping de replies/conversas do Twitter/X

Coleta todas as respostas (replies) de um tweet específico.

Exemplos de uso:
    # Todas as replies de um tweet
    python3 scrape_replies.py 1728108619189874825

    # Replies com hashtag específica
    python3 scrape_replies.py 1728108619189874825 --hashtag ai

    # Com limite
    python3 scrape_replies.py 1728108619189874825 --max-items 500

    # Com filtros
    python3 scrape_replies.py 1728108619189874825 --min-likes 10 --verified
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tools.apify_twitter import ApifyTwitterScraper


def extract_tweet_id(input_str: str) -> str:
    """Extrai o ID do tweet de uma URL ou string"""
    # Se já é um ID (apenas números)
    if input_str.isdigit():
        return input_str

    # Se é uma URL
    if "twitter.com" in input_str or "x.com" in input_str:
        # Formato: https://twitter.com/user/status/ID
        parts = input_str.split("/")
        for i, part in enumerate(parts):
            if part == "status" and i + 1 < len(parts):
                # Remove query params se houver
                tweet_id = parts[i + 1].split("?")[0]
                return tweet_id

    # Caso contrário, assume que é o ID
    return input_str


def main():
    parser = argparse.ArgumentParser(
        description="Scraping de replies/conversas do Twitter/X",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  ID do tweet:
    python3 scrape_replies.py 1728108619189874825

  URL completa:
    python3 scrape_replies.py "https://twitter.com/elonmusk/status/1728108619189874825"

  Com filtro de hashtag:
    python3 scrape_replies.py 1728108619189874825 --hashtag ai

  Com filtros de engajamento:
    python3 scrape_replies.py 1728108619189874825 --min-likes 10 --min-retweets 5

  Apenas usuários verificados:
    python3 scrape_replies.py 1728108619189874825 --verified

Como obter o ID do tweet:
  - Na URL: https://twitter.com/user/status/ID
  - O ID são os números após /status/
        """
    )

    # Argumento principal
    parser.add_argument(
        "tweet",
        help="ID do tweet ou URL completa"
    )

    # Filtros específicos
    parser.add_argument(
        "--hashtag",
        help="Filtrar replies com hashtag específica (sem #)"
    )

    # Limites
    parser.add_argument(
        "--max-items",
        type=int,
        help="Número máximo de replies"
    )

    # Filtros básicos
    parser.add_argument(
        "--lang",
        help="Idioma das replies (pt, en, es, etc)"
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
        help="Apenas replies com imagens"
    )

    parser.add_argument(
        "--videos",
        action="store_true",
        help="Apenas replies com vídeos"
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
        help="Número mínimo de replies (replies de replies)"
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
        help="Nome do arquivo de saída (padrão: replies_ID_TIMESTAMP.json)"
    )

    args = parser.parse_args()

    # Extrai ID do tweet
    tweet_id = extract_tweet_id(args.tweet)

    if not tweet_id.isdigit():
        print(f"❌ ID do tweet inválido: {tweet_id}")
        print(f"💡 Use o ID numérico ou a URL completa do tweet")
        sys.exit(1)

    print(f"💬 Scraping de replies do tweet {tweet_id}")
    if args.hashtag:
        print(f"🏷️  Filtrando por hashtag: #{args.hashtag}")

    # Executa scraping
    scraper = ApifyTwitterScraper()

    try:
        result = scraper.scrape_conversation(
            tweet_id=tweet_id,
            hashtag=args.hashtag,
            max_items=args.max_items,
            tweet_language=args.lang,
            only_verified_users=args.verified,
            only_twitter_blue=args.blue,
            only_image=args.images,
            only_video=args.videos,
            minimum_retweets=args.min_retweets,
            minimum_favorites=args.min_likes,
            minimum_replies=args.min_replies,
            sort=args.sort
        )

        # Nome do arquivo
        if args.output:
            filename = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"replies_{tweet_id}_{timestamp}.json"

        # Salva resultados
        output_path = os.path.expanduser(f"~/Downloads/{filename}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Scraping concluído!")
        print(f"💾 Resultados salvos em: {output_path}")
        print(f"\n📊 Estatísticas:")
        print(f"   Total de replies: {result['total_items']}")

        if result.get("stats"):
            stats = result["stats"]
            print(f"   Total de retweets: {stats.get('total_retweets', 0):,}")
            print(f"   Total de likes: {stats.get('total_likes', 0):,}")
            print(f"   Total de replies (de replies): {stats.get('total_replies', 0):,}")

            # Top autores (quem mais respondeu)
            if stats.get("authors"):
                print(f"\n👥 Top 5 autores (quem mais respondeu):")
                top_authors = sorted(
                    stats["authors"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                for author, count in top_authors:
                    print(f"   @{author}: {count} reply(ies)")

            # Idiomas
            if stats.get("languages"):
                print(f"\n🌍 Idiomas:")
                for lang, count in sorted(
                    stats["languages"].items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    print(f"   {lang}: {count} reply(ies)")

            # Tipos
            print(f"\n📝 Tipos:")
            print(f"   Replies diretas: {stats['total_tweets'] - stats.get('is_quote', 0)}")
            print(f"   Quote replies: {stats.get('is_quote', 0)}")

            # Mídia
            if stats.get("has_media"):
                print(f"\n🎨 Mídia:")
                print(f"   Com mídia: {stats.get('has_media', 0)}")
                print(f"   Com imagem: {stats.get('has_image', 0)}")
                print(f"   Com vídeo: {stats.get('has_video', 0)}")

        # Mostra replies com mais engajamento
        if result["items"]:
            # Ordena por engajamento total
            sorted_replies = sorted(
                result["items"],
                key=lambda t: t.get("likeCount", 0) + t.get("retweetCount", 0) * 2,
                reverse=True
            )

            print(f"\n🔥 Top 3 replies com mais engajamento:")
            for i, reply in enumerate(sorted_replies[:3], 1):
                total_engagement = (
                    reply.get("likeCount", 0) +
                    reply.get("retweetCount", 0) * 2
                )
                print(f"\n   Reply {i}:")
                print(f"   Autor: @{reply.get('author', {}).get('userName', 'N/A')}")
                author_info = reply.get('author', {})
                if author_info.get('isVerified'):
                    print(f"   ✓ Verificado")
                print(f"   Texto: {reply.get('text', '')[:150]}...")
                print(f"   ❤️  {reply.get('likeCount', 0)} | 🔁 {reply.get('retweetCount', 0)} | 💬 {reply.get('replyCount', 0)}")
                print(f"   Total: {total_engagement} interações")
                print(f"   URL: {reply.get('url', 'N/A')}")

            # Estatística de verificação
            verified_count = sum(
                1 for r in result["items"]
                if r.get("author", {}).get("isVerified")
            )
            if verified_count > 0:
                print(f"\n✓ {verified_count} reply(ies) de usuários verificados ({verified_count/len(result['items'])*100:.1f}%)")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
