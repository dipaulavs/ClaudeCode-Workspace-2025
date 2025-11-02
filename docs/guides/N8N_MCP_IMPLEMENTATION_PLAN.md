# 🚀 PLANO DE IMPLEMENTAÇÃO: n8n-MCP com Claude Code

## 📋 RESUMO EXECUTIVO

Este plano detalha como configurar o **n8n-MCP Server** para criar workflows do n8n automaticamente através do Claude Code usando prompts naturais.

**Fonte:** https://www.youtube.com/watch?v=d3bWvva6ucw
**Repositório:** https://github.com/czlonkowski/n8n-mcp

---

## 🎯 O QUE VOCÊ VAI CONSEGUIR

Depois de implementar este plano, você poderá:

- ✅ Criar workflows do n8n usando prompts em linguagem natural
- ✅ Automatizar a geração de agentes AI, automações e integrações
- ✅ Acessar 541 nodes do n8n com documentação completa
- ✅ Usar 3000+ templates como referência
- ✅ Construir diretamente na sua instância n8n (sem copiar JSON)

**Taxa de sucesso esperada:**
- Workflows simples: ~100% (one-shot)
- Workflows médios: ~80% (ajustes mínimos)
- Workflows complexos: ~50% (base sólida)

---

## 📊 PRÉ-REQUISITOS

### ✅ Você JÁ TEM
- [x] Claude Code instalado e funcionando
- [x] Python 3.9+ instalado
- [x] Workspace configurado

### ⚠️ Você PRECISA TER
- [ ] Instância n8n (self-hosted ou cloud)
  - Opções: Hostinger, Railway, Docker local, n8n.cloud
- [ ] Node.js instalado (para NPX)
  - Verificar: `node --version`
- [ ] Acesso admin ao n8n para criar API key

### 🔍 Verificação Rápida

Execute para verificar Node.js:
```bash
node --version
npm --version
```

Se não tiver Node.js, instale:
- **macOS:** `brew install node`
- **Windows:** https://nodejs.org/
- **Linux:** `sudo apt install nodejs npm`

---

## 📝 PLANO DE IMPLEMENTAÇÃO

### **FASE 1: PREPARAÇÃO DO N8N** ⏱️ 10-15 minutos

#### 1.1 - Acesse sua instância n8n
- [ ] Abra o n8n no navegador
- [ ] Faça login com suas credenciais
- [ ] Anote a URL completa (ex: `https://n8n-server.hostinger.com`)

#### 1.2 - Criar API Key
- [ ] No n8n, clique em **Settings** (canto inferior esquerdo)
- [ ] Clique em **n8n API**
- [ ] Clique em **Create an API Key**
- [ ] Configure:
  - **Nome:** `Claude-Code-MCP` (ou qualquer nome)
  - **Scopes:** Selecione TODOS os scopes disponíveis
  - **Expiration:** Configure conforme preferência (recomendado: sem expiração ou 1 ano)
- [ ] Clique em **Create**
- [ ] **COPIE a API Key** (só aparece uma vez!)
- [ ] Cole temporariamente em um arquivo seguro

**⚠️ IMPORTANTE:** Guarde esta API key em local seguro. Ela não será mostrada novamente!

---

### **FASE 2: CONFIGURAÇÃO DO PROJETO CLAUDE CODE** ⏱️ 5 minutos

#### 2.1 - Criar pasta do projeto
```bash
cd ~/Desktop/ClaudeCode-Workspace
mkdir n8n-mcp-project
cd n8n-mcp-project
```

#### 2.2 - Criar arquivo de configuração MCP

**Se você está no macOS/Linux:**

Crie o arquivo `.mcp.json`:
```bash
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "SUA_URL_DO_N8N_AQUI",
        "N8N_API_KEY": "SUA_API_KEY_AQUI"
      }
    }
  }
}
EOF
```

**Se você está no Windows:**

Crie o arquivo `.mcp.json` com este conteúdo:
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "cmd",
      "args": ["/c", "npx", "n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "SUA_URL_DO_N8N_AQUI",
        "N8N_API_KEY": "SUA_API_KEY_AQUI"
      }
    }
  }
}
```

#### 2.3 - Editar o arquivo com suas credenciais
- [ ] Abra `.mcp.json` no editor
- [ ] Substitua `SUA_URL_DO_N8N_AQUI` pela URL do seu n8n
  - Exemplo: `https://n8n-server.hostinger.com`
  - **IMPORTANTE:** Remova a barra `/` no final da URL
- [ ] Substitua `SUA_API_KEY_AQUI` pela API key copiada anteriormente
- [ ] Salve o arquivo

**Exemplo de configuração final:**
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "https://n8n-server.hostinger.com",
        "N8N_API_KEY": "n8n_api_1234567890abcdefghijklmnopqrstuvwxyz"
      }
    }
  }
}
```

---

### **FASE 3: CONFIGURAÇÃO DO CLAUDE CODE** ⏱️ 3 minutos

#### 3.1 - Iniciar Claude Code no projeto
```bash
# Certifique-se de estar na pasta do projeto
cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project

# Inicie o Claude Code
claude-code
```

#### 3.2 - Detectar o MCP Server
Quando o Claude Code iniciar, você deve ver a mensagem:
```
🔌 New MCP server found: n8n-mcp
```

Se não aparecer, reinicie o Claude Code.

#### 3.3 - Criar arquivo de instruções do projeto
No Claude Code, digite:
```
/init
```

Isso criará o arquivo `claude.md`.

#### 3.4 - Adicionar instruções do n8n-MCP

**Copie o conteúdo abaixo e cole no arquivo `claude.md`:**

```markdown
# n8n-MCP Claude Code Instructions

## Overview
This project uses the n8n-MCP server to create and manage n8n workflows through natural language prompts.

## How to Use n8n-MCP

### Available Tools
- `list_nodes`: Get all available n8n nodes
- `get_node_documentation`: Get detailed documentation for specific nodes
- `list_templates`: Browse 3000+ workflow templates
- `create_workflow`: Create new workflows on n8n instance
- `update_workflow`: Modify existing workflows
- `get_workflow`: Retrieve workflow details

### Best Practices

1. **Always use Plan Mode for complex workflows**
   - Ask clarifying questions before implementation
   - Break down complex automations into phases
   - Validate approach with user before building

2. **Start with node discovery**
   - Use `list_nodes` to see available options
   - Check `get_node_documentation` for specific nodes
   - Search `list_templates` for similar workflows

3. **Iterative approach**
   - Start simple, test, then enhance
   - Build workflows in logical phases
   - Test each phase before moving forward

4. **When creating workflows:**
   - Use descriptive names
   - Add helpful notes to nodes
   - Set up error handling
   - Configure proper credentials

### Workflow Complexity Guidelines

**Simple workflows** (1-5 nodes):
- Can usually be one-shotted
- Direct prompt is fine

**Medium workflows** (5-15 nodes):
- Use plan mode
- Ask for clarification on integrations
- Check templates for similar patterns

**Complex workflows** (15+ nodes):
- ALWAYS use plan mode
- Break into multiple phases
- Ask detailed questions about:
  - Data sources
  - Transformation requirements
  - Error handling needs
  - Scheduling preferences

### Example Prompts

**Good prompts:**
- "Create a chatbot using OpenAI with memory and Wikipedia tool"
- "Build a daily newsletter that scrapes RSS feeds, summarizes with AI, and emails via Gmail"
- "Set up a form trigger that processes data through multiple APIs and stores in Airtable"

**Better prompts (for complex workflows):**
- "I need a LinkedIn job automation. Let me know what details you need from me before we start."
- "Create a customer onboarding workflow. Ask me about the data sources and integrations first."

### Safety Guidelines

⚠️ **NEVER:**
- Edit production workflows directly
- Run workflows without user review
- Make destructive changes without confirmation

✅ **ALWAYS:**
- Create copies of existing workflows before editing
- Show complete workflow before deploying
- Ask for confirmation before executing
- Suggest testing in development first

## Troubleshooting

If n8n-MCP is not responding:
1. Check if .mcp.json is properly configured
2. Verify N8N_API_URL doesn't have trailing slash
3. Confirm N8N_API_KEY is valid
4. Restart Claude Code

## Project Structure

- `.mcp.json` - MCP server configuration
- `claude.md` - This instruction file
- `workflows/` - Exported workflows (optional)
```

Salve o arquivo e informe o Claude:
```
Take a look at the claude.md file. I just added info on how to use the n8n-mcp server.
```

---

### **FASE 4: TESTES E VALIDAÇÃO** ⏱️ 15-20 minutos

#### 4.1 - Teste Simples (Validação Básica)
No Claude Code, digite:

```
Create a simple chatbot workflow with:
- OpenAI chat model (GPT-4o-mini)
- Simple memory node
- Wikipedia tool
- Manual chat trigger

Use the n8n-mcp server to build this on my n8n instance.
```

**Resultado esperado:**
- Workflow criado automaticamente no n8n
- 4-5 nodes conectados corretamente
- Configuração básica completa

**Checklist de validação:**
- [ ] Workflow apareceu no n8n
- [ ] Todos os nodes estão conectados
- [ ] Configurações básicas estão presentes
- [ ] Nenhum node está vazio

---

#### 4.2 - Teste Médio (Automação com Múltiplas Etapas)
No Claude Code, digite:

```
First, switch to plan mode.

I want to create a daily newsletter automation that:
1. Runs every morning at 8 AM
2. Fetches latest AI news from 3 RSS feeds
3. Summarizes articles with OpenAI
4. Formats as HTML email
5. Sends via Gmail

What information do you need from me?
```

**Resultado esperado:**
- Claude faz perguntas de clarificação
- Apresenta um plano detalhado em fases
- Cria workflow com 8-12 nodes
- ~80% do trabalho concluído

**Checklist de validação:**
- [ ] Trigger de schedule está configurado
- [ ] RSS feeds conectados
- [ ] AI summarization funciona
- [ ] Email formatting existe
- [ ] Gmail node está configurado (pode precisar credenciais)

---

#### 4.3 - Teste Complexo (Workflow Avançado) - OPCIONAL
No Claude Code, digite:

```
Plan mode ON.

Create a job application automation:
1. Form for user to input job preferences
2. Scrape LinkedIn for matching jobs
3. Present results to user for selection
4. For selected jobs, find hiring managers
5. Generate personalized outreach message
6. Create Gmail draft for each

Ask me any questions you need before starting.
```

**Resultado esperado:**
- Muitas perguntas de clarificação
- Plano detalhado em 3-4 fases
- Workflow com 15-20 nodes
- ~50% do trabalho concluído (base sólida)

**Checklist de validação:**
- [ ] Estrutura geral faz sentido
- [ ] Principais integrações estão presentes
- [ ] Human-in-the-loop nodes estão corretos
- [ ] Fluxo lógico está coerente

---

### **FASE 5: OTIMIZAÇÃO E BOAS PRÁTICAS** ⏱️ Contínuo

#### 5.1 - Organize seus workflows
```bash
# No projeto, crie estrutura para exportar workflows
mkdir -p workflows/{production,development,templates}
```

#### 5.2 - Backup de configuração
```bash
# Faça backup do .mcp.json (sem commitar a API key!)
cp .mcp.json .mcp.json.backup
```

#### 5.3 - Gitignore (se usar git)
```bash
cat > .gitignore << 'EOF'
.mcp.json
*.backup
.env
node_modules/
EOF
```

#### 5.4 - Documentação de workflows criados
Mantenha um log dos workflows criados:

```bash
cat > WORKFLOWS_LOG.md << 'EOF'
# Workflows Criados

## [Data] - Nome do Workflow
- **Descrição:**
- **Complexidade:** Simples/Médio/Complexo
- **Status:** Funcionando/Em teste/Precisa ajustes
- **Ajustes necessários:**
- **Prompt usado:**

---
EOF
```

---

## 🎓 DICAS DE USO

### Para Workflows Simples
```
# Pode ir direto
"Create a [descrição simples]"
```

### Para Workflows Médios/Complexos
```
# SEMPRE usar plan mode
"Switch to plan mode. I want to create [descrição]. Ask me what you need."
```

### Melhorando Resultados
1. **Seja específico** sobre:
   - Fontes de dados
   - Triggers (schedule, webhook, manual)
   - Transformações necessárias
   - Output desejado

2. **Mencione integrações** por nome:
   - "Use Gmail" (não "envie email")
   - "Use OpenAI GPT-4o" (não "use AI")
   - "Store in Airtable" (não "salve os dados")

3. **Peça iterações:**
   ```
   "First create the basic structure, then we'll enhance it"
   ```

---

## 🚨 TROUBLESHOOTING

### Problema: MCP Server não conecta

**Checklist:**
- [ ] `.mcp.json` está no diretório correto?
- [ ] URL do n8n está sem barra final?
- [ ] API key é válida?
- [ ] Node.js está instalado? (`node --version`)
- [ ] NPX está acessível? (`npx --version`)

**Solução:**
```bash
# Teste o n8n-mcp diretamente
npx n8n-mcp

# Se funcionar, reinicie Claude Code
```

---

### Problema: Workflow criado mas nodes vazios

**Causa:** Informação insuficiente no prompt

**Solução:**
1. Use plan mode
2. Responda todas as perguntas do Claude
3. Forneça credenciais necessárias manualmente no n8n
4. Use `update_workflow` para refinar

---

### Problema: Erro de permissão no n8n

**Causa:** API key sem scopes suficientes

**Solução:**
1. Volte ao n8n > Settings > n8n API
2. Delete a API key antiga
3. Crie nova com TODOS os scopes
4. Atualize `.mcp.json`
5. Reinicie Claude Code

---

## 📊 MÉTRICAS DE SUCESSO

Você saberá que a implementação funcionou quando:

✅ **Nível 1 - Básico:**
- MCP server conecta no Claude Code
- Consegue criar workflow simples (chatbot)
- Workflow aparece no n8n

✅ **Nível 2 - Intermediário:**
- Consegue criar automações com múltiplas etapas
- Workflows precisam apenas ajustes mínimos
- Usa plan mode efetivamente

✅ **Nível 3 - Avançado:**
- Cria workflows complexos com 50%+ de completude
- Itera sobre workflows existentes
- Combina com seus conhecimentos de n8n

---

## 📚 RECURSOS ADICIONAIS

- **Vídeo original:** https://www.youtube.com/watch?v=d3bWvva6ucw
- **Repositório n8n-mcp:** https://github.com/czlonkowski/n8n-mcp
- **Canal do criador:** @Zlonkowski (4k subs - apoie!)
- **Documentação n8n:** https://docs.n8n.io
- **Claude Code docs:** https://docs.claude.com/claude-code

---

## 🎯 PRÓXIMOS PASSOS

Depois de implementar tudo:

1. **Experimente criar 5 workflows simples** para pegar o jeito
2. **Tente 2-3 automações médias** do seu dia a dia
3. **Documente o que funciona bem** e o que precisa ajuste
4. **Compartilhe seus resultados** (opcional)

---

## ⚡ CHECKLIST FINAL DE IMPLEMENTAÇÃO

### Preparação
- [ ] Node.js instalado
- [ ] Instância n8n acessível
- [ ] API key do n8n criada

### Configuração
- [ ] Pasta `n8n-mcp-project` criada
- [ ] Arquivo `.mcp.json` configurado
- [ ] Credenciais corretas no `.mcp.json`
- [ ] Claude Code detectou o MCP server
- [ ] Arquivo `claude.md` criado e configurado

### Validação
- [ ] Teste simples executado com sucesso
- [ ] Teste médio executado (opcional)
- [ ] Workflows aparecem no n8n
- [ ] Nodes estão configurados

### Próximos Passos
- [ ] Documentar workflows criados
- [ ] Criar estrutura de pastas
- [ ] Configurar backup
- [ ] Experimentar com seus casos de uso

---

## 💬 SUPORTE

Se encontrar problemas:

1. **Verifique o troubleshooting** acima
2. **Consulte o repositório:** https://github.com/czlonkowski/n8n-mcp/issues
3. **Assista o vídeo novamente:** marcador temporal específico
4. **Entre no Discord do n8n:** https://discord.gg/n8n

---

**Tempo total estimado:** 30-45 minutos
**Dificuldade:** Intermediária
**Pré-requisito de conhecimento:** Básico de n8n recomendado (não obrigatório)

**Sucesso!** 🎉 Você agora pode criar workflows do n8n com prompts naturais!
