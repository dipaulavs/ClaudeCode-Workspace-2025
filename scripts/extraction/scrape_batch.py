#!/usr/bin/env python3
"""
Template: Web Scraping em Batch (Múltiplas URLs)
Extrai conteúdo de múltiplos sites em sequência via Apify

Uso:
    python3 scripts/extraction/scrape_batch.py "URL1" "URL2" "URL3"
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Adiciona tools/ ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

try:
    from apify_scraper import ApifyScraper
except ImportError:
    print("❌ Erro: Não foi possível importar apify_scraper.py")
    print("Verifique se o arquivo existe em: tools/apify_scraper.py")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 scripts/extraction/scrape_batch.py 'URL1' 'URL2' 'URL3' ...")
        print("\nExemplos:")
        print("  # Scraping de 2 sites")
        print("  python3 scripts/extraction/scrape_batch.py 'https://docs.site1.com' 'https://docs.site2.com'")
        print("\n  # Scraping de múltiplas documentações")
        print("  python3 scripts/extraction/scrape_batch.py \\")
        print("    'https://docs.react.dev' \\")
        print("    'https://docs.python.org/3' \\")
        print("    'https://nodejs.org/docs'")
        print("\nRecursos:")
        print("  • Processa cada URL em sequência")
        print("  • Salva cada site em pasta separada")
        print("  • Preview automático para cada site")
        print("  • Resumo final com estatísticas")
        print("  • Tratamento de erros individual")
        sys.exit(1)

    urls = sys.argv[1:]

    # Valida URLs
    for url in urls:
        if not url.startswith(('http://', 'https://')):
            print(f"❌ Erro: URL inválida '{url}'")
            print("   URLs devem começar com http:// ou https://")
            sys.exit(1)

    print("=" * 80)
    print("🌐 WEB SCRAPING - MODO BATCH")
    print("=" * 80)
    print(f"\n📋 Total de URLs: {len(urls)}\n")

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

            # Scraping completo (sem confirmação no batch)
            print(f"\n🚀 Iniciando scraping automático...")
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
            print("\n\n⚠️  Interrompido pelo usuário.")
            print("   Salvando progresso...")
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
        print(f"⚠️  {len(failed)} URL(s) falharam")
    else:
        print("✅ Todas as URLs processadas com sucesso!")

    print("=" * 80)


if __name__ == "__main__":
    main()
