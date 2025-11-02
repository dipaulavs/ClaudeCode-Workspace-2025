# Estrutura de Skills - Padrão Progressive Disclosure

Este documento define a estrutura padrão para todas as Claude Skills neste workspace.

---

## 📐 Estrutura Padrão (4 Arquivos)

```
.claude/skills/
└── nome-da-skill/
    ├── SKILL.md                # Instruções principais (30-60 linhas)
    ├── REFERENCE.md            # Documentação técnica detalhada
    ├── EXAMPLES.md             # Casos de uso reais (mínimo 2)
    └── TROUBLESHOOTING.md      # Guia de erros comuns
```

**Princípio:** Usar **Progressive Disclosure** - Claude carrega arquivos sob demanda.

---

## 📄 SKILL.md (Arquivo Principal)

**Propósito:** Instruções focadas e claras do workflow principal.

**Tamanho ideal:** 30-60 linhas (máximo 80 linhas)

**Estrutura:**

```markdown
---
name: nome-da-skill
description: [Descrição com triggers claros]
allowed-tools: Read, Write, Edit  # (opcional)
---

# [Nome da Skill]

## Quando Usar
[Triggers claros]

## Workflow Principal
[Etapas do processo - FOCADO]
[Referências a REFERENCE.md quando precisar de detalhes]

## Exemplos
Veja [EXAMPLES.md](EXAMPLES.md)

## Troubleshooting
Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Regras Importantes
✅ FAZER:
❌ NÃO FAZER:
```

**O que incluir:**
- ✅ Workflow principal (etapas claras)
- ✅ Quando usar (triggers)
- ✅ Regras importantes
- ✅ Links para outros arquivos

**O que NÃO incluir:**
- ❌ Documentação técnica detalhada (→ REFERENCE.md)
- ❌ Exemplos longos (→ EXAMPLES.md)
- ❌ Lista de erros (→ TROUBLESHOOTING.md)
- ❌ Configurações detalhadas (→ REFERENCE.md)

---

## 📚 REFERENCE.md (Documentação Técnica)

**Propósito:** Documentação completa e detalhada.

**Tamanho:** Sem limite (quanto mais completo, melhor)

**Estrutura:**

```markdown
# Referência Técnica - [Nome da Skill]

## Framework Detalhado
[Metodologia completa]

## Configurações
[Todas as variáveis, caminhos, etc]

## Parâmetros
[Lista completa de opções]

## APIs e Integrações
[Documentação de APIs/ferramentas usadas]

## Formatos de Input/Output
[Estruturas de dados, formatos esperados]

## Algoritmos
[Lógica detalhada, pseudocódigo se necessário]
```

**Quando Claude lê:** Quando precisa de detalhes técnicos durante execução.

---

## 💡 EXAMPLES.md (Casos de Uso)

**Propósito:** Exemplos práticos e concretos.

**Mínimo:** 2 exemplos completos

**Estrutura:**

```markdown
# Exemplos - [Nome da Skill]

## Exemplo 1: [Nome Descritivo do Caso]

**Contexto:** [Situação do usuário]

**Input:**
```
[Entrada do usuário]
```

**Processo:**
1. [Etapa 1 executada]
2. [Etapa 2 executada]

**Output:**
```
[Resultado final]
```

**Observações:** [Insights, variações, notas importantes]

---

## Exemplo 2: [Outro Caso Real]

[Mesmo formato...]

---

## Exemplo 3: Edge Case - [Caso Especial]

[Casos difíceis, edge cases, etc]
```

**Tipos de exemplos a incluir:**
- ✅ Caso simples (happy path)
- ✅ Caso complexo (múltiplas variáveis)
- ✅ Edge case (situações raras/difíceis)

---

## 🔧 TROUBLESHOOTING.md (Guia de Erros)

**Propósito:** Documentar erros comuns e soluções.

**Estrutura:**

```markdown
# Troubleshooting - [Nome da Skill]

## Erro: [Descrição Clara do Erro]

**Sintoma:** [Como o erro aparece]

**Causa:** [Por que acontece]

**Solução:**
```bash
[Comandos específicos ou passos]
```

**Prevenção:** [Como evitar no futuro]

---

## Erro: [Outro Erro Comum]

[Mesmo formato...]

---

## Validação Geral

**Se nada funciona:**

1. [Passo 1 de debug geral]
2. [Passo 2 de debug geral]
3. [Contato/logs/onde buscar ajuda]
```

**Quando Claude lê:** Quando encontra erro durante execução.

---

## 🗂️ scripts/ (Opcional)

**Quando incluir:** Se a skill precisa de scripts auxiliares Python/Bash.

**Estrutura:**

```
nome-da-skill/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
├── TROUBLESHOOTING.md
└── scripts/
    ├── helper.py           # Script auxiliar principal
    ├── validator.py        # Validador
    └── utils.py            # Utilidades
```

**Regras para scripts:**
- ✅ Documentar no REFERENCE.md
- ✅ Adicionar exemplos no EXAMPLES.md
- ✅ Scripts devem ter docstrings claras
- ✅ Incluir requirements.txt se necessário

---

## 📁 templates/ (Opcional)

**Quando incluir:** Se a skill usa templates de arquivos.

**Estrutura:**

```
nome-da-skill/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
├── TROUBLESHOOTING.md
└── templates/
    ├── output.md.template      # Template de output
    ├── config.yaml.template    # Template de configuração
    └── README.md               # Doc dos templates
```

---

## 🎯 Progressive Disclosure em Ação

### Como Claude Usa os Arquivos

**Sequência típica:**

```
1. Skill ativa → Claude lê SKILL.md (sempre)
   ↓
2. Precisa de detalhes técnicos → Claude lê REFERENCE.md (sob demanda)
   ↓
3. Precisa de exemplo → Claude lê EXAMPLES.md (sob demanda)
   ↓
4. Encontra erro → Claude lê TROUBLESHOOTING.md (sob demanda)
```

**Benefício:** Economiza tokens, carrega só o necessário.

---

## ✅ Checklist de Validação

Antes de considerar a skill completa:

### Estrutura
- [ ] Pasta criada em `.claude/skills/nome-da-skill/`
- [ ] SKILL.md existe e tem frontmatter YAML válido
- [ ] REFERENCE.md existe e está completo
- [ ] EXAMPLES.md existe com mínimo 2 exemplos
- [ ] TROUBLESHOOTING.md existe com mínimo 2 erros

### Qualidade
- [ ] SKILL.md tem 30-60 linhas (máx 80)
- [ ] SKILL.md referencia outros arquivos com links markdown
- [ ] Description tem triggers claros
- [ ] Exemplos são concretos e completos
- [ ] Erros comuns estão documentados

### Integração
- [ ] Entry adicionada no CLAUDE.md (seção Skills)
- [ ] Commit criado com mensagem `feat: adicionar skill nome-da-skill`
- [ ] Testado manualmente (trigger funciona?)

---

## 🚫 Anti-Padrões (Evitar)

### ❌ Arquivo único gigante

```
nome-da-skill/
└── SKILL.md (200+ linhas)  # ERRADO!
```

**Por quê:** Carrega tudo sempre, desperdiça tokens.

### ❌ SKILL.md com documentação técnica

```markdown
# Skill

## API Documentation
[50 linhas de docs da API...]  # ERRADO! Mover para REFERENCE.md
```

### ❌ Sem exemplos

```
nome-da-skill/
├── SKILL.md
└── REFERENCE.md
# Falta EXAMPLES.md!  # ERRADO!
```

### ❌ Referências quebradas

```markdown
Veja [REFERENCE.md](reference.md)  # ERRADO! Case-sensitive
```

**Correto:** `[REFERENCE.md](REFERENCE.md)` (maiúsculas)

---

## 📊 Comparação: Antes vs Depois

### ❌ Estrutura Antiga (Arquivo Único)

```
estudar-video/
└── SKILL.md (226 linhas)
    ├─ Instruções (40 linhas)
    ├─ Documentação técnica (80 linhas)
    ├─ Exemplos (50 linhas)
    ├─ Troubleshooting (30 linhas)
    └─ Histórico (26 linhas)
```

**Problema:** 226 linhas carregadas sempre!

### ✅ Estrutura Nova (Progressive Disclosure)

```
estudar-video/
├── SKILL.md (45 linhas) ← Sempre carregado
├── REFERENCE.md (80 linhas) ← Sob demanda
├── EXAMPLES.md (50 linhas) ← Sob demanda
└── TROUBLESHOOTING.md (30 linhas) ← Sob demanda
```

**Benefício:** Carrega 45 linhas inicialmente, 226 linhas só se necessário!

---

## 🎓 Boas Práticas

1. **Mantenha SKILL.md limpo** - Apenas workflow principal
2. **Use links markdown** - `[REFERENCE.md](REFERENCE.md)` para referenciar
3. **Seja específico nos triggers** - Description clara ativa automaticamente
4. **Documente erros reais** - TROUBLESHOOTING com erros que você já viu
5. **Exemplos concretos** - Não usar "exemplo genérico", usar casos reais
6. **Atualize continuamente** - Adicione novos exemplos/erros conforme surgem

---

**Última atualização:** 02/11/2025
**Baseado em:** Documentação oficial Claude Code Skills
**Status:** ✅ Padrão obrigatório para todas as skills neste workspace
