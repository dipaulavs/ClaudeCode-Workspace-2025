#!/usr/bin/env python3
"""
Script para extrair título de vídeos do YouTube
Usa yt-dlp para obter metadados do vídeo
"""

import sys
import subprocess
import json
import re


def sanitize_filename(title):
    """
    Remove caracteres inválidos do título para usar como nome de arquivo/pasta
    """
    # Remove caracteres inválidos para nomes de arquivo
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '', title)

    # Remove espaços extras e limita tamanho
    sanitized = ' '.join(sanitized.split())

    # Limita tamanho do nome (máx 100 caracteres)
    if len(sanitized) > 100:
        sanitized = sanitized[:100].rsplit(' ', 1)[0]

    return sanitized


def get_video_title(url):
    """
    Extrai o título do vídeo usando yt-dlp
    """
    try:
        # Usa yt-dlp para obter metadados
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
                return sanitize_filename(title)

        return None

    except subprocess.TimeoutExpired:
        print("⚠️ Timeout ao obter título do vídeo", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("⚠️ Erro ao processar metadados do vídeo", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("⚠️ yt-dlp não encontrado. Instale com: brew install yt-dlp", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️ Erro ao obter título: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 get_video_title.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    title = get_video_title(url)

    if title:
        print(title)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
