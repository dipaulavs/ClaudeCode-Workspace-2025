#!/usr/bin/env python3
"""
Script para gerar áudio usando a API ElevenLabs Text-to-Speech
Os áudios são salvos automaticamente na pasta Downloads
"""

import requests
import sys
import os
from datetime import datetime
from pathlib import Path

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

# Configurações de output
OUTPUT_FORMATS = {
    "mp3_low": "mp3_22050_32",
    "mp3_medium": "mp3_44100_64",
    "mp3_high": "mp3_44100_128",
    "mp3_ultra": "mp3_44100_192",
    "pcm": "pcm_44100",
}


def list_voices():
    """
    Lista todas as vozes disponíveis na conta

    Returns:
        Lista de vozes ou None se erro
    """
    url = f"{BASE_URL}/voices"
    headers = {
        "xi-api-key": API_KEY,
    }

    try:
        print("\n🎤 Consultando vozes disponíveis...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        voices = data.get("voices", [])

        if voices:
            print(f"\n✅ {len(voices)} voz(es) disponível(is):\n")
            for voice in voices:
                voice_id = voice.get("voice_id", "N/A")
                name = voice.get("name", "N/A")
                category = voice.get("category", "N/A")
                labels = voice.get("labels", {})

                print(f"  • {name}")
                print(f"    ID: {voice_id}")
                print(f"    Categoria: {category}")
                if labels:
                    print(f"    Labels: {labels}")
                print()

            return voices
        else:
            print("⚠️  Nenhuma voz disponível")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao consultar vozes: {e}")
        return None


def generate_audio(text, voice_id=DEFAULT_VOICE_ID, model_id="eleven_v3",
                   output_format="mp3_high", stability=0.5, similarity_boost=0.75):
    """
    Gera áudio a partir de texto usando a API ElevenLabs

    Args:
        text: Texto a ser convertido em áudio
        voice_id: ID da voz a ser usada
        model_id: ID do modelo (eleven_multilingual_v2, eleven_monolingual_v1, etc)
        output_format: Formato de saída (mp3_low, mp3_medium, mp3_high, mp3_ultra, pcm)
        stability: Estabilidade da voz (0.0 a 1.0)
        similarity_boost: Aumento de similaridade (0.0 a 1.0)

    Returns:
        Dados do áudio se sucesso, None se erro
    """
    # Converte formato legível para formato da API
    format_code = OUTPUT_FORMATS.get(output_format, OUTPUT_FORMATS["mp3_high"])

    url = f"{BASE_URL}/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }

    params = {
        "output_format": format_code,
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        }
    }

    print(f"\n🎙️  Gerando áudio...")
    print(f"📝 Texto: {text[:100]}{'...' if len(text) > 100 else ''}")
    print(f"🎤 Voice ID: {voice_id}")
    print(f"🤖 Model: {model_id}")
    print(f"🔊 Formato: {output_format} ({format_code})")

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()

        print(f"✅ Áudio gerado com sucesso!")
        return response.content

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalhes: {e.response.text}")
        return None


def save_audio(audio_data, filename=None):
    """
    Salva o áudio na pasta Downloads

    Args:
        audio_data: Dados binários do áudio
        filename: Nome do arquivo (opcional)

    Returns:
        Caminho do arquivo salvo
    """
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_audio_{timestamp}.mp3"

        output_path = os.path.join(DOWNLOADS_PATH, filename)

        print(f"\n💾 Salvando áudio...")
        with open(output_path, 'wb') as f:
            f.write(audio_data)

        file_size = len(audio_data) / 1024  # KB
        print(f"✅ Áudio salvo em: {output_path}")
        print(f"📊 Tamanho: {file_size:.2f} KB")

        return output_path

    except Exception as e:
        print(f"❌ Erro ao salvar áudio: {e}")
        return None


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python3 generate_audio_elevenlabs.py \"seu texto aqui\" [opções]")
        print("\nOpções:")
        print("  --voice ID           ID da voz (padrão: JBFqnCBsd6RMkjVDRZzb)")
        print("  --model ID           ID do modelo (padrão: eleven_multilingual_v2)")
        print("  --format FORMAT      Formato de saída:")
        print("                       mp3_low, mp3_medium, mp3_high (padrão), mp3_ultra, pcm")
        print("  --stability VALOR    Estabilidade 0.0-1.0 (padrão: 0.5)")
        print("  --similarity VALOR   Similaridade 0.0-1.0 (padrão: 0.75)")
        print("  --output ARQUIVO     Nome do arquivo de saída")
        print("  --list-voices        Lista todas as vozes disponíveis")
        print("\nModelos disponíveis:")
        print("  - eleven_multilingual_v2 (padrão, suporta português)")
        print("  - eleven_monolingual_v1")
        print("  - eleven_turbo_v2")
        print("\nExemplos:")
        print('  python3 generate_audio_elevenlabs.py "Olá, como vai você?"')
        print('  python3 generate_audio_elevenlabs.py "Hello world" --format mp3_ultra')
        print('  python3 generate_audio_elevenlabs.py "Test" --voice VOICE_ID --stability 0.7')
        print('  python3 generate_audio_elevenlabs.py --list-voices')
        print(f"\nÁudios serão salvos em: {DOWNLOADS_PATH}")
        sys.exit(1)

    # Verifica se é para listar vozes
    if "--list-voices" in sys.argv:
        list_voices()
        sys.exit(0)

    # Parse dos argumentos
    text = sys.argv[1]
    voice_id = DEFAULT_VOICE_ID
    model_id = "eleven_v3"
    output_format = "mp3_high"
    stability = 0.5
    similarity_boost = 0.75
    output_filename = None

    # Processa argumentos opcionais
    i = 2
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
        elif sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1]
            if output_format not in OUTPUT_FORMATS:
                print(f"⚠️  Formato inválido: {output_format}. Usando mp3_high.")
                output_format = "mp3_high"
            i += 2
        elif sys.argv[i] == "--stability" and i + 1 < len(sys.argv):
            try:
                stability = float(sys.argv[i + 1])
                stability = max(0.0, min(1.0, stability))
            except ValueError:
                print("⚠️  Valor de stability inválido. Usando 0.5.")
            i += 2
        elif sys.argv[i] == "--similarity" and i + 1 < len(sys.argv):
            try:
                similarity_boost = float(sys.argv[i + 1])
                similarity_boost = max(0.0, min(1.0, similarity_boost))
            except ValueError:
                print("⚠️  Valor de similarity inválido. Usando 0.75.")
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_filename = sys.argv[i + 1]
            if not output_filename.endswith('.mp3'):
                output_filename += '.mp3'
            i += 2
        else:
            i += 1

    # Gera o áudio
    audio_data = generate_audio(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost
    )

    if not audio_data:
        sys.exit(1)

    # Salva o áudio
    output_path = save_audio(audio_data, output_filename)

    if not output_path:
        sys.exit(1)

    print("\n✨ Concluído!")
    print(f"📂 Áudio disponível em: {output_path}")


if __name__ == "__main__":
    main()
