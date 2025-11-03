#!/usr/bin/env python3
"""
Template: Gerador de Thumbnails YouTube

Wrapper simplificado que a skill youtube-thumbnailv2 usa para gerar 5 thumbnails.
Recebe prompts via stdin ou argumentos e executa batch edit.

Uso (via skill):
    # Skill gera 5 prompts e passa para este script
    python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py "prompt1" "prompt2" "prompt3" "prompt4" "prompt5"

Uso (manual):
    # Com argumentos
    python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py "$(cat prompt1.txt)" "$(cat prompt2.txt)"

    # Via stdin (para prompts muito longos)
    cat prompts.txt | python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py --stdin
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from batch_edit_thumbnails import edit_batch
import time


def main():
    """Função principal"""

    prompts = []

    # Verifica se deve ler do stdin
    if "--stdin" in sys.argv:
        print("📥 Lendo prompts do stdin...")
        print("   (Separe cada prompt com uma linha contendo apenas '---')")
        print("   (Pressione Ctrl+D para finalizar)\n")

        current_prompt = []
        for line in sys.stdin:
            if line.strip() == "---":
                if current_prompt:
                    prompts.append("\n".join(current_prompt))
                    current_prompt = []
            else:
                current_prompt.append(line.rstrip())

        # Adiciona último prompt se houver
        if current_prompt:
            prompts.append("\n".join(current_prompt))

    # Ou lê dos argumentos
    elif len(sys.argv) > 1:
        prompts = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    # Validação
    if not prompts:
        print("❌ Erro: Nenhum prompt fornecido\n")
        print("Uso:")
        print('  python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py "prompt1" "prompt2" ...\n')
        print("Ou:")
        print('  cat prompts.txt | python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py --stdin\n')
        print("📝 Prompts devem seguir o template do youtube-thumbnailv2")
        print("   Ver: .claude/skills/youtube-thumbnailv2/SKILL.md")
        sys.exit(1)

    # Validação de quantidade recomendada
    if len(prompts) != 5:
        print(f"⚠️  Aviso: Recebido {len(prompts)} prompts (recomendado: 5 para thumbnails)")
        print()

    print(f"🎬 Gerador de Thumbnails YouTube")
    print(f"📝 {len(prompts)} thumbnails para gerar")
    print("=" * 60)
    print()

    # Gera as thumbnails
    start_time = time.time()
    results = edit_batch(prompts)
    elapsed = time.time() - start_time

    # Resumo
    print(f"\n{'='*60}")
    print(f"✨ Processamento concluído em {elapsed:.1f}s")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"✅ Sucesso: {len(successful)}/{len(results)}")
    if successful:
        print("\n📦 Thumbnails geradas:\n")
        for i, r in enumerate(successful, 1):
            print(f"{i}. {os.path.basename(r['path'])}")
            print(f"   🔗 {r['url']}\n")

    if failed:
        print(f"❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]}... - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {str(Path.home() / 'Downloads')}")

    # Exit code
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
