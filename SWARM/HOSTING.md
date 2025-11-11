# 🌐 Self-Hosting vs Netlify

Guia completo para hospedar sites na sua própria VPS.

---

## 🎯 Comparação

| Feature | Netlify | Self-Hosting (VPS) |
|---------|---------|-------------------|
| **Custo** | Grátis até X builds | $0 (VPS já pago) |
| **SSL** | Automático | Automático (Traefik) |
| **Domínio Custom** | Sim | Sim (loop9.com.br) |
| **Build Automático** | Sim | N8N + GitHub webhook |
| **CDN Global** | Sim ⭐ | Não (single server) |
| **Limites** | 100GB bandwidth/mês | Ilimitado (VPS) |
| **Deploy** | `git push` | `git push` (com N8N) |
| **Performance BR** | Boa | Excelente (servidor BR) |
| **Controle** | Limitado | Total |
| **Integração** | APIs externas | Direto (N8N, APIs) |

---

## ✅ Quando Self-Hosting VALE A PENA

```
✅ Site para público brasileiro (99% BR)
✅ Integração com N8N/Evolution/APIs internas
✅ Tráfego alto (economiza bandwidth Netlify)
✅ Quer controle total
✅ Quer aprender infraestrutura
✅ Já tem VPS paga
```

## ❌ Quando Netlify É MELHOR

```
❌ Site global (USA, Europa, Ásia)
❌ Precisa de CDN edge (milissegundos importam)
❌ Não quer gerenciar servidor
❌ Precisa de Netlify Functions
❌ Time colaborativo (previews de PR)
```

---

## 🚀 Opções de Implementação

### **Opção 1: Coolify (Recomendado) ⭐**

**O que é:** Netlify/Vercel open source self-hosted

```bash
cd SWARM
./setup-coolify.sh

# Instala interface web completa:
# - Git integration
# - Build automático
# - Deploy com git push
# - Rollback
# - Logs de build
```

**Acesso:** http://82.25.68.132:8000

**Pros:**
- ✅ Interface bonita
- ✅ Git push = deploy
- ✅ Suporta: Static, Next.js, Node, PHP, Python
- ✅ Zero config

**Cons:**
- ⚠️ Mais complexo (banco de dados, workers)
- ⚠️ Usa mais recursos

---

### **Opção 2: Sistema Próprio (SWARM + Nginx)**

**O que é:** Template simples para sites estáticos

```bash
cd SWARM

# 1. Criar site
./new.sh meu-site static-site site

# 2. Build local
cd ~/meu-projeto
npm run build

# 3. Copiar arquivos
cp -r build/* ~/Desktop/ClaudeCode-Workspace/SWARM/automations/meu-site/dist/

# 4. Deploy
cd ~/Desktop/ClaudeCode-Workspace/SWARM
./deploy-static.sh meu-site
```

**Acesso:** https://site.loop9.com.br

**Pros:**
- ✅ Simples
- ✅ Leve (só Nginx)
- ✅ Usa Traefik existente
- ✅ Controle total

**Cons:**
- ⚠️ Deploy manual (ou via N8N)
- ⚠️ Sem interface web

---

## 🎬 Exemplo Completo: React App

### **Passo a Passo:**

**1. Criar React App local:**
```bash
npx create-react-app meu-portfolio
cd meu-portfolio

# Desenvolver...
# ...

# Build
npm run build
# Gera: build/
```

**2. Preparar deploy:**
```bash
cd ~/Desktop/ClaudeCode-Workspace/SWARM

# Criar estrutura
./new.sh portfolio static-site portfolio

# Copiar build
cp -r ~/meu-portfolio/build/* automations/portfolio/dist/
```

**3. Deploy:**
```bash
./deploy-static.sh portfolio

# Output:
# ✅ Deploy concluído!
# 🌐 Acesso: https://portfolio.loop9.com.br
```

**Pronto! Site no ar com SSL!** 🎉

---

## 🔄 Deploy Automático (Git Push)

**Usar N8N para automatizar:**

### **Fluxo:**

```
1. git push → GitHub
2. GitHub webhook → N8N
3. N8N:
   - SSH na VPS
   - git pull
   - npm install
   - npm run build
   - cp build → dist
   - ./deploy-static.sh
4. ✅ Site atualizado!
```

### **Workflow N8N:**

```json
{
  "nodes": [
    {
      "name": "GitHub Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "github-deploy"
      }
    },
    {
      "name": "SSH Build",
      "type": "n8n-nodes-base.ssh",
      "parameters": {
        "command": "cd /root/sites/portfolio && git pull && npm run build && cp -r build/* dist/"
      }
    },
    {
      "name": "Deploy",
      "type": "n8n-nodes-base.ssh",
      "parameters": {
        "command": "cd /root/swarm-sites/portfolio && docker stack deploy -c docker-compose.yml portfolio"
      }
    }
  ]
}
```

**Webhook URL:** https://n8n.loop9.com.br/webhook/github-deploy

**No GitHub:**
- Settings → Webhooks
- Add webhook
- Payload URL: N8N webhook
- Events: Push

**Agora:** `git push` = deploy automático! 🚀

---

## 💰 Economia

### **Netlify Pricing:**

```
Free: 100GB bandwidth/mês
Pro: $19/mês - 1TB bandwidth

Se ultrapassar:
$0.55 por 100GB extra
```

### **Self-Hosting:**

```
VPS: Já paga
Bandwidth: Ilimitado (VPS)
Builds: Ilimitados

Custo adicional: $0
```

**Exemplo:**
- Site com 500GB tráfego/mês
- Netlify: $19/mês + overage
- Self-hosting: $0 (VPS já paga)

**Economia:** ~$228/ano

---

## 📊 Performance

### **Teste de Velocidade (Brasil):**

```
Netlify (CDN global):
Brasil → São Paulo Edge → 50-80ms
USA → Dallas Edge → 20ms
Europa → Frankfurt Edge → 30ms

Self-Hosting (VPS Brasil):
Brasil → São Paulo VPS → 20-40ms ⭐
USA → São Paulo VPS → 150ms
Europa → São Paulo VPS → 200ms
```

**Para público brasileiro:** Self-hosting é MAIS RÁPIDO! 🏃

---

## 🔧 Manutenção

### **Netlify:**
```
✅ Zero manutenção
✅ Updates automáticos
✅ Suporte oficial
```

### **Self-Hosting:**
```
⚠️ Você gerencia updates
⚠️ Você é o suporte
✅ Controle total
✅ Aprendizado
```

---

## 🎯 Recomendação Final

### **Use Netlify se:**
- Site global (múltiplos países)
- Não quer gerenciar servidor
- Precisa de edge functions
- Time grande colaborando

### **Use Self-Hosting se:**
- Site para Brasil
- Já tem VPS
- Quer economizar
- Integração com serviços locais (N8N, APIs)
- Quer aprender

---

## 🚀 Começar Agora

### **Opção Fácil (Coolify):**
```bash
cd SWARM
./setup-coolify.sh
# Acesse: http://82.25.68.132:8000
# Configure e deploy!
```

### **Opção Simples (SWARM):**
```bash
cd SWARM

# 1. Criar
./new.sh meu-site static-site site

# 2. Build local
cd ~/meu-projeto && npm run build

# 3. Copiar
cp -r build/* ~/Desktop/ClaudeCode-Workspace/SWARM/automations/meu-site/dist/

# 4. Deploy
cd ~/Desktop/ClaudeCode-Workspace/SWARM
./deploy-static.sh meu-site
```

---

## 🆘 Troubleshooting

### **Build falha:**
```bash
# Verifique node version
node --version
npm --version

# Limpe cache
rm -rf node_modules package-lock.json
npm install
```

### **SSL não gera:**
```bash
# Aguarde 2-3 minutos
# Verifique logs Traefik
ssh root@82.25.68.132
docker service logs traefik_traefik -f
```

### **Site não carrega:**
```bash
# Ver logs
./logs.sh meu-site

# Verificar stack
./manage.sh status meu-site
```

---

## 📚 Recursos

- **Coolify:** https://coolify.io
- **Traefik Docs:** https://doc.traefik.io
- **Docker Swarm:** https://docs.docker.com/engine/swarm/

---

**Sistema criado em:** 2025-11-05
**Para:** Sites/apps estáticos na VPS loop9.com.br

**Happy Self-Hosting!** 🚀
