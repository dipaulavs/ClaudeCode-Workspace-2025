#!/usr/bin/env python3
"""
🎬 TEMPLATE: Geração de Vídeo Único com Sora 2

Gera um único vídeo usando Sora 2 (OpenAI) via API Kie.ai
Vídeos são salvos automaticamente em ~/Downloads/

Uso:
    python3 scripts/video-generation/generate_sora.py "seu prompt aqui"
    python3 scripts/video-generation/generate_sora.py "paisagem" --aspect landscape
    python3 scripts/video-generation/generate_sora.py "cidade" --aspect square

Argumentos:
    prompt (str): Descrição do vídeo a ser gerado
    --aspect (str): Proporção do vídeo (portrait, landscape, square). Padrão: portrait
    --watermark: Mantém a marca d'água (padrão: remove)

Retorna:
    Vídeo salvo em ~/Downloads/ no formato: sora_video_YYYYMMDD_HHMMSS.mp4
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar ferramentas
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.generate_video_sora import generate_video, wait_for_completion, download_video

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")


def main():
    """Executa geração de vídeo único"""
    if len(sys.argv) < 2:
        print("🎬 Gerador de Vídeo - Sora 2 (OpenAI)")
        print("\nUso:")
        print('  python3 scripts/video-generation/generate_sora.py "seu prompt aqui"')
        print("\nOpções:")
        print("  --aspect RATIO  Proporção do vídeo (landscape, portrait, square). Padrão: portrait")
        print("  --watermark     Mantém a marca d'água (padrão: remove)")
        print("\nExemplos:")
        print('  python3 scripts/video-generation/generate_sora.py "Gato brincando com novelo"')
        print('  python3 scripts/video-generation/generate_sora.py "Paisagem montanha" --aspect landscape')
        print('  python3 scripts/video-generation/generate_sora.py "Cidade futurista" --aspect square')
        print(f"\n📂 Vídeos salvos em: {DOWNLOADS_PATH}")
        print("⚠️  Geração pode levar 2-5 minutos")
        sys.exit(1)

    # Parse dos argumentos
    prompt = sys.argv[1]
    aspect_ratio = "portrait"
    remove_watermark = True

    if "--aspect" in sys.argv:
        idx = sys.argv.index("--aspect")
        if idx + 1 < len(sys.argv):
            ratio = sys.argv[idx + 1].lower()
            if ratio in ["landscape", "portrait", "square"]:
                aspect_ratio = ratio
            else:
                print("⚠️  Proporção inválida. Usando portrait.")

    if "--watermark" in sys.argv:
        remove_watermark = False

    # Gera o vídeo
    task_id = generate_video(prompt, aspect_ratio=aspect_ratio, remove_watermark=remove_watermark)

    if not task_id:
        print("❌ Falha ao criar tarefa de geração")
        sys.exit(1)

    # Aguarda conclusão
    video_urls = wait_for_completion(task_id, max_wait=600)

    if not video_urls:
        print("❌ Falha na geração ou timeout")
        sys.exit(1)

    # Baixa os vídeos
    from datetime import datetime

    print(f"\n🎬 {len(video_urls)} vídeo(s) gerado(s):")
    for i, url in enumerate(video_urls, 1):
        print(f"\n{i}. {url}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if len(video_urls) > 1:
            output_path = os.path.join(DOWNLOADS_PATH, f"sora_video_{timestamp}_v{i}.mp4")
        else:
            output_path = os.path.join(DOWNLOADS_PATH, f"sora_video_{timestamp}.mp4")

        download_video(url, output_path)

    print("\n✨ Concluído!")
    print(f"📂 Verifique seu(s) vídeo(s) em: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
