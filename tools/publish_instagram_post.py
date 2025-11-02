#!/usr/bin/env python3
"""
Script para publicar posts no Instagram via Instagram Graph API

Funcionalidades:
- ✅ Publicar posts com imagens (URL ou arquivo local)
- ✅ Upload automático para Nextcloud se for arquivo local
- ✅ Conversão automática de PNG para JPEG
- ✅ Verificação de rate limits
- ✅ Validação de status do container
- ✅ Legendas com formatação

Uso:
    python3 publish_instagram_post.py "caminho/para/imagem.jpg" "Minha legenda aqui"
    python3 publish_instagram_post.py "https://exemplo.com/imagem.jpg" "Legenda"
    python3 publish_instagram_post.py imagem.jpg  # Sem legenda
"""

import requests
import sys
import os
import time
import argparse
from pathlib import Path
from PIL import Image
import tempfile

# Importar configurações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import instagram_config as config

# Importar uploader do Nextcloud
sys.path.insert(0, os.path.dirname(__file__))


class InstagramPublisher:
    """Classe para publicar posts no Instagram"""

    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.endpoints = config.ENDPOINTS

    def check_rate_limit(self):
        """Verifica o rate limit atual"""
        if not config.RATE_LIMITS["check_before_post"]:
            return True

        print(config.MESSAGES["info_checking_rate_limit"])

        try:
            response = requests.get(
                config.ENDPOINTS["rate_limit"],
                params={"access_token": self.access_token}
            )
            response.raise_for_status()

            data = response.json()
            quota_usage = data.get("data", [{}])[0].get("quota_usage", 0)

            if quota_usage >= config.RATE_LIMITS["posts_per_day"]:
                print(config.MESSAGES["error_rate_limit"])
                print(f"📊 Uso atual: {quota_usage}/{config.RATE_LIMITS['posts_per_day']}")
                return False

            print(f"✅ Rate limit OK: {quota_usage}/{config.RATE_LIMITS['posts_per_day']} posts usados")
            return True

        except Exception as e:
            print(f"⚠️ Não foi possível verificar rate limit: {e}")
            print("Continuando mesmo assim...")
            return True

    def validate_image_format(self, file_path):
        """Valida se o formato da imagem é suportado"""
        ext = os.path.splitext(file_path)[1].lower()

        if ext in config.MEDIA_CONFIG["allowed_image_formats"]:
            return True, file_path

        if ext in [".png", ".gif", ".bmp", ".webp"]:
            if config.UPLOAD_CONFIG["convert_png_to_jpeg"]:
                print(config.MESSAGES["warning_converting_png"])
                return True, self.convert_to_jpeg(file_path)
            else:
                print(config.MESSAGES["error_invalid_image"])
                return False, None

        print(config.MESSAGES["error_invalid_image"])
        return False, None

    def convert_to_jpeg(self, file_path):
        """Converte imagem para JPEG"""
        try:
            img = Image.open(file_path)

            # Converter para RGB se necessário (PNG com transparência)
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background

            # Criar arquivo temporário
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg",
                dir=os.path.dirname(file_path)
            )

            # Salvar como JPEG
            img.save(
                temp_file.name,
                "JPEG",
                quality=config.UPLOAD_CONFIG["jpeg_quality"],
                optimize=True
            )

            temp_file.close()
            print(f"✅ Imagem convertida para JPEG: {temp_file.name}")
            return temp_file.name

        except Exception as e:
            print(f"❌ Erro ao converter imagem: {e}")
            return None

    def upload_to_catbox(self, file_path):
        """Faz upload da imagem para o Catbox.moe e retorna URL pública"""
        print(config.MESSAGES["info_uploading"])

        try:
            import subprocess

            # Upload via curl para Catbox.moe
            result = subprocess.run(
                [
                    'curl', '-s', '-F', 'reqtype=fileupload',
                    '-F', f'fileToUpload=@{file_path}',
                    'https://catbox.moe/user/api.php'
                ],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                url = result.stdout.strip()
                if url.startswith('https://files.catbox.moe/'):
                    print(f"✅ Upload concluído!")
                    print(f"🔗 URL: {url}")
                    return url
                else:
                    print(f"❌ Erro no upload: resposta inesperada")
                    return None
            else:
                print(f"❌ Erro ao fazer upload: {result.stderr}")
                return None

        except Exception as e:
            print(f"❌ Erro ao fazer upload: {e}")
            return None

    def get_image_url(self, image_path_or_url):
        """Obtém URL da imagem (faz upload se for arquivo local)"""
        # Se já é uma URL, retorna diretamente
        if image_path_or_url.startswith("http://") or image_path_or_url.startswith("https://"):
            print(f"🔗 Usando URL fornecida: {image_path_or_url}")
            return image_path_or_url

        # Se é arquivo local
        if not os.path.exists(image_path_or_url):
            print(f"❌ Arquivo não encontrado: {image_path_or_url}")
            return None

        # Validar formato
        is_valid, converted_path = self.validate_image_format(image_path_or_url)
        if not is_valid:
            return None

        # Fazer upload
        if config.UPLOAD_CONFIG["auto_upload_to_nextcloud"]:
            return self.upload_to_catbox(converted_path)
        else:
            print("❌ Upload automático está desabilitado. Forneça uma URL pública.")
            return None

    def validate_caption(self, caption):
        """Valida a legenda"""
        if not caption:
            return True, ""

        if len(caption) > config.MEDIA_CONFIG["max_caption_length"]:
            print(config.MESSAGES["error_caption_too_long"])
            print(f"Tamanho atual: {len(caption)} caracteres")
            return False, None

        return True, caption

    def create_media_container(self, image_url, caption=""):
        """Cria um container de mídia no Instagram"""
        print("\n📦 Criando container de mídia...")

        params = {
            "image_url": image_url,
            "access_token": self.access_token
        }

        if caption:
            params["caption"] = caption

        try:
            response = requests.post(
                self.endpoints["create_media"],
                params=params
            )
            response.raise_for_status()

            data = response.json()
            container_id = data.get("id")

            if not container_id:
                print(config.MESSAGES["error_container_failed"])
                print(f"Resposta da API: {data}")
                return None

            print(config.MESSAGES["success_container"])
            print(f"🆔 Container ID: {container_id}")

            return container_id

        except requests.exceptions.HTTPError as e:
            print(config.MESSAGES["error_container_failed"])
            print(f"Erro HTTP: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return None
        except Exception as e:
            print(config.MESSAGES["error_container_failed"])
            print(f"Erro: {e}")
            return None

    def check_container_status(self, container_id):
        """Verifica o status de processamento do container"""
        if not config.VALIDATION_CONFIG["check_container_status"]:
            return True

        print("\n⏳ Verificando status do container...")

        max_retries = config.VALIDATION_CONFIG["max_retries"]
        retry_delay = config.VALIDATION_CONFIG["retry_delay"]

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"{self.endpoints['get_media']}/{container_id}",
                    params={
                        "fields": "status_code,status",
                        "access_token": self.access_token
                    }
                )
                response.raise_for_status()

                data = response.json()
                status_code = data.get("status_code")
                status = data.get("status")

                print(f"🔍 Status: {status} (código: {status_code})")

                if status_code == "FINISHED":
                    print("✅ Container pronto para publicação!")
                    return True
                elif status_code == "ERROR":
                    print("❌ Erro no processamento do container")
                    return False
                elif status_code in ["IN_PROGRESS", "PUBLISHED"]:
                    if attempt < max_retries - 1:
                        print(f"⏳ Aguardando... (tentativa {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                    else:
                        print("⚠️ Timeout na verificação, mas vou tentar publicar mesmo assim")
                        return True

            except Exception as e:
                print(f"⚠️ Erro ao verificar status: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("⚠️ Vou tentar publicar mesmo assim")
                    return True

        return True

    def publish_media(self, container_id):
        """Publica o container de mídia"""
        print("\n🚀 Publicando post no Instagram...")

        params = {
            "creation_id": container_id,
            "access_token": self.access_token
        }

        try:
            response = requests.post(
                self.endpoints["publish_media"],
                params=params
            )
            response.raise_for_status()

            data = response.json()
            media_id = data.get("id")

            if not media_id:
                print(config.MESSAGES["error_publish_failed"])
                print(f"Resposta da API: {data}")
                return None

            print(config.MESSAGES["success_publish"])
            print(f"🆔 Media ID: {media_id}")
            print(f"🔗 Post publicado na conta: @{config.INSTAGRAM_USERNAME}")
            print(f"🔗 Ver post: https://www.instagram.com/p/{self._get_shortcode(media_id)}/")

            return media_id

        except requests.exceptions.HTTPError as e:
            print(config.MESSAGES["error_publish_failed"])
            print(f"Erro HTTP: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return None
        except Exception as e:
            print(config.MESSAGES["error_publish_failed"])
            print(f"Erro: {e}")
            return None

    def _get_shortcode(self, media_id):
        """Tenta obter o shortcode do post (código da URL)"""
        try:
            response = requests.get(
                f"{self.endpoints['get_media']}/{media_id}",
                params={
                    "fields": "permalink,shortcode",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("shortcode", media_id)
        except:
            return media_id

    def publish_post(self, image_path_or_url, caption=""):
        """Método principal para publicar um post completo"""
        print("=" * 60)
        print("📸 PUBLICANDO POST NO INSTAGRAM")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"🆔 User ID: {self.user_id}")
        print("=" * 60)

        # 1. Verificar rate limit
        if not self.check_rate_limit():
            return False

        # 2. Validar legenda
        is_valid, validated_caption = self.validate_caption(caption)
        if not is_valid:
            return False

        # 3. Obter URL da imagem
        image_url = self.get_image_url(image_path_or_url)
        if not image_url:
            return False

        # 4. Criar container
        container_id = self.create_media_container(image_url, validated_caption)
        if not container_id:
            return False

        # 5. Verificar status do container
        if not self.check_container_status(container_id):
            return False

        # 6. Publicar
        media_id = self.publish_media(container_id)
        if not media_id:
            return False

        print("\n" + "=" * 60)
        print("✅ POST PUBLICADO COM SUCESSO!")
        print("=" * 60)

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Publicar posts no Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Post com arquivo local e legenda
  python3 publish_instagram_post.py foto.jpg "Minha primeira postagem! #instagram"

  # Post com URL de imagem
  python3 publish_instagram_post.py "https://exemplo.com/foto.jpg" "Postagem via API"

  # Post sem legenda
  python3 publish_instagram_post.py foto.jpg

  # Post com arquivo PNG (será convertido para JPEG)
  python3 publish_instagram_post.py imagem.png "Post convertido automaticamente"

Notas:
  - Instagram API aceita APENAS imagens JPEG
  - Imagens PNG são convertidas automaticamente
  - Arquivos locais são enviados para Nextcloud
  - Máximo de 100 posts por 24 horas
        """
    )

    parser.add_argument(
        "image",
        help="Caminho do arquivo de imagem ou URL pública"
    )

    parser.add_argument(
        "caption",
        nargs="?",
        default="",
        help="Legenda do post (opcional, máximo 2200 caracteres)"
    )

    parser.add_argument(
        "--no-rate-check",
        action="store_true",
        help="Pular verificação de rate limit"
    )

    parser.add_argument(
        "--no-status-check",
        action="store_true",
        help="Não aguardar verificação de status do container"
    )

    args = parser.parse_args()

    # Aplicar flags opcionais
    if args.no_rate_check:
        config.RATE_LIMITS["check_before_post"] = False

    if args.no_status_check:
        config.VALIDATION_CONFIG["check_container_status"] = False

    # Criar publisher e publicar
    publisher = InstagramPublisher()
    success = publisher.publish_post(args.image, args.caption)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
