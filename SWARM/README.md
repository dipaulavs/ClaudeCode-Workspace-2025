

# 🐳 Sistema de Deploy - Docker Swarm + Traefik

Sistema profissional integrado com seu ambiente Hostinger/Portainer para deploy de automações 24/7 com SSL automático via Traefik.

---

## 🎯 O Que É Isso?

Deploy automações do Mac para VPS rodando em **Docker Swarm** com:
- ✅ SSL automático (Let's Encrypt via Traefik)
- ✅ Subdomínios `*.loop9.com.br`
- ✅ Integrado com N8N, Evolution, Chatwoot, etc
- ✅ Mesma rede overlay (`loop9Net`)
- ✅ Healthcheck e auto-restart
- ✅ Escalável (replicas)

---

## 📁 Estrutura

```
SWARM/
├── new.sh              → Criar nova automação
├── deploy.sh           → Deploy para Swarm
├── logs.sh             → Ver logs remotos
├── manage.sh           → Gerenciar stacks
├── README.md           → Este arquivo
├── templates/          → Templates com Traefik
│   └── webhook-api/
└── automations/        → Suas automações
    ├── chatbot-vendas/
    └── scraper-imoveis/
```

---

## 🚀 Quick Start (GitHub-First)

### **1. Criar Automação:**

```bash
cd SWARM

# Criar estrutura
./new.sh chatbot-vendas webhook-api chatbot

# Estrutura criada:
# automations/chatbot-vendas/
# ├── docker-compose.yml (com labels Traefik)
# ├── Dockerfile
# ├── app.py
# ├── requirements.txt
# └── .env
```

### **2. Configurar Git:**

```bash
cd automations/chatbot-vendas

# Inicializar repositório
git init
git add .
git commit -m "feat: criar estrutura inicial chatbot-vendas"

# Criar repositório no GitHub (via gh CLI ou web)
gh repo create chatbot-vendas --private --source=. --remote=origin

# Ou adicionar remote manualmente:
# git remote add origin git@github.com:seu-usuario/chatbot-vendas.git

git push -u origin main
```

### **3. Desenvolver:**

```bash
# Edite app.py com Claude Code
# Configure .env com credenciais
# Teste localmente (opcional):
python3 app.py

# Commit mudanças
git add .
git commit -m "feat: implementar lógica do chatbot"
git push origin main
```

### **4. Deploy (VPS):**

```bash
# SSH na VPS
ssh root@82.25.68.132

# Clone repositório (primeira vez)
cd /opt/swarm/automations
git clone git@github.com:seu-usuario/chatbot-vendas.git
cd chatbot-vendas

# Deploy no Swarm
docker stack deploy -c docker-compose.yml chatbot-vendas

# ✅ Deploy concluído!
# 🌐 Acesso: https://chatbot.loop9.com.br
```

### **5. Atualizar (após mudanças):**

```bash
# SSH na VPS
ssh root@82.25.68.132
cd /opt/swarm/automations/chatbot-vendas

# Atualizar código
git pull origin main

# Re-deploy
docker stack deploy -c docker-compose.yml chatbot-vendas
```

### **4. Gerenciar:**

```bash
# Ver logs
./logs.sh chatbot-vendas

# Status
./manage.sh status chatbot-vendas

# Reiniciar
./manage.sh restart chatbot-vendas

# Listar todas
./manage.sh list
```

---

## 🎬 Exemplo Completo

**Do zero ao deploy em 5 minutos:**

```bash
cd SWARM

# 1. Criar
./new.sh bot-telegram webhook-api bot

# 2. Desenvolver
cd automations/bot-telegram
# Pede ao Claude: "Cria bot Telegram que responde com IA"
cd ../..

# 3. Deploy
./deploy.sh bot-telegram

# 4. Acessar
# https://bot.loop9.com.br
```

**Pronto! Bot rodando com SSL!** 🎉

---

## 📝 Comandos Detalhados

### **new.sh - Criar Automação**

```bash
./new.sh <nome> [template] [subdominio]

# Exemplos:
./new.sh chatbot-vendas webhook-api chatbot
  → https://chatbot.loop9.com.br

./new.sh api-produtos webhook-api api
  → https://api.loop9.com.br

./new.sh scraper webhook-api scraper
  → https://scraper.loop9.com.br
```

**Templates disponíveis:**
- `webhook-api` - Servidor HTTP/API (Flask)

### **deploy.sh - Deploy**

```bash
./deploy.sh <nome>

# Faz:
# 1. Build da imagem Docker
# 2. Envia para VPS
# 3. Deploy no Swarm
# 4. Traefik configura SSL automático
```

### **logs.sh - Ver Logs**

```bash
./logs.sh <nome> [linhas]

# Exemplos:
./logs.sh chatbot-vendas          # Últimas 50
./logs.sh chatbot-vendas 100      # Últimas 100
./logs.sh chatbot-vendas 0        # Todas (follow)
```

### **manage.sh - Gerenciar**

```bash
./manage.sh <comando> [nome]

# Comandos:
list                    # Lista todas stacks
status <nome>           # Status da stack
restart <nome>          # Reinicia (force update)
scale <nome> <num>      # Escala réplicas
remove <nome>           # Remove stack

# Exemplos:
./manage.sh list
./manage.sh status chatbot-vendas
./manage.sh restart chatbot-vendas
./manage.sh scale chatbot-vendas 3
./manage.sh remove bot-antigo
```

---

## 🌐 Como Funciona o Traefik

### **Roteamento Automático:**

```yaml
# No docker-compose.yml:
labels:
  - "traefik.http.routers.chatbot.rule=Host(`chatbot.loop9.com.br`)"
  - "traefik.http.routers.chatbot.tls.certresolver=letsencrypt"
```

**Traefik automaticamente:**
1. ✅ Detecta novo serviço
2. ✅ Configura roteamento
3. ✅ Gera certificado SSL
4. ✅ Redireciona HTTP → HTTPS

**Sem configuração manual!**

---

## 🔧 Customizar Automação

### **Adicionar Banco de Dados:**

```yaml
# docker-compose.yml
services:
  app:
    # ... config existente

  postgres:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: senha
      POSTGRES_DB: meudb
    networks:
      - loop9Net
    deploy:
      replicas: 1
```

### **Adicionar Redis:**

```yaml
  redis:
    image: redis:7-alpine
    networks:
      - loop9Net
```

### **Cronjob (Scheduled Task):**

```python
# app.py
import schedule
import time

def job():
    print("Tarefa executada!")
    # Sua lógica

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## 🚨 Troubleshooting

### **Deploy falha:**

```bash
# Ver logs detalhados
./deploy.sh chatbot-vendas 2>&1 | tee deploy.log

# Verificar na VPS
ssh root@82.25.68.132
docker stack ps chatbot-vendas --no-trunc
```

### **SSL não gera:**

```bash
# Verificar logs do Traefik
ssh root@82.25.68.132
docker service logs traefik_traefik -f

# Verificar DNS
nslookup chatbot.loop9.com.br

# Deve apontar para: 82.25.68.132
```

### **Container não inicia:**

```bash
# Ver status
./manage.sh status chatbot-vendas

# Ver logs
./logs.sh chatbot-vendas

# Rebuild
./deploy.sh chatbot-vendas
```

---

## 🎯 Integração com Serviços Existentes

### **Chamar N8N de uma Automação:**

```python
# app.py
import requests

def trigger_n8n():
    url = "https://n8n.loop9.com.br/webhook/seu-webhook"
    data = {"mensagem": "Olá do chatbot!"}
    requests.post(url, json=data)
```

### **Usar Evolution API:**

```python
import os
import requests

EVOLUTION_URL = "https://evolution.loop9.com.br"
EVOLUTION_KEY = os.getenv("EVOLUTION_API_KEY")

def send_whatsapp(number, message):
    headers = {"apikey": EVOLUTION_KEY}
    data = {
        "number": number,
        "text": message
    }
    requests.post(f"{EVOLUTION_URL}/message/sendText",
                 json=data, headers=headers)
```

---

## 📊 Diferenças do Sistema Anterior

| Feature | Sistema Antigo (production/) | Sistema Novo (SWARM/) |
|---------|------------------------------|----------------------|
| Deploy | docker compose | docker stack deploy |
| Rede | bridge local | overlay (loop9Net) |
| SSL | Manual ou ngrok | Automático (Traefik) |
| Domínio | IP:porta | subdominio.loop9.com.br |
| Integração | Isolado | Mesma rede N8N/Evolution |
| Escalabilidade | 1 réplica fixa | Escalável (N réplicas) |
| Gerenciamento | Scripts manuais | Swarm + Portainer |

---

## 🎊 Benefícios

```
✅ SSL automático (Let's Encrypt)
✅ Subdomínios profissionais
✅ Integrado com serviços existentes
✅ Mesma rede do N8N/Evolution/Chatwoot
✅ Escalável (múltiplas réplicas)
✅ Auto-restart e healthcheck
✅ Deploy com um comando
✅ Logs centralizados
✅ Gerenciamento via Portainer
```

---

## 🔐 Segurança

### **Variáveis Sensíveis:**

**Nunca** comite `.env` no git!

```bash
# .env (local, não commitado)
OPENAI_API_KEY=sk-real-key
EVOLUTION_API_KEY=real-key

# .env.example (no git)
OPENAI_API_KEY=sk-...
EVOLUTION_API_KEY=sua-chave
```

### **Secrets do Swarm (Opcional):**

```yaml
# docker-compose.yml
secrets:
  openai_key:
    external: true

services:
  app:
    secrets:
      - openai_key
```

```bash
# Criar secret
echo "sk-real-key" | ssh root@82.25.68.132 \
  "docker secret create openai_key -"
```

---

## 🌍 Webhooks do N8N

### **Usar Automação como Webhook:**

**1. No N8N:**
```
Webhook Node
URL: https://chatbot.loop9.com.br/webhook
Method: POST
```

**2. Na Automação:**
```python
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Processar dados do N8N
    result = process(data)

    # Enviar resposta de volta
    return jsonify(result)
```

**3. Fluxo:**
```
N8N → https://chatbot.loop9.com.br/webhook → Processa → Responde → N8N
```

---

## 📈 Monitoramento

### **Via Portainer:**
- Acesse: `https://portainer.loop9.com.br`
- Stacks → Ver suas automações
- Logs, métricas, restart, etc

### **Via Terminal:**
```bash
# Listar tudo
./manage.sh list

# Status específico
./manage.sh status chatbot-vendas

# Logs em tempo real
./logs.sh chatbot-vendas
```

---

## 🎓 Exemplos Práticos

### **1. Chatbot WhatsApp**

```bash
./new.sh chatbot-whatsapp webhook-api whatsapp
cd automations/chatbot-whatsapp

# Editar app.py para integrar com Evolution
# Configurar webhook no Evolution:
# https://whatsapp.loop9.com.br/webhook

./deploy.sh chatbot-whatsapp
```

### **2. Scraper Periódico**

```bash
./new.sh scraper-imoveis webhook-api scraper
cd automations/scraper-imoveis

# app.py com schedule.every(1).hour
# Salva dados em banco/arquivo

./deploy.sh scraper-imoveis
```

### **3. API REST**

```bash
./new.sh api-clientes webhook-api api
cd automations/api-clientes

# Implementa endpoints REST
# GET /clientes, POST /clientes, etc

./deploy.sh api-clientes
# https://api.loop9.com.br
```

---

## 🔄 Workflow de Atualização (GitHub-First)

**⚠️ NUNCA deploy direto da máquina local para VPS!**

**Fluxo OBRIGATÓRIO:**

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Local   │ ──> │  GitHub  │ ──> │   VPS    │
│ Develop  │ git │  Source  │ git │  Deploy  │
└──────────┘     └──────────┘     └──────────┘
```

**Quando modificar código:**

```bash
# 1. LOCAL: Editar código
cd SWARM/automations/chatbot-vendas
vim app.py

# Testar localmente
python3 app.py

# 2. COMMITAR no GitHub
git add .
git commit -m "feat: adicionar nova funcionalidade"
git push origin main

# 3. VPS: Atualizar e re-deploy
ssh root@82.25.68.132
cd /opt/swarm/automations/chatbot-vendas
git pull origin main
docker stack deploy -c docker-compose.yml chatbot-vendas

# Container atualizado automaticamente!
```

**Automatizar (opcional):**
- GitHub Actions: Push → Auto-deploy na VPS
- Webhook: GitHub → N8N → VPS deploy

---

## 💡 Dicas

1. **Use Claude Code** para desenvolver em `automations/<nome>/`
2. **Teste local** antes de deployar (economiza tempo)
3. **`.env` para credenciais**, nunca hardcode
4. **Logs** para debug (`./logs.sh`)
5. **Escale** se precisar performance (`./manage.sh scale <nome> 3`)

---

## 🆘 Suporte

### **Logs detalhados:**
```bash
./logs.sh <nome> 500
```

### **SSH na VPS:**
```bash
ssh root@82.25.68.132
docker stack ps <nome> --no-trunc
docker service logs <service-id> -f
```

### **Rebuild completo:**
```bash
./manage.sh remove <nome>
./deploy.sh <nome>
```

---

## 🎯 Roadmap

- [ ] Template cronjob
- [ ] Template chatbot-whatsapp
- [ ] Template scraper
- [ ] Backup automático
- [ ] Métricas (Prometheus)
- [ ] CI/CD GitHub Actions

---

**Sistema criado em:** 2025-11-05
**VPS:** 82.25.68.132 (Hostinger)
**Domínio:** loop9.com.br
**Stack:** Docker Swarm + Traefik + Portainer

**Happy Deploying!** 🚀
