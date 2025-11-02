# 🤖 n8n-MCP Project

Projeto de integração do n8n com Claude Code através do n8n-MCP server.

## 📊 Status

✅ **Configuração completa**
- MCP server configurado
- Credenciais do n8n conectadas
- Instruções carregadas no Claude Code

## 🔗 Instância n8n

**URL:** https://n8n.loop9.com.br

## 🛠️ Estrutura do Projeto

```
n8n-mcp-project/
├── .mcp.json              # Configuração do MCP server (NÃO commitar!)
├── claude.md              # Instruções para o Claude Code
├── .gitignore            # Arquivos ignorados pelo git
├── README.md             # Este arquivo
├── workflows/            # Workflows exportados
│   ├── production/      # Workflows em produção
│   ├── development/     # Workflows em desenvolvimento
│   └── templates/       # Templates reutilizáveis
└── docs/                # Documentação dos workflows
```

## 🚀 Como Usar

### Iniciar Claude Code neste projeto

```bash
cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project
claude-code
```

### Verificar conexão com n8n-MCP

O Claude Code deve detectar automaticamente o MCP server ao iniciar.
Você verá: `🔌 New MCP server found: n8n-mcp`

### Exemplos de Comandos

**Criar workflow simples:**
```
Crie um chatbot simples com OpenAI e Wikipedia
```

**Listar workflows existentes:**
```
Liste todos os workflows na instância
```

**Criar workflow complexo:**
```
Modo de planejamento: Preciso criar uma automação de newsletter diária. O que você precisa saber?
```

## ⚠️ Regras de Segurança

### 🚫 CRÍTICO: Exclusão de Workflows

**NUNCA exclua workflows sem confirmação explícita do usuário.**

Esta regra está codificada no `claude.md` e o Claude Code sempre pedirá confirmação antes de qualquer operação destrutiva.

### ✅ Melhores Práticas

- Sempre use "plan mode" para workflows complexos
- Teste em desenvolvimento antes de produção
- Crie backups antes de editar workflows existentes
- Use nomes descritivos em português
- Documente workflows criados

## 🤖 Bot WhatsApp + Chatwoot (Integração Híbrida)

### 📊 Visão Geral

Sistema híbrido que combina **atendimento automatizado** (bot IA) com **atendimento humano** (Chatwoot):
- 🤖 Bot responde automaticamente quando não há atendente
- 👤 Atendente assume quando necessário (bot pausa)
- ✅ Bot volta quando conversa é resolvida

### ⚙️ Arquitetura

```
Cliente (WhatsApp)
    ↓
Evolution API (https://evolution.loop9.com.br)
    ↓
Middleware (porta 5002) → Chatwoot (https://chatwoot.loop9.com.br)
    ↓
Bot V4 (porta 5001) → Evolution API → Cliente
```

### 🎯 Recursos do Bot V4

**Debounce Inteligente:**
- ⏳ 15s aguarda agrupar mensagens do mesmo usuário
- 🧠 Análise IA verifica se mensagem está completa
- ⏱️ +50s aguarda mais se mensagem incompleta (1x apenas)
- 📦 Fila no Redis agrupa mensagens por número

**Resposta Humanizada:**
- ✂️ Mensagens picotadas (1-2 frases por vez)
- ⏱️ Delay entre partes (1.5-3s)
- 😊 Linguagem casual com emojis
- 🎭 Personalidade: Ricardo (corretor descontraído)

**IA & Contexto:**
- 🤖 Claude Haiku 4.5 via OpenRouter
- 💾 Contexto de 14 dias no Redis
- 🧠 Análise de completude com IA
- 📝 Histórico de até 30 mensagens

**Inteligência Híbrida:**
- 👤 Detecta quando atendente assume → Bot pausa
- ✅ Detecta quando conversa é resolvida → Bot retorna
- 🔄 Sem loop (responde direto via Evolution API)

### 🚀 Como Usar

**Iniciar tudo:**
```bash
# Inicia Bot V4 + Middleware + Ngrok
./INICIAR_V2.sh
```

**Parar tudo:**
```bash
./PARAR_V2.sh
```

**Monitorar logs:**
```bash
# Bot V4
tail -f logs/chatbot_v4.log

# Middleware
tail -f logs/middleware_v3.log
```

**Verificar status:**
```bash
curl http://localhost:5001/health  # Bot
curl http://localhost:5002/health  # Middleware
```

### 📁 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `chatbot_corretor_v4.py` | Bot completo com debounce + IA |
| `webhook_middleware_v2.py` | Ponte Evolution ↔ Chatwoot |
| `chatwoot_config.json` | Configurações (tokens, URLs) |
| `configurar_webhook.py` | Configura webhook Evolution |

### 🔧 Configuração

**Dados da Integração:**
- Evolution API: `https://evolution.loop9.com.br`
- Instância: `lfimoveis`
- Chatwoot: `https://chatwoot.loop9.com.br`
- Inbox: `LF IMOVEIS` (ID: 40)
- Número teste: `5531980160822`

**Webhooks:**
- Evolution → Middleware: `/webhook/evolution`
- Chatwoot → Middleware: `/webhook/chatwoot`
- Middleware → Bot V4: `http://localhost:5001/webhook/chatwoot`

### 📊 Performance

- Latência total: ~2.5-3.5s (receber → responder)
- Debounce: 15-65s (depende da análise)
- Custo IA: ~$0.60/mês (1000 mensagens)

### 📝 Documentação Completa

- **Guia completo:** `INTEGRACAO_HIBRIDA_README.md`
- **Mudanças V2:** `V2_MUDANCAS.md`
- **Chatbot original:** `CHATBOT_CORRETOR_README.md`

---

## 📚 Recursos

- **Vídeo Tutorial:** https://www.youtube.com/watch?v=d3bWvva6ucw
- **Repositório n8n-mcp:** https://github.com/czlonkowski/n8n-mcp
- **Plano de Implementação:** `../N8N_MCP_IMPLEMENTATION_PLAN.md`

## 🔧 Troubleshooting

### MCP server não conecta

```bash
# Testar conexão manual
npx n8n-mcp

# Verificar configurações
cat .mcp.json

# Reiniciar Claude Code
```

### Erro de API

1. Verifique se a URL não tem barra final: `https://n8n.loop9.com.br` ✅
2. Confirme se a API key é válida
3. Verifique se a API key tem todos os scopes necessários

## 📊 Workflows Criados

Documente aqui os workflows criados:

### [Data] - Nome do Workflow
- **ID:** workflow_id
- **Descrição:**
- **Status:**
- **Notas:**

---

## 📋 Resumo do Projeto

**n8n-MCP:**
- ✅ MCP server configurado
- ✅ Workflows criados via Claude Code
- 🔗 Instância: https://n8n.loop9.com.br

**Bot WhatsApp Híbrido:**
- ✅ Bot V4 completo (debounce + IA)
- ✅ Integração Evolution + Chatwoot
- 🤖 Atendimento automático + humano
- 📱 Número: 5531980160822

**Última atualização:** 01 de Novembro de 2025
**Instância n8n:** https://n8n.loop9.com.br
**Instância Chatwoot:** https://chatwoot.loop9.com.br
