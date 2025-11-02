#!/usr/bin/env python3
"""
Orshot - Geração com Templates Studio (Customizados)

Gera imagens usando templates customizados criados no Orshot Studio.
Templates Studio usam endpoint diferente dos pré-prontos.

Uso:
    # Com JSON de modificações
    python3 scripts/orshot/generate_studio.py --template 1337 --data '{"headline":"Texto","calendarDay1":"10"}'

    # Com arquivo JSON
    python3 scripts/orshot/generate_studio.py --template 1337 --data-file modifications.json

    # Especificar output
    python3 scripts/orshot/generate_studio.py --template 1337 --data '{"headline":"Test"}' --output result.png
"""

import sys
import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict
from io import BytesIO
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import requests
    from PIL import Image
except ImportError as e:
    print(f"❌ Erro: Biblioteca necessária não encontrada.")
    print(f"   Instale com: pip install requests pillow")
    sys.exit(1)

load_dotenv()


def generate_studio_image(
    template_id: int,
    modifications: Dict[str, Any],
    response_format: str = 'png',
    scale: int = 1,
    output_path: str = None,
    use_downloads: bool = True
) -> Dict[str, Any]:
    """
    Gera imagem usando template Studio do Orshot

    Args:
        template_id: ID do template Studio (número)
        modifications: Dict com parâmetros do template
        response_format: Formato (png, jpg, webp, pdf)
        scale: Escala da imagem (1, 2, 3)
        output_path: Caminho de saída (None = auto Downloads)
        use_downloads: Salvar em Downloads por padrão (True)

    Returns:
        Dict com resultado
    """

    # Valida API key
    api_key = os.getenv('ORSHOT_API_KEY')
    if not api_key:
        raise ValueError(
            "ORSHOT_API_KEY não encontrada no .env\n"
            "Adicione: ORSHOT_API_KEY=os-XXXXXXXXXXXXXXXX"
        )

    print(f"🎨 Gerando imagem com Orshot Studio...")
    print(f"   Template ID: {template_id}")
    print(f"   Formato: {response_format}")
    print(f"   Escala: {scale}x")
    print(f"   Modificações: {len(modifications)} parâmetros")

    # Request para API Studio
    response = requests.post(
        'https://api.orshot.com/v1/studio/render',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json={
            'templateId': template_id,
            'modifications': modifications,
            'response': {
                'type': 'binary',
                'format': response_format,
                'scale': scale
            }
        }
    )

    # Verifica erro
    if response.status_code != 200:
        raise Exception(
            f"API Error {response.status_code}: {response.text}\n"
            f"Verifique se o template {template_id} existe e os parâmetros estão corretos"
        )

    # Define nome do arquivo
    if not output_path:
        title = modifications.get('headline', modifications.get('title', 'output'))
        title_clean = title[:20].replace(' ', '_').replace('/', '_')
        filename = f"orshot_studio_{template_id}_{title_clean}.{response_format}"

        # Salva em Downloads por padrão
        if use_downloads:
            downloads_dir = Path.home() / "Downloads"
            output_path = str(downloads_dir / filename)
        else:
            output_path = filename

    # Salva imagem
    with Image.open(BytesIO(response.content)) as im:
        im.save(output_path)

    file_size = Path(output_path).stat().st_size
    file_size_kb = file_size / 1024

    result = {
        'status': 'success',
        'template_id': template_id,
        'template_type': 'studio',
        'output_path': output_path,
        'format': response_format,
        'size_kb': round(file_size_kb, 2),
        'modifications': modifications
    }

    print(f"✅ Imagem gerada com sucesso!")
    print(f"   Arquivo: {output_path}")
    print(f"   Tamanho: {file_size_kb:.2f} KB")

    return result


def main():
    """Função principal"""

    parser = argparse.ArgumentParser(
        description='Gera imagem usando template Studio customizado do Orshot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:

    # Template 1337 (Save the Date)
    python3 scripts/orshot/generate_studio.py \\
        --template 1337 \\
        --data '{
            "headline": "EVENTO 2025",
            "comingSoon": "Em Breve",
            "calendarDay1": "15",
            "calendarDay2": "16",
            "calendarDay3": "22",
            "calendarDay4": "23",
            "canvasBackgroundColor": "#1a1a2e",
            "description": "Prepare-se para o maior evento do ano",
            "megaphoneImage": "https://example.com/image.jpg"
        }'

    # Com arquivo JSON
    python3 scripts/orshot/generate_studio.py \\
        --template 1337 \\
        --data-file modifications.json \\
        --output evento.png

    # Formato WebP com escala 2x
    python3 scripts/orshot/generate_studio.py \\
        --template 1337 \\
        --data '{"headline":"TEST"}' \\
        --format webp \\
        --scale 2

Encontrar Template ID:
    1. Acesse: https://orshot.com/studio
    2. Abra seu template
    3. Copie o Template ID (número)
        """
    )

    # Template
    parser.add_argument(
        '--template', '-t',
        required=True,
        type=int,
        help='Template ID do Studio (número, ex: 1337)'
    )

    # Modificações
    parser.add_argument(
        '--data', '-d',
        help='JSON com modificações (ex: \'{"headline":"Texto"}\')'
    )

    parser.add_argument(
        '--data-file',
        help='Arquivo JSON com modificações'
    )

    # Configurações
    parser.add_argument(
        '--format', '-f',
        default='png',
        choices=['png', 'jpg', 'jpeg', 'webp', 'pdf'],
        help='Formato da imagem (padrão: png)'
    )

    parser.add_argument(
        '--scale', '-s',
        type=int,
        default=1,
        choices=[1, 2, 3],
        help='Escala da imagem (1x, 2x, 3x) - padrão: 1'
    )

    parser.add_argument(
        '--output', '-o',
        help='Caminho do arquivo de saída (padrão: ~/Downloads/)'
    )

    parser.add_argument(
        '--no-downloads',
        action='store_true',
        help='Não salvar em Downloads (salva na pasta atual)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verbose'
    )

    args = parser.parse_args()

    # Carrega modifications
    if args.data_file:
        try:
            with open(args.data_file, 'r', encoding='utf-8') as f:
                modifications = json.load(f)
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo não encontrado: {args.data_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            sys.exit(1)
    elif args.data:
        try:
            modifications = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            sys.exit(1)
    else:
        print("❌ Erro: Especifique --data OU --data-file")
        print("   Exemplos:")
        print("     --data '{\"headline\":\"Texto\"}'")
        print("     --data-file modifications.json")
        sys.exit(1)

    if args.verbose:
        print(f"🔧 Modo verbose ativado")
        print(f"   Template ID: {args.template}")
        print(f"   Modifications:")
        print(json.dumps(modifications, indent=4, ensure_ascii=False))
        print(f"   Formato: {args.format}")
        print(f"   Escala: {args.scale}x")

    try:
        result = generate_studio_image(
            template_id=args.template,
            modifications=modifications,
            response_format=args.format,
            scale=args.scale,
            output_path=args.output,
            use_downloads=not args.no_downloads
        )

        if args.verbose:
            print(f"\n📊 Resultado completo:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
