# Examples - upto-vps Skill

## Example 1: Deploy L&F Imóveis Dashboard

### Initial Setup

**Project Details:**
- Name: lfimoveis-dashboard
- Type: Flask app
- Port: 5000
- Subdomain: lfimoveis.loop9.com.br
- GitHub: dipaulavs/lf-dashboard
- VPS folder: /root/lf-dashboard
- Stack: lfimoveis

### Step-by-Step Execution

**1. Project organized:**
```bash
APPS E SITES/lfimoveis-dashboard/
├── app.py
├── docker-compose.yml
├── requirements.txt
└── static/
```

**2. Docker Compose configured:**
```yaml
services:
  app:
    image: python:3.11-slim
    deploy:
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.lfimoveis.rule=Host(`lfimoveis.loop9.com.br`)"
        - "traefik.http.routers.lfimoveis.entrypoints=websecure"
        - "traefik.http.routers.lfimoveis.tls.certresolver=letsencryptresolver"
        - "traefik.http.routers.lfimoveis.service=lfimoveis"
        - "traefik.http.services.lfimoveis.loadbalancer.server.port=5000"
```

**3. CNAME already existed (skipped)**

**4. GitHub push:**
```bash
cd "APPS E SITES/lfimoveis-dashboard"
git add . && git commit -m "feat: initial deploy" && git push origin main
```

**5. VPS deploy:**
```bash
ssh root@82.25.68.132 "cd /root && git clone https://github.com/dipaulavs/lf-dashboard.git"
ssh root@82.25.68.132 "cd /root/lf-dashboard && docker stack deploy -c docker-compose.yml lfimoveis"
```

**6. Validation:**
```bash
# Service running ✅
curl -I https://lfimoveis.loop9.com.br
# HTTP/2 302 (redirecting to login)

# SSL valid ✅
echo | openssl s_client -servername lfimoveis.loop9.com.br -connect lfimoveis.loop9.com.br:443 2>/dev/null | openssl x509 -noout -issuer -subject
# issuer=C=US, O=Let's Encrypt, CN=R12
# subject=CN=lfimoveis.loop9.com.br
```

**7. Deploy alias created:**
```bash
echo '
# L&F Imóveis Dashboard - Deploy rápido
alias deploy-lf="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/lfimoveis-dashboard\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/lf-dashboard && git pull && docker service update --force lfimoveis_app\""' >> ~/.zshrc

source ~/.zshrc
```

**8. Future updates (one command):**
```bash
deploy-lf
```

### Results

- **URL:** https://lfimoveis.loop9.com.br ✅
- **SSL:** Valid Let's Encrypt certificate ✅
- **Deploy time:** ~2 minutes (initial)
- **Update time:** ~30 seconds (with alias)
- **Alias:** `deploy-lf` ✅

---

## Example 2: Deploy Static Site

### Scenario
Deploy a static HTML/CSS/JS site for a landing page.

**Project Details:**
- Name: obrigado-site
- Type: Static HTML
- Port: 80 (nginx)
- Subdomain: obrigado.loop9.com.br
- Alias: deploy-obrigado

### Commands

**Create alias:**
```bash
echo '
# Obrigado Site - Deploy rápido
alias deploy-obrigado="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/obrigado-site\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/obrigado-site && git pull && docker service update --force obrigado_app\""' >> ~/.zshrc

source ~/.zshrc
```

**Update site:**
```bash
# Edit index.html
vim APPS\ E\ SITES/obrigado-site/index.html

# Deploy
deploy-obrigado
```

---

## Example 3: Deploy API/Webhook

### Scenario
Deploy a FastAPI webhook receiver.

**Project Details:**
- Name: webhook-receiver
- Type: FastAPI
- Port: 8000
- Subdomain: webhook.loop9.com.br
- Alias: deploy-webhook

### Alias Template

```bash
echo '
# Webhook Receiver - Deploy rápido
alias deploy-webhook="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/webhook-receiver\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/webhook-receiver && git pull && docker service update --force webhook_app\""' >> ~/.zshrc

source ~/.zshrc
```

---

## Common Patterns

### Pattern 1: Simple Name

```bash
# Project: blog
alias deploy-blog="cd \"/Users/.../blog\" && ... && docker service update --force blog_app\""
```

### Pattern 2: Abbreviated Name

```bash
# Project: analytics-dashboard
alias deploy-analytics="cd \"/Users/.../analytics-dashboard\" && ... && docker service update --force analytics_app\""
```

### Pattern 3: Client-Specific

```bash
# Project: cliente-joao-site
alias deploy-joao="cd \"/Users/.../cliente-joao-site\" && ... && docker service update --force joao_app\""
```

---

## Troubleshooting Alias

### Alias not found after creation

```bash
# Verify alias was added
tail -3 ~/.zshrc

# Reload shell
source ~/.zshrc

# Test alias
deploy-lf
```

### Permission denied on SSH

```bash
# Test SSH connection
ssh root@82.25.68.132 "echo 'Connection OK'"

# If fails, check SSH keys
ssh-add -l
```

### Docker service not found

```bash
# List services on VPS
ssh root@82.25.68.132 "docker service ls"

# Check correct service name
ssh root@82.25.68.132 "docker service ls | grep <project>"
```

---

## Best Practices

1. **Short alias names:** Use 2-5 characters for quick typing
2. **Consistent naming:** Match alias to project purpose (lf = L&F Imóveis)
3. **Test immediately:** Run alias right after creation to verify
4. **Document in INDEX:** Add alias command to project INDEX.md
5. **Use commit messages:** For important updates, don't use "update" - commit manually first

---

## Quick Copy Templates

### Flask/Python App
```bash
alias deploy-<NAME>="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/<PROJECT>\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/<FOLDER> && git pull && docker service update --force <STACK>_app\""
```

### Node/Express App
```bash
alias deploy-<NAME>="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/<PROJECT>\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/<FOLDER> && git pull && docker service update --force <STACK>_app\""
```

### Static Site (same as above - service name matters, not app type)
```bash
alias deploy-<NAME>="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/<PROJECT>\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/<FOLDER> && git pull && docker service update --force <STACK>_app\""
```
