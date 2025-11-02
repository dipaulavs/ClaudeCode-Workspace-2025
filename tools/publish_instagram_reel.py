#!/usr/bin/env python3
"""
Script para publicar Reels no Instagram via Instagram Graph API

Funcionalidades:
- ✅ Publicar Reels (vídeos curtos até 90s)
- ✅ Aceita arquivos locais ou URLs
- ✅ Upload automático via Catbox.moe
- ✅ Opções: compartilhar no feed, capa personalizada
- ✅ Validação de containers

Uso:
    python3 publish_instagram_reel.py video.mp4 "Legenda"
    python3 publish_instagram_reel.py https://url-video.mp4 "Legenda"
    python3 publish_instagram_reel.py video.mp4 "Legenda" --share-feed --cover capa.jpg
"""

import requests
import sys
import os
import time
import argparse
import subprocess

# Importar configurações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import instagram_config as config


class InstagramReelPublisher:
    """Classe para publicar Reels no Instagram"""

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

    def get_video_url(self, video_path_or_url):
        """Obtém URL do vídeo (faz upload se for arquivo local)"""
        # Se já é uma URL, retorna diretamente
        if video_path_or_url.startswith("http://") or video_path_or_url.startswith("https://"):
            print(f"🔗 Usando URL fornecida: {video_path_or_url}")
            return video_path_or_url

        # Se é arquivo local
        if not os.path.exists(video_path_or_url):
            print(f"❌ Arquivo não encontrado: {video_path_or_url}")
            return None

        # Validar formato
        ext = os.path.splitext(video_path_or_url)[1].lower()
        if ext not in ['.mp4', '.mov']:
            print(f"❌ Formato inválido. Use MP4 ou MOV (encontrado: {ext})")
            return None

        # Verificar tamanho
        file_size = os.path.getsize(video_path_or_url)
        file_size_mb = file_size / (1024 * 1024)

        print(f"📹 Vídeo: {os.path.basename(video_path_or_url)}")
        print(f"📏 Tamanho: {file_size_mb:.2f} MB")

        if file_size_mb > 200:  # Catbox suporta até 200MB
            print(f"⚠️ Aviso: Arquivo grande ({file_size_mb:.2f} MB)")
            print(f"   Limite do Catbox.moe: 200 MB")

        # Fazer upload
        return self.upload_to_catbox(video_path_or_url)

    def get_cover_url(self, cover_path_or_url):
        """Obtém URL da capa (se fornecida)"""
        if not cover_path_or_url:
            return None

        # Se já é uma URL, retorna diretamente
        if cover_path_or_url.startswith("http://") or cover_path_or_url.startswith("https://"):
            return cover_path_or_url

        # Se é arquivo local
        if not os.path.exists(cover_path_or_url):
            print(f"❌ Capa não encontrada: {cover_path_or_url}")
            return None

        print(f"📤 Fazendo upload da capa: {os.path.basename(cover_path_or_url)}...")
        return self.upload_to_catbox(cover_path_or_url)

    def validate_caption(self, caption):
        """Valida a legenda"""
        if not caption:
            return True, ""

        if len(caption) > config.MEDIA_CONFIG["max_caption_length"]:
            print(config.MESSAGES["error_caption_too_long"])
            print(f"Tamanho atual: {len(caption)} caracteres")
            return False, None

        return True, caption

    def create_reel_container(self, video_url, caption="", share_to_feed=True, cover_url=None, audio_name=None):
        """Cria um container de Reel"""
        print("\n📦 Criando container do Reel...")

        params = {
            "media_type": "REELS",
            "video_url": video_url,
            "share_to_feed": "true" if share_to_feed else "false",
            "access_token": self.access_token
        }

        if caption:
            params["caption"] = caption

        if cover_url:
            params["cover_url"] = cover_url
            print(f"🖼️  Com capa personalizada")

        if audio_name:
            params["audio_name"] = audio_name
            print(f"🎵 Áudio: {audio_name}")

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

        print("\n⏳ Verificando status do Reel...")
        print("   (Vídeos podem demorar mais para processar)")

        # Para vídeos, aumentar tentativas e delay
        max_retries = config.VALIDATION_CONFIG["max_retries"] * 3  # 9 tentativas
        retry_delay = config.VALIDATION_CONFIG["retry_delay"] * 2  # 10 segundos

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
                    print("✅ Reel pronto para publicação!")
                    return True
                elif status_code == "ERROR":
                    print("❌ Erro no processamento do Reel")
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
        print("\n🚀 Publicando Reel no Instagram...")

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
            print(f"🔗 Reel publicado na conta: @{config.INSTAGRAM_USERNAME}")

            return media_id

        except Exception as e:
            print(config.MESSAGES["error_publish_failed"])
            print(f"Erro: {e}")
            return None

    def publish_reel(self, video_path, caption="", share_to_feed=True, cover_path=None, audio_name=None):
        """Método principal para publicar um Reel completo"""
        print("=" * 60)
        print("🎬 PUBLICANDO REEL NO INSTAGRAM")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"🆔 User ID: {self.user_id}")
        print(f"📤 Compartilhar no feed: {'Sim' if share_to_feed else 'Não'}")
        print("=" * 60)

        # 1. Verificar rate limit
        if not self.check_rate_limit():
            return False

        # 2. Validar legenda
        is_valid, validated_caption = self.validate_caption(caption)
        if not is_valid:
            return False

        # 3. Obter URL do vídeo
        print(f"\n📹 Processando vídeo...")
        video_url = self.get_video_url(video_path)
        if not video_url:
            return False

        # 4. Obter URL da capa (se fornecida)
        cover_url = None
        if cover_path:
            print(f"\n🖼️  Processando capa...")
            cover_url = self.get_cover_url(cover_path)
            if not cover_url:
                print("⚠️ Falha ao processar capa, continuando sem capa")

        # 5. Criar container
        container_id = self.create_reel_container(
            video_url,
            validated_caption,
            share_to_feed,
            cover_url,
            audio_name
        )
        if not container_id:
            return False

        # 6. Verificar status (pode demorar para vídeos)
        if not self.check_container_status(container_id):
            return False

        # 7. Publicar
        media_id = self.publish_media(container_id)
        if not media_id:
            return False

        print("\n" + "=" * 60)
        print("✅ REEL PUBLICADO COM SUCESSO!")
        print("=" * 60)

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Publicar Reels no Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Reel simples com arquivo local
  python3 publish_instagram_reel.py video.mp4 "Meu primeiro Reel!"

  # Reel com URL
  python3 publish_instagram_reel.py "https://exemplo.com/video.mp4" "Reel via URL"

  # Reel com capa personalizada
  python3 publish_instagram_reel.py video.mp4 "Legenda" --cover capa.jpg

  # Reel sem compartilhar no feed
  python3 publish_instagram_reel.py video.mp4 "Legenda" --no-feed

  # Reel com nome de áudio
  python3 publish_instagram_reel.py video.mp4 "Legenda" --audio "Música Original"

Requisitos de vídeo:
  - Formato: MP4 ou MOV
  - Duração: 3s - 90s
  - Tamanho: até 200 MB (limite do Catbox.moe)
  - Aspect ratio: 9:16 recomendado (vertical)
  - Rate limit: 100 posts por 24 horas
        """
    )

    parser.add_argument(
        "video",
        help="Caminho do arquivo de vídeo ou URL pública"
    )

    parser.add_argument(
        "caption",
        nargs="?",
        default="",
        help="Legenda do Reel (opcional, máximo 2200 caracteres)"
    )

    parser.add_argument(
        "--cover",
        help="Imagem de capa do Reel (arquivo local ou URL)"
    )

    parser.add_argument(
        "--no-feed",
        action="store_true",
        help="Não compartilhar no feed (apenas em Reels)"
    )

    parser.add_argument(
        "--audio",
        help="Nome do áudio/música original"
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
    publisher = InstagramReelPublisher()
    success = publisher.publish_reel(
        video_path=args.video,
        caption=args.caption,
        share_to_feed=not args.no_feed,
        cover_path=args.cover,
        audio_name=args.audio
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
