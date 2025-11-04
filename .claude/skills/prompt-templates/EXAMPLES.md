# 📖 Prompt Templates - Exemplos de Uso

## Exemplo 1: Buscar Template para Security Audit

### Pedido do Usuário
```
Pesquise um template de prompt para auditar vulnerabilidades de segurança no código
```

### Execução da Skill

**1. Identificar Categoria**
- Objetivo: Auditar segurança
- Categoria: 🤖 **Agents** (especialista em Security)

**2. Consultar Fonte**
```python
WebFetch(
    url="https://www.aitmpl.com/agents",
    prompt="Find all agent templates related to security auditing, vulnerability scanning, or code security. List name, description, and use cases."
)
```

**Fallback (se site retornar vazio):**
```python
WebFetch(
    url="https://github.com/davila7/claude-code-templates",
    prompt="Search for security-related agent templates. Extract name, description, and when to use each."
)
```

**3. Apresentar Resultados**
```
🎯 Templates encontrados para auditoria de segurança:

📂 Categoria: Agents

✅ Security Auditor Agent
   → Descrição: Especialista em identificar vulnerabilidades OWASP Top 10
   → Quando usar: Antes de deploy, code review focado em segurança
   → Verifica: SQL injection, XSS, CSRF, auth issues, secrets exposure

✅ Dependency Scanner Agent
   → Descrição: Analisa dependências para CVEs conhecidas
   → Quando usar: Após npm/pip install, atualizações de pacotes
   → Verifica: Versões vulneráveis, licenças incompatíveis

✅ API Security Agent
   → Descrição: Valida endpoints REST/GraphQL
   → Quando usar: Desenvolvimento de APIs públicas
   → Verifica: Rate limiting, auth, input validation, CORS

💡 Como usar:
   npx claude-code-templates@latest
   → Selecione "Agents" → "Security Auditor"

🔗 Mais info: https://www.aitmpl.com/agents
```

---

## Exemplo 2: Buscar Template para Testes Automatizados

### Pedido do Usuário
```
Busque template de prompt para gerar testes unitários automaticamente
```

### Execução da Skill

**1. Identificar Categoria**
- Objetivo: Gerar testes
- Categoria: ⚡ **Commands** (comando customizado)

**2. Consultar Fonte**
```python
WebFetch(
    url="https://www.aitmpl.com/commands",
    prompt="Find command templates for generating tests, test automation, or unit testing. Include command name, description, and usage."
)
```

**3. Apresentar Resultados**
```
🎯 Templates encontrados para geração de testes:

📂 Categoria: Commands

✅ /generate-tests
   → Descrição: Gera testes unitários para funções/classes selecionadas
   → Frameworks suportados: Jest, Vitest, Pytest, JUnit
   → Cobertura: Happy path + edge cases + error handling

✅ /test-suite
   → Descrição: Cria suite completa de testes para arquivo/módulo
   → Quando usar: Novos features sem testes, refactoring
   → Inclui: Unit + integration + mocks

✅ /snapshot-test
   → Descrição: Gera snapshot tests para componentes React/Vue
   → Quando usar: Componentes visuais, rendering consistency
   → Frameworks: Jest snapshots, Storybook

💡 Como usar:
   1. Instale: npx claude-code-templates@latest
   2. Selecione "Commands" → "generate-tests"
   3. Use no Claude Code: /generate-tests [arquivo.js]

🔗 Mais info: https://www.aitmpl.com/commands
```

---

## Exemplo 3: Buscar Template para Integração com Stripe

### Pedido do Usuário
```
Tem algum template de prompt que integra com Stripe para pagamentos?
```

### Execução da Skill

**1. Identificar Categoria**
- Objetivo: Integração externa (Stripe)
- Categoria: 🔌 **MCPs** (Model Context Protocols)

**2. Consultar Fonte**
```python
WebFetch(
    url="https://www.aitmpl.com/mcps",
    prompt="Find MCP templates for Stripe integration. Include setup instructions, available APIs, and use cases."
)
```

**3. Apresentar Resultados**
```
🎯 Templates encontrados para Stripe:

📂 Categoria: MCPs (Model Context Protocols)

✅ Stripe Payment MCP
   → Descrição: Integração completa com Stripe APIs
   → Recursos disponíveis:
      • Criar checkout sessions
      • Gerenciar subscriptions
      • Processar webhooks
      • Consultar transactions
   → Quando usar: E-commerce, SaaS com pagamentos recorrentes

📋 Setup Rápido:
   1. Instale MCP: npx claude-code-templates@latest
   2. Configure API keys (STRIPE_SECRET_KEY)
   3. Teste: "Create checkout session for $29.99 product"

🔐 Segurança:
   • Nunca expor secret key no frontend
   • Validar webhooks com signature
   • Usar ambiente test antes de produção

💡 Como usar no Claude Code:
   "Create a Stripe checkout for product X with price $Y"
   → Claude usa MCP automaticamente

🔗 Mais info: https://www.aitmpl.com/mcps
📚 Stripe Docs: https://stripe.com/docs/api
```

---

## Exemplo 4: Template Não Encontrado (Criar Customizado)

### Pedido do Usuário
```
Pesquise um template de prompt para análise de sentimento em reviews de produtos
```

### Execução da Skill

**1. Identificar Categoria**
- Objetivo: Análise de sentimento
- Categorias possíveis: Agents (NLP specialist) ou Skills (text analysis)

**2. Consultar Fonte**
```python
WebFetch(
    url="https://www.aitmpl.com/agents",
    prompt="Find agents for sentiment analysis, NLP, text analysis, or review processing."
)

WebFetch(
    url="https://www.aitmpl.com/skills",
    prompt="Find skills for text processing, sentiment detection, or customer feedback analysis."
)
```

**3. Resultado: Não Encontrado**

**Apresentar Alternativas:**
```
🔍 Nenhum template específico encontrado para "análise de sentimento".

📂 Templates relacionados (mais próximos):

✅ Text Analyzer Agent
   → Descrição: Analisa estrutura e padrões em texto
   → Uso: Pode ser adaptado para sentimento básico

✅ Data Processing Skill
   → Descrição: Processa datasets estruturados
   → Uso: Pode classificar reviews em lote

💡 Recomendação: Criar skill customizada

🛠️ Opções:
   1. Adaptar "Text Analyzer Agent" manualmente
   2. Criar nova skill: "Quer que eu crie uma skill 'sentiment-analyzer'?"
      → Usaria skill-creator para gerar estrutura
      → Integraria com API de NLP (OpenAI, Hugging Face)

🔗 Explorar todas categorias: https://www.aitmpl.com
```

---

## Exemplo 5: Buscar por Categoria Ampla (Exploração)

### Pedido do Usuário
```
Quais templates de Skills estão disponíveis?
```

### Execução da Skill

**1. Identificar Categoria**
- Objetivo: Listar todos templates de 🎨 **Skills**

**2. Consultar Fonte**
```python
WebFetch(
    url="https://www.aitmpl.com/skills",
    prompt="List ALL available skill templates. For each, provide: name, description, when to use, and key features. Format as markdown list."
)
```

**3. Apresentar Resultados**
```
🎯 Todos os templates de Skills disponíveis:

📂 Categoria: Skills (Capacidades Reutilizáveis)

✅ PDF Processing Skill
   → Quando usar: Extrair texto, tabelas, metadados de PDFs
   → Features: OCR, layout preservation, multi-page

✅ Excel Automation Skill (XLSX)
   → Quando usar: Ler/escrever planilhas, análise de dados
   → Features: Fórmulas, charts, conditional formatting

✅ Image Analysis Skill
   → Quando usar: Detectar objetos, OCR, moderation
   → Features: Vision APIs, batch processing

✅ Workflow Orchestrator Skill
   → Quando usar: Automatizar multi-step tasks
   → Features: Parallel execution, error handling, logging

✅ File Operations Skill
   → Quando usar: Batch rename, format conversion, sync
   → Features: Glob patterns, streaming, validation

... [lista completa]

💡 Como instalar:
   npx claude-code-templates@latest
   → Navegue para "Skills" → selecione desejada

📊 Total: 15+ skills disponíveis
🔗 Ver todos: https://www.aitmpl.com/skills
```

---

## Padrões de Uso

### Padrão 1: Busca Específica
```
Usuário: "Pesquise template para [objetivo específico]"
→ Claude: Identifica categoria → WebFetch → Apresenta top 3 matches
```

### Padrão 2: Busca por Categoria
```
Usuário: "Quais templates de [categoria] existem?"
→ Claude: WebFetch na categoria → Lista todos
```

### Padrão 3: Busca por Keyword
```
Usuário: "Busque templates relacionados a [keyword]"
→ Claude: WebFetch em múltiplas categorias → Agrega resultados
```

### Padrão 4: Não Encontrado
```
Usuário: "Template para [caso raro]"
→ Claude: Busca → Não encontra → Oferece criar via skill-creator
```

---

## Output Consistente

Sempre seguir formato:
```
🎯 Templates encontrados para [objetivo]:

📂 Categoria: [nome]

✅ Template Name
   → Descrição: [resumo]
   → Quando usar: [contexto]
   → Features/Recursos: [lista]

💡 Como usar: [comandos]
🔗 Mais info: [link]
```

---

**Versão:** 1.0
**Total de Exemplos:** 5
