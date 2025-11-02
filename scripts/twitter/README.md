# Templates Twitter/X (Apify Scraper)

Templates prontos para scraping rápido de tweets, perfis e conversas do Twitter/X.

## 🎯 Templates Disponíveis

| Template | Descrição | Uso Principal |
|----------|-----------|---------------|
| `search_twitter.py` | Busca avançada com filtros | Pesquisar tweets por termo/hashtag |
| `scrape_profile.py` | Scraping de perfis (histórico) | Coletar tweets de um perfil |
| `scrape_tweets.py` | Scraping de tweets específicos | Coletar tweets por URL |
| `scrape_replies.py` | Scraping de replies/conversas | Coletar respostas de um tweet |
| `batch_twitter.py` | Batch de múltiplos perfis/termos | Coletar dados de vários perfis |

## ⚡ Quick Start

### 1. Busca de Tweets (`search_twitter.py`)

```bash
# Busca simples
python3 search_twitter.py "inteligência artificial"

# Com filtros
python3 search_twitter.py "python" --lang pt --verified --min-likes 100

# Período específico
python3 search_twitter.py "ChatGPT" --since 2024-01-01 --until 2024-12-31

# Operadores avançados
python3 search_twitter.py "(python OR javascript) tutorial -filter:retweets"
```

**Principais argumentos:**
- `--max-items N` - Limite de tweets
- `--lang pt` - Idioma (pt, en, es, etc)
- `--verified` - Apenas verificados
- `--images` / `--videos` - Apenas com mídia
- `--min-likes N` / `--min-retweets N` - Engajamento mínimo
- `--since YYYY-MM-DD` / `--until YYYY-MM-DD` - Período
- `--sort Latest|Top|Relevance` - Ordenação

### 2. Scraping de Perfil (`scrape_profile.py`)

```bash
# Últimos ~800 tweets
python3 scrape_profile.py elonmusk

# Ano específico (dividido por mês)
python3 scrape_profile.py NASA --year 2024

# Histórico multi-ano
python3 scrape_profile.py NASA --from-year 2020 --to-year 2024

# Período customizado
python3 scrape_profile.py NASA --since 2024-01-01 --until 2024-06-30

# Com filtros
python3 scrape_profile.py NASA --year 2023 --images --min-likes 1000
```

**Principais argumentos:**
- Handle do perfil (sem @)
- `--year 2024` - Ano específico
- `--from-year 2020 --to-year 2024` - Período multi-ano
- `--since / --until` - Período customizado
- `--max-items N` - Limite de tweets
- Mesmos filtros do search_twitter.py

**⚠️ Nota:** Twitter retorna ~800 tweets por busca. O script divide automaticamente em períodos mensais para histórico completo.

### 3. Scraping de Tweets (`scrape_tweets.py`)

```bash
# Tweet único
python3 scrape_tweets.py "https://twitter.com/elonmusk/status/123..."

# Múltiplos tweets
python3 scrape_tweets.py "URL1" "URL2" "URL3"

# De arquivo
python3 scrape_tweets.py --from-file urls.txt
```

**Formato do arquivo `urls.txt`:**
```
https://twitter.com/user1/status/123
https://twitter.com/user2/status/456
# Comentários ignorados
https://x.com/user3/status/789
```

**Principais argumentos:**
- URLs dos tweets (aceita twitter.com e x.com)
- `--from-file FILE` - Carregar URLs de arquivo
- `--max-items N` - Limite (útil para listas grandes)

### 4. Scraping de Replies (`scrape_replies.py`)

```bash
# Todas as replies de um tweet
python3 scrape_replies.py 1728108619189874825

# Por URL
python3 scrape_replies.py "https://twitter.com/user/status/123..."

# Com hashtag específica
python3 scrape_replies.py 1728108619189874825 --hashtag ai

# Com filtros
python3 scrape_replies.py 1728108619189874825 --verified --min-likes 10
```

**Principais argumentos:**
- ID do tweet ou URL completa
- `--hashtag TAG` - Filtrar por hashtag
- `--max-items N` - Limite de replies
- Mesmos filtros do search_twitter.py

### 5. Batch Processing (`batch_twitter.py`)

```bash
# Múltiplos perfis
python3 batch_twitter.py --handles NASA SpaceX elonmusk --max-items 500

# Múltiplos termos
python3 batch_twitter.py --search "ai" "machine learning" "deep learning"

# Mix
python3 batch_twitter.py --handles NASA SpaceX --search "space exploration"

# De arquivos
python3 batch_twitter.py --handles-file handles.txt --search-file searches.txt

# Arquivos separados por query
python3 batch_twitter.py --handles NASA SpaceX --separate-files --max-per-query 500
```

**Principais argumentos:**
- `--handles HANDLE1 HANDLE2 ...` - Lista de handles
- `--handles-file FILE` - Handles de arquivo
- `--search TERMO1 TERMO2 ...` - Lista de termos
- `--search-file FILE` - Termos de arquivo
- `--max-items N` - Limite total
- `--max-per-query N` - Limite por query
- `--separate-files` - Salvar cada query em arquivo separado
- Mesmos filtros do search_twitter.py

## 📊 Output

Todos os scripts salvam resultados em `~/Downloads/` no formato JSON:

```json
{
  "status": "success",
  "run_id": "...",
  "total_items": 150,
  "stats": {
    "total_tweets": 150,
    "total_retweets": 5432,
    "total_likes": 23456,
    "total_replies": 1234,
    "languages": {"pt": 100, "en": 50},
    "authors": {"NASA": 50, "SpaceX": 100}
  },
  "items": [...]
}
```

### Estrutura do Tweet

```json
{
  "id": "1728108619189874825",
  "url": "https://x.com/user/status/...",
  "text": "Tweet text here...",
  "author": {
    "userName": "nasa",
    "name": "NASA",
    "isVerified": true,
    "followers": 1000000
  },
  "likeCount": 1000,
  "retweetCount": 500,
  "replyCount": 200,
  "createdAt": "...",
  "lang": "en",
  "media": [...]
}
```

## 🎓 Exemplos de Uso Comum

### Monitoramento de Marca

```bash
# Mencões à marca nas últimas 24h
python3 search_twitter.py "MinhaEmpresa OR @MinhaEmpresa" \
  --since 2024-11-01 \
  --max-items 1000
```

### Análise de Competidores

```bash
# Tweets de múltiplos competidores
python3 batch_twitter.py \
  --handles competidor1 competidor2 competidor3 \
  --year 2024 \
  --separate-files
```

### Pesquisa de Tendências

```bash
# Trending topics com alto engajamento
python3 search_twitter.py "#trending #viral" \
  --min-retweets 1000 \
  --since 2024-11-01 \
  --sort Top
```

### Dataset para IA

```bash
# Tweets em português sobre IA
python3 search_twitter.py \
  "inteligência artificial OR machine learning" \
  --lang pt \
  --since 2024-01-01 \
  --max-items 10000
```

### Análise de Evento

```bash
# Cobertura de evento específico
python3 search_twitter.py "#NomeDoEvento" \
  --since 2024-11-01 \
  --until 2024-11-03 \
  --max-items 5000
```

## 🔍 Operadores de Busca Avançados

### Básicos

```bash
# OR (qualquer termo)
"python OR javascript"

# Excluir
"python -javascript"

# Frase exata
'"machine learning"'
```

### Filtros

```bash
# Sem retweets
"ai -filter:retweets"

# Apenas com imagens
"cats filter:images"

# De usuário
"from:NASA space"

# Para usuário
"to:elonmusk questions"

# Menciona usuário
"@NASA"
```

### Engajamento

```bash
# Mínimo de likes
"viral min_faves:1000"

# Mínimo de RTs
"trending min_retweets:500"

# Mínimo de replies
"controversial min_replies:100"
```

### Datas

```bash
# Desde data
"news since:2024-01-01"

# Até data
"news until:2024-12-31"

# Período
"news since:2024-01-01 until:2024-01-31"
```

### Localização

```bash
# Próximo a local
"earthquake near:Tokyo"

# Com raio
"earthquake near:Tokyo within:15km"
```

### Complexos

```bash
# Tutoriais de Python ou JS, sem RTs, alto engajamento
"(python OR javascript) tutorial -filter:retweets min_faves:50"

# NASA com imagens, alto RT
"from:NASA filter:images min_retweets:100"
```

## 💰 Pricing

- **Custo:** $0.30 por 1000 tweets
- **Performance:** 30-80 tweets/segundo
- **Demo Mode:** Máximo 5 tweets (Free Plan)

## ⚠️ Regras de Uso

### ❌ PROIBIDO

1. Monitoramento em tempo real (rodar mesma query repetidamente)
2. Menos de 50 tweets por query
3. Single tweet scraping (exceto com permissão)

### ✅ RECOMENDADO

1. Delay de 2+ minutos entre runs
2. Máximo 1 run concorrente
3. Usar períodos (since/until) para dividir coletas
4. Batch processing quando possível

## 🐛 Troubleshooting

### Poucos resultados

**Possíveis causas:**
- Filtros muito restritivos
- Período sem tweets
- Query incorreta

**Solução:**
- Remova alguns filtros
- Amplie período
- Teste query no Twitter web

### Rate limit

**Causa:** Muitas requests

**Solução:**
- Aguarde 2+ minutos
- Reduza queries simultâneas
- Use max_items para limitar

### Erro de API key

**Causa:** API key inválida

**Solução:**
- Verifique `config/apify_config.py`
- Confirme que tem créditos no Apify

## 📚 Documentação Completa

Para documentação detalhada da ferramenta base e exemplos avançados, consulte:

- **Docs completa:** `docs/tools/apify_twitter.md`
- **Ferramenta base:** `tools/apify_twitter.py`
- **Config:** `config/apify_config.py`

## 🔗 Links Úteis

- [Apify Console](https://console.apify.com)
- [Twitter Advanced Search](https://github.com/igorbrigadir/twitter-advanced-search)
- [Apify Twitter Scraper](https://apify.com/apidojo/tweet-scraper)

---

**Última atualização:** 2025-11-02
**Total de templates:** 5
