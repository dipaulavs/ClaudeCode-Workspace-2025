#!/usr/bin/env python3.11
"""
Template para busca no Twitter/X usando xAI Search

Realiza buscas apenas no Twitter/X (agora X), ideal para monitorar tendências,
opiniões públicas, discussões e posts virais em tempo real.

Uso:
    python3.11 scripts/search/xai_twitter.py "sua busca aqui"
    python3.11 scripts/search/xai_twitter.py "python" --recent
    python3.11 scripts/search/xai_twitter.py "AI trends" --handles elonmusk,gdb
    python3.11 scripts/search/xai_twitter.py "viral memes" --min-likes 1000

Exemplos:
    # Busca básica
    python3.11 scripts/search/xai_twitter.py "opinião sobre IA"

    # Posts recentes (últimas 24h)
    python3.11 scripts/search/xai_twitter.py "breaking news" --recent

    # Filtrar por handles específicos
    python3.11 scripts/search/xai_twitter.py "tech news" --handles elonmusk,gdb,sama

    # Posts populares (min. curtidas/visualizações)
    python3.11 scripts/search/xai_twitter.py "AI art" --min-likes 1000 --min-views 10000
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.search import SearchParameters, x_source
from config.xai_config import XAI_API_KEY


def buscar_twitter(
    query: str,
    max_results: int = 5,
    model: str = "grok-4-fast",
    return_citations: bool = True,
    included_handles: list = None,
    excluded_handles: list = None,
    min_likes: int = None,
    min_views: int = None,
    recent: bool = False
):
    """
    Realiza busca no Twitter/X

    Args:
        query: Texto da busca
        max_results: Número máximo de fontes (padrão: 5)
        model: Modelo xAI a usar (padrão: grok-4-fast)
        return_citations: Se deve retornar URLs das fontes (padrão: True)
        included_handles: Lista de handles para incluir (max 10)
        excluded_handles: Lista de handles para excluir (max 10)
        min_likes: Número mínimo de curtidas
        min_views: Número mínimo de visualizações
        recent: Se deve buscar apenas posts das últimas 24h

    Returns:
        dict: Dicionário com 'content', 'citations' e 'num_sources_used'
    """
    # Inicializa cliente
    client = Client(api_key=XAI_API_KEY)

    # Configura fonte do Twitter/X
    x_src = x_source()

    # Adiciona filtros de handles
    if included_handles:
        x_src['included_x_handles'] = included_handles[:10]  # Max 10
    if excluded_handles:
        x_src['excluded_x_handles'] = excluded_handles[:10]  # Max 10

    # Adiciona filtros de popularidade
    if min_likes:
        x_src['post_favorite_count'] = min_likes
    if min_views:
        x_src['post_view_count'] = min_views

    # Configura parâmetros de busca
    search_params = SearchParameters(
        mode="on",  # Força busca sempre
        max_search_results=max_results,
        return_citations=return_citations,
        sources=[x_src]
    )

    # Adiciona filtro de data se recente
    if recent:
        search_params.from_date = datetime.now() - timedelta(days=1)
        search_params.to_date = datetime.now()

    # Cria chat e realiza busca
    chat = client.chat.create(
        model=model,
        search_parameters=search_params
    )

    chat.append(user(query))
    response = chat.sample()

    return {
        'content': response.content,
        'citations': response.citations if hasattr(response, 'citations') else [],
        'num_sources_used': response.usage.num_sources_used if hasattr(response.usage, 'num_sources_used') else 0
    }


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Busca no Twitter/X usando xAI Search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s "opinião sobre IA"
  %(prog)s "breaking news" --recent
  %(prog)s "tech news" --handles elonmusk,gdb
  %(prog)s "viral memes" --min-likes 1000 --min-views 10000
        """
    )

    parser.add_argument(
        'query',
        nargs='+',
        help='Texto da busca'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=5,
        help='Número máximo de fontes (padrão: 5)'
    )

    parser.add_argument(
        '--model',
        default='grok-4-fast',
        choices=['grok-4-fast', 'grok-4'],
        help='Modelo xAI a usar (padrão: grok-4-fast)'
    )

    parser.add_argument(
        '--handles',
        help='Handles para incluir, separados por vírgula (max 10). Ex: elonmusk,gdb,sama'
    )

    parser.add_argument(
        '--exclude-handles',
        help='Handles para excluir, separados por vírgula (max 10)'
    )

    parser.add_argument(
        '--min-likes',
        type=int,
        help='Número mínimo de curtidas'
    )

    parser.add_argument(
        '--min-views',
        type=int,
        help='Número mínimo de visualizações'
    )

    parser.add_argument(
        '--recent',
        action='store_true',
        help='Buscar apenas posts das últimas 24 horas'
    )

    parser.add_argument(
        '--no-citations',
        action='store_true',
        help='Não mostrar URLs das fontes'
    )

    args = parser.parse_args()

    # Junta a query se vier em múltiplas partes
    query = ' '.join(args.query)

    # Processa handles
    included_handles = args.handles.split(',') if args.handles else None
    excluded_handles = args.exclude_handles.split(',') if args.exclude_handles else None

    print(f"\n🐦 Buscando no Twitter/X: {query}\n")
    print(f"📊 Modelo: {args.model}")
    print(f"📈 Máximo de fontes: {args.max_results}")
    if args.recent:
        print("⏰ Filtro: Últimas 24 horas")
    if included_handles:
        print(f"👤 Incluir handles: {', '.join(included_handles)}")
    if excluded_handles:
        print(f"🚫 Excluir handles: {', '.join(excluded_handles)}")
    if args.min_likes:
        print(f"❤️ Mínimo de curtidas: {args.min_likes}")
    if args.min_views:
        print(f"👁️ Mínimo de visualizações: {args.min_views}")
    print("\n" + "=" * 80)

    try:
        # Realiza busca
        result = buscar_twitter(
            query=query,
            max_results=args.max_results,
            model=args.model,
            return_citations=not args.no_citations,
            included_handles=included_handles,
            excluded_handles=excluded_handles,
            min_likes=args.min_likes,
            min_views=args.min_views,
            recent=args.recent
        )

        # Exibe resultado
        print(f"\n📝 Resposta:\n")
        print(result['content'])

        # Exibe citações
        if not args.no_citations and result['citations']:
            print(f"\n\n📚 Posts encontrados ({result['num_sources_used']}):\n")
            for i, citation in enumerate(result['citations'], 1):
                print(f"{i}. {citation}")

        print("\n" + "=" * 80)
        print(f"\n✅ Busca concluída! {result['num_sources_used']} posts consultados.\n")

    except Exception as e:
        print(f"\n❌ Erro ao realizar busca: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
