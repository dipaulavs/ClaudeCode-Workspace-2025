#!/usr/bin/env python3
"""
Template: Obter informações de usuário do TikTok

Uso:
    python3 scripts/tiktok/get_user_info.py --username taylorswift
    python3 scripts/tiktok/get_user_info.py --username tiktok --full
"""

import sys
import argparse
import json

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
from tools.tiktok_api23 import TikTokAPI23


def main():
    parser = argparse.ArgumentParser(description='Obter informações de usuário do TikTok')
    parser.add_argument('--username', required=True, help='Username do TikTok (sem @)')
    parser.add_argument('--full', action='store_true', help='Mostrar resposta completa')
    parser.add_argument('--posts', type=int, help='Também buscar N posts populares')

    args = parser.parse_args()

    api = TikTokAPI23()

    print(f"🔍 Buscando info do usuário @{args.username}...\n")

    try:
        # Buscar info do usuário
        result = api.get_user_info(args.username)

        if args.full:
            # Mostrar JSON completo
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Mostrar resumo formatado
            user = result['userInfo']['user']
            stats = result['userInfo']['stats']

            print(f"👤 Nome: {user['nickname']}")
            print(f"🔗 Username: @{user['uniqueId']}")
            print(f"📝 Bio: {user.get('signature', 'N/A')}")
            print(f"\n📊 Estatísticas:")
            print(f"  👥 Seguidores: {stats['followerCount']:,}")
            print(f"  👤 Seguindo: {stats['followingCount']:,}")
            print(f"  🎬 Vídeos: {stats['videoCount']:,}")
            print(f"  ❤️  Likes: {stats['heartCount']:,}")

            # Buscar posts se solicitado
            if args.posts:
                sec_uid = user['secUid']
                print(f"\n📹 Buscando {args.posts} posts populares...")
                posts_result = api.get_user_popular_posts(sec_uid, count=args.posts)

                if posts_result.get('itemList'):
                    print(f"\n🎬 Top {len(posts_result['itemList'])} posts:")
                    for i, post in enumerate(posts_result['itemList'][:args.posts], 1):
                        desc = post['desc'][:50] + '...' if len(post['desc']) > 50 else post['desc']
                        likes = post['stats']['diggCount']
                        print(f"  {i}. {desc} ({likes:,} likes)")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
