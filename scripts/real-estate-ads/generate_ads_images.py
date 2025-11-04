#!/usr/bin/env python3
"""
Template: Gerar Criativos de Anúncios de Imóveis

Wrapper simplificado para gerar imagens de anúncios de imóveis usando Nano Banana Edit.
Aceita URL da foto do imóvel e prompts com hooks persuasivos.

Uso:
    # Gerar 4 variações com hooks diferentes
    python3 scripts/real-estate-ads/generate_ads_images.py \\
      --image-url "https://exemplo.com/imovel.jpg" \\
      "Hook 1: Casa dos sonhos..." \\
      "Hook 2: Localização privilegiada..." \\
      "Hook 3: Investimento certeiro..." \\
      "Hook 4: Oportunidade única..."

    # Gerar para Stories (9:16)
    python3 scripts/real-estate-ads/generate_ads_images.py \\
      --image-url "https://exemplo.com/imovel.jpg" \\
      --size 9:16 \\
      "Hook 1..." "Hook 2..."
"""

import sys
import argparse
import subprocess
from pathlib import Path

# Path do script low-level
BATCH_SCRIPT = str(Path(__file__).resolve().parent.parent.parent / "tools" / "batch_edit_ads_portrait.py")


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gerar criativos de anúncios de imóveis (Instagram Feed 4:5)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    # Gerar 4 criativos com hooks diferentes (Feed 4:5)
    python3 scripts/real-estate-ads/generate_ads_images.py \\
      --image-url "https://media.loop9.com.br/s/ABC123/imovel.jpg" \\
      "Casa com 3 quartos, piscina e área gourmet. OPORTUNIDADE ÚNICA!" \\
      "Localização privilegiada! Próximo a tudo que você precisa." \\
      "Investimento certeiro: chácara com potencial de valorização." \\
      "Não perca! Casa dos sonhos com preço especial."

    # Stories (9:16)
    python3 scripts/real-estate-ads/generate_ads_images.py \\
      --image-url "https://exemplo.com/imovel.jpg" \\
      --size 9:16 \\
      "Hook 1..." "Hook 2..."

    # Formato JPEG
    python3 scripts/real-estate-ads/generate_ads_images.py \\
      --image-url "https://exemplo.com/imovel.jpg" \\
      --format JPEG \\
      "Hook 1..." "Hook 2..."

Características:
    - Modelo: Gemini 2.5 Flash (Nano Banana Edit)
    - Aspect ratio padrão: 4:5 (Instagram Feed)
    - Formato padrão: PNG
    - Processamento paralelo: todos criativos ao mesmo tempo
    - Tempo médio: ~90s para 4 criativos
    - Salvamento automático: ~/Downloads
        """
    )

    parser.add_argument('--image-url', '-u', required=True,
                        help='URL pública da foto do imóvel (obrigatório)')
    parser.add_argument('--format', '-f', default='PNG', choices=['PNG', 'JPEG'],
                        help='Formato da imagem de saída. Padrão: PNG')
    parser.add_argument('--size', '-s', default='4:5',
                        choices=['4:5', '9:16'],
                        help='Proporção: 4:5 (Feed) ou 9:16 (Stories). Padrão: 4:5')
    parser.add_argument('prompts', nargs='+',
                        help='Prompts com hooks persuasivos (um por criativo)')

    args = parser.parse_args()

    print("🏠 Gerador de Criativos para Anúncios de Imóveis")
    print("=" * 60)

    try:
        # Chama o script batch
        cmd = [
            "python3", BATCH_SCRIPT,
            "--image-url", args.image_url,
            "--format", args.format,
            "--size", args.size
        ] + args.prompts

        result = subprocess.run(cmd, check=True)
        return result.returncode

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao gerar criativos: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
