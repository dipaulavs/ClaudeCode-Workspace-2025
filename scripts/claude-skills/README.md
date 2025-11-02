# 🛠️ Claude Skills Creator

Sistema automatizado para criar Claude Skills profissionais usando **Progressive Disclosure**.

---

## 📋 O Que É Isso?

Este diretório contém ferramentas para **criar novas Claude Skills** automaticamente com estrutura profissional multi-arquivo.

**Problema resolvido:** Criar Skills manualmente é repetitivo e sujeito a erros.

**Solução:** Script Python + Skill model-invoked que geram estrutura completa automaticamente.

---

## 🎯 2 Maneiras de Criar Skills

### Opção 1: Via Claude (Recomendado) 🤖

**Ativação automática** - Claude detecta e cria automaticamente:

```
Você: "Crie uma skill para validar APIs REST"

Claude (automaticamente):
  ✓ Usa skill-creator
  ✓ Pergunta detalhes (triggers, ferramentas)
  ✓ Gera estrutura multi-arquivo
  ✓ Aplica Progressive Disclosure
  ✓ Cria todos os .md organizados
  ✓ Mostra próximos passos
```

**Localização da skill:** `.claude/skills/skill-creator/`

---

### Opção 2: Via Script Python 🐍

**Execução manual** via terminal:

```bash
python3 scripts/claude-skills/create_skill.py nome-da-skill
```

**Exemplo:**
```bash
python3 scripts/claude-skills/create_skill.py api-validator
```

**Output:**
```
📂 Estrutura criada:
  .claude/skills/api-validator/
  ├── SKILL.md
  ├── REFERENCE.md
  ├── EXAMPLES.md
  └── TROUBLESHOOTING.md
```

---

## 📐 Estrutura Gerada (Progressive Disclosure)

Ambas opções geram esta estrutura:

```
.claude/skills/
└── nome-da-skill/
    ├── SKILL.md                # Instruções principais (30-60 linhas)
    ├── REFERENCE.md            # Documentação técnica detalhada
    ├── EXAMPLES.md             # Casos de uso reais (mínimo 2)
    └── TROUBLESHOOTING.md      # Guia de erros comuns (mínimo 2)
```

**Princípio:** Progressive Disclosure - Claude carrega arquivos sob demanda.

---

## 🚀 Quick Start

### 1. Criar Nova Skill

**Via Claude:**
```
"Crie uma skill que valida código SQL"
```

**Via script:**
```bash
python3 scripts/claude-skills/create_skill.py sql-validator
```

### 2. Preencher Conteúdo

Editar os 4 arquivos gerados:

- **SKILL.md** - Workflow principal (triggers, etapas, regras)
- **REFERENCE.md** - Documentação técnica (APIs, configs, parâmetros)
- **EXAMPLES.md** - Mínimo 2 casos de uso reais
- **TROUBLESHOOTING.md** - Mínimo 2 erros comuns

### 3. Validar

Checklist antes de commitar:

- [ ] SKILL.md não excede 80 linhas
- [ ] Description tem triggers claros
- [ ] SKILL.md referencia outros arquivos com links markdown
- [ ] EXAMPLES.md tem mínimo 2 exemplos completos
- [ ] TROUBLESHOOTING.md tem mínimo 2 erros documentados

### 4. Documentar no CLAUDE.md

Adicionar entrada na seção "Skills Disponíveis":

```markdown
| **nome-da-skill** | [Quando usar] | [Descrição breve] |
```

### 5. Commitar

```bash
git add .claude/skills/nome-da-skill/
git commit -m "feat: adicionar skill nome-da-skill com Progressive Disclosure"
```

---

## 📁 Arquivos Deste Diretório

```
scripts/claude-skills/
├── README.md                   # Este arquivo
├── create_skill.py             # Script gerador
└── templates/                  # Templates de arquivos
    ├── SKILL.md.template
    ├── REFERENCE.md.template
    ├── EXAMPLES.md.template
    └── TROUBLESHOOTING.md.template
```

---

## 📚 Documentação Completa

### Skill: skill-creator

**Localização:** `.claude/skills/skill-creator/`

**Arquivos:**
- `SKILL.md` - Instruções para Claude criar skills
- `STRUCTURE.md` - Padrão de estrutura Progressive Disclosure
- `TEMPLATES.md` - Templates completos para copiar

**Como funciona:**
1. Claude detecta pedido para criar skill
2. Coleta informações (nome, triggers, ferramentas)
3. Gera estrutura multi-arquivo
4. Mostra próximos passos

---

## 🎯 Regras de Nomenclatura

### ✅ Nomes Válidos

- `api-validator`
- `sql-optimizer`
- `code-reviewer`
- `test-generator`

**Regras:**
- ✅ Lowercase (minúsculas)
- ✅ Hífens para separar palavras
- ✅ Máximo 64 caracteres

### ❌ Nomes Inválidos

- `API_Validator` (underscores, maiúsculas)
- `api validator` (espaços)
- `apiValidator` (camelCase)

---

## 🔍 Progressive Disclosure em Ação

### Como Claude Usa os Arquivos

**Sequência típica:**

```
1. Skill ativa
   ↓
   Claude lê SKILL.md (sempre - 40 linhas)

2. Precisa de detalhes técnicos
   ↓
   Claude lê REFERENCE.md (sob demanda - 80 linhas)

3. Precisa de exemplo
   ↓
   Claude lê EXAMPLES.md (sob demanda - 50 linhas)

4. Encontra erro
   ↓
   Claude lê TROUBLESHOOTING.md (sob demanda - 30 linhas)
```

**Benefício:** Economiza tokens - carrega 40 linhas inicialmente, 200 linhas só se necessário!

---

## 🎨 Templates Disponíveis

### 1. SKILL.md.template

Template do arquivo principal com:
- Frontmatter YAML
- Seção "Quando Usar"
- Workflow Principal (3 etapas)
- Links para outros arquivos
- Regras (FAZER/NÃO FAZER)

### 2. REFERENCE.md.template

Template de documentação técnica:
- Framework detalhado
- Configurações
- Parâmetros
- APIs e integrações
- Formatos de input/output
- Algoritmos

### 3. EXAMPLES.md.template

Template de casos de uso:
- 4 exemplos estruturados
- Contexto + Input + Processo + Output
- Observações e insights
- Edge cases
- Galeria de inputs comuns

### 4. TROUBLESHOOTING.md.template

Template de erros:
- 5 erros estruturados
- Sintoma + Causa + Solução
- Prevenção
- Debugging geral
- Tabela de frequência

---

## 💡 Exemplos de Uso

### Criar Skill de Validação de API

```bash
python3 scripts/claude-skills/create_skill.py api-validator
```

Gera:
```
.claude/skills/api-validator/
├── SKILL.md (validar endpoints, métodos HTTP, responses)
├── REFERENCE.md (OpenAPI spec, formato JSON)
├── EXAMPLES.md (validar API REST, validar GraphQL)
└── TROUBLESHOOTING.md (endpoint não responde, auth falha)
```

### Criar Skill de Otimização SQL

```bash
python3 scripts/claude-skills/create_skill.py sql-optimizer
```

Gera:
```
.claude/skills/sql-optimizer/
├── SKILL.md (analisar queries, sugerir indexes)
├── REFERENCE.md (EXPLAIN ANALYZE, query plans)
├── EXAMPLES.md (otimizar SELECT N+1, adicionar index)
└── TROUBLESHOOTING.md (query muito lenta, index não usado)
```

---

## 🚫 Anti-Padrões (Evitar)

### ❌ Arquivo Único Gigante

```
nome-da-skill/
└── SKILL.md (200+ linhas)  # ERRADO!
```

**Por quê:** Carrega tudo sempre, desperdiça tokens.

### ❌ SKILL.md com Documentação Técnica

```markdown
# Skill

## API Documentation
[50 linhas de docs...]  # ERRADO! → Mover para REFERENCE.md
```

### ❌ Sem Exemplos

```
nome-da-skill/
├── SKILL.md
└── REFERENCE.md
# Falta EXAMPLES.md!  # ERRADO!
```

---

## 🎓 Boas Práticas

1. **Mantenha SKILL.md limpo** (30-60 linhas, máx 80)
2. **Use links markdown** para referenciar outros arquivos
3. **Triggers específicos** na description (ativa automaticamente)
4. **Mínimo 2 exemplos** reais e completos
5. **Mínimo 2 erros** documentados com soluções
6. **Atualize continuamente** conforme skill evolui

---

## 🔄 Workflow Completo

```mermaid
1. Pedir para criar skill
   ↓
2. Claude/Script gera estrutura
   ↓
3. Preencher 4 arquivos (.md)
   ↓
4. Validar (checklist)
   ↓
5. Documentar no CLAUDE.md
   ↓
6. Commitar
   ↓
7. Testar ativação automática
   ↓
8. Iterar (adicionar exemplos/erros conforme usar)
```

---

## 📊 Comparação: Antes vs Depois

### ❌ Antes (Arquivo Único)

```
estudar-video/
└── SKILL.md (226 linhas)
    ├─ Instruções (40)
    ├─ Docs técnica (80)
    ├─ Exemplos (50)
    └─ Troubleshooting (30)
```

**Problema:** 226 linhas carregadas sempre!

### ✅ Depois (Progressive Disclosure)

```
estudar-video/
├── SKILL.md (45 linhas) ← Sempre
├── REFERENCE.md (80 linhas) ← Sob demanda
├── EXAMPLES.md (50 linhas) ← Sob demanda
└── TROUBLESHOOTING.md (30 linhas) ← Sob demanda
```

**Benefício:** 45 linhas inicialmente, 205 só se necessário!

---

## 🔗 Recursos Relacionados

- **Skill skill-creator:** `.claude/skills/skill-creator/SKILL.md`
- **Estrutura padrão:** `.claude/skills/skill-creator/STRUCTURE.md`
- **Templates completos:** `.claude/skills/skill-creator/TEMPLATES.md`
- **CLAUDE.md:** Seção "🧠 CLAUDE SKILLS"
- **Docs oficiais:** https://docs.claude.com/en/docs/claude-code/skills.md

---

## 🆘 Troubleshooting

### Script não funciona

```bash
# Verificar permissões
chmod +x scripts/claude-skills/create_skill.py

# Testar
python3 scripts/claude-skills/create_skill.py --help
```

### Claude não detecta skill-creator

1. Verificar se existe: `.claude/skills/skill-creator/SKILL.md`
2. Verificar frontmatter YAML (--- no início e fim)
3. Recarregar janela do Claude Code
4. Testar explicitamente: "Use skill-creator para criar uma skill..."

### Skill criada mas não ativa automaticamente

1. Verificar `description` tem triggers claros
2. Testar com frase exata dos triggers
3. Ativar explicitamente: "Use a skill [nome] para..."

---

## 📝 Contribuindo

### Adicionar Novo Template

1. Criar arquivo em `templates/NOME.md.template`
2. Usar placeholders `{{VARIAVEL}}`
3. Documentar em `TEMPLATES.md`
4. Atualizar script `create_skill.py` se necessário

### Melhorar skill-creator

1. Editar `.claude/skills/skill-creator/SKILL.md`
2. Adicionar exemplos em `.claude/skills/skill-creator/EXAMPLES.md`
3. Documentar erros em `.claude/skills/skill-creator/TROUBLESHOOTING.md`
4. Commitar mudanças

---

**Criado em:** 02/11/2025
**Baseado em:** Documentação oficial Claude Code Skills
**Padrão:** Progressive Disclosure (obrigatório)
**Status:** ✅ Sistema pronto para uso em produção
