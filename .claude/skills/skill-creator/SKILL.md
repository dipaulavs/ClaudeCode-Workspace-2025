---
name: skill-creator
description: Cria novas Claude Skills automaticamente usando Progressive Disclosure. Estrutura multi-arquivo profissional com SKILL.md + REFERENCE.md + EXAMPLES.md + TROUBLESHOOTING.md. Use quando usuário pedir para criar/adicionar/fazer nova skill.
allowed-tools: Write, Edit, Read, Bash
---

# 🛠️ Skill Creator - Criador Automático de Skills

## Quando Usar

Use esta skill automaticamente quando o usuário:
- Pedir para **criar nova skill**: "Crie uma skill para [propósito]"
- Pedir para **adicionar skill**: "Adicione uma skill que [faz algo]"
- Mencionar **nova capacidade**: "Quero uma skill que..."
- Solicitar **automatizar** algo específico

**IMPORTANTE:** Esta skill aplica **Progressive Disclosure** por padrão (padrão oficial Claude Code).

---

## Workflow Automático (4 Etapas)

### Etapa 1: Coletar Informações 📋

**Perguntar ao usuário:**

1. **Nome da skill** (lowercase, hífens)
   - Exemplo: `api-validator`, `sql-optimizer`

2. **Descrição** (triggers claros para ativação automática)
   - Exemplo: "Valida APIs REST. Use quando usuário pedir para validar/testar/checar API."

3. **Quando usar** (contextos de ativação)
   - Exemplos de frases que trigam a skill

4. **Ferramentas permitidas** (opcional)
   - Padrão: Read, Write, Edit, Bash
   - Restringir se necessário (ex: só Read/Grep para análise)

5. **Tem scripts auxiliares?** (sim/não)
   - Se sim, que tipo de scripts?

---

### Etapa 2: Gerar Estrutura Multi-arquivo 🏗️

**Use Progressive Disclosure** - veja [STRUCTURE.md](STRUCTURE.md) para estrutura completa.

**Criar esta estrutura:**

```
.claude/skills/
└── nome-da-skill/
    ├── SKILL.md                # Instruções principais (FOCADO)
    ├── REFERENCE.md            # Documentação técnica detalhada
    ├── EXAMPLES.md             # Casos de uso reais
    ├── TROUBLESHOOTING.md      # Guia de erros comuns
    └── scripts/                # (opcional) Scripts auxiliares
        └── helper.py
```

**Princípio:** SKILL.md deve ser **limpo e focado** (30-60 linhas), referenciando outros arquivos.

---

### Etapa 3: Criar Arquivos 📝

**Para cada arquivo, use os templates** - veja [TEMPLATES.md](TEMPLATES.md) para templates completos.

#### SKILL.md (Arquivo Principal)

```markdown
---
name: nome-da-skill
description: [Descrição com triggers claros]
allowed-tools: Read, Write, Edit  # (opcional)
---

# [Nome da Skill]

## Quando Usar

Use esta skill quando:
- [Trigger 1]
- [Trigger 2]

## Workflow Principal

1. [Etapa 1]
2. [Etapa 2] - Veja [REFERENCE.md](REFERENCE.md) para detalhes
3. [Etapa 3]

## Exemplos de Uso

Veja [EXAMPLES.md](EXAMPLES.md) para casos reais.

## Troubleshooting

Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Regras Importantes

### ✅ FAZER:
- [Regra 1]
- [Regra 2]

### ❌ NÃO FAZER:
- [Anti-pattern 1]
- [Anti-pattern 2]
```

#### REFERENCE.md (Documentação Técnica)

```markdown
# Referência Técnica - [Nome da Skill]

## Framework Detalhado

[Documentação completa da metodologia/framework]

## Configurações

[Variáveis, caminhos, APIs, etc]

## Parâmetros

[Lista completa de parâmetros e opções]

## APIs e Integrações

[Documentação de APIs usadas]
```

#### EXAMPLES.md (Casos de Uso)

```markdown
# Exemplos - [Nome da Skill]

## Exemplo 1: [Caso Real]

**Input:**
```
[Exemplo de entrada]
```

**Output:**
```
[Exemplo de saída]
```

**Observações:** [Insights do exemplo]

---

## Exemplo 2: [Outro Caso]

[...]
```

#### TROUBLESHOOTING.md (Guia de Erros)

```markdown
# Troubleshooting - [Nome da Skill]

## Erro: [Descrição do Erro]

**Causa:** [Por que acontece]

**Solução:**
```bash
[Comandos ou passos para resolver]
```

---

## Erro: [Outro Erro]

[...]
```

---

### Etapa 4: Documentar e Confirmar ✅

**1. Atualizar CLAUDE.md**

Adicionar entrada na seção "Skills Disponíveis":

```markdown
| **nome-da-skill** | [Quando usar] | [Descrição breve] |
```

**2. Criar commit:**

```bash
git add .claude/skills/nome-da-skill/
git commit -m "feat: adicionar skill nome-da-skill com Progressive Disclosure"
```

**3. Mostrar ao usuário:**

```
✅ Skill criada com Progressive Disclosure!

📂 Estrutura:
  .claude/skills/nome-da-skill/
  ├── SKILL.md (principal - 45 linhas)
  ├── REFERENCE.md (documentação técnica)
  ├── EXAMPLES.md (3 exemplos)
  └── TROUBLESHOOTING.md (2 erros comuns)

🎯 Como usar:
  "[Frase de exemplo que ativa a skill]"

📝 Claude detecta automaticamente e carrega arquivos sob demanda (Progressive Disclosure).

💾 Commited: feat: adicionar skill nome-da-skill
```

---

## Princípios de Progressive Disclosure

**SEMPRE aplicar:**

1. ✅ **SKILL.md limpo** (30-60 linhas) - só workflow principal
2. ✅ **Referenciar outros arquivos** com `[REFERENCE.md](REFERENCE.md)`
3. ✅ **Separar concerns:**
   - SKILL.md → Workflow
   - REFERENCE.md → Documentação técnica
   - EXAMPLES.md → Casos de uso
   - TROUBLESHOOTING.md → Erros
4. ✅ **Claude carrega sob demanda** - não precarregar tudo
5. ✅ **Escalável** - fácil adicionar novos arquivos depois

---

## Validação Antes de Criar

**Verificar:**

- [ ] Nome usa lowercase e hífens (ex: `api-validator`)
- [ ] Descrição tem triggers claros para ativação
- [ ] SKILL.md está focado (não excede 80 linhas)
- [ ] Referências a outros arquivos usam links markdown
- [ ] Estrutura usa Progressive Disclosure
- [ ] Tem pelo menos 1 exemplo em EXAMPLES.md

---

## Regras Importantes

### ✅ FAZER:

- **Sempre** usar Progressive Disclosure (multi-arquivo)
- **Sempre** criar SKILL.md + REFERENCE.md + EXAMPLES.md + TROUBLESHOOTING.md
- **Sempre** manter SKILL.md limpo e focado (30-60 linhas)
- **Sempre** adicionar entry em CLAUDE.md
- **Sempre** commitar após criar
- **Sempre** mostrar estrutura final ao usuário

### ❌ NÃO FAZER:

- **NÃO** criar skill em arquivo único (obsoleto)
- **NÃO** deixar SKILL.md passar de 80 linhas
- **NÃO** misturar documentação técnica no SKILL.md
- **NÃO** esquecer de atualizar CLAUDE.md
- **NÃO** criar sem exemplos

---

## Estrutura Detalhada

Veja [STRUCTURE.md](STRUCTURE.md) para estrutura completa e padrões.

## Templates Completos

Veja [TEMPLATES.md](TEMPLATES.md) para templates prontos para copiar.

---

**Criado em:** 02/11/2025
**Padrão usado:** Progressive Disclosure (documentação oficial Claude Code)
**Status:** ✅ Pronto para criar skills profissionais automaticamente
