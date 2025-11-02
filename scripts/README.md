# 📦 Scripts Templates - Quick Actions

Sistema organizado de **scripts templates prontos** para acelerar a execução de tarefas comuns.

Estes scripts são **parametrizados** e podem ser executados diretamente via linha de comando, sem necessidade de criar código novo a cada vez.

---

## 🎯 Objetivo

Ao invés de criar scripts novos toda vez que precisar executar uma ação, use estes templates prontos! Isso:

✅ **Acelera** a execução de tarefas
✅ **Padroniza** operações comuns
✅ **Reduz** erros de implementação
✅ **Facilita** o trabalho do agente Claude Code

---

## 📁 Estrutura

```
scripts/
├── README.md                 # Esta documentação
│
├── whatsapp/                 # Templates WhatsApp (Evolution API)
│   ├── README.md
│   ├── send_message.py       # ✅ Enviar mensagem
│   ├── send_media.py         # ✅ Enviar mídia (imagem/vídeo/doc)
│   ├── create_group.py       # ✅ Criar grupo
│   └── send_poll.py          # ✅ Enviar enquete
│
├── image-generation/         # Templates Geração de Imagens IA
│   ├── README.md
│   ├── generate_gpt4o.py     # ✅ Gerar imagem GPT-4o
│   ├── generate_nanobanana.py # ✅ Gerar imagem Nano Banana
│   ├── generate_dalle3.py    # ✅ Gerar imagem DALL-E 3
│   ├── batch_generate.py     # ✅ Geração em lote
│   └── edit_nanobanana.py    # ✅ Editar imagem
│
├── instagram/                # Templates Instagram (Graph API)
│   ├── README.md
│   ├── publish_post.py       # ✅ Publicar post
│   ├── publish_carousel.py   # ✅ Publicar carrossel
│   ├── publish_reel.py       # ✅ Publicar Reel
│   ├── publish_story.py      # ✅ Publicar Story
│   ├── get_insights.py       # ✅ Obter métricas
│   └── manage_comments.py    # ✅ Gerenciar comentários
│
├── meta-ads/                 # Templates Meta Ads
│   ├── README.md
│   ├── create_campaign.py    # ✅ Criar campanha
│   ├── create_adset.py       # ✅ Criar ad set
│   ├── create_ad.py          # ✅ Criar anúncio completo
│   └── get_insights.py       # ✅ Obter métricas
│
├── nextcloud/                # Templates Nextcloud (Upload)
│   ├── README.md
│   ├── upload_to_nextcloud.py      # ✅ Upload manual com caminho
│   └── upload_from_downloads.py   # ✅ Upload rápido do Downloads
│
├── extraction/               # Templates Extração de Conteúdo
│   ├── README.md
│   ├── transcribe_video.py   # ✅ Transcrever vídeos (YouTube, TikTok, IG, etc)
│   ├── extract_instagram.py  # ✅ Extrair posts IG (imagens + legendas)
│   ├── scrape_website.py     # ✅ Web scraping (conversão para Markdown)
│   └── scrape_batch.py       # ✅ Web scraping em batch (múltiplos sites)
│
├── video-generation/         # Templates Geração de Vídeos (Sora 2)
│   ├── README.md
│   ├── generate_sora.py      # ✅ Gerar vídeo único
│   └── batch_generate.py     # ✅ Gerar vídeos em lote
│
├── audio-generation/         # Templates Geração de Áudio (ElevenLabs)
│   ├── README.md
│   ├── generate_elevenlabs.py # ✅ Gerar áudio único
│   └── batch_generate.py      # ✅ Gerar áudios em lote
│
├── search/                   # Templates Busca em Tempo Real (xAI Search)
│   ├── README.md
│   ├── xai_web.py            # ✅ Busca na web
│   ├── xai_twitter.py        # ✅ Busca no Twitter/X
│   └── xai_news.py           # ✅ Busca em notícias
│
├── twitter/                  # Templates Twitter/X Scraping (Apify)
│   ├── README.md
│   ├── search_twitter.py     # ✅ Busca avançada de tweets
│   ├── scrape_profile.py     # ✅ Scraping de perfil
│   ├── scrape_tweets.py      # ✅ Scraping de tweets específicos
│   ├── scrape_replies.py     # ✅ Scraping de replies/conversas
│   └── batch_twitter.py      # ✅ Batch (múltiplos perfis/termos)
│
├── tiktok/                   # Templates TikTok Scraping (TikTok API23) ✅
│   ├── README.md
│   ├── get_user_info.py      # ✅ Info de usuário
│   ├── get_video_info.py     # ✅ Detalhes de vídeo
│   ├── search_content.py     # ✅ Buscar conteúdo
│   ├── get_trending.py       # ✅ Monitorar trending
│   └── analyze_hashtag.py    # ✅ Analisar hashtag
│
├── scraping/                 # Templates Google Maps Scraping (Apify)
│   ├── README.md
│   ├── google_maps_basic.py  # ✅ Busca básica
│   ├── google_maps_advanced.py # ✅ Busca avançada
│   └── google_maps_batch.py  # ✅ Batch (múltiplas buscas)
│
├── instagram-scraper/        # Templates Instagram Scraping (Apify)
│   ├── README.md
│   ├── scrape_user_posts.py  # ✅ Posts de usuário
│   ├── scrape_hashtag_posts.py # ✅ Posts de hashtag
│   ├── scrape_post_comments.py # ✅ Comentários de post
│   ├── scrape_user_profile.py # ✅ Perfil completo
│   └── scrape_place_posts.py # ✅ Posts de localização
│
└── common/                   # Templates genéricos
    └── template_base.py      # 📋 Template base para criar novos scripts
```

---

## 🚀 Como Usar (Para o Agente)

### Quando o usuário pedir uma ação comum:

**❌ ANTES (criar script novo):**
```
Usuário: "Envie uma mensagem WhatsApp para 5531980160822"
Agente: Cria novo script test_send.py → Executa → Descarta
```

**✅ AGORA (usar template):**
```
Usuário: "Envie uma mensagem WhatsApp para 5531980160822"
Agente: python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Texto"
```

### Benefícios:
- ⚡ **Mais rápido** - Execução direta sem criar arquivo
- 🎯 **Mais preciso** - Templates testados e confiáveis
- 📦 **Mais limpo** - Não cria arquivos temporários
- 🔄 **Reutilizável** - Scripts permanentes para uso futuro

---

## 📚 Templates Disponíveis

### WhatsApp (Evolution API) - ✅ PRONTOS

| Script | Descrição | Exemplo |
|--------|-----------|---------|
| `send_message.py` | Enviar mensagem de texto | `--phone 5531980160822 --message "Olá!"` |
| `send_media.py` | Enviar mídia (imagem/vídeo/doc) | `--phone 5531980160822 --file image.jpg --type image` |
| `create_group.py` | Criar grupo WhatsApp | `--name "Grupo" --phones 5531980160822,5511999999999` |
| `send_poll.py` | Enviar enquete | `--phone 5531980160822 --question "Pizza?" --options "Sim,Não"` |

**Documentação completa:** [scripts/whatsapp/README.md](whatsapp/README.md)

---

### Image Generation (APIs de IA) - ✅ PRONTOS

| Script | Descrição | Exemplo |
|--------|-----------|---------|
| `generate_gpt4o.py` | Gerar imagem com GPT-4o | `"astronauta gato" --variants 2 --enhance` |
| `generate_nanobanana.py` | Gerar imagem com Nano Banana | `"logo empresa" --format JPEG` |
| `generate_dalle3.py` | Gerar imagem com DALL-E 3 | `"paisagem" --size 1792x1024 --quality hd` |
| `batch_generate.py` | Gerar múltiplas imagens | `"gato" "cachorro" --api nanobanana` |
| `edit_nanobanana.py` | Editar imagem existente | `foto.jpg "remover fundo" --size 1:1` |

**APIs suportadas:** GPT-4o (Kie.ai), Nano Banana/Gemini 2.5 Flash (Kie.ai), DALL-E 3 (OpenAI)

**Documentação completa:** [scripts/image-generation/README.md](image-generation/README.md)

---

### Instagram (Graph API) - ✅ PRONTOS

| Script | Descrição | Exemplo |
|--------|-----------|---------|
| `publish_post.py` | Publicar post (imagem/vídeo) | `--image foto.jpg --caption "Meu post!"` |
| `publish_carousel.py` | Publicar carrossel (múltiplas imagens) | `--images foto1.jpg,foto2.jpg --caption "Carrossel"` |
| `publish_reel.py` | Publicar Reel | `--video reel.mp4 --caption "Meu Reel!" --cover capa.jpg` |
| `publish_story.py` | Publicar Story | `--media story.jpg --type image` |
| `get_insights.py` | Obter métricas de posts | `--post-id 123456 --metrics reach,impressions` |
| `manage_comments.py` | Gerenciar comentários | `--post-id 123456 --action reply --text "Obrigado!"` |

**API integrada:** Instagram Graph API v24.0

**Documentação completa:** [scripts/instagram/README.md](instagram/README.md)

---

### Meta Ads - ✅ PRONTOS

**4 templates funcionais** para automação Meta Ads:

| Script | Descrição | Exemplo |
|--------|-----------|---------|
| `create_campaign.py` | Criar campanha | `--name "Minha Campanha" --objective OUTCOME_TRAFFIC` |
| `create_adset.py` | Criar ad set | `--campaign-id 123456789 --name "Ad Set Brasil"` |
| `create_ad.py` | Criar anúncio completo (imagem + criativo + ad) | `--adset-id 987654321 --name "Anúncio Casa" --message "Casa linda!" --link "https://site.com" --image "foto.jpg"` |
| `get_insights.py` | Obter métricas | `--id 123456789 --level campaign --period last_7d` |

**Documentação completa:** [scripts/meta-ads/README.md](meta-ads/README.md)

---

### Nextcloud (Upload) - ✅ PRONTOS

**2 templates funcionais** para upload no Nextcloud:

| Script | Descrição | Exemplo |
|--------|-----------|---------|
| `upload_to_nextcloud.py` | Upload manual de qualquer arquivo | `arquivo.jpg --days 7 --folder "fotos"` |
| `upload_from_downloads.py` | Upload rápido da pasta Downloads | `--name "screenshot" --days 7` |

**Recursos:** Links públicos automáticos, expiração configurável (temporário ou permanente), busca por nome, listagem de arquivos recentes

**Documentação completa:** [scripts/nextcloud/README.md](nextcloud/README.md) | [docs/tools/cloud.md](../docs/tools/cloud.md)

---

### Video Generation (Sora 2) - ✅ PRONTOS

**2 templates funcionais** para geração de vídeos com Sora 2 (OpenAI):

| Script | Descrição | Exemplo |
|--------|-----------|---------|
| `generate_sora.py` | Gerar vídeo único | `"gato brincando" --aspect portrait` |
| `batch_generate.py` | Gerar vídeos em lote (paralelo) | `"cena 1" "cena 2" "cena 3" --aspect landscape` |

**Recursos:** Geração paralela (batch), suporte a 3 proporções (portrait, landscape, square), remoção automática de marca d'água, vídeos ~15s

**Documentação completa:** [scripts/video-generation/README.md](video-generation/README.md)

---

### Common - Templates Genéricos

| Script | Descrição |
|--------|-----------|
| `template_base.py` | Template base para criar novos scripts rapidamente |

---

## 🛠️ Como Criar Novos Templates

### 1. Use o template base:
```bash
cp scripts/common/template_base.py scripts/categoria/novo_script.py
```

### 2. Adapte para sua necessidade:
- Modifique a função `execute_action()`
- Adicione argumentos em `main()`
- Atualize a documentação do script

### 3. Torne executável:
```bash
chmod +x scripts/categoria/novo_script.py
```

### 4. Documente:
- Adicione ao README.md da categoria
- Adicione exemplos de uso
- Atualize o índice principal (este arquivo)

---

## 📖 Documentação Detalhada

Cada categoria tem seu próprio README.md com:
- ✅ Exemplos de uso detalhados
- ✅ Todos os parâmetros disponíveis
- ✅ Casos de uso comuns
- ✅ Troubleshooting

**READMEs por categoria:**
- [WhatsApp](whatsapp/README.md)
- [Image Generation](image-generation/README.md)
- [Video Generation](video-generation/README.md)
- [Instagram](instagram/README.md)
- [Meta Ads](meta-ads/README.md)
- [Nextcloud](nextcloud/README.md)

---

## 🎓 Instruções para Claude Code

### Quando usar templates:

1. **Ações WhatsApp** → Use `scripts/whatsapp/*`
2. **Geração de Imagens** → Use `scripts/image-generation/*`
3. **Geração de Vídeos** → Use `scripts/video-generation/*`
4. **Ações Instagram** → Use `scripts/instagram/*`
5. **Ações Meta Ads** → Use `scripts/meta-ads/*`
6. **Upload Nextcloud** → Use `scripts/nextcloud/*`

### Fluxo recomendado:

```
1. Usuário pede ação → Verificar se existe template
2. Template existe? → Executar diretamente
3. Template não existe? → Criar novo template reutilizável (não script temporário)
4. Documentar novo template → Adicionar ao README
```

### Regras importantes:

✅ **SEMPRE** use templates quando disponíveis
✅ **SEMPRE** crie templates reutilizáveis (não scripts temporários)
✅ **SEMPRE** documente novos templates
✅ **NUNCA** crie scripts descartáveis para ações que podem ser templates

---

## 🔧 Manutenção

### Adicionar novo template:
1. Criar script em `scripts/categoria/`
2. Adicionar documentação ao `README.md` da categoria
3. Atualizar este `README.md` principal
4. Tornar executável (`chmod +x`)

### Atualizar template existente:
1. Modificar o script
2. Atualizar documentação
3. Testar funcionamento
4. Commitar mudanças

---

## 📊 Status dos Templates

| Categoria | Templates | Status | Cobertura |
|-----------|-----------|--------|-----------|
| WhatsApp | 4 | ✅ Prontos | 100% funcional |
| Image Generation | 5 | ✅ Prontos | 100% funcional |
| Video Generation | 2 | ✅ Prontos | 100% funcional |
| Instagram | 6 | ✅ Prontos | 100% funcional |
| Meta Ads | 4 | ✅ Prontos | 100% funcional |
| Nextcloud | 2 | ✅ Prontos | 100% funcional |
| Common | 1 | ✅ Pronto | Template genérico |

---

## 🎯 Próximos Passos

### Prioridade Alta:
- [x] Implementar templates Instagram (publish_post, publish_carousel, publish_reel) ✅ **CONCLUÍDO**
- [x] Implementar templates Meta Ads (create_campaign, create_adset, create_ad, get_insights) ✅ **CONCLUÍDO**

### Prioridade Média:
- [ ] Adicionar mais templates WhatsApp (send_location, send_contact, etc)
- [ ] Adicionar mais templates Instagram (manage_dms, get_user_insights, etc)
- [ ] Criar templates para outras integrações (n8n, Chatwoot, etc)

### Prioridade Baixa:
- [ ] Criar interface web para executar templates
- [ ] Criar sistema de logs centralizado para templates

---

**Última atualização:** 2025-11-01
**Versão:** 1.0
**Desenvolvido para:** Claude Code Workspace
