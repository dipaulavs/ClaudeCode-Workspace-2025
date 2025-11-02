# Apify Twitter Scraper

Ferramenta completa para scraping de tweets, perfis, conversas e listas do Twitter/X usando a API do Apify.

## 🎯 Recursos

- ✅ **Busca avançada** com filtros (data, mídia, verificados, etc)
- ✅ **Scraping de perfis** (histórico de tweets)
- ✅ **Scraping de tweets específicos** (por URL)
- ✅ **Scraping de replies/conversas**
- ✅ **Scraping de listas do Twitter**
- ✅ **Geolocalização** (tweets por localização)
- ✅ **Filtros de engajamento** (min retweets, likes, replies)
- ✅ **Query Wizard** para buscas complexas
- ✅ **Batch processing** (múltiplos perfis/termos)

## 💰 Pricing

- **Custo:** $0.30 por 1000 tweets
- **Performance:** 30-80 tweets/segundo
- **Demo Mode:** Usuários Free Plan podem coletar máximo 5 tweets
- **Actor ID:** `61RPP7dywgiy0JPD0`

## 📋 Pré-requisitos

```bash
# Instalar dependência
pip3 install apify-client

# Configurar API key (já está em config/apify_config.py)
APIFY_API_TOKEN="apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
```

## 🚀 Quick Start

### Templates Prontos (Recomendado)

```bash
# Busca simples
python3 scripts/twitter/search_twitter.py "inteligência artificial" --max-items 100

# Scraping de perfil
python3 scripts/twitter/scrape_profile.py NASA --year 2024

# Scraping de tweets específicos
python3 scripts/twitter/scrape_tweets.py "https://twitter.com/elonmusk/status/123..."

# Scraping de replies
python3 scripts/twitter/scrape_replies.py 1728108619189874825

# Batch (múltiplos perfis)
python3 scripts/twitter/batch_twitter.py --handles NASA SpaceX --max-items 500
```

### Ferramenta Base (Python)

```python
from tools.apify_twitter import ApifyTwitterScraper

scraper = ApifyTwitterScraper()

# Busca simples
result = scraper.scrape(
    search_terms=["inteligência artificial"],
    max_items=100
)

# Scraping de perfil
result = scraper.scrape(
    twitter_handles=["NASA"],
    max_items=500
)

# Scraping de tweets específicos
result = scraper.scrape(
    start_urls=["https://twitter.com/user/status/123..."]
)
```

## 📚 Guia de Uso Detalhado

### 1. Busca Avançada (`search_twitter.py`)

#### Busca Simples

```bash
# Busca básica
python3 scripts/twitter/search_twitter.py "python"

# Com hashtag
python3 scripts/twitter/search_twitter.py "#ai #machinelearning"

# Múltiplos termos
python3 scripts/twitter/search_twitter.py "python" "javascript" "rust"
```

#### Com Filtros

```bash
# Idioma específico
python3 scripts/twitter/search_twitter.py "ai" --lang pt

# Apenas verificados
python3 scripts/twitter/search_twitter.py "tech news" --verified

# Apenas com imagens
python3 scripts/twitter/search_twitter.py "cats" --images

# Engajamento mínimo
python3 scripts/twitter/search_twitter.py "viral" --min-likes 1000 --min-retweets 500
```

#### Com Período

```bash
# Período específico
python3 scripts/twitter/search_twitter.py "ChatGPT" --since 2024-01-01 --until 2024-12-31

# Últimos 30 dias (usar data dinâmica)
python3 scripts/twitter/search_twitter.py "breaking news" --since 2024-11-01
```

#### Operadores Avançados

```bash
# OR (qualquer termo)
python3 scripts/twitter/search_twitter.py "(python OR javascript) tutorial"

# Excluir termo
python3 scripts/twitter/search_twitter.py "python -javascript"

# Frase exata
python3 scripts/twitter/search_twitter.py '"machine learning"'

# Sem retweets
python3 scripts/twitter/search_twitter.py "ai -filter:retweets"

# De usuário específico
python3 scripts/twitter/search_twitter.py "from:NASA space"

# Para usuário específico
python3 scripts/twitter/search_twitter.py "to:elonmusk"

# Menciona usuário
python3 scripts/twitter/search_twitter.py "@NASA"

# Combinações complexas
python3 scripts/twitter/search_twitter.py "(python OR javascript) tutorial -filter:retweets min_faves:50"
```

### 2. Scraping de Perfis (`scrape_profile.py`)

#### Scraping Simples

```bash
# Últimos ~800 tweets
python3 scripts/twitter/scrape_profile.py elonmusk

# Com limite
python3 scripts/twitter/scrape_profile.py NASA --max-items 5000
```

#### Histórico por Ano

```bash
# Ano específico (divide por mês automaticamente)
python3 scripts/twitter/scrape_profile.py NASA --year 2023

# Múltiplos anos
python3 scripts/twitter/scrape_profile.py NASA --from-year 2020 --to-year 2024
```

**⚠️ Importante:** Twitter retorna ~800 tweets por busca. O script divide automaticamente em períodos mensais para coletar histórico completo.

#### Período Customizado

```bash
# Período específico
python3 scripts/twitter/scrape_profile.py NASA --since 2024-01-01 --until 2024-06-30
```

#### Com Filtros

```bash
# Apenas com imagens
python3 scripts/twitter/scrape_profile.py NASA --year 2023 --images

# Alto engajamento
python3 scripts/twitter/scrape_profile.py NASA --year 2023 --min-likes 1000
```

### 3. Scraping de Tweets Específicos (`scrape_tweets.py`)

#### Tweet Único

```bash
# URL completa
python3 scripts/twitter/scrape_tweets.py "https://twitter.com/elonmusk/status/1728108619189874825"

# URL do x.com (também funciona)
python3 scripts/twitter/scrape_tweets.py "https://x.com/elonmusk/status/1728108619189874825"
```

#### Múltiplos Tweets

```bash
# Múltiplas URLs
python3 scripts/twitter/scrape_tweets.py "URL1" "URL2" "URL3"

# De arquivo
python3 scripts/twitter/scrape_tweets.py --from-file urls.txt
```

**Formato do arquivo `urls.txt`:**
```
https://twitter.com/user1/status/123
https://twitter.com/user2/status/456
# Comentários são ignorados
https://x.com/user3/status/789
```

### 4. Scraping de Replies/Conversas (`scrape_replies.py`)

#### Todas as Replies

```bash
# Por ID do tweet
python3 scripts/twitter/scrape_replies.py 1728108619189874825

# Por URL
python3 scripts/twitter/scrape_replies.py "https://twitter.com/user/status/1728108619189874825"
```

#### Com Filtros

```bash
# Com hashtag específica
python3 scripts/twitter/scrape_replies.py 1728108619189874825 --hashtag ai

# Apenas verificados
python3 scripts/twitter/scrape_replies.py 1728108619189874825 --verified

# Alto engajamento
python3 scripts/twitter/scrape_replies.py 1728108619189874825 --min-likes 10
```

### 5. Batch Processing (`batch_twitter.py`)

#### Múltiplos Perfis

```bash
# Lista de handles
python3 scripts/twitter/batch_twitter.py --handles NASA SpaceX elonmusk

# De arquivo
python3 scripts/twitter/batch_twitter.py --handles-file handles.txt
```

**Formato do arquivo `handles.txt`:**
```
NASA
SpaceX
elonmusk
# Comentários são ignorados
```

#### Múltiplos Termos de Busca

```bash
# Lista de termos
python3 scripts/twitter/batch_twitter.py --search "ai" "machine learning" "deep learning"

# De arquivo
python3 scripts/twitter/batch_twitter.py --search-file searches.txt
```

#### Mix de Perfis e Buscas

```bash
python3 scripts/twitter/batch_twitter.py \
  --handles NASA SpaceX \
  --search "space exploration" "mars mission" \
  --max-items 1000
```

#### Arquivos Separados por Query

```bash
# Salva cada query em arquivo separado
python3 scripts/twitter/batch_twitter.py \
  --handles NASA SpaceX elonmusk \
  --separate-files \
  --max-per-query 500
```

## 🔧 Parâmetros da Ferramenta Base

### Principais Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `start_urls` | list | URLs do Twitter (tweets, perfis, listas) |
| `search_terms` | list | Termos de busca (suporta operadores) |
| `twitter_handles` | list | Handles (@usuario) |
| `conversation_ids` | list | IDs de conversas |
| `max_items` | int | Número máximo de tweets |

### Filtros Básicos

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `tweet_language` | str | Código ISO 639-1 (pt, en, es, etc) |
| `only_verified_users` | bool | Apenas usuários verificados |
| `only_twitter_blue` | bool | Apenas Twitter Blue |
| `only_image` | bool | Apenas tweets com imagens |
| `only_video` | bool | Apenas tweets com vídeos |
| `only_quote` | bool | Apenas quote tweets |

### Filtros de Usuário

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `author` | str | Handle do autor (sem @) |
| `in_reply_to` | str | Handle do usuário respondido (sem @) |
| `mentioning` | str | Handle do usuário mencionado (sem @) |

### Filtros de Localização

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `geotagged_near` | str | Tweets próximos a localização |
| `within_radius` | str | Raio da busca geográfica |
| `geocode` | str | Lat/long para geocoding |
| `place_object_id` | str | ID do lugar no Twitter |

### Filtros de Engajamento

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `minimum_retweets` | int | Número mínimo de retweets |
| `minimum_favorites` | int | Número mínimo de likes |
| `minimum_replies` | int | Número mínimo de replies |

### Filtros de Data

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `start_date` | str | Data inicial (YYYY-MM-DD) |
| `end_date` | str | Data final (YYYY-MM-DD) |

### Outras Opções

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `sort` | str | Ordenação (Latest, Top, Relevance) |
| `include_search_terms` | bool | Incluir termo de busca nos resultados |

## 📊 Estrutura do Output

### Tweet Completo

```json
{
  "type": "tweet",
  "id": "1728108619189874825",
  "url": "https://x.com/elonmusk/status/1728108619189874825",
  "text": "More than 10 per human on average",
  "retweetCount": 11311,
  "replyCount": 6526,
  "likeCount": 104121,
  "quoteCount": 2915,
  "bookmarkCount": 702,
  "createdAt": "Fri Nov 24 17:49:36 +0000 2023",
  "lang": "en",
  "isReply": false,
  "isRetweet": false,
  "isQuote": true,
  "author": {
    "userName": "elonmusk",
    "name": "Elon Musk",
    "id": "44196397",
    "isVerified": true,
    "isBlueVerified": true,
    "followers": 172669889,
    "following": 538,
    "profilePicture": "https://...",
    "description": "...",
    "location": "..."
  },
  "media": [],
  "extendedEntities": {}
}
```

### Estatísticas Automáticas

Os scripts geram automaticamente:

- Total de tweets
- Total de retweets, likes, replies
- Top autores
- Distribuição por idioma
- Tipos de tweet (originais, RTs, quotes, replies)
- Estatísticas de mídia

## 🎓 Casos de Uso

### 1. Monitoramento de Marca

```bash
# Mencões à marca
python3 scripts/twitter/search_twitter.py "MinhaEmpresa OR @MinhaEmpresa" \
  --since 2024-11-01 \
  --max-items 1000

# Análise de sentimento (coletar para processar)
python3 scripts/twitter/search_twitter.py "MinhaEmpresa" \
  --min-replies 5 \
  --max-items 500
```

### 2. Análise de Competidores

```bash
# Tweets de competidores
python3 scripts/twitter/batch_twitter.py \
  --handles competidor1 competidor2 competidor3 \
  --year 2024 \
  --separate-files
```

### 3. Pesquisa de Tendências

```bash
# Trending topics
python3 scripts/twitter/search_twitter.py "#trending #viral" \
  --min-retweets 1000 \
  --since 2024-11-01 \
  --sort Top
```

### 4. Análise de Influenciadores

```bash
# Perfil completo
python3 scripts/twitter/scrape_profile.py influenciador \
  --from-year 2020 \
  --to-year 2024

# Apenas high engagement
python3 scripts/twitter/scrape_profile.py influenciador \
  --year 2024 \
  --min-likes 1000 \
  --min-retweets 100
```

### 5. Coleta de Dados para Treinamento de IA

```bash
# Dataset de tweets em português sobre IA
python3 scripts/twitter/search_twitter.py \
  "inteligência artificial OR machine learning OR deep learning" \
  --lang pt \
  --since 2024-01-01 \
  --max-items 10000
```

### 6. Análise de Eventos

```bash
# Cobertura de evento
python3 scripts/twitter/search_twitter.py "#NomeDoEvento" \
  --since 2024-11-01 \
  --until 2024-11-03 \
  --max-items 5000
```

## ⚠️ Regras de Uso (Importante!)

### ❌ PROIBIDO

1. **Monitoramento em tempo real:** Não use para monitorar atividades (rodar mesma query repetidamente em curto período)
2. **Poucos tweets:** Mínimo de 50 tweets por query (ou 250 se batching 5 queries)
3. **Single tweet:** Proibido buscar tweet único por URL (exceto com permissão)

### ✅ PERMITIDO

1. **Histórico:** Buscar tweets históricos
2. **Delay:** 2+ minutos entre runs
3. **Concorrência:** Máximo 1 run por vez (max 5 queries batched)

### 💡 Boas Práticas

- Use períodos (since/until) para dividir grandes coletas
- Prefira batch processing quando possível
- Respeite os limites de rate
- Salve resultados localmente para evitar re-scraping

## 🔍 Operadores de Busca Avançados

### Operadores Básicos

| Operador | Exemplo | Descrição |
|----------|---------|-----------|
| `OR` | `python OR javascript` | Qualquer termo |
| `AND` | `python javascript` | Ambos os termos (implícito) |
| `" "` | `"machine learning"` | Frase exata |
| `-` | `python -javascript` | Excluir termo |

### Filtros de Tipo

| Filtro | Exemplo | Descrição |
|--------|---------|-----------|
| `filter:media` | `gato filter:media` | Com qualquer mídia |
| `filter:images` | `gato filter:images` | Apenas com imagens |
| `filter:videos` | `gato filter:videos` | Apenas com vídeos |
| `-filter:retweets` | `ai -filter:retweets` | Sem retweets |
| `filter:replies` | `ai filter:replies` | Apenas replies |
| `filter:quote` | `ai filter:quote` | Apenas quotes |

### Filtros de Usuário

| Filtro | Exemplo | Descrição |
|--------|---------|-----------|
| `from:` | `from:NASA` | Tweets de @NASA |
| `to:` | `to:elonmusk` | Replies para @elonmusk |
| `@` | `@NASA` | Menciona @NASA |

### Filtros de Engajamento

| Filtro | Exemplo | Descrição |
|--------|---------|-----------|
| `min_faves:` | `ai min_faves:100` | Mínimo 100 likes |
| `min_retweets:` | `ai min_retweets:50` | Mínimo 50 RTs |
| `min_replies:` | `ai min_replies:10` | Mínimo 10 replies |

### Filtros de Data

| Filtro | Exemplo | Descrição |
|--------|---------|-----------|
| `since:` | `ai since:2024-01-01` | A partir de data |
| `until:` | `ai until:2024-12-31` | Até data |

### Filtros de Localização

| Filtro | Exemplo | Descrição |
|--------|---------|-----------|
| `near:` | `terremoto near:Tokyo` | Próximo a local |
| `within:` | `near:Tokyo within:15km` | Raio de busca |

### Exemplos Complexos

```bash
# Tutorial de Python ou JavaScript, sem RTs, mínimo 50 likes
"(python OR javascript) tutorial -filter:retweets min_faves:50"

# Tweets da NASA com imagens, mínimo 100 RTs
"from:NASA filter:images min_retweets:100"

# Mencões a "breaking news" nas últimas 24h, alto engajamento
"breaking news min_faves:1000 since:2024-11-01"
```

## 📁 Estrutura de Arquivos

```
ClaudeCode-Workspace/
├── tools/
│   └── apify_twitter.py          # Ferramenta base
├── scripts/
│   └── twitter/
│       ├── search_twitter.py     # Template busca
│       ├── scrape_profile.py     # Template perfil
│       ├── scrape_tweets.py      # Template tweets
│       ├── scrape_replies.py     # Template replies
│       └── batch_twitter.py      # Template batch
├── config/
│   └── apify_config.py           # Configuração (API key)
└── docs/
    └── tools/
        └── apify_twitter.md      # Esta documentação
```

## 🐛 Troubleshooting

### Erro: "Rate limit exceeded"

**Causa:** Muitas requisições em curto período

**Solução:**
- Aguarde 2+ minutos entre runs
- Reduza número de queries simultâneas
- Use max_items para limitar resultados

### Erro: "Insufficient credits"

**Causa:** Sem créditos no Apify

**Solução:**
- Verifique saldo em https://console.apify.com
- Adicione créditos ou faça upgrade do plano

### Poucos resultados retornados

**Possíveis causas:**
- Filtros muito restritivos
- Período sem tweets
- Perfil com poucos tweets

**Solução:**
- Remova alguns filtros
- Amplie período de busca
- Verifique se query está correta

### Erro: "Actor not found"

**Causa:** Actor ID incorreto

**Solução:**
- Verifique `APIFY_TWITTER_ACTOR_ID` em `config/apify_config.py`
- Deve ser: `61RPP7dywgiy0JPD0`

## 📞 Suporte

- **Docs Apify:** https://apify.com/apidojo/tweet-scraper
- **Twitter Search:** https://github.com/igorbrigadir/twitter-advanced-search
- **Issues:** Entre em contato via Discord ou email (apidojo10@gmail.com)

## 🔗 Links Úteis

- [Apify Console](https://console.apify.com)
- [Twitter Advanced Search Guide](https://github.com/igorbrigadir/twitter-advanced-search)
- [ISO 639-1 Language Codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
- [Twitter API Docs (referência)](https://developer.twitter.com/en/docs)

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
