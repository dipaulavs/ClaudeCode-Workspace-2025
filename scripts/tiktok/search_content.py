#!/usr/bin/env python3
"""
Template: Buscar conteúdo no TikTok

Uso:
    python3 scripts/tiktok/search_content.py --keyword "cat" --type video
    python3 scripts/tiktok/search_content.py --keyword "taylor" --type account
    python3 scripts/tiktok/search_content.py --keyword "dance" --type general
"""

import sys
import argparse
import json

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
from tools.tiktok_api23 import TikTokAPI23


def main():
    parser = argparse.ArgumentParser(description='Buscar conteúdo no TikTok')
    parser.add_argument('--keyword', required=True, help='Termo de busca')
    parser.add_argument('--type', choices=['video', 'account', 'general'], default='video',
                        help='Tipo de busca (padrão: video)')
    parser.add_argument('--limit', type=int, default=20, help='Limite de resultados (padrão: 20)')
    parser.add_argument('--full', action='store_true', help='Mostrar resposta completa')

    args = parser.parse_args()

    api = TikTokAPI23()

    print(f"🔍 Buscando '{args.keyword}' (tipo: {args.type})...\n")

    try:
        # Executar busca baseado no tipo
        if args.type == 'video':
            result = api.search_videos(args.keyword)
        elif args.type == 'account':
            result = api.search_accounts(args.keyword)
        else:  # general
            result = api.search_general(args.keyword)

        if args.full:
            # Mostrar JSON completo
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Mostrar resumo formatado
            if args.type == 'video':
                videos = result.get('data', [])[:args.limit]
                print(f"🎬 Encontrados {len(videos)} vídeos:\n")

                for i, video in enumerate(videos, 1):
                    author = video.get('author', {}).get('nickname', 'N/A')
                    desc = video.get('desc', '')[:50] + '...' if len(video.get('desc', '')) > 50 else video.get('desc', '')
                    likes = video.get('stats', {}).get('diggCount', 0)
                    print(f"{i}. {author}: {desc}")
                    print(f"   ❤️  {likes:,} likes")

            elif args.type == 'account':
                accounts = result.get('data', [])[:args.limit]
                print(f"👤 Encontradas {len(accounts)} contas:\n")

                for i, account in enumerate(accounts, 1):
                    nickname = account.get('nickname', 'N/A')
                    username = account.get('uniqueId', 'N/A')
                    followers = account.get('stats', {}).get('followerCount', 0)
                    print(f"{i}. {nickname} (@{username})")
                    print(f"   👥 {followers:,} seguidores")

            else:  # general
                print("📋 Resultados gerais:")
                print(json.dumps(result, indent=2, ensure_ascii=False)[:500] + "...")

            # Mostrar sugestões relacionadas
            print(f"\n💡 Sugestões relacionadas:")
            suggestions = api.search_others_searched_for(args.keyword)
            if suggestions:
                for suggestion in suggestions[:5]:
                    print(f"  - {suggestion}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
