# 🗺️ Matriz Rápida de Configuração - chatbot-template/

**Versão:** 1.0 | **Data:** 2025-11-05 | **Status:** Completo

---

## SUMÁRIO EXECUTIVO (30 segundos)

### O que está feito ✅
- ✅ Chatwoot + Evolution (JSON seguro)
- ✅ Google Sheets (JSON seguro)
- ✅ Validador automático
- ✅ Documentação completa

### O que está inseguro 🔴
- 🔴 OpenAI + OpenRouter (HARDCODED)
- 🔴 Redis Upstash (HARDCODED em 2 arquivos)

**Ação**: Mover para `.env` (ver SETUP_APIS.md)

---

## MATRIZ DE CONFIGURAÇÃO COMPLETA

| # | API/Serviço | Arquivo | Localização | Tipo | Status | Ação |
|---|---|---|---|---|---|---|
| 1 | **Chatwoot URL** | chatwoot_config_automaia.json | `chatwoot.url` | JSON | ✅ | Preenchido |
| 2 | **Chatwoot Token** | chatwoot_config_automaia.json | `chatwoot.token` | JSON | ✅ | Preenchido |
| 3 | **Chatwoot Account ID** | chatwoot_config_automaia.json | `chatwoot.account_id` | JSON | ✅ | Preenchido |
| 4 | **Chatwoot Inbox ID** | chatwoot_config_automaia.json | `chatwoot.inbox_id` | JSON | ✅ | Preenchido |
| 5 | **Evolution URL** | chatwoot_config_automaia.json | `evolution.url` | JSON | ✅ | Preenchido |
| 6 | **Evolution API Key** | chatwoot_config_automaia.json | `evolution.api_key` | JSON | ✅ | Preenchido |
| 7 | **Evolution Instance** | chatwoot_config_automaia.json | `evolution.instance` | JSON | ✅ | Preenchido |
| 8 | **OpenAI API Key** | chatbot_automaia_v4.py | linha 41 | Hardcoded | 🔴 | Mover para .env |
| 9 | **OpenRouter API Key** | chatbot_automaia_v4.py | linha 40 | Hardcoded | 🔴 | Mover para .env |
| 10 | **Redis URL (v4)** | chatbot_automaia_v4.py | linha 56-57 | Hardcoded | 🔴 | Mover para .env |
| 11 | **Redis Host (followup)** | sistema_followup.py | linha 16 | Hardcoded | 🔴 | Mover para .env |
| 12 | **Redis Port (followup)** | sistema_followup.py | linha 17 | Hardcoded | 🔴 | Mover para .env |
| 13 | **Redis Password (followup)** | sistema_followup.py | linha 18 | Hardcoded | 🔴 | Mover para .env |
| 14 | **Evolution URL (followup)** | sistema_followup.py | linha 20 | Hardcoded | 🔴 | Mover para .env |
| 15 | **Evolution Instance (followup)** | sistema_followup.py | linha 21 | Hardcoded | 🔴 | Mover para .env |
| 16 | **Evolution API Key (followup)** | sistema_followup.py | linha 22 | Hardcoded | 🔴 | Mover para .env |
| 17 | **Google Sheet ID** | chatwoot_config_automaia.json | `google_sheet_id` | JSON | ✅ | Preenchido |
| 18 | **Google OAuth Credentials** | google_credentials.json | web.* | JSON | ✅ | Preenchido |
| 19 | **Google OAuth Token** | google_token.pickle | (arquivo) | Pickle | ✅ | Auto-gerado |

---

## POR LOCALIZAÇÃO

### chatwoot_config_automaia.json (7 configurações) ✅
```json
{
  "chatwoot": {
    "url": "✅ https://chatwoot.loop9.com.br",
    "token": "✅ xp1AcWvf6F2p2ZypabNWHfW6",
    "account_id": "✅ 1",
    "inbox_id": "✅ 42"
  },
  "evolution": {
    "url": "✅ https://evolution.loop9.com.br",
    "api_key": "✅ 178e43e1c4f459527e7008e57e378e1c",
    "instance": "✅ automaia"
  },
  "google_sheet_id": "✅ 1OgPgNRVcnWtKePR54tKVQohchxwELiUsi5UTYoqVUfg"
}
```

### chatbot_automaia_v4.py (3 configurações) 🔴
```python
# Linha 40-41
OPENROUTER_API_KEY = "🔴 HARDCODED"      # Mover para .env
OPENAI_API_KEY = "🔴 HARDCODED"          # Mover para .env

# Linha 56-57
redis = Redis(
    url="🔴 HARDCODED",                   # Mover para .env
    token="🔴 HARDCODED"                  # Mover para .env
)
```

### sistema_followup.py (6 configurações) 🔴
```python
# Linhas 16-22
REDIS_HOST = "🔴 HARDCODED"              # Mover para .env
REDIS_PORT = "🔴 HARDCODED"              # Mover para .env
REDIS_PASSWORD = "🔴 HARDCODED"          # Mover para .env

EVOLUTION_URL = "🔴 HARDCODED"           # Mover para .env
EVOLUTION_INSTANCE = "🔴 HARDCODED"      # Mover para .env
EVOLUTION_API_KEY = "🔴 HARDCODED"       # Mover para .env
```

### google_credentials.json (4 configurações) ✅
```json
{
  "web": {
    "client_id": "✅ 386950317415-...",
    "client_secret": "✅ GOCSPX-...",
    "auth_uri": "✅ https://accounts.google.com/o/oauth2/auth",
    "token_uri": "✅ https://oauth2.googleapis.com/token"
  }
}
```

---

## POR TIPO DE SERVIÇO

### 🤖 LLM e IA (2 keys) 🔴
| Serviço | Chave | Localização | Segurança |
|---------|-------|-------------|-----------|
| OpenAI | OPENAI_API_KEY | chatbot_automaia_v4.py:41 | 🔴 Hardcoded |
| OpenRouter | OPENROUTER_API_KEY | chatbot_automaia_v4.py:40 | 🔴 Hardcoded |

**Ação**: Mover para `.env`

```bash
# Criar arquivo .env
cp .env.example .env
nano .env

# Adicionar
OPENAI_API_KEY=sk-proj-...
OPENROUTER_API_KEY=sk-or-v1-...
```

---

### 💬 Chat + WhatsApp (7 configs) ✅
| Serviço | Configs | Localização | Segurança |
|---------|---------|-------------|-----------|
| Chatwoot | url, token, account_id, inbox_id | chatwoot_config_automaia.json | ✅ JSON |
| Evolution | url, api_key, instance | chatwoot_config_automaia.json | ✅ JSON |

**Distribuição**: Chatwoot_config_automaia.json (CORRETO)

---

### 💾 Cache Redis (3+3 configs) 🔴
| Arquivo | Configs | Tipo | Segurança |
|---------|---------|------|-----------|
| chatbot_automaia_v4.py | url, token | Hardcoded | 🔴 Inseguro |
| sistema_followup.py | host, port, password | Hardcoded | 🔴 Inseguro |

**Ação**: Consolidar em `.env`

```bash
# .env (Opção A - URL)
REDIS_URL=https://default:TOKEN@HOST:PORT

# ou .env (Opção B - Separado)
REDIS_HOST=HOST
REDIS_PORT=PORT
REDIS_PASSWORD=PASSWORD
```

---

### 📅 Google (agendamento) (4+1 configs) ✅
| Componente | Arquivo | Configs | Segurança |
|---|---|---|---|
| Credenciais | google_credentials.json | client_id, client_secret, auth_uri, token_uri | ✅ JSON |
| Sheet ID | chatwoot_config_automaia.json | google_sheet_id | ✅ JSON |
| Token | google_token.pickle | (auto-gerado) | ✅ Pickle |

**Status**: Tudo em ordem

---

## CHECKLIST RÁPIDO

### Status Atual
- [x] Chatwoot + Evolution configurados
- [x] Google Sheets configurado
- [x] Validador criado e testado
- [ ] OpenAI + OpenRouter em .env
- [ ] Redis em .env
- [ ] .env ignorado no .gitignore

### Para cada API Insegura
- [ ] Criar `.env` (copiar `.env.example`)
- [ ] Preencher variáveis
- [ ] Modificar Python para `os.getenv()`
- [ ] Remover hardcoded do código
- [ ] Testar
- [ ] Commitar SEM .env

---

## FLUXO DE INICIALIZAÇÃO

```
Iniciar chatbot_automaia_v4.py
    ↓
├─► Carrega .env (se usar python-dotenv)
│   ├─ OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
│   ├─ OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
│   ├─ REDIS_URL = os.getenv('REDIS_URL')
│   └─ REDIS_TOKEN = os.getenv('REDIS_TOKEN')
│
├─► Carrega chatwoot_config_automaia.json
│   ├─ Chatwoot: url, token, account_id, inbox_id
│   ├─ Evolution: url, api_key, instance
│   └─ Google: sheet_id
│
├─► Inicializa componentes
│   ├─ RAG Simples (recebe api_keys)
│   ├─ Score (recebe chatwoot_config)
│   ├─ FollowUp (carrega Redis)
│   ├─ Escalonamento (usa Chatwoot + Google)
│   └─ Métricas
│
└─► Inicia webhook: /webhook/chatwoot
```

---

## ARQUIVOS DE REFERÊNCIA

| Documento | Propósito | Quando Usar |
|-----------|-----------|------------|
| **MAPA_CONFIGURACAO_APIS.md** | Análise detalhada de TODAS as configurações | Entender arquitetura |
| **SETUP_APIS.md** | Guia passo-a-passo para configurar cada API | Fazer setup pela 1ª vez |
| **MATRIZ_CONFIGURACAO_RAPIDA.md** | Este arquivo - referência rápida | Consulta rápida |
| **.env.example** | Template de variáveis de ambiente | Copiar para .env |
| **validar_configuracao.py** | Script de validação automática | Checar se tudo está OK |

---

## COMANDOS ÚTEIS

```bash
# Validar configuração
python3 validar_configuracao.py

# Gerar QR code WhatsApp
python3 gerar_qrcode.py

# Autenticar Google
python3 componentes/escalonamento/autenticar_google.py

# Copiar template .env
cp .env.example .env
nano .env

# Verificar se .env existe
ls -la .env

# Testar Redis
python3 -c "from upstash_redis import Redis; r = Redis.from_url('sua-url'); print(r.ping())"

# Testar OpenAI
python3 -c "import openai; openai.api_key='sua-key'; print(openai.Model.list())"
```

---

## PRÓXIMAS AÇÕES (Prioridade)

### 🔴 CRÍTICO (Hoje)
1. Criar `.env` a partir de `.env.example`
2. Mover hardcoded keys para `.env`
3. Adicionar `.env` ao `.gitignore`
4. Testar validador: `python3 validar_configuracao.py`

### 🟡 IMPORTANTE (Esta semana)
1. Remover hardcoded do código Python
2. Implementar `python-dotenv` no código
3. Testar fluxo completo com .env

### 🟢 MELHORIAS (Próximas semanas)
1. Usar AWS Secrets Manager para produção
2. Documentação de policies de segurança
3. Rotação automática de chaves

---

## PERGUNTAS FREQUENTES

**P: Onde preencher Chatwoot credentials?**
A: Em `chatwoot_config_automaia.json` (JSON seguro) ✅

**P: Onde preencher OpenAI key?**
A: Atualmente hardcoded em `chatbot_automaia_v4.py:41` (inseguro).
Mover para `.env` (seguro).

**P: Como testar se está tudo OK?**
A: `python3 validar_configuracao.py` e procurar por 🟢 ou 🟡

**P: Posso commitar .env?**
A: NÃO! Adicione ao `.gitignore` imediatamente.

**P: Redis está em qual arquivo?**
A: 2 arquivos (problema!):
- `chatbot_automaia_v4.py` linhas 56-57
- `sistema_followup.py` linhas 16-22

**P: Como migrar para .env?**
A: Ver SETUP_APIS.md seção "Alternativa Segura: Usar .env"

---

## RESUMO VISUAL

```
SEGURANÇA: ✅ ✅ ✅ 🔴 🔴 = 60% Seguro

┌─────────────────────────────────────┐
│  CHATWOOT + EVOLUTION              │ ✅ JSON Seguro
│  GOOGLE SHEETS + OAUTH             │ ✅ JSON Seguro
│  OPENAI + OPENROUTER               │ 🔴 Hardcoded
│  REDIS (2 arquivos)                │ 🔴 Hardcoded
└─────────────────────────────────────┘

AÇÕES NECESSÁRIAS:
🔴 1. Criar .env
🔴 2. Mover OpenAI/OpenRouter
🔴 3. Mover Redis
🟢 4. Validar
```

---

**Última atualização:** 2025-11-05
**Validador status:** ✅ Funcionando
**Documentação:** Completa
