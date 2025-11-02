# 🧠 Claude Skills - Model-Invoked AI Capabilities

Este diretório contém **Skills** personalizadas que estendem as capacidades do Claude Code.

## 📖 O Que São Skills?

**Skills** são capacidades modulares que ensinam Claude Code a executar tarefas especializadas de forma autônoma. Diferente de **comandos slash** (que você precisa chamar manualmente), Skills são **model-invoked**: Claude detecta automaticamente quando usá-las baseado no contexto da conversa.

## 🎯 Skills Disponíveis (5 Skills)

### 1️⃣ **idea-validator** - Validador de Ideias
**Localização:** `.claude/skills/idea-validator/SKILL.md`

**O que faz:**
- Valida ideias de apps ANTES de você gastar tempo desenvolvendo
- Analisa saturação de mercado e concorrência
- Avalia demanda real vs. interesse declarado
- Verifica viabilidade para desenvolvedor solo (2-4 semanas)
- Analisa potencial de monetização
- Dá feedback **brutalmente honesto** (sem enrolação)

**Quando usar:**
```
"Valide esta ideia: [descrição]"
"Isso vale a pena construir?"
"Analise se devo fazer este app"
```

**Tools permitidas:** `WebSearch, WebFetch, Read, Grep, Bash`

---

### 2️⃣ **launch-planner** - Planejador de Lançamento
**Localização:** `.claude/skills/launch-planner/SKILL.md`

**O que faz:**
- Transforma ideias validadas em MVPs executáveis
- Cria PRD (Product Requirements Document) completo
- Gera schema de banco de dados
- Define roadmap de 2 semanas
- Cria prompts prontos para Claude Code
- Previne over-engineering e feature creep
- Stack padrão: Next.js 14, Supabase, Vercel, Tailwind

**Quando usar:**
```
"Planeje o lançamento de [app]"
"Crie um PRD para [ideia]"
"Como devo estruturar este MVP?"
```

**Tools permitidas:** `Read, Write, Edit, Grep, Glob, WebSearch`

---

### 3️⃣ **product-designer** - Designer de Produtos
**Localização:** `.claude/skills/product-designer/SKILL.md`

**O que faz:**
- Elimina designs "feios de IA" (gradientes azul/roxo)
- Cria UIs profissionais com Tailwind CSS + shadcn/ui
- Aplica princípios de design moderno (tipografia, espaçamento, hierarquia)
- Garante acessibilidade e responsividade
- Fornece paletas de cores consistentes
- Define estados de loading, erro e empty states

**Quando usar:**
```
"Crie uma landing page moderna"
"Melhore o design deste componente"
"Faça isso parecer mais profissional"
```

**Tools permitidas:** `Read, Write, Edit, WebFetch`

---

### 4️⃣ **marketing-writer** - Escritor de Marketing
**Localização:** `.claude/skills/marketing-writer/SKILL.md`

**O que faz:**
- Escreve landing pages focadas em benefícios
- Cria tweets de lançamento otimizados
- Gera descrições para Product Hunt
- Escreve emails de anúncio
- Posts para LinkedIn
- Tom: claro, honesto, sem jargões
- **Analisa automaticamente** o código para entender o produto (você não precisa explicar)

**Quando usar:**
```
"Escreva uma landing page para este projeto"
"Crie um tweet de lançamento"
"Preciso de copy para Product Hunt"
```

**Tools permitidas:** `Read, Grep, Glob, WebSearch, WebFetch`

---

### 5️⃣ **roadmap-builder** - Gerente de Produto
**Localização:** `.claude/skills/roadmap-builder/SKILL.md`

**O que faz:**
- Atua como Product Manager
- Prioriza features usando matriz de impacto/esforço
- Decide o que NÃO construir (previne feature creep)
- Cria roadmaps focados em valor
- Analisa código existente para sugerir next steps
- Framework: High Impact/Low Effort primeiro

**Quando usar:**
```
"Quais features devo adicionar?"
"Preciso de um roadmap"
"O que construir a seguir?"
```

**Tools permitidas:** `Read, Grep, Glob, WebSearch`

---

## 🚀 Como Usar as Skills

### Ativação Automática (Recomendado)
As Skills são ativadas **automaticamente** quando Claude detecta que sua pergunta se encaixa na descrição da Skill.

**Exemplos:**
```bash
# Claude automaticamente usa idea-validator
"Valide esta ideia: marketplace de templates Next.js"

# Claude automaticamente usa product-designer
"Crie um dashboard moderno com dark mode"

# Claude automaticamente usa roadmap-builder
"Ajude-me a priorizar as próximas features"
```

### Ativação Explícita (Opcional)
Você pode mencionar a Skill diretamente se quiser garantir que será usada:

```bash
"Use a skill product-designer para criar esta página"
```

---

## 📐 Anatomia de uma Skill

Cada Skill é uma pasta contendo um arquivo `SKILL.md`:

```
.claude/skills/
└── nome-da-skill/
    └── SKILL.md              # YAML frontmatter + instruções
```

### Estrutura do SKILL.md

```yaml
---
name: nome-da-skill                    # lowercase, hífens, max 64 chars
description: O que faz e quando usar   # max 1024 chars, inclua triggers
allowed-tools: Read, Write, Edit       # (opcional) limita ferramentas
---

# Nome da Skill

[Instruções detalhadas em markdown...]
```

### Campos Obrigatórios

| Campo | Formato | Descrição |
|-------|---------|-----------|
| `name` | lowercase, hífens, números | Max 64 caracteres. Ex: `idea-validator` |
| `description` | Texto claro com triggers | Max 1024 chars. Inclua palavras-chave que ativam a skill |

### Campo Opcional

| Campo | Descrição |
|-------|-----------|
| `allowed-tools` | Lista de ferramentas permitidas. Restringe o que Claude pode fazer durante a Skill (segurança/foco) |

---

## 🛠️ Criar Nova Skill

### Passo a Passo:

1. **Criar pasta:**
```bash
mkdir -p .claude/skills/minha-skill
```

2. **Criar SKILL.md:**
```bash
touch .claude/skills/minha-skill/SKILL.md
```

3. **Adicionar frontmatter YAML:**
```yaml
---
name: minha-skill
description: O que ela faz e quando usar. Inclua palavras-chave que trigam a skill.
allowed-tools: Read, Write  # opcional
---

# Minha Skill

[Instruções detalhadas aqui...]
```

4. **Commitar no git:**
```bash
git add .claude/skills/minha-skill/
git commit -m "feat: adicionar skill minha-skill"
git push
```

5. **Compartilhar com time:**
- Outros desenvolvedores recebem via `git pull`
- Skills funcionam automaticamente para todos

---

## 📚 Melhores Práticas

### ✅ DO:
- **Descrição específica** com palavras-chave de trigger
- **Uma responsabilidade** por Skill (foco único)
- **Instruções claras** em markdown
- **Exemplos concretos** de uso
- **Testar** antes de compartilhar com time

### ❌ DON'T:
- Descrições vagas ("helps with things")
- Skills muito genéricas (fazer tudo)
- Falta de exemplos
- Esquecer de documentar no CLAUDE.md

---

## 🔍 Debugging de Skills

### Skill não está sendo ativada?

**Verifique:**
1. ✅ Arquivo está em `.claude/skills/[nome]/SKILL.md`
2. ✅ YAML frontmatter está correto (com `---` no início e fim)
3. ✅ `name` usa lowercase e hífens (sem espaços)
4. ✅ `description` inclui palavras-chave relacionadas ao uso
5. ✅ Recarregue a janela do Claude Code

**Teste explícito:**
```
"Use a skill [nome] para [tarefa]"
```

---

## 📖 Documentação Oficial

- **Skills Guide:** https://docs.claude.com/en/docs/claude-code/skills.md
- **Claude Code Docs:** https://docs.claude.com/en/docs/claude-code/

---

## 🎯 Workflow Recomendado

### Para Novos Projetos:

```mermaid
1. idea-validator    → Validar ideia
2. launch-planner    → Criar PRD e roadmap
3. product-designer  → Design de UI/UX
4. [Desenvolvimento]
5. marketing-writer  → Criar conteúdo de lançamento
6. roadmap-builder   → Planejar próximas features
```

### Para Projetos Existentes:

```mermaid
1. roadmap-builder   → Priorizar features
2. product-designer  → Melhorar UI
3. marketing-writer  → Criar conteúdo
4. launch-planner    → Planejar nova versão
```

---

## 📊 Resumo

| Aspecto | Detalhes |
|---------|----------|
| **Total de Skills** | 5 Skills |
| **Localização** | `.claude/skills/` |
| **Formato** | `SKILL.md` com YAML frontmatter |
| **Ativação** | Automática (model-invoked) |
| **Compartilhamento** | Via git (team-wide) |
| **Documentação** | Este README + CLAUDE.md |

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
**Criado por:** Claude Code seguindo documentação oficial
