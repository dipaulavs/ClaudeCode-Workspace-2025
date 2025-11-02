#!/usr/bin/env python3
"""
Template: Scraping de tweets específicos por URL

Coleta informações detalhadas de tweets individuais ou múltiplos.

Exemplos de uso:
    # Tweet único
    python3 scrape_tweets.py "https://twitter.com/elonmusk/status/1234567890"

    # Múltiplos tweets
    python3 scrape_tweets.py "https://twitter.com/user1/status/123" "https://twitter.com/user2/status/456"

    # Lista de URLs de arquivo
    python3 scrape_tweets.py --from-file urls.txt

    # Com limite
    python3 scrape_tweets.py "https://twitter.com/..." --max-items 10

Nota: URLs podem ser twitter.com ou x.com (ambos funcionam)
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tools.apify_twitter import ApifyTwitterScraper


def read_urls_from_file(filepath: str) -> list:
    """Lê URLs de um arquivo (uma por linha)"""
    urls = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignora linhas vazias e comentários
                urls.append(line)
    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Scraping de tweets específicos por URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

  Tweet único:
    python3 scrape_tweets.py "https://twitter.com/elonmusk/status/1728108619189874825"

  Múltiplos tweets:
    python3 scrape_tweets.py "URL1" "URL2" "URL3"

  De arquivo:
    python3 scrape_tweets.py --from-file urls.txt

Formato do arquivo (urls.txt):
  https://twitter.com/user1/status/123
  https://twitter.com/user2/status/456
  # Comentários são ignorados
  https://x.com/user3/status/789

Nota: Tanto twitter.com quanto x.com funcionam.
        """
    )

    # Argumentos principais
    parser.add_argument(
        "urls",
        nargs="*",
        help="URL(s) dos tweets"
    )

    parser.add_argument(
        "--from-file",
        help="Arquivo com URLs (uma por linha)"
    )

    # Limites
    parser.add_argument(
        "--max-items",
        type=int,
        help="Número máximo de tweets (útil para listas grandes)"
    )

    # Output
    parser.add_argument(
        "--output",
        help="Nome do arquivo de saída (padrão: tweets_TIMESTAMP.json)"
    )

    args = parser.parse_args()

    # Coleta URLs
    urls = []

    if args.urls:
        urls.extend(args.urls)

    if args.from_file:
        if not os.path.exists(args.from_file):
            print(f"❌ Arquivo não encontrado: {args.from_file}")
            sys.exit(1)

        file_urls = read_urls_from_file(args.from_file)
        urls.extend(file_urls)
        print(f"📄 {len(file_urls)} URL(s) carregadas de {args.from_file}")

    # Valida
    if not urls:
        parser.error("Informe pelo menos uma URL ou use --from-file")

    # Remove duplicatas
    urls = list(set(urls))

    print(f"🐦 Scraping de tweets...")
    print(f"📊 Total de URLs: {len(urls)}")

    # Normaliza URLs (twitter.com ou x.com, ambos funcionam)
    normalized_urls = []
    for url in urls:
        # Garante que é uma URL válida do Twitter
        if "twitter.com" in url or "x.com" in url:
            normalized_urls.append(url)
        else:
            print(f"⚠️  URL inválida (ignorada): {url}")

    if not normalized_urls:
        print(f"❌ Nenhuma URL válida encontrada")
        sys.exit(1)

    print(f"✅ URLs válidas: {len(normalized_urls)}")

    # Executa scraping
    scraper = ApifyTwitterScraper()

    try:
        result = scraper.scrape(
            start_urls=normalized_urls,
            max_items=args.max_items
        )

        # Nome do arquivo
        if args.output:
            filename = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tweets_{timestamp}.json"

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

            # Autores
            if stats.get("authors"):
                print(f"\n👥 Autores:")
                for author, count in stats["authors"].items():
                    print(f"   @{author}: {count} tweet(s)")

            # Tipos
            print(f"\n📝 Tipos:")
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

        # Preview dos tweets
        if result["items"]:
            print(f"\n📄 Preview dos tweets:")
            for i, tweet in enumerate(result["items"], 1):
                print(f"\n   Tweet {i}/{len(result['items'])}:")
                print(f"   Autor: @{tweet.get('author', {}).get('userName', 'N/A')}")
                print(f"   Data: {tweet.get('createdAt', 'N/A')}")
                print(f"   Texto: {tweet.get('text', '')[:100]}...")
                print(f"   ❤️  {tweet.get('likeCount', 0)} | 🔁 {tweet.get('retweetCount', 0)} | 💬 {tweet.get('replyCount', 0)}")
                print(f"   URL: {tweet.get('url', 'N/A')}")

                # Mostra mídia se houver
                media = tweet.get("media", [])
                if media:
                    print(f"   🎨 Mídia: {len(media)} arquivo(s)")
                    for m in media[:2]:  # Max 2 para não poluir
                        print(f"      - {m.get('type', 'unknown')}: {m.get('url', 'N/A')}")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
