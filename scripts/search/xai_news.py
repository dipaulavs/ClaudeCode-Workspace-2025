#!/usr/bin/env python3.11
"""
Template para busca em notícias usando xAI Search

Realiza buscas em fontes de notícias confiáveis, ideal para acompanhar
breaking news, análises jornalísticas e cobertura de eventos atuais.

Uso:
    python3.11 scripts/search/xai_news.py "sua busca aqui"
    python3.11 scripts/search/xai_news.py "política Brasil" --24h
    python3.11 scripts/search/xai_news.py "tecnologia" --last-week
    python3.11 scripts/search/xai_news.py "economia" --max-results 10

Exemplos:
    # Busca básica em notícias
    python3.11 scripts/search/xai_news.py "inteligência artificial"

    # Notícias das últimas 24 horas
    python3.11 scripts/search/xai_news.py "breaking news" --24h

    # Notícias da última semana
    python3.11 scripts/search/xai_news.py "mercado financeiro" --last-week

    # Buscar com mais fontes
    python3.11 scripts/search/xai_news.py "política internacional" --max-results 10
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.search import SearchParameters, news_source, web_source
from config.xai_config import XAI_API_KEY


def buscar_noticias(
    query: str,
    max_results: int = 5,
    model: str = "grok-4-fast",
    return_citations: bool = True,
    last_24h: bool = False,
    last_week: bool = False,
    include_web: bool = True
):
    """
    Realiza busca em notícias

    Args:
        query: Texto da busca
        max_results: Número máximo de fontes (padrão: 5)
        model: Modelo xAI a usar (padrão: grok-4-fast)
        return_citations: Se deve retornar URLs das fontes (padrão: True)
        last_24h: Se deve buscar apenas últimas 24h
        last_week: Se deve buscar apenas última semana
        include_web: Se deve incluir fontes web além de notícias (padrão: True)

    Returns:
        dict: Dicionário com 'content', 'citations' e 'num_sources_used'
    """
    # Inicializa cliente
    client = Client(api_key=XAI_API_KEY)

    # Configura fontes (notícias + web se solicitado)
    sources = [news_source()]
    if include_web:
        sources.append(web_source())

    # Configura parâmetros de busca
    search_params = SearchParameters(
        mode="on",  # Força busca sempre
        max_search_results=max_results,
        return_citations=return_citations,
        sources=sources
    )

    # Adiciona filtro de data
    if last_24h:
        search_params.from_date = datetime.now() - timedelta(days=1)
        search_params.to_date = datetime.now()
    elif last_week:
        search_params.from_date = datetime.now() - timedelta(days=7)
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
        description='Busca em notícias usando xAI Search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s "inteligência artificial"
  %(prog)s "breaking news" --24h
  %(prog)s "mercado financeiro" --last-week
  %(prog)s "política" --max-results 10 --news-only
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
        '--24h',
        dest='last_24h',
        action='store_true',
        help='Buscar apenas notícias das últimas 24 horas'
    )

    parser.add_argument(
        '--last-week',
        action='store_true',
        help='Buscar apenas notícias da última semana'
    )

    parser.add_argument(
        '--news-only',
        action='store_true',
        help='Buscar apenas em fontes de notícias (excluir web geral)'
    )

    parser.add_argument(
        '--no-citations',
        action='store_true',
        help='Não mostrar URLs das fontes'
    )

    args = parser.parse_args()

    # Junta a query se vier em múltiplas partes
    query = ' '.join(args.query)

    print(f"\n📰 Buscando em notícias: {query}\n")
    print(f"📊 Modelo: {args.model}")
    print(f"📈 Máximo de fontes: {args.max_results}")
    if args.last_24h:
        print("⏰ Período: Últimas 24 horas")
    elif args.last_week:
        print("⏰ Período: Última semana")
    if args.news_only:
        print("📑 Tipo: Apenas fontes de notícias")
    else:
        print("📑 Tipo: Notícias + Web")
    print("\n" + "=" * 80)

    try:
        # Realiza busca
        result = buscar_noticias(
            query=query,
            max_results=args.max_results,
            model=args.model,
            return_citations=not args.no_citations,
            last_24h=args.last_24h,
            last_week=args.last_week,
            include_web=not args.news_only
        )

        # Exibe resultado
        print(f"\n📝 Resposta:\n")
        print(result['content'])

        # Exibe citações
        if not args.no_citations and result['citations']:
            print(f"\n\n📚 Fontes utilizadas ({result['num_sources_used']}):\n")
            for i, citation in enumerate(result['citations'], 1):
                print(f"{i}. {citation}")

        print("\n" + "=" * 80)
        print(f"\n✅ Busca concluída! {result['num_sources_used']} fontes consultadas.\n")

    except Exception as e:
        print(f"\n❌ Erro ao realizar busca: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
