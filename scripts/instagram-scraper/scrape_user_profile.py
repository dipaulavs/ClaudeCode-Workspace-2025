#!/usr/bin/env python3
"""
Template: Scrape Perfil de Usuário do Instagram

Extrai detalhes completos de um perfil do Instagram (biografia, seguidores, posts recentes, etc).

Uso:
    python3 scrape_user_profile.py "natgeo"
    python3 scrape_user_profile.py "avengers" --output perfil_avengers.json

Autor: Claude Code
Data: 2025-11-02
"""

import sys
import os
import argparse
import json

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.apify_instagram import InstagramScraper


def main():
    parser = argparse.ArgumentParser(
        description="Scrape perfil de usuário do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python3 scrape_user_profile.py "natgeo"
  python3 scrape_user_profile.py "avengers" --output perfil_avengers.json
        """
    )

    parser.add_argument('username', help='Username do Instagram (sem @)')
    parser.add_argument('--output', help='Arquivo de saída (JSON)')

    args = parser.parse_args()

    # Executar
    scraper = InstagramScraper()

    result = scraper.scrape_user_profile(
        username=args.username,
        output_file=args.output
    )

    # Mostrar detalhes do perfil
    if result.get("success") and result.get("items"):
        profile = result["items"][0]

        print(f"\n👤 Perfil de @{profile.get('username', 'N/A')}")
        print("=" * 50)

        # Informações básicas
        print(f"\n📊 Informações Básicas:")
        print(f"   Nome: {profile.get('fullName', 'N/A')}")
        print(f"   ID: {profile.get('id', 'N/A')}")
        verified = "✅ Verificado" if profile.get('verified') else "❌ Não verificado"
        print(f"   Status: {verified}")
        private = "🔒 Privado" if profile.get('private') else "🔓 Público"
        print(f"   Privacidade: {private}")

        # Biografia
        bio = profile.get('biography', '')
        if bio:
            print(f"\n📝 Biografia:")
            print(f"   {bio}")

        # URL externa
        url = profile.get('externalUrl', '')
        if url:
            print(f"\n🔗 Link: {url}")

        # Estatísticas
        print(f"\n📊 Estatísticas:")
        print(f"   👥 Seguidores: {profile.get('followersCount', 0):,}")
        print(f"   ➕ Seguindo: {profile.get('followsCount', 0):,}")
        print(f"   📸 Posts: {profile.get('postsCount', 0):,}")
        print(f"   📹 IGTV: {profile.get('igtvVideoCount', 0):,}")
        print(f"   🎯 Highlights: {profile.get('highlightReelCount', 0):,}")

        # Categoria de negócio
        if profile.get('isBusinessAccount'):
            category = profile.get('businessCategoryName', 'N/A')
            print(f"\n💼 Conta Business: {category}")

        # Posts recentes
        latest = profile.get('latestPosts', [])
        if latest:
            print(f"\n📸 Últimos {len(latest)} posts:")
            for i, post in enumerate(latest[:5], 1):
                print(f"   {i}. {post.get('type', 'Unknown')} - ❤️ {post.get('likesCount', 0):,} likes")

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
