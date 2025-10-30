#!/usr/bin/env python3
"""
Script para fazer upload de imagens para o Nextcloud e gerar links públicos diretos.
"""

import requests
import os
import sys
import argparse
from pathlib import Path
from urllib.parse import quote
from datetime import datetime, timedelta

# Configurações do Nextcloud
NEXTCLOUD_URL = "https://media.loop9.com.br"
NEXTCLOUD_USER = "dipaula"
NEXTCLOUD_PASSWORD = "Felipe33876865@"
NEXTCLOUD_FOLDER = "claude-code"

class NextcloudUploader:
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

    def upload_image(self, local_path):
        """Faz upload da imagem para o Nextcloud"""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {local_path}")

        filename = os.path.basename(local_path)

        # Força extensão .jpg se não tiver
        name_without_ext = os.path.splitext(filename)[0]
        if not filename.lower().endswith(('.jpg', '.jpeg')):
            filename = f"{name_without_ext}.jpg"
            print(f"🔄 Renomeando para: {filename}")

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

    def create_public_link(self, remote_path, expire_days=1):
        """Cria um link público para a imagem"""
        ocs_url = f"{self.url}/ocs/v2.php/apps/files_sharing/api/v1/shares"

        data = {
            'path': f"/{remote_path}",
            'shareType': 3,  # Link público
            'permissions': 1  # Somente leitura
        }

        # Adiciona data de expiração (padrão 24h)
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
            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)

            # Busca o token do compartilhamento
            token = root.find('.//token')

            if token is not None:
                share_token = token.text
                # URL direta do arquivo (com nome do arquivo no final)
                filename = os.path.basename(remote_path)
                direct_url = f"{self.url}/s/{share_token}/download/{filename}"
                print(f"✅ Link público criado!")
                return direct_url
            else:
                raise Exception("Token não encontrado na resposta")
        else:
            raise Exception(f"Erro ao criar link público: {response.status_code} - {response.text}")

    def upload_and_share(self, local_path, expire_days=1):
        """Faz upload e retorna o link público direto"""
        # Cria a pasta se não existir
        self.create_folder()

        # Faz upload
        remote_path = self.upload_image(local_path)

        # Cria link público com expiração
        public_url = self.create_public_link(remote_path, expire_days)

        return public_url


def main():
    parser = argparse.ArgumentParser(
        description='Upload de imagem para Nextcloud com link público temporário',
        epilog='Exemplos:\n'
               '  %(prog)s imagem.jpg                    # Expira em 1 dia (padrão)\n'
               '  %(prog)s imagem.jpg --days 7           # Expira em 7 dias\n'
               '  %(prog)s imagem.jpg --permanent        # Link permanente\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('image_path', help='Caminho da imagem local')
    parser.add_argument('--folder', default=NEXTCLOUD_FOLDER, help='Pasta no Nextcloud')
    parser.add_argument('--days', type=int, default=1, metavar='DAYS',
                        help='Dias até expiração (padrão: 1 dia = 24h)')
    parser.add_argument('--permanent', action='store_true',
                        help='Criar link permanente (sem expiração)')

    args = parser.parse_args()

    try:
        uploader = NextcloudUploader(
            NEXTCLOUD_URL,
            NEXTCLOUD_USER,
            NEXTCLOUD_PASSWORD,
            args.folder
        )

        expire_days = None if args.permanent else args.days
        public_url = uploader.upload_and_share(args.image_path, expire_days=expire_days)

        print("\n" + "="*60)
        print("🎉 SUCESSO!")
        print("="*60)
        print(f"\n📸 URL Pública da Imagem:")
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
