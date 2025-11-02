#!/usr/bin/env python3.11
"""
Script de busca usando xAI Live Search API

Este script permite realizar buscas na web e no Twitter/X usando a API xAI
com configurações personalizadas.

Configurações padrão:
- Modelo: grok-4-fast
- Máximo de resultados: 5 fontes
- Fontes: Web e Twitter/X
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path para importar a config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.search import SearchParameters, web_source, x_source
from config.xai_config import (
    XAI_API_KEY,
    DEFAULT_MODEL,
    DEFAULT_MAX_SEARCH_RESULTS,
    DEFAULT_SEARCH_MODE,
    DEFAULT_RETURN_CITATIONS
)


class XAISearch:
    """Classe para realizar buscas usando a API xAI"""

    def __init__(
        self,
        api_key: str = XAI_API_KEY,
        model: str = DEFAULT_MODEL,
        max_results: int = DEFAULT_MAX_SEARCH_RESULTS,
        search_mode: str = DEFAULT_SEARCH_MODE,
        return_citations: bool = DEFAULT_RETURN_CITATIONS
    ):
        """
        Inicializa o cliente de busca xAI

        Args:
            api_key: Chave da API xAI
            model: Modelo a ser usado (padrão: grok-4-fast)
            max_results: Número máximo de fontes (padrão: 5)
            search_mode: Modo de busca - "auto", "on", "off" (padrão: auto)
            return_citations: Se deve retornar citações (padrão: True)
        """
        self.client = Client(api_key=api_key)
        self.model = model
        self.max_results = max_results
        self.search_mode = search_mode
        self.return_citations = return_citations

    def search(
        self,
        query: str,
        sources: list = None,
        from_date: datetime = None,
        to_date: datetime = None,
        **kwargs
    ):
        """
        Realiza uma busca

        Args:
            query: Pergunta ou busca a ser realizada
            sources: Lista de fontes personalizadas (opcional)
            from_date: Data inicial para filtrar resultados (opcional)
            to_date: Data final para filtrar resultados (opcional)
            **kwargs: Parâmetros adicionais para SearchParameters

        Returns:
            dict: Dicionário com 'content' e 'citations'
        """
        # Define fontes padrão se não especificado
        if sources is None:
            sources = [web_source(), x_source()]

        # Cria parâmetros de busca
        search_params = SearchParameters(
            mode=self.search_mode,
            max_search_results=self.max_results,
            return_citations=self.return_citations,
            sources=sources,
            **kwargs
        )

        # Adiciona filtros de data se fornecidos
        if from_date:
            search_params.from_date = from_date
        if to_date:
            search_params.to_date = to_date

        # Cria chat e realiza busca
        chat = self.client.chat.create(
            model=self.model,
            search_parameters=search_params
        )

        chat.append(user(query))
        response = chat.sample()

        return {
            'content': response.content,
            'citations': response.citations if hasattr(response, 'citations') else [],
            'num_sources_used': response.usage.num_sources_used if hasattr(response.usage, 'num_sources_used') else 0
        }

    def search_web_only(self, query: str, **kwargs):
        """
        Busca apenas na web

        Args:
            query: Pergunta ou busca a ser realizada
            **kwargs: Parâmetros adicionais

        Returns:
            dict: Resultado da busca
        """
        return self.search(query, sources=[web_source()], **kwargs)

    def search_x_only(self, query: str, **kwargs):
        """
        Busca apenas no Twitter/X

        Args:
            query: Pergunta ou busca a ser realizada
            **kwargs: Parâmetros adicionais

        Returns:
            dict: Resultado da busca
        """
        return self.search(query, sources=[x_source()], **kwargs)

    def search_with_handles(
        self,
        query: str,
        included_handles: list = None,
        excluded_handles: list = None,
        **kwargs
    ):
        """
        Busca no Twitter/X com filtros de handles

        Args:
            query: Pergunta ou busca a ser realizada
            included_handles: Lista de handles para incluir (max 10)
            excluded_handles: Lista de handles para excluir (max 10)
            **kwargs: Parâmetros adicionais

        Returns:
            dict: Resultado da busca
        """
        x_src = x_source()
        if included_handles:
            x_src['included_x_handles'] = included_handles
        if excluded_handles:
            x_src['excluded_x_handles'] = excluded_handles

        return self.search(query, sources=[x_src], **kwargs)


def main():
    """Função principal para uso via linha de comando"""
    if len(sys.argv) < 2:
        print("Uso: python3.11 xai_search.py 'sua pergunta aqui'")
        print("\nExemplos:")
        print("  python3.11 xai_search.py 'Quais são as últimas notícias sobre IA?'")
        print("  python3.11 xai_search.py 'O que as pessoas estão falando sobre xAI no Twitter?'")
        sys.exit(1)

    query = ' '.join(sys.argv[1:])

    print(f"\n🔍 Buscando: {query}\n")
    print(f"Modelo: {DEFAULT_MODEL}")
    print(f"Máximo de fontes: {DEFAULT_MAX_SEARCH_RESULTS}\n")
    print("=" * 80)

    # Cria instância e realiza busca
    searcher = XAISearch()
    result = searcher.search(query)

    # Exibe resultado
    print(f"\n📝 Resposta:\n")
    print(result['content'])

    # Exibe citações
    if result['citations']:
        print(f"\n\n📚 Fontes utilizadas ({result['num_sources_used']}):\n")
        for i, citation in enumerate(result['citations'], 1):
            print(f"{i}. {citation}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
