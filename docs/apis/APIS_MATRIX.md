# APIs Matrix - Chatbot Automaia V4

## Matriz de Configuração e Uso

| # | Serviço | Tipo | Arquivo Config | Variáveis | Autenticação | Status |
|---|---------|------|-----------------|-----------|--------------|--------|
| 1 | OpenAI | IA (Whisper) | chatbot_automaia_v4.py | OPENAI_API_KEY | Bearer Token | Hard-coded ⚠️ |
| 2 | OpenAI | IA (GPT-4o) | chatbot_automaia_v4.py | OPENAI_API_KEY | Bearer Token | Hard-coded ⚠️ |
| 3 | OpenRouter | IA (Claude) | chatbot_automaia_v4.py | OPENROUTER_API_KEY | Bearer Token | Hard-coded ⚠️ |
| 4 | Chatwoot | CRM | chatwoot_config_automaia.json | TOKEN, URL, ACCOUNT_ID | api_access_token | JSON ⚠️ |
| 5 | Evolution | WhatsApp | chatwoot_config_automaia.json | API_KEY, URL, INSTANCE | apikey Header | JSON ⚠️ |
| 6 | Redis | Cache/Queue | chatbot_automaia_v4.py | URL, TOKEN | Token | Hard-coded ⚠️ |
| 7 | Google Sheets | Agenda | chatwoot_config_automaia.json | SHEET_ID | OAuth / Service Account | JSON + OAuth |
| 8 | Ngrok | Tunnel | Não configurado | authtoken | CLI | Manual |

---

## Matriz de Funcionalidades

| Serviço | Funcionalidade | Endpoint | Método | Headers | Payload | Resposta |
|---------|---|---|---|---|---|---|
| **OpenAI** | Transcrever áudio | /v1/audio/transcriptions | POST | Authorization: Bearer | file, model, language | texto |
| **OpenAI** | Analisar imagem | /v1/chat/completions | POST | Authorization: Bearer | model, messages (vision) | conteúdo |
| **OpenRouter** | Análise completude | /api/v1/chat/completions | POST | Authorization: Bearer | model, messages | COMPLETA/INCOMPLETA |
| **Chatwoot** | Buscar contato | /api/v1/accounts/{id}/contacts/search | GET | api_access_token | q (número) | contact[] |
| **Chatwoot** | Criar contato | /api/v1/accounts/{id}/contacts | POST | api_access_token | name, phone_number | contact |
| **Chatwoot** | Buscar conversa | /api/v1/accounts/{id}/conversations | GET | api_access_token | status, inbox_id | conversation[] |
| **Chatwoot** | Criar conversa | /api/v1/accounts/{id}/conversations | POST | api_access_token | contact_id, inbox_id | conversation |
| **Chatwoot** | Enviar mensagem | /api/v1/accounts/{id}/conversations/{id}/messages | POST | api_access_token | content, attachments | message |
| **Chatwoot** | Verificar atendente | /api/v1/accounts/{id}/conversations/{id} | GET | api_access_token | - | assignee_id |
| **Chatwoot** | Atribuir corretor | /api/v1/accounts/{id}/conversations/{id}/assignments | POST | api_access_token | assignee_id | success |
| **Evolution** | Enviar texto | /message/sendText/{instance} | POST | apikey | number, text | status |
| **Evolution** | Enviar imagem | /message/sendMedia/{instance} | POST | apikey | number, media, caption | status |
| **Evolution** | Webhook | /webhook/evolution | POST | - | event, data | ACK |
| **Redis** | Fila mensagens | redis.setex | - | - | fila:automaia:{num} | OK |
| **Redis** | Contexto histórico | redis.setex | - | - | contexto:automaia:{num} | OK |
| **Redis** | Health check | redis.ping | - | - | - | PONG |
| **Google Sheets** | Consultar agenda | sheets.get | - | OAuth | range, sheet_id | horários[] |
| **Google Sheets** | Criar planilha | sheets.create | - | OAuth | title, sheets | spreadsheet_id |
| **Google Sheets** | Atualizar agenda | sheets.update | - | OAuth | range, values | updated_cells |

---

## Matriz de Segurança

| Serviço | Credencial | Localização | Exposto? | Tipo | TTL | Ação |
|---------|---|---|---|---|---|---|
| OpenAI | sk-proj-* | chatbot_automaia_v4.py:40 | SIM ⚠️ | API Key | ∞ | Regenerar |
| OpenRouter | sk-or-v1-* | chatbot_automaia_v4.py:40 | SIM ⚠️ | API Key | ∞ | Regenerar |
| Chatwoot | xp1Acwvf* | chatwoot_config_automaia.json | SIM ⚠️ | API Token | ∞ | Regenerar |
| Evolution | 178e43e1* | chatwoot_config_automaia.json | SIM ⚠️ | API Key | ∞ | Regenerar |
| Redis | ASVBAAIm* | chatbot_automaia_v4.py:57 | SIM ⚠️ | Token | ∞ | Regenerar |
| Google | pickle | config/google_token.pickle | SIM se no repo | OAuth Token | Refresh | .gitignore |

---

## Matriz de Fluxo de Mensagens

```
┌─────────────────────────────────────────────────────────────────┐
│ ENTRADA (Evolution → Middleware)                                │
├─────────────────────────────────────────────────────────────────┤
│ 1. Evolution API envia: POST /webhook/evolution                 │
│    └─ Evento: messages.upsert                                   │
│    └─ Contém: texto, áudio, imagem ou vídeo                     │
│                                                                 │
│ 2. Middleware webhook_evolution() (linha 202)                   │
│    ├─ Valida número (filtro NUMEROS_PERMITIDOS)                │
│    ├─ Se áudio: nada (deixa para bot processar)                │
│    ├─ Se imagem: nada (deixa para bot processar)               │
│    └─ Busca/cria contato no Chatwoot                            │
│    └─ Busca/cria conversa no Chatwoot                           │
│    └─ Envia mensagem ao Chatwoot                                │
│                                                                 │
│ 3. Chatwoot dispara webhook: POST /webhook/chatwoot (5004)     │
│    └─ Evento: message_created                                   │
│                                                                 │
│ 4. Middleware webhook_chatwoot() (linha 300)                    │
│    ├─ Verifica se atendente está ativo                          │
│    ├─ SIM → Ignora (atendente responde)                        │
│    └─ NÃO → Encaminha para bot                                  │
│       └─ POST http://localhost:5003/webhook/chatwoot           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROCESSAMENTO (Bot V4)                                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Bot recebe: POST /webhook/chatwoot (5003)                    │
│                                                                 │
│ 2. Adiciona na fila: redis.setex(fila:automaia:{num})          │
│                                                                 │
│ 3. Debounce inteligente (15s + 50s extra)                       │
│    └─ Aguarda para agrupar múltiplas mensagens                 │
│    └─ Se incompleta, aguarda +50s                              │
│                                                                 │
│ 4. Processa com Orquestrador:                                   │
│    ├─ OpenAI: Transcreve áudio (Whisper)                        │
│    ├─ OpenAI: Analisa imagem (GPT-4o Vision)                    │
│    ├─ OpenRouter: Verifica completude (Claude)                 │
│    ├─ Componentes:                                              │
│    │  ├─ RAG Simples: Ferramentas (lista_carros, faq)          │
│    │  ├─ Score: Quente/morno/frio                              │
│    │  ├─ Follow-ups: Agenda (Redis)                             │
│    │  ├─ Escalonamento: Atribui ao Chatwoot                     │
│    │  └─ Métricas: Coleta dados (Redis)                         │
│    └─ Resposta: Texto + fotos (se houver)                       │
│                                                                 │
│ 5. Salva contexto: redis.setex(contexto:automaia:{num})        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SAÍDA (Bot → Evolution)                                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Bot envia resposta: POST /message/sendText/{instance}       │
│    └─ Headers: apikey                                           │
│    └─ Payload: { number, text }                                 │
│                                                                 │
│ 2. Se houver fotos:                                             │
│    POST /message/sendMedia/{instance}                           │
│    └─ Payload: { number, mediatype, media, caption }           │
│                                                                 │
│ 3. Evolution envia para WhatsApp                                │
│                                                                 │
│ 4. Callback: on_bot_enviou_mensagem()                           │
│    └─ Agenda follow-ups automáticos                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Matriz de Timing (TTLs e Delays)

| Evento | TTL/Delay | Redis Key | Arquivo |
|--------|-----------|-----------|---------|
| Fila de mensagens | 90s | fila:automaia:{num} | chatbot_automaia_v4.py |
| Contexto histórico | 14 dias | contexto:automaia:{num} | chatbot_automaia_v4.py |
| Flag aguardou extra | 90s | aguardou_extra:automaia:{num} | chatbot_automaia_v4.py |
| Debounce padrão | 15s | - (timer thread) | chatbot_automaia_v4.py |
| Debounce estendido | 50s | - (timer thread) | chatbot_automaia_v4.py |
| Follow-up 2h | 2h | - (Redis task queue) | sistema_followup.py |
| Follow-up 24h | 24h | - (Redis task queue) | sistema_followup.py |
| Follow-up 48h | 48h | - (Redis task queue) | sistema_followup.py |
| Token Google | ~1h | google_token.pickle | autenticar_google.py |

---

## Matriz de Componentes

| Componente | Arquivo | API Usada | Redis | Webhook |
|---|---|---|---|---|
| **RAG Simples** | rag_simples_carros.py | OpenAI/OpenRouter | Leitura | Não |
| **Score** | score/sistema_score.py | Nenhuma | Escrita | Não |
| **Follow-ups** | followup/sistema_followup.py | Evolution, Redis | Escrita/Leitura | Não |
| **Escalonamento** | escalonamento/chatwoot_integration.py | Chatwoot | Nenhum | Não |
| **Agenda** | escalonamento/consulta_agenda.py | Google Sheets | Nenhum | Não |
| **Métricas** | relatorios/metricas.py | Nenhuma | Escrita | Não |
| **Orquestrador** | orquestrador_carros.py | Todos | Todos | Não |

---

## Matriz de Testes

| Serviço | Health Check | Teste Rápido | Log |
|---------|---|---|---|
| Bot V4 | GET http://localhost:5003/health | curl http://localhost:5003/health | stdout |
| Middleware | GET http://localhost:5004/health | curl http://localhost:5004/health | stdout |
| Redis | redis.ping() | python3 -c "from upstash_redis import Redis; r=Redis(...); r.ping()" | stdout |
| Chatwoot | GET /api/v1/accounts/1 | curl -H "api_access_token: ..." https://chatwoot.loop9.com.br/... | API response |
| Evolution | Test webhook | Enviar mensagem WhatsApp | stdout |
| OpenAI | API key válida | curl -H "Authorization: Bearer ..." https://api.openai.com/v1/models | response |
| Google Sheets | OAuth token válida | python3 autenticar_google.py | stdout |

---

## Matriz de Portas

| Porta | Serviço | Endpoint | Evento | Origem | Destino |
|---|---|---|---|---|---|
| 5003 | Bot V4 | POST /webhook/chatwoot | message → processamento | Middleware | Bot |
| 5003 | Bot V4 | GET /health | health check | CLI/Monitor | Bot |
| 5004 | Middleware | POST /webhook/evolution | messages.upsert | Evolution | Middleware |
| 5004 | Middleware | POST /webhook/chatwoot | message_created | Chatwoot | Middleware |
| 5004 | Middleware | GET /health | health check | CLI/Monitor | Middleware |
| 443 | OpenAI | HTTPS | Transcrição + Visão | Bot | OpenAI |
| 443 | OpenRouter | HTTPS | IA (Claude) | Bot | OpenRouter |
| 443 | Chatwoot | HTTPS | Contatos, Conversas | Bot/Middleware | Chatwoot |
| 443 | Evolution | HTTPS | Enviar/Receber WhatsApp | Bot/Middleware | Evolution |
| 443 | Redis | HTTPS | Cache/Queue | Bot | Upstash |
| 443 | Google Sheets | HTTPS | Agenda | Bot | Google |
| NGROK | Ngrok | HTTP/HTTPS | Tunelamento | Internet | Localhost |

---

## Resumo de Credenciais por Severidade

### CRÍTICA (Regenerar URGENTE)
- OPENAI_API_KEY (hard-coded, público em GitHub)
- OPENROUTER_API_KEY (hard-coded, público em GitHub)
- UPSTASH_TOKEN (hard-coded, público em GitHub)
- CHATWOOT_TOKEN (JSON, público em GitHub)
- EVOLUTION_API_KEY (JSON, público em GitHub)

### ALTA (Revisar)
- NUMEROS_PERMITIDOS (Filtrável, mas modificável)
- Google Sheets ID (Público, mas não sensível)
- Conta Chatwoot (ID 1, pode ser enumerável)

### MÉDIA (Monitorar)
- Google OAuth Token (Pickle, expiração automática)
- Redis URL (Público mas não traz dados sensíveis)

---

## Checklist Final de Segurança

- [ ] Regenerar OPENAI_API_KEY
- [ ] Regenerar OPENROUTER_API_KEY
- [ ] Regenerar UPSTASH_TOKEN
- [ ] Regenerar EVOLUTION_API_KEY
- [ ] Regenerar CHATWOOT_TOKEN
- [ ] Mover tudo para .env
- [ ] Adicionar .env ao .gitignore
- [ ] Criar .env.example com placeholders
- [ ] Adicionar chatwoot_config_automaia.json ao .gitignore
- [ ] Auditar logs de acesso (quem acessou as credenciais expostas)
- [ ] Habilitar MFA no Chatwoot
- [ ] Habilitar MFA no Evolution API
- [ ] Rotação automática de tokens

