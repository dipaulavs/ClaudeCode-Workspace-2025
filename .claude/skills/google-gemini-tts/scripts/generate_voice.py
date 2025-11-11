#!/usr/bin/env python3
"""
Google Gemini TTS - Geração de voz conversacional realista
Gera áudio natural com tom casual de conversa entre amigos/podcast informal
"""

import os
import sys
import wave
import argparse
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Erro: biblioteca google-genai não instalada")
    print("Execute: pip install google-genai")
    sys.exit(1)


# Vozes ideais para tom conversacional casual
CASUAL_VOICES = {
    'male': {
        'default': 'Puck',  # Upbeat mas não artificial
        'alternatives': ['Zubenelgenubi', 'Achird', 'Umbriel']  # Casual, Friendly, Easy-going
    },
    'female': {
        'default': 'Callirrhoe',  # Easy-going
        'alternatives': ['Aoede', 'Vindemiatrix', 'Zephyr']  # Breezy, Gentle, Bright
    }
}


def add_conversational_style(text: str) -> str:
    """
    Adiciona marcadores de conversa casual ao texto
    - Pausas naturais (respiração, pensamento)
    - Tom de conversa telefônica entre amigos
    """
    # Adicionar pausas curtas em vírgulas e pontos
    styled_text = text.replace(',', ', [short pause]')
    styled_text = styled_text.replace('.', '. [short pause]')
    styled_text = styled_text.replace('?', '? [short pause]')
    styled_text = styled_text.replace('!', '! [short pause]')

    # Adicionar suspiros/respirações ocasionais (cada ~3 frases)
    sentences = styled_text.split('. ')
    for i in range(2, len(sentences), 3):
        if i < len(sentences):
            sentences[i] = f"[short pause] {sentences[i]}"

    return '. '.join(sentences)


def save_wav(filename: str, pcm_data: bytes, rate: int = 24000) -> None:
    """Salva áudio PCM como arquivo WAV"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(rate)  # 24kHz
        wf.writeframes(pcm_data)


def generate_casual_voice(
    text: str,
    output_file: str,
    voice: str = None,
    gender: str = 'male',
    api_key: str = None,
    model: str = 'gemini-2.5-flash-preview-tts',
    add_style: bool = True
) -> str:
    """
    Gera áudio com tom conversacional casual

    Args:
        text: Texto para converter em voz
        output_file: Caminho do arquivo de saída (.wav)
        voice: Nome da voz (padrão: voz casual do gênero escolhido)
        gender: 'male' ou 'female' (padrão: male)
        api_key: API key do Google Gemini (padrão: env GEMINI_API_KEY)
        model: Modelo TTS (padrão: gemini-2.5-flash-preview-tts)
        add_style: Adicionar pausas/respirações automáticas (padrão: True)

    Returns:
        Caminho do arquivo gerado
    """
    # API Key
    if api_key is None:
        api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        raise ValueError(
            "API key não encontrada. "
            "Defina GEMINI_API_KEY ou passe via --api-key"
        )

    # Voz padrão casual
    if voice is None:
        voice = CASUAL_VOICES[gender]['default']

    # Adicionar estilo conversacional ao texto
    if add_style:
        processed_text = add_conversational_style(text)
    else:
        processed_text = text

    # Prompt conversacional casual (telefone/podcast informal)
    prompt = (
        "Fale de forma super casual e natural, como uma conversa entre amigos no telefone. "
        "Sem energia exagerada de locutor, sem tom robótico alegre demais. "
        "Tom relaxado, pausas naturais, como quem está conversando descontraído. "
        f"Texto: {processed_text}"
    )

    # Cliente Gemini
    client = genai.Client(api_key=api_key)

    # Gerar áudio
    response = client.models.generate_content(
        model=model,
        contents=prompt,
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

    # Extrair e salvar áudio
    audio_data = response.candidates[0].content.parts[0].inline_data.data
    save_wav(output_file, audio_data)

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Gera voz conversacional casual com Google Gemini TTS'
    )
    parser.add_argument(
        'text',
        help='Texto para converter em voz'
    )
    parser.add_argument(
        '-o', '--output',
        default='output.wav',
        help='Arquivo de saída (padrão: output.wav)'
    )
    parser.add_argument(
        '-v', '--voice',
        help='Nome da voz (padrão: voz casual do gênero escolhido)'
    )
    parser.add_argument(
        '-g', '--gender',
        choices=['male', 'female'],
        default='male',
        help='Gênero da voz (padrão: male)'
    )
    parser.add_argument(
        '--api-key',
        help='Google Gemini API key (padrão: env GEMINI_API_KEY)'
    )
    parser.add_argument(
        '--model',
        default='gemini-2.5-flash-preview-tts',
        choices=['gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts'],
        help='Modelo TTS (padrão: flash)'
    )
    parser.add_argument(
        '--no-style',
        action='store_true',
        help='Não adicionar pausas/respirações automáticas'
    )
    parser.add_argument(
        '--list-voices',
        action='store_true',
        help='Listar vozes casuais recomendadas'
    )

    args = parser.parse_args()

    # Listar vozes
    if args.list_voices:
        print("\n🎤 Vozes Conversacionais Casual:")
        print("\n👨 Masculinas:")
        print(f"  • {CASUAL_VOICES['male']['default']} (padrão)")
        for v in CASUAL_VOICES['male']['alternatives']:
            print(f"  • {v}")
        print("\n👩 Femininas:")
        print(f"  • {CASUAL_VOICES['female']['default']} (padrão)")
        for v in CASUAL_VOICES['female']['alternatives']:
            print(f"  • {v}")
        print()
        return

    # Gerar áudio
    try:
        print(f"🎙️  Gerando voz conversacional casual...")
        print(f"📝 Texto: {args.text[:50]}{'...' if len(args.text) > 50 else ''}")
        print(f"🎤 Voz: {args.voice or CASUAL_VOICES[args.gender]['default']} ({args.gender})")
        print(f"🤖 Modelo: {args.model}")

        output = generate_casual_voice(
            text=args.text,
            output_file=args.output,
            voice=args.voice,
            gender=args.gender,
            api_key=args.api_key,
            model=args.model,
            add_style=not args.no_style
        )

        file_size = Path(output).stat().st_size / 1024  # KB
        print(f"\n✅ Áudio gerado com sucesso!")
        print(f"📁 Arquivo: {output}")
        print(f"📊 Tamanho: {file_size:.1f} KB")

    except Exception as e:
        print(f"\n❌ Erro ao gerar áudio: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
