#!/usr/bin/env python3
"""
Template: Geração em Lote de Imagens

Wrapper simplificado para gerar múltiplas imagens usando diferentes APIs.
Suporta GPT-4o e Nano Banana para geração em lote eficiente.

Uso:
    python3 scripts/image-generation/batch_generate.py "prompt 1" "prompt 2" "prompt 3"
    python3 scripts/image-generation/batch_generate.py --api nanobanana "gato" "cachorro" "pássaro"
    python3 scripts/image-generation/batch_generate.py --api gpt4o "logo A" "logo B" --variants 2
"""

import sys
import argparse
from pathlib import Path

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))


def batch_generate_gpt4o(prompts, n_variants=1):
    """Gera múltiplas imagens usando GPT-4o"""
    from generate_image_batch_gpt import generate_batch

    print(f"🎨 Gerando {len(prompts)} imagens com GPT-4o...")
    print(f"📊 Total de imagens: {len(prompts) * n_variants}")
    print("=" * 60)

    try:
        results = generate_batch(prompts, n_variants=n_variants)

        # Conta sucessos
        success_count = sum(1 for r in results if r['success'])

        print(f"\n✅ Geradas: {success_count}/{len(prompts)} imagens")

        if success_count < len(prompts):
            print(f"⚠️  Falhas: {len(prompts) - success_count}")
            for result in results:
                if not result['success']:
                    print(f"   - {result['prompt']}: {result.get('error', 'Erro desconhecido')}")

        return results

    except Exception as e:
        print(f"❌ Erro na geração em lote: {e}")
        raise


def batch_generate_nanobanana(prompts, output_format='PNG'):
    """Gera múltiplas imagens usando Nano Banana"""
    from generate_image_batch import generate_batch

    print(f"🍌 Gerando {len(prompts)} imagens com Nano Banana...")
    print("=" * 60)

    try:
        results = generate_batch(prompts, output_format=output_format)

        # Conta sucessos
        success_count = sum(1 for r in results if r['success'])

        print(f"\n✅ Geradas: {success_count}/{len(prompts)} imagens")

        if success_count < len(prompts):
            print(f"⚠️  Falhas: {len(prompts) - success_count}")
            for result in results:
                if not result['success']:
                    print(f"   - {result['prompt']}: {result.get('error', 'Erro desconhecido')}")

        return results

    except Exception as e:
        print(f"❌ Erro na geração em lote: {e}")
        raise


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Geração em lote de imagens com IA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    # GPT-4o (padrão)
    python3 scripts/image-generation/batch_generate.py "gato" "cachorro" "pássaro"

    # GPT-4o com múltiplas variações
    python3 scripts/image-generation/batch_generate.py "logo A" "logo B" --variants 2

    # Nano Banana
    python3 scripts/image-generation/batch_generate.py --api nanobanana "arte 1" "arte 2"

    # Nano Banana em JPEG
    python3 scripts/image-generation/batch_generate.py --api nanobanana "foto 1" "foto 2" --format JPEG

Características:
    - Geração paralela eficiente
    - Salvamento automático em ~/Downloads
    - Nomes descritivos em português
    - Suporte a múltiplas APIs
        """
    )

    parser.add_argument('prompts', nargs='+',
                        help='Prompts das imagens a serem geradas (separados por espaço)')
    parser.add_argument('--api', '-a', default='gpt4o', choices=['gpt4o', 'nanobanana'],
                        help='API a ser usada (gpt4o ou nanobanana). Padrão: gpt4o')
    parser.add_argument('--variants', '-v', type=int, default=1,
                        help='Número de variações por prompt (apenas GPT-4o). Padrão: 1')
    parser.add_argument('--format', '-f', default='PNG', choices=['PNG', 'JPEG'],
                        help='Formato da imagem (apenas Nano Banana). Padrão: PNG')

    args = parser.parse_args()

    print("🎨 Geração em Lote de Imagens")
    print("=" * 60)
    print(f"📝 Prompts: {len(args.prompts)}")
    print(f"🔧 API: {args.api.upper()}")

    try:
        if args.api == 'gpt4o':
            results = batch_generate_gpt4o(args.prompts, n_variants=args.variants)
        else:  # nanobanana
            results = batch_generate_nanobanana(args.prompts, output_format=args.format)

        print(f"\n✅ Processo concluído!")
        print(f"📂 Verifique suas imagens em: ~/Downloads")

        return 0

    except Exception as e:
        print(f"❌ Erro ao gerar imagens em lote: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
