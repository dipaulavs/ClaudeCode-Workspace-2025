# 🎵 TikTok API23 - Documentação Completa

**Ferramenta completa para integração com TikTok API23 via RapidAPI**

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso Básico](#uso-básico)
- [Endpoints Disponíveis](#endpoints-disponíveis)
  - [User (12 endpoints)](#1-user-12-endpoints)
  - [Search (4 endpoints)](#2-search-4-endpoints)
  - [Post/Video (5 endpoints)](#3-postvideo-5-endpoints)
  - [Trending/Ads (13 endpoints)](#4-trendingads-13-endpoints)
  - [Challenge/Hashtag (2 endpoints)](#5-challengehashtag-2-endpoints)
  - [Place (2 endpoints)](#6-place-2-endpoints)
- [Exemplos Práticos](#exemplos-práticos)
- [Scripts Templates](#scripts-templates)
- [Rate Limits](#rate-limits)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

**TikTok API23** é uma API completa e rápida para extração de dados do TikTok, disponível via RapidAPI.

### Características:
- ✅ **38 endpoints** completos
- ✅ **6 categorias:** User, Search, Post, Trending, Challenge, Place
- ✅ **Dados em tempo real** sem rate limits extremos
- ✅ **Sem autenticação TikTok** (usa RapidAPI key)
- ✅ **Retry automático** em caso de falhas

### O que você pode fazer:
- 📊 Analisar perfis, seguidores, posts
- 🔍 Buscar vídeos, hashtags, usuários
- 📈 Monitorar trending (vídeos, músicas, hashtags, produtos)
- 💬 Extrair comentários e respostas
- 🎯 Pesquisar anúncios e criadores em alta
- 📍 Analisar posts por localização

---

## 📦 Instalação

### 1. Dependências

Nenhuma dependência externa necessária! Usa apenas bibliotecas nativas do Python:
- `http.client` (requisições HTTP)
- `json` (parse de respostas)
- `urllib.parse` (encoding de URLs)

### 2. Verificar instalação

```bash
python3 tools/tiktok_api23.py
```

Se configurado corretamente, deve retornar informações do usuário @tiktok.

---

## ⚙️ Configuração

### 1. API Key (RapidAPI)

Sua API key já está configurada em `config/tiktok_config.py`:

```python
RAPIDAPI_KEY = "82a6c38fa1msh40088bb99ac4883p1bd271jsn604d036bd581"
RAPIDAPI_HOST = "tiktok-api23.p.rapidapi.com"
```

### 2. Customizar configurações

Edite `config/tiktok_config.py` para ajustar:
- `DEFAULT_COUNT`: Quantidade padrão de resultados (30)
- `DEFAULT_CURSOR`: Cursor inicial para paginação (0)
- `MAX_RETRIES`: Tentativas em caso de erro (3)
- `TIMEOUT`: Timeout de requisições em segundos (30)

---

## 🚀 Uso Básico

### Importar e inicializar

```python
from tools.tiktok_api23 import TikTokAPI23

api = TikTokAPI23()
```

### Exemplo simples

```python
# Buscar informações de usuário
result = api.get_user_info("taylorswift")
print(result)
```

### Com tratamento de erros

```python
try:
    result = api.get_user_info("taylorswift")
    print(f"Followers: {result['userInfo']['stats']['followerCount']}")
except Exception as e:
    print(f"Erro: {e}")
```

---

## 📚 Endpoints Disponíveis

### 1️⃣ USER (12 endpoints)

#### `get_user_info(unique_id)`
Obter informações básicas de usuário por @username.

```python
result = api.get_user_info("taylorswift")
# Retorna: nickname, bio, followers, following, likes, vídeos, etc.
```

**Parâmetros:**
- `unique_id` (str): Username do TikTok (sem @)

---

#### `get_user_info_with_region(unique_id)`
Obter informações de usuário com dados de região.

```python
result = api.get_user_info_with_region("tiktok")
# Retorna: info do usuário + dados de região/país
```

---

#### `get_user_info_by_id(user_id)`
Obter informações por ID numérico do usuário.

```python
result = api.get_user_info_by_id("107955")
# Útil quando você tem apenas o userId
```

---

#### `get_user_followers(sec_uid, count=30, min_cursor=0)`
Listar seguidores de um usuário.

```python
result = api.get_user_followers(
    sec_uid="MS4wLjABAAAAqB08cUbXaDWqbD6MCga2RbGTuhfO2EsHayBYx08NDrN7IE3jQuRDNNN6YwyfH6_6",
    count=50
)
# Retorna: lista de seguidores + hasMore + minCursor (paginação)
```

**Parâmetros:**
- `sec_uid` (str): ID seguro do usuário (obtido em get_user_info)
- `count` (int): Quantidade de seguidores (padrão: 30)
- `min_cursor` (int): Cursor para próxima página (padrão: 0)

---

#### `get_user_followings(sec_uid, count=30, min_cursor=0, max_cursor=0)`
Listar quem o usuário segue.

```python
result = api.get_user_followings(
    sec_uid="MS4wLjABAAAAY3pcRUgWNZAUWlErRzIyrWoc1cMUIdws4KMQQAS5aKN9AD1lcmx5IvCXMUJrP2dB"
)
```

---

#### `get_user_popular_posts(sec_uid, count=35, cursor=0)`
Posts mais populares do usuário (ordenados por engajamento).

```python
result = api.get_user_popular_posts(
    sec_uid="MS4wLjABAAAAqB08cUbXaDWqbD6MCga2RbGTuhfO2EsHayBYx08NDrN7IE3jQuRDNNN6YwyfH6_6"
)
# Retorna: vídeos com mais likes/comentários/shares
```

---

#### `get_user_oldest_posts(sec_uid, count=30, cursor=0)`
Posts mais antigos do usuário (ordem cronológica inversa).

```python
result = api.get_user_oldest_posts(sec_uid="...")
```

---

#### `get_user_liked_posts(sec_uid, count=30, cursor=0)`
Posts curtidos pelo usuário (se perfil público).

```python
result = api.get_user_liked_posts(sec_uid="...")
```

⚠️ **Nota:** Só funciona se o usuário tem likes públicos.

---

#### `get_user_playlist(sec_uid, count=20, cursor=0)`
Playlists criadas pelo usuário.

```python
result = api.get_user_playlist(sec_uid="...")
```

---

#### `get_user_repost(sec_uid, count=30, cursor=0)`
Reposts feitos pelo usuário.

```python
result = api.get_user_repost(sec_uid="...")
```

---

#### `get_user_story(user_id, max_cursor=0)`
Stories ativos do usuário (24h).

```python
result = api.get_user_story(user_id="6881290705605477381")
```

⚠️ **Nota:** Stories expiram em 24h.

---

### 2️⃣ SEARCH (4 endpoints)

#### `search_general(keyword, cursor=0, search_id=0)`
Busca geral (mistura vídeos, usuários, hashtags).

```python
result = api.search_general("cat")
# Retorna: vídeos, accounts, hashtags relacionados
```

---

#### `search_videos(keyword, cursor=0, search_id=0)`
Buscar apenas vídeos.

```python
result = api.search_videos("cat", cursor=0)
# Retorna: lista de vídeos + cursor para próxima página
```

---

#### `search_accounts(keyword, cursor=0, search_id=0)`
Buscar apenas contas/usuários.

```python
result = api.search_accounts("taylor")
# Retorna: lista de usuários correspondentes
```

---

#### `search_others_searched_for(keyword)`
Sugestões de busca relacionadas (autocomplete).

```python
result = api.search_others_searched_for("cat")
# Retorna: ["cat videos", "cat funny", "cat cute", ...]
```

---

### 3️⃣ POST/VIDEO (5 endpoints)

#### `get_post_detail(video_id)`
Detalhes completos de um vídeo.

```python
result = api.get_post_detail("7306132438047116586")
# Retorna: título, descrição, likes, shares, comentários, música, autor, etc.
```

---

#### `get_post_comments(video_id, count=50, cursor=0)`
Comentários de um vídeo.

```python
result = api.get_post_comments(
    video_id="6574657885953933314",
    count=100
)
# Retorna: lista de comentários + hasMore + cursor
```

---

#### `get_comment_replies(video_id, comment_id, count=6, cursor=0)`
Respostas de um comentário específico.

```python
result = api.get_comment_replies(
    video_id="7230348754455481601",
    comment_id="7230359281404740357"
)
```

---

#### `get_trending_posts(count=16)`
Vídeos em trending/alta no TikTok.

```python
result = api.get_trending_posts(count=30)
# Retorna: vídeos virais atuais
```

---

#### `explore_posts(category_type=119, count=16)`
Explorar vídeos por categoria.

```python
result = api.explore_posts(category_type=119, count=20)
# category_type: código da categoria (ex: 119 = entretenimento)
```

---

### 4️⃣ TRENDING/ADS (13 endpoints)

#### `get_trending_ads_detail(ads_id)`
Detalhes de um anúncio em trending.

```python
result = api.get_trending_ads_detail("7169172119488577537")
```

---

#### `get_trending_ads(page=1, period=7, limit=20, country="US", order_by="ctr")`
Anúncios em alta.

```python
result = api.get_trending_ads(
    period=7,        # últimos 7 dias
    country="BR",    # Brasil
    order_by="ctr"   # ordenar por CTR
)
```

**Parâmetros:**
- `period`: Período em dias (7, 30, etc.)
- `country`: Código do país (US, BR, etc.)
- `order_by`: `ctr`, `impressions`, `engagement`

---

#### `get_trending_creators(page=1, limit=20, sort_by="follower", country="US")`
Criadores em alta.

```python
result = api.get_trending_creators(
    country="BR",
    sort_by="engagement"
)
```

---

#### `get_trending_hashtags(page=1, limit=20, period=120, country="US", sort_by="popular")`
Hashtags em alta.

```python
result = api.get_trending_hashtags(
    period=24,      # últimas 24h
    country="BR"
)
```

**Parâmetros:**
- `period`: Período em **horas** (24, 120, etc.)

---

#### `get_trending_songs(page=1, limit=20, period=7, rank_type="popular", country="US")`
Músicas em alta.

```python
result = api.get_trending_songs(period=7, country="BR")
```

---

#### `get_trending_keywords(page=1, limit=20, period=7, country="US")`
Keywords em alta.

```python
result = api.get_trending_keywords(country="BR")
```

---

#### `get_commercial_music_playlist_detail(playlist_id, page=1, limit=20, region="US")`
Detalhes de playlist da biblioteca comercial.

```python
result = api.get_commercial_music_playlist_detail(
    playlist_id="6929526806429469442"
)
```

---

#### `get_commercial_music_playlists(limit=20, region="US")`
Listar playlists da biblioteca comercial.

```python
result = api.get_commercial_music_playlists(region="US")
```

---

#### `get_commercial_music_library(page=1, limit=20, region="US", scenarios=0, duration=0)`
Músicas da biblioteca comercial (uso em anúncios).

```python
result = api.get_commercial_music_library(region="US")
```

---

#### `get_top_products(page=1, last=7, order_by="post", order_type="desc")`
Produtos em alta (TikTok Shop).

```python
result = api.get_top_products(
    last=30,           # últimos 30 dias
    order_by="sales"   # ordenar por vendas
)
```

---

#### `get_top_product_detail(product_id)`
Detalhes de produto em alta.

```python
result = api.get_top_product_detail("601226")
```

---

#### `get_top_product_metrics(product_id)`
Métricas de produto em alta.

```python
result = api.get_top_product_metrics("601226")
# Retorna: vendas, posts, engajamento, etc.
```

---

### 5️⃣ CHALLENGE/HASHTAG (2 endpoints)

#### `get_challenge_info(challenge_name)`
Informações de uma hashtag.

```python
result = api.get_challenge_info("xh")
# Retorna: descrição, views, posts, etc.
```

**Parâmetros:**
- `challenge_name`: Nome da hashtag (sem #)

---

#### `get_challenge_posts(challenge_id, count=30, cursor=0)`
Posts de uma hashtag.

```python
result = api.get_challenge_posts(
    challenge_id="763263",
    count=50
)
```

---

### 6️⃣ PLACE (2 endpoints)

#### `get_place_info(place_id)`
Informações de um local.

```python
result = api.get_place_info("22535796481538024")
# Retorna: nome, endereço, coordenadas, etc.
```

---

#### `get_place_posts(place_id, count=30, cursor=0)`
Posts marcados em um local.

```python
result = api.get_place_posts(
    place_id="22535796481538024",
    count=50
)
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Analisar perfil completo

```python
from tools.tiktok_api23 import TikTokAPI23

api = TikTokAPI23()

# 1. Info do usuário
user = api.get_user_info("taylorswift")
print(f"Followers: {user['userInfo']['stats']['followerCount']}")

# 2. Posts populares
sec_uid = user['userInfo']['user']['secUid']
posts = api.get_user_popular_posts(sec_uid, count=10)
print(f"Top 10 posts: {len(posts['itemList'])}")
```

---

### Exemplo 2: Monitorar trending

```python
# Vídeos em alta
trending = api.get_trending_posts(count=20)

# Hashtags em alta (últimas 24h)
hashtags = api.get_trending_hashtags(period=24, country="BR")

# Músicas em alta
songs = api.get_trending_songs(period=7, country="BR")

print(f"Vídeos: {len(trending['itemList'])}")
print(f"Hashtags: {len(hashtags['data'])}")
print(f"Músicas: {len(songs['data'])}")
```

---

### Exemplo 3: Analisar vídeo específico

```python
video_id = "7306132438047116586"

# Detalhes do vídeo
details = api.get_post_detail(video_id)
print(f"Likes: {details['itemInfo']['itemStruct']['stats']['diggCount']}")

# Comentários
comments = api.get_post_comments(video_id, count=100)
print(f"Total comentários: {len(comments['comments'])}")

# Respostas de comentário específico
if comments['comments']:
    comment_id = comments['comments'][0]['cid']
    replies = api.get_comment_replies(video_id, comment_id)
    print(f"Respostas: {len(replies['comments'])}")
```

---

### Exemplo 4: Buscar e analisar

```python
keyword = "cat"

# Buscar vídeos
videos = api.search_videos(keyword, cursor=0)

# Buscar usuários
users = api.search_accounts(keyword)

# Sugestões relacionadas
suggestions = api.search_others_searched_for(keyword)

print(f"Vídeos encontrados: {len(videos['data'])}")
print(f"Usuários encontrados: {len(users['data'])}")
print(f"Sugestões: {suggestions}")
```

---

## 📜 Scripts Templates

**Localização:** `scripts/tiktok/`

### Templates disponíveis:

1. **`get_user_info.py`** - Obter info de usuário
2. **`get_video_info.py`** - Obter info de vídeo
3. **`search_content.py`** - Buscar vídeos/usuários
4. **`get_trending.py`** - Monitorar trending
5. **`analyze_hashtag.py`** - Analisar hashtag

### Como usar:

```bash
# Info de usuário
python3 scripts/tiktok/get_user_info.py --username taylorswift

# Info de vídeo
python3 scripts/tiktok/get_video_info.py --video-id 7306132438047116586

# Buscar vídeos
python3 scripts/tiktok/search_content.py --keyword "cat" --type video

# Trending
python3 scripts/tiktok/get_trending.py --type videos --count 20

# Analisar hashtag
python3 scripts/tiktok/analyze_hashtag.py --hashtag xh
```

**Docs completa:** `scripts/tiktok/README.md`

---

## ⏱️ Rate Limits

### RapidAPI Limits (verificar seu plano):

- **Free Plan:** ~100-500 requests/mês
- **Basic Plan:** ~10.000 requests/mês
- **Pro/Ultra:** Unlimited

### Verificar uso:

Acesse: https://rapidapi.com/developer/billing

### Retry automático:

A ferramenta já implementa retry automático (3 tentativas) em caso de:
- Timeout
- Erros 5xx (servidor)
- Falhas de conexão

---

## 🔧 Troubleshooting

### Erro: `401 Unauthorized`

**Causa:** API key inválida ou expirada.

**Solução:**
1. Verificar key em `config/tiktok_config.py`
2. Renovar key no RapidAPI se necessário
3. Verificar se está assinando a API no RapidAPI Hub

---

### Erro: `429 Too Many Requests`

**Causa:** Rate limit excedido.

**Solução:**
1. Aguardar reset do limite (geralmente 1h ou 24h)
2. Upgrade de plano no RapidAPI
3. Implementar cache local para reduzir chamadas

---

### Erro: `Timeout after 30 seconds`

**Causa:** Requisição demorou muito.

**Solução:**
1. Aumentar `TIMEOUT` em `config/tiktok_config.py`
2. Verificar conexão com internet
3. Tentar novamente (retry automático já implementado)

---

### Dados vazios ou incompletos

**Causa:** Perfil privado ou conteúdo indisponível.

**Solução:**
1. Verificar se perfil é público
2. Verificar se vídeo não foi deletado
3. Alguns endpoints (liked_posts) só funcionam em perfis públicos

---

### `sec_uid` não encontrado

**Causa:** Precisa buscar `sec_uid` antes de usar outros endpoints.

**Solução:**
```python
# Primeiro buscar usuário para obter sec_uid
user = api.get_user_info("taylorswift")
sec_uid = user['userInfo']['user']['secUid']

# Agora usar sec_uid
posts = api.get_user_popular_posts(sec_uid)
```

---

## 📊 Estrutura de Resposta

### Padrão geral:

```json
{
  "status": "success",
  "data": { ... },
  "message": "OK"
}
```

### User Info:

```json
{
  "userInfo": {
    "user": {
      "id": "...",
      "uniqueId": "taylorswift",
      "nickname": "Taylor Swift",
      "secUid": "...",
      ...
    },
    "stats": {
      "followerCount": 1000000,
      "followingCount": 100,
      "videoCount": 50,
      "heartCount": 5000000
    }
  }
}
```

### Post Detail:

```json
{
  "itemInfo": {
    "itemStruct": {
      "id": "...",
      "desc": "descrição do vídeo",
      "author": { ... },
      "stats": {
        "diggCount": 10000,
        "shareCount": 500,
        "commentCount": 200,
        "playCount": 100000
      },
      "music": { ... }
    }
  }
}
```

---

## 🎯 Boas Práticas

### 1. Cache de resultados

```python
import json
from datetime import datetime, timedelta

def cache_result(key, data, ttl_hours=1):
    """Cachear resultado por N horas"""
    cache_file = f"cache/{key}.json"
    with open(cache_file, 'w') as f:
        json.dump({
            'data': data,
            'expires_at': (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
        }, f)

def get_cached(key):
    """Buscar do cache se não expirado"""
    cache_file = f"cache/{key}.json"
    try:
        with open(cache_file, 'r') as f:
            cached = json.load(f)
            if datetime.fromisoformat(cached['expires_at']) > datetime.now():
                return cached['data']
    except:
        pass
    return None
```

---

### 2. Paginação eficiente

```python
def get_all_user_posts(sec_uid, max_posts=100):
    """Buscar todos os posts com paginação"""
    all_posts = []
    cursor = 0

    while len(all_posts) < max_posts:
        result = api.get_user_popular_posts(sec_uid, count=30, cursor=cursor)

        if not result.get('itemList'):
            break

        all_posts.extend(result['itemList'])

        if not result.get('hasMore'):
            break

        cursor = result.get('cursor', 0)

    return all_posts[:max_posts]
```

---

### 3. Tratamento robusto de erros

```python
def safe_api_call(func, *args, **kwargs):
    """Wrapper seguro para chamadas API"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Erro na API: {e}")
        return None
```

---

## 📞 Suporte

**Ferramenta:** `tools/tiktok_api23.py`
**Config:** `config/tiktok_config.py`
**Docs:** `docs/tools/tiktok_api23.md`
**Scripts:** `scripts/tiktok/`

**RapidAPI Hub:** https://rapidapi.com/Lundehund/api/tiktok-api23
**Suporte RapidAPI:** https://rapidapi.com/Lundehund/api/tiktok-api23/discussions

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
**Total de endpoints:** 38
