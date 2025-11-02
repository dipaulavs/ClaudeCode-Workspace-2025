#!/usr/bin/env python3
"""
Apify Web Scraper - Batch (Múltiplas URLs)

Permite fazer scraping de múltiplas URLs em sequência, salvando cada uma
em sua própria pasta organizada.

Uso:
    python3 tools/apify_scraper_batch.py "URL1" "URL2" "URL3" ...
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from apify_scraper import ApifyScraper


def main():
    """Função principal para scraping em batch"""
    if len(sys.argv) < 2:
        print("Uso: python3 tools/apify_scraper_batch.py 'URL1' 'URL2' 'URL3' ...")
        print("\nExemplos:")
        print("  python3 tools/apify_scraper_batch.py 'https://docs.site1.com' 'https://docs.site2.com'")
        sys.exit(1)

    urls = sys.argv[1:]

    # Valida URLs
    for url in urls:
        if not url.startswith(('http://', 'https://')):
            print(f"❌ Erro: URL inválida '{url}' - deve começar com http:// ou https://")
            sys.exit(1)

    print("=" * 80)
    print("🌐 APIFY WEB SCRAPER - BATCH MODE")
    print("=" * 80)
    print(f"\n📋 Total de URLs para processar: {len(urls)}\n")

    for idx, url in enumerate(urls, 1):
        print(f"   {idx}. {url}")

    print(f"\n{'=' * 80}")

    # Inicializa scraper
    scraper = ApifyScraper()

    # Processa cada URL
    results_summary = []
    start_time = datetime.now()

    for idx, url in enumerate(urls, 1):
        print(f"\n\n{'#' * 80}")
        print(f"# URL {idx}/{len(urls)}")
        print(f"{'#' * 80}\n")

        try:
            # Preview
            preview = scraper.preview_scrape(url, max_preview_pages=50)

            if not preview["success"]:
                print(f"❌ Erro no preview: {preview['error']}")
                results_summary.append({
                    "url": url,
                    "success": False,
                    "error": preview['error']
                })
                continue

            num_pages = preview["num_pages"]
            print(f"📊 Páginas encontradas: {num_pages}")

            # Scraping completo
            print(f"\n🚀 Iniciando scraping...")
            results = scraper.scrape(url)

            if results["success"]:
                # Salva resultados
                output_path = scraper.save_results(url, results)
                results_summary.append({
                    "url": url,
                    "success": True,
                    "pages": results["num_pages"],
                    "output_path": output_path
                })
                print(f"✅ Concluído! ({results['num_pages']} páginas)")
            else:
                print(f"❌ Erro no scraping: {results['error']}")
                results_summary.append({
                    "url": url,
                    "success": False,
                    "error": results['error']
                })

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido pelo usuário. Salvando progresso até aqui...")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")
            results_summary.append({
                "url": url,
                "success": False,
                "error": str(e)
            })

    # Resumo final
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n\n{'=' * 80}")
    print("📊 RESUMO FINAL")
    print("=" * 80)
    print(f"\n⏱️  Tempo total: {duration:.1f} segundos")
    print(f"📋 URLs processadas: {len(results_summary)}/{len(urls)}\n")

    successful = [r for r in results_summary if r["success"]]
    failed = [r for r in results_summary if not r["success"]]

    print(f"✅ Sucessos: {len(successful)}")
    for result in successful:
        print(f"   • {result['url']} ({result['pages']} páginas)")
        print(f"     └─ {result['output_path']}")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for result in failed:
            print(f"   • {result['url']}")
            print(f"     └─ Erro: {result['error']}")

    print("\n" + "=" * 80)

    if failed:
        print(f"⚠️  Atenção: {len(failed)} URL(s) falharam")
    else:
        print("✅ Todas as URLs foram processadas com sucesso!")

    print("=" * 80)


if __name__ == "__main__":
    main()
