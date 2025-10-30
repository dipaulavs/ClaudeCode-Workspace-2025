#!/usr/bin/env python3
"""
Script wrapper para upload de imagens no Nextcloud com conversão automática para JPG
e expiração padrão de 24 horas.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from PIL import Image
import tempfile

def convert_to_jpg(input_path):
    """
    Converte qualquer imagem para JPG.
    Se já for JPG, retorna o caminho original.
    """
    path = Path(input_path)

    # Se já for JPG, retorna o original
    if path.suffix.lower() in ['.jpg', '.jpeg']:
        print(f"✅ Imagem já está em formato JPG")
        return input_path

    # Cria um arquivo temporário com extensão .jpg
    temp_dir = tempfile.gettempdir()
    output_filename = path.stem + '.jpg'
    output_path = os.path.join(temp_dir, output_filename)

    print(f"🔄 Convertendo {path.suffix} para JPG...")

    try:
        # Abre a imagem e converte para RGB (necessário para JPG)
        img = Image.open(input_path)

        # Se a imagem tiver transparência (RGBA), converte para RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            # Cria um fundo branco
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Salva como JPG com qualidade alta
        img.save(output_path, 'JPEG', quality=95, optimize=True)
        print(f"✅ Conversão concluída: {output_filename}")

        return output_path

    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        sys.exit(1)

def upload_to_nextcloud(image_path, expire_days=1):
    """
    Faz upload da imagem usando o script original do Nextcloud.
    """
    script_path = Path(__file__).parent / "upload_to_nextcloud.py"

    cmd = [
        'python3',
        str(script_path),
        image_path,
        '--days', str(expire_days)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)

        # Extrai a URL da saída
        for line in result.stdout.split('\n'):
            if line.startswith('https://'):
                return line.strip()

        return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no upload: {e.stderr}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Upload de imagem para Nextcloud com conversão para JPG e expiração de 24h',
        epilog='A imagem será automaticamente convertida para JPG e expirará em 24 horas.'
    )
    parser.add_argument('image_path', help='Caminho da imagem local (qualquer formato)')
    parser.add_argument('--days', type=int, default=1,
                        help='Dias até expiração (padrão: 1 dia)')

    args = parser.parse_args()

    # Verifica se o arquivo existe
    if not os.path.exists(args.image_path):
        print(f"❌ Arquivo não encontrado: {args.image_path}")
        sys.exit(1)

    print("="*60)
    print("🖼️  UPLOAD DE IMAGEM PARA NEXTCLOUD")
    print("="*60)
    print(f"📁 Arquivo: {os.path.basename(args.image_path)}")
    print(f"⏰ Expiração: {args.days} dia(s)")
    print("="*60)
    print()

    # Converte para JPG
    jpg_path = convert_to_jpg(args.image_path)

    # Faz upload
    print()
    url = upload_to_nextcloud(jpg_path, expire_days=args.days)

    # Remove arquivo temporário se foi criado
    if jpg_path != args.image_path:
        try:
            os.remove(jpg_path)
            print(f"🗑️  Arquivo temporário removido")
        except:
            pass

    if url:
        return url
    else:
        print("❌ Não foi possível obter a URL do arquivo")
        sys.exit(1)

if __name__ == "__main__":
    main()
