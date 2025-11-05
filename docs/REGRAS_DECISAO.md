# 🔍 Regras de Decisão - Fluxogramas

Fluxogramas de decisão para escolher o template/ferramenta correto.

---

## 🖼️ Imagens

```
Usuário pede quantas imagens?
├─ 1 imagem → generate_nanobanana.py
└─ 2+ imagens → batch_generate.py --api nanobanana (OBRIGATÓRIO)
```

**Modelos disponíveis:**
- Nano Banana (Gemini 2.5 Flash) - **PADRÃO**
- GPT-4o

**Docs:** `scripts/image-generation/README.md`

---

## 🎬 Vídeos

```
Usuário pede quantos vídeos?
├─ 1 vídeo → generate_sora.py
└─ 2+ vídeos → batch_generate.py (OBRIGATÓRIO)
```

**Proporções:**
- Portrait (9:16) - **PADRÃO** (Stories/Reels)
- Landscape (16:9)
- Square (1:1)

**Docs:** `scripts/video-generation/README.md`

---

## 🎧 Áudio

```
Usuário pede quantos áudios?
├─ 1 áudio → generate_elevenlabs.py
└─ 2+ áudios → batch_generate.py (OBRIGATÓRIO)
```

**Vozes:**
- Michele (voz feminina) - **PADRÃO**
- Outras vozes clonadas disponíveis

**Docs:** `scripts/audio-generation/README.md`

---

## 📸 Instagram

```
Usuário quer publicar ou extrair?
├─ Publicar → scripts/instagram/publish_*.py
│   ├─ Post simples → publish_post.py
│   ├─ Carrossel → publish_carousel.py
│   ├─ Reel → publish_reel.py
│   └─ Story → publish_story.py
│
└─ Extrair/Scrape → scripts/instagram-scraper/scrape_*.py
    ├─ Perfil → scrape_profile.py
    ├─ Hashtag → scrape_hashtag.py
    ├─ Posts → scrape_posts.py
    └─ Comentários → scrape_comments.py
```

**Docs:**
- Publicação: `scripts/instagram/README.md`
- Scraper: `scripts/instagram-scraper/README.md`

---

## 📍 Google Maps

```
Quantas buscas?
├─ 1 busca simples → google_maps_basic.py
├─ 1 busca com filtros → google_maps_advanced.py
└─ 2+ buscas → google_maps_batch.py (OBRIGATÓRIO)
```

**Filtros disponíveis:**
- Raio (km)
- Rating mínimo
- Tipo de lugar
- Horário de funcionamento

**Docs:** `scripts/scraping/README.md`

---

## 🌐 Busca (xAI Search)

```
Buscar onde?
├─ Web/Documentação → xai_web.py (Python 3.11)
├─ Twitter/X → xai_twitter.py (Python 3.11)
└─ Notícias → xai_news.py (Python 3.11)
```

**⚠️ Requer:** Python 3.11+ (usar `python3.11`)

**Docs:** `scripts/search/README.md`

---

## 📝 Obsidian (Salvar/Anotar)

```
Usuário quer salvar algo no Obsidian?
└─ SEMPRE → Skill obsidian-organizer (automática)
   ├─ É tarefa/ação? → 📋 Tarefas/
   ├─ É vídeo YouTube? → 📺 Vídeos/
   └─ É ideia/nota? → 💡 Anotações/
```

**⚠️ NUNCA:**
- Usar scripts Python antigos (quick_note.py, etc) - OBSOLETOS
- Criar arquivos diretamente com Write tool
- Usar estrutura antiga ("00 - Inbox", etc)

**Docs:** `.claude/skills/obsidian-organizer/SKILL.md`

---

## 📤 Upload Nextcloud

```
De onde vem o arquivo?
├─ ~/Pictures/upload/ → upload_rapido.py --from-local (PADRÃO)
├─ ~/Downloads/ → upload_from_downloads.py
└─ Caminho personalizado → upload_to_nextcloud.py
```

**Workflow padrão:**
1. Usuário joga imagens em `~/Pictures/upload/`
2. Dizer "suba as imagens" ou "upload rápido"
3. `upload_rapido.py --from-local` executa automaticamente
4. Links permanentes retornados
5. Arquivos locais deletados

**Docs:** `scripts/nextcloud/README.md`

---

## 📱 WhatsApp

```
Tipo de conteúdo?
├─ Texto → send_message.py
├─ Mídia (imagem/vídeo/áudio) → send_media.py --url [URL_PUBLICA]
├─ Criar grupo → create_group.py
└─ Agendar → scheduling-system/schedule_whatsapp.py
```

**⚠️ Mídia:** SEMPRE usar `--url` (URLs públicas). NUNCA `--file` (não existe mais).

**Docs:** `scripts/whatsapp/README.md`

---

## 🎨 Design

```
Tipo de design?
├─ Clonar site existente → SKILL website-cloner
├─ Imagem/post social → scripts/orshot/generate_image.py
├─ 2+ designs → scripts/orshot/batch_generate.py
└─ Apresentação interativa → scripts/visual-explainer/generate.py
```

**Orshot:** $0.01/render | Designs profissionais automatizados
**Website Cloner:** 100% fidelidade CSS (não 60-70%)

**Docs:**
- Orshot: `scripts/orshot/README.md`
- Visual Explainer: `scripts/visual-explainer/README.md`
- Website Cloner: `.claude/skills/website-cloner/SKILL.md`

---

## 🎥 YouTube

```
Objetivo?
├─ Estudar/resumir vídeo → WORKFLOW AUTOMÁTICO (estudar-video)
├─ Criar vídeo educativo → SKILL youtube-educator
│   ├─ Roteiro + apresentação + thumbnails
│   └─ Workflow completo FASE 1 (pré-gravação)
│
└─ Só thumbnails → SKILL youtube-thumbnailv2
    └─ 5 variações (estilo dourado/azul-ciano)
```

**Estudar vídeo:**
- Transcrição (Whisper) → Análise (Claude) → Obsidian (📺 Vídeos/)
- Custo: ~$0.006/vídeo | Tempo: ~3min
- SEMPRE executar ao receber link YouTube

**Docs:**
- Estudar: `.claude/skills/estudar-video/SKILL.md`
- Educator: `.claude/skills/youtube-educator/SKILL.md`
- Thumbnails: `.claude/skills/youtube-thumbnailv2/SKILL.md`

---

## 🤖 Chatbots WhatsApp

```
Ação?
├─ Adicionar imóvel → Workflow automático (whatsapp-chatbot)
│   ├─ Upload fotos (Nextcloud)
│   ├─ Criar estrutura (base.txt, faq.txt, etc)
│   └─ links.json gerado
│
├─ Adicionar carro → Workflow automático (whatsapp-chatbot-carros)
│   ├─ Upload fotos (Nextcloud)
│   ├─ Preencher .txt (base, detalhes, faq, historico, financiamento)
│   └─ links.json gerado
│
└─ Criar novo chatbot → 3 opções
    ├─ Opção A: Mesma conta Chatwoot, nova inbox (2-3 clientes)
    ├─ Opção B: Conta Chatwoot separada (4-10 clientes)
    └─ Opção C: Multi-tenant framework (10+ clientes)
```

**Docs:**
- Imóveis: `whatsapp-chatbot/FRAMEWORK_COMPLETO_README.md`
- Automaia: `whatsapp-chatbot-carros/README.md`
- Integração: `whatsapp-chatbot/INTEGRACAO_FRAMEWORK.md`

---

## 💡 Propostas & Orçamentos

```
Tipo de documento?
├─ Orçamento técnico → SKILL orcamento-profissional
│   ├─ Analisa recursos disponíveis
│   ├─ Calcula preço baseado em VALOR
│   ├─ Gera apresentação HTML profissional
│   └─ ROI matemático (3 cenários)
│
└─ Proposta comercial → templates/proposta-orcamento/
    └─ Template HTML interativo (Dark mode, animações)
```

**Docs:**
- Skill: `.claude/skills/orcamento-profissional/SKILL.md`
- Template: `templates/proposta-orcamento/README.md`

---

## 🚨 Regras Críticas

### 1. Batch Obrigatório (2+ itens)
```
Gerar múltiplos?
└─ SIM → SEMPRE usar batch_generate.py (OBRIGATÓRIO)
   ├─ Imagens: --api nanobanana
   ├─ Vídeos: (padrão)
   └─ Áudios: (padrão)
```

### 2. Skills Prioritárias
```
Usuário menciona ideia/dúvida genérica?
└─ SEMPRE → adaptive-mentor PRIMEIRO
   └─ Skill se adapta e delega para outras se necessário
```

### 3. Obsidian
```
Salvar/anotar no Obsidian?
└─ SEMPRE → obsidian-organizer (NUNCA scripts diretos)
```

### 4. Links YouTube
```
Recebeu link YouTube?
└─ SEMPRE → python3 scripts/extraction/transcribe_video.py "URL"
   └─ NUNCA WebFetch (não funciona)
```

---

**Última atualização:** 2025-11-05
