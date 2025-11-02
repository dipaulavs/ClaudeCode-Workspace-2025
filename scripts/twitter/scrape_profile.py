#!/usr/bin/env python3
"""
Template: Scraping de perfil do Twitter/X (histórico de tweets)

Twitter retorna ~800 tweets por busca. Este script divide automaticamente
o scraping em períodos (mês, semana, dia) para coletar histórico completo.

Exemplos de uso:
    # Scraping básico (últimos ~800 tweets)
    python3 scrape_profile.py elonmusk

    # Histórico completo de 2023
    python3 scrape_profile.py NASA --year 2023

    # Período específico
    python3 scrape_profile.py NASA --since 2023-01-01 --until 2023-12-31

    # Histórico multi-ano (dividido por mês automaticamente)
    python3 scrape_profile.py NASA --from-year 2020 --to-year 2024

    # Com filtros
    python3 scrape_profile.py NASA --year 2023 --images --min-likes 1000

    # Limite de tweets
    python3 scrape_profile.py elonmusk --max-items 5000
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
        description="Scraping de perfil do Twitter/X (histórico de tweets)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Estratégias de coleta:

  1. Scraping simples (~800 tweets):
     python3 scrape_profile.py elonmusk

  2. Ano específico (dividido por mês automaticamente):
     python3 scrape_profile.py NASA --year 2023

  3. Período customizado:
     python3 scrape_profile.py NASA --since 2023-01-01 --until 2023-06-30

  4. Histórico completo multi-ano:
     python3 scrape_profile.py NASA --from-year 2020 --to-year 2024

Nota: Se o perfil tweeta mais de ~800 vezes por mês, considere usar
períodos menores (semanal ou diário) via --since e --until.
        """
    )

    # Argumento principal
    parser.add_argument(
        "handle",
        help="Handle do Twitter (sem @)"
    )

    # Opções de período
    period_group = parser.add_mutually_exclusive_group()

    period_group.add_argument(
        "--year",
        type=int,
        help="Ano específico (divide por mês automaticamente)"
    )

    period_group.add_argument(
        "--from-year",
        type=int,
        help="Ano inicial (usar com --to-year)"
    )

    parser.add_argument(
        "--to-year",
        type=int,
        help="Ano final (usar com --from-year)"
    )

    parser.add_argument(
        "--since",
        help="Data inicial (YYYY-MM-DD) - período customizado"
    )

    parser.add_argument(
        "--until",
        help="Data final (YYYY-MM-DD) - período customizado"
    )

    # Limites
    parser.add_argument(
        "--max-items",
        type=int,
        help="Número máximo de tweets total"
    )

    # Filtros
    parser.add_argument(
        "--lang",
        help="Idioma dos tweets (pt, en, es, etc)"
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
        help="Nome do arquivo de saída (padrão: perfil_HANDLE_TIMESTAMP.json)"
    )

    args = parser.parse_args()

    # Remove @ se presente
    handle = args.handle.lstrip("@")

    print(f"👤 Scraping do perfil @{handle}")

    # Determina estratégia de scraping
    scraper = ApifyTwitterScraper()

    # Caso 1: Histórico multi-ano
    if args.from_year and args.to_year:
        print(f"📅 Período: {args.from_year} - {args.to_year}")
        print(f"⚠️  Dividindo scraping por mês (otimizado para coletar máximo de tweets)")

        result = scraper.scrape_profile_historical(
            handle=handle,
            start_year=args.from_year,
            end_year=args.to_year,
            max_items=args.max_items,
            tweet_language=args.lang,
            only_image=args.images,
            only_video=args.videos,
            only_quote=args.quotes,
            minimum_retweets=args.min_retweets,
            minimum_favorites=args.min_likes,
            minimum_replies=args.min_replies,
            sort=args.sort
        )

    # Caso 2: Ano específico
    elif args.year:
        print(f"📅 Ano: {args.year}")
        print(f"⚠️  Dividindo scraping por mês (otimizado para coletar máximo de tweets)")

        result = scraper.scrape_profile_historical(
            handle=handle,
            start_year=args.year,
            end_year=args.year,
            max_items=args.max_items,
            tweet_language=args.lang,
            only_image=args.images,
            only_video=args.videos,
            only_quote=args.quotes,
            minimum_retweets=args.min_retweets,
            minimum_favorites=args.min_likes,
            minimum_replies=args.min_replies,
            sort=args.sort
        )

    # Caso 3: Período customizado ou scraping simples
    else:
        query = f"from:{handle}"

        if args.since:
            query += f" since:{args.since}"
            print(f"📅 Desde: {args.since}")

        if args.until:
            query += f" until:{args.until}"
            print(f"📅 Até: {args.until}")

        if not args.since and not args.until:
            print(f"📅 Período: Últimos ~800 tweets")

        result = scraper.scrape(
            search_terms=[query],
            max_items=args.max_items,
            tweet_language=args.lang,
            only_image=args.images,
            only_video=args.videos,
            only_quote=args.quotes,
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
        filename = f"perfil_{handle}_{timestamp}.json"

    # Salva resultados
    output_path = os.path.expanduser(f"~/Downloads/{filename}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Scraping concluído!")
    print(f"💾 Resultados salvos em: {output_path}")
    print(f"\n📊 Estatísticas:")
    print(f"   Total de tweets: {result['total_items']}")

    if result.get("stats"):
        stats = result["stats"]
        print(f"   Total de retweets: {stats.get('total_retweets', 0):,}")
        print(f"   Total de likes: {stats.get('total_likes', 0):,}")
        print(f"   Total de replies: {stats.get('total_replies', 0):,}")

        # Tipos de tweet
        print(f"\n📝 Tipos de tweet:")
        print(f"   Originais: {stats['total_tweets'] - stats.get('is_retweet', 0) - stats.get('is_quote', 0)}")
        print(f"   Retweets: {stats.get('is_retweet', 0)}")
        print(f"   Quotes: {stats.get('is_quote', 0)}")
        print(f"   Replies: {stats.get('is_reply', 0)}")

        # Mídia
        if stats.get("has_media"):
            print(f"\n🎨 Mídia:")
            print(f"   Com mídia: {stats.get('has_media', 0)}")
            print(f"   Com imagem: {stats.get('has_image', 0)}")
            print(f"   Com vídeo: {stats.get('has_video', 0)}")

        # Idiomas
        if stats.get("languages") and len(stats["languages"]) > 1:
            print(f"\n🌍 Idiomas:")
            for lang, count in stats["languages"].items():
                print(f"   {lang}: {count} tweet(s)")

    # Mostra preview dos tweets mais engajados
    if result["items"]:
        # Ordena por engajamento total
        sorted_tweets = sorted(
            result["items"],
            key=lambda t: t.get("likeCount", 0) + t.get("retweetCount", 0) * 2 + t.get("replyCount", 0),
            reverse=True
        )

        print(f"\n🔥 Top 3 tweets com mais engajamento:")
        for i, tweet in enumerate(sorted_tweets[:3], 1):
            total_engagement = (
                tweet.get("likeCount", 0) +
                tweet.get("retweetCount", 0) * 2 +
                tweet.get("replyCount", 0)
            )
            print(f"\n   Tweet {i}:")
            print(f"   Texto: {tweet.get('text', '')[:100]}...")
            print(f"   ❤️  {tweet.get('likeCount', 0)} | 🔁 {tweet.get('retweetCount', 0)} | 💬 {tweet.get('replyCount', 0)}")
            print(f"   Total: {total_engagement} interações")
            print(f"   Data: {tweet.get('createdAt', 'N/A')}")
            print(f"   URL: {tweet.get('url', 'N/A')}")


if __name__ == "__main__":
    main()
