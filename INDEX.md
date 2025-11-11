# 🖥️ Claude Code Workspace - Índice Principal

**Versão:** 1.0
**Última atualização:** 2025-11-11
**Localização Local:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace`
**Repositório GitHub:** https://github.com/dipaulavs/claude-workspace
**VPS Remoto:** `root@82.25.68.132:/root/claude-workspace`
**Status:** 🟢 Ativo e sincronizado

---

## 📊 Estatísticas

| Recurso | Quantidade | Status |
|---------|------------|--------|
| **Skills** | 38 | ✅ Produção |
| **Templates** | 71+ | ✅ Produção |
| **Scripts** | 60+ | ✅ Produção |
| **Apps & Sites** | 15 | ✅ Produção |
| **Automações SWARM** | 12 | ✅ Produção |
| **Docs** | 100+ | 📝 Em evolução |

---

## 📁 Estrutura do Workspace

```
ClaudeCode-Workspace/
├── 📂 .claude/skills/           → 38 Skills model-invoked (IA decide automaticamente)
├── 📂 APPS E SITES/             → Aplicações web deployadas (loop9.com.br)
├── 📂 SCRIPTS/                  → Scripts Python/Bash organizados por categoria
├── 📂 SWARM/                    → Automações production-ready (Docker Swarm)
├── 📂 docs/                     → Documentação técnica detalhada
├── 📂 templates/                → Templates reutilizáveis
├── 📂 config/                   → Configs e credenciais (não commitadas)
├── 📂 TOOLS/                    → Ferramentas low-level
└── 📄 CLAUDE.md                 → Configuração principal do Claude Code
```

---

## 🎯 Diretórios Principais

### 🧠 [.claude/skills/](.claude/skills/)
**Descrição:** Skills modulares que o Claude invoca automaticamente
**Total:** 38 skills
**Categorias:** Mentoria, IA & Prompts, Pesquisa, Design, Marketing, YouTube, Development, Multi-agente, Produtividade
**Index:** [.claude/skills/INDEX.md](.claude/skills/INDEX.md)

**Skills mais usadas:**
- `adaptive-mentor` - Mentor adaptativo (first-contact)
- `hormozi-leads` - Copy Hormozi para leads
- `upto-vps` - Deploy automático VPS
- `search-specialist` - Deep research especializado
- `estudar-video` - Transcrição e análise de vídeos

### 🌐 [APPS E SITES/](APPS%20E%20SITES/)
**Descrição:** Aplicações web organizadas e deployadas
**VPS:** 82.25.68.132 (Docker Swarm + Traefik)
**SSL:** Automático via Let's Encrypt
**Index:** [APPS E SITES/INDEX.md](APPS%20E%20SITES/INDEX.md)

**Em produção:**
- `obrigado-site` - https://obrigado.loop9.com.br
- `lfimoveis-dashboard` - https://lfimoveis.loop9.com.br
- E mais 13 apps ativos

### 🐍 [SCRIPTS/](SCRIPTS/)
**Descrição:** Scripts Python e Bash categorizados
**Total:** 60+ scripts
**Categorias:** Automation, Deployment, Data Processing, APIs, Utils

**Destaques:**
- `deployment/sync_workspace.sh` - Sincronização Git automática
- `automation/` - Automações diversas
- `claude-skills/` - Gerenciamento de skills

### 🐳 [SWARM/](SWARM/)
**Descrição:** Automações production-ready com Docker Swarm
**VPS:** 82.25.68.132
**Total:** 12 automações

**Serviços ativos:**
- Instagram Webhook
- Obsidian Remote CLI
- Evolution API
- Chatwoot
- N8N

### 📚 [docs/](docs/)
**Descrição:** Documentação técnica completa
**Total:** 100+ documentos

**Categorias:**
- `DOCS-API/` - Documentação de APIs externas
- `MAPA_ACOES.md` - 71+ templates de ações
- `REGRAS_DECISAO.md` - Fluxogramas de decisão
- `KNOWLEDGE_BASES.md` - Knowledge bases disponíveis
- `tools/INDEX.md` - 65+ ferramentas low-level

### 📋 [templates/](templates/)
**Descrição:** Templates reutilizáveis para projetos

**Tipos:**
- Docker Compose
- Dockerfile multi-stage
- Nginx configs
- Scripts deployment
- Webhooks

### ⚙️ [config/](config/)
**Descrição:** Configurações e credenciais (não commitadas)
**Status:** 🔒 Protegido via .gitignore

**Arquivos:**
- `google_service_account.json` - Google Cloud APIs
- Chaves API diversas (ver Obsidian Vault para inventário)

---

## 🚀 Como Usar Este Workspace

### 📤 Sincronizar Mudanças

```bash
# Sincronização rápida
bash SCRIPTS/deployment/sync_workspace.sh

# Com mensagem customizada
bash SCRIPTS/deployment/sync_workspace.sh "feat: adicionar nova skill"

# Alias (após configurar)
sync-workspace
```

### 🔍 Encontrar Recursos

```bash
# Buscar skill específica
cat .claude/skills/INDEX.md | grep "nome-da-skill"

# Listar todos os apps
ls -la "APPS E SITES/"

# Ver scripts disponíveis
tree SCRIPTS -L 2
```

### 📝 Criar Novo Projeto

```bash
# App/Site
cd "APPS E SITES"
# Usar skill upto-vps para scaffold

# Script
cd SCRIPTS/categoria
# Criar script + documentar no INDEX.md local

# Skill
# Pedir ao Claude: "Crie uma skill para [propósito]"
# Skill skill-creator ativa automaticamente
```

### 🌐 Deploy para VPS

```bash
# Usar skill upto-vps (automático)
# Ou manualmente:
cd "APPS E SITES/meu-projeto"
bash ../../.claude/skills/upto-vps/scripts/deploy.sh meu-projeto
```

---

## 🔐 Segurança e Backup

### Arquivos Excluídos do Git
Ver [.dockerignore](.dockerignore) e [.gitignore](.gitignore)

**Nunca commitados:**
- Credenciais (*.key, *.pem, .env)
- Chaves API
- Dados pessoais (Obsidian Vault)
- Arquivos temporários
- node_modules, venv, __pycache__

### Backups
- **Local:** Mac (tempo real)
- **GitHub:** Repositório privado (sincronizado)
- **VPS:** `/root/claude-workspace` (24/7 online)

---

## 🔗 Links Importantes

| Recurso | URL/Localização |
|---------|-----------------|
| **Docs Claude Code** | https://docs.claude.com/en/docs/claude-code |
| **VPS Dashboard** | https://vps.loop9.com.br |
| **GitHub Repo** | https://github.com/dipaulavs/claude-workspace |
| **Cloudflare DNS** | https://dash.cloudflare.com (zona: loop9.com.br) |
| **Obsidian Vault** | `/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Felipe/` |
| **Credenciais Vault** | `Obsidian Vault/🔐 Credenciais/🔑 Cofre de APIs.md` |

---

## 📞 Contato e Suporte

**Desenvolvedor:** Felipe de Paula
**Email:** felipidipaula@gmail.com
**GitHub:** [@dipaulavs](https://github.com/dipaulavs)
**VPS:** root@82.25.68.132

---

## 📜 Changelog Principal

### 2025-11-11 - v1.0 - Deploy Remoto
- ✅ Criado .dockerignore para segurança
- ✅ Criado script sync_workspace.sh
- ✅ Criado INDEX.md principal
- 🚧 Preparando para deploy na VPS (Fase 1 completa)

### 2025-11-10 - v0.9 - Organização
- Atualizado INDEX.md de skills (38 skills)
- Criado sistema de organização hierárquica
- Implementado CLAUDE.md v8.0 (skill-first)

---

**Última sincronização:** 2025-11-11 15:51
**Status do repositório:** 🟢 Clean (pronto para commit)
