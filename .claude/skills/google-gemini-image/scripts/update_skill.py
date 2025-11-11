#!/usr/bin/env python3
"""
Update Skill - Atualiza SKILL.md de uma skill automaticamente

Permite correções programáticas em arquivos SKILL.md.
"""

import sys
from pathlib import Path


def update_skill(skill_path: str, old_text: str, new_text: str) -> bool:
    """
    Atualiza SKILL.md de uma skill, substituindo old_text por new_text

    Args:
        skill_path: Caminho para a pasta da skill
        old_text: Texto a ser substituído
        new_text: Novo texto

    Returns:
        True se atualizado com sucesso, False caso contrário
    """

    skill_md = Path(skill_path) / "SKILL.md"

    if not skill_md.exists():
        print(f"❌ Erro: SKILL.md não encontrado em {skill_path}")
        return False

    try:
        # Ler conteúdo atual
        content = skill_md.read_text()

        # Verificar se old_text existe
        if old_text not in content:
            print(f"⚠️  Aviso: Texto não encontrado no SKILL.md")
            print(f"   Procurando: {old_text[:100]}...")
            return False

        # Substituir
        new_content = content.replace(old_text, new_text)

        # Salvar
        skill_md.write_text(new_content)

        print(f"✅ SKILL.md atualizado com sucesso!")
        print(f"   Skill: {Path(skill_path).name}")
        print(f"   Substituído: {old_text[:80]}...")
        print(f"   Por: {new_text[:80]}...")

        return True

    except Exception as e:
        print(f"❌ Erro ao atualizar SKILL.md: {e}")
        return False


def main():
    """CLI para testar update_skill"""

    if len(sys.argv) < 4:
        print("Uso: python3 update_skill.py <skill_path> <old_text> <new_text>")
        print("\nExemplos:")
        print('  python3 update_skill.py .claude/skills/gerar-foto-realista "--prompt" ""')
        sys.exit(1)

    skill_path = sys.argv[1]
    old_text = sys.argv[2]
    new_text = sys.argv[3]

    success = update_skill(skill_path, old_text, new_text)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
