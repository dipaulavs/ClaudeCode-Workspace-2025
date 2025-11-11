---
name: upto-vps
description: Deploy any application or website to VPS (82.25.68.132) with automatic SSL certificates via Traefik and Docker Swarm. Auto-invokes when user requests to deploy, upload, or put online any web application, API, dashboard, or site. Handles GitHub setup, docker-compose configuration with correct Traefik labels, SSL validation, and ensures no conflicts with existing services.
---

# Upto VPS

## Overview

Deploy applications to production VPS with automatic SSL certificates and zero downtime. This skill automates the entire deployment workflow: GitHub repository setup, Docker Swarm deployment with Traefik reverse proxy, Let's Encrypt SSL certificate provisioning, and validation. Ensures deployments don't conflict with 40+ existing services running on the VPS.

## When to Use This Skill

Auto-invoke when user requests:
- "Deploy this to the VPS"
- "Put this site online"
- "Upload this app to production"
- "I need SSL for this"
- "Make this accessible at <subdomain>.loop9.com.br"
- "Set up production deployment"

## Core Workflow

### Step 1: Create Project Structure

**CRITICAL:** All apps and sites MUST be created in organized structure.

**Base directory:**
```
/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/
```

**Use scaffold script:**
```bash
bash .claude/skills/upto-vps/scripts/scaffold_project.sh <project-name> <type>
```

**Manual creation (if script unavailable):**
```bash
cd "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES"
mkdir -p <project-name>
cd <project-name>

# Copy INDEX template
cp ../../.claude/skills/upto-vps/assets/PROJECT_INDEX_TEMPLATE.md INDEX.md

# Create CHANGELOG
echo "# Changelog - <project-name>\n\n## 2025-11-10 - Initial Release\n- Project created" > CHANGELOG.md
```

**After project creation:**
1. Update `APPS E SITES/INDEX.md` with new project entry
2. Fill project-specific `INDEX.md` with details
3. Ensure naming convention: kebab-case

### Step 2: Prepare Application

1. **Identify application type** (Flask/Node/Static/etc.)
2. **Detect port** application runs on
3. **Check for existing docker-compose.yml**
   - If exists: Validate Traefik labels configuration
   - If missing: Create from template

### Step 3: Configure Docker Compose

Read `references/traefik_labels.md` for correct configuration, then apply:

**Critical requirements:**
- Labels must be under `deploy.labels` (not service top-level)
- Use `letsencryptresolver` as certresolver name
- Include explicit service reference: `.service=<service-name>`
- Never add `tls=true` (causes default certificate)
- Network must be `loop9Net` (external)

**Template variables to replace:**
- `{{SERVICE_NAME}}` - Router/service identifier (e.g., "lfimoveis")
- `{{SUBDOMAIN}}` - Domain prefix (e.g., "lfimoveis" for lfimoveis.loop9.com.br)
- `{{PORT}}` - Application internal port
- `{{IMAGE}}` - Docker image name
- `{{COMMAND}}` - Container startup command
- `{{ENVIRONMENT}}` - Environment variables

Use `assets/docker-compose.template.yml` as base.

### Step 4: Create DNS CNAME Record

**ALWAYS create CNAME before deployment** to ensure SSL provisioning works correctly.

```bash
bash .claude/skills/upto-vps/scripts/create_cloudflare_cname.sh <subdomain>
```

This script:
- Creates CNAME record: `<subdomain>.loop9.com.br` → `vps.loop9.com.br`
- Automatically detects if record already exists
- Waits for DNS propagation (5 seconds)
- Uses Cloudflare API with pre-configured credentials

**Example:**
```bash
bash .claude/skills/upto-vps/scripts/create_cloudflare_cname.sh obrigado
# Creates: obrigado.loop9.com.br → vps.loop9.com.br
```

**Manual creation (if script unavailable):**
```bash
curl -X POST 'https://api.cloudflare.com/client/v4/zones/e28ff35f0f4e5ba0da93688f8352dd9f/dns_records' \
-H 'X-Auth-Email: felipidipaula@gmail.com' \
-H 'X-Auth-Key: 7e720179db9ea1041b9a030a531250750ce17' \
-H 'Content-Type: application/json' \
--data '{"type":"CNAME","name":"<subdomain>","content":"vps.loop9.com.br","ttl":1,"proxied":false}'
```

### Step 5: GitHub Setup

```bash
# Initialize if needed
git init
git remote add origin https://github.com/dipaulavs/<repo-name>.git

# Commit current state
git add .
git commit -m "feat: initial deployment setup"
git push origin main
```

If repository doesn't exist, create it first:
```bash
gh repo create <repo-name> --public --source=. --remote=origin --push
```

### Step 6: VPS Deployment

**Initial deployment:**
```bash
ssh root@82.25.68.132 "cd /root && git clone https://github.com/dipaulavs/<repo-name>.git <project-name>"
ssh root@82.25.68.132 "cd /root/<project-name> && docker stack deploy -c docker-compose.yml <stack-name>"
```

**Update existing deployment:**
```bash
# Method 1: Force update (preserves state)
ssh root@82.25.68.132 "cd /root/<project> && git pull && docker service update --force <stack>_app"

# Method 2: Full recreation (if SSL issues)
ssh root@82.25.68.132 "cd /root/<project> && git pull && docker stack rm <stack> && sleep 10 && docker stack deploy -c docker-compose.yml <stack>"
```

### Step 7: Validation & Documentation

**Validate deployment:**

**Check service status:**
```bash
ssh root@82.25.68.132 "docker service ls | grep <stack-name>"
ssh root@82.25.68.132 "docker service logs <stack-name>_app --tail 50"
```

**Validate SSL certificate:**
```bash
bash scripts/validate_ssl.sh <subdomain>.loop9.com.br
```

Expected output:
```
issuer=C=US, O=Let's Encrypt, CN=R12
subject=CN=<subdomain>.loop9.com.br
```

If shows "TRAEFIK DEFAULT CERT", SSL failed. Perform full stack recreation (Step 4, Method 2).

**Test endpoints:**
```bash
# HTTP should redirect to HTTPS
curl -I http://<subdomain>.loop9.com.br

# HTTPS should return 200 OK
curl -I https://<subdomain>.loop9.com.br
```

### Step 8: Create Deploy Alias

**CRITICAL:** Always create a deploy alias for easy updates.

```bash
# Add alias to .zshrc
echo '
# <Project Name> - Deploy rápido
alias deploy-<project-slug>="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/<project-name>\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/<vps-folder> && git pull && docker service update --force <stack-name>_app\""' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

**Example:**
```bash
# For project lfimoveis-dashboard:
alias deploy-lf="cd \"/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/lfimoveis-dashboard\" && git add . && git commit -m \"update\" && git push origin main && ssh root@82.25.68.132 \"cd /root/lf-dashboard && git pull && docker service update --force lfimoveis_app\""
```

**Variables to replace:**
- `<project-slug>` - Short alias name (e.g., "lf", "api", "blog")
- `<project-name>` - Local folder name
- `<vps-folder>` - Folder name on VPS (usually same as repo name)
- `<stack-name>` - Docker stack name

**After alias creation:**
- Test it: `deploy-<project-slug>`
- Document it in project INDEX.md
- User can now update with single command

### Step 9: Update Documentation

1. **Update master INDEX:**
```bash
# Edit APPS E SITES/INDEX.md
# Add project to "Ativos (em produção)" section
# Update statistics
```

2. **Update project INDEX:**
```bash
# Edit <project-name>/INDEX.md
# Fill all {{PLACEHOLDERS}} with real values
# Update status to "production"
# Add deploy log entry with timestamp
# Add deploy alias command
```

3. **Update CHANGELOG:**
```bash
# Edit <project-name>/CHANGELOG.md
# Add deploy entry with date and changes
```

## Troubleshooting

### SSL Shows "Not Secure" in Browser

**Cause:** Browser cached old certificate

**Solutions:**
1. Clear SSL state: `chrome://net-internals/#hsts` → Delete domain
2. Clear browser cache (last hour)
3. Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
4. Test in incognito/private window
5. Wait 2-3 minutes for full propagation

### Certificate Shows "TRAEFIK DEFAULT CERT"

**Cause:** Traefik labels misconfigured

**Fix:**
1. Verify labels are under `deploy.labels` (not top level)
2. Check certresolver is `letsencryptresolver` (not `letsencrypt`)
3. Remove `tls=true` if present
4. Verify service reference: `.service=<service-name>`
5. Full recreation required:
```bash
ssh root@82.25.68.132 "docker stack rm <stack> && sleep 10 && docker stack deploy -c docker-compose.yml <stack>"
```

### Port Conflict

**Check existing services:**
```bash
ssh root@82.25.68.132 "docker service ls"
```

Read `references/vps_info.md` for list of used ports. Use different internal port if needed.

### Service Won't Start

**Check logs:**
```bash
ssh root@82.25.68.132 "docker service ps <stack>_app --no-trunc"
ssh root@82.25.68.132 "docker service logs <stack>_app"
```

Common issues:
- Missing dependencies in requirements.txt/package.json
- Wrong working directory
- Port already bound
- Environment variables not set

## Organization & Naming Conventions

### Directory Structure

**MANDATORY:** All projects in `APPS E SITES/`

```
APPS E SITES/
├── INDEX.md (master registry)
└── <project-name>/
    ├── INDEX.md (project documentation)
    ├── CHANGELOG.md (version history)
    ├── docker-compose.yml
    ├── Dockerfile (if needed)
    └── source code
```

### Naming Conventions

- **Project folder:** kebab-case (e.g., `obrigado-site`, `lf-dashboard`, `api-webhook`)
- **Stack name:** Same as folder (e.g., `obrigado-site`)
- **Subdomain:** Same as folder (e.g., `obrigado-site.loop9.com.br`)
- **Service name:** Usually `app` for single-service stacks
- **Router name:** Match subdomain without domain suffix

### Documentation Requirements

**Every project MUST have:**
1. `INDEX.md` - Current status, tech stack, deploy commands, logs
2. `CHANGELOG.md` - Version history and updates
3. Entry in master `APPS E SITES/INDEX.md`

**Master INDEX MUST contain:**
- List of all active projects
- List of projects in development
- List of archived projects
- Statistics (total, active, dev, archived)
- Quick access links to each project's INDEX

## Reference Files

- **references/traefik_labels.md** - Complete Traefik labels configuration with working examples
- **references/vps_info.md** - VPS details, existing services, troubleshooting guide
- **assets/docker-compose.template.yml** - Base template with correct structure

## Quick Reference Commands

```bash
# Create DNS CNAME
bash .claude/skills/upto-vps/scripts/create_cloudflare_cname.sh <subdomain>

# List all services on VPS
ssh root@82.25.68.132 "docker service ls"

# Check service logs
ssh root@82.25.68.132 "docker service logs <service-name> --tail 50"

# Inspect service labels
ssh root@82.25.68.132 "docker service inspect <service> --format '{{json .Spec.Labels}}' | jq ."

# Remove stack
ssh root@82.25.68.132 "docker stack rm <stack-name>"

# Validate SSL
echo | openssl s_client -servername <subdomain>.loop9.com.br -connect <subdomain>.loop9.com.br:443 2>/dev/null | openssl x509 -noout -issuer -subject

# Deploy updates (after alias is created)
deploy-<project-slug>

# Manual update (without alias)
cd "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES/<project-name>"
git add . && git commit -m "update" && git push origin main
ssh root@82.25.68.132 "cd /root/<vps-folder> && git pull && docker service update --force <stack-name>_app"
```

## Auto-Correction System

When deployment fails, use auto-correction to prevent recurrence:

```bash
# Fix SKILL.md
python3 scripts/update_skill.py <old_text> <new_text>

# Log the fix
python3 scripts/log_learning.py <error> <fix> <line>
```

All corrections are tracked in `LEARNINGS.md`.
