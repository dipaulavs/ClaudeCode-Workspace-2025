# 🚀 Sistema de Deploy Híbrido - Mac ↔ VPS

Sistema profissional para desenvolver automações localmente no Mac com Claude Code e fazer deploy para VPS rodando 24/7 em containers Docker.

---

## 📋 Visão Geral

```
┌──────────────────┐         ┌─────────────────┐
│   MAC (Dev)      │         │  VPS (Produção) │
├──────────────────┤         ├─────────────────┤
│ Claude Code      │         │ Docker 24/7     │
│ Desenvolve aqui  │  ────>  │ Automações aqui │
│ Testa local      │ Deploy  │ 82.25.68.132    │
└──────────────────┘         └─────────────────┘
```

---

## 🎯 Workflow Completo

### 1️⃣ Criar Nova Automação

```bash
./new.sh minha-automacao webhook-api
```

**Estrutura criada:**
```
production/deployed/minha-automacao/
├── Dockerfile
├── docker-compose.yml
├── app.py
├── requirements.txt
├── .env
├── data/
└── logs/
```

### 2️⃣ Desenvolver com Claude Code

```bash
# No Mac, normalmente
cd production/deployed/minha-automacao
code .

# Desenvolve com Claude Code
# Testa localmente
python3 app.py
```

### 3️⃣ Deploy para VPS

```bash
./deploy.sh minha-automacao 8080
```

**O que acontece:**
1. ✅ Valida estrutura
2. ✅ Roda testes (se existir test.sh)
3. ✅ Envia arquivos via rsync
4. ✅ Builda container Docker
5. ✅ Inicia serviço 24/7
6. ✅ Verifica status

### 4️⃣ Gerenciar Automação

```bash
# Ver logs em tempo real
./logs.sh minha-automacao

# Status
./manage.sh status minha-automacao

# Reiniciar
./manage.sh restart minha-automacao

# Parar
./manage.sh stop minha-automacao

# Listar todas
./manage.sh list
```

---

## 📁 Estrutura de Pastas

### No Mac (Desenvolvimento)

```
ClaudeCode-Workspace/
├── production/
│   ├── templates/           → Templates de automações
│   │   └── webhook-api/
│   └── deployed/            → Suas automações
│       ├── chatbot-vendas/
│       ├── scraper-imoveis/
│       └── notificador/
├── deploy.sh                → Deploy para VPS
├── logs.sh                  → Ver logs remotos
├── manage.sh                → Gerenciar automações
└── new.sh                   → Criar nova automação
```

### Na VPS (Produção)

```
/root/
├── automations/             → Automações rodando 24/7
│   ├── chatbot-vendas/
│   │   ├── docker-compose.yml
│   │   ├── app.py
│   │   └── .env
│   └── scraper-imoveis/
└── workspace/               → Backup/mirror
```

---

## 🛠️ Comandos Disponíveis

### new.sh - Criar Automação

```bash
./new.sh <nome> [template]

# Exemplos:
./new.sh chatbot-vendas webhook-api
./new.sh scraper-dados webhook-api
```

**Templates disponíveis:**
- `webhook-api` - Servidor HTTP/API (Flask)
- Mais templates em breve (cronjob, chatbot, etc)

---

### deploy.sh - Deploy para VPS

```bash
./deploy.sh <nome> [porta]

# Exemplos:
./deploy.sh chatbot-vendas 8080
./deploy.sh scraper-dados 8081
./deploy.sh notificador none  # Sem porta exposta
```

**Flags automáticas:**
- Exclui: venv, __pycache__, .git, *.pyc
- Valida: Dockerfile obrigatório
- Testes: Roda test.sh se existir

---

### logs.sh - Ver Logs

```bash
./logs.sh <nome> [linhas]

# Exemplos:
./logs.sh chatbot-vendas        # Últimas 50 linhas
./logs.sh chatbot-vendas 100    # Últimas 100 linhas
./logs.sh chatbot-vendas 0      # Todas (infinito)
```

**Modo follow:** Logs em tempo real (CTRL+C para sair)

---

### manage.sh - Gerenciar

```bash
./manage.sh <comando> [nome]

# Comandos:
start <nome>     # Inicia automação
stop <nome>      # Para automação
restart <nome>   # Reinicia automação
status <nome>    # Status da automação
list             # Lista todas automações
remove <nome>    # Remove automação (pede confirmação)

# Exemplos:
./manage.sh list
./manage.sh status chatbot-vendas
./manage.sh restart chatbot-vendas
./manage.sh remove scraper-antigo
```

---

## 📝 Criar Automação Personalizada

### Exemplo: Chatbot WhatsApp

```bash
# 1. Criar estrutura
./new.sh chatbot-whatsapp webhook-api

# 2. Editar código
cd production/deployed/chatbot-whatsapp

# Agora use Claude Code para desenvolver:
# "Cria um chatbot WhatsApp que responde com OpenAI"
```

**Claude Code vai:**
1. Modificar `app.py`
2. Atualizar `requirements.txt`
3. Configurar `.env`

```bash
# 3. Testar localmente
python3 app.py

# 4. Deploy
./deploy.sh chatbot-whatsapp 8000
```

**Pronto! Rodando 24/7 na VPS!**

---

## 🐳 Estrutura Docker

### Dockerfile Padrão

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Healthcheck
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

# Iniciar
CMD ["python", "app.py"]
```

### docker-compose.yml Padrão

```yaml
services:
  app:
    build: .
    container_name: ${AUTOMATION_NAME}
    restart: unless-stopped
    ports:
      - "${PORT}:${PORT}"
    environment:
      - PORT=${PORT}
      - TZ=America/Sao_Paulo
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${PORT}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 🔧 Customizar Automação

### Adicionar Banco de Dados

**docker-compose.yml:**
```yaml
services:
  app:
    # ... config existente
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: senha
      POSTGRES_DB: meudb
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### Adicionar Redis

```yaml
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
```

### Cronjob (Scheduled Task)

**app.py:**
```python
import schedule
import time

def job():
    print("Executando tarefa...")
    # Sua lógica aqui

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## 🚨 Troubleshooting

### Deploy falha

```bash
# Ver logs do deploy
./deploy.sh minha-automacao 2>&1 | tee deploy.log

# Verificar na VPS
ssh root@82.25.68.132
cd /root/automations/minha-automacao
docker compose logs
```

### Container não inicia

```bash
# Ver status
./manage.sh status minha-automacao

# Ver logs
./logs.sh minha-automacao

# Rebuild
ssh root@82.25.68.132
cd /root/automations/minha-automacao
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Porta em uso

```bash
# Verificar porta
ssh root@82.25.68.132 'netstat -tlnp | grep :8000'

# Usar porta diferente
./deploy.sh minha-automacao 8001
```

---

## 🎯 Casos de Uso

### 1. Chatbot WhatsApp 24/7

```bash
./new.sh chatbot-vendas webhook-api
# Desenvolve com Claude Code
./deploy.sh chatbot-vendas 8000
# Configura webhook no WhatsApp: http://82.25.68.132:8000/webhook
```

### 2. Scraper de Dados

```bash
./new.sh scraper-imoveis webhook-api
# Adiciona lógica de scraping
# Configura cronjob (schedule.every(1).hour.do(scrape))
./deploy.sh scraper-imoveis none
```

### 3. API REST

```bash
./new.sh api-produtos webhook-api
# Implementa endpoints REST
./deploy.sh api-produtos 8080
# Acesso: http://82.25.68.132:8080
```

---

## 📊 Monitoramento

### Ver logs em tempo real

```bash
./logs.sh chatbot-vendas
```

### Ver status de todas automações

```bash
./manage.sh list
```

**Output:**
```
[MANAGE] Automações na VPS:
  ✅ chatbot-vendas (rodando)
  ✅ scraper-imoveis (rodando)
  ⚪ notificador (parado)
```

---

## 🔐 Segurança

### Variáveis Sensíveis

**Nunca** comite `.env` no git!

**.env.example:**
```bash
AUTOMATION_NAME=minha-automacao
PORT=8000
API_KEY=sua-chave-aqui
DATABASE_URL=postgres://...
```

**Copie para `.env` e preencha:**
```bash
cp .env.example .env
# Edite .env com credenciais reais
```

### SSH Seguro

Chave SSH já configurada:
- `~/.ssh/id_rsa`
- `~/.ssh/config` com alias `vps-hostinger`

---

## 🚀 Próximos Passos

### 1. Criar mais templates

```bash
production/templates/
├── webhook-api/        ✅ Pronto
├── cronjob/           🚧 TODO
├── chatbot-whatsapp/  🚧 TODO
└── scraper/           🚧 TODO
```

### 2. CI/CD Automático

```bash
# GitHub Actions
git push → Testa → Deploy automático
```

### 3. Domínio Personalizado

```bash
# Nginx reverse proxy
chatbot.seudominio.com → http://82.25.68.132:8000
```

---

## 📞 Suporte

### Comandos úteis foram salvos

```bash
./deploy.sh --help
./manage.sh --help
./logs.sh --help
./new.sh --help
```

### SSH na VPS

```bash
ssh root@82.25.68.132
cd /root/automations
ls -la
```

---

## ✨ Exemplo Completo

**Do zero ao deploy em 5 minutos:**

```bash
# 1. Criar automação
./new.sh bot-telegram webhook-api

# 2. Desenvolver com Claude Code
cd production/deployed/bot-telegram
# Pede ao Claude: "Cria bot Telegram que responde com IA"

# 3. Configurar credenciais
echo "TELEGRAM_TOKEN=seu-token" >> .env

# 4. Testar local
python3 app.py

# 5. Deploy
./deploy.sh bot-telegram 8000

# 6. Ver logs
./logs.sh bot-telegram

# 7. Gerenciar
./manage.sh status bot-telegram
```

**Pronto! Bot rodando 24/7 na VPS!** 🎉

---

**Sistema criado em:** 2025-11-05
**VPS:** 82.25.68.132 (Hostinger)
**Mac:** Desenvolvimento local com Claude Code
**Stack:** Docker + Python + Flask

**Happy Deploying!** 🚀
