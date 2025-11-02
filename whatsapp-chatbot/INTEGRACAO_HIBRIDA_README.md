# 🤖 Integração Híbrida - Chatwoot + Bot WhatsApp

## 🎯 O que é?

Sistema inteligente que combina **atendimento automatizado** (bot) com **atendimento humano** (Chatwoot), permitindo que:

- 🤖 **Bot responde automaticamente** quando não há atendente disponível
- 👤 **Atendente assume** quando necessário, e o bot para de responder
- ✅ **Bot volta a funcionar** quando a conversa é resolvida

---

## 📋 Arquivos Criados

```
📁 n8n-mcp-project/
├── chatbot_corretor.py                 # Bot original com IA
├── webhook_middleware.py               # Ponte entre Evolution e Chatwoot
├── setup_chatwoot_integration.py       # Configuração automática
├── configurar_webhook.py               # Configura Evolution API
├── chatwoot_config.json                # Configurações da integração
├── INICIAR_INTEGRACAO_HIBRIDA.sh      # 🚀 Inicia tudo automaticamente
├── PARAR_INTEGRACAO.sh                # 🛑 Para tudo
└── logs/                              # Logs dos serviços
    ├── chatbot.log
    └── middleware.log
```

---

## 🚀 COMO USAR

### 1️⃣ Iniciar Integração (Tudo Automático)

```bash
./INICIAR_INTEGRACAO_HIBRIDA.sh
```

Este script faz **TUDO automaticamente**:
- ✅ Inicia o chatbot (porta 5001)
- ✅ Inicia o middleware (porta 5002)
- ✅ Inicia ngrok (expõe publicamente)
- ✅ Configura webhook na Evolution API
- ✅ Mostra URL pública e logs

---

### 2️⃣ Configurar Webhook do Chatwoot

Após iniciar, você terá uma URL ngrok. Agora configure o Chatwoot para enviar mensagens de atendentes:

**No Chatwoot:**
1. Acesse: `https://chatwoot.loop9.com.br`
2. Vá em **Settings** → **Inboxes** → **LF IMOVEIS** (ID: 40)
3. Vá em **Settings** da inbox
4. Em **Webhook URL**, coloque:
   ```
   https://SEU-NGROK-URL.ngrok-free.app/webhook/chatwoot
   ```
5. Marque os eventos:
   - ✅ Message Created
   - ✅ Message Updated
6. Salve

Pronto! A integração bidirecional está completa! 🎉

---

### 3️⃣ Testar a Integração

**Teste 1: Bot Automático**
1. Envie mensagem para: `+55 31 98016-0822`
2. Bot deve responder automaticamente
3. Mensagem aparece no Chatwoot

**Teste 2: Atendente Assume**
1. No Chatwoot, abra a conversa
2. Clique em "Assign to me" (atribuir para mim)
3. Envie uma mensagem pelo Chatwoot
4. Resposta vai para o WhatsApp
5. Bot fica em standby (não responde mais)

**Teste 3: Bot Volta**
1. No Chatwoot, resolva a conversa (marcar como "Resolved")
2. Cliente envia nova mensagem
3. Bot volta a responder automaticamente

---

### 4️⃣ Parar Integração

```bash
./PARAR_INTEGRACAO.sh
```

---

## 📊 Monitorar Logs

### Ver logs do Middleware (integração):
```bash
tail -f logs/middleware.log
```

### Ver logs do Chatbot:
```bash
tail -f logs/chatbot.log
```

### Ver status:
```bash
# Middleware
curl http://localhost:5002/health

# Chatbot
curl http://localhost:5001/health
```

---

## 🎯 Como Funciona

```
┌─────────────────────────────────────────────────────────────────┐
│                         FLUXO COMPLETO                          │
└─────────────────────────────────────────────────────────────────┘

1. MENSAGEM RECEBIDA:
   Cliente → WhatsApp → Evolution API

2. EVOLUTION ENVIA PARA MIDDLEWARE:
   Evolution API → ngrok → Middleware (porta 5002)

3. MIDDLEWARE PROCESSA:
   ├─ Envia mensagem para Chatwoot
   ├─ Verifica: Tem atendente ativo?
   │  ├─ SIM → Bloqueia bot (humano responde)
   │  └─ NÃO → Permite bot responder
   └─ Se bot pode responder:
      └─ Encaminha para chatbot_corretor.py (porta 5001)

4. BOT RESPONDE (se permitido):
   Bot → Evolution API → WhatsApp → Cliente

5. ATENDENTE RESPONDE:
   Chatwoot → Middleware → Evolution API → WhatsApp → Cliente

6. BOT VOLTA A FUNCIONAR:
   Conversa resolvida → Bot volta a responder automaticamente
```

---

## ⚙️ Configurações

Edite `chatwoot_config.json` para ajustar comportamento:

```json
{
  "bot": {
    "enabled": true,                          // Bot ligado/desligado
    "responde_quando_nao_ha_atendente": true, // Bot responde se sem atendente
    "responde_fora_horario": true             // Bot responde fora do horário
  }
}
```

---

## 🔧 Troubleshooting

### Middleware não recebe mensagens:
```bash
# Verifica se ngrok está rodando
curl http://localhost:4040/api/tunnels

# Verifica webhook Evolution
python3 configurar_webhook.py verificar
```

### Chatwoot não recebe mensagens:
```bash
# Verifica logs do middleware
tail -f logs/middleware.log

# Testa manualmente
curl -X POST http://localhost:5002/health
```

### Bot não responde:
```bash
# Verifica se bot está rodando
curl http://localhost:5001/health

# Verifica logs
tail -f logs/chatbot.log
```

### Ngrok mudou URL:
```bash
# Reconfigure webhook
./PARAR_INTEGRACAO.sh
./INICIAR_INTEGRACAO_HIBRIDA.sh
```

---

## 📝 Notas Importantes

- ⚠️ **Ngrok gratuito** muda URL a cada reinício (reconfigure webhook)
- ⚠️ **Mac precisa estar ligado** para tudo funcionar
- ✅ **Logs salvos** em `logs/` para debug
- ✅ **Configuração persistente** em `chatwoot_config.json`

---

## 🎉 Pronto para Produção

Para usar em produção (sem ngrok):

1. **Hospede o middleware** em um servidor (VPS, Heroku, etc.)
2. **Use domínio próprio** (ex: `https://webhook.seudominio.com`)
3. **Configure webhook fixo** na Evolution
4. **Configure webhook fixo** no Chatwoot
5. **Use PM2** para manter processos rodando:
   ```bash
   pm2 start chatbot_corretor.py --name "chatbot"
   pm2 start webhook_middleware.py --name "middleware"
   pm2 save
   ```

---

## 💡 Dicas

### Personalizar respostas do bot:
Edite `chatbot_corretor.py`, variável `PROMPT_CORRETOR` (linha 54)

### Adicionar mais números permitidos:
Edite `chatbot_corretor.py`, linha 37:
```python
NUMEROS_PERMITIDOS = ["5531980160822", "5531999999999"]
```

### Alterar porta do middleware:
Edite `webhook_middleware.py`, última linha:
```python
app.run(host='0.0.0.0', port=5002, debug=False)  # Altere 5002
```

---

## 📞 Suporte

Se tiver problemas:
1. Verifique logs: `logs/middleware.log` e `logs/chatbot.log`
2. Teste conexões: `python3 setup_chatwoot_integration.py` (opção 1)
3. Reinicie tudo: `./PARAR_INTEGRACAO.sh && ./INICIAR_INTEGRACAO_HIBRIDA.sh`

---

**Criado por:** Claude Code
**Data:** 2025-11-01
**Versão:** 1.0 - Integração Híbrida Completa
