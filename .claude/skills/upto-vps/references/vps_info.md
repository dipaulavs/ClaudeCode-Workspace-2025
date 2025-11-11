# VPS Information

## Connection Details

- **IP:** 82.25.68.132
- **Access:** `ssh root@82.25.68.132`
- **Domain:** *.loop9.com.br (wildcard DNS pointing to VPS)

## Infrastructure

### Traefik (Reverse Proxy)

- **Service:** traefik_traefik
- **HTTP Port:** 80 (redirects to HTTPS)
- **HTTPS Port:** 443
- **SSL:** Automatic Let's Encrypt certificates
- **Network:** loop9Net
- **Certresolver name:** letsencryptresolver

### Docker Swarm

- **Mode:** Swarm (not standalone Docker)
- **Network:** loop9Net (external, shared by all services)
- **Deploy method:** `docker stack deploy -c docker-compose.yml <stack-name>`
- **Management:**
  - List stacks: `docker stack ls`
  - List services: `docker service ls`
  - Logs: `docker service logs <service-name>`
  - Remove: `docker stack rm <stack-name>`

## Existing Services (as of 2025-01-10)

Major services running on the VPS:

- **n8n** (n8n.loop9.com.br) - Automation platform
- **chatwoot** - Customer support
- **evolution** - WhatsApp API
- **flowise** - LLM workflows
- **supabase** - Database/backend
- **portainer** - Docker management UI
- **typebot** - Chatbot builder
- **mautic** - Marketing automation
- **nextcloud** - File storage
- **And more...** (40+ services total)

## Deployment Workflow

### Standard Process

1. **Develop locally** in project directory
2. **Initialize Git repository** (if not exists)
   ```bash
   git init
   git remote add origin <github-repo>
   ```
3. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "feat: initial deployment"
   git push origin main
   ```
4. **Clone on VPS**
   ```bash
   ssh root@82.25.68.132
   cd /root
   git clone <github-repo> <project-name>
   ```
5. **Deploy with Docker Swarm**
   ```bash
   docker stack deploy -c docker-compose.yml <stack-name>
   ```
6. **Verify deployment**
   - Check service: `docker service ls | grep <stack-name>`
   - Check logs: `docker service logs <stack-name>_app`
   - Test SSL: `curl -Ik https://<subdomain>.loop9.com.br`

### Update Workflow

```bash
# Local
git add .
git commit -m "update: ..."
git push

# VPS
ssh root@82.25.68.132 "cd /root/<project> && git pull && docker service update --force <stack>_app"
```

Or full recreation:
```bash
ssh root@82.25.68.132 "cd /root/<project> && git pull && docker stack rm <stack> && sleep 5 && docker stack deploy -c docker-compose.yml <stack>"
```

## Port Allocation

**Avoid these ports** (already in use):
- 5432 (PostgreSQL)
- 6333-6334, 6343-6344, 6353-6354, 6363-6364, 6373-6374 (Qdrant cluster)

**Safe practice:** Let Traefik handle external access. Services should only expose ports internally to loop9Net network.

## Naming Conventions

- **Stack name:** Use kebab-case (e.g., `lf-dashboard`, `my-api`)
- **Service name in compose:** Usually `app` for single-service stacks
- **Router name in Traefik labels:** Match subdomain without `.loop9.com.br` (e.g., `lfimoveis` for lfimoveis.loop9.com.br)
- **Subdomain:** Short, descriptive, kebab-case

## Troubleshooting

### Service won't start
```bash
docker service ps <service-name> --no-trunc
docker service logs <service-name>
```

### SSL shows "Not Secure"
1. Check labels are under `deploy.labels` (not top level)
2. Verify certresolver is `letsencryptresolver`
3. Full recreation: `docker stack rm <name> && sleep 10 && docker stack deploy ...`
4. Wait 30-60 seconds for Let's Encrypt

### Port conflicts
```bash
# Check what's using a port
docker service ls
docker ps
netstat -tuln | grep <port>
```

### Can't connect to service
1. Check service is running: `docker service ls`
2. Check Traefik labels: `docker service inspect <service> --format '{{json .Spec.Labels}}'`
3. Check logs: `docker service logs <service>`
4. Test from VPS: `curl -I http://localhost:<port>`
