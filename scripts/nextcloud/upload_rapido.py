#!/usr/bin/env python3
"""
Upload rápido de imagens para Nextcloud com auto-delete.

Upload permanente para imagens/upload/ com exclusão automática do arquivo local.

Uso:
    # Upload da pasta local (~/Pictures/upload/)
    python3 scripts/nextcloud/upload_rapido.py --from-local

    # 1 imagem
    python3 scripts/nextcloud/upload_rapido.py foto.jpg

    # Múltiplas imagens
    python3 scripts/nextcloud/upload_rapido.py foto1.jpg foto2.jpg foto3.jpg

    # Buscar no Downloads
    python3 scripts/nextcloud/upload_rapido.py --name "screenshot"
"""

import requests
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Importa configurações
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.nextcloud_config import (
    NEXTCLOUD_URL,
    NEXTCLOUD_USER,
    NEXTCLOUD_PASSWORD
)

# Configuração fixa para este script
FIXED_FOLDER = "imagens/upload"

class QuickUploader:
    """Upload rápido com auto-delete"""

    def __init__(self, url, user, password):
        self.url = url.rstrip('/')
        self.user = user
        self.password = password
        self.folder = FIXED_FOLDER
        self.webdav_url = f"{self.url}/remote.php/dav/files/{self.user}"
        self.auth = (user, password)

    def upload_file(self, local_path):
        """Faz upload de arquivo para o Nextcloud"""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {local_path}")

        filename = os.path.basename(local_path)
        remote_path = f"{self.folder}/{filename}"
        upload_url = f"{self.webdav_url}/{remote_path}"

        print(f"📤 Upload: {filename}")

        with open(local_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                auth=self.auth,
                headers={'Content-Type': 'application/octet-stream'}
            )

        if response.status_code in [201, 204]:
            return remote_path
        else:
            raise Exception(f"Erro no upload: {response.status_code}")

    def create_public_link(self, remote_path):
        """Cria link público permanente"""
        ocs_url = f"{self.url}/ocs/v2.php/apps/files_sharing/api/v1/shares"

        data = {
            'path': f"/{remote_path}",
            'shareType': 3,  # Link público
            'permissions': 1  # Somente leitura
        }

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
                return direct_url
            else:
                raise Exception("Token não encontrado")
        else:
            raise Exception(f"Erro ao criar link: {response.status_code}")

    def upload_and_delete(self, local_path):
        """
        Upload + Link + Delete local

        Returns:
            dict: {'filename': str, 'url': str, 'deleted': bool}
        """
        filename = os.path.basename(local_path)

        try:
            # Upload
            remote_path = self.upload_file(local_path)

            # Link público
            public_url = self.create_public_link(remote_path)

            # Delete arquivo local
            os.remove(local_path)
            deleted = True
            print(f"✅ {filename} → 🗑️  Local deletado")

            return {
                'filename': filename,
                'url': public_url,
                'deleted': deleted
            }

        except Exception as e:
            print(f"❌ {filename}: {e}")
            return {
                'filename': filename,
                'url': None,
                'deleted': False,
                'error': str(e)
            }


def find_file_in_downloads(search_name):
    """Busca arquivo no Downloads por nome parcial"""
    downloads = Path.home() / "Downloads"

    if not downloads.exists():
        return None

    # Lista arquivos que contêm o termo de busca
    matches = []
    for file_path in downloads.iterdir():
        if file_path.is_file() and search_name.lower() in file_path.name.lower():
            matches.append(file_path)

    if not matches:
        return None

    # Retorna o mais recente
    return max(matches, key=lambda p: p.stat().st_mtime)


def get_files_from_local_folder():
    """Pega todos os arquivos da pasta ~/Pictures/upload/"""
    local_folder = Path.home() / "Pictures" / "upload"

    if not local_folder.exists():
        return []

    # Lista todos os arquivos (imagens)
    files = []
    for file_path in local_folder.iterdir():
        if file_path.is_file():
            files.append(file_path)

    if not files:
        return []

    # Ordena por data de modificação (mais recente primeiro)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def main():
    parser = argparse.ArgumentParser(
        description='Upload rápido de imagens com auto-delete',
        epilog='Exemplos:\n'
               '  %(prog)s --from-local                    # Upload da pasta ~/Pictures/upload/\n'
               '  %(prog)s foto.jpg                        # Upload de 1 imagem\n'
               '  %(prog)s foto1.jpg foto2.jpg foto3.jpg   # Upload múltiplo\n'
               '  %(prog)s --name "screenshot"             # Busca no Downloads\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('files', nargs='*', help='Arquivos para upload')
    parser.add_argument('--name', help='Buscar arquivo no Downloads por nome')
    parser.add_argument('--from-local', action='store_true',
                        help='Upload de todos os arquivos da pasta ~/Pictures/upload/')

    args = parser.parse_args()

    # Determina arquivos a fazer upload
    files_to_upload = []

    if args.from_local:
        # Busca todos os arquivos da pasta local
        local_files = get_files_from_local_folder()
        if local_files:
            files_to_upload = [str(f) for f in local_files]
            print(f"📂 Pasta local: ~/Pictures/upload/")
            print(f"📸 Encontrados: {len(local_files)} arquivo(s)")
        else:
            print(f"❌ Nenhum arquivo encontrado em ~/Pictures/upload/")
            sys.exit(1)
    elif args.name:
        # Busca no Downloads
        found = find_file_in_downloads(args.name)
        if found:
            files_to_upload.append(str(found))
            print(f"🔍 Encontrado: {found.name}")
        else:
            print(f"❌ Nenhum arquivo encontrado com '{args.name}' no Downloads")
            sys.exit(1)
    elif args.files:
        # Usa arquivos fornecidos
        files_to_upload = args.files
    else:
        parser.print_help()
        sys.exit(1)

    # Valida existência dos arquivos
    for file_path in files_to_upload:
        if not os.path.exists(file_path):
            print(f"❌ Arquivo não encontrado: {file_path}")
            sys.exit(1)

    try:
        uploader = QuickUploader(
            NEXTCLOUD_URL,
            NEXTCLOUD_USER,
            NEXTCLOUD_PASSWORD
        )

        print(f"\n🚀 Upload para: {FIXED_FOLDER}/")
        print(f"📁 Total: {len(files_to_upload)} arquivo(s)")
        print(f"♾️  Links: Permanentes\n")
        print("="*60)

        results = []
        for file_path in files_to_upload:
            result = uploader.upload_and_delete(file_path)
            results.append(result)
            print("")

        # Resumo final
        print("="*60)
        print("📋 RESUMO")
        print("="*60)

        success_count = sum(1 for r in results if r.get('url'))
        print(f"\n✅ Sucesso: {success_count}/{len(results)}\n")

        for result in results:
            if result.get('url'):
                print(f"🔗 {result['filename']}")
                print(f"   {result['url']}\n")
            else:
                print(f"❌ {result['filename']}: {result.get('error', 'Erro desconhecido')}\n")

        print("="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
