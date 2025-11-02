#!/usr/bin/env python3
"""
Template: Gerar Imagem com GPT-4o Image Generation

Wrapper simplificado para gerar imagens usando GPT-4o via Kie.ai API.
Sempre gera imagens em formato portrait (2:3).

Uso:
    python3 scripts/image-generation/generate_gpt4o.py "seu prompt aqui"
    python3 scripts/image-generation/generate_gpt4o.py "astronauta gato" --variants 2
    python3 scripts/image-generation/generate_gpt4o.py "cidade futurista" --enhance
"""

import sys
import argparse
from pathlib import Path

# Adiciona o diretório tools ao path para importar as ferramentas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from generate_image import generate_image, wait_for_completion, download_image


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gerar imagem com GPT-4o Image Generation (Kie.ai)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python3 scripts/image-generation/generate_gpt4o.py "astronauta gato no espaço"
    python3 scripts/image-generation/generate_gpt4o.py "cidade cyberpunk" --variants 2
    python3 scripts/image-generation/generate_gpt4o.py "paisagem montanhosa" --enhance
    python3 scripts/image-generation/generate_gpt4o.py "retrato realista" --variants 4 --enhance

Características:
    - Formato: Portrait (2:3)
    - Salvamento automático em ~/Downloads
    - Nomes de arquivo em português
    - Suporte a múltiplas variações (1, 2 ou 4)
    - Refinamento de prompt opcional
        """
    )

    parser.add_argument('prompt', help='Descrição da imagem a ser gerada')
    parser.add_argument('--variants', '-v', type=int, default=1, choices=[1, 2, 4],
                        help='Número de variações (1, 2 ou 4). Padrão: 1')
    parser.add_argument('--enhance', '-e', action='store_true',
                        help='Ativar refinamento automático do prompt')

    args = parser.parse_args()

    print("🎨 GPT-4o Image Generation")
    print("=" * 60)

    try:
        # Gera a imagem
        task_id = generate_image(
            prompt=args.prompt,
            n_variants=args.variants,
            enhance=args.enhance
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

        # Mostra URLs públicas (podem ser usadas diretamente no WhatsApp)
        print("\n🔗 URLs públicas:")
        for i, url in enumerate(image_urls, 1):
            print(f"   {i}. {url}")

        for i, url in enumerate(image_urls, 1):
            print(f"\n📥 Baixando imagem {i}/{len(image_urls)}...")
            download_image(url, prompt=args.prompt)

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
