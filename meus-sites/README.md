# 🚀 Meus Sites - Deploy Automático VPS

Sistema para deployar sites na VPS com **1 comando** + **DNS automático via Cloudflare**.

---

## 📁 Estrutura

```
~/meus-sites/
├── deploy-site.sh           → Script de deploy (com DNS automático)
├── cloudflare-dns.sh        → Gerenciador de DNS via API Cloudflare
├── configs/                 → Configs dos sites (YAMLs)
│   ├── _template.yaml       → Template para copiar
│   ├── casanova.yaml        → Exemplo
│   └── testesite.yaml       → Exemplo subdomínio loop9
└── projetos/                → Seus projetos (opcional)
    └── testesite/           → Site de exemplo
```

---

## 🎉 NOVO: DNS Automático para loop9.com.br

**Subdomínios `*.loop9.com.br` são configurados automaticamente!**

Quando você faz deploy de um site com domínio terminando em `.loop9.com.br`, o script automaticamente:
- ✅ Cria o registro DNS na Cloudflare via API
- ✅ Adiciona registro www (se `www: true`)
- ✅ Aguarda propagação
- ✅ Faz o deploy completo

**Você não precisa fazer NADA manualmente!**

---

## 🎯 Como Usar

### **Opção A: Subdomínio loop9.com.br (100% Automático)**

```bash
# 1. Criar projeto
mkdir -p ~/meus-sites/projetos/meu-site
echo "<h1>Meu Site</h1>" > ~/meus-sites/projetos/meu-site/index.html

# 2. Criar config
cat > ~/meus-sites/configs/meu-site.yaml << EOF
dominio: meu-site.loop9.com.br
www: false
projeto: ~/meus-sites/projetos/meu-site
build: echo "Site estático"
pasta_build: ./
EOF

# 3. Deploy (DNS + Build + Deploy tudo automático!)
cd ~/meus-sites
./deploy-site.sh meu-site

# ✅ Pronto! Site no ar: https://meu-site.loop9.com.br
```

**Isso é tudo!** DNS, deploy, SSL - tudo automático! 🎉

---

### **Opção B: Domínio Externo (Configuração Manual de DNS)**

#### **1. Criar Config do Site**

```bash
cd ~/meus-sites/configs

# Copiar template
cp _template.yaml meu-site.yaml

# Editar
vim meu-site.yaml
```

**Preencher:**
```yaml
dominio: meusite.com.br
www: true
projeto: ~/projetos/meu-site
build: npm run build
pasta_build: build/
```

#### **2. Configurar DNS**

No painel do domínio (Hostinger/Registro.br):

```
Tipo: A
Nome: @
Valor: 82.25.68.132
TTL: 300

Tipo: A
Nome: www
Valor: 82.25.68.132
TTL: 300
```

Aguardar propagação (5-30 min).

#### **3. Deploy!**

```bash
cd ~/meus-sites

./deploy-site.sh meu-site

# Output:
# [DEPLOY] Lendo config...
# [DEPLOY] Executando build...
# [DEPLOY] Copiando para SWARM...
# [DEPLOY] Deployando stack...
# ✅ Deploy concluído!
#
# 🌐 Acesso: https://meusite.com.br
```

Aguardar 30-60s para SSL.

---

### **4. Atualizar Site**

```bash
# Fez alteração no código?
# Só rodar de novo:

./deploy-site.sh meu-site

# Build → Deploy → ✅ Atualizado!
```

---

## 📝 Exemplo Completo

```bash
# 1. Criar projeto React
npx create-react-app ~/projetos/portfolio
cd ~/projetos/portfolio
# ... desenvolver ...

# 2. Criar config
cd ~/meus-sites/configs
cat > portfolio.yaml << EOF
dominio: meuportfolio.com.br
www: true
projeto: ~/projetos/portfolio
build: npm run build
pasta_build: build/
EOF

# 3. Configurar DNS (meuportfolio.com.br → 82.25.68.132)

# 4. Deploy
cd ~/meus-sites
./deploy-site.sh portfolio

# ✅ https://meuportfolio.com.br
```

---

## 🔧 Frameworks Suportados

```yaml
# React
build: npm run build
pasta_build: build/

# Next.js (export estático)
build: npm run build
pasta_build: out/

# Vue
build: npm run build
pasta_build: dist/

# Angular
build: npm run build
pasta_build: dist/nome-projeto/

# HTML/CSS/JS puro
build: echo "Sem build"
pasta_build: ./
```

---

## 📊 Gerenciar Sites

```bash
# Listar sites deployados
ls configs/

# Ver logs
ssh root@82.25.68.132 'docker service logs meu-site_web -f'

# Status
ssh root@82.25.68.132 'docker stack ps meu-site'

# Remover
ssh root@82.25.68.132 'docker stack rm meu-site'
```

---

## 🎬 Workflow Diário

```
1. Desenvolve no projeto
   cd ~/projetos/meu-site
   # ... código ...

2. Deploy
   cd ~/meus-sites
   ./deploy-site.sh meu-site

3. ✅ Site atualizado!
```

---

## ✅ Checklist Novo Site

- [ ] Projeto React/Next/Vue criado
- [ ] Config YAML criada em `configs/`
- [ ] DNS apontado (dominio → 82.25.68.132)
- [ ] DNS propagado (testar: `nslookup dominio.com.br`)
- [ ] Deploy: `./deploy-site.sh nome`
- [ ] Aguardar SSL (30-60s)
- [ ] Testar: `https://dominio.com.br`

---

## 🆘 Troubleshooting

### DNS não resolve
```bash
nslookup meusite.com.br
# Deve mostrar: 82.25.68.132
# Se não: aguardar propagação ou verificar painel DNS
```

### Build falha
```bash
# Testar build manual:
cd ~/projetos/meu-site
npm run build
# Ver erro e corrigir
```

### SSL não gera
```bash
# Ver logs Traefik:
ssh root@82.25.68.132 'docker service logs traefik_traefik -f'
# Causa comum: DNS ainda não propagou
```

### Site não carrega
```bash
# Ver logs do site:
ssh root@82.25.68.132 'docker service logs meu-site_web -f'

# Verificar stack:
ssh root@82.25.68.132 'docker stack ps meu-site'
```

---

## 🎯 Múltiplos Sites

Você pode hospedar **quantos sites quiser**:

```
configs/
├── casanova.yaml         → casanova.com.br
├── portfolio.yaml        → portfolio.loop9.com.br (DNS automático!)
├── testesite.yaml        → testesite.loop9.com.br (DNS automático!)
├── cliente1.yaml         → cliente1.com.br
├── cliente2.yaml         → cliente2.com.br
└── loja.yaml             → minhaloja.com.br

Todos na mesma VPS, SSL automático! ✅
```

---

## 🌐 Gerenciar DNS via Cloudflare (Manual)

O script `cloudflare-dns.sh` permite gerenciar DNS manualmente se necessário:

### **Adicionar DNS**
```bash
./cloudflare-dns.sh add meu-site.loop9.com.br
```

### **Listar todos os DNS**
```bash
./cloudflare-dns.sh list loop9.com.br
```

### **Deletar DNS**
```bash
./cloudflare-dns.sh delete meu-site.loop9.com.br
```

### **Primeira vez (configurar credenciais)**

Se ainda não configurou, o script vai pedir:
- Email da Cloudflare
- API Token ou Global API Key

**Como obter:**
1. Acesse: https://dash.cloudflare.com/profile/api-tokens
2. Crie um "API Token" com permissão "Edit zone DNS"
3. Ou use a "Global API Key" (menos seguro)

As credenciais ficam salvas em `~/.cloudflare-credentials` (seguro, chmod 600)

---

## 📋 Exemplos Práticos

### **Exemplo 1: Site HTML Simples (loop9)**
```bash
# Criar site
mkdir -p ~/meus-sites/projetos/landing
cat > ~/meus-sites/projetos/landing/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Landing Page</title></head>
<body><h1>Minha Landing Page</h1></body>
</html>
EOF

# Config
cat > ~/meus-sites/configs/landing.yaml << EOF
dominio: landing.loop9.com.br
www: false
projeto: ~/meus-sites/projetos/landing
build: echo "HTML puro"
pasta_build: ./
EOF

# Deploy (tudo automático!)
cd ~/meus-sites && ./deploy-site.sh landing

# ✅ https://landing.loop9.com.br
```

### **Exemplo 2: Site React**
```bash
# Criar projeto React
npx create-react-app ~/projetos/meu-app
cd ~/projetos/meu-app
# ... desenvolver ...

# Config
cat > ~/meus-sites/configs/meu-app.yaml << EOF
dominio: app.loop9.com.br
www: false
projeto: ~/projetos/meu-app
build: npm run build
pasta_build: build/
EOF

# Deploy
cd ~/meus-sites && ./deploy-site.sh meu-app

# ✅ https://app.loop9.com.br
```

### **Exemplo 3: Múltiplos Ambientes**
```bash
# Produção
dominio: meusite.loop9.com.br

# Staging
dominio: staging.loop9.com.br

# Dev
dominio: dev.loop9.com.br

# Todos com DNS automático! 🚀
```

---

## ✅ Checklist Novo Site (loop9.com.br)

Para subdomínios `*.loop9.com.br`:
- [ ] Criar projeto ou usar existente
- [ ] Criar config YAML em `configs/`
- [ ] Deploy: `./deploy-site.sh nome`
- [ ] Aguardar 30-60s para SSL
- [ ] Testar: `https://seu-site.loop9.com.br`

**DNS é automático!** ✨

---

## ✅ Checklist Novo Site (Domínio Externo)

Para domínios externos:
- [ ] Projeto React/Next/Vue criado
- [ ] Config YAML criada em `configs/`
- [ ] DNS apontado (dominio → 82.25.68.132)
- [ ] DNS propagado (testar: `nslookup dominio.com.br`)
- [ ] Deploy: `./deploy-site.sh nome`
- [ ] Aguardar SSL (30-60s)
- [ ] Testar: `https://dominio.com.br`

---

**Sistema criado em:** 2025-01-05
**Atualizado em:** 2025-11-05 (DNS automático via Cloudflare API)
**VPS:** 82.25.68.132 (loop9.com.br)
**Stack:** Docker Swarm + Traefik + Nginx + Cloudflare DNS

**Happy Deploying!** 🚀
