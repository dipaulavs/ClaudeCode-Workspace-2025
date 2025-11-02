#!/usr/bin/env python3
"""
Upload rápido de arquivos da pasta Downloads para Nextcloud.

Este script facilita o upload de arquivos baixados, pegando automaticamente
o arquivo mais recente da pasta Downloads ou permitindo buscar por nome.

Exemplos:
    # Upload do arquivo mais recente do Downloads
    python3 scripts/nextcloud/upload_from_downloads.py

    # Upload de arquivo específico (busca por nome)
    python3 scripts/nextcloud/upload_from_downloads.py --name "imagem"

    # Upload com expiração de 7 dias
    python3 scripts/nextcloud/upload_from_downloads.py --days 7

    # Upload permanente
    python3 scripts/nextcloud/upload_from_downloads.py --permanent

    # Listar arquivos recentes do Downloads
    python3 scripts/nextcloud/upload_from_downloads.py --list
"""

import requests
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import glob

# Importa configurações
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.nextcloud_config import (
    NEXTCLOUD_URL,
    NEXTCLOUD_USER,
    NEXTCLOUD_PASSWORD,
    NEXTCLOUD_FOLDER,
    DEFAULT_EXPIRE_DAYS
)

class NextcloudUploader:
    """Classe para gerenciar uploads no Nextcloud"""

    def __init__(self, url, user, password, folder):
        self.url = url.rstrip('/')
        self.user = user
        self.password = password
        self.folder = folder
        self.webdav_url = f"{self.url}/remote.php/dav/files/{self.user}"
        self.auth = (user, password)

    def create_folder(self):
        """Cria a pasta no Nextcloud se não existir"""
        folder_url = f"{self.webdav_url}/{self.folder}"
        response = requests.request('MKCOL', folder_url, auth=self.auth)

        if response.status_code in [201, 405]:  # 201 = criado, 405 = já existe
            return True
        else:
            print(f"⚠️  Aviso ao criar pasta: {response.status_code}")
            return True  # Continua mesmo assim

    def upload_file(self, local_path, custom_filename=None):
        """Faz upload de arquivo para o Nextcloud"""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {local_path}")

        filename = custom_filename or os.path.basename(local_path)
        remote_path = f"{self.folder}/{filename}"
        upload_url = f"{self.webdav_url}/{remote_path}"

        print(f"📤 Fazendo upload de {filename}...")

        with open(local_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                auth=self.auth,
                headers={'Content-Type': 'application/octet-stream'}
            )

        if response.status_code in [201, 204]:
            print(f"✅ Upload concluído!")
            return remote_path
        else:
            raise Exception(f"Erro no upload: {response.status_code} - {response.text}")

    def create_public_link(self, remote_path, expire_days=None):
        """Cria um link público para o arquivo"""
        ocs_url = f"{self.url}/ocs/v2.php/apps/files_sharing/api/v1/shares"

        data = {
            'path': f"/{remote_path}",
            'shareType': 3,  # Link público
            'permissions': 1  # Somente leitura
        }

        if expire_days:
            expiration_date = (datetime.now() + timedelta(days=expire_days)).date()
            data['expireDate'] = expiration_date.strftime('%Y-%m-%d')
            print(f"🔗 Criando link público (expira em {expire_days} dia(s) - {expiration_date.strftime('%d/%m/%Y')})...")
        else:
            print(f"🔗 Criando link público (permanente)...")

        headers = {
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(
            ocs_url,
            data=data,
            auth=self.auth,
            headers=headers
        )

        if response.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            token = root.find('.//token')

            if token is not None:
                share_token = token.text
                filename = os.path.basename(remote_path)
                direct_url = f"{self.url}/s/{share_token}/download/{filename}"
                print(f"✅ Link público criado!")
                return direct_url
            else:
                raise Exception("Token não encontrado na resposta")
        else:
            raise Exception(f"Erro ao criar link público: {response.status_code} - {response.text}")

    def upload_and_share(self, local_path, expire_days=None, custom_filename=None):
        """Faz upload e retorna o link público"""
        self.create_folder()
        remote_path = self.upload_file(local_path, custom_filename)
        public_url = self.create_public_link(remote_path, expire_days)
        return public_url


def get_downloads_folder():
    """Retorna o caminho da pasta Downloads do usuário"""
    home = Path.home()
    downloads = home / "Downloads"

    if not downloads.exists():
        raise FileNotFoundError("Pasta Downloads não encontrada")

    return downloads


def list_recent_files(limit=10):
    """Lista os arquivos mais recentes da pasta Downloads"""
    downloads = get_downloads_folder()

    # Pega todos os arquivos (não diretórios)
    files = [f for f in downloads.iterdir() if f.is_file()]

    # Ordena por data de modificação (mais recente primeiro)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    return files[:limit]


def find_file_by_name(search_term):
    """Busca arquivo na pasta Downloads por nome parcial"""
    downloads = get_downloads_folder()

    # Busca por nome (case-insensitive)
    pattern = f"*{search_term}*"
    matches = list(downloads.glob(pattern))

    # Filtra apenas arquivos (não diretórios)
    files = [f for f in matches if f.is_file()]

    if not files:
        return None

    # Retorna o mais recente se houver múltiplos
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files[0]


def get_most_recent_file():
    """Retorna o arquivo mais recente da pasta Downloads"""
    files = list_recent_files(limit=1)
    return files[0] if files else None


def format_file_info(file_path):
    """Formata informações do arquivo para exibição"""
    stat = file_path.stat()
    size = stat.st_size
    mtime = datetime.fromtimestamp(stat.st_mtime)

    # Formata tamanho
    if size < 1024:
        size_str = f"{size} B"
    elif size < 1024 * 1024:
        size_str = f"{size / 1024:.1f} KB"
    else:
        size_str = f"{size / (1024 * 1024):.1f} MB"

    return f"{file_path.name} ({size_str}, {mtime.strftime('%d/%m/%Y %H:%M')})"


def main():
    parser = argparse.ArgumentParser(
        description='Upload rápido de arquivos da pasta Downloads para Nextcloud',
        epilog='Exemplos:\n'
               '  %(prog)s                              # Upload do arquivo mais recente\n'
               '  %(prog)s --name "imagem"              # Busca e faz upload de "imagem*"\n'
               '  %(prog)s --days 7                     # Upload com expiração de 7 dias\n'
               '  %(prog)s --permanent                  # Upload permanente\n'
               '  %(prog)s --list                       # Lista arquivos recentes\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--name', metavar='SEARCH',
                        help='Buscar arquivo por nome (parcial)')
    parser.add_argument('--folder', default=NEXTCLOUD_FOLDER,
                        help=f'Pasta no Nextcloud (padrão: {NEXTCLOUD_FOLDER})')
    parser.add_argument('--days', type=int, default=DEFAULT_EXPIRE_DAYS, metavar='DAYS',
                        help=f'Dias até expiração (padrão: {DEFAULT_EXPIRE_DAYS} dia)')
    parser.add_argument('--permanent', action='store_true',
                        help='Criar link permanente (sem expiração)')
    parser.add_argument('--rename', metavar='FILENAME',
                        help='Renomear arquivo no upload')
    parser.add_argument('--list', action='store_true',
                        help='Listar 10 arquivos mais recentes do Downloads')

    args = parser.parse_args()

    try:
        # Modo listagem
        if args.list:
            print("📁 Arquivos mais recentes na pasta Downloads:\n")
            files = list_recent_files(limit=10)
            for i, file_path in enumerate(files, 1):
                print(f"{i:2d}. {format_file_info(file_path)}")
            print("\n💡 Use --name para fazer upload de um arquivo específico")
            return

        # Busca o arquivo
        if args.name:
            file_path = find_file_by_name(args.name)
            if not file_path:
                print(f"❌ Nenhum arquivo encontrado com '{args.name}' na pasta Downloads")
                print("\n💡 Use --list para ver os arquivos disponíveis")
                sys.exit(1)
            print(f"📄 Arquivo encontrado: {format_file_info(file_path)}\n")
        else:
            file_path = get_most_recent_file()
            if not file_path:
                print("❌ Nenhum arquivo encontrado na pasta Downloads")
                sys.exit(1)
            print(f"📄 Arquivo mais recente: {format_file_info(file_path)}\n")

        # Faz upload
        uploader = NextcloudUploader(
            NEXTCLOUD_URL,
            NEXTCLOUD_USER,
            NEXTCLOUD_PASSWORD,
            args.folder
        )

        expire_days = None if args.permanent else args.days
        public_url = uploader.upload_and_share(
            str(file_path),
            expire_days=expire_days,
            custom_filename=args.rename
        )

        print("\n" + "="*60)
        print("🎉 SUCESSO!")
        print("="*60)
        print(f"\n📎 URL Pública:")
        print(f"\n{public_url}\n")

        if not args.permanent:
            expiration_date = (datetime.now() + timedelta(days=args.days)).date()
            print(f"⏰ Link expira em: {expiration_date.strftime('%d/%m/%Y')} às 23:59")
            print(f"💡 O Nextcloud deleta automaticamente após expiração")
        else:
            print(f"♾️  Link permanente (não expira)")

        print("="*60)

        return public_url

    except Exception as e:
        print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
