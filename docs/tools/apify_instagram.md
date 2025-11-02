# 📸 Instagram Scraper (Apify API)

Ferramenta completa para extrair dados públicos do Instagram usando Apify API.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Instalação](#instalação)
- [Uso Rápido](#uso-rápido)
- [Templates Disponíveis](#templates-disponíveis)
- [API Avançada](#api-avançada)
- [Estrutura de Dados](#estrutura-de-dados)
- [Pricing & Limites](#pricing--limites)
- [Casos de Uso](#casos-de-uso)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Instagram Scraper permite extrair dados públicos do Instagram:

- ✅ **Posts de usuário** - Imagens, vídeos, carrosseis
- ✅ **Posts de hashtag** - Descubra conteúdo por hashtag
- ✅ **Comentários** - Análise de sentimento e engajamento
- ✅ **Perfis** - Seguidores, biografia, posts recentes
- ✅ **Localizações** - Posts geolocalizados

### Por que usar?

Instagram removeu API pública em 2020. Este scraper:

- Acessa dados públicos sem API oficial
- Sem necessidade de conta Business/Creator
- Extração em larga escala
- Pricing pay-per-result transparente

---

## 📦 Instalação

```bash
# Biblioteca Apify
pip3 install apify-client
```

**Configuração:**

A API key já está configurada em `config/apify_config.py`:

```python
APIFY_API_KEY = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
INSTAGRAM_SCRAPER_ACTOR_ID = "apify/instagram-scraper"
```

---

## 🚀 Uso Rápido

### Templates (Recomendado)

Use os templates em `scripts/instagram-scraper/`:

```bash
# Posts de usuário
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo" --limit 50

# Posts de hashtag
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "travel" --limit 100

# Comentários de post
python3 scripts/instagram-scraper/scrape_post_comments.py "https://instagram.com/p/ABC123/"

# Perfil completo
python3 scripts/instagram-scraper/scrape_user_profile.py "avengers"

# Posts de localização
python3 scripts/instagram-scraper/scrape_place_posts.py "Niagara Falls" --limit 50
```

### Ferramenta Base

Para uso avançado:

```bash
# Sintaxe geral
python3 tools/apify_instagram.py \
  --user "USERNAME" \
  --results-type posts \
  --limit 50 \
  --output resultado.json

# Com filtros de data
python3 tools/apify_instagram.py \
  --hashtag "fitness" \
  --results-type posts \
  --limit 100 \
  --newer-than "2024-01-01" \
  --older-than "2024-12-31"
```

---

## 📂 Templates Disponíveis

### 1. scrape_user_posts.py

Extrai posts de perfil.

```bash
# Uso básico
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo"

# Com limite
python3 scripts/instagram-scraper/scrape_user_posts.py "avengers" --limit 100

# Filtrar por data
python3 scripts/instagram-scraper/scrape_user_posts.py "humansofny" \
  --newer-than "2024-01-01" \
  --older-than "2024-12-31"

# Arquivo personalizado
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo" \
  --output ~/Documents/natgeo_posts.json
```

**Output:**
- Tipo de post (Image/Video/Sidecar)
- URL, caption, hashtags, mentions
- Likes, comentários
- Timestamp, dimensões
- Display URL

### 2. scrape_hashtag_posts.py

Extrai posts de hashtag.

```bash
# Uso básico
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "travel"

# Com limite
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "endgame" --limit 100

# Filtrar por data
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "fitness" \
  --newer-than "2024-01-01"
```

**Output:**
- Mesmos dados de posts de usuário
- Adicional: `ownerUsername` (quem postou)

### 3. scrape_post_comments.py

Extrai comentários de post.

```bash
# Uso básico
python3 scripts/instagram-scraper/scrape_post_comments.py \
  "https://instagram.com/p/ABC123/"

# Com limite
python3 scripts/instagram-scraper/scrape_post_comments.py \
  "https://instagram.com/p/ABC123/" \
  --limit 200
```

**Output:**
- id, postId, text
- timestamp
- ownerUsername, ownerIsVerified
- ownerProfilePicUrl

### 4. scrape_user_profile.py

Extrai detalhes completos de perfil.

```bash
# Uso básico
python3 scripts/instagram-scraper/scrape_user_profile.py "natgeo"

# Salvar em arquivo
python3 scripts/instagram-scraper/scrape_user_profile.py "avengers" \
  --output perfil_avengers.json
```

**Output:**
- id, username, fullName
- biography, externalUrl
- followersCount, followsCount, postsCount
- verified, private, isBusinessAccount
- latestPosts (array)
- latestIgtvVideos (array)

### 5. scrape_place_posts.py

Extrai posts de localização.

```bash
# Uso básico
python3 scripts/instagram-scraper/scrape_place_posts.py "Niagara Falls"

# Com limite
python3 scripts/instagram-scraper/scrape_place_posts.py "Eiffel Tower" --limit 100

# Filtrar por data
python3 scripts/instagram-scraper/scrape_place_posts.py "Times Square" \
  --newer-than "2024-01-01"
```

**Output:**
- Mesmos dados de posts
- Adicional: `locationName`, `locationId`

---

## 🔧 API Avançada

### Ferramenta Base (tools/apify_instagram.py)

```bash
python3 tools/apify_instagram.py [OPTIONS]
```

**Opções principais:**

| Opção | Descrição | Exemplo |
|-------|-----------|---------|
| `--user` | Username (sem @) | `--user "natgeo"` |
| `--hashtag` | Hashtag (sem #) | `--hashtag "travel"` |
| `--place` | Localização | `--place "Niagara Falls"` |
| `--url` | URL de post | `--url "https://instagram.com/p/ABC/"` |
| `--results-type` | Tipo de resultado | `--results-type posts` |
| `--limit` | Limite de resultados | `--limit 100` |
| `--search-limit` | Limite de busca | `--search-limit 10` |
| `--newer-than` | Filtro de data (após) | `--newer-than "2024-01-01"` |
| `--older-than` | Filtro de data (antes) | `--older-than "2024-12-31"` |
| `--output` | Arquivo de saída | `--output resultado.json` |
| `--timeout` | Timeout (segundos) | `--timeout 600` |

**Tipos de Resultado:**

- **posts**: Posts (imagens/vídeos/carrosseis)
- **comments**: Comentários (requer URL)
- **details**: Detalhes (perfil/hashtag/place)

### Uso Programático (Python)

```python
from tools.apify_instagram import InstagramScraper

# Inicializar
scraper = InstagramScraper()

# 1. Posts de usuário
result = scraper.scrape_user_posts(
    username="natgeo",
    limit=50,
    output_file="~/Downloads/natgeo_posts.json"
)

# 2. Posts de hashtag
result = scraper.scrape_hashtag_posts(
    hashtag="travel",
    limit=100
)

# 3. Comentários
result = scraper.scrape_post_comments(
    post_url="https://instagram.com/p/ABC123/",
    limit=200
)

# 4. Perfil
result = scraper.scrape_user_profile(
    username="avengers",
    output_file="perfil.json"
)

# 5. Uso avançado (scrape genérico)
result = scraper.scrape(
    user="natgeo",
    results_type="posts",
    results_limit=50,
    newer_than="2024-01-01",
    older_than="2024-12-31",
    timeout=600,
    output_file="resultado.json"
)

# Processar resultados
if result["success"]:
    print(f"Total: {result['items_count']} itens")

    for item in result["items"]:
        # Posts
        if "shortCode" in item:
            print(f"Post: {item['url']}")
            print(f"Likes: {item.get('likesCount', 0)}")

        # Comentários
        if "text" in item and "postId" in item:
            print(f"@{item['ownerUsername']}: {item['text']}")

        # Perfil
        if "followersCount" in item:
            print(f"@{item['username']}: {item['followersCount']} seguidores")
```

---

## 📊 Estrutura de Dados

### Post (Image/Video/Sidecar)

```json
{
  "inputUrl": "https://www.instagram.com/natgeo",
  "url": "https://www.instagram.com/p/ABC123/",
  "type": "Image",
  "shortCode": "ABC123",
  "caption": "Legenda do post com #hashtags e @mentions",
  "hashtags": ["travel", "nature"],
  "mentions": ["natgeo"],
  "commentsCount": 1234,
  "firstComment": "Primeiro comentário",
  "latestComments": [],
  "dimensionsHeight": 1080,
  "dimensionsWidth": 1080,
  "displayUrl": "https://scontent-...",
  "images": [],
  "alt": "Texto alternativo",
  "likesCount": 123456,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "childPosts": [],
  "ownerFullName": "National Geographic",
  "ownerUsername": "natgeo",
  "ownerId": "123456789",
  "isSponsored": false
}
```

### Comentário

```json
{
  "id": "17900515570488496",
  "postId": "BwrsO1Bho2N",
  "text": "Ótimo post! 👏",
  "position": 1,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "ownerId": "5319127183",
  "ownerIsVerified": false,
  "ownerUsername": "user123",
  "ownerProfilePicUrl": "https://scontent-..."
}
```

### Perfil de Usuário

```json
{
  "id": "6622284809",
  "username": "avengers",
  "fullName": "Avengers: Endgame",
  "biography": "Marvel Studios' \"Avengers: Endgame\" is now playing in theaters.",
  "externalUrl": "http://www.fandango.com/avengersendgame",
  "externalUrlShimmed": "https://l.instagram.com/?u=...",
  "followersCount": 8212505,
  "followsCount": 4,
  "hasChannel": false,
  "highlightReelCount": 3,
  "isBusinessAccount": true,
  "joinedRecently": false,
  "businessCategoryName": "Content & Apps",
  "private": false,
  "verified": true,
  "profilePicUrl": "https://scontent-...",
  "profilePicUrlHD": "https://scontent-...",
  "facebookPage": null,
  "igtvVideoCount": 5,
  "latestIgtvVideos": [...],
  "postsCount": 274,
  "latestPosts": [...]
}
```

### Hashtag

```json
{
  "id": "17843854051054595",
  "name": "endgame",
  "topPostsOnly": false,
  "profilePicUrl": "https://scontent-...",
  "postsCount": 1510549,
  "topPosts": [...],
  "latestPosts": [...]
}
```

### Localização (Place)

```json
{
  "id": "1017812091",
  "name": "Náměstí Míru",
  "public": true,
  "lat": 50.0753325,
  "lng": 14.43769,
  "slug": "namesti-miru",
  "description": "",
  "website": "",
  "phone": "",
  "addressCityName": "Prague, Czech Republic",
  "addressCountryCode": "CZ",
  "profilePicUrl": "https://scontent-...",
  "postsCount": 5310,
  "topPosts": [...],
  "latestPosts": [...]
}
```

---

## 💰 Pricing & Limites

### Custo

**Pay-per-result:** $2.30 por 1.000 comentários

- $0.0023 por comentário
- Custo similar para posts e perfis
- Varia conforme complexidade da extração

### Planos

**Free:**
- $5 créditos gratuitos/mês
- ~2.100 comentários/mês

**Starter ($49/mês):**
- ~21.000 comentários/mês

### Limites de Resultados

O número de resultados varia:

- **Disponibilidade pública**: Instagram limita dados para não-logados
- **Perfis privados**: Apenas dados básicos
- **Teste**: Sempre abra URL em janela anônima para ver o que está disponível

**Recomendação:**
1. Teste com `--limit 10` primeiro
2. Verifique quantos resultados retornaram
3. Ajuste `--limit` conforme necessário

### Controle de Custos

```bash
# Sempre use --limit para controlar custos
python3 scripts/instagram-scraper/scrape_user_posts.py "natgeo" --limit 20

# Para testes, use limites baixos
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "travel" --limit 10
```

---

## 🎯 Casos de Uso

### 1. Análise de Competidores

**Objetivo:** Entender estratégia de conteúdo de concorrentes

```bash
# Extrair últimos 100 posts
python3 scripts/instagram-scraper/scrape_user_posts.py "concorrente" --limit 100

# Analisar:
# - Frequência de posts (timestamps)
# - Tipos de conteúdo (type: Image/Video/Sidecar)
# - Hashtags usadas (hashtags[])
# - Engajamento médio (likesCount, commentsCount)
# - Horários de maior engajamento
```

**Métricas a extrair:**
- Taxa de engajamento: (likes + comments) / followers
- Hashtags mais usadas
- Tipos de post com melhor performance
- Frequência de publicação

### 2. Monitoramento de Hashtags

**Objetivo:** Descobrir quem usa hashtags da marca

```bash
# Monitorar hashtag
python3 scripts/instagram-scraper/scrape_hashtag_posts.py "minhamarca" --limit 200

# Analisar:
# - ownerUsername (quem postou)
# - caption (contexto do uso)
# - likesCount (alcance)
# - timestamp (quando foi postado)
```

**Use cases:**
- User-generated content (UGC)
- Influencer discovery
- Brand monitoring
- Trend analysis

### 3. Análise de Sentimento

**Objetivo:** Entender sentimento de comentários

```bash
# Extrair comentários
python3 scripts/instagram-scraper/scrape_post_comments.py \
  "https://instagram.com/p/ABC123/" \
  --limit 500

# Processar com IA:
# - Análise de sentimento (positivo/negativo/neutro)
# - Tópicos recorrentes
# - Perguntas frequentes
# - Críticas/elogios
```

**Integração com IA:**

```python
from tools.apify_instagram import InstagramScraper
import openai  # ou outro LLM

scraper = InstagramScraper()
result = scraper.scrape_post_comments("https://instagram.com/p/ABC/", limit=100)

comments_text = [c["text"] for c in result["items"]]

# Análise com GPT
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"Analise o sentimento destes comentários:\n{comments_text}"
    }]
)
```

### 4. Pesquisa de Mercado

**Objetivo:** Entender tendências locais

```bash
# Posts de localização
python3 scripts/instagram-scraper/scrape_place_posts.py "São Paulo, Brazil" \
  --limit 500 \
  --newer-than "2024-01-01"

# Analisar:
# - Tendências locais (hashtags, captions)
# - Influenciadores locais (ownerUsername com muitos likes)
# - Melhores horários (timestamp)
# - Tipos de conteúdo populares (type)
```

**Insights:**
- O que está sendo postado em locais específicos?
- Quem são os influenciadores locais?
- Quais produtos/serviços aparecem mais?

### 5. Influencer Research

**Objetivo:** Encontrar influenciadores relevantes

```bash
# Extrair perfil
python3 scripts/instagram-scraper/scrape_user_profile.py "influencer"

# Verificar:
# - followersCount (alcance)
# - verified (credibilidade)
# - latestPosts (engajamento médio)
# - isBusinessAccount (profissionalismo)
# - externalUrl (outras plataformas)
```

**Métricas de análise:**

```python
from tools.apify_instagram import InstagramScraper

scraper = InstagramScraper()
result = scraper.scrape_user_profile("influencer")

if result["success"]:
    profile = result["items"][0]

    # Métricas
    followers = profile["followersCount"]
    posts = profile["latestPosts"]

    # Taxa de engajamento
    total_likes = sum(p.get("likesCount", 0) for p in posts)
    avg_engagement = (total_likes / len(posts)) / followers * 100

    print(f"Engajamento médio: {avg_engagement:.2f}%")
```

### 6. Content Strategy

**Objetivo:** Planejar calendário de conteúdo

```bash
# Extrair posts de múltiplos concorrentes
for user in "concorrente1" "concorrente2" "concorrente3"; do
  python3 scripts/instagram-scraper/scrape_user_posts.py "$user" \
    --limit 50 \
    --output "${user}_posts.json"
done

# Analisar:
# - Dias/horários com mais engajamento
# - Tipos de conteúdo que performam melhor
# - Hashtags efetivas
# - Formatos (carrossel vs single image)
```

---

## 🚨 Limitações

### O que funciona ✅

- ✅ Perfis públicos
- ✅ Posts públicos
- ✅ Hashtags públicas
- ✅ Localizações públicas
- ✅ Comentários de posts públicos

### O que NÃO funciona ❌

- ❌ Perfis privados (apenas dados básicos: username, bio, followers)
- ❌ Posts de perfis privados
- ❌ DMs (mensagens diretas)
- ❌ Stories (expiram em 24h, não acessíveis)
- ❌ Dados privados (email, telefone, gênero, localização exata)
- ❌ Histórico completo (Instagram limita dados antigos)

### Considerações Legais

**⚠️ IMPORTANTE:**

Este scraper extrai **apenas dados públicos**. É sua responsabilidade:

- ✅ Usar dados apenas para fins éticos e legais
- ✅ Respeitar LGPD/GDPR se processar dados pessoais
- ✅ Não usar para spam, assédio ou propósitos maliciosos
- ✅ Verificar termos de uso do Instagram

**Dados públicos ≠ Uso irrestrito**

Mesmo sendo públicos, os dados podem conter informações pessoais protegidas por lei. Consulte um advogado se tiver dúvidas sobre seu caso de uso.

---

## 🔍 Troubleshooting

### Erro: `apify-client` não instalado

```bash
pip3 install apify-client
```

### Erro: API Key inválida

Verifique em `config/apify_config.py`:

```python
APIFY_API_KEY = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
```

### Poucos resultados retornados

**Causa:** Instagram limita dados públicos para não-logados

**Solução:**

1. Teste manualmente em janela anônima:
   ```
   https://instagram.com/USERNAME
   ```

2. Veja quantos posts são exibidos sem login

3. Ajuste `--limit` conforme disponibilidade

4. Use filtros de data para limitar escopo:
   ```bash
   python3 scripts/instagram-scraper/scrape_user_posts.py "user" \
     --newer-than "2024-01-01" \
     --limit 50
   ```

### Timeout ao extrair grande volume

**Causa:** Extração de muitos dados

**Solução:**

1. Aumente timeout:
   ```bash
   python3 tools/apify_instagram.py \
     --user "natgeo" \
     --limit 500 \
     --timeout 600
   ```

2. Divida em batches menores:
   ```bash
   # Ao invés de 1000 de uma vez
   python3 scripts/instagram-scraper/scrape_user_posts.py "user" --limit 200
   ```

### Perfil privado retorna poucos dados

**Esperado:** Perfis privados só expõem dados básicos

**Dados disponíveis:**
- username, fullName
- biography
- profilePicUrl
- followersCount, followsCount
- verified, private (true)

**Dados indisponíveis:**
- latestPosts
- latestIgtvVideos

### Custo maior que esperado

**Causa:** `resultsLimit` muito alto ou scraping repetido

**Solução:**

1. Use `--limit` apropriado:
   ```bash
   # Ao invés de 1000
   python3 scripts/instagram-scraper/scrape_user_posts.py "user" --limit 50
   ```

2. Salve resultados em arquivo para evitar re-scraping:
   ```bash
   python3 scripts/instagram-scraper/scrape_user_posts.py "user" \
     --output resultados.json
   ```

3. Processe arquivo local posteriormente:
   ```python
   import json
   with open("resultados.json") as f:
       data = json.load(f)
       items = data["items"]
   ```

---

## 📚 Recursos Adicionais

### Documentação

- **README:** `scripts/instagram-scraper/README.md`
- **Este arquivo:** `docs/tools/apify_instagram.md`
- **Configuração:** `config/apify_config.py`
- **Ferramenta:** `tools/apify_instagram.py`
- **Templates:** `scripts/instagram-scraper/*.py`

### Links Úteis

- **Apify Docs:** https://apify.com/apify/instagram-scraper
- **Apify Console:** https://console.apify.com/
- **Pricing:** https://apify.com/pricing

### Outras Ferramentas Apify

- **Instagram Profile Scraper:** Foco em perfis
- **Instagram Hashtag Scraper:** Foco em hashtags
- **Instagram Post Scraper:** Foco em posts únicos
- **Instagram Comments Scraper:** Foco em comentários

**Quando usar o Instagram Scraper genérico:**
- Precisa de flexibilidade (posts, comentários, perfis)
- Quer controlar todos parâmetros
- Uso avançado com filtros de data

**Quando usar scrapers dedicados:**
- Scraping de grande volume de um tipo específico
- Máxima velocidade (menos configuração)
- Uso simplificado

---

## 📞 Suporte

**Problemas com a ferramenta:**
- Verifique `scripts/instagram-scraper/README.md`
- Consulte este arquivo
- Teste com `--limit 10` primeiro

**Problemas com Apify:**
- Console: https://console.apify.com/
- Docs: https://docs.apify.com/
- Support: https://apify.com/contact

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
**Status:** ✅ Produção (5 templates testados)
