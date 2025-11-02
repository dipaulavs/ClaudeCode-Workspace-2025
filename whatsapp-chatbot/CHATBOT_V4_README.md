# 🤖 Chatbot Corretor V4.3 - Quick Reference

## 📊 Status & Specs

| Item | Valor |
|------|-------|
| **Versão** | 4.3 (Produção) |
| **Arquivo** | `chatbot_corretor_v4.py` |
| **Porta** | 5001 |
| **Modelo IA** | Claude Haiku 4.5 (OpenRouter) |
| **Transcrição** | Whisper-1 (OpenAI) |
| **Visão** | GPT-4o (OpenAI) |
| **Memória** | Redis (Upstash) - 14 dias |
| **Integrações** | Evolution API + Chatwoot |

---

## ✨ Funcionalidades

- ✅ Debounce inteligente (15s + 50s se incompleta)
- ✅ Análise IA de completude de mensagens
- ✅ Fila Redis por número
- ✅ Resposta humanizada e picotada
- ✅ Contexto histórico (30 msgs, 14 dias)
- 🎤 Transcrição automática de áudios (Whisper)
- 👁️ Visão de imagens (GPT-4o)
- 🏠 Banco de dados de imóveis (diretório `imoveis/`)
- 📸 Envio automático de fotos via comando `[ENVIAR_FOTOS:ID]`

---

## ⚙️ Configurações Principais

```python
# Debounce
DEBOUNCE_SEGUNDOS = 15       # Aguarda após última mensagem
DEBOUNCE_ESTENDIDO = 50      # Tempo extra se incompleta

# Memória
CONTEXTO_TTL = 1209600       # 14 dias (segundos)
LIMITE_MENSAGENS = 30        # Últimas 30 mensagens

# APIs
OPENROUTER_API_KEY = "sk-or-v1-..."
OPENAI_API_KEY = "sk-proj-..."
REDIS_URL = "https://legible-collie-9537.upstash.io"
```

### Chatwoot & Evolution
```python
# Carregado de: chatwoot_config.json
CHATWOOT_URL, CHATWOOT_TOKEN, ACCOUNT_ID
EVOLUTION_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE
```

---

## 🚀 Operação

### Iniciar
```bash
python3 chatbot_corretor_v4.py > logs/chatbot_v4.log 2>&1 &
```

### Parar
```bash
pkill -f chatbot_corretor_v4.py
```

### Verificar Status
```bash
# Health check
curl http://localhost:5001/health

# Monitorar logs
tail -f logs/chatbot_v4.log

# Processo ativo
ps aux | grep chatbot_corretor_v4.py
```

---

## 🏠 Sistema de Imóveis

**Estrutura:**
```
imoveis/
├── exemplo-001/
│   ├── descricao.txt        # Descrição do imóvel
│   ├── localizacao.txt      # Endereço/região
│   ├── faq.txt              # Perguntas frequentes
│   ├── links.json           # {"fotos": [{"link": "...", "nome": "..."}]}
│   └── [arquivos das fotos]
└── lote-cascata/
    └── ...
```

**Envio automático:**
- Bot detecta `[ENVIAR_FOTOS:ID_IMOVEL]` na resposta
- Envia até 5 fotos automaticamente
- Delay de 4s entre cada foto

---

## 🔍 Fluxo de Processamento

```
WhatsApp → Evolution → Chatwoot → Middleware → Bot V4
                                                  ↓
                                        Fila Redis (15s)
                                                  ↓
                                        Análise IA Completude
                                        ├─ COMPLETA → Processa
                                        └─ INCOMPLETA → +50s
                                                  ↓
                                        Busca Contexto (30 msgs)
                                                  ↓
                                        Gera Resposta (Claude)
                                                  ↓
                                        Divide & Envia (1.5-3s delay)
                                                  ↓
                                        Evolution → WhatsApp
```

---

## 🎤 Mídia Suportada

### Áudios
- Detecta tipo `audio` em attachments
- Download automático do Chatwoot
- Transcrição com Whisper-1 (português)
- Adiciona ao contexto: `[Áudio transcrito]: texto...`

### Imagens
- Detecta tipo `image` em attachments
- Análise automática com GPT-4o
- Adiciona ao contexto: `[Imagem enviada]: descrição...`

### Outros Arquivos
- Contabiliza mas não processa
- Adiciona ao contexto: `[Usuário enviou N arquivo(s)]`

---

## 📝 Endpoints

| Endpoint | Método | Função |
|----------|--------|--------|
| `/webhook/chatwoot` | POST | Recebe mensagens do Chatwoot |
| `/health` | GET | Status do sistema |

---

## 🛠️ Troubleshooting

### Bot não responde
```bash
# 1. Verificar servidor
curl http://localhost:5001/health

# 2. Verificar processo
ps aux | grep chatbot_corretor_v4.py

# 3. Verificar logs
tail -30 logs/chatbot_v4.log
```

### Redis erro
```python
# Testar conexão
from upstash_redis import Redis
redis = Redis(url="...", token="...")
redis.ping()  # Deve retornar 'PONG'
```

### Fotos não enviam
- Verificar URLs públicas em `links.json`
- URLs devem estar encodadas (espaços = %20)
- Limite: 5 fotos por comando
- Delay: 4s entre cada foto (evita rate limit)

### Debounce muito longo
- Mensagem detectada como INCOMPLETA
- Aguarda 15s + 50s = 65s total
- Verificar logs: `"🔍 Análise IA: INCOMPLETA"`

---

## 💰 Custos Estimados

| Serviço | Custo |
|---------|-------|
| Claude Haiku 4.5 | ~$0.60/mês (1000 msgs) |
| Whisper | ~$0.006/min áudio |
| GPT-4o Vision | ~$0.01/imagem |
| **Total** | **< $2/mês** (uso moderado) |

---

## 📦 Dependências

```python
Flask, requests, upstash_redis, tempfile, pathlib, threading
```

---

## 🔑 Variáveis Críticas

```python
# chatbot_corretor_v4.py linha 35
OPENROUTER_API_KEY = "sk-or-v1-..."

# linha 38
OPENAI_API_KEY = "sk-proj-..."

# linha 53-56
redis = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="ASVBAAImcDFiOTlmYTM1..."
)

# linha 41-50 (carregado de chatwoot_config.json)
CHATWOOT_URL, CHATWOOT_TOKEN, ACCOUNT_ID
EVOLUTION_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE
```

---

## 🎯 Personalização

### Modificar Personalidade
```python
# chatbot_corretor_v4.py linha 158-179
PROMPT_CORRETOR_BASE = """Vc é Ricardo, corretor..."""
```

### Adicionar Imóveis
```bash
# Usar ferramenta de upload
python3 upload_fotos_imoveis.py

# Estrutura manual
mkdir imoveis/novo-imovel
echo "Descrição" > imoveis/novo-imovel/descricao.txt
echo '{"fotos":[{"link":"...","nome":"..."}]}' > imoveis/novo-imovel/links.json
```

---

## 📊 Health Check Response

```json
{
  "status": "online",
  "version": "4.3 - CORRETOR COMPLETO!",
  "chatbot": "Corretor de Imóveis V4.3",
  "model": "anthropic/claude-haiku-4.5",
  "whisper": "openai/whisper-1",
  "vision": "openai/gpt-4o",
  "redis": "✅ conectado",
  "imoveis": {
    "total": 2,
    "total_fotos": 4,
    "ids": ["lote no bairro cascata", "exemplo-001"]
  },
  "timers_ativos": 0,
  "debounce_segundos": 15,
  "debounce_estendido_segundos": 50
}
```

---

**Última atualização:** 2025-11-01
**Arquivo de código:** `chatbot_corretor_v4.py:990` linhas
