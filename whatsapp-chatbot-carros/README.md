# 🚗 Chatbot Automaia - Bot WhatsApp V1

Bot de WhatsApp inteligente para **Automaia - Agência de Carros Seminovos**.

Baseado no Chatbot Corretor V4, com adaptações para vendas de veículos.

---

## 🚀 Quick Start

### Iniciar Bot:
```bash
./INICIAR_BOT_AUTOMAIA.sh
```

### Parar Bot:
```bash
./PARAR_BOT_AUTOMAIA.sh
```

---

## 📊 Arquitetura

```
whatsapp-chatbot-carros/
├── chatbot_automaia_v1.py         # Bot principal (porta 5003)
├── webhook_middleware_automaia.py # Middleware (porta 5004)
├── upload_fotos_carros.py         # Upload fotos de carros
│
├── INICIAR_BOT_AUTOMAIA.sh        # 🚀 Script de inicialização
├── PARAR_BOT_AUTOMAIA.sh          # 🛑 Script para parar
│
├── logs/                          # Logs do bot
│   ├── chatbot_automaia.log
│   └── middleware_automaia.log
│
├── carros/                        # Banco de carros
│   └── [id-do-carro]/
│       ├── base.txt               # Marca, modelo, ano, km, preço
│       ├── detalhes.txt           # Motor, opcionais, estado
│       ├── faq.txt                # Perguntas frequentes
│       ├── historico.txt          # Proprietários, acidentes, revisões
│       ├── financiamento.txt      # Opções de pagamento
│       └── links.json             # URLs das fotos (Nextcloud)
│
├── componentes/                   # Framework Híbrido (copiado de imóveis)
│   ├── rag/
│   ├── score/
│   ├── followup/
│   ├── escalonamento/
│   └── relatorios/
│
├── chatwoot_config_automaia.json  # Config Chatwoot + Evolution
└── README.md                      # Este arquivo
```

---

## ⚡ Funcionalidades V1

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

### 🚗 Negócio:
- ✅ **Banco de carros** (busca inteligente)
- ✅ **Envio automático de fotos**
- ✅ **Integração Chatwoot** (híbrida)
- ✅ **Timers por número** (evita duplicação)

---

## 📝 Setup Inicial

### 1️⃣ Criar Instância Evolution API

**Nome da instância:** `automaia`

```bash
# No painel Evolution API:
1. Criar nova instância "automaia"
2. Escanear QR Code
3. Copiar API Key
```

### 2️⃣ Criar Inbox no Chatwoot

```bash
# No painel Chatwoot:
1. Settings → Inboxes → Add Inbox
2. Nome: "Automaia - Seminovos"
3. Tipo: WhatsApp (via Evolution)
4. Copiar Inbox ID (ex: 123)
```

### 3️⃣ Configurar Chatwoot e Credenciais

**Execute o script de setup:**
```bash
python3 setup_chatwoot.py
```

Este script vai:
- ✅ Criar inbox no Chatwoot automaticamente
- ✅ Gerar arquivo `chatwoot_config_automaia.json`
- ✅ Configurar todas as credenciais

**Informações necessárias:**
- URL do Chatwoot (ex: https://chatwoot.loop9.com.br)
- Access Token do Chatwoot
- Account ID (normalmente 1)
- API Key da Evolution API
- Nome da instância Evolution

### 4️⃣ Adicionar Carros

**Passo 1: Organizar fotos**

```bash
# Crie a estrutura:
~/Desktop/fotos de carros/
├── gol-prata-2020/
│   ├── frente.jpg
│   ├── lateral.jpg
│   ├── interior.jpg
│   └── painel.jpg
├── civic-preto-2019/
│   └── ...
```

**Passo 2: Upload para Nextcloud**

```bash
python3 upload_fotos_carros.py
```

Isso vai:
- Fazer upload das fotos para Nextcloud
- Gerar links públicos permanentes
- Criar arquivos template (base.txt, detalhes.txt, etc)

**Passo 3: Preencher informações**

Edite os arquivos criados em `carros/[id-do-carro]/`:

```bash
# Exemplo: carros/gol-prata-2020/
vim base.txt          # Marca, modelo, ano, km, preço
vim detalhes.txt      # Motor, opcionais, consumo
vim faq.txt           # Perguntas frequentes
vim historico.txt     # Proprietários, acidentes
vim financiamento.txt # Planos de pagamento
```

### 5️⃣ Configurar Filtro de Números (Opcional)

**Para restringir quais números podem interagir com o bot:**

```bash
python3 configurar_filtro_numero.py
```

- Digite os números permitidos (formato: 5531986549366)
- Script gera automaticamente variações (com/sem 9 extra)
- Outros números serão ignorados automaticamente

**Para aceitar TODOS os números:**
- Pule esta etapa e remova o filtro em `webhook_middleware_automaia.py`

### 6️⃣ Iniciar Bot com Ngrok

**✅ RECOMENDADO - Use sempre com ngrok:**

```bash
./INICIAR_COM_NGROK.sh
```

Este script automático vai:
- ✅ Iniciar middleware (porta 5004)
- ✅ Iniciar bot (porta 5003)
- ✅ Iniciar ngrok e obter URL pública
- ✅ Configurar webhook Evolution automaticamente
- ✅ Configurar webhook Chatwoot automaticamente

**Verificar status:**
```bash
curl http://localhost:5003/health
curl http://localhost:5004/health
```

**⚠️ Alternativa - Sem ngrok (apenas local, webhooks NÃO funcionarão):**

```bash
./INICIAR_BOT_AUTOMAIA.sh
```

---

## 🔧 Comandos Úteis

### Ver logs em tempo real:
```bash
# Bot
tail -f logs/chatbot_automaia.log

# Middleware
tail -f logs/middleware_automaia.log
```

### Verificar processos:
```bash
ps aux | grep automaia
```

### Matar processos manualmente:
```bash
pkill -f chatbot_automaia_v1.py
pkill -f webhook_middleware_automaia.py
```

---

## 📸 Estrutura de Dados de um Carro

```
carros/gol-prata-2020/
├── base.txt              # Informações básicas
├── detalhes.txt          # Detalhes técnicos
├── faq.txt               # Perguntas frequentes
├── historico.txt         # Histórico do veículo
├── financiamento.txt     # Opções de pagamento
└── links.json            # Links das fotos (gerado automaticamente)
```

### Exemplo base.txt:
```
🚗 Volkswagen Gol 1.0 2020

📋 Informações Básicas:
• Marca: Volkswagen
• Modelo: Gol 1.0 Flex
• Ano: 2020
• Kilometragem: 35.000 km
• Cor: Prata
• Combustível: Flex
• Câmbio: Manual

💰 Preço:
• À vista: R$ 45.000
• Entrada: R$ 10.000
• Parcelas: R$ 1.200/mês (até 48x)
```

---

## 🤖 Como o Bot Funciona

### Fluxo de Mensagem:

```
1. Cliente envia WhatsApp
   ↓
2. Evolution API → Middleware (porta 5004)
   ↓
3. Middleware cria mensagem no Chatwoot
   ↓
4. Chatwoot verifica: Tem atendente?
   ├─ SIM → Bloqueia bot, atendente responde
   └─ NÃO → Envia para Bot (porta 5003)
   ↓
5. Bot processa com IA (Claude Haiku 4.5)
   ↓
6. Bot detecta comando [ENVIAR_FOTOS:id-carro]
   ↓
7. Bot envia resposta + fotos via Evolution
   ↓
8. Cliente recebe mensagem
```

### Comando de Fotos:

Quando o cliente pede fotos, o bot responde:
```
"Claro! Vou te enviar as fotos agora 🚗 [ENVIAR_FOTOS:gol-prata-2020]"
```

O sistema detecta `[ENVIAR_FOTOS:gol-prata-2020]` e automaticamente envia todas as fotos do carro.

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **Flask** (webhooks)
- **OpenRouter** (Claude Haiku 4.5)
- **OpenAI** (Whisper + GPT-4o Vision)
- **Upstash Redis** (contexto + filas)
- **Evolution API** (WhatsApp)
- **Chatwoot** (atendimento híbrido)
- **Nextcloud** (armazenamento de fotos)

---

## 📊 Métricas

Acesse:
```bash
curl http://localhost:5003/health
```

Retorna:
```json
{
  "status": "online",
  "version": "1.0 - AUTOMAIA SEMINOVOS",
  "chatbot": "Automaia V1",
  "model": "anthropic/claude-haiku-4.5",
  "carros": {
    "total": 5,
    "total_fotos": 20,
    "ids": ["gol-prata-2020", "civic-preto-2019", ...]
  },
  "timers_ativos": 3
}
```

---

## 🐛 Troubleshooting

### Bot não responde:

1. Verificar se está rodando:
   ```bash
   curl http://localhost:5003/health
   ```

2. Ver logs:
   ```bash
   tail -f logs/chatbot_automaia.log
   ```

3. Verificar Redis:
   ```bash
   # No código Python:
   redis.ping()
   ```

### Fotos não enviam:

1. Verificar links.json:
   ```bash
   cat carros/[id-carro]/links.json
   ```

2. Testar URL das fotos (abrir no navegador)

3. Verificar se Evolution API está online

### Atendente não consegue assumir:

1. Verificar webhook do Chatwoot
2. Ver logs do middleware:
   ```bash
   tail -f logs/middleware_automaia.log
   ```

---

## 📚 Próximos Passos

- [ ] Integrar Framework Híbrido (RAG, Score, Follow-ups)
- [ ] Adicionar mais carros
- [ ] Criar relatórios de vendas
- [ ] Integração com CRM

---

## 📞 Suporte

Em caso de dúvidas, consulte:
- `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/CLAUDE.md`
- `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/README.md` (chatbot de imóveis)

---

**Versão:** 1.0
**Data:** 04/11/2025
**Status:** ✅ Pronto para produção (após configuração)
