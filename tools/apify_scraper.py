#!/usr/bin/env python3
"""
Apify Web Scraper - Extração de conteúdo de websites

Este script usa o Apify para fazer scraping de websites e salvar o conteúdo
em formato Markdown. Segue links de referência automaticamente e mostra
preview antes de executar.

Uso:
    python3 tools/apify_scraper.py "https://example.com/docs"
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Adiciona o diretório pai ao path para importar a config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from apify_client import ApifyClient
except ImportError:
    print("❌ Erro: apify-client não está instalado")
    print("Execute: pip3 install apify-client")
    sys.exit(1)

from config.apify_config import (
    APIFY_API_TOKEN,
    APIFY_ACTOR_ID,
    DEFAULT_CRAWLER_CONFIG,
    PREVIEW_MAX_PAGES
)


class ApifyScraper:
    """Classe para realizar scraping de websites usando Apify"""

    def __init__(self, api_token: str = APIFY_API_TOKEN):
        """
        Inicializa o cliente Apify

        Args:
            api_token: Token da API do Apify
        """
        self.client = ApifyClient(api_token)
        self.actor_id = APIFY_ACTOR_ID

    def _get_domain_name(self, url: str) -> str:
        """
        Extrai nome do domínio da URL para nomenclatura

        Args:
            url: URL completa

        Returns:
            Nome do domínio simplificado
        """
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        # Remove TLD e usa apenas o nome principal
        domain_parts = domain.split('.')
        if len(domain_parts) > 1:
            return domain_parts[0]
        return domain

    def preview_scrape(self, url: str, max_preview_pages: int = 50) -> dict:
        """
        Executa preview do scraping para contar páginas

        Args:
            url: URL inicial para scraping
            max_preview_pages: Limite de páginas para preview

        Returns:
            dict com informações do preview
        """
        print(f"\n🔍 Analisando site: {url}")
        print(f"⏳ Executando preview (máx. {max_preview_pages} páginas)...\n")

        # Configuração para preview (limitado)
        preview_config = DEFAULT_CRAWLER_CONFIG.copy()
        preview_config["startUrls"] = [{"url": url, "method": "GET"}]
        preview_config["maxCrawlPages"] = max_preview_pages
        preview_config["maxCrawlDepth"] = 3  # Profundidade reduzida no preview

        try:
            # Executa preview
            run = self.client.actor(self.actor_id).call(run_input=preview_config)

            # Busca resultados
            dataset_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

            num_pages = len(dataset_items)
            urls_found = [item.get('url', 'N/A') for item in dataset_items[:10]]  # Primeiras 10 URLs

            return {
                "success": True,
                "num_pages": num_pages,
                "reached_limit": num_pages >= max_preview_pages,
                "sample_urls": urls_found,
                "run_id": run["id"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def scrape(self, url: str, max_pages: int = None, max_depth: int = None) -> dict:
        """
        Executa scraping completo do site

        Args:
            url: URL inicial para scraping
            max_pages: Limite máximo de páginas (None = ilimitado)
            max_depth: Profundidade máxima de crawl (None = usa padrão)

        Returns:
            dict com resultados do scraping
        """
        print(f"\n🚀 Iniciando scraping completo...")
        print(f"📄 URL: {url}")
        if max_pages:
            print(f"📊 Limite: {max_pages} páginas")
        print()

        # Configuração para scraping completo
        scrape_config = DEFAULT_CRAWLER_CONFIG.copy()
        scrape_config["startUrls"] = [{"url": url, "method": "GET"}]

        if max_pages:
            scrape_config["maxCrawlPages"] = max_pages
        if max_depth:
            scrape_config["maxCrawlDepth"] = max_depth

        try:
            # Executa scraping
            run = self.client.actor(self.actor_id).call(run_input=scrape_config)

            print(f"✅ Scraping concluído!")
            print(f"🆔 Run ID: {run['id']}\n")

            # Busca todos os resultados
            print("📥 Baixando resultados...\n")
            dataset_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

            return {
                "success": True,
                "run_id": run["id"],
                "dataset_id": run["defaultDatasetId"],
                "num_pages": len(dataset_items),
                "items": dataset_items
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def save_results(self, url: str, results: dict) -> str:
        """
        Salva resultados em arquivos Markdown

        Args:
            url: URL original do scraping
            results: Resultados do scraping

        Returns:
            Caminho da pasta criada
        """
        if not results["success"]:
            print(f"❌ Erro: {results['error']}")
            return None

        # Cria pasta de destino
        domain_name = self._get_domain_name(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"apify_scrape_{domain_name}_{timestamp}"
        output_dir = Path.home() / "Downloads" / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"💾 Salvando resultados em: {output_dir}\n")

        items = results["items"]
        metadata = []
        full_content = []

        # Processa cada página
        for idx, item in enumerate(items, 1):
            page_url = item.get('url', 'N/A')
            page_title = item.get('metadata', {}).get('title', 'Sem título')
            markdown_content = item.get('markdown', '')

            # Salva página individual
            page_filename = f"page_{idx:03d}.md"
            page_path = output_dir / page_filename

            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(f"# {page_title}\n\n")
                f.write(f"**URL:** {page_url}\n\n")
                f.write("---\n\n")
                f.write(markdown_content)

            # Adiciona ao metadata
            metadata.append({
                "page_number": idx,
                "filename": page_filename,
                "title": page_title,
                "url": page_url,
                "content_length": len(markdown_content)
            })

            # Adiciona ao conteúdo completo
            full_content.append(f"# Página {idx}: {page_title}\n")
            full_content.append(f"**URL:** {page_url}\n\n")
            full_content.append(markdown_content)
            full_content.append("\n\n---\n\n")

            # Exibe progresso
            if idx % 10 == 0 or idx == len(items):
                print(f"  ✓ Salvou {idx}/{len(items)} páginas")

        # Salva metadata
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                "source_url": url,
                "scrape_date": datetime.now().isoformat(),
                "total_pages": len(items),
                "run_id": results["run_id"],
                "dataset_id": results["dataset_id"],
                "pages": metadata
            }, f, indent=2, ensure_ascii=False)

        # Salva conteúdo completo
        full_content_path = output_dir / "full_content.md"
        with open(full_content_path, 'w', encoding='utf-8') as f:
            f.write(f"# Scraping Completo: {domain_name}\n\n")
            f.write(f"**URL Original:** {url}\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"**Total de Páginas:** {len(items)}\n\n")
            f.write("---\n\n")
            f.write("\n".join(full_content))

        print(f"\n✅ Resultados salvos com sucesso!")
        print(f"📁 Pasta: {output_dir}")
        print(f"📄 Páginas individuais: {len(items)} arquivos")
        print(f"📋 Metadata: metadata.json")
        print(f"📚 Conteúdo completo: full_content.md\n")

        return str(output_dir)


def main():
    """Função principal para uso via linha de comando"""
    if len(sys.argv) < 2:
        print("Uso: python3 tools/apify_scraper.py 'URL'")
        print("\nExemplos:")
        print("  python3 tools/apify_scraper.py 'https://docs.example.com'")
        print("  python3 tools/apify_scraper.py 'https://doc.evolution-api.com/v2/api-reference/'")
        sys.exit(1)

    url = sys.argv[1]

    # Valida URL
    if not url.startswith(('http://', 'https://')):
        print("❌ Erro: URL deve começar com http:// ou https://")
        sys.exit(1)

    print("=" * 80)
    print("🌐 APIFY WEB SCRAPER")
    print("=" * 80)

    # Inicializa scraper
    scraper = ApifyScraper()

    # Executa preview
    preview = scraper.preview_scrape(url, max_preview_pages=50)

    if not preview["success"]:
        print(f"❌ Erro no preview: {preview['error']}")
        sys.exit(1)

    # Mostra informações do preview
    num_pages = preview["num_pages"]
    print(f"📊 Páginas encontradas (preview): {num_pages}")

    if preview["reached_limit"]:
        print(f"⚠️  O site pode ter MAIS de {num_pages} páginas (preview limitado)")
        print(f"   O scraping completo pode levar mais tempo e consumir mais recursos.")

    # Mostra algumas URLs encontradas
    print(f"\n📝 Exemplos de páginas que serão extraídas:")
    for idx, sample_url in enumerate(preview["sample_urls"][:5], 1):
        print(f"   {idx}. {sample_url}")

    if len(preview["sample_urls"]) > 5:
        print(f"   ... e mais {num_pages - 5} páginas")

    # Pede confirmação
    print(f"\n{'=' * 80}")
    try:
        response = input(f"Deseja continuar com o scraping completo? (s/n): ").strip().lower()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(0)

    if response != 's':
        print("❌ Operação cancelada.")
        sys.exit(0)

    # Executa scraping completo
    print(f"\n{'=' * 80}")
    results = scraper.scrape(url)

    if results["success"]:
        # Salva resultados
        scraper.save_results(url, results)
        print("=" * 80)
        print("✅ Scraping concluído com sucesso!")
        print("=" * 80)
    else:
        print(f"❌ Erro no scraping: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
