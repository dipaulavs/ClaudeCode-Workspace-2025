# 🤖 Claude Code - Workspace Configuration

**Auto-load:** Este arquivo é carregado automaticamente e SOBRESCREVE comportamentos padrão do Claude Code.

---

## 🚨 REGRAS DE COMPORTAMENTO (PRIORIDADE MÁXIMA)

### 1️⃣ Confirmação Obrigatória

**SEMPRE que usuário pedir qualquer ação que crie/modifique arquivos:**

**Passo 1 - PLANEJAR:**
- Apresentar plano objetivo (3-5 itens)
- Mostrar quais arquivos serão criados/modificados
- Indicar comandos que serão executados

**Passo 2 - AGUARDAR:**
- Não executar até usuário confirmar
- Aceitar ajustes no plano

**Passo 3 - EXECUTAR:**
- Só após confirmação explícita

**Exceções** (executar direto sem plano):
- Leitura de arquivos (Read, Grep, Glob)
- Busca/pesquisa
- Comandos informativos (ls, git status)
- Templates únicos e diretos (ex: enviar mensagem WhatsApp)

**Por quê:** Garante alinhamento com raciocínio do usuário e evita retrabalho.

---

### 2️⃣ Preferência por Templates

**SEMPRE verificar se existe template antes de criar código novo:**

| Categoria | Localização | Verificar em |
|-----------|-------------|--------------|
| WhatsApp | `scripts/whatsapp/` | 22 templates |
| Instagram Publicação | `scripts/instagram/` | 6 templates |
| Instagram Scraper | `scripts/instagram-scraper/` | 5 templates |
| Meta Ads | `scripts/meta-ads/` | 4 templates |
| Nextcloud | `scripts/nextcloud/` | 2 templates |
| Obsidian | `scripts/obsidian/` | 5 templates |
| Imagens | `scripts/image-generation/` | 5 templates |
| Vídeos | `scripts/video-generation/` | 2 templates |
| Áudio | `scripts/audio-generation/` | 2 templates |
| Extração | `scripts/extraction/` | 4 templates |
| Busca (xAI) | `scripts/search/` | 3 templates |
| Twitter/X | `scripts/twitter/` | 5 templates |
| TikTok | `scripts/tiktok/` | 5 templates |
| Google Maps | `scripts/scraping/` | 3 templates |

**NUNCA:**
- ❌ Criar scripts descartáveis/temporários
- ❌ Criar arquivos `test_*.py` quando existe template
- ❌ Usar ferramentas de `tools/` diretamente (usar templates de `scripts/`)

---

### 3️⃣ Organização de Arquivos

**Ao criar QUALQUER novo recurso:**

1. ✅ **Nunca criar arquivos soltos na raiz**
2. ✅ **Usar estrutura existente:**
   - Scripts Python → `tools/` (ferramenta low-level) ou `scripts/` (template)
   - Documentação → `docs/` (na subpasta apropriada)
   - Configs → `config/` (com nome descritivo)
   - Projetos completos → Pasta própria na raiz

3. ✅ **Estrutura para NOVOS projetos:**
   ```
   nome-projeto/
   ├── README.md          (obrigatório)
   ├── src/               (código)
   ├── config/            (configurações)
   └── docs/              (docs detalhadas)
   ```

---

### 4️⃣ Auto-Documentação de Novos Recursos (OBRIGATÓRIO)

**Gatilho:** Quando criar nova ferramenta/template/funcionalidade

**Após criar o recurso, SEMPRE executar 4 passos:**

#### ✅ Passo 1: Documentar no README da Categoria

```bash
# Exemplo: Criou template WhatsApp
scripts/whatsapp/README.md
  ↳ Adicionar na seção apropriada
  ↳ Incluir exemplo de uso
  ↳ Parâmetros principais
```

#### ✅ Passo 2: Registrar no CLAUDE.md

**Localização neste arquivo:**
- **Templates (scripts/)** → Adicionar em `📍 MAPA DE AÇÕES` + `🗂️ CATEGORIAS`
- **Ferramentas (tools/)** → Adicionar em `🛠️ FERRAMENTAS DISPONÍVEIS`
- **Novos projetos** → Adicionar em `📁 ESTRUTURA DO WORKSPACE`

**Formato de registro:**

**A) Para Templates (scripts/):**
```markdown
## 📍 MAPA DE AÇÕES
[...]
| **[NOVA AÇÃO]** | `scripts/[categoria]/[nome].py` | `scripts/[categoria]/README.md` |

## 🗂️ CATEGORIAS DE TEMPLATES
### [Categoria] (X templates) ← ATUALIZAR CONTADOR
- **[Subcategoria]:** [...], [NOVO_TEMPLATE] ← ADICIONAR AQUI
```

**B) Para Ferramentas (tools/):**
```markdown
## 🛠️ FERRAMENTAS DISPONÍVEIS
| **[Categoria]** | [...], [NOVA_FERRAMENTA] | `docs/tools/[nome].md` |
```

**C) Para Regras de Decisão (se aplicável):**
```markdown
## 🔍 REGRAS DE DECISÃO
### [Categoria]
[Nova condição]?
├─ [Caso 1] → [template]
└─ [Caso 2] → [template]
```

#### ✅ Passo 3: Manter Organização

**Princípios:**
1. Não quebrar estrutura existente
2. Atualizar contadores (X templates) → (X+1 templates)
3. Manter ordem alfabética (quando aplicável)
4. Formato consistente com entradas existentes
5. Não duplicar (verificar antes)

#### ✅ Passo 4: Resumo Final ao Usuário

**SEMPRE mostrar:**
```
✅ Recurso criado e documentado:

📂 Arquivos:
  • scripts/[categoria]/[arquivo].py (novo template)
  • scripts/[categoria]/README.md (atualizado)
  • CLAUDE.md (registrado em 2 locais)

📍 Registrado no CLAUDE.md:
  • Seção "MAPA DE AÇÕES" (linha ~XX)
  • Seção "[CATEGORIA]" (linha ~YY)

🎯 Como usar:
  python3 scripts/[categoria]/[arquivo].py [exemplo]
```

---

### 5️⃣ TodoWrite Obrigatório

**Usar quando:**
- Tarefa com 3+ etapas
- Múltiplos arquivos envolvidos
- Usuário lista múltiplas ações

**Não usar quando:**
- Ação única trivial
- Leitura simples
- Template direto

---

## 📍 MAPA DE AÇÕES (Índice Rápido)

### Quando usuário pedir... | Use isto | Doc completa
|---------------------------|----------|--------------|
| **Enviar WhatsApp** | `scripts/whatsapp/send_message.py` | `scripts/whatsapp/README.md` |
| **Mídia WhatsApp** | `scripts/whatsapp/send_media.py` | `scripts/whatsapp/README.md` |
| **Criar grupo WhatsApp** | `scripts/whatsapp/create_group.py` | `scripts/whatsapp/README.md` |
| **Agendar WhatsApp** | `scheduling-system/schedule_whatsapp.py` | `scheduling-system/README.md` |
| **Publicar Instagram** | `scripts/instagram/publish_post.py` | `scripts/instagram/README.md` |
| **Carrossel Instagram** | `scripts/instagram/publish_carousel.py` | `scripts/instagram/README.md` |
| **Reel Instagram** | `scripts/instagram/publish_reel.py` | `scripts/instagram/README.md` |
| **Story Instagram** | `scripts/instagram/publish_story.py` | `scripts/instagram/README.md` |
| **Scrape Instagram** | `scripts/instagram-scraper/scrape_*.py` | `scripts/instagram-scraper/README.md` |
| **Campanha Meta Ads** | `scripts/meta-ads/create_campaign.py` | `scripts/meta-ads/README.md` |
| **Anúncio Meta Ads** | `scripts/meta-ads/create_ad.py` | `scripts/meta-ads/README.md` |
| **Upload Nextcloud** | `scripts/nextcloud/upload_from_downloads.py` | `scripts/nextcloud/README.md` |
| **1 imagem** | `scripts/image-generation/generate_nanobanana.py` | `scripts/image-generation/README.md` |
| **2+ imagens** | `scripts/image-generation/batch_generate.py --api nanobanana` | `scripts/image-generation/README.md` |
| **Editar imagem** | `scripts/image-generation/edit_nanobanana.py` | `scripts/image-generation/README.md` |
| **1 vídeo** | `scripts/video-generation/generate_sora.py` | `scripts/video-generation/README.md` |
| **2+ vídeos** | `scripts/video-generation/batch_generate.py` | `scripts/video-generation/README.md` |
| **1 áudio** | `scripts/audio-generation/generate_elevenlabs.py` | `scripts/audio-generation/README.md` |
| **2+ áudios** | `scripts/audio-generation/batch_generate.py` | `scripts/audio-generation/README.md` |
| **Transcrever vídeo** | `scripts/extraction/transcribe_video.py` | `scripts/extraction/README.md` |
| **Web scraping** | `scripts/extraction/scrape_website.py` | `scripts/extraction/README.md` |
| **Buscar web** | `scripts/search/xai_web.py` (Python 3.11) | `scripts/search/README.md` |
| **Buscar Twitter/X** | `scripts/search/xai_twitter.py` (Python 3.11) | `scripts/search/README.md` |
| **Buscar notícias** | `scripts/search/xai_news.py` (Python 3.11) | `scripts/search/README.md` |
| **Scrape Twitter/X** | `scripts/twitter/search_twitter.py` | `scripts/twitter/README.md` |
| **Scrape TikTok** | `scripts/tiktok/*.py` | `scripts/tiktok/README.md` |
| **Scrape Google Maps** | `scripts/scraping/google_maps_*.py` | `scripts/scraping/README.md` |
| **Nota rápida Obsidian** | `scripts/obsidian/quick_note.py` | `scripts/obsidian/README.md` |
| **Capturar ideia Obsidian** | `scripts/obsidian/capture_idea.py` | `scripts/obsidian/README.md` |
| **Daily note Obsidian** | `scripts/obsidian/create_daily.py` | `scripts/obsidian/README.md` |
| **Projeto Obsidian** | `scripts/obsidian/new_project.py` | `scripts/obsidian/README.md` |

---

## 🗂️ CATEGORIAS DE TEMPLATES

### WhatsApp (22 templates)
- **Envio:** send_message, send_media, send_audio, send_location, send_contact, send_poll
- **Interação:** send_reaction, send_reply, send_mention, send_status, message_actions
- **Grupos:** list_groups, create_group, update_group, manage_participants, leave_group
- **Sistema:** instance_info, check_number, manage_webhooks, get_contacts, manage_profile, get_profile
- **Doc:** `scripts/whatsapp/README.md`

### Instagram Publicação (6 templates)
- **Templates:** publish_post, publish_carousel, publish_reel, publish_story, get_insights, manage_comments
- **Doc:** `scripts/instagram/README.md`

### Instagram Scraper (5 templates)
- **Templates:** scrape_user_posts, scrape_hashtag_posts, scrape_post_comments, scrape_user_profile, scrape_place_posts
- **Doc:** `scripts/instagram-scraper/README.md`

### Meta Ads (4 templates)
- **Templates:** create_campaign, create_adset, create_ad, get_insights
- **Doc:** `scripts/meta-ads/README.md`

### Nextcloud (2 templates)
- **Templates:** upload_to_nextcloud, upload_from_downloads
- **Doc:** `scripts/nextcloud/README.md`

### Obsidian (5 templates)
- **Templates:** quick_note, capture_idea, create_daily, new_project, obsidian_client (API)
- **Doc:** `scripts/obsidian/README.md`

### Imagens (5 templates)
- **Templates:** generate_nanobanana (padrão), generate_gpt4o, generate_dalle3, batch_generate, edit_nanobanana
- **Doc:** `scripts/image-generation/README.md`

### Vídeos (2 templates)
- **Templates:** generate_sora, batch_generate
- **Doc:** `scripts/video-generation/README.md`

### Áudio (2 templates)
- **Templates:** generate_elevenlabs, batch_generate
- **Doc:** `scripts/audio-generation/README.md`

### Extração (4 templates)
- **Templates:** transcribe_video, extract_instagram, scrape_website, scrape_batch
- **Doc:** `scripts/extraction/README.md`

### Busca xAI (3 templates)
- **Templates:** xai_web, xai_twitter, xai_news
- **Requer:** Python 3.11+
- **Doc:** `scripts/search/README.md`

### Twitter/X (5 templates)
- **Templates:** search_twitter, scrape_profile, scrape_tweets, scrape_replies, batch_twitter
- **Doc:** `scripts/twitter/README.md`

### TikTok (5 templates)
- **Templates:** get_user_info, get_video_info, search_content, get_trending, analyze_hashtag
- **Doc:** `scripts/tiktok/README.md`

### Google Maps (3 templates)
- **Templates:** google_maps_basic, google_maps_advanced, google_maps_batch
- **Doc:** `scripts/scraping/README.md`

---

## 🔍 REGRAS DE DECISÃO (Fluxogramas)

### Imagens
```
Usuário pede quantas imagens?
├─ 1 imagem → generate_nanobanana.py
└─ 2+ imagens → batch_generate.py --api nanobanana (OBRIGATÓRIO)
```

### Vídeos
```
Usuário pede quantos vídeos?
├─ 1 vídeo → generate_sora.py
└─ 2+ vídeos → batch_generate.py (OBRIGATÓRIO)
```

### Áudio
```
Usuário pede quantos áudios?
├─ 1 áudio → generate_elevenlabs.py
└─ 2+ áudios → batch_generate.py (OBRIGATÓRIO)
```

### Instagram
```
Usuário quer publicar ou extrair?
├─ Publicar → scripts/instagram/publish_*.py
└─ Extrair/Scrape → scripts/instagram-scraper/scrape_*.py
```

### Google Maps
```
Quantas buscas?
├─ 1 busca simples → google_maps_basic.py
├─ 1 busca com filtros → google_maps_advanced.py
└─ 2+ buscas → google_maps_batch.py (OBRIGATÓRIO)
```

### Busca (xAI Search)
```
Buscar onde?
├─ Web/Documentação → xai_web.py (Python 3.11)
├─ Twitter/X → xai_twitter.py (Python 3.11)
└─ Notícias → xai_news.py (Python 3.11)
```

---

## 🧠 CLAUDE SKILLS (Model-Invoked AI Capabilities)

**Localização:** `.claude/skills/` (compartilhadas via git)

### O Que São Skills?
Skills são **capacidades modulares** que estendem Claude Code. Diferente de comandos slash (user-invoked), as Skills são **model-invoked**: Claude decide automaticamente quando usá-las baseado no contexto da conversa.

### Skills Disponíveis (5 Skills)

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **idea-validator** | Validar ideias antes de construir | Analisa saturação de mercado, viabilidade, demanda real, monetização. Dá feedback brutalmente honesto. |
| **launch-planner** | Planejar lançamento de MVP | Transforma ideias validadas em PRDs completos com roadmap, schema de DB, e escopo MVP (2-4 semanas). |
| **product-designer** | Design de UI/UX | Elimina o "visual de IA" (gradientes azul/roxo). Cria interfaces profissionais com Tailwind + shadcn/ui. |
| **marketing-writer** | Criar conteúdo de marketing | Escreve landing pages, tweets, Product Hunt, emails de lançamento. Tom claro e focado em benefícios. |
| **roadmap-builder** | Priorizar features | Atua como PM: decide o que construir (e o que NÃO construir). Previne feature creep. |

### Como Funcionam
1. ✅ **Ativação automática** - Claude detecta quando usar baseado na descrição da Skill
2. ✅ **Context-aware** - Analisa código existente automaticamente
3. ✅ **Tool restrictions** - Cada Skill limita ferramentas permitidas (segurança/foco)
4. ✅ **Compartilháveis** - Time todo recebe via `git pull`

### Estrutura de uma Skill

```
.claude/skills/
└── nome-da-skill/
    └── SKILL.md              # YAML frontmatter + instruções
```

**YAML frontmatter obrigatório:**
```yaml
---
name: nome-da-skill          # lowercase, hífens, max 64 chars
description: O que faz e quando usar (max 1024 chars)
allowed-tools: Read, Write   # (opcional) limita ferramentas
---
```

### Exemplos de Uso

**Validar Ideia:**
```
Usuário: "Valide esta ideia: app store para apps vibe coded"
Claude: [Automaticamente usa idea-validator skill]
```

**Planejar MVP:**
```
Usuário: "Ajude-me a planejar o lançamento de [app]"
Claude: [Automaticamente usa launch-planner skill]
```

**Design de Componente:**
```
Usuário: "Crie uma landing page moderna"
Claude: [Automaticamente usa product-designer skill]
```

**Marketing:**
```
Usuário: "Escreva um tweet de lançamento"
Claude: [Automaticamente usa marketing-writer skill]
```

**Roadmap:**
```
Usuário: "Quais features devo adicionar?"
Claude: [Automaticamente usa roadmap-builder skill]
```

### Criar Nova Skill

1. Criar pasta: `.claude/skills/minha-skill/`
2. Criar arquivo: `SKILL.md` com YAML frontmatter
3. Commitar no git (time todo recebe)
4. Claude detecta automaticamente

### Documentação Oficial
- 📚 Skills Guide: https://docs.claude.com/en/docs/claude-code/skills.md

---

## ⚡ Quick Actions (Comandos Mais Usados)

### Chatbot WhatsApp
```bash
bot         # Iniciar (alias)
botstop     # Parar (alias)
# Logs: whatsapp-chatbot/logs/chatbot_v4.log
```

### Backup Git (Sistema Automático)
```bash
# Fazer backup automático (add + commit + push)
/bk

# Listar e restaurar backups anteriores
/cbk

# Comandos manuais alternativos:
git add . && git commit -m "Backup manual" && git push origin main

# Ver histórico de backups
git log --oneline -10

# Restaurar arquivo específico de versão antiga
git checkout HASH -- caminho/arquivo.py

# Repositório: https://github.com/dipaulavs/ClaudeCode-Workspace-2025
# Status: PRIVADO (inclui .env)
```

### Agendamento WhatsApp
```bash
# Agendar mensagem única
python3 scheduling-system/schedule_whatsapp.py --phone 5531980160822 --message "Texto" --time 17:00

# Agendar recorrente (diário)
python3 scheduling-system/schedule_whatsapp.py --phone 5531980160822 --message "Bom dia!" --time 09:00 --daily

# Listar agendamentos
python3 scheduling-system/schedule_whatsapp.py --list
```

### Geração de Conteúdo
```bash
# Imagem (padrão: Nano Banana)
python3 scripts/image-generation/generate_nanobanana.py "prompt"

# Múltiplas imagens (BATCH obrigatório)
python3 scripts/image-generation/batch_generate.py --api nanobanana "prompt1" "prompt2" "prompt3"

# Vídeo (padrão: portrait Stories/Reels)
python3 scripts/video-generation/generate_sora.py "prompt"

# Áudio (padrão: voz Michele)
python3 scripts/audio-generation/generate_elevenlabs.py "texto"
```

### WhatsApp Templates
```bash
# Enviar mensagem
python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Olá!"

# Enviar mídia
python3 scripts/whatsapp/send_media.py --phone 5531980160822 --file "foto.jpg" --type image

# Criar grupo
python3 scripts/whatsapp/create_group.py --name "Grupo" --phones 5531980160822,5511999999999
```

### Instagram
```bash
# Publicar post
python3 scripts/instagram/publish_post.py --image "foto.jpg" --caption "Legenda"

# Scrape posts
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo" --limit 50
```

### Busca/Extração
```bash
# Transcrever vídeo
python3 scripts/extraction/transcribe_video.py "https://youtu.be/VIDEO_ID"

# Buscar na web (Python 3.11)
python3.11 scripts/search/xai_web.py "Python best practices 2025"
```

---

## 🛠️ FERRAMENTAS DISPONÍVEIS

**📚 Índice completo:** `docs/tools/INDEX.md`

| Categoria | Ferramentas | Docs |
|-----------|-------------|------|
| **Geração Imagem** | GPT-4o, Nano Banana, DALL-E 3, Batch, Edição | `scripts/image-generation/README.md` |
| **Geração Vídeo** | Sora 2 (único, batch), 3 proporções | `scripts/video-generation/README.md` |
| **Geração Áudio** | ElevenLabs TTS (único, batch), Vozes clonadas | `scripts/audio-generation/README.md` |
| **Instagram API** | Post, Carrossel, Reel, Story, Insights, Comments | `scripts/instagram/README.md` |
| **Instagram Scraper** | Posts, Hashtags, Comentários, Perfis (Apify) | `scripts/instagram-scraper/README.md` |
| **WhatsApp** | 22 templates (mensagens, grupos, mídia, etc) | `scripts/whatsapp/README.md` |
| **Meta Ads** | Campanhas, Ad Sets, Anúncios, Insights | `scripts/meta-ads/README.md` |
| **Extração** | Transcrição vídeos, IG posts, Web scraping | `scripts/extraction/README.md` |
| **Busca xAI** | Web, Twitter/X, Notícias (tempo real) | `scripts/search/README.md` |
| **Twitter Scraper** | Tweets, Perfis, Replies (Apify) | `scripts/twitter/README.md` |
| **TikTok Scraper** | Usuários, Vídeos, Trending, Hashtags | `scripts/tiktok/README.md` |
| **Google Maps** | Locais, Reviews, Dados de negócios (Apify) | `scripts/scraping/README.md` |
| **Nextcloud** | Upload manual, Upload rápido Downloads | `scripts/nextcloud/README.md` |
| **Obsidian PKM** | Notes, Ideas, Daily, Projects, Search | `docs/tools/obsidian_integration.md` |
| **Agendamento** | Sistema WhatsApp (único/recorrente) | `scheduling-system/README.md` |

**Total:** 65+ templates | 40+ ferramentas

---

## 📁 ESTRUTURA DO WORKSPACE

```
ClaudeCode-Workspace/
├── 📄 README.md                 # Índice geral
├── 📄 CLAUDE.md                 # Config auto-load (este arquivo)
├── 📄 requirements.txt          # Dependências Python
│
├── 📁 .claude/                  # Configuração Claude Code
│   ├── commands/                # Comandos slash (/bk, /cbk)
│   └── skills/                  # 🧠 5 Claude Skills (model-invoked)
│       ├── idea-validator/      # Valida ideias antes de construir
│       ├── launch-planner/      # Planeja MVPs e roadmaps
│       ├── product-designer/    # Design profissional de UI
│       ├── marketing-writer/    # Conteúdo de marketing
│       └── roadmap-builder/     # Priorização de features (PM)
│
├── 📁 scripts/                  # 65+ Templates prontos
│   ├── whatsapp/                # 22 templates WhatsApp
│   ├── instagram/               # 6 templates publicação IG
│   ├── instagram-scraper/       # 5 templates scraping IG
│   ├── meta-ads/                # 4 templates Meta Ads
│   ├── nextcloud/               # 2 templates upload
│   ├── obsidian/                # 5 templates Obsidian PKM
│   ├── image-generation/        # 5 templates imagens
│   ├── video-generation/        # 2 templates vídeos
│   ├── audio-generation/        # 2 templates áudio
│   ├── extraction/              # 4 templates extração
│   ├── search/                  # 3 templates busca xAI
│   ├── twitter/                 # 5 templates Twitter/X
│   ├── tiktok/                  # 5 templates TikTok
│   ├── scraping/                # 3 templates Google Maps
│   └── common/                  # template_base.py
│
├── 📁 tools/                    # 40+ Ferramentas low-level
├── 📁 config/                   # Configurações APIs
│
├── 📁 docs/                     # Documentação organizada
│   ├── tools/                   # 40+ docs ferramentas
│   ├── guides/                  # Guias gerais
│   ├── workflows/               # Workflows
│   ├── meta-ads-api/            # Docs Meta Ads API
│   └── instagram-api/           # Docs Instagram API
│
├── 📁 whatsapp-chatbot/         # Bot V4 (produção)
├── 📁 scheduling-system/        # Agendamento WhatsApp
├── 📁 n8n-mcp-project/          # n8n-MCP (automação)
├── 📁 crewai/                   # Multi-agentes
└── 📁 evolution-api-integration/# WhatsApp Helper
```

---

## 💡 DICAS IMPORTANTES

### Geração de Múltiplos Itens
🚨 **REGRA CRÍTICA:** 2+ itens = SEMPRE usar batch
- Imagens: `batch_generate.py --api nanobanana`
- Vídeos: `batch_generate.py`
- Áudios: `batch_generate.py`
- **NUNCA** executar múltiplos individuais em sequência

### Modelos Padrão
- **Imagens:** Nano Banana (rápido/econômico)
- **Vídeos:** Sora 2 portrait (Stories/Reels)
- **Áudio:** ElevenLabs voz Michele

### Busca xAI
⚠️ **IMPORTANTE:** Requer Python 3.11+ (sempre usar `python3.11`)

### WhatsApp
- Formato números: DDI+DDD+Número (ex: 5531980160822)
- Sem espaços, hífens ou parênteses

### Instagram Scraping
- Sempre usar `--limit` para controlar custos
- Pricing: $2.30/1000 itens

---

## 📖 DOCUMENTAÇÕES COMPLETAS

| Recurso | Localização |
|---------|-------------|
| **README Principal** | `README.md` |
| **Ferramentas (40+)** | `docs/tools/INDEX.md` |
| **Templates (65+)** | `scripts/README.md` |
| **Obsidian Integration** | `docs/tools/obsidian_integration.md` |
| **Chatbot WhatsApp V4** | `whatsapp-chatbot/README.md` |
| **Agendamento WhatsApp** | `scheduling-system/README.md` |
| **n8n-MCP** | `n8n-mcp-project/README.md` |
| **Meta Ads API** | `docs/meta-ads-api/META_ADS_API_DOCUMENTATION.md` |
| **Instagram API** | `docs/instagram-api/INSTAGRAM_API_DOCUMENTATION.md` |
| **CrewAI** | `crewai/README.md` |

---

## ⚙️ APIs CONFIGURADAS

- ✅ OpenRouter (Claude Haiku/Sonnet 4.5)
- ✅ OpenAI (GPT-4o, Whisper)
- ✅ Gemini 2.5 Flash (Nano Banana)
- ✅ Instagram API (v24.0)
- ✅ Meta Ads API (v24.0)
- ✅ Evolution API (WhatsApp - instância lfimoveis)
- ✅ xAI (Grok)
- ✅ ElevenLabs (TTS)
- ✅ Kie.ai (GPT-4o Image, Sora)
- ✅ Apify (Scraping)
- ✅ RapidAPI (Transcrição)
- ✅ Nextcloud (Upload)
- ✅ Upstash Redis (Memória chatbot)

---

## 💾 SISTEMA DE BACKUP AUTOMÁTICO

### 📦 Repositório GitHub

- **URL:** https://github.com/dipaulavs/ClaudeCode-Workspace-2025
- **Tipo:** Repositório PRIVADO
- **Conteúdo:** Código completo + configs + .env (chaves API incluídas)
- **Branch principal:** main

### ⚡ Comandos Slash Personalizados

#### `/bk` - Backup Automático
**Função:** Fazer backup completo instantâneo para GitHub

**O que faz:**
1. `git add .` (adiciona todas mudanças)
2. `git commit -m "🔄 Backup automático - [DATA/HORA]"` (cria commit)
3. `git push origin main` (envia para GitHub)

**Uso:**
```
Digite: /bk
[ENTER]
Pronto! Backup feito automaticamente.
```

**Quando usar:**
- ✅ Antes de testar código novo/arriscado
- ✅ Após implementar funcionalidade importante
- ✅ Final do dia de trabalho
- ✅ Antes de fazer mudanças estruturais

#### `/cbk` - Consultar Backups (Check Backup)
**Função:** Listar histórico e restaurar versões antigas

**O que mostra:**
- 📊 Total de backups (commits)
- 🕐 Últimos 20 backups com data/hora
- 📝 Arquivos modificados em cada backup
- 🔧 Opções de restauração

**Opções disponíveis:**
1. **Ver detalhes** de commit específico
2. **Comparar** duas versões
3. **Restaurar arquivo** específico
4. **Restaurar projeto inteiro** (cria branch segura)
5. **Apenas visualizar** (sem ação)

**Uso:**
```
Digite: /cbk
[Veja lista de backups]
[Escolha opção desejada]
[Siga instruções]
```

### 🔄 Como Funciona a Restauração

#### Restaurar Arquivo Específico
```bash
# Via /cbk (automático):
1. Digite /cbk
2. Escolha "Restaurar arquivo específico"
3. Informe hash do commit (ex: 6ba7dd2)
4. Informe caminho do arquivo
5. Arquivo é restaurado NA SUA PASTA LOCAL

# Manual (se preferir):
git checkout HASH -- caminho/do/arquivo.py
```

**Exemplo prático:**
```bash
# Restaurar send_message.py de 2 horas atrás
git checkout 6ba7dd2 -- scripts/whatsapp/send_message.py
```

#### Restaurar Projeto Inteiro (Seguro)
```bash
# Via /cbk (recomendado - cria branch):
1. Digite /cbk
2. Escolha "Restaurar projeto inteiro"
3. Sistema faz backup atual automaticamente
4. Cria branch: backup-restore-TIMESTAMP
5. Todos arquivos voltam para aquela versão
6. Para voltar: git checkout main

# Manual (avançado):
git checkout -b backup-restore-20251102 HASH
# Testar...
# Se OK: git checkout main && git merge backup-restore-20251102
# Se não: git checkout main
```

### 📍 Localização dos Arquivos

```
.claude/commands/
├── bk.md        # Comando /bk (backup automático)
└── cbk.md       # Comando /cbk (check backups)
```

### ⚠️ SEGURANÇA

**Repositório PRIVADO:**
- ✅ Arquivo `.env` está INCLUÍDO no backup
- ✅ Todas chaves API estão salvas
- ⚠️ NUNCA tornar repositório público
- ⚠️ Se tornar público: deletar repo e revogar TODAS as chaves

**Boas práticas:**
1. Usar `/bk` frequentemente (não custa nada)
2. Testar `/cbk` antes de precisar (conhecer o sistema)
3. Sempre fazer `/bk` ANTES de restaurar versão antiga
4. Git mantém TUDO - nada é perdido permanentemente

### 🎯 Workflow Recomendado

```bash
# 1. Começar o dia - verificar status
git status

# 2. Trabalhar normalmente
# ... editar código ...

# 3. Backup frequente (a cada funcionalidade)
/bk

# 4. Antes de testar algo arriscado
/bk  # Backup de segurança

# 5. Se algo der errado
/cbk  # Ver backups e restaurar

# 6. Fim do dia
/bk  # Backup final
```

### 📊 Comandos Git Úteis

```bash
# Ver histórico
git log --oneline -10
git log --graph --oneline --all

# Ver mudanças
git status
git diff
git show HASH

# Comparar versões
git diff HASH1 HASH2
git diff HASH1 HASH2 --name-only  # Só nomes

# Ver arquivo sem restaurar
git show HASH:caminho/arquivo.py

# Informações do repo
git remote -v
git branch -a
```

---

**Última atualização:** 2025-11-02 (Sistema de backup automático adicionado)
**Versão:** 3.2 (65 templates + Sistema de backup /bk e /cbk)
