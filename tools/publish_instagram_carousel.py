#!/usr/bin/env python3
"""
Script para publicar carrosséis no Instagram via Instagram Graph API

Funcionalidades:
- ✅ Publicar carrosséis com até 10 imagens
- ✅ Aceita arquivos locais ou URLs
- ✅ Upload automático via Catbox.moe
- ✅ Conversão automática PNG → JPEG
- ✅ Validação de containers

Uso:
    python3 publish_instagram_carousel.py img1.jpg img2.jpg img3.jpg "Legenda"
    python3 publish_instagram_carousel.py https://url1.jpg https://url2.jpg "Legenda"
    python3 publish_instagram_carousel.py img1.jpg https://url2.jpg img3.png "Legenda"
"""

import requests
import sys
import os
import time
import argparse
from pathlib import Path
from PIL import Image
import tempfile
import subprocess

# Importar configurações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import instagram_config as config


class InstagramCarouselPublisher:
    """Classe para publicar carrosséis no Instagram"""

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
                print(f"🔄 Convertendo {os.path.basename(file_path)} para JPEG...")
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

            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg",
                dir=os.path.dirname(file_path)
            )

            img.save(
                temp_file.name,
                "JPEG",
                quality=config.UPLOAD_CONFIG["jpeg_quality"],
                optimize=True
            )

            temp_file.close()
            return temp_file.name

        except Exception as e:
            print(f"❌ Erro ao converter imagem: {e}")
            return None

    def upload_to_catbox(self, file_path):
        """Faz upload da imagem para o Catbox.moe"""
        try:
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
                    return url
                else:
                    return None
            else:
                return None

        except Exception as e:
            print(f"❌ Erro ao fazer upload: {e}")
            return None

    def get_image_url(self, image_path_or_url):
        """Obtém URL da imagem (faz upload se for arquivo local)"""
        # Se já é uma URL, retorna diretamente
        if image_path_or_url.startswith("http://") or image_path_or_url.startswith("https://"):
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
        print(f"📤 Fazendo upload: {os.path.basename(image_path_or_url)}...")
        url = self.upload_to_catbox(converted_path)

        if url:
            print(f"✅ Upload OK: {os.path.basename(image_path_or_url)}")
            return url
        else:
            print(f"❌ Falha no upload: {os.path.basename(image_path_or_url)}")
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

    def create_carousel_item_container(self, image_url):
        """Cria um container de item de carrossel"""
        params = {
            "image_url": image_url,
            "is_carousel_item": "true",
            "access_token": self.access_token
        }

        try:
            response = requests.post(
                self.endpoints["create_media"],
                params=params
            )
            response.raise_for_status()

            data = response.json()
            container_id = data.get("id")

            if not container_id:
                print(f"❌ Falha ao criar item: {data}")
                return None

            return container_id

        except Exception as e:
            print(f"❌ Erro ao criar item: {e}")
            return None

    def create_carousel_container(self, item_ids, caption=""):
        """Cria o container principal do carrossel"""
        params = {
            "media_type": "CAROUSEL",
            "children": ",".join(item_ids),
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

                if status_code == "FINISHED":
                    return True
                elif status_code == "ERROR":
                    print("❌ Erro no processamento do container")
                    return False
                elif status_code in ["IN_PROGRESS", "PUBLISHED"]:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        return True

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    return True

        return True

    def publish_media(self, container_id):
        """Publica o container de mídia"""
        print("\n🚀 Publicando carrossel no Instagram...")

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

            return media_id

        except Exception as e:
            print(config.MESSAGES["error_publish_failed"])
            print(f"Erro: {e}")
            return None

    def publish_carousel(self, image_paths, caption=""):
        """Método principal para publicar um carrossel completo"""
        print("=" * 60)
        print("🎠 PUBLICANDO CARROSSEL NO INSTAGRAM")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"🆔 User ID: {self.user_id}")
        print(f"🖼️  Imagens: {len(image_paths)}")
        print("=" * 60)

        # 1. Verificar rate limit
        if not self.check_rate_limit():
            return False

        # 2. Validar legenda
        is_valid, validated_caption = self.validate_caption(caption)
        if not is_valid:
            return False

        # 3. Validar número de imagens
        if len(image_paths) < 2:
            print("❌ Carrossel precisa de pelo menos 2 imagens")
            return False

        if len(image_paths) > 10:
            print("❌ Carrossel suporta no máximo 10 imagens")
            return False

        # 4. Processar todas as imagens e obter URLs
        print(f"\n📸 Processando {len(image_paths)} imagens...")
        image_urls = []

        for i, img_path in enumerate(image_paths, 1):
            print(f"\n[{i}/{len(image_paths)}] Processando: {os.path.basename(img_path) if not img_path.startswith('http') else 'URL'}")
            url = self.get_image_url(img_path)
            if not url:
                print(f"❌ Falha ao processar imagem {i}")
                return False
            image_urls.append(url)

        print(f"\n✅ Todas as {len(image_urls)} imagens processadas!")

        # 5. Criar containers individuais para cada imagem
        print(f"\n📦 Criando containers dos itens...")
        item_ids = []

        for i, url in enumerate(image_urls, 1):
            print(f"[{i}/{len(image_urls)}] Criando container do item...")
            item_id = self.create_carousel_item_container(url)
            if not item_id:
                print(f"❌ Falha ao criar container do item {i}")
                return False
            item_ids.append(item_id)
            print(f"✅ Item {i} criado: {item_id}")

        print(f"\n✅ Todos os {len(item_ids)} containers criados!")

        # 6. Criar container do carrossel
        print("\n📦 Criando container do carrossel...")
        carousel_id = self.create_carousel_container(item_ids, validated_caption)
        if not carousel_id:
            return False

        # 7. Verificar status
        print("\n⏳ Verificando status do carrossel...")
        if not self.check_container_status(carousel_id):
            return False

        print("✅ Carrossel pronto para publicação!")

        # 8. Publicar
        media_id = self.publish_media(carousel_id)
        if not media_id:
            return False

        print("\n" + "=" * 60)
        print("✅ CARROSSEL PUBLICADO COM SUCESSO!")
        print("=" * 60)

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Publicar carrosséis no Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Carrossel com 3 imagens locais
  python3 publish_instagram_carousel.py img1.jpg img2.jpg img3.jpg "Meu carrossel!"

  # Mix de URLs e arquivos locais
  python3 publish_instagram_carousel.py foto1.jpg https://exemplo.com/foto2.jpg foto3.png "Legenda"

  # Apenas URLs
  python3 publish_instagram_carousel.py https://url1.jpg https://url2.jpg "Carrossel via URLs"

Notas:
  - Mínimo: 2 imagens
  - Máximo: 10 imagens
  - Instagram aceita APENAS JPEG
  - PNG é convertido automaticamente
  - Arquivos locais são enviados para Catbox.moe
  - Rate limit: 100 posts por 24 horas
        """
    )

    parser.add_argument(
        "images",
        nargs="+",
        help="Caminhos de arquivos ou URLs das imagens (2-10 imagens)"
    )

    parser.add_argument(
        "--caption",
        default="",
        help="Legenda do carrossel (opcional, máximo 2200 caracteres)"
    )

    parser.add_argument(
        "--no-rate-check",
        action="store_true",
        help="Pular verificação de rate limit"
    )

    parser.add_argument(
        "--no-status-check",
        action="store_true",
        help="Não aguardar verificação de status"
    )

    args = parser.parse_args()

    # Separar legenda dos argumentos se for o último
    images = args.images
    caption = args.caption

    # Se o último argumento não é uma imagem válida, assume como legenda
    if len(images) > 0:
        last_arg = images[-1]
        # Se não começa com http e não existe como arquivo, assume como legenda
        if not last_arg.startswith("http") and not os.path.exists(last_arg):
            caption = last_arg
            images = images[:-1]

    if len(images) < 2:
        print("❌ Erro: É necessário fornecer pelo menos 2 imagens para um carrossel")
        print("Uso: python3 publish_instagram_carousel.py img1.jpg img2.jpg [img3.jpg ...] \"Legenda\"")
        sys.exit(1)

    # Aplicar flags opcionais
    if args.no_rate_check:
        config.RATE_LIMITS["check_before_post"] = False

    if args.no_status_check:
        config.VALIDATION_CONFIG["check_container_status"] = False

    # Criar publisher e publicar
    publisher = InstagramCarouselPublisher()
    success = publisher.publish_carousel(images, caption)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
