# Apify Google Maps Scraper

## 📍 O que é?

Ferramenta para **extração de dados de empresas do Google Maps** usando Apify API. Permite extrair informações completas de estabelecimentos como nome, endereço, telefone, website, avaliações, horários de funcionamento, fotos e muito mais.

## 🎯 Casos de Uso

- **Geração de Leads:** Extrair dados de contato (telefone, website, email) para prospecção de vendas
- **Análise de Mercado:** Identificar saturação de mercado, gaps de serviço, benchmarking
- **Monitoramento de Concorrência:** Rastrear localização, avaliações e reviews de competidores
- **Pesquisa de Mercado:** Analisar empresas por região, categoria, tamanho e popularidade
- **Parcerias e Networking:** Descobrir empresas top-rated para colaboração

## ✨ Recursos Principais

### Dados Extraídos

✅ **Informações Básicas:**
- Nome do estabelecimento
- Categoria/subcategoria
- Endereço completo (rua, cidade, estado, CEP)
- Coordenadas GPS (latitude, longitude)
- Plus Code

✅ **Contato:**
- Telefone (formatado e sem formatação)
- Website
- Email da empresa (via scraping do site)
- Perfis de redes sociais (Instagram, Facebook, LinkedIn, etc)

✅ **Avaliações:**
- Nota média (totalScore)
- Número total de reviews
- Distribuição de reviews (1-5 estrelas)
- Reviews detalhados (texto, data, autor, fotos)
- Respostas do proprietário

✅ **Operação:**
- Horário de funcionamento
- Status (aberto/fechado temporariamente/permanentemente)
- Horários de pico (popular times)
- Reserva de mesa/hotel

✅ **Mídia:**
- Fotos do lugar (até 1 padrão, configurável)
- Fotos dos reviews
- Menu (se disponível)

✅ **Extras:**
- Informações adicionais (acessibilidade, amenidades, etc)
- "Pessoas também pesquisam"
- Perguntas e respostas
- Preços (faixa de preço)
- Hotéis similares próximos (para hotéis)

### Modos de Busca

1. **Busca por termo + localização:** `"restaurantes"` em `"São Paulo, Brasil"`
2. **URL direta:** Link completo do Google Maps
3. **Place ID:** ID único do Google (ex: `ChIJN1t_tDeuEmsRUsoyG83frY4`)
4. **Geolocalização customizada:** Polígono, círculo ou área específica

### Vantagens sobre Google Places API

- ❌ **API oficial:** Limite de 60 resultados por busca
- ✅ **Apify Scraper:** Sem limite (scraping completo da área)
- ✅ **Dados extras:** Histogramas de horários populares, reviews completos
- ✅ **Bypass de restrições:** Não limitado a 120 lugares por área

## 📦 Instalação

```bash
# Instalar dependência (se necessário)
pip3 install apify-client
```

## 🔧 Configuração

A API key já está configurada em `config/apify_config.py`:

```python
APIFY_API_TOKEN = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
GOOGLE_MAPS_SCRAPER_ACTOR_ID = "compass/crawler-google-places"
```

### Configurações Padrão

```python
GOOGLE_MAPS_DEFAULTS = {
    "language": "pt",
    "maxCrawledPlaces": 20,
    "maxReviews": 0,  # 0 = sem reviews (mais rápido)
    "maxImages": 1,
    "includeOpeningHours": True,
    # ... outras configurações
}
```

## 🚀 Uso Rápido (Templates)

### 1. Busca Básica (`scripts/scraping/google_maps_basic.py`)

**Uso mais simples:** termo de busca + localização

```bash
# Restaurantes em São Paulo (20 resultados padrão)
python3 scripts/scraping/google_maps_basic.py "restaurantes" "São Paulo, Brasil"

# Hotéis no Rio (50 resultados)
python3 scripts/scraping/google_maps_basic.py "hotéis" "Rio de Janeiro" --max 50

# Cafeterias em Lisboa (export CSV)
python3 scripts/scraping/google_maps_basic.py "cafeterias" "Lisboa, Portugal" --csv

# Academias em BH com reviews
python3 scripts/scraping/google_maps_basic.py "academias" "Belo Horizonte" --reviews

# Com nome de arquivo customizado
python3 scripts/scraping/google_maps_basic.py "pizzarias" "Curitiba" --output minhas_pizzarias
```

### 2. Busca Avançada (`scripts/scraping/google_maps_advanced.py`)

**Filtros avançados:** categorias múltiplas, geolocalização customizada

```bash
# Múltiplas categorias
python3 scripts/scraping/google_maps_advanced.py \
  --search "restaurantes" \
  --location "São Paulo" \
  --categories "Chinese restaurant,Japanese restaurant,Italian restaurant"

# Busca em círculo (raio de 5km)
python3 scripts/scraping/google_maps_advanced.py \
  --circle -46.6333 -23.5505 --radius 5 \
  --search "academias" --max 100

# Busca em polígono customizado
python3 scripts/scraping/google_maps_advanced.py \
  --polygon "[[[-46.6,-23.5],[-46.7,-23.5],[-46.7,-23.6],[-46.6,-23.6],[-46.6,-23.5]]]" \
  --search "cafeterias"

# URL direta do Google Maps
python3 scripts/scraping/google_maps_advanced.py \
  --url "https://www.google.com/maps/place/..."

# Com reviews detalhados (20 por lugar)
python3 scripts/scraping/google_maps_advanced.py \
  --search "hotéis" --location "Rio de Janeiro" \
  --reviews --max-reviews 20 --csv
```

**Criando polígono customizado:**

Use [Geojson.io](https://geojson.io) para desenhar a área e copiar as coordenadas:

1. Acesse https://geojson.io
2. Desenhe o polígono na área desejada
3. Copie as coordenadas do campo "coordinates"
4. ⚠️ **ATENÇÃO:** GeoJSON usa [longitude, latitude] (ordem invertida!)

### 3. Busca em Lote (`scripts/scraping/google_maps_batch.py`)

**Múltiplas buscas em paralelo:** economiza tempo e combina resultados

```bash
# Múltiplas buscas na mesma localização
python3 scripts/scraping/google_maps_batch.py \
  --searches "restaurantes,hotéis,cafeterias,academias" \
  --location "São Paulo, Brasil"

# Mesma busca em múltiplas localizações
python3 scripts/scraping/google_maps_batch.py \
  --search "academias" \
  --locations "São Paulo,Rio de Janeiro,Belo Horizonte,Curitiba"

# Combinação (produto cartesiano: 2 buscas x 2 locais = 4 scrapes)
python3 scripts/scraping/google_maps_batch.py \
  --searches "restaurantes,cafeterias" \
  --locations "São Paulo,Rio de Janeiro" \
  --max 30

# Com reviews e 5 workers paralelos
python3 scripts/scraping/google_maps_batch.py \
  --search "hotéis" \
  --locations "Lisboa,Porto,Faro" \
  --reviews --workers 5 --csv

# Salvar cada busca em arquivo separado
python3 scripts/scraping/google_maps_batch.py \
  --searches "pizzarias,hamburguerias" \
  --locations "SP,RJ" \
  --separate
```

## 🛠️ Uso Direto (Ferramenta Principal)

Para casos mais complexos, use `tools/apify_google_maps.py` diretamente:

```bash
# Busca simples
python3 tools/apify_google_maps.py --search "restaurantes" --location "São Paulo, Brasil"

# Com limite de resultados
python3 tools/apify_google_maps.py --search "hotéis" --location "Rio de Janeiro" --max-results 50

# Com reviews
python3 tools/apify_google_maps.py --search "cafeterias" --location "Lisboa, Portugal" --reviews --max-reviews 10

# URL direta
python3 tools/apify_google_maps.py --url "https://www.google.com/maps/place/..."

# Place ID
python3 tools/apify_google_maps.py --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" --reviews

# Export em CSV
python3 tools/apify_google_maps.py --search "academias" --location "Belo Horizonte" --format csv

# Múltiplas categorias
python3 tools/apify_google_maps.py \
  --search "restaurantes" \
  --location "São Paulo" \
  --categories "Chinese restaurant,Japanese restaurant,Pizza restaurant" \
  --max-results 100
```

## 🐍 Uso Programático (Python)

```python
from tools.apify_google_maps import GoogleMapsScraper

# Inicializa scraper
scraper = GoogleMapsScraper()

# 1. Busca simples
results = scraper.scrape_by_search(
    search_query="restaurantes",
    location="São Paulo, Brasil",
    max_results=50,
    include_reviews=True,
    max_reviews=10
)

# 2. Busca por URL
results = scraper.scrape_by_url(
    url="https://www.google.com/maps/place/...",
    include_reviews=True
)

# 3. Busca por Place ID
results = scraper.scrape_by_place_id(
    place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
    include_reviews=True,
    max_reviews=20
)

# 4. Busca com geolocalização customizada
geolocation = {
    "type": "Point",
    "coordinates": [-46.6333, -23.5505],  # lng, lat
    "radiusKm": 10
}

results = scraper.scrape_with_geolocation(
    search_query="academias",
    geolocation=geolocation,
    max_results=100
)

# 5. Salva resultados
if results["success"]:
    # JSON (padrão)
    scraper.save_results(results, format="json", filename="meus_resultados")

    # CSV
    scraper.save_results(results, format="csv", filename="meus_resultados")

    # Acessa dados diretamente
    places = results["places"]
    for place in places:
        print(f"{place['title']} - {place['address']}")
        print(f"Rating: {place.get('totalScore', 'N/A')}")
        print(f"Phone: {place.get('phone', 'N/A')}")
        print(f"Website: {place.get('website', 'N/A')}")
        print("---")
```

### Configurações Customizadas

```python
custom_config = {
    "maxReviews": 50,
    "maxImages": 10,
    "includeHistogram": True,  # Horários populares
    "includePeopleAlsoSearch": True,
    "scrapeReviewerName": True,
    "scrapeReviewerId": True,
    "scrapeResponseFromOwnerText": True,
}

results = scraper.scrape_by_search(
    search_query="hotéis",
    location="Rio de Janeiro",
    max_results=20,
    custom_config=custom_config
)
```

## 📊 Estrutura dos Dados de Saída

### JSON Output

```json
{
  "title": "Kim's Island",
  "categoryName": "Chinese restaurant",
  "address": "175 Main St, Staten Island, NY 10307",
  "city": "Staten Island",
  "state": "New York",
  "countryCode": "US",
  "phone": "(718) 356-5168",
  "phoneUnformatted": "+17183565168",
  "website": "http://kimsislandsi.com/",
  "location": {
    "lat": 40.5107736,
    "lng": -74.2482624
  },
  "totalScore": 4.5,
  "reviewsCount": 91,
  "reviewsDistribution": {
    "oneStar": 4,
    "twoStar": 3,
    "threeStar": 3,
    "fourStar": 10,
    "fiveStar": 71
  },
  "price": "$10–20",
  "openingHours": [
    {"day": "Monday", "hours": "Closed"},
    {"day": "Tuesday", "hours": "11 AM to 9:30 PM"}
  ],
  "placeId": "ChIJJQz5EZzKw4kRCZ95UajbyGw",
  "url": "https://www.google.com/maps/search/?api=1&query=Kim's%20Island&query_place_id=...",
  "imageUrl": "https://lh5.googleusercontent.com/p/AF1QipMyThXuZM...",
  "reviews": [
    {
      "name": "Rocco Castellano",
      "text": "Excellent food great service n always on time",
      "publishAt": "a month ago",
      "stars": 5,
      "reviewDetailedRating": {
        "Food": 5,
        "Service": 5,
        "Atmosphere": 5
      }
    }
  ]
}
```

### CSV Output

Tabela achatada com todos os campos (listas convertidas para JSON strings).

**Colunas principais:**
- `title`, `categoryName`, `address`, `city`, `state`, `postalCode`
- `phone`, `phoneUnformatted`, `website`
- `location_lat`, `location_lng`
- `totalScore`, `reviewsCount`
- `price`, `permanentlyClosed`, `temporarilyClosed`
- E muito mais...

## 📁 Onde os Arquivos São Salvos

**Todos os resultados são salvos em:** `~/Downloads/`

**Formato dos nomes:**
- JSON: `google_maps_scrape_YYYYMMDD_HHMMSS.json`
- CSV: `google_maps_scrape_YYYYMMDD_HHMMSS.csv`
- Custom: `seu_nome_customizado.json` / `.csv`

## ⚡ Performance e Custos

| Métrica | Valor |
|---------|-------|
| **Latência** | ~30-120s (depende do número de resultados) |
| **Custo Apify** | ~$0.01 - $0.10 por run (varia com quantidade de dados) |
| **Rate Limits** | Controlado pelo Apify (sem preocupação) |
| **Resultados/Run** | Ilimitado (configurável via `maxCrawledPlaces`) |

**Dicas de otimização:**
- ✅ Sem reviews: ~30-60s para 20 lugares
- ⚠️ Com reviews (10/lugar): ~90-120s para 20 lugares
- 🚀 Batch paralelo: 3+ buscas simultâneas (use `--workers`)

## 🔍 Casos de Uso Práticos

### 1. Geração de Leads B2B

```bash
# Extrair academias em SP para prospecção
python3 scripts/scraping/google_maps_basic.py \
  "academias" "São Paulo" --max 200 --csv

# Resultado: nome, telefone, website, endereço para cold call/email
```

### 2. Análise de Concorrência

```bash
# Monitorar restaurantes concorrentes
python3 scripts/scraping/google_maps_advanced.py \
  --search "restaurantes" \
  --location "Bairro Vila Madalena, São Paulo" \
  --reviews --max-reviews 50 --csv

# Análise: ratings, volume de reviews, reclamações comuns
```

### 3. Expansão de Mercado

```bash
# Identificar regiões com gaps de serviço
python3 scripts/scraping/google_maps_batch.py \
  --search "academias" \
  --locations "São Paulo,Campinas,Santos,Sorocaba" \
  --max 100 --separate

# Análise: densidade de academias por cidade
```

### 4. Enriquecimento de Base de Dados

```python
# Adicionar dados de Google Maps à base existente
scraper = GoogleMapsScraper()

for cliente in base_clientes:
    results = scraper.scrape_by_search(
        search_query=cliente['nome'],
        location=cliente['cidade'],
        max_results=1
    )

    if results["success"] and results["places"]:
        place = results["places"][0]
        cliente['google_rating'] = place.get('totalScore')
        cliente['google_reviews_count'] = place.get('reviewsCount')
        cliente['lat'] = place.get('location', {}).get('lat')
        cliente['lng'] = place.get('location', {}).get('lng')
```

## 🛡️ Limitações e Considerações

### ⚠️ Importante

1. **Termos de uso:** Web scraping do Google Maps é permitido para dados públicos, mas respeite os limites
2. **Personal data:** Reviews contém dados pessoais (nomes, fotos) - use responsavelmente (LGPD/GDPR)
3. **Rate limiting:** Apify controla automaticamente, mas evite abuso
4. **Dados desatualizados:** Scraping é snapshot - dados podem mudar
5. **Categorias:** Google tem milhares de categorias - use lista completa para evitar false negatives

### 🚫 NÃO Recomendado

- ❌ Scraping massivo sem propósito legítimo
- ❌ Revenda de dados extraídos
- ❌ Spam/contato não solicitado baseado em scraping
- ❌ Uso de dados pessoais sem consentimento

### ✅ Recomendado

- ✅ Pesquisa de mercado e análise competitiva
- ✅ Enriquecimento de base própria de clientes
- ✅ Geração de leads B2B qualificados
- ✅ Estudos acadêmicos e análises

## 📚 Recursos Adicionais

- **Apify Docs:** https://docs.apify.com/platform/actors/running/input-and-output
- **Google Maps Scraper Actor:** https://apify.com/compass/crawler-google-places
- **Geojson.io (criar polígonos):** https://geojson.io
- **Open Street Map (validar localizações):** https://www.openstreetmap.org

## 🐛 Troubleshooting

### Erro: "apify-client não instalado"

```bash
pip3 install apify-client
```

### Erro: "Location not found"

- Certifique-se de usar formato completo: `"Cidade, Estado, País"`
- Teste a localização no Open Street Map primeiro
- Use geolocalização customizada se necessário

### Nenhum resultado encontrado

- Tente busca mais genérica (ex: "restaurante" ao invés de "restaurante japonês vegano")
- Aumente `--max-results`
- Verifique se a localização está correta
- Teste a busca manualmente no Google Maps primeiro

### Timeout / Muito lento

- Reduza `--max-results`
- Desabilite reviews: não use `--reviews`
- Reduza `--max-reviews`
- Use batch com menos workers: `--workers 2`

## 📞 Suporte

- **Issues:** Abrir issue no repositório
- **Docs:** Este arquivo + `scripts/scraping/README.md`
- **Config:** `config/apify_config.py`
- **Templates:** `scripts/scraping/google_maps_*.py`

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
**Status:** ✅ Testado e funcional
