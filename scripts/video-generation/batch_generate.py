#!/usr/bin/env python3
"""
🎬 TEMPLATE: Geração de Vídeos em Lote com Sora 2

Gera múltiplos vídeos simultaneamente usando Sora 2 (OpenAI) via API Kie.ai
Todas as tarefas são criadas e processadas em PARALELO para máxima eficiência
Vídeos são salvos automaticamente em ~/Downloads/

Uso:
    python3 scripts/video-generation/batch_generate.py "prompt1" "prompt2" "prompt3"
    python3 scripts/video-generation/batch_generate.py "cena1" "cena2" --aspect landscape

Argumentos:
    prompts (str): Lista de prompts para gerar vídeos (2 ou mais)
    --aspect (str): Proporção dos vídeos (portrait, landscape, square). Padrão: portrait
    --watermark: Mantém a marca d'água (padrão: remove)

Retorna:
    Vídeos salvos em ~/Downloads/ no formato: batch_sora_[prompt]_YYYYMMDD_HHMMSS.mp4

Exemplo:
    python3 scripts/video-generation/batch_generate.py "gato" "cachorro" "pássaro"
    # Gera 3 vídeos em PARALELO (não em fila!)
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar ferramentas
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.generate_video_batch_sora import generate_batch

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")


def main():
    """Executa geração de vídeos em lote"""
    if len(sys.argv) < 2:
        print("🎬 Gerador de Vídeos em Lote - Sora 2 (OpenAI)")
        print("\nUso:")
        print('  python3 scripts/video-generation/batch_generate.py "prompt1" "prompt2" "prompt3"')
        print("\nOpções:")
        print("  --aspect RATIO  Proporção dos vídeos (landscape, portrait, square). Padrão: portrait")
        print("  --watermark     Mantém a marca d'água (padrão: remove)")
        print("\nExemplos:")
        print('  python3 scripts/video-generation/batch_generate.py "Gato brincando" "Cachorro correndo"')
        print('  python3 scripts/video-generation/batch_generate.py "Paisagem 1" "Paisagem 2" --aspect landscape')
        print('  python3 scripts/video-generation/batch_generate.py "Cena 1" "Cena 2" "Cena 3" --aspect square')
        print("\n💡 Vantagens:")
        print("  ✅ Todas as tarefas são criadas e processadas em PARALELO")
        print("  ✅ Muito mais rápido que gerar vídeos individualmente")
        print(f"\n📂 Vídeos salvos em: {DOWNLOADS_PATH}")
        print("⚠️  Geração pode levar 2-5 minutos por vídeo")
        sys.exit(1)

    # Parse dos argumentos
    prompts = []
    aspect_ratio = "portrait"
    remove_watermark = True

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--aspect":
            if i + 1 < len(sys.argv):
                ratio = sys.argv[i + 1].lower()
                if ratio in ["landscape", "portrait", "square"]:
                    aspect_ratio = ratio
                else:
                    print("⚠️  Proporção inválida. Usando portrait.")
                i += 2
            else:
                i += 1
        elif arg == "--watermark":
            remove_watermark = False
            i += 1
        else:
            prompts.append(arg)
            i += 1

    if not prompts:
        print("❌ Erro: Nenhum prompt fornecido")
        print("💡 Forneça pelo menos 1 prompt para gerar vídeo")
        sys.exit(1)

    if len(prompts) == 1:
        print("💡 Apenas 1 prompt fornecido")
        print("   Para vídeo único, use: scripts/video-generation/generate_sora.py")
        print("   Mas vou gerar mesmo assim...\n")

    # Gera os vídeos em lote
    import time

    start_time = time.time()
    results = generate_batch(prompts, aspect_ratio=aspect_ratio, remove_watermark=remove_watermark)
    elapsed = time.time() - start_time

    # Resumo
    print(f"\n{'='*60}")
    print(f"✨ Processamento concluído em {elapsed/60:.1f} minutos ({elapsed:.1f}s)")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    total_size = sum(r.get("size_mb", 0) for r in successful)

    print(f"✅ Sucesso: {len(successful)}/{len(results)} vídeos")
    if successful:
        print(f"📊 Tamanho total: {total_size:.2f} MB\n")
        for r in successful:
            print(f"   📁 {os.path.basename(r['path'])} ({r['size_mb']:.2f} MB)")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
