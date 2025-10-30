#!/usr/bin/env python3
"""
Script para gerar múltiplos áudios em lote usando a API ElevenLabs
Os áudios são salvos automaticamente na pasta Downloads
"""

import requests
import sys
import os
from datetime import datetime
from pathlib import Path
import time

# Configuração da API
API_KEY = "22b09979fe8495a6efe8053ee7c8aa5942de081781b0dbc206b218418ad4d184"
BASE_URL = "https://api.elevenlabs.io/v1"

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Voice IDs disponíveis
# Michele (padrão)
DEFAULT_VOICE_ID = "QQFzOTqaZ9W1XGSTWyBw"  # Michele - voz padrão
# Felipe (voz clonada)
FELIPE_VOICE_ID = "3QlvO7Xt2e9OCfetPOd8"  # Felipe - voz clonada


def generate_audio(text, voice_id=DEFAULT_VOICE_ID, model_id="eleven_v3",
                   output_format="mp3_44100_128"):
    """
    Gera áudio a partir de texto usando a API ElevenLabs

    Args:
        text: Texto a ser convertido em áudio
        voice_id: ID da voz a ser usada
        model_id: ID do modelo
        output_format: Formato de saída

    Returns:
        Dados do áudio se sucesso, None se erro
    """
    url = f"{BASE_URL}/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }

    params = {
        "output_format": output_format,
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        }
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        return response.content

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalhes: {e.response.text}")
        return None


def save_audio(audio_data, index, total):
    """
    Salva o áudio na pasta Downloads

    Args:
        audio_data: Dados binários do áudio
        index: Índice do áudio
        total: Total de áudios

    Returns:
        Caminho do arquivo salvo
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_batch_{timestamp}_{index:02d}_of_{total:02d}.mp3"
        output_path = os.path.join(DOWNLOADS_PATH, filename)

        with open(output_path, 'wb') as f:
            f.write(audio_data)

        file_size = len(audio_data) / 1024  # KB
        print(f"  💾 Salvo: {filename} ({file_size:.2f} KB)")

        return output_path

    except Exception as e:
        print(f"  ❌ Erro ao salvar: {e}")
        return None


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python3 generate_audio_batch_elevenlabs.py \"texto1\" \"texto2\" \"texto3\" ... [opções]")
        print("\nOpções:")
        print("  --voice ID     ID da voz (padrão: JBFqnCBsd6RMkjVDRZzb)")
        print("  --model ID     ID do modelo (padrão: eleven_multilingual_v2)")
        print("  --delay SECS   Delay entre requisições em segundos (padrão: 1)")
        print("\nExemplo:")
        print('  python3 generate_audio_batch_elevenlabs.py "Olá mundo" "Como vai?" "Até logo"')
        print(f"\nÁudios serão salvos em: {DOWNLOADS_PATH}")
        sys.exit(1)

    # Separa textos de opções
    texts = []
    voice_id = DEFAULT_VOICE_ID
    model_id = "eleven_v3"
    delay = 1.0

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--voice" and i + 1 < len(sys.argv):
            # Permite usar "felipe" como atalho
            if sys.argv[i + 1].lower() == "felipe":
                voice_id = FELIPE_VOICE_ID
            else:
                voice_id = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model_id = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--delay" and i + 1 < len(sys.argv):
            try:
                delay = float(sys.argv[i + 1])
            except ValueError:
                print("⚠️  Valor de delay inválido. Usando 1 segundo.")
            i += 2
        else:
            texts.append(sys.argv[i])
            i += 1

    if not texts:
        print("❌ Nenhum texto fornecido!")
        sys.exit(1)

    print(f"\n🎙️  Gerando {len(texts)} áudio(s) em lote...")
    print(f"🎤 Voice ID: {voice_id}")
    print(f"🤖 Model: {model_id}")
    print(f"⏱️  Delay entre requisições: {delay}s\n")

    successful = 0
    failed = 0
    saved_files = []

    for i, text in enumerate(texts, 1):
        print(f"[{i}/{len(texts)}] 📝 Texto: {text[:60]}{'...' if len(text) > 60 else ''}")

        # Gera o áudio
        audio_data = generate_audio(text, voice_id=voice_id, model_id=model_id)

        if audio_data:
            # Salva o áudio
            output_path = save_audio(audio_data, i, len(texts))
            if output_path:
                successful += 1
                saved_files.append(output_path)
            else:
                failed += 1
        else:
            failed += 1

        # Delay entre requisições (exceto na última)
        if i < len(texts):
            print(f"  ⏳ Aguardando {delay}s...\n")
            time.sleep(delay)

    # Resumo final
    print("\n" + "="*60)
    print("✨ RESUMO DO LOTE")
    print("="*60)
    print(f"✅ Sucesso: {successful}/{len(texts)}")
    if failed > 0:
        print(f"❌ Falhas: {failed}/{len(texts)}")
    print(f"\n📂 Áudios salvos em: {DOWNLOADS_PATH}")

    if saved_files:
        print("\n📋 Arquivos gerados:")
        for filepath in saved_files:
            filename = os.path.basename(filepath)
            print(f"  • {filename}")

    print("\n✨ Concluído!")


if __name__ == "__main__":
    main()
