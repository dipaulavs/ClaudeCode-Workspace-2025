# Learnings - Upto VPS Skill

## 2025-11-10: DNS CNAME Must Be Created Before Deployment

**Problema:**
SSL não era provisionado automaticamente porque o DNS CNAME não existia quando o Traefik tentava emitir o certificado Let's Encrypt.

**Solução:**
1. Criado script `scripts/create_cloudflare_cname.sh` que automatiza criação de CNAME via API Cloudflare
2. Adicionado Step 3 no workflow: "Create DNS CNAME Record" (antes do GitHub Setup)
3. Script detecta CNAMEs duplicados e continua deploy sem erro

**Workflow atualizado:**
```
Step 1: Prepare Application
Step 2: Configure Docker Compose
Step 3: Create DNS CNAME Record  ← NOVO
Step 4: GitHub Setup
Step 5: VPS Deployment
Step 6: Validation
```

**Credenciais Cloudflare (pré-configuradas no script):**
- Zone ID: `e28ff35f0f4e5ba0da93688f8352dd9f`
- Email: `felipidipaula@gmail.com`
- API Key: `7e720179db9ea1041b9a030a531250750ce17`
- Domain: `loop9.com.br`

**Uso:**
```bash
bash .claude/skills/upto-vps/scripts/create_cloudflare_cname.sh <subdomain>
```

**Validação:**
Após criar CNAME, sempre validar com:
```bash
echo | openssl s_client -servername <subdomain>.loop9.com.br -connect <subdomain>.loop9.com.br:443 2>/dev/null | openssl x509 -noout -issuer -subject
```

Deve mostrar:
```
issuer=C=US, O=Let's Encrypt, CN=R12
subject=CN=<subdomain>.loop9.com.br
```

Se mostrar "TRAEFIK DEFAULT CERT", recriar stack:
```bash
ssh root@82.25.68.132 "docker stack rm <stack> && sleep 10 && docker stack deploy -c docker-compose.yml <stack>"
```

**Arquivos atualizados:**
- `.claude/skills/upto-vps/SKILL.md` (Step 3 adicionado)
- `.claude/skills/upto-vps/scripts/create_cloudflare_cname.sh` (criado)
- `.claude/skills/upto-vps/LEARNINGS.md` (este arquivo)

**Prevenção:**
Skill agora SEMPRE cria CNAME antes de fazer deploy, garantindo SSL em primeira tentativa.

---

## 2025-11-10: Organização Obrigatória em APPS E SITES

**Problema:**
Apps e sites criados sem organização, espalhados em pastas aleatórias, sem documentação, dificultando manutenção e rastreamento.

**Solução:**
1. Criada pasta centralizada: `APPS E SITES/`
2. Estrutura obrigatória para cada projeto:
   - `INDEX.md` (documentação completa do projeto)
   - `CHANGELOG.md` (histórico de versões)
   - Entry no master `APPS E SITES/INDEX.md`

3. Criado script `scaffold_project.sh` para automação
4. Templates padronizados para documentação
5. Naming convention: kebab-case para tudo

**Estrutura implementada:**
```
APPS E SITES/
├── INDEX.md (master registry - lista todos projetos)
└── <project-name>/
    ├── INDEX.md (status, tech, deploy logs)
    ├── CHANGELOG.md (version history)
    ├── README.md (quick start)
    ├── .gitignore
    ├── docker-compose.yml
    └── source code
```

**Workflow atualizado:**
```
Step 1: Create Project Structure  ← NOVO (scaffold + docs)
Step 2: Prepare Application
Step 3: Configure Docker Compose
Step 4: Create DNS CNAME
Step 5: GitHub Setup
Step 6: VPS Deployment
Step 7: Validation & Documentation  ← ATUALIZADO (update INDEXes)
```

**Uso do scaffold:**
```bash
bash .claude/skills/upto-vps/scripts/scaffold_project.sh <project-name> <type>
# Tipos: static, flask, node, api, dashboard
```

**Documentação obrigatória:**
- Master INDEX: Lista completa de projetos com links
- Project INDEX: Status, tech stack, commands, logs
- CHANGELOG: Histórico de updates
- Atualizar todos após cada deploy

**Arquivos criados:**
- `APPS E SITES/INDEX.md` (master registry)
- `.claude/skills/upto-vps/assets/PROJECT_INDEX_TEMPLATE.md` (template)
- `.claude/skills/upto-vps/scripts/scaffold_project.sh` (automation)

**Prevenção:**
Skill agora SEMPRE cria projetos em `APPS E SITES/` com documentação completa, garantindo rastreabilidade e organização.
