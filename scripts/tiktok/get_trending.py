#!/usr/bin/env python3
"""
Template: Obter conteúdo em trending do TikTok

Uso:
    python3 scripts/tiktok/get_trending.py --type videos
    python3 scripts/tiktok/get_trending.py --type hashtags --country BR
    python3 scripts/tiktok/get_trending.py --type songs --period 7
    python3 scripts/tiktok/get_trending.py --type creators --country US
"""

import sys
import argparse
import json

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
from tools.tiktok_api23 import TikTokAPI23


def main():
    parser = argparse.ArgumentParser(description='Obter conteúdo em trending do TikTok')
    parser.add_argument('--type', choices=['videos', 'hashtags', 'songs', 'creators', 'keywords'],
                        required=True, help='Tipo de trending')
    parser.add_argument('--country', default='US', help='Código do país (padrão: US)')
    parser.add_argument('--period', type=int, default=7, help='Período em dias (padrão: 7)')
    parser.add_argument('--limit', type=int, default=20, help='Limite de resultados (padrão: 20)')
    parser.add_argument('--full', action='store_true', help='Mostrar resposta completa')

    args = parser.parse_args()

    api = TikTokAPI23()

    print(f"📈 Buscando {args.type} em trending ({args.country})...\n")

    try:
        # Executar busca baseado no tipo
        if args.type == 'videos':
            result = api.get_trending_posts(count=args.limit)
        elif args.type == 'hashtags':
            result = api.get_trending_hashtags(
                period=args.period * 24,  # converter dias para horas
                country=args.country,
                limit=args.limit
            )
        elif args.type == 'songs':
            result = api.get_trending_songs(
                period=args.period,
                country=args.country,
                limit=args.limit
            )
        elif args.type == 'creators':
            result = api.get_trending_creators(
                country=args.country,
                limit=args.limit
            )
        else:  # keywords
            result = api.get_trending_keywords(
                period=args.period,
                country=args.country,
                limit=args.limit
            )

        if args.full:
            # Mostrar JSON completo
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Mostrar resumo formatado
            if args.type == 'videos':
                videos = result.get('itemList', [])
                print(f"🎬 Top {len(videos)} vídeos em trending:\n")

                for i, video in enumerate(videos, 1):
                    author = video.get('author', {}).get('nickname', 'N/A')
                    desc = video.get('desc', '')[:50] + '...' if len(video.get('desc', '')) > 50 else video.get('desc', '')
                    likes = video.get('stats', {}).get('diggCount', 0)
                    print(f"{i}. {author}: {desc}")
                    print(f"   ❤️  {likes:,} likes\n")

            elif args.type == 'hashtags':
                hashtags = result.get('data', [])
                print(f"#️⃣ Top {len(hashtags)} hashtags em trending:\n")

                for i, tag in enumerate(hashtags, 1):
                    name = tag.get('hashtag_name', 'N/A')
                    views = tag.get('view_count', 0)
                    print(f"{i}. #{name}")
                    print(f"   👁️  {views:,} views\n")

            elif args.type == 'songs':
                songs = result.get('data', [])
                print(f"🎵 Top {len(songs)} músicas em trending:\n")

                for i, song in enumerate(songs, 1):
                    title = song.get('title', 'N/A')
                    author = song.get('author', 'N/A')
                    posts = song.get('post_count', 0)
                    print(f"{i}. {title} - {author}")
                    print(f"   🎬 {posts:,} posts\n")

            elif args.type == 'creators':
                creators = result.get('data', [])
                print(f"👤 Top {len(creators)} criadores em trending:\n")

                for i, creator in enumerate(creators, 1):
                    nickname = creator.get('nickname', 'N/A')
                    username = creator.get('unique_id', 'N/A')
                    followers = creator.get('follower_count', 0)
                    print(f"{i}. {nickname} (@{username})")
                    print(f"   👥 {followers:,} seguidores\n")

            else:  # keywords
                keywords = result.get('data', [])
                print(f"🔑 Top {len(keywords)} keywords em trending:\n")

                for i, kw in enumerate(keywords, 1):
                    word = kw.get('keyword', 'N/A')
                    volume = kw.get('search_volume', 0)
                    print(f"{i}. {word}")
                    print(f"   🔍 {volume:,} buscas\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
