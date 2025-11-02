#!/usr/bin/env python3
"""
Template: Obter métricas do Instagram

Uso:
    # Métricas da conta
    python3 scripts/instagram/get_insights.py --account

    # Métricas de post específico
    python3 scripts/instagram/get_insights.py --media MEDIA_ID

    # Posts recentes com métricas
    python3 scripts/instagram/get_insights.py --recent --limit 10

    # Salvar em arquivo JSON
    python3 scripts/instagram/get_insights.py --account --output insights.json
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.get_instagram_insights import InstagramInsights


def get_insights(mode: str, media_id: str = None, limit: int = 25, output: str = None):
    """
    Obtém métricas do Instagram

    Args:
        mode: Tipo de métrica ('account', 'media', 'recent')
        media_id: ID do post (necessário se mode='media')
        limit: Quantidade de posts recentes (padrão: 25)
        output: Arquivo para salvar JSON (opcional)

    Returns:
        dict: Dados das métricas
    """

    # Inicializa insights
    insights = InstagramInsights()

    # Obtém métricas conforme modo
    if mode == 'account':
        data = insights.get_account_insights()
    elif mode == 'media':
        if not media_id:
            raise ValueError("--media requer ID do post")
        data = insights.get_media_insights(media_id)
    elif mode == 'recent':
        data = insights.get_recent_media(limit)
    else:
        raise ValueError(f"Modo inválido: {mode}")

    # Salva em arquivo se especificado
    if output:
        import json
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Dados salvos em: {output}")

    return data


def main():
    parser = argparse.ArgumentParser(description='Obter métricas do Instagram')

    # Modos mutuamente exclusivos
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--account', action='store_true', help='Métricas da conta')
    mode_group.add_argument('--media', help='ID do post para métricas específicas')
    mode_group.add_argument('--recent', action='store_true', help='Posts recentes com métricas')

    parser.add_argument('--limit', '-l', type=int, default=25, help='Quantidade de posts recentes (padrão: 25)')
    parser.add_argument('--output', '-o', help='Salvar em arquivo JSON (opcional)')

    args = parser.parse_args()

    # Determina modo
    if args.account:
        mode = 'account'
        media_id = None
    elif args.media:
        mode = 'media'
        media_id = args.media
    else:  # args.recent
        mode = 'recent'
        media_id = None

    print(f"📊 Obtendo métricas do Instagram...")

    try:
        data = get_insights(mode, media_id, args.limit, args.output)

        # Exibe resumo
        if mode == 'account':
            print(f"✅ Métricas da conta:")
            print(f"   Seguidores: {data.get('followers_count', 'N/A')}")
            print(f"   Seguindo: {data.get('follows_count', 'N/A')}")
            print(f"   Posts: {data.get('media_count', 'N/A')}")
        elif mode == 'media':
            print(f"✅ Métricas do post {media_id}:")
            print(f"   Curtidas: {data.get('like_count', 'N/A')}")
            print(f"   Comentários: {data.get('comments_count', 'N/A')}")
        else:  # recent
            print(f"✅ {len(data)} posts recentes com métricas")

        if not args.output:
            import json
            print("\n" + json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
