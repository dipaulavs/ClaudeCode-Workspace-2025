#!/usr/bin/env python3
"""
Template: Obter informações de vídeo do TikTok

Uso:
    python3 scripts/tiktok/get_video_info.py --video-id 7306132438047116586
    python3 scripts/tiktok/get_video_info.py --video-id 7306132438047116586 --comments 50
"""

import sys
import argparse
import json

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
from tools.tiktok_api23 import TikTokAPI23


def main():
    parser = argparse.ArgumentParser(description='Obter informações de vídeo do TikTok')
    parser.add_argument('--video-id', required=True, help='ID do vídeo')
    parser.add_argument('--full', action='store_true', help='Mostrar resposta completa')
    parser.add_argument('--comments', type=int, help='Também buscar N comentários')

    args = parser.parse_args()

    api = TikTokAPI23()

    print(f"🎬 Buscando info do vídeo {args.video_id}...\n")

    try:
        # Buscar detalhes do vídeo
        result = api.get_post_detail(args.video_id)

        if args.full:
            # Mostrar JSON completo
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Mostrar resumo formatado
            video = result['itemInfo']['itemStruct']
            author = video['author']
            stats = video['stats']
            music = video.get('music', {})

            print(f"👤 Autor: {author['nickname']} (@{author['uniqueId']})")
            print(f"📝 Descrição: {video['desc']}")
            print(f"🎵 Música: {music.get('title', 'N/A')} - {music.get('authorName', 'N/A')}")
            print(f"\n📊 Estatísticas:")
            print(f"  👁️  Views: {stats.get('playCount', 0):,}")
            print(f"  ❤️  Likes: {stats['diggCount']:,}")
            print(f"  💬 Comentários: {stats['commentCount']:,}")
            print(f"  🔄 Shares: {stats['shareCount']:,}")

            # Buscar comentários se solicitado
            if args.comments:
                print(f"\n💬 Buscando {args.comments} comentários...")
                comments_result = api.get_post_comments(args.video_id, count=args.comments)

                if comments_result.get('comments'):
                    print(f"\n📝 Top {len(comments_result['comments'])} comentários:")
                    for i, comment in enumerate(comments_result['comments'][:args.comments], 1):
                        text = comment['text'][:60] + '...' if len(comment['text']) > 60 else comment['text']
                        likes = comment['digg_count']
                        user = comment['user']['nickname']
                        print(f"  {i}. {user}: {text} ({likes:,} likes)")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
