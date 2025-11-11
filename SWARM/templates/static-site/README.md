# 🌐 Template: Site Estático

Deploy de sites estáticos (React, Vue, Next.js export, HTML/CSS/JS) com Nginx + Traefik.

## 🚀 Como Usar

### 1. Criar projeto local

```bash
# React
npx create-react-app meu-site
cd meu-site
npm run build
# Gera pasta: build/

# Next.js (export estático)
npx create-next-app meu-site
cd meu-site
# Adiciona no next.config.js: output: 'export'
npm run build
# Gera pasta: out/

# Vue
npm create vue@latest meu-site
cd meu-site
npm run build
# Gera pasta: dist/

# HTML puro
mkdir meu-site
cd meu-site
# Seus arquivos .html, .css, .js
```

### 2. Criar estrutura no SWARM

```bash
cd SWARM
./new.sh meu-site static-site site

# Estrutura criada:
# automations/meu-site/
# ├── docker-compose.yml
# ├── nginx.conf
# ├── .env
# └── dist/  ← Cole seus arquivos aqui
```

### 3. Copiar build para dist/

```bash
# React
cp -r ~/meu-projeto/build/* automations/meu-site/dist/

# Next.js
cp -r ~/meu-projeto/out/* automations/meu-site/dist/

# Vue
cp -r ~/meu-projeto/dist/* automations/meu-site/dist/

# HTML puro
cp -r ~/meu-projeto/* automations/meu-site/dist/
```

### 4. Deploy

```bash
# NÃO precisa de build Docker!
# Só envia arquivos:

cd automations/meu-site
scp -r dist/ root@82.25.68.132:/root/swarm-sites/meu-site/

# Deploy stack
cd ../..
./deploy.sh meu-site
```

**Acesso:** https://site.loop9.com.br

## 🔄 Atualização

```bash
# 1. Rebuild local
npm run build

# 2. Copia arquivos novos
cp -r ~/meu-projeto/build/* automations/meu-site/dist/

# 3. Re-deploy
./deploy.sh meu-site
```

## ⚡ Deploy Automático (GitHub Webhook)

Quer deploy automático no `git push`? Use N8N:

1. **Webhook do GitHub** → N8N
2. **N8N** → Build & deploy automático
3. **Pronto!** Sistema tipo Netlify

Fluxo N8N:
```
GitHub Push
  ↓
N8N Webhook
  ↓
SSH na VPS
  ↓
git pull
  ↓
npm run build
  ↓
cp build → dist
  ↓
Stack restart
  ↓
✅ Site atualizado!
```

## 🎯 Suporta

- ✅ React
- ✅ Vue
- ✅ Next.js (export)
- ✅ Angular
- ✅ HTML/CSS/JS puro
- ✅ Gatsby
- ✅ Svelte
- ✅ Qualquer SPA

## 📊 Performance

- **Gzip:** Ativado
- **Cache:** Headers configurados
- **SPA:** Fallback para index.html
- **Security:** Headers de segurança

## 🔧 Customizar nginx.conf

```nginx
# Exemplo: Adicionar redirect
location /old-page {
    return 301 https://site.loop9.com.br/new-page;
}

# Exemplo: Proxy para API
location /api {
    proxy_pass http://api-backend:3000;
}
```

Depois de editar:
```bash
./deploy.sh meu-site
```
