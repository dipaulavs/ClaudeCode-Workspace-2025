#!/usr/bin/env python3
"""
Orshot - Geração de Imagem Única

Gera uma imagem usando template do Orshot (pré-pronto ou Studio customizado).

Uso:
    # Usando template pré-pronto
    python3 scripts/orshot/generate_image.py --template open-graph-image-1 --title "Meu Título"

    # Usando template Studio customizado
    python3 scripts/orshot/generate_image.py --template custom-post-123 --data '{"title":"Test","color":"#FF0000"}'

    # Especificar formato e output
    python3 scripts/orshot/generate_image.py --template tweet-1 --title "Hello" --format webp --output result.webp
"""

import sys
import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict
from io import BytesIO
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path para imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import orshot
    from PIL import Image
except ImportError as e:
    print(f"❌ Erro: Biblioteca necessária não encontrada.")
    print(f"   Instale com: pip install orshot pillow")
    sys.exit(1)

# Carrega variáveis de ambiente
load_dotenv()


def generate_image(
    template_id: str,
    modifications: Dict[str, Any],
    response_format: str = 'png',
    output_path: str = None,
    use_downloads: bool = True
) -> Dict[str, Any]:
    """
    Gera imagem usando Orshot API

    Args:
        template_id: ID do template (ex: 'open-graph-image-1')
        modifications: Dict com parâmetros do template
        response_format: Formato da imagem (png, jpg, webp, pdf)
        output_path: Caminho para salvar (None = auto Downloads)
        use_downloads: Salvar em Downloads por padrão (True)

    Returns:
        Dict com resultado da geração
    """

    # Valida API key
    api_key = os.getenv('ORSHOT_API_KEY')
    if not api_key:
        raise ValueError(
            "ORSHOT_API_KEY não encontrada no .env\n"
            "Adicione: ORSHOT_API_KEY=os-XXXXXXXXXXXXXXXX"
        )

    print(f"🎨 Gerando imagem com Orshot...")
    print(f"   Template: {template_id}")
    print(f"   Formato: {response_format}")
    print(f"   Modificações: {modifications}")

    # Inicializa cliente Orshot
    os_client = orshot.Orshot(api_key)

    # Gera imagem (resposta binária)
    response = os_client.render_from_template({
        'template_id': template_id,
        'modifications': modifications,
        'response_type': 'binary',
        'response_format': response_format
    })

    # Define nome do arquivo se não especificado
    if not output_path:
        # Nome do arquivo
        filename = f"orshot_{template_id}_{modifications.get('title', 'output')[:20]}.{response_format}"
        filename = filename.replace(' ', '_').replace('/', '_')

        # Salva em Downloads por padrão
        if use_downloads:
            downloads_dir = Path.home() / "Downloads"
            output_path = str(downloads_dir / filename)
        else:
            output_path = filename

    # Salva imagem
    with Image.open(BytesIO(response.content)) as im:
        im.save(output_path)

    # Informações do arquivo
    file_size = Path(output_path).stat().st_size
    file_size_kb = file_size / 1024

    result = {
        'status': 'success',
        'template_id': template_id,
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
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gera imagem usando Orshot API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    # Template pré-pronto (Open Graph)
    python3 scripts/orshot/generate_image.py \\
        --template open-graph-image-1 \\
        --title "Claude Code: AI Dev Assistant"

    # Template customizado do Studio (JSON)
    python3 scripts/orshot/generate_image.py \\
        --template custom-post-instagram \\
        --data '{"title":"Lançamento!","color":"#FF6B6B","date":"10/Jan"}'

    # Especificar formato e output
    python3 scripts/orshot/generate_image.py \\
        --template tweet-image-1 \\
        --title "Hello World" \\
        --format webp \\
        --output post.webp

Templates comuns:
    - open-graph-image-1: OG image para blogs
    - tweet-image-1: Post estilo Twitter
    - instagram-post-1: Post quadrado Instagram
    - certificate-1: Certificado genérico

    Ver todos: python3 scripts/orshot/list_templates.py
        """
    )

    # Template
    parser.add_argument(
        '--template', '-t',
        required=True,
        help='ID do template (ex: open-graph-image-1 ou ID Studio)'
    )

    # Modificações (2 formas: simples ou JSON completo)
    parser.add_argument(
        '--title',
        help='Título/texto principal (atalho para templates simples)'
    )

    parser.add_argument(
        '--data', '-d',
        help='JSON completo com todas modificações (ex: \'{"title":"Texto","color":"#FF0000"}\')'
    )

    # Configurações
    parser.add_argument(
        '--format', '-f',
        default='png',
        choices=['png', 'jpg', 'jpeg', 'webp', 'pdf'],
        help='Formato da imagem (padrão: png)'
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

    # Prepara modifications
    if args.data:
        # Usa JSON completo
        try:
            modifications = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            sys.exit(1)
    elif args.title:
        # Atalho simples (só título)
        modifications = {'title': args.title}
    else:
        print("❌ Erro: Especifique --title OU --data")
        print("   Exemplos:")
        print("     --title 'Meu Título'")
        print("     --data '{\"title\":\"Título\",\"color\":\"#FF0000\"}'")
        sys.exit(1)

    if args.verbose:
        print(f"🔧 Modo verbose ativado")
        print(f"   Template: {args.template}")
        print(f"   Modifications: {modifications}")
        print(f"   Formato: {args.format}")

    try:
        result = generate_image(
            template_id=args.template,
            modifications=modifications,
            response_format=args.format,
            output_path=args.output,
            use_downloads=not args.no_downloads
        )

        if args.verbose:
            print(f"\n📊 Resultado completo:")
            print(json.dumps(result, indent=2))

        return result

    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
