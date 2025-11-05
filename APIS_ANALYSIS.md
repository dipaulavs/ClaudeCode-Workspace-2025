# Análise Completa de APIs e Serviços Externos - WhatsApp Chatbot Carros

**Data**: 2025-11-05  
**Projeto**: whatsapp-chatbot-carros  
**Versão**: V4 (Framework Híbrido Completo)

---

## 1. OPENAI API (Whisper + GPT-4o Vision)

### Configuração
- **Arquivo**: `whatsapp-chatbot-carros/chatbot_automaia_v4.py` (linhas 40-41)
- **Variáveis**:
  - `OPENAI_API_KEY` = "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"

### Funcionalidades Usadas
1. **Whisper** - Transcrição de áudio
   - URL: `https://api.openai.com/v1/audio/transcriptions`
   - Modelo: `whisper-1`
   - Função: `transcrever_audio()` (linha 75)
   - Suporta: português (pt)

2. **GPT-4o Vision** - Análise de imagens
   - URL: `https://api.openai.com/v1/chat/completions`
   - Modelo: `gpt-4o`
   - Função: `analisar_imagem()` (linha 112)
   - Max tokens: 300

### Onde é Usada
- `chatbot_automaia_v4.py` linhas 87-141
- Processa áudio e imagens recebidas via Evolution API

---

## 2. OPENROUTER API (Claude IA)

### Configuração
- **Arquivo**: `whatsapp-chatbot-carros/chatbot_automaia_v4.py` (linha 40)
- **Variáveis**:
  - `OPENROUTER_API_KEY` = "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"

### Funcionalidades Usadas
1. **Claude Haiku 4.5** - Análise de completude de mensagem
   - URL: `https://openrouter.ai/api/v1/chat/completions`
   - Modelo: `anthropic/claude-haiku-4.5`
   - Função: `analisar_completude_mensagem()` (linha 257)
   - Uso: Determina se mensagem do usuário está completa ou incompleta
   - Temperatura: 0.3, Max tokens: 10

2. **Orquestrador (Claude)** - Processamento principal
   - Arquivo: `componentes/orquestrador_carros.py`
   - Processa mensagens com contexto histórico
   - Integra RAG + Score + Follow-ups

### Onde é Usada
- Debounce inteligente (15s + 50s)
- Decisão de quando processar mensagem
- Integração com orquestrador principal

---

## 3. CHATWOOT API

### Configuração
- **Arquivo de Config**: `whatsapp-chatbot-carros/chatwoot_config_automaia.json`
- **Variáveis**:
  - `CHATWOOT_URL` = "https://chatwoot.loop9.com.br"
  - `CHATWOOT_TOKEN` = "xp1AcWvf6F2p2ZypabNWHfW6"
  - `ACCOUNT_ID` = "1"
  - `INBOX_ID` = "42"

### Funcionalidades Usadas

#### 1. Criar Inbox (Setup)
- **Arquivo**: `setup_chatwoot.py`
- **Endpoint**: `/api/v1/accounts/{account_id}/inboxes`
- **Método**: POST
- **Headers**: `api_access_token`
- **Uso**: Criar inbox API para o bot Automaia

#### 2. Buscar/Criar Contato
- **Endpoint**: `/api/v1/accounts/{account_id}/contacts/search` (GET)
- **Endpoint**: `/api/v1/accounts/{account_id}/contacts` (POST)
- **Arquivo**: `webhook_middleware_automaia.py`
- **Função**: `buscar_ou_criar_contato_chatwoot()` (linha 54)
- **Dados**: name, phone_number, identifier

#### 3. Buscar/Criar Conversa
- **Endpoint**: `/api/v1/accounts/{account_id}/conversations` (GET/POST)
- **Arquivo**: `webhook_middleware_automaia.py`
- **Função**: `buscar_ou_criar_conversa_chatwoot()` (linha 101)

#### 4. Enviar Mensagem
- **Endpoint**: `/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages`
- **Método**: POST
- **Arquivo**: `webhook_middleware_automaia.py`
- **Função**: `enviar_mensagem_chatwoot()` (linha 148)
- **Suporta**: Texto + attachments (áudio, imagem, vídeo)

#### 5. Verificar Atendente Ativo
- **Endpoint**: `/api/v1/accounts/{account_id}/conversations/{conversation_id}`
- **Método**: GET
- **Arquivo**: `webhook_middleware_automaia.py`
- **Função**: `verificar_atendente_ativo()` (linha 180)
- **Uso**: Decide se bot responde ou humano

#### 6. Escalonamento - Atribuir Corretor
- **Endpoint**: `/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments`
- **Método**: POST
- **Arquivo**: `componentes/escalonamento/chatwoot_integration.py`
- **Função**: `atribuir_corretor()` (linha 69)
- **Payload**: `{ "assignee_id": corretor_id }`

### Webhooks Configurados
1. **Evolution → Middleware**: `/webhook/evolution` (porta 5004)
2. **Middleware → Bot**: `/webhook/chatwoot` (porta 5003)
3. **Chatwoot → Middleware**: `/webhook/chatwoot` (porta 5004)

---

## 4. EVOLUTION API (WhatsApp)

### Configuração
- **Arquivo de Config**: `whatsapp-chatbot-carros/chatwoot_config_automaia.json`
- **Variáveis**:
  - `EVOLUTION_URL` = "https://evolution.loop9.com.br"
  - `EVOLUTION_API_KEY` = "178e43e1c4f459527e7008e57e378e1c"
  - `EVOLUTION_INSTANCE` = "automaia"

### Funcionalidades Usadas

#### 1. Enviar Texto
- **Endpoint**: `/message/sendText/{instance}`
- **Método**: POST
- **Arquivo**: `chatbot_automaia_v4.py`
- **Função**: `enviar_resposta_whatsapp()` (linha 175)
- **Payload**: `{ "number": phone, "text": message }`
- **Headers**: `apikey`

#### 2. Enviar Imagem
- **Endpoint**: `/message/sendMedia/{instance}`
- **Método**: POST
- **Arquivo**: `chatbot_automaia_v4.py`
- **Função**: `enviar_imagem_whatsapp()` (linha 196)
- **Payload**: `{ "number": phone, "mediatype": "image", "media": url, "caption": "" }`

#### 3. Receber Mensagens (Webhook)
- **Evento**: `messages.upsert`
- **Arquivo**: `webhook_middleware_automaia.py`
- **Função**: `webhook_evolution()` (linha 202)
- **Extrai**: texto, áudio, imagem, vídeo

### Filtro de Números
- **Arquivo**: `webhook_middleware_automaia.py` (linha 43)
- **NUMEROS_PERMITIDOS**: ["5531986549366", "553186549366"]
- **Configuração**: `configurar_filtro_numero.py`

---

## 5. REDIS (Upstash)

### Configuração
- **Arquivo**: `whatsapp-chatbot-carros/chatbot_automaia_v4.py` (linha 55-58)
- **Variáveis**:
  - `URL` = "https://legible-collie-9537.upstash.io"
  - `TOKEN` = "ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"

### Funcionalidades Usadas

#### 1. Fila de Mensagens (Debounce)
- **Chave**: `fila:automaia:{numero}`
- **TTL**: 90 segundos
- **Função**: `adicionar_mensagem_na_fila()` (linha 407)
- **Uso**: Agrupa mensagens antes de processar

#### 2. Contexto Histórico
- **Chave**: `contexto:automaia:{numero}`
- **TTL**: 1.209.600 segundos (14 dias)
- **Função**: `obter_contexto_historico()` (linha 227)
- **Função**: `salvar_contexto()` (linha 237)
- **Limite**: Mantém últimas 30 mensagens

#### 3. Aguardou Extra (Flag)
- **Chave**: `aguardou_extra:automaia:{numero}`
- **TTL**: 90 segundos
- **Uso**: Controla se já aguardou tempo estendido

#### 4. Timers Ativos
- **Armazenamento**: Dicionário em memória `timers_ativos`
- **Lock**: Threading `lock`
- **Função**: Debounce com threading

### Operações Redis Usadas
- `redis.get(chave)`
- `redis.setex(chave, ttl, valor)` - Set + TTL
- `redis.delete(chave)`
- `redis.ping()`

---

## 6. GOOGLE SHEETS API

### Configuração

#### Opção 1: Service Account (Produção)
- **Arquivo de Credenciais**: `config/google_service_account.json`
- **Scopes**: 
  - `https://www.googleapis.com/auth/spreadsheets`
  - `https://www.googleapis.com/auth/drive.file`

#### Opção 2: OAuth (Desenvolvimento)
- **Arquivo de Credenciais**: `config/google_credentials.json`
- **Token**: `config/google_token.pickle`
- **Script de Autenticação**: `componentes/escalonamento/autenticar_google.py`

### Variáveis
- **SHEET_ID** = "1OgPgNRVcnWtKePR54tKVQohchxwELiUsi5UTYoqVUfg" (em `chatwoot_config_automaia.json`)
- **Modo Default**: MOCK (sem Google API)

### Funcionalidades Usadas

#### 1. Consulta de Agenda
- **Arquivo**: `componentes/escalonamento/consulta_agenda.py`
- **Classe**: `ConsultaAgenda`
- **Função**: `buscar_horarios_disponiveis()` (linha 73)
- **Modo**: Mock ou Google API
- **Retorna**: Lista de horários disponíveis nos próximos N dias

#### 2. Criar Planilha de Agenda
- **Arquivo**: `componentes/escalonamento/criar_agenda_publica_oauth.py`
- **Classe**: `CriadorAgendaPublicaOAuth`
- **Uso**: Cria planilha com horários/vendedores para agendamento
- **Padrão**: 7 dias, 4 horários (10:00, 14:00, 15:00, 16:00)

#### 3. Atualizar Planilha
- **Arquivo**: `componentes/escalonamento/atualizar_agenda.py`
- **Uso**: Marca slots como ocupados após agendamento

### APIs Google Utilizadas
- **Sheets API v4**: Ler/escrever dados
- **Drive API v3**: Criar/compartilhar planilhas

---

## 7. NGROK (Tunelamento)

### Uso
- **Arquivo**: `configurar_filtro_numero.py` (linha 115)
- **Comando**: `./INICIAR_COM_NGROK.sh`
- **Propósito**: Expor servidores locais (portas 5003, 5004) na internet
- **Webhooks Publicados**:
  - Evolution → `http://SEU_NGROK_URL/webhook/evolution`
  - Bot → `http://SEU_NGROK_URL/webhook/chatwoot`

---

## 8. OUTRAS APIs E SERVIÇOS

### Flask (Framework Web)
- **Arquivo**: `chatbot_automaia_v4.py` (linha 20)
- **Portas**:
  - Bot V4: 5003
  - Middleware: 5004
- **Endpoints**:
  - `/webhook/chatwoot` (POST)
  - `/health` (GET)

### Requests (HTTP Client)
- **Uso**: Todas as chamadas HTTP para APIs
- **Arquivo**: Diversos

### Python Stdlib
- `threading` - Debounce com timers
- `json` - Serialização
- `datetime` - Timestamps
- `pathlib` - Manipulação de arquivos
- `tempfile` - Áudios temporários

---

## 9. RESUMO DE VARIÁVEIS DE AMBIENTE NECESSÁRIAS

```bash
# OpenAI/OpenRouter
OPENAI_API_KEY=sk-proj-...
OPENROUTER_API_KEY=sk-or-v1-...

# Chatwoot
CHATWOOT_URL=https://chatwoot.loop9.com.br
CHATWOOT_TOKEN=xp1AcWvf6F2p2ZypabNWHfW6
CHATWOOT_ACCOUNT_ID=1
CHATWOOT_INBOX_ID=42

# Evolution API
EVOLUTION_URL=https://evolution.loop9.com.br
EVOLUTION_API_KEY=178e43e1c4f459527e7008e57e378e1c
EVOLUTION_INSTANCE=automaia

# Redis (Upstash)
UPSTASH_URL=https://legible-collie-9537.upstash.io
UPSTASH_TOKEN=ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw

# Google Sheets (Opcional)
GOOGLE_SHEET_ID=1OgPgNRVcnWtKePR54tKVQohchxwELiUsi5UTYoqVUfg

# Filtro de Números (Configurável)
NUMEROS_PERMITIDOS=["5531986549366", "553186549366"]
```

---

## 10. FLUXO DE INTEGRAÇÃO DAS APIs

```
Evolution (WhatsApp)
    ↓ (webhook /webhook/evolution)
Middleware (5004)
    ↓ (cria/busca contato e conversa no Chatwoot)
Chatwoot (gerencia conversas)
    ↓ (webhook /webhook/chatwoot - message_created)
Middleware (verifica atendente ativo)
    ├─ SIM: Atendente responde
    └─ NÃO: Encaminha para Bot
        ↓ (webhook /webhook/chatwoot)
    Bot V4 (5003)
        ├─ Redis: Fila + Debounce + Contexto
        ├─ OpenAI: Whisper (áudio) + GPT-4o (imagem)
        ├─ OpenRouter: Análise completude + Orquestrador
        ├─ Componentes:
        │  ├─ RAG Simples (ferramentas)
        │  ├─ Score (quente/morno/frio)
        │  ├─ Follow-ups (2h, 24h, 48h)
        │  ├─ Escalonamento (Chatwoot atribuição)
        │  └─ Métricas (Redis)
        └─ Google Sheets: Agenda vendedores
        ↓ (resposta via Evolution)
Evolution (envia resposta no WhatsApp)
```

---

## 11. ARQUIVOS DE CONFIGURAÇÃO

### Primário
- **`chatwoot_config_automaia.json`**: Configuração centralizada (com credenciais)

### Secundários
- **`config/google_credentials.json`**: OAuth Google (criado por autenticar_google.py)
- **`config/google_token.pickle`**: Token OAuth Google persistente
- **`config/google_service_account.json`**: Service Account (se usado)

---

## 12. SCRIPTS DE SETUP

1. **Setup Chatwoot**: `setup_chatwoot.py`
   - Cria inbox no Chatwoot
   - Atualiza token em chatwoot_config_automaia.json

2. **Setup Google OAuth**: `componentes/escalonamento/autenticar_google.py`
   - Abre navegador para login Google
   - Salva credenciais em `config/google_token.pickle`

3. **Criar Agenda**: `componentes/escalonamento/criar_agenda_publica_oauth.py`
   - Cria planilha de agenda no Google Sheets
   - Configura horários e vendedores

4. **Filtro de Números**: `configurar_filtro_numero.py`
   - Configura quais números podem usar o bot
   - Atualiza NUMEROS_PERMITIDOS no middleware

---

## 13. TESTES E VALIDAÇÃO

### Health Check
- URL: `http://localhost:5003/health`
- Retorna: Status de todos os componentes
- Verifica: Redis, Timers, Componentes

### Modo Mock
- Google Sheets: Usa dados mockados se não configurado
- Ideal para teste sem autenticação

---

## NOTAS DE SEGURANÇA

**ATENÇÃO**: Credenciais encontradas em código aberto:
- OPENAI_API_KEY (visível em chatbot_automaia_v4.py)
- OPENROUTER_API_KEY (visível em chatbot_automaia_v4.py)
- UPSTASH_TOKEN (visível em chatbot_automaia_v4.py)
- EVOLUTION_API_KEY (em chatwoot_config_automaia.json)
- CHATWOOT_TOKEN (em chatwoot_config_automaia.json)

**Recomendação**: Mover todas para variáveis de ambiente e usar `python-dotenv`

---

## RESUMO EXECUTIVO

| Serviço | Tipo | URL | Configuração | Status |
|---------|------|-----|--------------|--------|
| OpenAI | IA (Whisper + GPT-4o) | api.openai.com | Hard-coded | OK |
| OpenRouter | IA (Claude) | openrouter.ai | Hard-coded | OK |
| Chatwoot | CRM | chatwoot.loop9.com.br | JSON config | OK |
| Evolution | WhatsApp | evolution.loop9.com.br | JSON config | OK |
| Redis | Cache/Queue | upstash.io | Hard-coded | OK |
| Google Sheets | Agenda | sheets.google.com | JSON config | Opcional |
| Ngrok | Tunneling | ngrok.io | CLI | Manual |

**Total de APIs**: 7 principais + suporte a 2+ modelos de IA
**Modo de Implantação**: Híbrido (localhost + cloud)
**Segurança**: Crítica - credenciais expostas em código
