#!/usr/bin/env python3
"""
Template para geração de múltiplos áudios em lote com ElevenLabs

Uso rápido:
    python3 scripts/audio-generation/batch_generate.py "texto1" "texto2" "texto3"

Funcionalidades:
    - Gera múltiplos áudios em sequência
    - Nomeação automática com índice (01_of_03, 02_of_03, etc.)
    - Resumo final com estatísticas
    - Delay configurável entre requisições
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório tools ao path para importar a ferramenta original
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../tools'))

from generate_audio_batch_elevenlabs import (
    generate_audio,
    save_audio,
    DEFAULT_VOICE_ID,
    FELIPE_VOICE_ID,
    DOWNLOADS_PATH
)
import time


def main():
    """Template simplificado para geração de áudios em lote"""
    if len(sys.argv) < 2:
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║        🎤 GERAÇÃO DE ÁUDIO EM LOTE - ELEVENLABS (TTS)        ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print("📖 USO BÁSICO:")
        print('   python3 scripts/audio-generation/batch_generate.py "texto1" "texto2" "texto3"')
        print()
        print("📖 USO AVANÇADO:")
        print('   python3 scripts/audio-generation/batch_generate.py "texto1" "texto2" [opções]')
        print()
        print("⚙️  OPÇÕES DISPONÍVEIS:")
        print("   --voice ID      ID da voz ou 'felipe' para voz clonada")
        print("                   (padrão: Michele)")
        print()
        print("   --model ID      Modelo a usar:")
        print("                   • eleven_v3 (padrão, mais recente)")
        print("                   • eleven_multilingual_v2")
        print("                   • eleven_turbo_v2 (mais rápido)")
        print()
        print("   --delay SECS    Tempo de espera entre requisições em segundos")
        print("                   (padrão: 1.0, mínimo recomendado: 0.5)")
        print()
        print("📋 EXEMPLOS PRÁTICOS:")
        print()
        print("   # Básico - 3 áudios com voz padrão")
        print('   python3 scripts/audio-generation/batch_generate.py \\')
        print('       "Olá, mundo!" "Como vai?" "Até logo!"')
        print()
        print("   # Com voz clonada Felipe")
        print('   python3 scripts/audio-generation/batch_generate.py \\')
        print('       "Primeiro áudio" "Segundo áudio" --voice felipe')
        print()
        print("   # Múltiplos áudios sem delay (mais rápido, cuidado com rate limit)")
        print('   python3 scripts/audio-generation/batch_generate.py \\')
        print('       "Audio 1" "Audio 2" "Audio 3" --delay 0')
        print()
        print("   # Com delay maior (mais seguro para muitos áudios)")
        print('   python3 scripts/audio-generation/batch_generate.py \\')
        print('       "Um" "Dois" "Três" "Quatro" "Cinco" --delay 2')
        print()
        print("💡 DICAS:")
        print("   • Para 2+ áudios, SEMPRE use este script (batch)")
        print("   • Evite delays muito baixos para não exceder rate limits")
        print("   • Arquivos salvos com numeração automática (01_of_03, 02_of_03...)")
        print("   • Para áudio único, use generate_elevenlabs.py")
        print("   • Resumo final mostra estatísticas e lista de arquivos gerados")
        print()
        print("⚠️  AVISOS:")
        print("   • Cada requisição consome créditos da API ElevenLabs")
        print("   • Respeite os rate limits da API (delay mínimo 0.5s recomendado)")
        print("   • Em caso de erro em um áudio, o script continua os demais")
        print()
        print(f"📂 Destino dos áudios: {DOWNLOADS_PATH}")
        print()
        sys.exit(1)

    # Separa textos de opções
    texts = []
    voice_id = DEFAULT_VOICE_ID
    model_id = "eleven_v3"
    delay = 1.0
    voice_name = "Michele (padrão)"

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--voice" and i + 1 < len(sys.argv):
            # Permite usar "felipe" como atalho
            if sys.argv[i + 1].lower() == "felipe":
                voice_id = FELIPE_VOICE_ID
                voice_name = "Felipe (clonada)"
            else:
                voice_id = sys.argv[i + 1]
                voice_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model_id = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--delay" and i + 1 < len(sys.argv):
            try:
                delay = float(sys.argv[i + 1])
                if delay < 0:
                    print("⚠️  Delay não pode ser negativo. Usando 0.")
                    delay = 0
            except ValueError:
                print("⚠️  Valor de delay inválido. Usando 1 segundo.")
            i += 2
        else:
            texts.append(sys.argv[i])
            i += 1

    if not texts:
        print("❌ Nenhum texto fornecido!")
        print("💡 Use: python3 scripts/audio-generation/batch_generate.py \"texto1\" \"texto2\" ...")
        sys.exit(1)

    # Cabeçalho da execução
    print("\n" + "="*70)
    print(f"🎙️  GERANDO {len(texts)} ÁUDIO(S) EM LOTE")
    print("="*70)
    print(f"🎤 Voz: {voice_name}")
    print(f"🤖 Modelo: {model_id}")
    print(f"⏱️  Delay: {delay}s entre requisições")
    print(f"📂 Destino: {DOWNLOADS_PATH}")
    print("="*70 + "\n")

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
                print("  ✅ Sucesso!")
            else:
                failed += 1
                print("  ❌ Falha ao salvar!")
        else:
            failed += 1
            print("  ❌ Falha ao gerar!")

        # Delay entre requisições (exceto na última)
        if i < len(texts) and delay > 0:
            print(f"  ⏳ Aguardando {delay}s...\n")
            time.sleep(delay)
        elif i < len(texts):
            print()

    # Resumo final
    print("\n" + "="*70)
    print("✨ RESUMO DO LOTE")
    print("="*70)
    print(f"📊 Total processado: {len(texts)} áudio(s)")
    print(f"✅ Sucesso: {successful}/{len(texts)} ({successful/len(texts)*100:.1f}%)")

    if failed > 0:
        print(f"❌ Falhas: {failed}/{len(texts)} ({failed/len(texts)*100:.1f}%)")

    if saved_files:
        # Calcula tamanho total
        total_size = sum(os.path.getsize(f) for f in saved_files) / 1024  # KB
        print(f"\n💾 Tamanho total: {total_size:.2f} KB")
        print(f"📂 Localização: {DOWNLOADS_PATH}")
        print("\n📋 Arquivos gerados:")
        for filepath in saved_files:
            filename = os.path.basename(filepath)
            size = os.path.getsize(filepath) / 1024  # KB
            print(f"  • {filename} ({size:.2f} KB)")

    print("="*70)

    if successful == len(texts):
        print("\n🎉 Todos os áudios gerados com sucesso!")
    elif successful > 0:
        print(f"\n⚠️  Concluído com {failed} falha(s). {successful} áudio(s) gerado(s).")
    else:
        print("\n❌ Nenhum áudio foi gerado. Verifique os erros acima.")

    print()


if __name__ == "__main__":
    main()
