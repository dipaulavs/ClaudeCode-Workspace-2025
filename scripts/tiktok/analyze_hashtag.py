#!/usr/bin/env python3
"""
Template: Analisar hashtag do TikTok

Uso:
    python3 scripts/tiktok/analyze_hashtag.py --hashtag cat
    python3 scripts/tiktok/analyze_hashtag.py --hashtag fyp --posts 30
"""

import sys
import argparse
import json

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
from tools.tiktok_api23 import TikTokAPI23


def main():
    parser = argparse.ArgumentParser(description='Analisar hashtag do TikTok')
    parser.add_argument('--hashtag', required=True, help='Nome da hashtag (sem #)')
    parser.add_argument('--posts', type=int, default=20, help='Número de posts para buscar (padrão: 20)')
    parser.add_argument('--full', action='store_true', help='Mostrar resposta completa')

    args = parser.parse_args()

    api = TikTokAPI23()

    hashtag = args.hashtag.replace('#', '')  # Remover # se usuário incluiu

    print(f"#️⃣ Analisando hashtag #{hashtag}...\n")

    try:
        # 1. Buscar info da hashtag
        info = api.get_challenge_info(hashtag)

        if args.full:
            print("📊 INFO DA HASHTAG:")
            print(json.dumps(info, indent=2, ensure_ascii=False))
            print("\n" + "="*50 + "\n")
        else:
            challenge = info.get('challengeInfo', {}).get('challenge', {})
            stats = info.get('challengeInfo', {}).get('stats', {})

            print(f"📝 Nome: #{challenge.get('title', 'N/A')}")
            print(f"📄 Descrição: {challenge.get('desc', 'N/A')}")
            print(f"\n📊 Estatísticas:")
            print(f"  👁️  Views: {stats.get('viewCount', 0):,}")
            print(f"  🎬 Posts: {stats.get('videoCount', 0):,}")

            # 2. Buscar posts da hashtag
            challenge_id = challenge.get('id')
            if challenge_id:
                print(f"\n🎬 Buscando top {args.posts} posts da hashtag...\n")
                posts_result = api.get_challenge_posts(challenge_id, count=args.posts)

                if posts_result.get('itemList'):
                    posts = posts_result['itemList']
                    print(f"📹 Encontrados {len(posts)} posts:\n")

                    total_likes = 0
                    total_comments = 0
                    total_shares = 0

                    for i, post in enumerate(posts[:args.posts], 1):
                        author = post.get('author', {}).get('nickname', 'N/A')
                        desc = post.get('desc', '')[:40] + '...' if len(post.get('desc', '')) > 40 else post.get('desc', '')
                        likes = post.get('stats', {}).get('diggCount', 0)
                        comments = post.get('stats', {}).get('commentCount', 0)
                        shares = post.get('stats', {}).get('shareCount', 0)

                        total_likes += likes
                        total_comments += comments
                        total_shares += shares

                        print(f"{i}. {author}: {desc}")
                        print(f"   ❤️  {likes:,} | 💬 {comments:,} | 🔄 {shares:,}\n")

                    # Média de engajamento
                    avg_likes = total_likes // len(posts) if posts else 0
                    avg_comments = total_comments // len(posts) if posts else 0
                    avg_shares = total_shares // len(posts) if posts else 0

                    print("="*50)
                    print(f"\n📈 Média de engajamento por post:")
                    print(f"  ❤️  Likes: {avg_likes:,}")
                    print(f"  💬 Comentários: {avg_comments:,}")
                    print(f"  🔄 Shares: {avg_shares:,}")
                else:
                    print("Nenhum post encontrado para esta hashtag.")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
