# Mapa Completo de Configuração de API Keys - chatbot-template/

## Resumo Executivo
O chatbot-template possui **3 abordagens de configuração**:
1. **Hardcoded** (arquivos Python) - INSEGURO
2. **JSON** (chatwoot_config_automaia.json) - RECOMENDADO
3. **Variáveis de Ambiente** (os.getenv) - FALLBACK

---

## 1. ARQUIVO PRINCIPAL: chatwoot_config_automaia.json
**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/chatbot-template/chatwoot_config_automaia.json`

**Estrutura atual:**
```json
{
  "chatwoot": {
    "url": "https://chatwoot.loop9.com.br",
    "token": "xp1AcWvf6F2p2ZypabNWHfW6",
    "account_id": "1",
    "inbox_id": "42"
  },
  "evolution": {
    "url": "https://evolution.loop9.com.br",
    "api_key": "178e43e1c4f459527e7008e57e378e1c",
    "instance": "automaia"
  },
  "google_sheet_id": "1OgPgNRVcnWtKePR54tKVQohchxwELiUsi5UTYoqVUfg"
}
```

### O que está aqui:
| Campo | Tipo | Usado em | Descrição |
|-------|------|----------|-----------|
| `chatwoot.url` | URL | chatbot_automaia_v4.py, webhook_middleware_automaia.py | URL base do Chatwoot |
| `chatwoot.token` | Token | chatbot_automaia_v4.py, webhook_middleware_automaia.py | Token de acesso da API Chatwoot |
| `chatwoot.account_id` | ID | Todos os módulos Chatwoot | ID da conta no Chatwoot |
| `chatwoot.inbox_id` | ID | webhook_middleware_automaia.py | ID da inbox para receber mensagens |
| `evolution.url` | URL | chatbot_automaia_v4.py, webhook_middleware_automaia.py | URL base da Evolution API |
| `evolution.api_key` | Token | chatbot_automaia_v4.py, webhook_middleware_automaia.py, gerar_qrcode.py | Chave da API Evolution |
| `evolution.instance` | String | chatbot_automaia_v4.py, gerar_qrcode.py | Nome da instância WhatsApp |
| `google_sheet_id` | ID | componentes/escalonamento/* | ID da planilha Google Sheets (agenda) |

---

## 2. HARDCODED NO chatbot_automaia_v4.py (INSEGURO!)
**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/chatbot-template/chatbot_automaia_v4.py`

### Linhas 40-58 - Configurações Críticas:
```python
# ⚠️ INSECURO: Hardcoded na linha 40-41
OPENROUTER_API_KEY = "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"
OPENAI_API_KEY = "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"

# ⚠️ INSECURO: Hardcoded na linha 56-57 (Redis Upstash)
redis = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
)
```

### Detalhes do Hardcoded:

| API | Chave | Localização | Tipo | Status |
|-----|-------|-------------|------|--------|
| OpenRouter | `sk-or-v1-...` | linha 40 | LLM | HARDCODED |
| OpenAI | `sk-proj-...` | linha 41 | Whisper + Vision | HARDCODED |
| Redis Upstash | URL + Token | linhas 56-57 | Cache de Conversas | HARDCODED |
| Chatwoot Config | Carregado de JSON | linha 44-52 | Config | JSON ✅ |
| Evolution Config | Carregado de JSON | linha 50-52 | WhatsApp | JSON ✅ |

---

## 3. VARIÁVEIS DE AMBIENTE (Fallback)
**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/chatbot-template/componentes/escalonamento/chatwoot_integration.py`

### Suporta getenv como fallback (linhas 26-28):
```python
if chatwoot_config:
    self.api_url = chatwoot_config.get('url', '').rstrip('/')
    self.api_token = chatwoot_config.get('token', '')
    self.account_id = chatwoot_config.get('account_id', '')
else:
    # Fallback para variáveis de ambiente
    self.api_url = os.getenv('CHATWOOT_API_URL', '').rstrip('/')
    self.api_token = os.getenv('CHATWOOT_API_TOKEN', '')
    self.account_id = os.getenv('CHATWOOT_ACCOUNT_ID', '')
```

### Variáveis de Ambiente Suportadas:
| Variável | Módulo | Valor Esperado | Descrição |
|----------|--------|----------------|-----------|
| `CHATWOOT_API_URL` | chatwoot_integration.py | https://... | URL do Chatwoot |
| `CHATWOOT_API_TOKEN` | chatwoot_integration.py | Token String | Token API |
| `CHATWOOT_ACCOUNT_ID` | chatwoot_integration.py | Número | ID da conta |

---

## 4. GOOGLE CREDENTIALS (OAuth)
**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/chatbot-template/componentes/escalonamento/config/google_credentials.json`

**Arquivo de credenciais OAuth:**
```json
{
  "web": {
    "client_id": "386950317415-kr0n7vr4a99t5e0v2vk4lnosdhrcumk2.apps.googleusercontent.com",
    "project_id": "n8n-auto-451514",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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"
  }
}
```

**Uso:**
- Script: `componentes/escalonamento/autenticar_google.py`
- Salva token em: `config/google_token.pickle`
- Usado para: Acesso ao Google Sheets (agenda)

---

## 5. REDIS UPSTASH (Hardcoded em sistema_followup.py)
**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/chatbot-template/componentes/followup/sistema_followup.py`

**Linhas 16-22:**
```python
# ⚠️ INSECURO: Hardcoded
REDIS_HOST = "usw1-popular-stallion-42128.upstash.io"
REDIS_PORT = 42128
REDIS_PASSWORD = "AaEoAAIjcDFiODk5OWQ5ZjdiOTY0NmM4OWNkZTI2YzI3NTU3NGI5YnAxMA"

EVOLUTION_URL = "https://megatalk.com.br"
EVOLUTION_INSTANCE = "lfimoveis"
EVOLUTION_API_KEY = "6C60BE7E-A2D7-4EF3-8BA4-E4C050"
```

---

## 6. RESUMO POR TIPO DE API

### 🤖 LLMs e Modelos
| API | Onde está | Formato | Status | Necessária |
|-----|-----------|---------|--------|-----------|
| OpenAI (Whisper + GPT-4o) | chatbot_automaia_v4.py:41 | Hardcoded | INSEGURO | SIM |
| OpenRouter | chatbot_automaia_v4.py:40 | Hardcoded | INSECURO | SIM |

### 💬 WhatsApp / Chat
| API | Onde está | Formato | Status | Necessária |
|-----|-----------|---------|--------|-----------|
| Evolution API Key | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |
| Evolution URL | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |
| Evolution Instance | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |
| Chatwoot Token | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |
| Chatwoot URL | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |
| Chatwoot Account ID | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |
| Chatwoot Inbox ID | chatwoot_config_automaia.json | JSON | SEGURO ✅ | SIM |

### 💾 Cache / Persistência
| API | Onde está | Formato | Status | Necessária |
|-----|-----------|---------|--------|-----------|
| Upstash Redis (chatbot_automaia_v4.py) | chatbot_automaia_v4.py:56 | Hardcoded | INSEGURO | SIM |
| Upstash Redis (sistema_followup.py) | sistema_followup.py:16 | Hardcoded | INSECURO | SIM |

### 📅 Agendamento
| API | Onde está | Formato | Status | Necessária |
|-----|-----------|---------|--------|-----------|
| Google Sheets ID | chatwoot_config_automaia.json | JSON | SEGURO ✅ | NÃO (mock) |
| Google OAuth Credentials | google_credentials.json | JSON | SEGURO ✅ | NÃO (mock) |
| Google OAuth Token | config/google_token.pickle | Pickle | SEGURO ✅ | NÃO |

---

## 7. FLUXO DE CARREGAMENTO

```
┌─ chatbot_automaia_v4.py inicia
│
├─► Carrega chatwoot_config_automaia.json
│   ├─ Chatwoot: url, token, account_id, inbox_id
│   ├─ Evolution: url, api_key, instance
│   └─ Google Sheets ID (opcional)
│
├─► Hardcoded no código:
│   ├─ OPENROUTER_API_KEY
│   ├─ OPENAI_API_KEY
│   └─ Redis: url + token (Upstash)
│
├─► Inicializa Orquestrador
│   ├─► RAGSimplesCarros (recebe api_keys)
│   ├─► IntegradorScore (recebe chatwoot_config)
│   ├─► IntegradorFollowUp
│   │   └─► Sistema de Follow-up.py (hardcoded Redis)
│   ├─► IntegradorEscalonamento
│   │   └─► Chatwoot Integration (usa getenv fallback)
│   │   └─► Google Auth (carrega google_credentials.json)
│   └─► IntegradorMetricas
│
└─► Inicia webhook em /webhook/chatwoot
```

---

## 8. CHECKLIST DE CONFIGURAÇÃO NECESSÁRIA

### Para usar o chatbot-template:

- [ ] **Editar chatwoot_config_automaia.json:**
  - [ ] `chatwoot.url` - URL do seu Chatwoot
  - [ ] `chatwoot.token` - Token da API
  - [ ] `chatwoot.account_id` - ID da conta
  - [ ] `chatwoot.inbox_id` - ID da inbox
  - [ ] `evolution.url` - URL da Evolution API
  - [ ] `evolution.api_key` - API Key da Evolution
  - [ ] `evolution.instance` - Nome da instância
  - [ ] `google_sheet_id` - (Opcional) ID da planilha

- [ ] **Editar chatbot_automaia_v4.py (INSEGURO):**
  - [ ] Linha 40: `OPENROUTER_API_KEY`
  - [ ] Linha 41: `OPENAI_API_KEY`
  - [ ] Linhas 56-57: Redis URL e Token

- [ ] **Editar sistema_followup.py (INSEGURO):**
  - [ ] Linhas 16-22: Redis credentials
  - [ ] Linhas 20-21: Evolution URL e Instance
  - [ ] Linha 22: Evolution API Key

- [ ] **Adicionar google_credentials.json:**
  - [ ] Copiar credenciais OAuth do Google Cloud
  - [ ] Ou executar: `python3 componentes/escalonamento/autenticar_google.py`

---

## 9. PROBLEMAS DE SEGURANÇA IDENTIFICADOS

### 🚨 Crítico - Hardcoded Keys
1. **chatbot_automaia_v4.py:40-41** - OpenAI + OpenRouter keys
2. **chatbot_automaia_v4.py:56-57** - Redis credentials
3. **sistema_followup.py:16-22** - Redis + Evolution credentials

### ⚠️ Alto - Sem validação
- Sem `.env` file support
- Sem verificação de keys faltantes
- Sem erro clara quando API key inválida

### Recomendação:
Migrar para arquivo `.env` com `python-dotenv`

---

## 10. ARQUIVOS RELACIONADOS

| Arquivo | Função | Configurações |
|---------|--------|---------------|
| `chatbot_automaia_v4.py` | Bot principal | OPENAI, OPENROUTER, Redis |
| `webhook_middleware_automaia.py` | Middleware Chatwoot | Chatwoot, Evolution |
| `gerar_qrcode.py` | Gera QR code | Evolution |
| `setup_chatwoot.py` | Setup inicial | Chatwoot |
| `chatwoot_config_automaia.json` | Config centralizada | Todas as APIs |
| `componentes/escalonamento/chatwoot_integration.py` | Escalonamento | Chatwoot (getenv fallback) |
| `componentes/escalonamento/autenticar_google.py` | OAuth Google | Google |
| `componentes/followup/sistema_followup.py` | Follow-ups | Redis, Evolution |
| `componentes/rag_simples_carros.py` | RAG | OpenAI, OpenRouter |
| `componentes/config/google_credentials.json` | OAuth Creds | Google |

---

## 11. ESTRUTURA DE DIRETÓRIOS

```
chatbot-template/
├── chatwoot_config_automaia.json          ← ARQUIVO PRINCIPAL DE CONFIG
├── chatbot_automaia_v4.py                 ← Hardcoded: OpenAI, OpenRouter, Redis
├── webhook_middleware_automaia.py
├── gerar_qrcode.py
├── setup_chatwoot.py
├── config/
│   └── google_credentials.json            ← Google OAuth
├── componentes/
│   ├── rag_simples_carros.py
│   ├── orquestrador_carros.py
│   ├── escalonamento/
│   │   ├── autenticar_google.py
│   │   ├── chatwoot_integration.py        ← Usa getenv fallback
│   │   ├── config/
│   │   │   └── google_credentials.json
│   │   └── ...
│   ├── followup/
│   │   ├── sistema_followup.py            ← Hardcoded: Redis, Evolution
│   │   └── ...
│   └── ...
└── carros/                                 ← Dados dos produtos (links.json)
```

---

## 12. MATRIZ RÁPIDA DE REFERÊNCIA

| O que preciso? | Onde configurar? | Formato | Segurança |
|---|---|---|---|
| Chatwoot + Evolution | `chatwoot_config_automaia.json` | JSON | ✅ Bom |
| OpenAI + OpenRouter | `chatbot_automaia_v4.py` linha 40-41 | Hardcoded | 🔴 Perigoso |
| Redis (chatbot_automaia_v4) | `chatbot_automaia_v4.py` linha 56-57 | Hardcoded | 🔴 Perigoso |
| Redis (followup) | `sistema_followup.py` linha 16-22 | Hardcoded | 🔴 Perigoso |
| Google Sheets | `chatwoot_config_automaia.json` | JSON | ✅ Bom |
| Google OAuth | `config/google_credentials.json` | JSON | ✅ Bom |
| Chatwoot (fallback) | ENV vars | getenv() | ⚠️ Não usado |

---

## PRÓXIMOS PASSOS RECOMENDADOS

1. Criar `.env` file na raiz do projeto
2. Migrar todas as chaves hardcoded para `.env`
3. Usar `python-dotenv` para carregar
4. Implementar validação de chaves obrigatórias
5. Documentar cada API necessária
6. Criar script de validação de setup
