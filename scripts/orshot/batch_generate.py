#!/usr/bin/env python3
"""
Orshot - Geração em Lote (Batch)

Gera múltiplas imagens de uma vez usando template + dados (JSON/CSV).

Uso:
    # Gerar 50 certificados
    python3 scripts/orshot/batch_generate.py --template certificate-1 --data alunos.json --output certs/

    # Gerar posts Instagram de produtos (CSV)
    python3 scripts/orshot/batch_generate.py --template product-post --data produtos.csv --format webp
"""

import sys
import argparse
import json
import csv
import os
from pathlib import Path
from typing import Any, Dict, List
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import orshot
    from PIL import Image
except ImportError:
    print(f"❌ Erro: Bibliotecas necessárias não encontradas.")
    print(f"   Instale com: pip install orshot pillow")
    sys.exit(1)

# Carrega variáveis de ambiente
load_dotenv()


def load_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Carrega dados de arquivo JSON ou CSV

    Args:
        file_path: Caminho do arquivo (.json ou .csv)

    Returns:
        Lista de dicionários com dados
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # JSON
    if file_path.suffix.lower() == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Se for dict único, converte para lista
            if isinstance(data, dict):
                return [data]
            return data

    # CSV
    elif file_path.suffix.lower() == '.csv':
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    else:
        raise ValueError(f"Formato não suportado: {file_path.suffix}. Use .json ou .csv")


def batch_generate(
    template_id: str,
    data_list: List[Dict[str, Any]],
    response_format: str = 'png',
    output_dir: str = 'orshot_batch',
    max_items: int = None
) -> Dict[str, Any]:
    """
    Gera múltiplas imagens em lote

    Args:
        template_id: ID do template
        data_list: Lista de dicts com modificações
        response_format: Formato (png, jpg, webp, pdf)
        output_dir: Diretório de saída
        max_items: Limite de itens (None = todos)

    Returns:
        Dict com estatísticas da geração
    """

    # Valida API key
    api_key = os.getenv('ORSHOT_API_KEY')
    if not api_key:
        raise ValueError(
            "ORSHOT_API_KEY não encontrada no .env\n"
            "Adicione: ORSHOT_API_KEY=os-XXXXXXXXXXXXXXXX"
        )

    # Cria diretório de saída
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Limita quantidade se especificado
    if max_items:
        data_list = data_list[:max_items]

    total = len(data_list)
    print(f"🚀 Gerando {total} imagens em lote...")
    print(f"   Template: {template_id}")
    print(f"   Formato: {response_format}")
    print(f"   Output: {output_path}")
    print()

    # Inicializa cliente
    os_client = orshot.Orshot(api_key)

    # Estatísticas
    success_count = 0
    error_count = 0
    errors = []
    total_size = 0

    start_time = datetime.now()

    # Gera cada imagem
    for idx, modifications in enumerate(data_list, 1):
        try:
            print(f"   [{idx}/{total}] Gerando: {modifications.get('title', modifications.get('name', f'item_{idx}'))[:40]}...", end=' ')

            # Gera imagem
            response = os_client.render_from_template({
                'template_id': template_id,
                'modifications': modifications,
                'response_type': 'binary',
                'response_format': response_format
            })

            # Define nome do arquivo
            filename = modifications.get('filename',
                       modifications.get('title',
                       modifications.get('name', f'item_{idx}')))
            filename = f"{idx:03d}_{filename[:30]}.{response_format}"
            filename = filename.replace(' ', '_').replace('/', '_').replace('\\', '_')

            file_path = output_path / filename

            # Salva
            with Image.open(BytesIO(response.content)) as im:
                im.save(file_path)

            file_size = file_path.stat().st_size
            total_size += file_size

            print(f"✅ ({file_size/1024:.1f}KB)")
            success_count += 1

        except Exception as e:
            print(f"❌ Erro: {str(e)[:50]}")
            error_count += 1
            errors.append({
                'index': idx,
                'data': modifications,
                'error': str(e)
            })

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Resultado
    result = {
        'status': 'completed',
        'total_items': total,
        'success': success_count,
        'errors': error_count,
        'total_size_mb': round(total_size / (1024*1024), 2),
        'duration_seconds': round(duration, 2),
        'avg_time_per_image': round(duration / total, 2) if total > 0 else 0,
        'output_dir': str(output_path),
        'error_details': errors if errors else None
    }

    print()
    print(f"✅ Geração em lote concluída!")
    print(f"   Sucesso: {success_count}/{total}")
    print(f"   Erros: {error_count}")
    print(f"   Tamanho total: {result['total_size_mb']} MB")
    print(f"   Tempo: {duration:.1f}s ({result['avg_time_per_image']:.2f}s/imagem)")
    print(f"   Pasta: {output_path}")

    if errors:
        print(f"\n⚠️ {error_count} erros detectados:")
        for err in errors[:5]:  # Mostra até 5 erros
            print(f"   - Item {err['index']}: {err['error'][:60]}")
        if len(errors) > 5:
            print(f"   ... e mais {len(errors)-5} erros")

    return result


def main():
    """Função principal"""

    parser = argparse.ArgumentParser(
        description='Gera múltiplas imagens em lote com Orshot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    # Gerar 50 certificados (JSON)
    python3 scripts/orshot/batch_generate.py \\
        --template certificate-1 \\
        --data alunos.json \\
        --output certificados/

    # Gerar posts de produtos (CSV)
    python3 scripts/orshot/batch_generate.py \\
        --template product-post \\
        --data produtos.csv \\
        --format webp \\
        --limit 100

    # Gerar convites
    python3 scripts/orshot/batch_generate.py \\
        --template convite-festa \\
        --data convidados.json

Formato dos dados:

JSON:
[
  {"title": "João Silva", "date": "10/01/2025"},
  {"title": "Maria Santos", "date": "10/01/2025"}
]

CSV:
title,date,color
João Silva,10/01/2025,#FF0000
Maria Santos,10/01/2025,#00FF00
        """
    )

    parser.add_argument(
        '--template', '-t',
        required=True,
        help='ID do template'
    )

    parser.add_argument(
        '--data', '-d',
        required=True,
        help='Arquivo com dados (.json ou .csv)'
    )

    parser.add_argument(
        '--output', '-o',
        default='orshot_batch',
        help='Diretório de saída (padrão: orshot_batch)'
    )

    parser.add_argument(
        '--format', '-f',
        default='png',
        choices=['png', 'jpg', 'jpeg', 'webp', 'pdf'],
        help='Formato das imagens (padrão: png)'
    )

    parser.add_argument(
        '--limit', '-l',
        type=int,
        help='Limitar quantidade de imagens geradas'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verbose'
    )

    args = parser.parse_args()

    try:
        # Carrega dados
        print(f"📂 Carregando dados de {args.data}...")
        data_list = load_data(args.data)
        print(f"   {len(data_list)} itens carregados")

        if args.limit:
            print(f"   Limitando a {args.limit} itens")

        if args.verbose:
            print(f"\n🔧 Modo verbose")
            print(f"   Primeiros 3 itens:")
            for item in data_list[:3]:
                print(f"     - {item}")

        print()

        # Gera em lote
        result = batch_generate(
            template_id=args.template,
            data_list=data_list,
            response_format=args.format,
            output_dir=args.output,
            max_items=args.limit
        )

        if args.verbose:
            print(f"\n📊 Resultado completo:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        # Exit code baseado em erros
        if result['errors'] > 0:
            sys.exit(1)  # Pelo menos 1 erro

        return result

    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
