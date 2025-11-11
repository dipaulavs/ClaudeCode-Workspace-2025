# 🚀 Deploy via GitHub - Política Obrigatória

**Data:** 2025-11-06
**Status:** OBRIGATÓRIO para todos os deploys VPS

---

## 🎯 Regra Fundamental

**NUNCA** fazer deploy direto da máquina local para VPS.
**SEMPRE** usar GitHub como intermediário.

---

## ✅ Fluxo Correto

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Local      │ ──> │   GitHub     │ ──> │     VPS      │
│  Desenvolve  │ git │  Versionado  │ git │   Deploy     │
└──────────────┘     └──────────────┘     └──────────────┘
```

### **Passos:**

1. **Desenvolver localmente**
   ```bash
   cd SWARM/automations/meu-projeto
   # Editar código, testar
   ```

2. **Commitar no GitHub**
   ```bash
   git add .
   git commit -m "feat: nova funcionalidade"
   git push origin main
   ```

3. **Deploy na VPS**
   ```bash
   ssh root@82.25.68.132
   cd /opt/swarm/automations/meu-projeto
   git pull origin main
   docker stack deploy -c docker-compose.yml meu-projeto
   ```

---

## ❌ Fluxos PROIBIDOS

### **Proibido 1: Deploy direto local→VPS**
```bash
# ❌ NUNCA FAZER ISSO:
./deploy.sh meu-projeto
scp app.py root@82.25.68.132:/opt/swarm/
rsync -avz . root@82.25.68.132:/opt/swarm/
```

### **Proibido 2: Código não versionado**
```bash
# ❌ NUNCA FAZER ISSO:
# Editar código local e subir direto sem commit
```

### **Proibido 3: Build local e push da imagem**
```bash
# ❌ NUNCA FAZER ISSO:
docker build -t meu-projeto .
docker save meu-projeto | ssh root@82.25.68.132 docker load
```

---

## 🎯 Benefícios da Política GitHub-First

| Aspecto | Sem GitHub | Com GitHub ✅ |
|---------|------------|---------------|
| **Versionamento** | ❌ Nenhum | ✅ Histórico completo |
| **Backup** | ❌ Código na VPS apenas | ✅ GitHub + VPS |
| **Rollback** | ❌ Impossível | ✅ `git checkout` |
| **Colaboração** | ❌ Impossível | ✅ Pull requests |
| **Auditoria** | ❌ Nenhuma | ✅ Commits rastreados |
| **CI/CD** | ❌ Impossível | ✅ GitHub Actions |
| **Disaster Recovery** | ❌ Se VPS cair, perdeu | ✅ Clone do GitHub |

---

## 🛠️ Setup Inicial (1ª vez)

### **1. Criar estrutura local**
```bash
cd SWARM
./new.sh meu-projeto webhook-api meuapp
cd automations/meu-projeto
```

### **2. Inicializar Git**
```bash
git init
git add .
git commit -m "feat: estrutura inicial"
```

### **3. Criar repo no GitHub**
```bash
# Opção 1: Via GitHub CLI
gh repo create meu-projeto --private --source=. --remote=origin
git push -u origin main

# Opção 2: Manual
# 1. Criar repo no GitHub (web)
# 2. Adicionar remote
git remote add origin git@github.com:seu-usuario/meu-projeto.git
git push -u origin main
```

### **4. Setup na VPS (1ª vez)**
```bash
ssh root@82.25.68.132

# Criar diretório se não existir
mkdir -p /opt/swarm/automations
cd /opt/swarm/automations

# Clone do GitHub
git clone git@github.com:seu-usuario/meu-projeto.git
cd meu-projeto

# Deploy inicial
docker stack deploy -c docker-compose.yml meu-projeto
```

---

## 🔄 Workflow Diário

### **Desenvolvimento**
```bash
# Local: desenvolver
cd SWARM/automations/meu-projeto
vim app.py

# Testar localmente
python3 app.py

# Commit
git add .
git commit -m "feat: adicionar feature X"
git push origin main
```

### **Deploy**
```bash
# VPS: atualizar
ssh root@82.25.68.132
cd /opt/swarm/automations/meu-projeto
git pull origin main
docker stack deploy -c docker-compose.yml meu-projeto
```

---

## 🤖 Automação (Opcional)

### **GitHub Actions - Auto-deploy**

Criar `.github/workflows/deploy.yml`:

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: 82.25.68.132
          username: root
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/swarm/automations/meu-projeto
            git pull origin main
            docker stack deploy -c docker-compose.yml meu-projeto
```

**Setup:**
```bash
# Gerar chave SSH (se não tiver)
ssh-keygen -t ed25519 -C "github-actions"

# Adicionar chave pública na VPS
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@82.25.68.132

# Adicionar chave privada no GitHub Secrets
# Settings → Secrets → New secret
# Nome: SSH_PRIVATE_KEY
# Valor: conteúdo de ~/.ssh/id_ed25519
```

**Resultado:**
```
Push → GitHub → Action → SSH VPS → git pull → deploy
```

---

## 🔐 Segurança

### **Variáveis Sensíveis**

**NUNCA** commitar `.env`:

```bash
# .gitignore
.env
*.env
config/credentials.json
```

**Gerenciar secrets na VPS:**

```bash
# VPS: criar .env manualmente
ssh root@82.25.68.132
cd /opt/swarm/automations/meu-projeto
vim .env
# Adicionar credenciais

# Ou usar Docker Secrets
echo "sk-real-key" | docker secret create openai_key -
```

---

## 📊 Exemplo Completo: Chatbot WhatsApp

```bash
# 1. LOCAL: Criar estrutura
cd SWARM
./new.sh chatbot-whatsapp webhook-api whatsapp
cd automations/chatbot-whatsapp

# 2. Desenvolver
# Editar app.py com lógica do chatbot

# 3. Git setup
git init
git add .
git commit -m "feat: chatbot whatsapp inicial"
gh repo create chatbot-whatsapp --private --source=. --remote=origin
git push -u origin main

# 4. VPS: Clone e deploy
ssh root@82.25.68.132
cd /opt/swarm/automations
git clone git@github.com:seu-usuario/chatbot-whatsapp.git
cd chatbot-whatsapp
vim .env  # Adicionar credenciais
docker stack deploy -c docker-compose.yml chatbot-whatsapp

# 5. Acessar
# https://whatsapp.loop9.com.br

# 6. Atualizar depois
# LOCAL:
git add .
git commit -m "feat: adicionar comando /ajuda"
git push origin main

# VPS:
ssh root@82.25.68.132
cd /opt/swarm/automations/chatbot-whatsapp
git pull origin main
docker stack deploy -c docker-compose.yml chatbot-whatsapp
```

---

## 🚨 Troubleshooting

### **Erro: VPS não consegue pull**

```bash
# VPS: Verificar SSH keys
ssh root@82.25.68.132
ssh -T git@github.com

# Se falhar, gerar chave na VPS
ssh-keygen -t ed25519 -C "vps@loop9"
cat ~/.ssh/id_ed25519.pub
# Adicionar em: GitHub → Settings → SSH Keys
```

### **Erro: Conflitos de merge**

```bash
# VPS: se modificou código direto (NÃO FAZER!)
cd /opt/swarm/automations/meu-projeto
git stash  # Salva mudanças locais
git pull origin main
git stash pop  # Re-aplica (resolver conflitos)
```

---

## ✅ Checklist de Compliance

Antes de cada deploy, verificar:

- [ ] Código commitado no GitHub?
- [ ] Push feito para `origin main`?
- [ ] `.env` NÃO commitado?
- [ ] VPS faz `git pull` antes de deploy?
- [ ] Usando `docker stack deploy` (não scripts locais)?

---

## 📚 Referências

- **CLAUDE.md** - Regra #12 (Deploy Padrão)
- **SWARM/README.md** - Quick Start GitHub-First
- **docs/CONFIG.md** - Configurações VPS

---

**Política estabelecida:** 2025-11-06
**Aplicável a:** Todos os deploys em `82.25.68.132` (VPS loop9)
**Exceções:** Nenhuma
