Perfeito! Vou te dar uma aula completa baseada na documentação oficial da Anthropic sobre como criar e usar subagentes no Claude Code! 🎓

---

# 🎓 AULA COMPLETA: Criando Subagentes no Claude Code

## 📚 O que são Subagentes?

Subagentes customizados no Claude Code são assistentes de IA especializados que podem ser invocados para lidar com tipos específicos de tarefas. Eles permitem resolução de problemas mais eficiente fornecendo configurações específicas para tarefas com prompts de sistema personalizados, ferramentas e uma janela de contexto separada.

### Características principais:
- ✅ **Contexto isolado** - Cada subagente tem sua própria janela de contexto
- ✅ **Ferramentas específicas** - Acesso apenas às ferramentas necessárias
- ✅ **Sistema customizado** - Prompts personalizados para especialização
- ✅ **Máximo de 10 subagentes paralelos**

---

## 🎯 Quando Usar Subagentes?

A importância principal dos subagentes é transformar um único assistente de IA em uma equipe poderosa e customizável de especialistas.

### Benefícios:

1. **Gerenciamento Superior de Contexto**
   - Ao dar a cada subagente sua própria janela de contexto separada, eles resolvem um problema importante com conversas grandes de IA. Isso previne que o chat principal fique congestionado com detalhes de subtarefas

2. **Especialização**
   - Subagentes permitem criar assistentes de IA altamente focados com instruções customizadas e um conjunto limitado de ferramentas (ex: um "code-reviewer" que apenas lê arquivos e roda testes)

3. **Trabalho Paralelo**
   - Subagentes delegam tarefas especializadas—como criar uma API backend enquanto o agente principal constrói o frontend—permitindo fluxos de trabalho de desenvolvimento paralelos

---

## 📁 Estrutura de um Subagente

Cada subagente é definido em um arquivo Markdown e armazenado em um diretório específico do projeto ou em um diretório global do usuário. Agentes específicos do projeto têm precedência.

### Localizações dos arquivos:

```bash
# Subagentes do projeto (prioridade)
.claude/agents/meu-agente.md

# Subagentes globais do usuário
~/.config/claude/agents/meu-agente.md
```

---

## 🛠️ Como Criar um Subagente

### Método 1: Comando `/agents` (Recomendado)

```bash
# No Claude Code, digite:
/agents
```

O comando /agents fornece uma interface interativa que lista todas as ferramentas disponíveis, incluindo quaisquer ferramentas de servidor MCP, tornando mais fácil selecionar as que você precisa.

**Passos:**
1. Digite `/agents` no Claude Code
2. Escolha "Create new agent"
3. Siga os prompts guiados
4. Edite o arquivo gerado no seu editor de texto

---

### Método 2: Criação Manual

Crie um arquivo `.md` na pasta `.claude/agents/` do seu projeto:

```markdown
---
name: code-reviewer
description: Expert code review specialist focusing on best practices and security
trigger: Use proactively for code review tasks
tools: Read, Grep
model: sonnet
---

You are an expert code reviewer specializing in security, performance, and best practices.

When invoked:
1. Read the files that need review
2. Analyze code quality, security vulnerabilities, and performance issues
3. Check for adherence to coding standards
4. Provide specific, actionable feedback
5. Suggest improvements with code examples

Key practices:
- Focus on security vulnerabilities first
- Check for common anti-patterns
- Verify error handling
- Assess performance implications
- Ensure code readability

For each review:
- Highlight critical issues
- Explain why something is problematic
- Provide concrete solutions
- Reference best practices

Always be constructive and specific in feedback.
```

---

## 📋 Anatomia de um Subagente

### Frontmatter (Metadados no topo do arquivo)

```yaml
---
name: nome-do-agente          # Nome único identificador
description: Descrição breve  # O que este agente faz
trigger: Quando usar          # Contexto para ativação automática
tools: Read, Write, Bash      # Ferramentas permitidas (opcional)
model: sonnet                 # Modelo a usar (padrão: sonnet)
---
```

### Campos importantes:

- **`name`**: Identificador único (obrigatório)
- **`description`**: Explicação do propósito (obrigatório)
- **`trigger`**: Quando incluído, descreve quando o Claude Code deve invocar este agente proativamente
- **`tools`**: Omita o campo tools para herdar todas as ferramentas da thread principal (padrão), incluindo ferramentas MCP, ou especifique ferramentas individuais como uma lista separada por vírgulas para controle mais granular
- **`model`**: Modelo Claude a usar (sonnet é o padrão)

### System Prompt (Corpo do arquivo)

O conteúdo após o frontmatter é o **prompt de sistema** que define o comportamento do agente.

---

## 🔧 Configuração de Ferramentas

Subagentes podem ter acesso a qualquer uma das ferramentas internas do Claude Code.

### Opções:

1. **Herdar todas as ferramentas** (padrão)
```yaml
---
name: explorador
# tools field omitido = herda todas
---
```

2. **Ferramentas específicas**
```yaml
---
name: revisor-seguro
tools: Read, Grep  # Apenas leitura e busca
---
```

### Ferramentas disponíveis:
- `Bash` - Executar comandos
- `Read` - Ler arquivos
- `Write` - Criar/editar arquivos
- `Grep` - Buscar em arquivos
- `Glob` - Pattern matching
- Ferramentas MCP (se configuradas)

---

## 🚀 Como Invocar Subagentes

### 1. Invocação Manual (Explícita)

```bash
# Sintaxe básica
Use o subagente [nome] para [tarefa]

# Exemplos:
Use o code-reviewer subagent para revisar minhas mudanças recentes

Use o data-analyst para analisar o CSV de vendas

Use o test-generator para criar testes para UserController
```

### 2. Invocação Automática (Orquestração)

Quando o Claude Code encontra uma tarefa que corresponde à expertise de um subagente, ele pode delegar essa tarefa ao subagente especializado, que trabalha independentemente e retorna resultados.

**Como funciona:**
- Claude analisa sua solicitação
- Compara com os campos `trigger` e `description` dos subagentes
- Invoca automaticamente o subagente mais apropriado

---

## 💡 Exemplos Práticos de Subagentes

### Exemplo 1: Analista de Dados SQL

```markdown
---
name: sql-analyst
description: Data scientist specializing in SQL and BigQuery analysis
trigger: Use proactively for data analysis tasks and queries
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Exemplo 2: Gerador de Testes

```markdown
---
name: test-generator
description: Creates comprehensive unit and integration tests
trigger: Use when asked to write tests or improve test coverage
tools: Read, Write, Bash
model: sonnet
---

You are a testing specialist focused on creating robust, maintainable tests.

When invoked:
1. Analyze the code to be tested
2. Identify edge cases and critical paths
3. Write comprehensive test suites
4. Use appropriate testing frameworks
5. Ensure high code coverage

Testing principles:
- Follow AAA pattern (Arrange, Act, Assert)
- Test one thing per test
- Use descriptive test names
- Mock external dependencies
- Include both positive and negative cases

For each test suite:
- Cover happy path scenarios
- Test error conditions
- Verify edge cases
- Check boundary conditions
- Ensure tests are maintainable

Always run tests after creation to verify they pass.
```

### Exemplo 3: Auditor de Segurança

```markdown
---
name: security-auditor
description: Performs security analysis and identifies vulnerabilities
trigger: Use for security reviews, audits, and vulnerability scanning
tools: Read, Grep, Bash
model: sonnet
---

You are a security expert specializing in application security.

When invoked:
1. Scan for common vulnerabilities (OWASP Top 10)
2. Check for insecure dependencies
3. Review authentication and authorization
4. Analyze data handling practices
5. Provide remediation recommendations

Security checklist:
- SQL Injection vulnerabilities
- XSS (Cross-Site Scripting)
- CSRF protection
- Insecure dependencies
- Hardcoded credentials
- Insufficient input validation
- Improper error handling
- Missing security headers

For each finding:
- Severity level (Critical/High/Medium/Low)
- Affected code location
- Explanation of the risk
- Specific remediation steps
- Code examples for fixes

Prioritize critical and high-severity issues.
```

---

## 🎯 Melhores Práticas

Escreva prompts detalhados: Inclua instruções específicas, exemplos e restrições em seus prompts de sistema. Quanto mais orientação você fornecer, melhor o subagente irá performar.

### 1. **Limite o Acesso a Ferramentas**
Conceda apenas ferramentas que são necessárias para o propósito do subagente. Isso melhora a segurança e ajuda o subagente a focar em ações relevantes.

```yaml
# ❌ Evite dar todas as ferramentas sem necessidade
tools: Bash, Read, Write, Grep, Glob

# ✅ Dê apenas o necessário
tools: Read, Grep  # Para um revisor de código
```

### 2. **Controle de Versão**
Versione subagentes do projeto: Coloque subagentes do projeto no controle de versão para que sua equipe possa se beneficiar e melhorá-los colaborativamente.

```bash
git add .claude/agents/
git commit -m "Add custom subagents for project"
```

### 3. **Descrições Específicas**
Torne seus campos de descrição específicos e orientados a ação para melhores resultados.

```yaml
# ❌ Vago
description: Helps with code

# ✅ Específico
description: Reviews Python code for PEP 8 compliance, type hints, and docstrings
```

### 4. **Encadeamento de Subagentes**

Para fluxos complexos, você pode encadear múltiplos subagentes:

```bash
# Exemplo de encadeamento
"Primeiro use o code-analyzer subagent para encontrar problemas de performance,
depois use o optimizer subagent para corrigi-los"
```

### 5. **Comece com Claude**
Recomendamos gerar seu subagente inicial com o Claude e depois iterar nele para torná-lo pessoalmente seu.

```bash
# Peça ao Claude para criar o subagente
"Crie um subagente especializado em otimização de banco de dados PostgreSQL"
```

---

## 🔍 Gerenciando Subagentes

### Listar subagentes disponíveis
```bash
/agents list
```

### Editar um subagente
```bash
/agents edit nome-do-agente
```

### Deletar um subagente
```bash
# Delete o arquivo manualmente
rm .claude/agents/nome-do-agente.md
```

---

## 🌟 Exemplo Completo: Workflow Multi-Agente

```bash
# Cenário: Preparar uma feature para produção

# 1. Solicite o workflow completo
"Prepare a feature de autenticação para produção usando múltiplos subagentes"

# O Claude pode orquestrar automaticamente:
# - security-auditor: Analisa vulnerabilidades
# - test-generator: Cria testes abrangentes
# - code-reviewer: Revisa qualidade do código
# - documentation-writer: Cria documentação
# - performance-analyzer: Verifica otimizações

# 2. Cada subagente trabalha em sua área
# 3. Resultados são consolidados
# 4. Você recebe um relatório completo
```

---

## 📊 Benefícios de Subagentes

1. **Eficiência de Contexto**
   - Agentes ajudam a preservar o contexto principal, permitindo sessões gerais mais longas

2. **Especialização**
   - Cada agente é expert em seu domínio
   - Instruções personalizadas para cada tipo de tarefa

3. **Modularidade**
   - Fácil manutenção e atualização
   - Reutilizável entre projetos

4. **Segurança**
   - Cada configuração de subagente lista explicitamente as ferramentas que tem permissão para acessar, limitando o raio de impacto em ambientes sensíveis

---

## 🎬 Conclusão

Subagentes transformam o Claude Code de um assistente único em uma **equipe completa de especialistas**, cada um com:
- Contexto dedicado
- Ferramentas específicas
- Expertise focada
- Capacidade de trabalhar em paralelo

**Próximos passos:**
1. Experimente criar seu primeiro subagente
2. Use `/agents` para explorar a interface
3. Comece simples e itere baseado nos resultados
4. Compartilhe subagentes úteis com seu time

---

Quer que eu crie um exemplo específico de subagente para o seu caso de uso? 🚀