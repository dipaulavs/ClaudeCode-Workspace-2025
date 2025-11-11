# 🤖 Claude Code Configuration v7.7
**Auto-load:** Sobrescreve comportamentos padrão | **Limite:** 150 linhas | **Última atualização:** 2025-11-10 21:30

---

## 🚨 REGRAS CRÍTICAS (Prioridade Máxima)

### 1️⃣ Comunicação Ultra-Concisa
**Formato:** O que farei (1 linha) → Executo → Resultado (1-2 linhas)
**Proibido:** Repetir pedido, contexto óbvio, explicações longas
**Exceções:** Erros críticos, usuário pede detalhes

### 2️⃣ Uso Máximo de Subagentes (PRIORIDADE)
**Avaliar PRIMEIRO:** Toda solicitação pode usar Task/subagentes?
**Se SIM:** Usar SEMPRE (Explore, Plan, general-purpose, skills)
**Nunca economizar:** Tokens/recursos irrelevantes vs velocidade
**Princípio:** Paralelizar subagentes = máxima eficiência

### 3️⃣ Confirmação para Modificações
**Planejar → Aguardar → Executar** (criar/modificar arquivos)
**Executar direto:** Read, Grep, ls, git status, templates únicos

### 4️⃣ Priorização de Recursos
**Ordem:** 1) Skills → 2) Templates → 3) Criar novo
**Consultar antes de criar:** `.claude/skills/INDEX.md` | `docs/MAPA_ACOES.md`

### 5️⃣ TodoWrite Inteligente
**Usar:** 3+ etapas, múltiplos arquivos
**Não usar:** Ação trivial única

### 6️⃣ Credenciais e APIs
**ANTES de criar ferramenta:** Consultar `🔐 Credenciais/🔑 Cofre de APIs.md` (Obsidian)
**Verificar:** Chave já existe? Usar a existente!
**Após nova API:** Registrar no Cofre com nome, chave, uso, localização
**Google APIs:** `config/google_service_account.json` já configurado (projeto: claude-code)

### 7️⃣ Formato Visual Universal
**OBRIGATÓRIO em:** Respostas | Explicações | Resumos | Qualquer comunicação

**Boxes (processos/fluxos):**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Cliente   │ → │   Template  │ → │  Chatbot ✅ │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Fluxograma ASCII (decisões/lógica):**
```
Tem skill? ──YES──> Usa skill
    │
    NO
    │
    ├──> Tem template? ──YES──> Usa template
    │         │
    │         NO
    │         └──> Cria novo
```

**Aplicar sempre que:** Responder | Explicar | Resumir | Usuário pedir resumo

### 8️⃣ Criação de Slash Commands
**Estrutura OBRIGATÓRIA:**
```markdown
---
description: Descrição breve do comando
---

# Título

Instruções do comando
```

**Local:** `.claude/commands/nome.md`
**Regra:** SEMPRE incluir frontmatter YAML com `description` ou comando não aparece

### 9️⃣ Auto-Melhoria Contínua (OBRIGATÓRIO)
**Regra:** Erro corrigido = Registro atualizado
**Fluxo:** Corrigir bug/erro → Atualizar script/doc → Prevenir recorrência
**Aplicar em:** Scripts Python | Docs | Skills | Templates | Qualquer processo
**Objetivo:** Nunca repetir o mesmo erro

### 🔟 Avaliar MCP Primeiro (ESSENCIAL)
**ANTES de criar ferramenta:** Verificar se existe MCP tool disponível
**Fluxo:** MCP existe? → Usar MCP | Não existe? → Criar ferramenta nova
**Princípio:** Reusar MCP tools > Criar código novo
**Onde verificar:** Lista de `mcp__*` tools disponíveis no contexto

### 1️⃣1️⃣ Organização É Tudo (ABSOLUTO)
**REGRA ABSOLUTA:** NUNCA criar arquivos soltos ou em pastas aleatórias
**Princípio:** Pastas → Subpastas → INDEX.md com endereço/função resumida
**Fluxo obrigatório:**
```
App/Site/HTML?  ────> APPS E SITES/categoria/ + INDEX.md
Script Python?  ────> SCRIPTS/categoria/ + INDEX.md
Script Bash?    ────> SCRIPTS/categoria/ + INDEX.md
Skill nova?     ────> .claude/skills/nome/ + atualizar INDEX.md
Documentação?   ────> docs/categoria/ + INDEX.md
Template?       ────> templates/categoria/ + INDEX.md
Config?         ────> config/
Outro?          ────> Perguntar ao usuário
```
**OBRIGATÓRIO em cada pasta:**
- `INDEX.md` listando arquivos com endereço e função resumida
- Estrutura hierárquica clara (categoria/subcategoria)
- Nunca misturar tipos diferentes na mesma pasta

**Proibido:** Criar `.py`, `.sh`, `.md`, `.json`, `.html` diretamente em `/` ou pasta genérica
**Exceções:** `CLAUDE.md`, `README.md`, `.gitignore`, `package.json` (raiz apenas)
**Antes de criar:** Identificar categoria → Criar estrutura de pastas → Criar INDEX.md → Criar arquivo

### 1️⃣2️⃣ Deploy Padrão com SWARM + GitHub (OBRIGATÓRIO)
**Quando:** Criar servidor | Subir site | API webhook | Automação 24/7
**Fluxo SEMPRE (via GitHub):**
```
1. cd SWARM/automations/<nome> → desenvolver
2. git add . && git commit -m "feat: ..."
3. git push origin main
4. SSH VPS: git pull && docker stack deploy
5. https://<subdominio>.loop9.com.br ✅
```
**Setup inicial:**
```
cd SWARM && ./new.sh <nome> webhook-api <subdominio>
cd automations/<nome> && git init && git remote add origin <repo>
```
**PROIBIDO:** Deploy direto sem Git | `./deploy.sh` local→VPS | Copiar arquivos via SCP
**OBRIGATÓRIO:** Todo código versionado no GitHub primeiro
**Padrões:** Naming kebab-case | SSL automático | Rede loop9Net
**Gerenciar:** SSH VPS → `docker stack` commands
**Logs:** SSH VPS → `docker service logs`

---

## 🔑 CREDENCIAIS PRÉ-CONFIGURADAS

**Google Service Account (Universal):**
- **Email:** calude-code@claude-code-477312.iam.gserviceaccount.com
- **Projeto:** claude-code (NÃO automaia)
- **Local:** `config/google_service_account.json`
- **APIs ativas:** Sheets, Drive, Gmail, Docs
- **Uso:** Qualquer ferramenta Google (sheets, calendar, drive, etc)

**Cofre Completo:** `~/Documents/Obsidian/Claude-code-ios/🔐 Credenciais/🔑 Cofre de APIs.md`
**Regra:** SEMPRE consultar Cofre ANTES de criar ferramenta nova

---

## ⚡ GATILHOS AUTOMÁTICOS

| Situação | Ação | Detalhes |
|----------|------|----------|
| **"To com uma ideia..."** | `adaptive-mentor` skill | Mentoria contextual |
| **"Estuda esse vídeo pra mim"** | `estudar-video` skill | Somente pedido explícito |
| **"Valida essa ideia"** | `idea-validator` skill | Validação mercado |
| **"Cria PRD/MVP"** | `launch-planner` skill | Planejamento produto |
| **"Upload rápido"** | `upload_rapido.py --from-local` | ~/Pictures/upload/ |
| **"Adiciona imóvel"** | Upload → estrutura → links.json | Bot WhatsApp |
| **"Cria chatbot para..."** | `criar_chatbot_cliente.py` | Framework Universal 5min |
| **"Anota no Obsidian"** | `obsidian-organizer` skill | NUNCA direto |
| **"Organize minhas notas"** | `obsidian-organizer` skill | Organização Obsidian |
| **2+ imagens/vídeos** | `batch_generate.py` | OBRIGATÓRIO batch |
| **WhatsApp mídia** | `--url` com link público | NUNCA --file |
| **Script com erro** | Corrigir → Atualizar script → Docs | Auto-melhoria |
| **"Criar ferramenta..."** | 1° Consultar Cofre APIs | Reusar credenciais existentes |
| **Nova API implementada** | Registrar no Cofre de APIs | Obsidian: `🔐 Credenciais/🔑 Cofre de APIs.md` |
| **"Sobe servidor/site"** | SWARM: `./new.sh` → deploy | SSL automático .loop9.com.br |
| **"Criar API/webhook"** | SWARM template webhook-api | Flask + Traefik + SSL |

---

## 📚 ÍNDICES MESTRES

| Recurso | Localização | Quantidade |
|---------|-------------|------------|
| **Skills** | `.claude/skills/INDEX.md` | 26 skills |
| **Templates** | `docs/MAPA_ACOES.md` | 71+ templates |
| **Ferramentas** | `docs/tools/INDEX.md` | 65+ tools |
| **Regras Decisão** | `docs/REGRAS_DECISAO.md` | 10+ fluxogramas |
| **Knowledge Bases** | `docs/KNOWLEDGE_BASES.md` | 3 KBs |

---

## 🚀 COMANDOS ESSENCIAIS

```bash
# Chatbots
python3 criar_chatbot_cliente.py       # 🚀 CRIAR NOVO CHATBOT (framework universal)
cd whatsapp-chatbot-carros && ./INICIAR_COM_NGROK.sh  # Exemplo funcional (Automaia)

# Deploy (SWARM)
cd SWARM
./new.sh <nome> webhook-api <subdom>   # Criar estrutura
cd automations/<nome>                  # Desenvolver
cd ../.. && ./deploy.sh <nome>         # Deploy VPS
./manage.sh list                       # Listar
./logs.sh <nome>                       # Logs

# Backup
/bk                     # Git backup automático
/cbk                    # Listar/restaurar backups

# Geração (1 item = direto | 2+ = batch)
python3 scripts/image-generation/generate_nanobanana.py "prompt"
python3 scripts/video-generation/generate_sora.py "prompt"
python3 scripts/audio-generation/generate_elevenlabs.py "texto"
python3 scripts/image-generation/batch_generate.py --api nanobanana "p1" "p2"
```

---

## 📁 ESTRUTURA SIMPLIFICADA

```
ClaudeCode-Workspace/
├── .claude/skills/      → 26 Skills com INDEX.md
├── SWARM/               → 🐳 Deploy profissional VPS (82.25.68.132)
├── scripts/             → 71+ Templates organizados
├── tools/               → 65+ Ferramentas low-level
├── docs/                → Toda documentação detalhada
├── chatbot-template/    → 🎯 Template universal (base limpa)
├── whatsapp-chatbot-carros/ → Exemplo funcional (Automaia)
├── criar_chatbot_cliente.py → 🚀 Gerador (5min)
└── CLAUDE.md            → Este arquivo (config mínima)
```

---

## ⚙️ META-CONFIGURAÇÃO

**Editar CLAUDE.md:** Máx 150 linhas | Só regras críticas | Links para detalhes
**Adicionar recurso:** Criar → Documentar → Indexar → Nunca inline aqui
**Prioridade absoluta:** Skills > Templates > Criar novo
**APIs/Detalhes:** Movidos para `docs/CONFIG.md`

---

## 🔗 LINKS RÁPIDOS

- **README Principal:** `README.md`
- **Configurações APIs:** `docs/CONFIG.md`
- **🔑 Cofre de APIs (Obsidian):** `🔐 Credenciais/🔑 Cofre de APIs.md`
- **🚀 Framework Chatbot Universal:** `FRAMEWORK_CHATBOT.md`
- **🐳 Deploy SWARM:** `SWARM/README.md`
- **Exemplo Automaia (carros):** `whatsapp-chatbot-carros/README.md`

---

**v7.7** | **SWARM padrão** | **Deploy profissional** | **SSL automático** | **loop9.com.br**