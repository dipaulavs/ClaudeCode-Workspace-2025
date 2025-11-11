#!/usr/bin/env python3
"""
Script para atualizar transcribe_universal.py com suporte a título do vídeo
"""

import sys
from pathlib import Path


def update_transcribe_universal():
    """
    Atualiza o transcribe_universal.py para usar título do vídeo
    """
    tools_path = Path(__file__).parent.parent.parent.parent.parent / "TOOLS" / "transcribe_universal.py"

    if not tools_path.exists():
        print(f"❌ Arquivo não encontrado: {tools_path}")
        return False

    # Lê conteúdo atual
    with open(tools_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Adiciona import subprocess no topo
    if 'import subprocess' not in content:
        content = content.replace(
            'from urllib.parse import quote',
            'from urllib.parse import quote\nimport subprocess'
        )

    # Adiciona função para obter título
    get_title_function = '''
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
                invalid_chars = r'[<>:"/\\\\|?*]'
                sanitized = re.sub(invalid_chars, '', title)
                sanitized = ' '.join(sanitized.split())

                # Limita tamanho
                if len(sanitized) > 100:
                    sanitized = sanitized[:100].rsplit(' ', 1)[0]

                return sanitized

        return None
    except:
        return None

'''

    # Adiciona função antes de detect_platform se não existir
    if 'def get_video_title' not in content:
        content = content.replace(
            'def detect_platform(url):',
            get_title_function + 'def detect_platform(url):'
        )

    # Atualiza função save_transcription
    old_save_function = '''def save_transcription(video_url, transcription_data, language):
    """
    Salva a transcrição em arquivo
    """
    if not transcription_data:
        return

    # Cria pasta com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    platform = detect_platform(video_url).replace('/', '-')
    output_dir = DOWNLOADS_DIR / f"transcription_{platform.lower()}_{timestamp}"
    output_dir.mkdir(exist_ok=True)'''

    new_save_function = '''def save_transcription(video_url, transcription_data, language):
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

    output_dir.mkdir(exist_ok=True)'''

    content = content.replace(old_save_function, new_save_function)

    # Atualiza nome do arquivo de transcrição
    content = content.replace(
        'transcription_file = output_dir / "transcription.txt"',
        'transcription_file = output_dir / output_filename'
    )

    # Atualiza mensagem de salvamento
    content = content.replace(
        'print(f"💾 Transcrição salva: transcription.txt")',
        'print(f"💾 Transcrição salva: {output_filename}")'
    )

    # Salva arquivo atualizado
    with open(tools_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Arquivo atualizado: {tools_path}")
    return True


if __name__ == "__main__":
    success = update_transcribe_universal()
    sys.exit(0 if success else 1)
