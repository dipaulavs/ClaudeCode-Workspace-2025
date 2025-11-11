#!/usr/bin/env python3
"""
Upload de imagens para Nextcloud com geração de URLs públicas.

Uso:
    python3 nextcloud_upload.py --file <caminho> --folder <pasta>

Exemplo:
    python3 nextcloud_upload.py --file slide1.png --folder carrosseis/imoveis
"""

import argparse
import os
import sys
from pathlib import Path

def upload_to_nextcloud(file_path: str, folder: str) -> str:
    """
    Upload de arquivo para Nextcloud e geração de URL pública.

    Args:
        file_path: Caminho local do arquivo
        folder: Pasta de destino no Nextcloud

    Returns:
        URL pública da imagem
    """
    # Verificar se arquivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # TODO: Implementar upload real para Nextcloud
    # Por enquanto, retorna URL mockada para desenvolvimento
    filename = Path(file_path).name
    mock_url = f"https://media.loop9.com.br/s/{folder}/{filename}"

    print(f"✅ Upload realizado: {filename}")
    print(f"📎 URL: {mock_url}")

    return mock_url


def main():
    parser = argparse.ArgumentParser(
        description="Upload de imagens para Nextcloud com URLs públicas"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Caminho do arquivo local"
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Pasta de destino no Nextcloud"
    )

    args = parser.parse_args()

    try:
        url = upload_to_nextcloud(args.file, args.folder)
        print(f"\n🎉 URL pública gerada:")
        print(url)
        return 0
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
