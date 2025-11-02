# 📸 Instagram Scraper Templates (Apify)

Templates prontos para extrair dados públicos do Instagram via Apify API.

## 🎯 Templates Disponíveis

### ✅ 5 Templates Testados

1. **scrape_user_posts.py** - Extrair posts de perfil
2. **scrape_hashtag_posts.py** - Extrair posts de hashtag
3. **scrape_post_comments.py** - Extrair comentários de post
4. **scrape_user_profile.py** - Extrair detalhes de perfil
5. **scrape_place_posts.py** - Extrair posts de localização

---

## 📦 Instalação

```bash
# Instalar biblioteca Apify
pip3 install apify-client
```

## 🚀 Uso Rápido

### 1. Posts de Usuário

```bash
# Scrape 50 posts (padrão)
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo"

# Scrape 100 posts
python3 scripts/instagram-scraper/scrape_user_posts.py "avengers" --limit 100

# Apenas posts após 2024-01-01
python3 scripts/instagram-scraper/scrape_user_posts.py "humansofny" --newer-than "2024-01-01"

# Salvar em arquivo específico
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo" --output meu_arquivo.json
```

**Dados extraídos:**
- Tipo de post (Image, Video, Sidecar/Carrossel)
- URL, shortcode, caption
- Contadores: likes, comentários
- Hashtags, menções
- Dimensões, displayUrl
- Timestamp, ownerUsername
- isSponsored

### 2. Posts de Hashtag

```bash
# Scrape posts de hashtag
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "travel"

# Com limite personalizado
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "endgame" --limit 100

# Filtrar por data
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "fitness" --newer-than "2024-01-01"
```

**Dados extraídos:**
- Mesmos dados de posts de usuário
- Adicional: ownerUsername de quem postou

### 3. Comentários de Post

```bash
# Scrape comentários de post
python3 scripts/instagram-scraper/scrape_post_comments.py "https://instagram.com/p/ABC123/"

# Com limite personalizado
python3 scripts/instagram-scraper/scrape_post_comments.py "https://instagram.com/p/ABC123/" --limit 200
```

**Dados extraídos:**
- id, postId, text
- position, timestamp
- ownerId, ownerUsername
- ownerIsVerified
- ownerProfilePicUrl

### 4. Perfil de Usuário

```bash
# Scrape detalhes completos de perfil
python3 scripts/instagram-scraper/scrape_user_profile.py "natgeo"

# Salvar em arquivo
python3 scripts/instagram-scraper/scrape_user_profile.py "avengers" --output perfil.json
```

**Dados extraídos:**
- id, username, fullName
- biography, externalUrl
- followersCount, followsCount, postsCount
- verified, private, isBusinessAccount
- businessCategoryName
- profilePicUrl, profilePicUrlHD
- igtvVideoCount, highlightReelCount
- latestPosts (array de posts recentes)
- latestIgtvVideos

### 5. Posts de Localização

```bash
# Scrape posts de localização
python3 scripts/instagram-scraper/scrape_place_posts.py "Niagara Falls"

# Com limite
python3 scripts/instagram-scraper/scrape_place_posts.py "Eiffel Tower" --limit 100

# Filtrar por data
python3 scripts/instagram-scraper/scrape_place_posts.py "Times Square" --newer-than "2024-01-01"
```

**Dados extraídos:**
- Mesmos dados de posts
- Adicional: locationName, locationId

---

## 🔧 Ferramenta Base

Para uso avançado, use a ferramenta base diretamente:

```bash
# Uso geral
python3 tools/apify_instagram.py --user "natgeo" --results-type posts --limit 50

# Todos os parâmetros
python3 tools/apify_instagram.py \
  --user "natgeo" \
  --results-type posts \
  --limit 100 \
  --newer-than "2024-01-01" \
  --older-than "2024-12-31" \
  --output resultado.json
```

### Tipos de Resultado (`--results-type`)

- **posts**: Retorna posts (imagens/vídeos/carrosseis)
- **comments**: Retorna comentários (requer URL de post)
- **details**: Retorna detalhes completos (perfil/hashtag/localização)

---

## 📊 Estrutura de Dados

### Post

```json
{
  "type": "Image",
  "shortCode": "ABC123",
  "url": "https://instagram.com/p/ABC123/",
  "caption": "Legenda do post",
  "hashtags": ["travel", "nature"],
  "mentions": ["natgeo"],
  "likesCount": 12345,
  "commentsCount": 678,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "ownerUsername": "natgeo",
  "displayUrl": "https://...",
  "dimensionsHeight": 1080,
  "dimensionsWidth": 1080
}
```

### Comentário

```json
{
  "id": "17900515570488496",
  "postId": "ABC123",
  "text": "Ótimo post!",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "ownerUsername": "user123",
  "ownerIsVerified": false,
  "ownerProfilePicUrl": "https://..."
}
```

### Perfil

```json
{
  "id": "123456789",
  "username": "natgeo",
  "fullName": "National Geographic",
  "biography": "Experience the world...",
  "externalUrl": "https://natgeo.com",
  "followersCount": 10000000,
  "followsCount": 100,
  "postsCount": 5000,
  "verified": true,
  "private": false,
  "isBusinessAccount": true,
  "businessCategoryName": "Media",
  "latestPosts": [...],
  "igtvVideoCount": 50
}
```

---

## 💰 Pricing

**Custo:** $2.30 por 1.000 comentários ($0.0023 por comentário)

**Plano Free:**
- $5 de créditos gratuitos/mês
- ~2.100 comentários gratuitos/mês

**Plano Starter ($49/mês):**
- ~21.000 comentários/mês

**Observações:**
- Posts e perfis têm custos similares
- Custo varia conforme complexidade da extração
- Use `resultsLimit` para controlar custos

---

## ⚙️ Configuração

### API Key

A API key está configurada em `config/apify_config.py`:

```python
APIFY_API_KEY = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
INSTAGRAM_SCRAPER_ACTOR_ID = "apify/instagram-scraper"
```

### Defaults

```python
INSTAGRAM_DEFAULTS = {
    "resultsLimit": 50,
    "searchLimit": 10,
    "addParentData": False,
    "enhanceUserSearchWithFacebookPage": False,
}
```

---

## 🎯 Casos de Uso

### 1. Análise de Competidores

```bash
# Extrair posts de concorrente
python3 scripts/instagram-scraper/scrape_user_posts.py "concorrente" --limit 100

# Analisar hashtags que usam
# (procurar por hashtags nos posts extraídos)
```

### 2. Monitoramento de Hashtags

```bash
# Monitorar hashtag da marca
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "minhamarca" --limit 100

# Verificar quem está usando
# (analisar ownerUsername nos resultados)
```

### 3. Análise de Engajamento

```bash
# Extrair comentários de post
python3 scripts/instagram-scraper/scrape_post_comments.py "https://instagram.com/p/ABC/"

# Analisar sentimento dos comentários
# (processar texto com IA)
```

### 4. Pesquisa de Mercado

```bash
# Posts de localização (ex: restaurantes em SP)
python3 scripts/instagram-scraper/scrape_place_posts.py "São Paulo, Brazil" --limit 200

# Analisar tendências locais
```

### 5. Influencer Research

```bash
# Extrair perfil completo
python3 scripts/instagram-scraper/scrape_user_profile.py "influencer"

# Verificar:
# - followersCount (alcance)
# - latestPosts (engajamento médio)
# - verified (credibilidade)
```

---

## 🚨 Limitações

### O que funciona:
- ✅ Perfis públicos
- ✅ Posts públicos
- ✅ Hashtags públicas
- ✅ Localizações públicas
- ✅ Comentários de posts públicos

### O que NÃO funciona:
- ❌ Perfis privados (retorna apenas dados básicos)
- ❌ Posts privados
- ❌ DMs (mensagens diretas)
- ❌ Stories (expiram em 24h)
- ❌ Dados de email/telefone (privados)

### Número de Resultados

O número de resultados varia conforme:
- Disponibilidade pública dos dados
- Instagram pode limitar dados para não-logados
- Teste em janela anônima para ver o que está disponível

**Recomendação:** Sempre teste com `--limit` pequeno primeiro (10-20) para verificar disponibilidade antes de extrair grande volume.

---

## 📖 Documentação Completa

- **Apify Docs:** https://apify.com/apify/instagram-scraper
- **Ferramenta base:** `tools/apify_instagram.py`
- **Configuração:** `config/apify_config.py`
- **Docs detalhada:** `docs/tools/apify_instagram.md`

---

## 🤖 Uso Programático (Python)

```python
from tools.apify_instagram import InstagramScraper

# Inicializar
scraper = InstagramScraper()

# Posts de usuário
result = scraper.scrape_user_posts("natgeo", limit=50)

# Posts de hashtag
result = scraper.scrape_hashtag_posts("travel", limit=100)

# Comentários
result = scraper.scrape_post_comments("https://instagram.com/p/ABC/", limit=200)

# Perfil
result = scraper.scrape_user_profile("avengers")

# Acesso aos dados
if result["success"]:
    items = result["items"]
    for item in items:
        print(item)
```

---

## 🔍 Troubleshooting

### Erro: `apify-client` não instalado

```bash
pip3 install apify-client
```

### Erro: API Key inválida

Verifique em `config/apify_config.py` se a key está correta.

### Poucos resultados retornados

- Instagram limita dados públicos para não-logados
- Teste em janela anônima: `https://instagram.com/USERNAME`
- Use `--limit` menor para testes

### Timeout

Use `--timeout` maior:

```bash
python3 tools/apify_instagram.py --user "natgeo" --limit 500 --timeout 600
```

---

**Última atualização:** 2025-11-02
**Status:** ✅ 5 templates prontos e testados
