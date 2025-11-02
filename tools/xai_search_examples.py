#!/usr/bin/env python3.11
"""
Exemplos de uso da API xAI Live Search

Este script demonstra diferentes formas de usar a busca xAI
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from xai_search import XAISearch
from xai_sdk.search import web_source, x_source, news_source


def exemplo_basico():
    """Exemplo de busca básica"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Busca básica na web e Twitter/X")
    print("=" * 80 + "\n")

    searcher = XAISearch()
    result = searcher.search("Quais são as últimas tendências em IA generativa?")

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")
    if result['citations']:
        print("\nCitações:")
        for i, url in enumerate(result['citations'], 1):
            print(f"  {i}. {url}")


def exemplo_web_apenas():
    """Exemplo de busca apenas na web"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Busca apenas na web")
    print("=" * 80 + "\n")

    searcher = XAISearch()
    result = searcher.search_web_only("Melhores práticas de Python 2025")

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def exemplo_twitter_apenas():
    """Exemplo de busca apenas no Twitter/X"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Busca apenas no Twitter/X")
    print("=" * 80 + "\n")

    searcher = XAISearch()
    result = searcher.search_x_only("O que as pessoas estão dizendo sobre xAI?")

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def exemplo_com_handles():
    """Exemplo de busca filtrando por handles específicos"""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: Busca no Twitter/X de handles específicos")
    print("=" * 80 + "\n")

    searcher = XAISearch()
    result = searcher.search_with_handles(
        "Últimas atualizações da empresa",
        included_handles=["xai", "elonmusk"]
    )

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def exemplo_com_datas():
    """Exemplo de busca com filtro de datas"""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: Busca com filtro de período")
    print("=" * 80 + "\n")

    searcher = XAISearch()
    result = searcher.search(
        "Principais eventos de tecnologia",
        from_date=datetime(2025, 10, 1),
        to_date=datetime(2025, 10, 31)
    )

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def exemplo_customizado():
    """Exemplo de busca com configurações customizadas"""
    print("\n" + "=" * 80)
    print("EXEMPLO 6: Busca com mais resultados e configurações customizadas")
    print("=" * 80 + "\n")

    # Cria searcher com configurações personalizadas
    searcher = XAISearch(
        max_results=10,  # Mais resultados
        search_mode="on"  # Força a busca sempre
    )

    result = searcher.search("Análise do mercado de criptomoedas em 2025")

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def exemplo_posts_populares():
    """Exemplo de busca por posts populares no Twitter/X"""
    print("\n" + "=" * 80)
    print("EXEMPLO 7: Busca por posts populares no Twitter/X")
    print("=" * 80 + "\n")

    searcher = XAISearch()

    # Busca com filtro de popularidade
    x_src = x_source(
        post_favorite_count=1000,  # Mínimo 1000 curtidas
        post_view_count=10000      # Mínimo 10000 visualizações
    )

    result = searcher.search(
        "Memes virais recentes",
        sources=[x_src]
    )

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def exemplo_news():
    """Exemplo de busca em notícias"""
    print("\n" + "=" * 80)
    print("EXEMPLO 8: Busca em fontes de notícias")
    print("=" * 80 + "\n")

    searcher = XAISearch()

    result = searcher.search(
        "Últimas notícias sobre inteligência artificial",
        sources=[news_source(), web_source()]
    )

    print("Resposta:", result['content'])
    print(f"\nFontes usadas: {result['num_sources_used']}")


def menu():
    """Menu interativo de exemplos"""
    exemplos = {
        '1': ('Busca básica na web e Twitter/X', exemplo_basico),
        '2': ('Busca apenas na web', exemplo_web_apenas),
        '3': ('Busca apenas no Twitter/X', exemplo_twitter_apenas),
        '4': ('Busca com handles específicos', exemplo_com_handles),
        '5': ('Busca com filtro de período', exemplo_com_datas),
        '6': ('Busca com configurações customizadas', exemplo_customizado),
        '7': ('Busca por posts populares', exemplo_posts_populares),
        '8': ('Busca em notícias', exemplo_news),
        '0': ('Executar todos os exemplos', None)
    }

    print("\n" + "=" * 80)
    print("EXEMPLOS DE USO DA API xAI LIVE SEARCH")
    print("=" * 80)
    print("\nEscolha um exemplo para executar:\n")

    for num, (descricao, _) in exemplos.items():
        if num != '0':
            print(f"  {num}. {descricao}")

    print(f"\n  0. Executar todos os exemplos")
    print("  q. Sair\n")

    escolha = input("Digite sua escolha: ").strip()

    if escolha.lower() == 'q':
        print("\nSaindo...\n")
        return

    if escolha == '0':
        for num in sorted(exemplos.keys()):
            if num != '0' and exemplos[num][1]:
                try:
                    exemplos[num][1]()
                    input("\nPressione Enter para continuar...")
                except Exception as e:
                    print(f"\n❌ Erro: {e}")
                    input("\nPressione Enter para continuar...")
    elif escolha in exemplos and exemplos[escolha][1]:
        try:
            exemplos[escolha][1]()
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    else:
        print("\n❌ Opção inválida!\n")

    input("\nPressione Enter para voltar ao menu...")
    menu()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.\n")
        sys.exit(0)
