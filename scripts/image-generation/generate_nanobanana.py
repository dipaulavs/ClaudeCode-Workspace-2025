#!/usr/bin/env python3
"""
Template: Gerar Imagem com Nano Banana (Gemini 2.5 Flash)

Wrapper simplificado para gerar imagens usando Nano Banana via Kie.ai API.
Sempre gera imagens em formato portrait (2:3).

Uso:
    python3 scripts/image-generation/generate_nanobanana.py "seu prompt aqui"
    python3 scripts/image-generation/generate_nanobanana.py "logo minimalista" --format JPEG
"""

import sys
import argparse
from pathlib import Path

# Adiciona o diretório tools ao path para importar as ferramentas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from generate_image_nanobanana import generate_image, wait_for_completion, download_image, create_descriptive_filename
import os


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gerar imagem com Nano Banana (Gemini 2.5 Flash Image Preview)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python3 scripts/image-generation/generate_nanobanana.py "gato astronauta"
    python3 scripts/image-generation/generate_nanobanana.py "logo empresa" --format JPEG
    python3 scripts/image-generation/generate_nanobanana.py "arte abstrata"

Características:
    - Formato: Portrait (2:3)
    - Modelo: Gemini 2.5 Flash (Nano Banana)
    - Salvamento automático em ~/Downloads
    - Nomes de arquivo em português
    - Formatos: PNG (padrão) ou JPEG
        """
    )

    parser.add_argument('prompt', help='Descrição da imagem a ser gerada')
    parser.add_argument('--format', '-f', default='PNG', choices=['PNG', 'JPEG'],
                        help='Formato da imagem (PNG ou JPEG). Padrão: PNG')

    args = parser.parse_args()

    print("🍌 Nano Banana Image Generation (Gemini 2.5 Flash)")
    print("=" * 60)

    try:
        # Gera a imagem
        task_id = generate_image(
            prompt=args.prompt,
            output_format=args.format
        )

        if not task_id:
            print("❌ Falha ao criar tarefa de geração")
            sys.exit(1)

        # Aguarda conclusão
        image_urls = wait_for_completion(task_id)

        if not image_urls:
            print("❌ Falha ao gerar imagem")
            sys.exit(1)

        # Baixa as imagens
        print(f"\n🖼️  {len(image_urls)} imagem(ns) gerada(s)")

        downloads_path = str(Path.home() / "Downloads")
        for i, url in enumerate(image_urls, 1):
            print(f"\n📥 Baixando imagem {i}/{len(image_urls)}...")

            extension = args.format.lower()
            filename = create_descriptive_filename(args.prompt, extension=extension)
            output_path = os.path.join(downloads_path, filename)

            download_image(url, output_path)

        print("\n✅ Concluído com sucesso!")
        print(f"📂 Verifique suas imagens em: ~/Downloads")

        return 0

    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
