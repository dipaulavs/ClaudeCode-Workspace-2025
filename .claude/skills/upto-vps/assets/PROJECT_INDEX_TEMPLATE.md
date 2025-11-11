# {{PROJECT_NAME}}

**Criado em:** {{DATE}}
**Última atualização:** {{DATE}}

---

## 📋 Informações Básicas

- **Nome:** {{PROJECT_NAME}}
- **Tipo:** {{TYPE}} (static/flask/node/api/dashboard)
- **URL:** https://{{SUBDOMAIN}}.loop9.com.br
- **Repositório:** https://github.com/dipaulavs/{{REPO_NAME}}
- **Status:** {{STATUS}} (dev/staging/production/archived)

---

## 🛠️ Stack Técnica

- **Framework/Runtime:** {{TECH}}
- **Servidor:** {{SERVER}} (Nginx/Gunicorn/Node/etc)
- **Porta interna:** {{PORT}}
- **Docker:** ✅ Swarm + Traefik
- **SSL:** ✅ Let's Encrypt (automático)

---

## 📦 Deploy

### Comandos de Deploy

```bash
# Deploy inicial
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS\ E\ SITES/{{PROJECT_NAME}}
git add . && git commit -m "feat: ..." && git push

# Atualizar no VPS
ssh root@82.25.68.132 "cd /root/{{PROJECT_NAME}} && git pull && docker service update --force {{STACK_NAME}}_app"

# Recriar stack (se necessário)
ssh root@82.25.68.132 "cd /root/{{PROJECT_NAME}} && git pull && docker stack rm {{STACK_NAME}} && sleep 10 && docker stack deploy -c docker-compose.yml {{STACK_NAME}}"
```

### Validação

```bash
# Verificar serviço
ssh root@82.25.68.132 "docker service ls | grep {{STACK_NAME}}"

# Ver logs
ssh root@82.25.68.132 "docker service logs {{STACK_NAME}}_app --tail 50"

# Testar SSL
echo | openssl s_client -servername {{SUBDOMAIN}}.loop9.com.br -connect {{SUBDOMAIN}}.loop9.com.br:443 2>/dev/null | openssl x509 -noout -issuer -subject

# Testar endpoint
curl -I https://{{SUBDOMAIN}}.loop9.com.br
```

---

## 📝 Log de Deploys

### {{DATE}} - Deploy Inicial
- ✅ Projeto criado
- ✅ CNAME configurado: {{SUBDOMAIN}}.loop9.com.br
- ✅ Docker Compose configurado
- ✅ GitHub repo criado
- ✅ Deploy no VPS realizado
- ✅ SSL provisionado
- **Status:** Production

---

## 🎯 Próximos Passos

- [ ] Item pendente 1
- [ ] Item pendente 2
- [ ] Item pendente 3

---

## 📚 Notas

(Adicionar notas importantes sobre o projeto aqui)

---

**Última modificação:** {{DATE}}
