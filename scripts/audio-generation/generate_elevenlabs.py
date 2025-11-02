#!/usr/bin/env python3
"""
Template para geração de áudio com ElevenLabs (TTS único)

Uso rápido:
    python3 scripts/audio-generation/generate_elevenlabs.py "Seu texto aqui"

Funcionalidades:
    - Gera áudio de alta qualidade com ElevenLabs
    - Salva automaticamente em ~/Downloads
    - Suporte a múltiplas vozes (Michele padrão, Felipe clonada)
    - Configurações avançadas (formato, estabilidade, similaridade)
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório tools ao path para importar a ferramenta original
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../tools'))

from generate_audio_elevenlabs import (
    generate_audio,
    save_audio,
    list_voices,
    DEFAULT_VOICE_ID,
    FELIPE_VOICE_ID,
    OUTPUT_FORMATS,
    DOWNLOADS_PATH
)


def main():
    """Template simplificado para geração de áudio único"""
    if len(sys.argv) < 2:
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║          🎤 GERAÇÃO DE ÁUDIO - ELEVENLABS (TTS ÚNICO)         ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print("📖 USO BÁSICO:")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py "Seu texto aqui"')
        print()
        print("📖 USO AVANÇADO:")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py "Texto" [opções]')
        print()
        print("⚙️  OPÇÕES DISPONÍVEIS:")
        print("   --voice ID           ID da voz ou 'felipe' para voz clonada")
        print("                        (padrão: Michele)")
        print()
        print("   --model ID           Modelo a usar:")
        print("                        • eleven_v3 (padrão, mais recente)")
        print("                        • eleven_multilingual_v2")
        print("                        • eleven_turbo_v2 (mais rápido)")
        print()
        print("   --format FORMAT      Qualidade do áudio:")
        print("                        • mp3_low (menor arquivo)")
        print("                        • mp3_medium")
        print("                        • mp3_high (padrão, recomendado)")
        print("                        • mp3_ultra (máxima qualidade)")
        print("                        • pcm (sem compressão)")
        print()
        print("   --stability VALOR    Controle de estabilidade (0.0 a 1.0)")
        print("                        • Baixo (0.2-0.4): Mais variação emocional")
        print("                        • Médio (0.5): Padrão balanceado")
        print("                        • Alto (0.7-0.9): Mais consistente")
        print()
        print("   --similarity VALOR   Similaridade com voz original (0.0 a 1.0)")
        print("                        • Padrão: 0.75 (recomendado)")
        print()
        print("   --output ARQUIVO     Nome do arquivo de saída")
        print("                        (extensão .mp3 adicionada automaticamente)")
        print()
        print("   --list-voices        Lista todas as vozes disponíveis na conta")
        print()
        print("📋 EXEMPLOS PRÁTICOS:")
        print()
        print("   # Básico (voz padrão Michele)")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py "Olá, como vai?"')
        print()
        print("   # Com voz clonada Felipe")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py "Teste" --voice felipe')
        print()
        print("   # Alta qualidade com nome personalizado")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py "Mensagem importante" \\')
        print('       --format mp3_ultra --output mensagem_importante')
        print()
        print("   # Voz mais expressiva (baixa estabilidade)")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py "História emocionante" \\')
        print('       --stability 0.3 --similarity 0.8')
        print()
        print("   # Listar vozes disponíveis")
        print('   python3 scripts/audio-generation/generate_elevenlabs.py --list-voices')
        print()
        print("💡 DICAS:")
        print("   • Textos mais longos funcionam bem (até ~5000 caracteres)")
        print("   • Use pontuação para controlar pausas e entonação")
        print("   • Para múltiplos áudios, use batch_generate.py (mais rápido)")
        print("   • Áudios são salvos automaticamente em ~/Downloads")
        print()
        print(f"📂 Destino dos áudios: {DOWNLOADS_PATH}")
        print()
        sys.exit(1)

    # Se for --list-voices, executa e sai
    if "--list-voices" in sys.argv:
        print("\n🎤 Listando vozes disponíveis na conta ElevenLabs...\n")
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
                print("🎤 Usando voz clonada: Felipe")
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
        print("\n❌ Falha ao gerar áudio!")
        sys.exit(1)

    # Salva o áudio
    output_path = save_audio(audio_data, output_filename)

    if not output_path:
        print("\n❌ Falha ao salvar áudio!")
        sys.exit(1)

    print("\n✨ Concluído com sucesso!")
    print(f"📂 Áudio disponível em: {output_path}")


if __name__ == "__main__":
    main()
