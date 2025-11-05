# 🤖 Framework Universal de Chatbot WhatsApp

**Versão:** 1.0
**Base:** whatsapp-chatbot-carros (Automaia)
**Stack:** Python + Flask + Redis + Chatwoot + Evolution API

---

## 🎯 Visão Geral

Framework completo e reutilizável para criar chatbots WhatsApp inteligentes para qualquer nicho em **5 minutos**.

**Capacidades:**
- ✅ RAG Híbrido (keywords + semântico)
- ✅ 4 Ferramentas via Function Calling
- ✅ Follow-ups automáticos (Redis)
- ✅ Score de leads inteligente
- ✅ Escalonamento (notifica vendedor)
- ✅ Agenda Google Sheets (OAuth)
- ✅ Áudio (Whisper) + Imagem (GPT-4o Vision)
- ✅ Respostas em chunks
- ✅ Tagueamento Chatwoot
- ✅ Métricas e relatórios
- ✅ Progressive Disclosure (economia 50% tokens)

---

## 📁 Estrutura do Framework

```
ClaudeCode-Workspace/
├── chatbot-template/              # Template base (cópia Automaia)
│   ├── chatbot_automaia_v4.py     # Bot principal
│   ├── webhook_middleware_automaia.py
│   ├── componentes/               # 5 componentes
│   │   ├── rag/                   # RAG Híbrido
│   │   ├── score/                 # Sistema de pontuação
│   │   ├── followup/              # Follow-ups automáticos
│   │   ├── escalonamento/         # Agenda + Notificações
│   │   └── relatorios/            # Métricas
│   ├── ferramentas/               # 4 Ferramentas (function calling)
│   │   ├── lista_carros.py        # Lista itens disponíveis
│   │   ├── consulta_faq.py        # Busca FAQ (subagente)
│   │   ├── tagueamento.py         # Tags Chatwoot
│   │   └── agendar_visita.py      # Agenda + notifica vendedor
│   ├── carros/                    # Database de itens
│   └── config/                    # Configs
│
├── criar_chatbot_cliente.py       # 🚀 GERADOR (script principal)
│
└── whatsapp-chatbot-{slug}/       # Chatbot gerado (output)
```

---

## 🚀 Uso Rápido

### 1. Gerar Novo Chatbot

```bash
python3 criar_chatbot_cliente.py
```

**Interativo:**
- Nome do cliente
- Nicho (Imobiliária, Loja, Seminovos, Telemarketing, Personalizado)
- Descrição do negócio
- WhatsApp vendedor
- Porta (padrão: 5005)

**Resultado:** Pasta `whatsapp-chatbot-{slug}` completa e funcional

### 2. Configurar APIs

Editar `chatwoot_config_{slug}.json`:
```json
{
  "chatwoot": {
    "url": "https://chatwoot.loop9.com.br",
    "token": "SEU_TOKEN",
    "inbox_id": "42"
  },
  "evolution": {
    "url": "https://evolution.loop9.com.br",
    "api_key": "SUA_KEY",
    "instance": "slug"
  }
}
```

### 3. Criar Agenda Google Sheets

```bash
cd whatsapp-chatbot-{slug}

# Autenticar OAuth (1x)
python3 componentes/escalonamento/autenticar_google.py

# Criar planilha
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

### 4. Adicionar Itens (Produtos/Imóveis/Carros)

Estrutura em `{pasta_itens}/`:
```
imoveis/
└── apartamento-leblon-001/
    ├── base.txt          # Info básica (nome, preço, localização)
    ├── detalhes.txt      # Especificações técnicas
    ├── faq.txt           # Perguntas frequentes
    ├── legal.txt         # Documentação (opcional)
    ├── financiamento.txt # Opções pagamento (opcional)
    └── links.json        # URLs das fotos
```

### 5. Iniciar Bot

```bash
./INICIAR_COM_NGROK.sh
```

**Verifica:**
- ✅ Bot: ONLINE (porta 5005)
- ✅ Middleware: ONLINE (porta 5006)
- ✅ Ngrok: URL pública configurada

---

## 🛠️ Componentes Técnicos

### 1. RAG Híbrido (`componentes/rag/`)

**Busca Inteligente:**
- Keywords (BM25): precisão
- Semântica (embeddings): contexto
- Progressive Disclosure: carrega só necessário

**Fluxo:**
1. Cliente pergunta sobre item
2. RAG busca nos arquivos .txt
3. IA Especialista responde com contexto

### 2. Sistema de Score (`componentes/score/`)

**Pontuação 0-100:**
- Interações
- Perguntas qualificadas
- Interesse em agendamento
- Origem (orgânico/anúncio)

**Tags automáticas:** `lead-quente`, `apenas-curioso`, etc.

### 3. Follow-ups (`componentes/followup/`)

**Automático via Redis:**
- Abandono pós-interesse
- Abandono pré-agendamento
- Follow-up 24h/48h/7d

**Mensagens humanizadas por contexto**

### 4. Escalonamento (`componentes/escalonamento/`)

**Agenda Google Sheets:**
- Consulta horários disponíveis
- Sugere 3 opções ao cliente
- Confirma escolha
- Notifica vendedor via WhatsApp

**Notificação inclui:**
- Nome cliente
- Score
- Carro/item de interesse
- Data/hora agendada

### 5. Ferramentas (Function Calling)

**4 ferramentas Claude Haiku 4.5:**

1. **lista_itens** → Busca itens disponíveis
2. **consulta_faq** → Subagente com FAQ completo
3. **tagueamento** → Marca conversa no Chatwoot
4. **agendar_visita** → 2 passos + notifica vendedor

---

## 🎨 Nichos Pré-Configurados

### 1. Imobiliária

**Pasta:** `imoveis/`
**Tom:** Profissional e consultivo
**Campos:** base, detalhes, faq, legal, financiamento, links

### 2. Loja/E-commerce

**Pasta:** `produtos/`
**Tom:** Amigável e prestativo
**Campos:** base, detalhes, faq, garantia, especificacoes, links

### 3. Seminovos (Carros)

**Pasta:** `carros/`
**Tom:** Direto e transparente
**Campos:** base, detalhes, faq, historico, financiamento, links

### 4. Telemarketing/Serviços

**Pasta:** `servicos/`
**Tom:** Persuasivo e profissional
**Campos:** base, detalhes, faq, planos, diferenciais

### 5. Personalizado

**Configuração customizada durante criação**

---

## 📊 Métricas e Relatórios

**Dashboard automático:**
- Total conversas
- Taxa conversão
- Score médio
- Horários pico
- Follow-ups enviados
- Agendamentos confirmados

**Relatórios:**
- Diário (via cron)
- Semanal (dashboard completo)
- Por item (mais procurados)

---

## 🔧 Manutenção

### Ver Logs

```bash
tail -f logs/chatbot_{slug}.log
```

### Adicionar Novo Item

```bash
# 1. Criar pasta
mkdir -p {pasta_itens}/novo-item-001

# 2. Preencher arquivos
nano {pasta_itens}/novo-item-001/base.txt

# 3. Upload fotos (opcional)
python3 upload_fotos_{pasta_itens}.py
```

### Atualizar Agenda

```bash
# Adicionar mais 7 dias
python3 componentes/escalonamento/atualizar_agenda.py --dias 7
```

### Backup

```bash
# Automático via Redis
# Conversas: TTL 24h
# Contexto: TTL 7d
```

---

## 🆚 Diferenças vs Chatbot Comum

| Recurso | Chatbot Comum | Framework Universal |
|---------|---------------|---------------------|
| **Setup** | Dias/semanas | 5 minutos |
| **RAG** | Simples | Híbrido (keywords + semântico) |
| **Follow-ups** | Manual | Automático (Redis) |
| **Agendamento** | Não | Google Sheets + notificações |
| **Score** | Não | 0-100 inteligente |
| **Multimodal** | Só texto | Áudio + Imagem |
| **Escalável** | Não | Multi-tenant pronto |
| **Manutenção** | Alta | Baixa (add itens = arquivos .txt) |

---

## 🚀 Roadmap

- [ ] Interface web para gerenciar itens
- [ ] Multi-instância (1 servidor = N clientes)
- [ ] Analytics dashboard real-time
- [ ] Integração CRM (Pipedrive, RD Station)
- [ ] Suporte Telegram/Instagram DM

---

## 📖 Documentações Relacionadas

**Criadas automaticamente:**
- `whatsapp-chatbot-{slug}/README.md` → Setup específico do cliente
- `componentes/escalonamento/README_ESCOLHA_METODO.md` → Agenda Google Sheets
- `componentes/followup/README.md` → Sistema de follow-ups

---

## 💡 Exemplos de Uso

### Criar chatbot para imobiliária

```bash
$ python3 criar_chatbot_cliente.py

📝 Nome do cliente/empresa: Imobiliária Horizonte
🎯 Escolha o nicho: 1 (Imobiliária)
📋 Descrição: Imóveis de alto padrão em Belo Horizonte
📱 WhatsApp vendedor: 5531999887766
🔌 Porta: 5007

✅ CHATBOT CRIADO: whatsapp-chatbot-imobiliaria-horizonte
```

### Criar chatbot para loja de eletrônicos

```bash
$ python3 criar_chatbot_cliente.py

📝 Nome do cliente/empresa: TechStore BH
🎯 Escolha o nicho: 2 (Loja/E-commerce)
📋 Descrição: Loja de eletrônicos e informática
📱 WhatsApp vendedor: 5531988776655
🔌 Porta: 5009

✅ CHATBOT CRIADO: whatsapp-chatbot-techstore-bh
```

---

## 🆘 Suporte

**Problemas comuns:**

### Bot não responde
```bash
# Verificar logs
tail -f logs/chatbot_{slug}.log

# Verificar portas
lsof -i :5005
```

### Agenda não consulta
```bash
# Verificar Google Sheet ID
cat chatwoot_config_{slug}.json | grep google_sheet_id

# Re-autenticar OAuth
python3 componentes/escalonamento/autenticar_google.py
```

### Follow-ups não enviam
```bash
# Verificar Redis
redis-cli ping

# Processar manualmente
python3 componentes/followup/processador_cron.py
```

---

**✅ Framework pronto para produção!**

**Baseado em:** whatsapp-chatbot-carros (Automaia)
**Criado:** 2025-01-05
**Autor:** Claude Code + Felipe Paula
