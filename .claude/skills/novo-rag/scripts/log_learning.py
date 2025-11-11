#!/usr/bin/env python3
"""
Log Learning - Registra aprendizados/correções em LEARNINGS.md

Mantém histórico de erros corrigidos em cada skill.
"""

import sys
from pathlib import Path
from datetime import datetime


def log_learning(
    skill_path: str,
    error_description: str,
    fix_description: str,
    line_affected: str = "N/A"
) -> bool:
    """
    Registra aprendizado em LEARNINGS.md da skill

    Args:
        skill_path: Caminho para a pasta da skill
        error_description: Descrição do erro
        fix_description: Descrição da correção
        line_affected: Linha/arquivo afetado (opcional)

    Returns:
        True se registrado com sucesso, False caso contrário
    """

    skill_dir = Path(skill_path)
    learnings_md = skill_dir / "LEARNINGS.md"

    # Se LEARNINGS.md não existe, criar do template
    if not learnings_md.exists():
        template_path = Path(__file__).parent.parent / "assets" / "LEARNINGS_TEMPLATE.md"

        if template_path.exists():
            template = template_path.read_text()
            skill_name = skill_dir.name
            header = template.replace("{SKILL_NAME}", skill_name)
            learnings_md.write_text(header)
        else:
            # Fallback: criar header básico
            learnings_md.write_text(f"# Learnings - {skill_dir.name}\n\n## Histórico de Correções\n\n")

    try:
        # Ler conteúdo atual
        content = learnings_md.read_text()

        # Criar nova entrada
        today = datetime.now().strftime("%Y-%m-%d")
        entry = f"""
### {today} - {error_description}

**Problema:** {error_description}
**Correção:** {fix_description}
**Linha afetada:** {line_affected}
**Status:** ✅ Corrigido

---
"""

        # Inserir após o header (antes do primeiro "###" existente, ou no final)
        if "###" in content:
            # Inserir antes da primeira entrada existente
            parts = content.split("###", 1)
            new_content = parts[0] + entry + "###" + parts[1]
        else:
            # Adicionar no final
            new_content = content + entry

        # Salvar
        learnings_md.write_text(new_content)

        print(f"✅ Aprendizado registrado em LEARNINGS.md!")
        print(f"   Skill: {skill_dir.name}")
        print(f"   Data: {today}")
        print(f"   Erro: {error_description}")

        return True

    except Exception as e:
        print(f"❌ Erro ao registrar aprendizado: {e}")
        return False


def main():
    """CLI para testar log_learning"""

    if len(sys.argv) < 4:
        print("Uso: python3 log_learning.py <skill_path> <error_desc> <fix_desc> [line]")
        print("\nExemplos:")
        print('  python3 log_learning.py .claude/skills/gerar-foto-realista "Erro: --prompt não reconhecido" "Removido --prompt" "SKILL.md:97"')
        sys.exit(1)

    skill_path = sys.argv[1]
    error_desc = sys.argv[2]
    fix_desc = sys.argv[3]
    line_affected = sys.argv[4] if len(sys.argv) > 4 else "N/A"

    success = log_learning(skill_path, error_desc, fix_desc, line_affected)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
