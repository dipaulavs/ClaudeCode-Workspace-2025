# 📚 Índice de Ferramentas

Documentação completa de todas as ferramentas do workspace.

## 🎨 Geração de Imagens

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **GPT-4o Image** | Gera imagens com GPT-4o (portrait 2:3) | [generate_image.md](generate_image.md) |
| **GPT-4o Batch** | Geração em lote (paralelo) | [generate_image_batch_gpt.md](generate_image_batch_gpt.md) |
| **Nano Banana** | Gemini 2.5 Flash (hiper-realismo) | [generate_image_nanobanana.md](generate_image_nanobanana.md) |
| **Nano Banana Batch** | Geração em lote (paralelo) | [generate_image_batch.md](generate_image_batch.md) |
| **Editor Nano Banana** | Edita imagens com IA | [edit_image_nanobanana.md](edit_image_nanobanana.md) |
| **DALL-E 3 (Kie.ai)** | Gera imagens com DALL-E 3 via Kie.ai | [generate_image_ai.md](generate_image_ai.md) |

### 📋 Templates de Geração de Imagens (Scripts Prontos)

Templates simplificados para uso rápido (wrappers otimizados).

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Generate GPT-4o** | Gerar imagens com GPT-4o (wrapper simplificado) | `scripts/image-generation/generate_gpt4o.py` |
| **Generate Nano Banana** | Gerar imagens com Gemini 2.5 Flash (wrapper simplificado) | `scripts/image-generation/generate_nanobanana.py` |
| **Generate DALL-E 3** | Gerar imagens com DALL-E 3 (wrapper simplificado) | `scripts/image-generation/generate_dalle3.py` |
| **Batch Generate** | Geração em lote multi-modelo (GPT-4o + Nano Banana) | `scripts/image-generation/batch_generate.py` |
| **Edit Nano Banana** | Edição de imagens com Nano Banana (wrapper simplificado) | `scripts/image-generation/edit_nanobanana.py` |

**Documentação completa:** [scripts/image-generation/README.md](../../scripts/image-generation/README.md)

## 🎤 Geração de Áudio

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **ElevenLabs TTS** | Text-to-Speech (70+ idiomas) | [generate_audio_elevenlabs.md](generate_audio_elevenlabs.md) ⏳ |
| **ElevenLabs Batch** | Geração em lote (sequencial) | [generate_audio_batch_elevenlabs.md](generate_audio_batch_elevenlabs.md) ⏳ |

## 🎬 Geração de Vídeos

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **Sora 2** | Gera vídeos ~15s (OpenAI) | [generate_video_sora.md](generate_video_sora.md) ⏳ |
| **Sora Batch** | Geração em lote (paralelo) | [generate_video_batch_sora.md](generate_video_batch_sora.md) ⏳ |

## 📥 Extração de Conteúdo

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **Transcrição Universal** | YouTube, TikTok, IG, LinkedIn, X, Vimeo | [transcribe_universal.md](transcribe_universal.md) |
| **Instagram Posts** | Extrai imagens, legendas, metadados | [extract_instagram.md](extract_instagram.md) ⏳ |
| **Instagram Reels** | Transcreve áudio de Reels | [transcribe_instagram_reels.md](transcribe_instagram_reels.md) ⏳ |
| **TikTok API23** | API completa TikTok (38 endpoints) - User, Search, Posts, Trending, Ads, Hashtags | [tiktok_api23.md](tiktok_api23.md) |
| **Web Scraping** | Extrai sites completos em Markdown | [apify_scraper.md](apify_scraper.md) ⏳ |
| **Scraping Batch** | Scraping múltiplas URLs | [apify_scraper_batch.md](apify_scraper_batch.md) ⏳ |

### 📋 Templates TikTok (Scripts Prontos)

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Get User Info** | Obter info de usuário (stats, posts, seguidores) | `scripts/tiktok/get_user_info.py` |
| **Get Video Info** | Obter info de vídeo (detalhes, comentários) | `scripts/tiktok/get_video_info.py` |
| **Search Content** | Buscar vídeos, usuários, conteúdo geral | `scripts/tiktok/search_content.py` |
| **Get Trending** | Monitorar trending (vídeos, hashtags, músicas, criadores) | `scripts/tiktok/get_trending.py` |
| **Analyze Hashtag** | Analisar hashtag (info + posts + engajamento médio) | `scripts/tiktok/analyze_hashtag.py` |

**Docs completa:** `scripts/tiktok/README.md` + `docs/tools/tiktok_api23.md`

## 📱 Instagram (API - Publicação)

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **Post** | Publica posts (imagem + legenda) | [publish_instagram_post.md](publish_instagram_post.md) |
| **Carrossel** | Publica carrosséis (2-10 imagens) | [publish_instagram_carousel.md](publish_instagram_carousel.md) ⏳ |
| **Reel** | Publica Reels (vídeos até 90s) | [publish_instagram_reel.md](publish_instagram_reel.md) |
| **Story** | Publica Stories (imagem/vídeo 24h) | [publish_instagram_story.md](publish_instagram_story.md) ⏳ |
| **Comentários** | Gerencia comentários (list/reply/hide/delete) | [manage_instagram_comments.md](manage_instagram_comments.md) ⏳ |
| **Insights** | Métricas de conta e mídia | [get_instagram_insights.md](get_instagram_insights.md) ⏳ |
| **DMs** | Gerencia mensagens diretas | [manage_instagram_dms.md](manage_instagram_dms.md) ⏳ |

### 📋 Templates Instagram (Scripts Prontos)

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Publish Post** | Template para publicar posts via API | `scripts/instagram/publish_post.py` |
| **Publish Carousel** | Template para publicar carrosséis via API | `scripts/instagram/publish_carousel.py` |
| **Publish Reel** | Template para publicar Reels via API | `scripts/instagram/publish_reel.py` |
| **Publish Story** | Template para publicar Stories via API | `scripts/instagram/publish_story.py` |
| **Get Insights** | Template para obter métricas via API | `scripts/instagram/get_insights.py` |
| **Manage Comments** | Template para gerenciar comentários via API | `scripts/instagram/manage_comments.py` |

**Docs completa:** `scripts/instagram/README.md`

## 📸 Instagram Scraper (Apify - Extração de Dados)

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **Instagram Scraper** | Extrai posts, comentários, perfis, hashtags, localizações | [apify_instagram.md](apify_instagram.md) |

### 📋 Templates Instagram Scraper (Scripts Prontos)

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Scrape User Posts** | Extrair posts de perfil (imagens/vídeos/carrosseis) | `scripts/instagram-scraper/scrape_user_posts.py` |
| **Scrape Hashtag Posts** | Extrair posts de hashtag | `scripts/instagram-scraper/scrape_hashtag_posts.py` |
| **Scrape Post Comments** | Extrair comentários de post específico | `scripts/instagram-scraper/scrape_post_comments.py` |
| **Scrape User Profile** | Extrair perfil completo (seguidores, bio, posts) | `scripts/instagram-scraper/scrape_user_profile.py` |
| **Scrape Place Posts** | Extrair posts de localização | `scripts/instagram-scraper/scrape_place_posts.py` |

**Docs completa:** `scripts/instagram-scraper/README.md` + `docs/tools/apify_instagram.md`

**Pricing:** $2.30/1000 itens (~$0.0023/item)

## 📢 Meta Ads (Marketing API)

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **Campanhas** | Criar, listar, atualizar, deletar | [meta_ads_campaigns.md](meta_ads_campaigns.md) |
| **Ad Sets** | Gerenciar conjuntos de anúncios | [meta_ads_adsets.md](meta_ads_adsets.md) ⏳ |
| **Anúncios** | Gerenciar anúncios | [meta_ads_ads.md](meta_ads_ads.md) ⏳ |
| **Criativos** | Criar criativos (imagem/vídeo/texto) | [meta_ads_creatives.md](meta_ads_creatives.md) ⏳ |
| **Insights** | Métricas e relatórios | [meta_ads_insights.md](meta_ads_insights.md) ⏳ |
| **Upload Imagem** | Upload de imagens para criativos | [meta_ads_upload_image.md](meta_ads_upload_image.md) ⏳ |
| **Regional (Raio)** | Campanha com targeting geográfico | [meta_ads_regional_campaign.md](meta_ads_regional_campaign.md) |

## 💬 WhatsApp

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **WhatsApp Helper** | Controle programático completo via Evolution API | [whatsapp_helper.md](whatsapp_helper.md) |

## 🔍 Busca, Scraping e Upload

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **xAI Live Search** | Busca em tempo real (Web/Twitter/News) via Grok | [xai_search.md](xai_search.md) |
| **Google Maps Scraper** | Extração completa de dados de empresas do Google Maps | [apify_google_maps.md](apify_google_maps.md) |
| **Upload Nextcloud** | Upload de arquivos com links públicos (temporários ou permanentes) | [cloud.md](cloud.md) |

### 📋 Templates Google Maps (Scripts Prontos)

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Basic Search** | Busca simples por termo + localização | `scripts/scraping/google_maps_basic.py` |
| **Advanced Search** | Busca com filtros, categorias e geolocalização customizada | `scripts/scraping/google_maps_advanced.py` |
| **Batch Search** | Múltiplas buscas em paralelo (2+ locais/termos) | `scripts/scraping/google_maps_batch.py` |

**Docs completa:** `scripts/scraping/README.md` + `docs/tools/apify_google_maps.md`

## 🐦 Twitter/X Scraping (Apify)

| Ferramenta | Descrição | Docs |
|------------|-----------|------|
| **Apify Twitter Scraper** | Scraping completo de tweets, perfis, conversas e listas | [apify_twitter.md](apify_twitter.md) |

### 📋 Templates Twitter (Scripts Prontos)

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Search Twitter** | Busca avançada de tweets com filtros | `scripts/twitter/search_twitter.py` |
| **Scrape Profile** | Scraping de perfis (histórico de tweets) | `scripts/twitter/scrape_profile.py` |
| **Scrape Tweets** | Scraping de tweets específicos por URL | `scripts/twitter/scrape_tweets.py` |
| **Scrape Replies** | Scraping de replies/conversas | `scripts/twitter/scrape_replies.py` |
| **Batch Twitter** | Batch de múltiplos perfis/termos | `scripts/twitter/batch_twitter.py` |

**Docs completa:** `scripts/twitter/README.md` + `docs/tools/apify_twitter.md`

### 📋 Templates Nextcloud (Scripts Prontos)

| Template | Descrição | Localização |
|----------|-----------|-------------|
| **Upload Manual** | Upload de qualquer arquivo com caminho completo | `scripts/nextcloud/upload_to_nextcloud.py` |
| **Upload Downloads** | Upload rápido da pasta Downloads (mais recente ou busca por nome) | `scripts/nextcloud/upload_from_downloads.py` |

**Docs completa:** `scripts/nextcloud/README.md` + `docs/tools/cloud.md`

---

**Legenda:**
- ✅ Documentação completa
- ⏳ Documentação em criação (usar README principal temporariamente)

---

**Última atualização:** 2025-11-02 (Adicionado Twitter Scraping: 5 templates + docs completa)
