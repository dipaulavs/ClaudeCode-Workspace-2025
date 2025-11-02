#!/usr/bin/env python3
"""
Template: Gerar Imagem com DALL-E 3

Wrapper simplificado para gerar imagens usando DALL-E 3 via OpenAI API.
Suporta múltiplos tamanhos e qualidades.

Uso:
    python3 scripts/image-generation/generate_dalle3.py "seu prompt aqui"
    python3 scripts/image-generation/generate_dalle3.py "logo empresa" --size 1024x1024
    python3 scripts/image-generation/generate_dalle3.py "arte premium" --quality hd
"""

import sys
import argparse
from pathlib import Path

# Adiciona o diretório tools ao path para importar as ferramentas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from generate_image_ai import AIImageGenerator


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gerar imagem com DALL-E 3 (OpenAI)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python3 scripts/image-generation/generate_dalle3.py "gato astronauta"
    python3 scripts/image-generation/generate_dalle3.py "paisagem" --size 1792x1024
    python3 scripts/image-generation/generate_dalle3.py "retrato" --size 1024x1792
    python3 scripts/image-generation/generate_dalle3.py "arte premium" --quality hd

Características:
    - Modelo: DALL-E 3
    - Tamanhos: 1024x1024, 1792x1024 (landscape), 1024x1792 (portrait)
    - Qualidade: standard ou hd
    - Salvamento automático em ~/Downloads
    - Prompt revisado automaticamente pela API
        """
    )

    parser.add_argument('prompt', help='Descrição da imagem a ser gerada')
    parser.add_argument('--size', '-s', default='1024x1024',
                        choices=['1024x1024', '1792x1024', '1024x1792'],
                        help='Tamanho da imagem. Padrão: 1024x1024')
    parser.add_argument('--quality', '-q', default='standard',
                        choices=['standard', 'hd'],
                        help='Qualidade da imagem (standard ou hd). Padrão: standard')

    args = parser.parse_args()

    print("🎨 DALL-E 3 Image Generation")
    print("=" * 60)

    try:
        # Cria o gerador
        generator = AIImageGenerator()

        # Gera a imagem
        filepath = generator.generate_image(
            prompt=args.prompt,
            size=args.size,
            quality=args.quality
        )

        if filepath:
            print(f"\n✅ Concluído com sucesso!")
            print(f"📂 Arquivo: {filepath}")
            return 0
        else:
            print("❌ Falha ao gerar imagem")
            return 1

    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
