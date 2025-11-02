# 🤖 Claude Code Workspace

Workspace com ferramentas de IA pré-configuradas.

## 📁 Estrutura

```
ClaudeCode-Workspace/
├── agentes/            # Agentes especializados
├── crewai/             # Sistema multi-agentes colaborativos
├── docs/               # Documentação (APIs + Tools)
├── evolution-api-integration/  # Automação WhatsApp
├── n8n-mcp-project/    # n8n + Chatbot Corretor V4
├── tools/              # Scripts Python de IA
└── config/             # Configurações
```

---

## ⚡ Quick Start

### Chatbot WhatsApp Corretor V4
```bash
cd n8n-mcp-project
./INICIAR_BOT_V4.sh    # Iniciar
./PARAR_BOT_V4.sh      # Parar
```
**Recursos:** Bot IA (Claude Haiku 4.5) + Transcrição áudios (Whisper) + Visão imagens (GPT-4o) + Chatwoot

📖 **Docs:** `n8n-mcp-project/CHATBOT_V4_README.md`

---

## 🛠️ Ferramentas

**📚 ÍNDICE COMPLETO:** [`docs/tools/INDEX.md`](docs/tools/INDEX.md)

### 🎨 Geração de Imagens

| Ferramenta | Função | Docs |
|------------|--------|------|
| GPT-4o Image | Gera imagens com GPT-4o (portrait 2:3, variações, refinamento) | [`docs/tools/generate_image.md`](docs/tools/generate_image.md) |
| GPT-4o Batch | Geração em lote (paralelo) | Ver README atual |
| Nano Banana | Gemini 2.5 Flash (hiper-realismo, portrait 2:3) | [`docs/tools/generate_image_nanobanana.md`](docs/tools/generate_image_nanobanana.md) |
| Nano Banana Batch | Geração em lote (paralelo) | Ver README atual |
| Editor Nano Banana | Edita imagens com IA (múltiplas proporções) | Ver README atual |

---

### 🎤 Geração de Áudio

| Ferramenta | Função | Docs |
|------------|--------|------|
| ElevenLabs TTS | Text-to-Speech (70+ idiomas, 4 modelos) | Ver README atual |
| ElevenLabs Batch | Geração em lote (sequencial) | Ver README atual |

---

### 🎬 Geração de Vídeos

| Ferramenta | Função | Docs |
|------------|--------|------|
| Sora 2 | Gera vídeos ~15s (OpenAI via Kie.ai) | Ver README atual |
| Sora Batch | Geração em lote (paralelo, 2-5min) | Ver README atual |

---

### 📥 Extração de Conteúdo

| Ferramenta | Função | Docs |
|------------|--------|------|
| Transcrição Universal | YouTube, TikTok, Instagram, LinkedIn, X, Vimeo | [`docs/tools/transcribe_universal.md`](docs/tools/transcribe_universal.md) |
| Instagram Posts | Extrai imagens, legendas, metadados | Ver README atual |
| Instagram Reels | Transcreve áudio de Reels (Whisper) | Ver README atual |
| TikTok Transcrição | Transcreve áudio de vídeos (Whisper) | Ver README atual |
| Web Scraping | Extrai sites completos em Markdown | Ver README atual |
| Scraping Batch | Múltiplas URLs em sequência | Ver README atual |

---

### 🎵 TikTok (Scraping)

**Config:** `config/tiktok_config.py` | **Docs:** `docs/tools/tiktok_api23.md` | **Scripts:** `scripts/tiktok/README.md`

| Ação | Função | Script |
|------|--------|--------|
| Info de Usuário | Perfil completo (seguidores, bio, posts populares) | `scripts/tiktok/get_user_info.py` |
| Info de Vídeo | Detalhes de vídeo (views, likes, comentários) | `scripts/tiktok/get_video_info.py` |
| Buscar Conteúdo | Busca vídeos, usuários, conteúdo geral | `scripts/tiktok/search_content.py` |
| Trending | Vídeos, hashtags, músicas, criadores em alta | `scripts/tiktok/get_trending.py` |
| Analisar Hashtag | Info, posts e engajamento médio | `scripts/tiktok/analyze_hashtag.py` |

**Recursos:** 5 templates prontos | Filtros por país/período | Dados completos de engajamento

---

### 📱 Instagram (API)

**Config:** `config/instagram_config.py` | **Docs API:** `docs/instagram-api/INSTAGRAM_API_DOCUMENTATION.md`

| Ação | Função | Docs |
|------|--------|------|
| Post | Publica posts (imagem + legenda, auto-upload, PNG→JPEG) | [`docs/tools/publish_instagram_post.md`](docs/tools/publish_instagram_post.md) |
| Carrossel | Publica carrosséis (2-10 imagens) | Ver README atual |
| Reel | Publica Reels (vídeos até 90s, capa opcional) | [`docs/tools/publish_instagram_reel.md`](docs/tools/publish_instagram_reel.md) |
| Story | Publica Stories (imagem/vídeo, 24h) | Ver README atual |
| Comentários | Gerencia comentários (list, reply, hide, delete) | Ver README atual |
| Insights | Métricas de conta e mídia | Ver README atual |
| DMs | Gerencia mensagens diretas | Ver README atual |

**Recursos:** Auto-upload (Catbox.moe) | PNG→JPEG | Rate limit: 100 posts/24h

---

### 📢 Meta Ads (Marketing API)

**Config:** `config/meta_ads_config.py` | **Docs API:** `docs/meta-ads-api/META_ADS_API_DOCUMENTATION.md`

| Ação | Função | Docs |
|------|--------|------|
| Campanhas | Criar, listar, atualizar, deletar | [`docs/tools/meta_ads_campaigns.md`](docs/tools/meta_ads_campaigns.md) |
| Ad Sets | Gerenciar conjuntos de anúncios (targeting, budget) | Ver README atual |
| Anúncios | Gerenciar anúncios (criativos, status) | Ver README atual |
| Criativos | Criar criativos (imagem/vídeo/texto, CTAs) | Ver README atual |
| Insights | Métricas e relatórios (CPC, CPM, CTR, conversões) | Ver README atual |
| Upload Imagem | Upload de imagens para criativos | Ver README atual |
| Regional (Raio) | Campanha com targeting geográfico (lat/long + raio km) | [`docs/tools/meta_ads_regional_campaign.md`](docs/tools/meta_ads_regional_campaign.md) |

**Recursos:** Targeting por raio | Budgets (diário/total) | Otimizações | Breakdowns

---

### 💬 WhatsApp (Evolution API)

| Ferramenta | Função | Docs |
|------------|--------|------|
| WhatsApp Helper | Controle programático completo (mensagens, grupos, enquetes, localização) | [`docs/tools/whatsapp_helper.md`](docs/tools/whatsapp_helper.md) |

**Recursos:** Mensagens (texto, imagem, vídeo, doc, áudio) | Grupos (criar, membros, admins) | Enquetes | Localização | Status

**Docs:** `evolution-api-integration/README.md` | `evolution-api-integration/GUIA_RAPIDO.md`

---

### 🔍 Busca e Upload

| Ferramenta | Função | Docs |
|------------|--------|------|
| xAI Live Search | Busca em tempo real (Web/Twitter/News) via Grok-4-fast | [`docs/tools/xai_search.md`](docs/tools/xai_search.md) |
| Upload Nextcloud | Upload de arquivos com links públicos (exp. 24h) | Ver README atual |

**xAI:** 5 fontes max | ~$0.125/busca | Citações com links

**Docs:** `XAI_QUICK_START.md` | `tools/XAI_SEARCH_README.md`

---

## 🤖 Sistema de Agentes

| Tipo | Comando | Descrição |
|------|---------|-----------|
| **Agentes MD** | `"Ative o agente [nome] para [tarefa]"` | especificidade33 (conteúdos virais IG) |
| **OpenRouter** | `python3 tools/agent_openrouter.py <agente> "input" [--model MODEL]` | copywriter-vendas, analista-negocios |

**Modelos:** Claude Haiku/Sonnet 4.5, GPT-4o/5, Gemini 2.5 Pro, Grok 4, DeepSeek, GLM 4.6

📖 **Docs:** `agentes/openrouter/README.md`

---

## 🤝 CrewAI (Multi-Agentes)

```bash
cd crewai
python3.11 crews/copywriter_crew.py
```

**Recursos:** Hierarchical + Manager automático + Context + OpenRouter

📖 **Docs:** `crewai/README.md` | `crewai/INICIO-RAPIDO.md`

---

## 🔄 n8n-MCP (Automação)

**Instância:** https://n8n.loop9.com.br

```bash
cd n8n-mcp-project && claude-code
```

**Recursos:** 3000+ templates | Integração APIs/webhooks/DBs | Segurança (nunca deleta sem confirmação)

📖 **Docs:** `n8n-mcp-project/README.md` | `n8n-mcp-project/CLAUDE.md`

---

## ⏰ Agendamento (Cron)

```bash
crontab -e  # Configurar
crontab -l  # Ver agendamentos
```

**Formato:** `MIN HORA DIA MÊS DIA_SEMANA comando`

**Exemplo:**
```bash
# Todo dia 9h - Instagram post
0 9 * * * cd ~/Desktop/ClaudeCode-Workspace && python3 workflow_instagram.py
```

**Compatível:** Imagens, áudio, vídeo, social media, scraping, Meta Ads, agentes IA

📖 **Docs:** `n8n-mcp-project/AGENDAMENTO_WHATSAPP.md`

---

## 🔧 Manutenção

**Setup:** `bash setup.sh` (primeira vez)

**Adicionar ferramenta:**
1. Coloque em `tools/`
2. Adicione dependências em `requirements.txt`
3. Rode `bash setup.sh`

**Troubleshooting:**
- Module not found: `pip3 install --user requests`
- Script não executa: `chmod +x tools/*.py *.sh`

---

**Docs externas:** [Kie.ai](https://docs.kie.ai) | [Claude Code](https://claude.com/claude-code)
