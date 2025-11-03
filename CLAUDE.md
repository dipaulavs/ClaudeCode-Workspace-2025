# 🤖 Claude Code - Workspace Configuration

**Auto-load:** Este arquivo é carregado automaticamente e SOBRESCREVE comportamentos padrão do Claude Code.

---

## 📝 REGRAS DE EDIÇÃO DESTE ARQUIVO (OBRIGATÓRIO)

### ⚠️ ANTES DE ADICIONAR/EDITAR CONTEÚDO NO CLAUDE.md

**PRINCÍPIO:** CLAUDE.md é um **índice navegável**, NÃO uma documentação completa.

### ✅ O QUE INCLUIR (permitido):

1. **MAPA DE AÇÕES** → Linha única por ação (template path + doc)
2. **Regras de comportamento** → Instruções críticas de como Claude Code deve agir
3. **Regras de decisão** → Fluxogramas simples (3-5 linhas por regra)
4. **Skills tabela** → Nome + quando usar + descrição (1 linha por skill)
5. **Quick Actions** → Comandos essenciais (formato resumido)
6. **Tabelas de referência** → Formato compacto (sem detalhes inline)

### ❌ O QUE NÃO INCLUIR (proibido):

1. ❌ **Documentação inline detalhada** → Vai para README específico
2. ❌ **Exemplos de código longos** → Vai para EXAMPLES.md da skill/template
3. ❌ **Seções duplicadas** → Se está no MAPA, não repetir em "Categorias"
4. ❌ **Tutoriais passo a passo** → Vai para docs/ ou script README
5. ❌ **Descrições longas** → Máximo 1-2 linhas, linkar para doc completa
6. ❌ **Comandos git detalhados** → Linkar para .claude/commands/

### 🎯 FORMATO OBRIGATÓRIO ao adicionar novo recurso:

```markdown
## 📍 MAPA DE AÇÕES
| **[Ação]** | `caminho/template.py` | `caminho/README.md` |
```

**Se precisar mais detalhes:**
- Criar/atualizar README na pasta do recurso
- Criar EXAMPLES.md se for skill
- NUNCA escrever mais de 3 linhas no CLAUDE.md

### 📏 LIMITES RÍGIDOS:

- **MAPA DE AÇÕES:** 1 linha por entrada (template | doc)
- **Regras comportamento:** Máx 10 linhas por regra
- **Skills:** Só tabela (sem exemplos inline)
- **Backup/Docs:** Máx 5 linhas + link para arquivo
- **Arquivo total:** Máx 600 linhas

### 🔍 CHECKLIST antes de salvar edições:

- [ ] Removi duplicações?
- [ ] Usei links para docs detalhadas?
- [ ] Mantive formato tabela compacto?
- [ ] Informação cabe em 1-2 linhas?
- [ ] Se não cabe → criei README separado?

---

## 🚨 REGRAS DE COMPORTAMENTO (PRIORIDADE MÁXIMA)

### 0️⃣ Modo Conciso (Comunicação)

**SEMPRE usar Modo Conciso nas respostas:**

**Estrutura:**
1. O que vou fazer (1 linha)
2. Executo
3. Resultado (1-2 linhas)

**Proibido:**
- ❌ Repetir o que usuário pediu
- ❌ Explicações longas desnecessárias
- ❌ Contexto óbvio

**Exceções:**
- ✅ Erros críticos (explicar o problema)
- ✅ Usuário pede detalhes explicitamente
- ✅ Decisões complexas que precisam clarificação

---

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
- **Estudo de vídeos YouTube** (workflow automático - ver seção 6️⃣)

**Por quê:** Garante alinhamento com raciocínio do usuário e evita retrabalho.

---

### 2️⃣ Preferência por Templates

**SEMPRE verificar se existe template antes de criar código novo:**

| Categoria | Localização | Total |
|-----------|-------------|-------|
| WhatsApp | `scripts/whatsapp/` | 22 templates |
| Instagram Publicação | `scripts/instagram/` | 6 templates |
| Instagram Scraper | `scripts/instagram-scraper/` | 5 templates |
| Meta Ads | `scripts/meta-ads/` | 4 templates |
| Nextcloud | `scripts/nextcloud/` | 2 templates |
| Obsidian | `scripts/obsidian/` | 6 templates |
| Imagens | `scripts/image-generation/` | 4 templates |
| Vídeos | `scripts/video-generation/` | 2 templates |
| Áudio | `scripts/audio-generation/` | 2 templates |
| Extração | `scripts/extraction/` | 4 templates |
| Busca (xAI) | `scripts/search/` | 3 templates |
| Twitter/X | `scripts/twitter/` | 5 templates |
| TikTok | `scripts/tiktok/` | 5 templates |
| Google Maps | `scripts/scraping/` | 3 templates |
| Scheduling | `scripts/scheduling/` | 1 template |
| Canva MCP | `scripts/canva/` | 1 script + MCP |
| Orshot Design | `scripts/orshot/` | 3 templates |

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
- **Templates (scripts/)** → Adicionar em `📍 MAPA DE AÇÕES` (1 linha)
- **Ferramentas (tools/)** → Adicionar em `🛠️ FERRAMENTAS DISPONÍVEIS` (1 linha)
- **Novos projetos** → Adicionar em `📁 ESTRUTURA DO WORKSPACE` (1 linha)

**Formato de registro:**
```markdown
| **[NOVA AÇÃO]** | `scripts/[categoria]/[nome].py` | `scripts/[categoria]/README.md` |
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
  • CLAUDE.md (registrado no MAPA DE AÇÕES)

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

### 6️⃣ Workflow Automático: Estudar Vídeo YouTube

**GATILHO:** Usuário diz "Estuda esse vídeo: [URL]" ou fornece URL YouTube

**MÉTODO:** Claude Code Skill `estudar-video` (model-invoked, totalmente automática)

**WORKFLOW:** Transcrever (Whisper) → Analisar (Claude) → Classificar tipo → Salvar Obsidian

**Custo:** ~$0.006/vídeo | **Tempo:** ~3min | **Regras:** ❌ Sem confirmação
**Skill:** `.claude/skills/estudar-video/SKILL.md` | **Doc:** `09 - YouTube Knowledge/README.md`

---

### 7️⃣ WhatsApp Mídia: SEMPRE URL Pública

**REGRA ABSOLUTA:** Evolution API aceita APENAS URLs públicas.

**SEMPRE:**
- ✅ Usar `--url` com link público (http:// ou https://)
- ✅ URLs vêm nas respostas das APIs (Nano Banana, GPT-4o, Sora)

**NUNCA:**
- ❌ `--file` foi REMOVIDO do script (não existe mais)
- ❌ Arquivos locais não funcionam
- ❌ Base64 não funciona

**Workflow correto:** Gerar mídia → Pegar URL da resposta → `send_media.py --url [URL]`

---

### 8️⃣ Auto-Correção de Scripts (OBRIGATÓRIO)

**GATILHO:** Script executado retorna erro → Corrijo o erro → Script funciona

**SEMPRE após corrigir erro:**
1. ✅ **Atualizar o script** para prevenir o erro no futuro
2. ✅ **Melhorar validação** (adicionar checks, avisos)
3. ✅ **Remover informações confusas** (código obsoleto, docs enganosas, exemplos errados)
4. ✅ **Atualizar documentação** (README, docstrings, comentários)

**Objetivo:** Erro só acontece UMA vez. Scripts melhoram continuamente.

**Exemplo send_media.py:**
- ❌ Problema: Script tinha `--file` mas Evolution API rejeita arquivos locais
- ✅ Fix: Removi `--file` do código + removi exemplos de `--file` do README + atualizei docstring
- 🎯 Resultado: IA nunca mais tenta usar `--file`

---

## 📍 MAPA DE AÇÕES (Índice Rápido)

| Quando usuário pedir... | Use isto | Doc completa |
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
| **Estudar vídeo YouTube** | WORKFLOW AUTOMÁTICO (ver seção 6️⃣) | `09 - YouTube Knowledge/README.md` |
| **AI News diário** | `scripts/scheduling/daily_ai_news.py` (Python 3.11) | `scripts/scheduling/README.md` |
| **Canva via MCP** | Claude.ai web (OAuth) | `scripts/canva/README.md` |
| **Gerar design/imagem** | `scripts/orshot/generate_image.py` | `scripts/orshot/README.md` |
| **Designs em lote** | `scripts/orshot/batch_generate.py` | `scripts/orshot/README.md` |

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

**Localização:** `.claude/skills/` | **Doc oficial:** https://docs.claude.com/en/docs/claude-code/skills.md

Skills são capacidades modulares model-invoked (Claude decide quando usar automaticamente).

### Skills Disponíveis (9 Skills)

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **idea-validator** | Validar ideias antes de construir | Analisa saturação de mercado, viabilidade, demanda real, monetização. Dá feedback brutalmente honesto. |
| **launch-planner** | Planejar lançamento de MVP | Transforma ideias validadas em PRDs completos com roadmap, schema de DB, e escopo MVP (2-4 semanas). |
| **product-designer** | Design de UI/UX | Elimina o "visual de IA" (gradientes azul/roxo). Cria interfaces profissionais com Tailwind + shadcn/ui. |
| **marketing-writer** | Criar conteúdo de marketing | Escreve landing pages, tweets, Product Hunt, emails de lançamento. Tom claro e focado em benefícios. |
| **roadmap-builder** | Priorizar features | Atua como PM: decide o que construir (e o que NÃO construir). Previne feature creep. |
| **adaptive-mentor** | Explicar/implementar qualquer conceito | Mentor especialista que se adapta ao assunto. Explica ELI5 + analogias + diagramas. Cria plano executável simplificado. |
| **estudar-video** | Estudar vídeos do YouTube | Workflow automático: transcreve (Whisper) → analisa com IA → classifica tipo → extrai insights → salva no Obsidian. |
| **orshot-design** | Gerar designs/imagens | Automação de designs profissionais usando Orshot API. Posts sociais, certificados, OG images. $0.01/render. |
| **skill-creator** | Criar novas Skills | Meta-skill que cria outras Skills automaticamente. Gera estrutura multi-arquivo Progressive Disclosure. |

### Estrutura de uma Skill (Progressive Disclosure)

```
.claude/skills/nome-da-skill/
├── SKILL.md               # Instruções principais (30-60 linhas, máx 80)
├── REFERENCE.md           # Documentação técnica detalhada
├── EXAMPLES.md            # Casos de uso reais (mínimo 2)
└── TROUBLESHOOTING.md     # Guia de erros comuns (mínimo 2)
```

**Criar nova Skill:** "Crie uma skill para [propósito]" ou `python3 scripts/claude-skills/create_skill.py nome-da-skill`
**Doc:** `scripts/claude-skills/README.md` | **Exemplos:** Ver `.claude/skills/*/EXAMPLES.md`

---

## ⚡ Quick Actions

### Chatbot WhatsApp
```bash
bot         # Iniciar
botstop     # Parar
# Logs: whatsapp-chatbot/logs/chatbot_v4.log
```

### Backup Git
```bash
/bk         # Backup automático (add + commit + push)
/cbk        # Listar e restaurar backups
```
**Repo:** https://github.com/dipaulavs/ClaudeCode-Workspace-2025 (PRIVADO)
**Doc completa:** `.claude/commands/bk.md` e `.claude/commands/cbk.md`

### Geração de Conteúdo
```bash
# Imagem (Nano Banana)
python3 scripts/image-generation/generate_nanobanana.py "prompt"

# Múltiplas imagens (BATCH obrigatório)
python3 scripts/image-generation/batch_generate.py --api nanobanana "prompt1" "prompt2"

# Vídeo (Sora portrait)
python3 scripts/video-generation/generate_sora.py "prompt"

# Áudio (ElevenLabs voz Michele)
python3 scripts/audio-generation/generate_elevenlabs.py "texto"
```

### WhatsApp/Instagram
```bash
# WhatsApp
python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Olá!"

# Instagram
python3 scripts/instagram/publish_post.py --image "foto.jpg" --caption "Legenda"
```

---

## 🛠️ FERRAMENTAS DISPONÍVEIS

**📚 Índice completo:** `docs/tools/INDEX.md` | **Total:** 65+ templates | 40+ ferramentas

| Categoria | Ferramentas | Docs |
|-----------|-------------|------|
| **Geração Imagem** | GPT-4o, Nano Banana, Batch, Edição (URLs públicas) | `scripts/image-generation/README.md` |
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

---

## 📁 ESTRUTURA DO WORKSPACE

```
ClaudeCode-Workspace/
├── 📄 CLAUDE.md                 # Config auto-load (este arquivo)
├── 📄 README.md                 # Índice geral
├── 📄 requirements.txt          # Dependências Python
│
├── 📁 .claude/
│   ├── commands/                # /bk, /cbk
│   └── skills/                  # 9 Claude Skills (model-invoked)
│
├── 📁 scripts/                  # 65+ Templates prontos
│   ├── whatsapp/                # 22 templates
│   ├── instagram/               # 6 templates
│   ├── image-generation/        # 5 templates
│   ├── video-generation/        # 2 templates
│   ├── audio-generation/        # 2 templates
│   └── [outras categorias]/
│
├── 📁 tools/                    # 40+ Ferramentas low-level
├── 📁 config/                   # Configurações APIs
├── 📁 docs/                     # Documentação organizada
├── 📁 whatsapp-chatbot/         # Bot V4 (produção)
├── 📁 scheduling-system/        # Agendamento WhatsApp
└── [outros projetos]/
```

---

## 💡 DICAS IMPORTANTES

### Geração de Múltiplos Itens
🚨 **REGRA CRÍTICA:** 2+ itens = SEMPRE usar batch
- Imagens: `batch_generate.py --api nanobanana`
- Vídeos: `batch_generate.py`
- Áudios: `batch_generate.py`

### Modelos Padrão
- **Imagens:** Nano Banana (Gemini 2.5 Flash)
- **Vídeos:** Sora 2 portrait (Stories/Reels)
- **Áudio:** ElevenLabs voz Michele

### Outros
- **Busca xAI:** Requer Python 3.11+ (usar `python3.11`)
- **WhatsApp:** Formato DDI+DDD+Número (ex: 5531980160822)
- **Instagram Scraping:** Usar `--limit` ($2.30/1000 itens)
- **Obsidian:** Datas em formato brasileiro DD/MM/YYYY

---

## 📖 DOCUMENTAÇÕES COMPLETAS

| Recurso | Localização |
|---------|-------------|
| **README Principal** | `README.md` |
| **Ferramentas (40+)** | `docs/tools/INDEX.md` |
| **Templates (65+)** | Ver README em `scripts/[categoria]/` |
| **Obsidian** | `docs/tools/obsidian_integration.md` |
| **Chatbot WhatsApp** | `whatsapp-chatbot/README.md` |
| **Meta Ads API** | `docs/meta-ads-api/META_ADS_API_DOCUMENTATION.md` |
| **Instagram API** | `docs/instagram-api/INSTAGRAM_API_DOCUMENTATION.md` |

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

**Última atualização:** 2025-11-02 (Otimização estrutural - 600 linhas)
**Versão:** 4.0 (Otimizado com regras de edição absolutas)
