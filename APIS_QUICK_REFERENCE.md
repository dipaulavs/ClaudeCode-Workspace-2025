# APIs Quick Reference - Chatbot Automaia V4

## Arquivos Críticos (Com Credenciais)

```
whatsapp-chatbot-carros/
├── chatbot_automaia_v4.py         ⚠️ Hard-coded: OPENAI_API_KEY, OPENROUTER_API_KEY, UPSTASH
├── chatwoot_config_automaia.json  ⚠️ Credenciais: Chatwoot, Evolution, Google Sheets ID
├── webhook_middleware_automaia.py ⚠️ Filtro de números
└── componentes/
    └── escalonamento/
        ├── autenticar_google.py    → Google OAuth
        ├── consulta_agenda.py      → Google Sheets (Mock ou Real)
        └── criar_agenda_publica_oauth.py
```

---

## 1️⃣ OPENAI (Hard-coded em chatbot_automaia_v4.py)

```python
OPENAI_API_KEY = "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"

# Whisper (Transcrição)
POST https://api.openai.com/v1/audio/transcriptions
  Modelo: whisper-1
  Idioma: pt

# GPT-4o Vision (Análise de Imagem)
POST https://api.openai.com/v1/chat/completions
  Modelo: gpt-4o
  Max tokens: 300
```

---

## 2️⃣ OPENROUTER (Hard-coded em chatbot_automaia_v4.py)

```python
OPENROUTER_API_KEY = "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"

# Claude Haiku 4.5
POST https://openrouter.ai/api/v1/chat/completions
  Modelo: anthropic/claude-haiku-4.5
  Temperatura: 0.3
  Max tokens: 10
  Uso: Análise de completude de mensagem
```

---

## 3️⃣ CHATWOOT (chatwoot_config_automaia.json)

```json
{
  "chatwoot": {
    "url": "https://chatwoot.loop9.com.br",
    "token": "xp1AcWvf6F2p2ZypabNWHfW6",
    "account_id": "1",
    "inbox_id": "42"
  }
}
```

### Endpoints Principais
```
GET  /api/v1/accounts/{account_id}/contacts/search
POST /api/v1/accounts/{account_id}/contacts
POST /api/v1/accounts/{account_id}/conversations
GET  /api/v1/accounts/{account_id}/conversations/{conv_id}
POST /api/v1/accounts/{account_id}/conversations/{conv_id}/messages
POST /api/v1/accounts/{account_id}/conversations/{conv_id}/assignments
```

### Headers
```
api_access_token: xp1AcWvf6F2p2ZypabNWHfW6
Content-Type: application/json
```

---

## 4️⃣ EVOLUTION (chatwoot_config_automaia.json)

```json
{
  "evolution": {
    "url": "https://evolution.loop9.com.br",
    "api_key": "178e43e1c4f459527e7008e57e378e1c",
    "instance": "automaia"
  }
}
```

### Endpoints
```
POST /message/sendText/{instance}
POST /message/sendMedia/{instance}
```

### Headers
```
apikey: 178e43e1c4f459527e7008e57e378e1c
Content-Type: application/json
```

### Webhooks Recebidos
```
POST http://localhost:5004/webhook/evolution
Evento: messages.upsert
```

---

## 5️⃣ REDIS (Hard-coded em chatbot_automaia_v4.py)

```python
redis = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
)
```

### Chaves Usadas
```
fila:automaia:{numero}              → Fila de mensagens (TTL: 90s)
contexto:automaia:{numero}          → Histórico (TTL: 14 dias)
aguardou_extra:automaia:{numero}    → Flag de debounce (TTL: 90s)
```

---

## 6️⃣ GOOGLE SHEETS (chatwoot_config_automaia.json)

```json
{
  "google_sheet_id": "1OgPgNRVcnWtKePR54tKVQohchxwELiUsi5UTYoqVUfg"
}
```

### Modos
- **MOCK** (padrão): Usa dados fake, sem autenticação
- **REAL**: Requer OAuth ou Service Account

### Setup OAuth
```bash
python3 componentes/escalonamento/autenticar_google.py
→ Abre navegador → Login → Salva em config/google_token.pickle
```

### Crear Planilha
```bash
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

---

## 7️⃣ PORTAS E WEBHOOKS

```
5003 (Bot V4)
  POST /webhook/chatwoot   ← Middleware envia mensagens
  GET  /health             ← Status

5004 (Middleware)
  POST /webhook/evolution  ← Evolution envia mensagens
  POST /webhook/chatwoot   ← Chatwoot envia events
  GET  /health

NGROK (Tunelamento)
  Publica: http://SEU_URL/webhook/evolution
           http://SEU_URL/webhook/chatwoot
```

---

## 8️⃣ NÚMEROS PERMITIDOS

```python
# webhook_middleware_automaia.py (linha 43)
NUMEROS_PERMITIDOS = ["5531986549366", "553186549366"]

# Configurar via script
python3 configurar_filtro_numero.py
```

---

## 9️⃣ FLUXO DE MENSAGEM

```
1. Evolution API → Webhook (5004) /webhook/evolution
2. Middleware cria contato e conversa no Chatwoot
3. Chatwoot → Webhook (5004) /webhook/chatwoot (message_created)
4. Middleware verifica atendente ativo
   ├─ SIM → Atendente responde
   └─ NÃO → Encaminha para Bot via /webhook/chatwoot (5003)
5. Bot V4
   ├─ Redis: Fila + Debounce
   ├─ OpenAI/OpenRouter: IA
   ├─ Componentes: Score, Follow-ups, Escalonamento
   └─ Evolution: Envia resposta
```

---

## 🔟 VARIÁVEIS CRÍTICAS

### Ambiente (.env recomendado)

```bash
# ⚠️ Atualmente HARD-CODED em código Python:
OPENAI_API_KEY=sk-proj-...
OPENROUTER_API_KEY=sk-or-v1-...
UPSTASH_URL=https://legible-collie-9537.upstash.io
UPSTASH_TOKEN=ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw

# ⚠️ Em JSON (chatwoot_config_automaia.json):
CHATWOOT_URL=https://chatwoot.loop9.com.br
CHATWOOT_TOKEN=xp1AcWvf6F2p2ZypabNWHfW6
CHATWOOT_ACCOUNT_ID=1
CHATWOOT_INBOX_ID=42

EVOLUTION_URL=https://evolution.loop9.com.br
EVOLUTION_API_KEY=178e43e1c4f459527e7008e57e378e1c
EVOLUTION_INSTANCE=automaia

GOOGLE_SHEET_ID=1OgPgNRVcnWtKePR54tKVQohchxwELiUsi5UTYoqVUfg

# Modificável via script:
NUMEROS_PERMITIDOS=["5531986549366", "553186549366"]
```

---

## 📋 CHECKLIST DE DEPLOY

- [ ] Verificar OPENAI_API_KEY válida
- [ ] Verificar OPENROUTER_API_KEY válida
- [ ] Verificar UPSTASH_TOKEN conecta
- [ ] Verificar CHATWOOT_TOKEN válido
- [ ] Verificar EVOLUTION_API_KEY válida
- [ ] Configurar NUMEROS_PERMITIDOS via script
- [ ] NGROK configurado e rodando
- [ ] Middleware (5004) iniciado
- [ ] Bot V4 (5003) iniciado
- [ ] Health check: curl http://localhost:5003/health
- [ ] Google Sheets: Autenticar (OAuth) se usar agenda real

---

## 🚨 SEGURANÇA - AÇÕES IMEDIATAS

1. **Mover hard-coded para .env**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
   ```

2. **Remover credenciais de JSON**
   ```bash
   # Criar .env.example com placeholders
   # Adicionar chatwoot_config_automaia.json ao .gitignore
   ```

3. **Regenerar tokens expostos**
   - OPENAI_API_KEY
   - OPENROUTER_API_KEY
   - UPSTASH_TOKEN
   - EVOLUTION_API_KEY
   - CHATWOOT_TOKEN

---

## 📞 SUPORTE RÁPIDO

**Health Check**
```bash
curl http://localhost:5003/health
```

**Logs Bot**
```bash
tail -f /var/log/chatbot_automaia.log
```

**Redis Test**
```python
from upstash_redis import Redis
redis = Redis(url="...", token="...")
print(redis.ping())  # Deve retornar True
```

**Chatwoot API Test**
```bash
curl -H "api_access_token: xp1AcWvf6F2p2ZypabNWHfW6" \
  https://chatwoot.loop9.com.br/api/v1/accounts/1/conversations
```

---

## 📚 DOCUMENTAÇÃO ADICIONAL

- `APIS_ANALYSIS.md` - Análise completa e detalhada
- `whatsapp-chatbot-carros/README.md` - Setup e execução
- `componentes/escalonamento/README.md` - Google Sheets
