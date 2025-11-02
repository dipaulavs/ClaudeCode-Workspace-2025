#!/usr/bin/env python3
"""
Script para publicar Stories no Instagram via Instagram Graph API

Funcionalidades:
- ✅ Publicar Stories (imagens e vídeos)
- ✅ Aceita arquivos locais ou URLs
- ✅ Conversão automática PNG → JPG
- ✅ Upload automático via Catbox.moe
- ✅ Stories duram 24 horas
- ✅ Somente para contas Business/Creator

Uso:
    python3 publish_instagram_story.py imagem.jpg
    python3 publish_instagram_story.py imagem.png  # Convertido automaticamente
    python3 publish_instagram_story.py video.mp4
    python3 publish_instagram_story.py https://url-imagem.jpg
"""

import requests
import sys
import os
import time
import argparse
import subprocess
import tempfile
from PIL import Image

# Importar configurações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import instagram_config as config


class InstagramStoryPublisher:
    """Classe para publicar Stories no Instagram"""

    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.endpoints = config.ENDPOINTS
        self.temp_files = []  # Para limpar arquivos temporários

    def convert_png_to_jpg(self, png_path):
        """Converte PNG para JPG (Instagram não aceita PNG em Stories)"""
        print(f"🔄 Convertendo PNG para JPG...")

        try:
            # Abrir PNG
            img = Image.open(png_path)

            # Converter RGBA para RGB (se necessário)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Criar arquivo temporário JPG
            temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg', prefix='instagram_story_')
            os.close(temp_fd)

            # Salvar como JPG
            img.save(temp_path, 'JPEG', quality=95, optimize=True)

            # Registrar para limpar depois
            self.temp_files.append(temp_path)

            print(f"✅ Conversão concluída!")
            return temp_path

        except Exception as e:
            print(f"❌ Erro ao converter PNG: {e}")
            return None

    def cleanup_temp_files(self):
        """Remove arquivos temporários criados"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass

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

    def upload_to_catbox(self, file_path):
        """Faz upload de arquivo para o Catbox.moe"""
        print(f"📤 Fazendo upload: {os.path.basename(file_path)}...")

        try:
            result = subprocess.run(
                [
                    'curl', '-s', '-F', 'reqtype=fileupload',
                    '-F', f'fileToUpload=@{file_path}',
                    'https://catbox.moe/user/api.php'
                ],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos para vídeos
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

    def get_media_url(self, media_path_or_url):
        """Obtém URL da mídia (faz upload se for arquivo local)"""
        # Se já é uma URL, retorna diretamente
        if media_path_or_url.startswith("http://") or media_path_or_url.startswith("https://"):
            print(f"🔗 Usando URL fornecida: {media_path_or_url}")
            return media_path_or_url, self.detect_media_type(media_path_or_url)

        # Se é arquivo local
        if not os.path.exists(media_path_or_url):
            print(f"❌ Arquivo não encontrado: {media_path_or_url}")
            return None, None

        # Detectar tipo de mídia
        ext = os.path.splitext(media_path_or_url)[1].lower()

        # Se for PNG, converter para JPG automaticamente
        if ext == '.png':
            print(f"📁 Arquivo: {os.path.basename(media_path_or_url)} (PNG)")
            converted_path = self.convert_png_to_jpg(media_path_or_url)
            if not converted_path:
                return None, None
            media_path_or_url = converted_path
            ext = '.jpg'

        media_type = self.detect_media_type_by_extension(ext)

        if not media_type:
            print(f"❌ Formato não suportado: {ext}")
            print("   Formatos suportados: .jpg, .jpeg, .png (auto-convertido), .mp4, .mov")
            return None, None

        # Verificar tamanho
        file_size = os.path.getsize(media_path_or_url)
        file_size_mb = file_size / (1024 * 1024)

        if ext not in ['.png']:  # Já foi mostrado acima se for PNG
            print(f"📁 Arquivo: {os.path.basename(media_path_or_url)}")
        print(f"📏 Tamanho: {file_size_mb:.2f} MB")

        if file_size_mb > 200:
            print(f"⚠️ Arquivo muito grande ({file_size_mb:.2f} MB)")
            print(f"   Limite do Catbox.moe: 200 MB")
            return None, None

        # Fazer upload
        url = self.upload_to_catbox(media_path_or_url)
        return url, media_type

    def detect_media_type_by_extension(self, ext):
        """Detecta o tipo de mídia pela extensão"""
        if ext in ['.jpg', '.jpeg']:
            return 'image'
        elif ext in ['.mp4', '.mov']:
            return 'video'
        return None

    def detect_media_type(self, url):
        """Detecta o tipo de mídia pela URL"""
        if url.lower().endswith(('.jpg', '.jpeg')):
            return 'image'
        elif url.lower().endswith(('.mp4', '.mov')):
            return 'video'
        return 'image'  # Default para imagem

    def create_story_container(self, media_url, media_type):
        """Cria um container de Story"""
        print("\n📦 Criando container do Story...")

        params = {
            "media_type": "STORIES",
            "access_token": self.access_token
        }

        # Adicionar URL baseada no tipo de mídia
        if media_type == 'video':
            params["video_url"] = media_url
            print("🎬 Tipo: Vídeo")
        else:
            params["image_url"] = media_url
            print("🖼️  Tipo: Imagem")

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

    def check_container_status(self, container_id, is_video=False):
        """Verifica o status de processamento do container"""
        if not config.VALIDATION_CONFIG["check_container_status"]:
            return True

        print("\n⏳ Verificando status do Story...")

        # Para vídeos, aumentar tentativas e delay
        if is_video:
            max_retries = config.VALIDATION_CONFIG["max_retries"] * 3  # 9 tentativas
            retry_delay = config.VALIDATION_CONFIG["retry_delay"] * 2  # 10 segundos
            print("   (Vídeos podem demorar mais para processar)")
        else:
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

                print(f"🔍 [{attempt + 1}/{max_retries}] Status: {status}")

                if status_code == "FINISHED":
                    print("✅ Story pronto para publicação!")
                    return True
                elif status_code == "ERROR":
                    print("❌ Erro no processamento do Story")
                    return False
                elif status_code in ["IN_PROGRESS", "PUBLISHED"]:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        print("⚠️ Timeout, mas vou tentar publicar mesmo assim")
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
        print("\n🚀 Publicando Story no Instagram...")

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
            print(f"🔗 Story publicado na conta: @{config.INSTAGRAM_USERNAME}")
            print(f"⏰ Durará 24 horas")

            return media_id

        except Exception as e:
            print(config.MESSAGES["error_publish_failed"])
            print(f"Erro: {e}")
            return None

    def publish_story(self, media_path):
        """Método principal para publicar um Story completo"""
        print("=" * 60)
        print("📱 PUBLICANDO STORY NO INSTAGRAM")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"🆔 User ID: {self.user_id}")
        print(f"⏰ Duração: 24 horas")
        print("=" * 60)

        try:
            # 1. Verificar rate limit
            if not self.check_rate_limit():
                return False

            # 2. Obter URL da mídia
            print(f"\n📁 Processando mídia...")
            media_url, media_type = self.get_media_url(media_path)
            if not media_url:
                return False

            # 3. Criar container
            container_id = self.create_story_container(media_url, media_type)
            if not container_id:
                return False

            # 4. Verificar status
            if not self.check_container_status(container_id, is_video=(media_type == 'video')):
                return False

            # 5. Publicar
            media_id = self.publish_media(container_id)
            if not media_id:
                return False

            print("\n" + "=" * 60)
            print("✅ STORY PUBLICADO COM SUCESSO!")
            print("=" * 60)

            return True

        finally:
            # Limpar arquivos temporários (PNG convertidos)
            self.cleanup_temp_files()


def main():
    parser = argparse.ArgumentParser(
        description="Publicar Stories no Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Story com imagem local
  python3 publish_instagram_story.py foto.jpg

  # Story com vídeo local
  python3 publish_instagram_story.py video.mp4

  # Story com URL
  python3 publish_instagram_story.py "https://exemplo.com/imagem.jpg"

Requisitos de mídia:
  - Imagens: JPEG, PNG (convertido automaticamente para JPG)
  - Vídeos: MP4 ou MOV
  - Aspect ratio recomendado: 9:16 (vertical)
  - Tamanho: até 200 MB (limite do Catbox.moe)
  - Duração do Story: 24 horas
  - Rate limit: 100 posts por 24 horas
  - Somente contas Business/Creator

Notas:
  - Stories são publicados apenas no seu perfil
  - Aparecem no topo do feed dos seguidores
  - Desaparecem automaticamente após 24 horas
        """
    )

    parser.add_argument(
        "media",
        help="Caminho do arquivo (imagem/vídeo) ou URL pública"
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

    # Aplicar flags opcionais
    if args.no_rate_check:
        config.RATE_LIMITS["check_before_post"] = False

    if args.no_status_check:
        config.VALIDATION_CONFIG["check_container_status"] = False

    # Criar publisher e publicar
    publisher = InstagramStoryPublisher()
    success = publisher.publish_story(media_path=args.media)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
