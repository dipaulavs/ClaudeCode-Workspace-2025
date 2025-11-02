#!/usr/bin/env python3.11
"""
Template para busca na web usando xAI Search

Realiza buscas apenas em fontes web, excluindo Twitter/X e outras redes sociais.
Ideal para pesquisas de artigos, documentação técnica e conteúdo web geral.

Uso:
    python3.11 scripts/search/xai_web.py "sua busca aqui"
    python3.11 scripts/search/xai_web.py "tutoriais Python" --max-results 10
    python3.11 scripts/search/xai_web.py "documentação React" --model grok-4

Exemplos:
    # Busca básica
    python3.11 scripts/search/xai_web.py "melhores práticas Python 2025"

    # Com mais resultados
    python3.11 scripts/search/xai_web.py "tutoriais React avançados" --max-results 10

    # Usando modelo mais poderoso
    python3.11 scripts/search/xai_web.py "arquitetura de software" --model grok-4
"""

import sys
import os
import argparse

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.search import SearchParameters, web_source
from config.xai_config import XAI_API_KEY


def buscar_web(
    query: str,
    max_results: int = 5,
    model: str = "grok-4-fast",
    return_citations: bool = True
):
    """
    Realiza busca apenas na web

    Args:
        query: Texto da busca
        max_results: Número máximo de fontes (padrão: 5)
        model: Modelo xAI a usar (padrão: grok-4-fast)
        return_citations: Se deve retornar URLs das fontes (padrão: True)

    Returns:
        dict: Dicionário com 'content', 'citations' e 'num_sources_used'
    """
    # Inicializa cliente
    client = Client(api_key=XAI_API_KEY)

    # Configura parâmetros de busca (apenas web)
    search_params = SearchParameters(
        mode="on",  # Força busca sempre
        max_search_results=max_results,
        return_citations=return_citations,
        sources=[web_source()]  # Apenas web
    )

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
        description='Busca na web usando xAI Search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s "tutoriais Python avançados"
  %(prog)s "documentação React hooks" --max-results 10
  %(prog)s "melhores práticas Node.js" --model grok-4
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
        '--no-citations',
        action='store_true',
        help='Não mostrar URLs das fontes'
    )

    args = parser.parse_args()

    # Junta a query se vier em múltiplas partes
    query = ' '.join(args.query)

    print(f"\n🔍 Buscando na web: {query}\n")
    print(f"📊 Modelo: {args.model}")
    print(f"📈 Máximo de fontes: {args.max_results}\n")
    print("=" * 80)

    try:
        # Realiza busca
        result = buscar_web(
            query=query,
            max_results=args.max_results,
            model=args.model,
            return_citations=not args.no_citations
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
