# 🤖 Chatbot WhatsApp - Bot V4 Completo

Bot de WhatsApp inteligente com IA Claude Haiku 4.5, integração com Chatwoot e recursos avançados.

---

## 🚀 Quick Start

### Iniciar Bot:
```bash
bot
# ou
cd ~/Desktop/ClaudeCode-Workspace/whatsapp-chatbot && ./INICIAR_BOT_V4.sh
```

### Parar Bot:
```bash
botstop
# ou
cd ~/Desktop/ClaudeCode-Workspace/whatsapp-chatbot && ./PARAR_BOT_V4.sh
```

---

## 📊 Arquitetura

```
whatsapp-chatbot/
├── chatbot_corretor_v4.py         # Bot principal (porta 5001)
├── webhook_middleware_v2.py       # Middleware (porta 5002)
├── configurar_webhook.py          # Config webhook Evolution API
├── setup_chatwoot_integration.py  # Setup Chatwoot
├── upload_fotos_imoveis.py        # Upload fotos de imóveis
├── test_scheduled_whatsapp.py     # Teste de agendamento
│
├── INICIAR_BOT_V4.sh             # 🚀 Script de inicialização
├── PARAR_BOT_V4.sh               # 🛑 Script para parar
├── INICIAR_*.sh                  # Outros scripts (V2, V3, etc)
├── PARAR_*.sh                    # Scripts de parada
│
├── logs/                         # Logs do bot
│   ├── chatbot_v4.log
│   └── middleware_v3.log
│
├── imoveis/                      # Banco de imóveis
│
├── chatwoot_config.json          # Config Chatwoot
├── crontab_temp.txt              # Config cron
│
└── docs/                         # Documentação completa
    ├── CHATBOT_V4_README.md
    ├── AUDIO_TRANSCRIPTION.md
    ├── CONFIGURAR_NGROK.md
    └── ...
```

---

## ⚡ Funcionalidades V4

### 🧠 IA e Processamento:
- ✅ **Claude Haiku 4.5** via OpenRouter
- ✅ **Transcrição de áudio** (Whisper)
- ✅ **Visão de imagens** (GPT-4o)
- ✅ **Análise de completude** (IA detecta mensagens incompletas)
- ✅ **Debounce inteligente** (15s + até 50s se necessário)

### 💬 Comunicação:
- ✅ **Mensagens humanizadas** (picotadas em chunks)
- ✅ **Contexto persistente** (30 mensagens, 14 dias)
- ✅ **Fila no Redis** (evita concorrência)
- ✅ **Resposta direta** via Evolution API (sem loop)

### 🏢 Negócio:
- ✅ **Banco de imóveis** (busca inteligente)
- ✅ **Integração Chatwoot** (híbrida)
- ✅ **Timers por número** (evita duplicação)

---

## 🔧 Como Funciona

### 1. Fluxo de Mensagem:

```
WhatsApp (Evolution API)
    ↓
Webhook → Middleware (5002)
    ↓
Debounce 15s + Análise IA
    ↓
Bot V4 (5001) → Claude Haiku 4.5
    ↓
Resposta → Evolution API → WhatsApp
```

### 2. Debounce Inteligente:

- **15s base**: Agrupa mensagens do mesmo número
- **+50s condicional**: Se IA detectar mensagem incompleta
- **Timers individuais**: Cada número tem seu próprio timer

### 3. Integração Híbrida Chatwoot:

- **Modo bot**: Responde automaticamente
- **Modo humano**: Encaminha para Chatwoot
- **Toggle**: `/chatwoot on|off` (em desenvolvimento)

---

## 📡 Portas e Serviços

| Serviço | Porta | Log |
|---------|-------|-----|
| Chatbot V4 | 5001 | `logs/chatbot_v4.log` |
| Middleware | 5002 | `logs/middleware_v3.log` |
| Ngrok | 4040 | Dashboard: http://localhost:4040 |
| Chatwoot | - | Ver config |

---

## 🔍 Monitoramento

### Health Check:
```bash
curl http://localhost:5001/health
```

**Output:**
```json
{
  "status": "healthy",
  "version": "4.3",
  "timers_ativos": 0,
  "timestamp": "2025-11-01 15:30:00"
}
```

### Logs em Tempo Real:
```bash
# Bot principal
tail -f logs/chatbot_v4.log

# Middleware
tail -f logs/middleware_v3.log

# Ambos
tail -f logs/*.log
```

### Status Processos:
```bash
# Ver PIDs
ps aux | grep "chatbot\|webhook\|ngrok"

# Ver portas
lsof -i:5001
lsof -i:5002
```

---

## 🐛 Troubleshooting

### Bot não inicia:

```bash
# 1. Verificar se já está rodando
ps aux | grep chatbot

# 2. Parar processos antigos
./PARAR_BOT_V4.sh

# 3. Limpar PIDs
rm -f .*.pid

# 4. Verificar portas
lsof -i:5001
lsof -i:5002

# 5. Iniciar novamente
./INICIAR_BOT_V4.sh
```

### Webhook não funciona:

```bash
# 1. Verificar ngrok
curl http://localhost:4040/api/tunnels

# 2. Reconfigurar webhook
python3 configurar_webhook.py https://seu-ngrok.ngrok.io/webhook/evolution

# 3. Verificar Evolution API
# Ver variáveis de ambiente
```

### Erros de dependência:

```bash
# Instalar dependências
cd ~/Desktop/ClaudeCode-Workspace
pip3 install -r requirements.txt
```

---

## 📋 Versões Disponíveis

| Script | Versão | Descrição |
|--------|--------|-----------|
| `INICIAR_BOT_V4.sh` | **V4.3** | ✅ **Atual** - Debounce + IA + Redis |
| `INICIAR_V2.sh` | V2.0 | Versão anterior simples |
| `INICIAR_INTEGRACAO_HIBRIDA.sh` | V3.0 | Chatwoot híbrido |

**Recomendado:** Sempre use `INICIAR_BOT_V4.sh`

---

## 🔐 Configurações

### Evolution API:
- URL: Ver variável `EVOLUTION_API_URL`
- Instância: `lfimoveis`
- Webhook: Configurado automaticamente

### Chatwoot:
- Arquivo: `chatwoot_config.json`
- Inbox: LF IMOVEIS

### Redis:
- URL: Ver variável `REDIS_URL` (Upstash)
- Uso: Fila de mensagens + contexto

### APIs:
- OpenRouter: Claude Haiku 4.5
- OpenAI: Whisper (transcrição) + GPT-4o (visão)
- Upstash: Redis (memória)

---

## 📚 Documentação Completa

Todos os arquivos de documentação estão na raiz da pasta:

| Arquivo | Conteúdo |
|---------|----------|
| `CHATBOT_V4_README.md` | Docs completa V4 |
| `AUDIO_TRANSCRIPTION.md` | Como funciona transcrição |
| `CONFIGURAR_NGROK.md` | Setup ngrok |
| `AGENDAMENTO_WHATSAPP.md` | Mensagens agendadas |
| `INTEGRACAO_HIBRIDA_README.md` | Bot + Chatwoot |
| `IMOVEIS_README.md` | Banco de imóveis |
| `V2_MUDANCAS.md` | Changelog V2 |

---

## 🚨 Avisos Importantes

### ⚠️ NUNCA:
- Editar arquivos com bot rodando
- Deletar PIDs manualmente durante execução
- Mudar portas sem atualizar scripts
- Commitar secrets/API keys

### ✅ SEMPRE:
- Parar bot antes de editar código
- Usar `./PARAR_BOT_V4.sh` antes de reiniciar
- Verificar logs após mudanças
- Testar webhook após reconfigurar

---

## 💰 Custos Estimados

**Bot V4 (1000 mensagens/mês):**
- Claude Haiku 4.5: ~$0.50
- Whisper (áudio): ~$0.10 (10 áudios)
- Redis Upstash: Grátis (tier free)
- Evolution API: Grátis (self-hosted)
- Ngrok: Grátis (tier free)

**Total:** ~$0.60/mês

---

## 🎯 Próximas Melhorias

- [ ] Toggle Chatwoot via comando
- [ ] Dashboard web de métricas
- [ ] Múltiplas instâncias (multi-tenant)
- [ ] Agendamento via interface
- [ ] Relatórios de performance
- [ ] A/B testing de prompts

---

## 📞 Suporte

**Logs:** Sempre verifique `logs/` primeiro
**Status:** `curl http://localhost:5001/health`
**Restart:** `./PARAR_BOT_V4.sh && ./INICIAR_BOT_V4.sh`

---

**Última atualização:** 2025-11-01
**Versão:** 4.3
**Status:** ✅ Produção
