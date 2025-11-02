# 🤖 Template: Sistema de Chatbot WhatsApp Inteligente

## 🎯 Visão Geral

Template completo para criar chatbots WhatsApp com:
- Respostas **humanizadas** (mensagens picotadas com delays)
- Debounce **inteligente** (15s + análise IA)
- **Memória** de 14 dias (Redis)
- Integração **Evolution API** + **OpenRouter**

---

## 🏗️ Componentes

| Componente | Tecnologia | Função |
|------------|-----------|--------|
| Webhook Server | Flask | Recebe mensagens |
| Fila | Redis | Agrupa mensagens durante debounce |
| Memória | Redis | Contexto 14 dias (30 msgs) |
| IA Principal | Claude Haiku 4.5 | Gera respostas |
| Analisador IA | Claude Haiku 4.5 | Detecta completude |
| WhatsApp | Evolution API | Envia/recebe mensagens |

**Fluxo:**
```
WhatsApp → Evolution → Flask → Redis (fila 15s) →
Análise IA → Contexto (30 msgs) → Claude → Resposta picotada → Evolution → WhatsApp
```

---

## ⚙️ Configurações Padrão

### 1. Modelo IA (OBRIGATÓRIO)
```python
MODEL_IA = "anthropic/claude-haiku-4.5"  # Usar em TODAS as chamadas
```

### 2. Debounce Inteligente
```python
DEBOUNCE_SEGUNDOS = 15      # Timer base
DEBOUNCE_ESTENDIDO = 50     # Se mensagem incompleta
```

**Funcionamento:**
- Aguarda 15s após última mensagem
- IA analisa completude → Se incompleta, +50s
- Total máximo: 65s

### 3. Memória Redis
```python
CONTEXTO_TTL = 1209600      # 14 dias
LIMITE_MENSAGENS = 30       # Últimas 30 mensagens
```

### 4. Respostas Humanizadas
```python
# Divide mensagens em partes (max 100 chars)
# Delay entre partes: 1.5-3s
def dividir_mensagem(texto):
    # Quebra por \n, pontos, ou 100 chars
    ...
```

### 5. Análise de Completude
```python
# ✅ CORRETO: Usa startswith
return resposta_ia.startswith("COMPLETA")

# ❌ ERRADO: Não usar
return "COMPLETA" in resposta_ia  # Bug: detecta "INCOMPLETA" como completa
```

---

## 🔧 Implementações Críticas

### ✅ Checklist Obrigatório

- [ ] **Modelo IA:** `anthropic/claude-haiku-4.5` em TODAS as chamadas
- [ ] **Análise completude:** `.startswith("COMPLETA")` (não usar `in`)
- [ ] **Flag anti-loop:** Sistema `aguardou_extra:{numero}` no Redis
- [ ] **Memória:** 30 mensagens (não 10)
- [ ] **TTL fila:** 90s (não 30s)
- [ ] **Limpeza flags:** Ao processar E ao receber nova mensagem

### Anti-Loop System
```python
def processar_mensagens_agrupadas(numero):
    chave_aguardou = f"aguardou_extra:{numero}"
    ja_aguardou_extra = redis.get(chave_aguardou)

    if not ja_aguardou_extra:
        # 1ª análise: Se incompleta, aguarda +50s
        if not analisar_completude_mensagem(mensagens):
            redis.setex(chave_aguardou, 90, "1")  # Marca que aguardou
            # Cria timer de 50s
            return
    else:
        # 2ª vez: Processa de qualquer jeito (sem loop)
        pass

    # Processa resposta
    ...
    redis.delete(chave_aguardou)  # Limpa flag

def adicionar_mensagem_na_fila(numero, mensagem):
    # Nova mensagem = novo ciclo, limpa flag
    redis.delete(f"aguardou_extra:{numero}")
    ...
```

---

## 📝 Criar Novo Bot

### 1. Copiar Template Base
```bash
cp chatbot_corretor_v4.py chatbot_meu_bot.py
```

### 2. Personalizar
```python
# === MODIFICAR ===

# Prompt da persona
PROMPT_BOT = """Vc é [NOME], [PERSONA].

LINGUAGEM:
- Use abreviações: vc, tbm, pq, blz, mt, oq
- Seja informal, como WhatsApp
- Emojis à vontade! 😊 🚀 👍

ESTILO:
- Respostas CURTAS (1-2 frases)
- Natural, como amigo

[INSTRUÇÕES ESPECÍFICAS DO SEU BOT]"""

# Porta (se múltiplos bots)
PORT = 5002  # V4 usa 5001

# === NÃO MODIFICAR ===
DEBOUNCE_SEGUNDOS = 15
DEBOUNCE_ESTENDIDO = 50
CONTEXTO_TTL = 1209600
MODEL_IA = "anthropic/claude-haiku-4.5"
```

### 3. Configurar Redis
```python
# Mesmo Redis (recomendado)
redis = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="..."
)

# OU criar novo em: https://upstash.com
```

### 4. Configurar Evolution API
```python
# Cada bot = instância diferente
EVOLUTION_INSTANCE_NAME = "meu_bot_unico"
EVOLUTION_API_KEY = "..."
EVOLUTION_API_URL = "https://evolution.loop9.com.br"
```

### 5. Rodar
```bash
# Terminal 1: Bot
python3 chatbot_meu_bot.py

# Terminal 2: ngrok
ngrok http 5002

# Terminal 3: Webhook
python3 configurar_webhook.py https://[URL-NGROK]/webhook
```

---

## 🎨 Exemplo de Persona

```python
PROMPT_BOT = """Vc é Carlos, vendedor de carros descontraído e expert.

LINGUAGEM:
- Use abreviações: vc, tbm, pq, blz, mt
- Seja informal mas profissional
- Emojis à vontade! 🚗 🔑 💰

CONHECIMENTO:
- Carros usados e novos
- Preços de mercado
- Financiamento e documentação

EXEMPLOS:
Cliente: "Quero Civic 2018"
Você: "Civic 2018 é top! 🚗\nTenho na faixa de 80-90k. Qual sua condição de pagamento?"
"""

PORT = 5002
```

---

## 🛠️ Troubleshooting

### Bot não responde
```bash
# 1. Servidor rodando?
curl http://localhost:5001/health

# 2. Verificar logs
tail -f logs/chatbot.log
# Procure: "✅ Redis conectado", "💬 MSG de [numero]"

# 3. Webhook configurado?
python3 configurar_webhook.py verificar
```

### Bot demora muito
```bash
# Ver logs de análise
tail -f logs/chatbot.log | grep "Análise IA"
# Se "INCOMPLETA" → aguarda +50s (esperado)
```

### Redis erro
```python
# Testar conexão
from upstash_redis import Redis
redis = Redis(url="...", token="...")
redis.ping()  # Deve retornar 'PONG'
```

### OpenRouter 401
```python
# Verificar key válida
OPENROUTER_API_KEY = "sk-or-v1-..."  # Deve começar assim

# Obter nova: https://openrouter.ai/keys
```

---

## 📊 Monitoramento

### Health Check
```bash
curl http://localhost:5001/health | jq
```

**Resposta esperada:**
```json
{
  "status": "online",
  "model": "anthropic/claude-haiku-4.5",
  "redis": "✅ conectado",
  "debounce_segundos": 15,
  "debounce_estendido_segundos": 50,
  "timers_ativos": 0
}
```

### Logs Importantes
```
💬 MSG de [numero]: [texto]          → Mensagem recebida
⏳ TIMER RESETADO: N msg na fila     → Debounce ativo
🚀 Timer disparado!                  → Debounce terminou
🧠 Analisando completude...          → Análise IA
🔍 Análise IA: COMPLETA/INCOMPLETA   → Resultado
📤 Enviando mensagem humanizada...   → Enviando resposta
✅ N mensagem(ns) enviada(s)!        → Sucesso
```

---

## 🔒 Segurança

**NÃO commitar:**
```python
OPENROUTER_API_KEY = "..."
EVOLUTION_API_KEY = "..."
REDIS_TOKEN = "..."
```

**Use .env:**
```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-...
REDIS_URL=https://...
REDIS_TOKEN=...

# Python
from dotenv import load_dotenv
load_dotenv()
```

---

## 💡 Dicas

1. **Sempre** use `anthropic/claude-haiku-4.5`
2. **Memória 14 dias** é padrão (não diminua)
3. **Teste com números limitados** antes de produção
4. **Monitore logs** para entender comportamento
5. **Debounce 15s+50s** funciona bem (ajuste se necessário)

---

## 📚 Referências

- **Evolution API:** https://evolution.loop9.com.br
- **OpenRouter:** https://openrouter.ai
- **Upstash Redis:** https://upstash.com
- **Claude Haiku 4.5:** https://www.anthropic.com/claude

---

**Versão:** 1.0
**Atualizado:** 2025-11-01
**Modelo Padrão:** `anthropic/claude-haiku-4.5`
