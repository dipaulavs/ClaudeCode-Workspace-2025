#!/usr/bin/env python3
"""
Google Gemini TTS - Geração de Voz Conversacional Realista
Gera áudio com voz natural e casual usando Google Gemini 2.5 TTS
"""

import os
import sys
import argparse
import subprocess
import wave
from google import genai
from google.genai import types

# API Key padrão
DEFAULT_API_KEY = "AIzaSyAz2Jbiir_0-D3RvQGPk-e5Mb4HzvlerXA"

# Vozes casuais por gênero
CASUAL_VOICES = {
    'male': ['Puck', 'Zubenelgenubi', 'Achird'],
    'female': ['Callirrhoe', 'Aoede', 'Vindemiatrix']
}

# Vozes neutras/sérias (tom baixo, sem empolgação)
NEUTRAL_VOICES = {
    'male': ['Charon', 'Kore'],
    'female': ['Kore', 'Charon']  # Vozes mais neutras e profissionais
}

# Vozes para podcast (tom reflexivo, levemente cansado/grave)
PODCAST_VOICES = {
    'male': ['Charon', 'Kore'],  # Vozes mais graves e sérias
    'female': ['Kore', 'Charon']  # Tom reflexivo e natural
}

ALL_VOICES = {
    'male': ['Puck', 'Charon', 'Kore', 'Fenrir', 'Aoede'],
    'female': ['Puck', 'Charon', 'Kore', 'Callirrhoe', 'Aoede', 'Vindemiatrix']
}

def adjust_text_gender(text: str, gender: str) -> str:
    """
    Ajusta o texto para refletir a perspectiva de gênero correto
    """
    if gender == 'female':
        # Ajustes para perspectiva feminina
        replacements = {
            'nervoso': 'nervosa',
            'Nervoso': 'Nervosa',
            'empolgado': 'empolgada',
            'Empolgado': 'Empolgada',
            'animado': 'animada',
            'Animado': 'Animada',
            'cansado': 'cansada',
            'Cansado': 'Cansada',
            'preocupado': 'preocupada',
            'Preocupado': 'Preocupada',
            'feliz demais': 'feliz demais',
            'estressado': 'estressada',
            'Estressado': 'Estressada'
        }
        for male, female in replacements.items():
            text = text.replace(male, female)

    return text

def add_conversational_style(text: str, tone: str = 'casual') -> str:
    """
    Adiciona pausas naturais e estilo conversacional ao texto
    """
    if tone == 'podcast':
        # Podcast: tom natural, quase triste, com leves prolongamentos
        import re

        styled = text

        # Prolongamentos sutis apenas em algumas palavras (não todas)
        styled = styled.replace('Passei', 'Passei tipo')
        styled = styled.replace(' e ', ', eee ')
        styled = styled.replace('Até que', 'Aí... até que')
        styled = styled.replace('perdi', 'perdi, tipo,')
        styled = styled.replace('problema', 'problema, sabe,')

        # Mantém naturalidade sem exagerar
        styled = styled.replace('...', '...')
        styled = styled.replace('.', '.')

        return styled

    else:
        # Casual/Neutral: pausas curtas padrão
        styled = text.replace(',', ', [short pause]')
        styled = styled.replace('.', '. [short pause]')
        styled = styled.replace('?', '? [short pause]')
        styled = styled.replace('!', '! [short pause]')

    # Remove pausas duplas
    styled = styled.replace('[short pause] [short pause]', '[short pause]')
    styled = styled.replace('[PAUSE=0.5s] [PAUSE=0.5s]', '[PAUSE=0.5s]')

    return styled

def convert_to_mp3(wav_file: str, mp3_file: str, bitrate: str = '128k'):
    """Converte WAV para MP3 usando ffmpeg"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-i', wav_file, '-codec:a', 'libmp3lame', '-b:a', bitrate, '-y', mp3_file],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Erro ao converter para MP3: {e.stderr}")
        return False
    except FileNotFoundError:
        print("⚠️  ffmpeg não encontrado. Mantendo formato WAV.")
        return False

def generate_casual_voice(
    text: str,
    output_file: str = "output.mp3",
    voice: str = None,
    gender: str = 'male',
    api_key: str = None,
    model: str = 'gemini-2.5-flash-preview-tts',
    add_style: bool = True,
    output_format: str = 'mp3',
    tone: str = 'casual'
):
    """
    Gera áudio com voz conversacional casual

    Args:
        text: Texto para converter em voz
        output_file: Caminho do arquivo de saída
        voice: Nome da voz específica (opcional)
        gender: 'male' ou 'female' para seleção automática
        api_key: Google API key (usa env GEMINI_API_KEY se None)
        model: Modelo Gemini TTS
        add_style: Adicionar pausas automáticas
        output_format: 'mp3' (default) ou 'wav'
        tone: 'casual' (empolgado) ou 'neutral' (sério, sem empolgação)
    """
    # Obter API key
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY', DEFAULT_API_KEY)

    # Configurar cliente
    client = genai.Client(api_key=api_key)

    # Selecionar voz baseado no tom
    if not voice:
        if tone == 'podcast':
            voice = PODCAST_VOICES[gender][0]  # Voz para podcast
        elif tone == 'neutral':
            voice = NEUTRAL_VOICES[gender][0]  # Voz neutra/séria
        else:
            voice = CASUAL_VOICES[gender][0]  # Voz casual

    # Ajustar texto para perspectiva de gênero
    adjusted_text = adjust_text_gender(text, gender)

    # Adicionar estilo conversacional
    if add_style:
        styled_text = add_conversational_style(adjusted_text, tone)
    else:
        styled_text = adjusted_text

    # Prompt baseado no tom
    if tone == 'podcast':
        conversational_prompt = f"""Você está falando RÁPIDO mas com tom sério e levemente melancólico.
Tom baixo, meio cansado, sem empolgação - mas fale num ritmo acelerado e natural.
Voz grave e suave, como quem está desabafando rapidamente pra alguém.
NÃO seja alegre, NÃO seja empolgada - seja neutra/triste mas RÁPIDA.
Ritmo acelerado de conversa fluida, sem pausas longas.
Fale rápido como se estivesse contando algo de forma direta e sem enrolação.

{styled_text}"""
    elif tone == 'neutral':
        conversational_prompt = f"Fale de forma neutra e natural, como se estivesse gravando um áudio de voz no celular. Tom sério, sem empolgação ou entonação exagerada. Não pareça um locutor, apenas uma pessoa normal falando: {styled_text}"
    else:
        conversational_prompt = f"Fale de forma natural e casual, como uma conversa entre amigos ao telefone: {styled_text}"

    print(f"🎙️  Gerando áudio com voz {voice} ({gender})...")
    print(f"📝 Texto: {text[:100]}{'...' if len(text) > 100 else ''}")

    # Calcular custo aproximado
    cost = 0.005 if model == 'gemini-2.5-flash-preview-tts' else 0.015
    print(f"💰 Custo estimado: ${cost:.4f} USD (~R$ {cost * 6:.4f})")

    # Gerar áudio
    response = client.models.generate_content(
        model=model,
        contents=conversational_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice
                    )
                )
            )
        )
    )

    # Salvar áudio
    audio_data = b''
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            audio_data += part.inline_data.data

    # Expandir ~ para caminho home
    output_path = os.path.expanduser(output_file)

    # Garantir extensão correta
    if output_format == 'mp3' and not output_path.endswith('.mp3'):
        output_path = output_path.rsplit('.', 1)[0] + '.mp3'
    elif output_format == 'wav' and not output_path.endswith('.wav'):
        output_path = output_path.rsplit('.', 1)[0] + '.wav'

    # Salvar WAV temporário (API retorna PCM raw, precisa criar WAV válido)
    if output_format == 'mp3':
        temp_wav = output_path.rsplit('.', 1)[0] + '_temp.wav'

        # Criar WAV válido com header correto
        with wave.open(temp_wav, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(24000)  # 24kHz
            wav_file.writeframes(audio_data)

        # Converter para MP3
        if convert_to_mp3(temp_wav, output_path):
            os.remove(temp_wav)
            file_size = os.path.getsize(output_path) / 1024
            print(f"✅ Áudio salvo: {output_path}")
            print(f"📊 Formato: MP3 | Tamanho: {file_size:.1f} KB")
        else:
            # Fallback para WAV se conversão falhar
            os.rename(temp_wav, output_path.rsplit('.', 1)[0] + '.wav')
            print(f"✅ Áudio salvo: {output_path.rsplit('.', 1)[0] + '.wav'} (WAV)")
            print(f"📊 Tamanho: {len(audio_data) / 1024:.1f} KB")
    else:
        # Salvar WAV diretamente com header correto
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(24000)  # 24kHz
            wav_file.writeframes(audio_data)

        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Áudio salvo: {output_path}")
        print(f"📊 Formato: WAV | Tamanho: {file_size:.1f} KB")

    return output_path

def list_voices():
    """Lista todas as vozes disponíveis"""
    print("\n🎙️  Vozes Casuais (Conversação Natural):\n")

    print("👨 MASCULINAS:")
    for voice in CASUAL_VOICES['male']:
        print(f"  - {voice}")

    print("\n👩 FEMININAS:")
    for voice in CASUAL_VOICES['female']:
        print(f"  - {voice}")

    print("\n💡 Uso: python3 generate_voice.py 'texto' -v Puck")

def main():
    parser = argparse.ArgumentParser(
        description='Google Gemini TTS - Voz Conversacional Casual (MP3 por padrão)'
    )

    parser.add_argument('text', nargs='?', help='Texto para converter em voz')
    parser.add_argument('-o', '--output', default='output.mp3', help='Arquivo de saída (padrão: output.mp3)')
    parser.add_argument('-v', '--voice', help='Nome da voz específica')
    parser.add_argument('-g', '--gender', choices=['male', 'female'], default='male', help='Gênero da voz')
    parser.add_argument('-t', '--tone', choices=['casual', 'neutral', 'podcast'], default='casual', help='Tom: casual (empolgado), neutral (sério), ou podcast (reflexivo/pensativo)')
    parser.add_argument('-m', '--model', default='gemini-2.5-flash-preview-tts', help='Modelo Gemini')
    parser.add_argument('-f', '--format', choices=['mp3', 'wav'], default='mp3', help='Formato de saída (padrão: mp3)')
    parser.add_argument('--api-key', help='Google API Key')
    parser.add_argument('--no-style', action='store_true', help='Não adicionar pausas automáticas')
    parser.add_argument('--list-voices', action='store_true', help='Listar vozes disponíveis')

    args = parser.parse_args()

    if args.list_voices:
        list_voices()
        return

    if not args.text:
        parser.print_help()
        print("\n❌ Erro: Texto obrigatório")
        sys.exit(1)

    try:
        generate_casual_voice(
            text=args.text,
            output_file=args.output,
            voice=args.voice,
            gender=args.gender,
            api_key=args.api_key,
            model=args.model,
            add_style=not args.no_style,
            output_format=args.format,
            tone=args.tone
        )
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
