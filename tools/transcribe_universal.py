#!/usr/bin/env python3
"""
Transcritor Universal de Vídeos via RapidAPI
Transcreve vídeos de YouTube, TikTok, Instagram, LinkedIn, X/Twitter, Vimeo e arquivos locais
"""

import requests
import json
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import subprocess

# Configuração
RAPIDAPI_KEY = "82a6c38fa1msh40088bb99ac4883p1bd271jsn604d036bd581"
RAPIDAPI_HOST = "speech-to-text-ai.p.rapidapi.com"
API_URL = f"https://{RAPIDAPI_HOST}/transcribe"
DOWNLOADS_DIR = Path.home() / "Downloads"

# Plataformas suportadas
SUPPORTED_PLATFORMS = {
    'youtube.com': 'YouTube',
    'youtu.be': 'YouTube',
    'tiktok.com': 'TikTok',
    'instagram.com': 'Instagram',
    'linkedin.com': 'LinkedIn',
    'twitter.com': 'X/Twitter',
    'x.com': 'X/Twitter',
    'vimeo.com': 'Vimeo'
}


def get_video_title(url):
    """
    Extrai título do vídeo usando yt-dlp
    """
    try:
        import subprocess
        import json
        import re

        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-download', url],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            title = data.get('title', '')

            if title:
                # Sanitiza título para nome de arquivo
                invalid_chars = r'[<>:"/\\|?*]'
                sanitized = re.sub(invalid_chars, '', title)
                sanitized = ' '.join(sanitized.split())

                # Limita tamanho
                if len(sanitized) > 100:
                    sanitized = sanitized[:100].rsplit(' ', 1)[0]

                return sanitized

        return None
    except:
        return None

def detect_platform(url):
    """
    Detecta a plataforma do vídeo pela URL
    """
    url_lower = url.lower()
    for platform_key, platform_name in SUPPORTED_PLATFORMS.items():
        if platform_key in url_lower:
            return platform_name

    # Se não detectou plataforma, pode ser arquivo direto
    if url.startswith('http'):
        return 'URL direta'

    return 'Arquivo local'

def transcribe_video(video_url, language="en", task="transcribe"):
    """
    Transcreve vídeo usando a API RapidAPI
    """
    platform = detect_platform(video_url)

    print(f"🎬 Iniciando transcrição...")
    print(f"📍 Origem: {platform}")
    print(f"🔗 URL/Arquivo: {video_url}")
    print(f"🌐 Idioma: {language}")

    # Prepara headers
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Prepara URL com parâmetros
    encoded_url = quote(video_url, safe='')
    full_url = f"{API_URL}?url={encoded_url}&lang={language}&task={task}"

    print(f"\n⏳ Processando transcrição...")
    print("   (Isso pode levar alguns minutos dependendo do tamanho do vídeo...)\n")

    try:
        # Faz requisição POST
        response = requests.post(full_url, headers=headers, data={}, timeout=300)

        if response.status_code == 200:
            print("✅ Transcrição concluída!")
            return response.json()
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("❌ Timeout: A transcrição demorou muito. Tente um vídeo menor.")
        return None
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None

def save_transcription(video_url, transcription_data, language):
    """
    Salva a transcrição em arquivo usando título do vídeo
    """
    if not transcription_data:
        return

    # Tenta obter título do vídeo
    video_title = get_video_title(video_url)

    if video_title:
        # Usa título do vídeo como nome da pasta
        output_dir = DOWNLOADS_DIR / video_title
        output_filename = f"{video_title}.txt"
    else:
        # Fallback para timestamp se não conseguir título
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform = detect_platform(video_url).replace('/', '-')
        output_dir = DOWNLOADS_DIR / f"transcription_{platform.lower()}_{timestamp}"
        output_filename = "transcription.txt"

    output_dir.mkdir(exist_ok=True)

    print(f"\n📁 Salvando em: {output_dir}")

    # Extrai texto da transcrição
    transcription_text = ""

    if isinstance(transcription_data, dict):
        # Tenta diferentes formatos de resposta
        if 'text' in transcription_data:
            transcription_text = transcription_data['text']
        elif 'transcription' in transcription_data:
            transcription_text = transcription_data['transcription']
        elif 'results' in transcription_data:
            if isinstance(transcription_data['results'], list):
                transcription_text = ' '.join([item.get('text', '') for item in transcription_data['results']])
            elif isinstance(transcription_data['results'], str):
                transcription_text = transcription_data['results']

    # Salva transcrição formatada
    transcription_file = output_dir / output_filename

    with open(transcription_file, 'w', encoding='utf-8') as f:
        f.write(f"TRANSCRIÇÃO UNIVERSAL DE VÍDEO\n")
        f.write(f"=" * 60 + "\n\n")
        f.write(f"Origem: {detect_platform(video_url)}\n")
        f.write(f"URL/Arquivo: {video_url}\n")
        f.write(f"Idioma: {language}\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"\n" + "=" * 60 + "\n\n")
        f.write("TRANSCRIÇÃO:\n\n")
        f.write(transcription_text if transcription_text else str(transcription_data))
        f.write("\n")

    print(f"💾 Transcrição salva: {output_filename}")

    # Salva JSON completo
    json_file = output_dir / "transcription_full.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(transcription_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Dados completos salvos: transcription_full.json")

    # Exibe transcrição no terminal
    if transcription_text:
        print(f"\n{'=' * 60}")
        print("📝 TRANSCRIÇÃO:")
        print(f"{'=' * 60}\n")
        print(transcription_text)
        print(f"\n{'=' * 60}\n")

    print(f"\n✅ Processo completo!")
    print(f"📂 Arquivos salvos em: {output_dir}")

    return output_dir

def main():
    parser = argparse.ArgumentParser(
        description="Transcreve vídeos de múltiplas plataformas ou arquivos de áudio/vídeo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Plataformas suportadas:
  • YouTube (youtube.com, youtu.be)
  • TikTok (tiktok.com)
  • Instagram (instagram.com)
  • LinkedIn (linkedin.com)
  • X/Twitter (x.com, twitter.com)
  • Vimeo (vimeo.com)
  • URLs diretas de vídeo/áudio
  • Arquivos locais (upload automático)

Exemplos:
  # YouTube
  python3 transcribe_universal.py "https://www.youtube.com/watch?v=VIDEO_ID"

  # TikTok
  python3 transcribe_universal.py "https://www.tiktok.com/@user/video/123"

  # Instagram
  python3 transcribe_universal.py "https://www.instagram.com/reel/ABC123/"

  # Especificar idioma
  python3 transcribe_universal.py "URL" --lang pt

  # Arquivo de áudio direto
  python3 transcribe_universal.py "https://exemplo.com/audio.mp3"

Idiomas suportados:
  en (inglês), pt (português), es (espanhol), fr (francês), de (alemão),
  it (italiano), ja (japonês), ko (coreano), zh (chinês), ru (russo), etc.
        """
    )

    parser.add_argument(
        "url",
        help="URL do vídeo ou arquivo de áudio/vídeo"
    )

    parser.add_argument(
        "--lang",
        default="en",
        help="Código do idioma (padrão: en). Use 'pt' para português, 'es' para espanhol, etc."
    )

    parser.add_argument(
        "--task",
        default="transcribe",
        help="Tarefa: transcribe (padrão) ou translate"
    )

    args = parser.parse_args()

    # Transcreve
    result = transcribe_video(args.url, args.lang, args.task)

    # Salva resultado
    if result:
        save_transcription(args.url, result, args.lang)
    else:
        print("\n❌ Não foi possível completar a transcrição.")

if __name__ == "__main__":
    main()
