---
name: skill-creator
description: Cria novas Claude Skills automaticamente usando Progressive Disclosure. Estrutura multi-arquivo profissional com SKILL.md + REFERENCE.md + EXAMPLES.md + TROUBLESHOOTING.md. Use quando usuário pedir para criar/adicionar/fazer nova skill.
allowed-tools: Write, Edit, Read, Bash
---

# 🛠️ Skill Creator - Criador Automático de Skills

## Quando Usar

Automaticamente quando usuário:
- Pedir para **criar nova skill**: "Crie uma skill para [propósito]"
- Pedir para **adicionar skill**: "Adicione uma skill que [faz algo]"
- Mencionar **nova capacidade**: "Quero uma skill que..."

**IMPORTANTE:** Sempre usar **Progressive Disclosure** (padrão obrigatório).

---

## Workflow Automático (4 Etapas)

### Etapa 1: Coletar Informações 📋

Perguntar ao usuário:
1. **Nome da skill** (lowercase, hífens) - ex: `api-validator`
2. **Descrição** (triggers claros) - ex: "Use quando usuário pedir para validar API"
3. **Quando usar** (contextos de ativação)
4. **Ferramentas permitidas** (opcional, padrão: Read, Write, Edit, Bash)
5. **Scripts auxiliares?** (sim/não)

### Etapa 2: Gerar Estrutura Multi-arquivo 🏗️

Criar Progressive Disclosure structure:
```
.claude/skills/nome-da-skill/
├── SKILL.md              # 30-60 linhas (focado)
├── REFERENCE.md          # Docs técnicas completas
├── EXAMPLES.md           # Mínimo 2 exemplos
└── TROUBLESHOOTING.md    # Mínimo 2 erros
```

Ver estrutura completa em [REFERENCE.md](REFERENCE.md).

### Etapa 3: Criar Arquivos 📝

Usar templates do [REFERENCE.md](REFERENCE.md):
- **SKILL.md:** Workflow principal (limpo e focado)
- **REFERENCE.md:** Framework detalhado + configs
- **EXAMPLES.md:** Casos de uso reais
- **TROUBLESHOOTING.md:** Erros comuns + soluções

### Etapa 4: Documentar e Confirmar ✅

1. Atualizar `CLAUDE.md` (seção Skills Disponíveis)
2. Criar commit: `feat: adicionar skill nome-da-skill`
3. Mostrar estrutura final ao usuário

---

## Output Final para Usuário

```
✅ Skill criada com Progressive Disclosure!

📂 Estrutura:
  .claude/skills/nome-da-skill/
  ├── SKILL.md (45 linhas)
  ├── REFERENCE.md
  ├── EXAMPLES.md (3 exemplos)
  └── TROUBLESHOOTING.md (2 erros)

🎯 Como usar: "[frase que ativa]"
📝 Claude carrega arquivos sob demanda
💾 Commited: feat: adicionar skill nome-da-skill
```

---

## Regras Importantes

### ✅ FAZER:
- **Sempre** usar Progressive Disclosure (multi-arquivo)
- **Sempre** manter SKILL.md focado (30-60 linhas, máx 80)
- **Sempre** criar 4 arquivos (SKILL + REFERENCE + EXAMPLES + TROUBLESHOOTING)
- **Sempre** atualizar CLAUDE.md
- **Sempre** commitar após criar

### ❌ NÃO FAZER:
- **NÃO** criar skill em arquivo único
- **NÃO** deixar SKILL.md passar de 80 linhas
- **NÃO** misturar docs técnicas no SKILL.md
- **NÃO** esquecer exemplos

---

## Documentação Adicional

- **Estrutura + Templates:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos de criação:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Problemas comuns:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (ativação automática)
**Versão:** 2.0 (Progressive Disclosure)
