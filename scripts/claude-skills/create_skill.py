#!/usr/bin/env python3
"""
Script auxiliar para criar Claude Skills com Progressive Disclosure.

Usage:
    python3 scripts/claude-skills/create_skill.py <skill-name>

Exemplo:
    python3 scripts/claude-skills/create_skill.py api-validator
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def validate_skill_name(name: str) -> bool:
    """Valida nome da skill (lowercase, hífens, max 64 chars)."""
    if not name:
        return False
    if len(name) > 64:
        print(f"❌ Nome muito longo: {len(name)} caracteres (máximo 64)")
        return False
    if not all(c.islower() or c.isdigit() or c == '-' for c in name):
        print("❌ Use apenas letras minúsculas, números e hífens")
        return False
    return True


def get_workspace_root() -> Path:
    """Retorna caminho raiz do workspace."""
    script_path = Path(__file__).resolve()
    # scripts/claude-skills/create_skill.py -> raiz (2 níveis acima)
    return script_path.parent.parent.parent


def create_skill_structure(skill_name: str):
    """Cria estrutura de pastas e arquivos da skill."""

    workspace_root = get_workspace_root()
    skills_dir = workspace_root / ".claude" / "skills" / skill_name

    # Verificar se skill já existe
    if skills_dir.exists():
        print(f"❌ Skill '{skill_name}' já existe em: {skills_dir}")
        return False

    # Criar diretório da skill
    skills_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Criado: {skills_dir}")

    # Data atual
    today = datetime.now().strftime("%d/%m/%Y")

    # Criar SKILL.md
    skill_md = f"""---
name: {skill_name}
description: [PREENCHER: Descrição clara com triggers que ativam automaticamente. Inclua verbos de ação e contextos específicos.]
allowed-tools: Read, Write, Edit, Bash  # (opcional - remover se não restringir)
---

# {skill_name.replace('-', ' ').title()}

## Quando Usar

Use esta skill automaticamente quando o usuário:
- Pedir para **[ação 1]**: "[exemplo de frase]"
- Pedir para **[ação 2]**: "[exemplo de frase]"
- Mencionar **[contexto específico]**

**IMPORTANTE:** [Alguma regra crítica de comportamento]

---

## Workflow Principal ([N] Etapas)

### Etapa 1: [Nome da Etapa] 📋

**O que fazer:**
[Descrição clara da etapa]

Para detalhes técnicos, veja [REFERENCE.md](REFERENCE.md).

---

### Etapa 2: [Nome da Etapa] 🔍

**O que fazer:**
[Descrição clara]

---

## Exemplos de Uso

Veja [EXAMPLES.md](EXAMPLES.md) para casos reais completos.

---

## Troubleshooting

Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para guia completo de erros.

---

## Regras Importantes

### ✅ FAZER:

- **Sempre** [regra crítica 1]
- **Sempre** [regra crítica 2]

### ❌ NÃO FAZER:

- **NÃO** [anti-pattern 1]
- **NÃO** [anti-pattern 2]

---

**Criado em:** {today}
**Status:** 🚧 Em desenvolvimento
"""

    (skills_dir / "SKILL.md").write_text(skill_md)
    print(f"✅ Criado: SKILL.md")

    # Criar REFERENCE.md
    reference_md = f"""# Referência Técnica - {skill_name.replace('-', ' ').title()}

Este arquivo contém documentação técnica completa e detalhada.

---

## 🎯 Framework Detalhado

### Metodologia

[PREENCHER: Explicação completa do framework/metodologia usada]

---

## ⚙️ Configurações

### Variáveis de Ambiente

```bash
# PREENCHER: Variáveis necessárias
VARIABLE_NAME=value
```

### Caminhos

```
# PREENCHER: Caminhos importantes
/caminho/para/arquivos/
```

---

## 📝 Parâmetros

### Parâmetro 1: [Nome]

**Tipo:** string | number | boolean
**Obrigatório:** sim | não
**Padrão:** [valor]
**Descrição:** [O que faz]

---

## 🔌 APIs e Integrações

[PREENCHER: APIs utilizadas]

---

## 📥 Formatos de Input

[PREENCHER: Estrutura de input esperado]

---

## 📤 Formatos de Output

[PREENCHER: Estrutura de output gerado]

---

**Última atualização:** {today}
**Versão:** 1.0
"""

    (skills_dir / "REFERENCE.md").write_text(reference_md)
    print(f"✅ Criado: REFERENCE.md")

    # Criar EXAMPLES.md
    examples_md = f"""# Exemplos - {skill_name.replace('-', ' ').title()}

Este arquivo contém casos de uso reais e completos.

---

## Exemplo 1: [Nome Descritivo do Caso]

### Contexto

[PREENCHER: Situação do usuário, problema que precisa resolver]

### Input do Usuário

```
[PREENCHER: Exatamente o que o usuário digitou]
```

### Processo de Execução

**Etapa 1: [Nome]**
- [O que aconteceu]
- [Ferramenta usada]

**Etapa 2: [Nome]**
- [O que aconteceu]

### Output Gerado

```
[PREENCHER: Output completo mostrado ao usuário]
```

### Observações

- **Insight:** [Aprendizado deste caso]

---

## Exemplo 2: [Caso Mais Complexo]

### Contexto

[PREENCHER: Cenário mais complexo]

### Input do Usuário

```
[PREENCHER]
```

### Output Gerado

```
[PREENCHER]
```

---

**Total de exemplos:** 2 (adicionar mais conforme skill evolui)
**Última atualização:** {today}
"""

    (skills_dir / "EXAMPLES.md").write_text(examples_md)
    print(f"✅ Criado: EXAMPLES.md")

    # Criar TROUBLESHOOTING.md
    troubleshooting_md = f"""# Troubleshooting - {skill_name.replace('-', ' ').title()}

Guia completo para resolver erros comuns.

---

## 🚨 Erro: [Descrição Clara do Erro 1]

### Sintoma

```
[PREENCHER: Como o erro aparece - mensagem exata ou descrição]
```

### Causa

[PREENCHER: Por que este erro acontece]

### Solução

**Passo a passo:**

1. [Passo 1]
```bash
[Comando ou ação]
```

2. [Passo 2]

### Prevenção

- [Como evitar]

---

## 🚨 Erro: [Descrição do Erro 2]

### Sintoma

```
[PREENCHER]
```

### Causa

[PREENCHER]

### Solução

```bash
[Comando rápido para resolver]
```

---

## 🔍 Debugging Geral

### Se Nenhuma Solução Acima Funcionou

**1. Verificar logs:**
```bash
[Como acessar logs]
```

**2. Validar ambiente:**
```bash
[Verificações necessárias]
```

---

**Total de erros documentados:** 2 (adicionar mais conforme surgem)
**Última atualização:** {today}
"""

    (skills_dir / "TROUBLESHOOTING.md").write_text(troubleshooting_md)
    print(f"✅ Criado: TROUBLESHOOTING.md")

    return True


def show_next_steps(skill_name: str):
    """Mostra próximos passos após criação."""
    print(f"""
╔════════════════════════════════════════════════════════════════════
║ ✅ Skill '{skill_name}' criada com sucesso!
╚════════════════════════════════════════════════════════════════════

📂 Estrutura criada:
  .claude/skills/{skill_name}/
  ├── SKILL.md               (principal - PREENCHER)
  ├── REFERENCE.md           (documentação técnica - PREENCHER)
  ├── EXAMPLES.md            (casos de uso - PREENCHER)
  └── TROUBLESHOOTING.md     (erros comuns - PREENCHER)

📝 Próximos passos:

1. PREENCHER os arquivos:
   - Edite SKILL.md (description, triggers, workflow)
   - Complete REFERENCE.md (documentação técnica)
   - Adicione exemplos reais em EXAMPLES.md
   - Documente erros em TROUBLESHOOTING.md

2. VALIDAR:
   - SKILL.md não deve exceder 80 linhas
   - Description deve ter triggers claros
   - Mínimo 2 exemplos em EXAMPLES.md
   - Mínimo 2 erros em TROUBLESHOOTING.md

3. DOCUMENTAR no CLAUDE.md:
   - Adicionar entrada na seção "Skills Disponíveis"

4. COMMITAR:
   git add .claude/skills/{skill_name}/
   git commit -m "feat: adicionar skill {skill_name} com Progressive Disclosure"

5. TESTAR:
   - Testar trigger automático
   - Verificar se Claude carrega arquivos sob demanda

🎯 Padrão usado: Progressive Disclosure (documentação oficial)

📚 Referências:
   - Estrutura: .claude/skills/skill-creator/STRUCTURE.md
   - Templates: .claude/skills/skill-creator/TEMPLATES.md
""")


def main():
    """Função principal."""

    if len(sys.argv) != 2:
        print("""
╔════════════════════════════════════════════════════════════════════
║ 🛠️  Criador de Claude Skills com Progressive Disclosure
╚════════════════════════════════════════════════════════════════════

Usage:
    python3 scripts/claude-skills/create_skill.py <skill-name>

Exemplo:
    python3 scripts/claude-skills/create_skill.py api-validator

Regras para nome:
  ✅ Usar lowercase (minúsculas)
  ✅ Usar hífens para separar palavras
  ✅ Máximo 64 caracteres
  ❌ Sem espaços, underscores ou caracteres especiais

Exemplos válidos:
  • api-validator
  • sql-optimizer
  • code-reviewer
  • test-generator
""")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Validar nome
    if not validate_skill_name(skill_name):
        sys.exit(1)

    print(f"\n🚀 Criando skill '{skill_name}' com Progressive Disclosure...\n")

    # Criar estrutura
    success = create_skill_structure(skill_name)

    if success:
        show_next_steps(skill_name)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
