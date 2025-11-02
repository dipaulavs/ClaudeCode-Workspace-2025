# Scripts de Scraping - Templates de Uso Rápido

## 📍 Google Maps Scraper

Sistema completo de extração de dados do Google Maps via Apify API.

### ✅ Templates Disponíveis

| Template | Uso | Quando Usar |
|----------|-----|-------------|
| `google_maps_basic.py` | Busca simples (termo + local) | Extração rápida e direta |
| `google_maps_advanced.py` | Busca avançada (categorias, geolocalização) | Casos complexos, filtros precisos |
| `google_maps_batch.py` | Múltiplas buscas em paralelo | Extrair dados de várias localizações/termos |

---

## 🚀 Quick Start

### 1. Busca Básica

**Use quando:** Busca simples por termo + localização

```bash
# Restaurantes em São Paulo (20 resultados)
python3 scripts/scraping/google_maps_basic.py "restaurantes" "São Paulo, Brasil"

# Hotéis no Rio (50 resultados)
python3 scripts/scraping/google_maps_basic.py "hotéis" "Rio de Janeiro" --max 50

# Cafeterias em Lisboa (CSV)
python3 scripts/scraping/google_maps_basic.py "cafeterias" "Lisboa, Portugal" --csv

# Academias com reviews
python3 scripts/scraping/google_maps_basic.py "academias" "Belo Horizonte" --reviews
```

**Argumentos:**
- `search` (obrigatório): Termo de busca
- `location` (obrigatório): Localização
- `--max N`: Máximo de resultados (padrão: 20)
- `--csv`: Exportar em CSV (padrão: JSON)
- `--reviews`: Incluir reviews (5 por lugar)
- `--output NOME`: Nome do arquivo de saída

---

### 2. Busca Avançada

**Use quando:** Filtros complexos, geolocalização customizada, múltiplas categorias

```bash
# Múltiplas categorias
python3 scripts/scraping/google_maps_advanced.py \
  --search "restaurantes" \
  --location "São Paulo" \
  --categories "Chinese restaurant,Japanese restaurant,Italian restaurant"

# Busca em círculo (raio de 5km ao redor de coordenadas)
python3 scripts/scraping/google_maps_advanced.py \
  --circle -46.6333 -23.5505 --radius 5 \
  --search "academias" --max 100

# Busca em polígono customizado (área específica)
python3 scripts/scraping/google_maps_advanced.py \
  --polygon "[[[-46.6,-23.5],[-46.7,-23.5],[-46.7,-23.6],[-46.6,-23.6],[-46.6,-23.5]]]" \
  --search "cafeterias"

# URL direta do Google Maps
python3 scripts/scraping/google_maps_advanced.py \
  --url "https://www.google.com/maps/place/..."

# Reviews detalhados (20 por lugar)
python3 scripts/scraping/google_maps_advanced.py \
  --search "hotéis" --location "Rio de Janeiro" \
  --reviews --max-reviews 20 --csv
```

**Argumentos principais:**
- **Busca:**
  - `--search TERMO`: Termo de busca
  - `--url URL`: URL direta do Google Maps

- **Geolocalização:**
  - `--location "Local"`: Localização textual
  - `--circle LNG LAT`: Círculo (coordenadas)
  - `--polygon "..."`: Polígono GeoJSON
  - `--radius N`: Raio do círculo em km (padrão: 10)

- **Filtros:**
  - `--categories "cat1,cat2"`: Categorias (separadas por vírgula)
  - `--max N`: Máximo de resultados
  - `--reviews`: Incluir reviews
  - `--max-reviews N`: Reviews por lugar (padrão: 5)

- **Export:**
  - `--csv`: Exportar em CSV
  - `--output NOME`: Nome do arquivo

**💡 Dica - Criar Polígono:**
1. Acesse https://geojson.io
2. Desenhe a área desejada
3. Copie as coordenadas do campo "coordinates"
4. ⚠️ **ATENÇÃO:** GeoJSON usa [longitude, latitude] (ordem invertida!)

---

### 3. Busca em Lote (Batch)

**Use quando:** Múltiplas buscas (2+) que podem rodar em paralelo

**🚨 REGRA IMPORTANTE:**
- Se precisar de **2 ou mais buscas** = SEMPRE use `batch`
- **NUNCA** execute múltiplos scripts individuais em sequência
- Batch executa TODAS em paralelo (economiza tempo!)

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

**Argumentos:**
- **Buscas:**
  - `--search TERMO`: Termo único
  - `--searches "t1,t2,t3"`: Múltiplos termos

- **Localizações:**
  - `--location "Local"`: Localização única
  - `--locations "l1,l2,l3"`: Múltiplas localizações

- **Configurações:**
  - `--max N`: Resultados por busca (padrão: 20)
  - `--reviews`: Incluir reviews
  - `--max-reviews N`: Reviews por lugar (padrão: 5)
  - `--workers N`: Buscas paralelas (padrão: 3)

- **Export:**
  - `--csv`: CSV (padrão: JSON)
  - `--output NOME`: Nome do arquivo (combinado)
  - `--separate`: Salvar cada busca em arquivo separado

**📊 Exemplo de execução:**
```
🗺️  GOOGLE MAPS SCRAPER - BUSCA EM LOTE
================================================================================

📊 Total de buscas: 4
👷 Workers paralelos: 3
📍 Localizações: São Paulo, Rio de Janeiro
🔍 Buscas: restaurantes, cafeterias

  🔄 Iniciando: restaurantes em São Paulo
  🔄 Iniciando: cafeterias em São Paulo
  🔄 Iniciando: restaurantes em Rio de Janeiro
  ✅ Concluído: restaurantes em São Paulo (20 lugares)
  🔄 Iniciando: cafeterias em Rio de Janeiro
  ✅ Concluído: cafeterias em São Paulo (18 lugares)
  ✅ Concluído: restaurantes em Rio de Janeiro (20 lugares)
  ✅ Concluído: cafeterias em Rio de Janeiro (15 lugares)

================================================================================
📊 RESUMO
================================================================================
✅ Buscas bem-sucedidas: 4
❌ Buscas com erro: 0

💾 Salvando resultados combinados...

✅ Resultados salvos com sucesso!
📁 Arquivo: ~/Downloads/gmaps_batch_20251102_143022.json
📊 Total de lugares: 73
```

---

## 📁 Onde os Arquivos São Salvos

**Todos os resultados em:** `~/Downloads/`

**Formatos de nome:**
- **JSON:** `google_maps_scrape_YYYYMMDD_HHMMSS.json`
- **CSV:** `google_maps_scrape_YYYYMMDD_HHMMSS.csv`
- **Batch:** `gmaps_batch_YYYYMMDD_HHMMSS.json` (combinado)
- **Batch separado:** `gmaps_TERMO_LOCAL_YYYYMMDD_HHMMSS.json` (um por busca)
- **Custom:** `seu_nome.json` / `.csv` (com `--output`)

---

## 📊 Dados Extraídos

### Campos Principais

✅ **Informações:**
- `title`: Nome do estabelecimento
- `categoryName`: Categoria principal
- `address`: Endereço completo
- `city`, `state`, `postalCode`, `countryCode`
- `location.lat`, `location.lng`: Coordenadas GPS

✅ **Contato:**
- `phone`: Telefone formatado
- `phoneUnformatted`: Telefone sem formatação
- `website`: Website oficial

✅ **Avaliações:**
- `totalScore`: Nota média (0-5)
- `reviewsCount`: Número de reviews
- `reviewsDistribution`: Distribuição 1-5 estrelas
- `reviews[]`: Array de reviews (se `--reviews`)

✅ **Extras:**
- `openingHours[]`: Horário de funcionamento
- `price`: Faixa de preço
- `permanentlyClosed`, `temporarilyClosed`: Status
- `images[]`: Fotos (se configurado)
- `placeId`: Google Place ID único

### Exemplo de Saída JSON

```json
{
  "title": "Pizzaria Bella Napoli",
  "categoryName": "Pizza restaurant",
  "address": "Rua Augusta 123, São Paulo, SP 01305-100",
  "city": "São Paulo",
  "state": "São Paulo",
  "countryCode": "BR",
  "phone": "(11) 3456-7890",
  "phoneUnformatted": "+551134567890",
  "website": "https://bellanapoli.com.br",
  "location": {
    "lat": -23.5505,
    "lng": -46.6333
  },
  "totalScore": 4.7,
  "reviewsCount": 523,
  "reviewsDistribution": {
    "oneStar": 5,
    "twoStar": 8,
    "threeStar": 42,
    "fourStar": 156,
    "fiveStar": 312
  },
  "price": "$$",
  "openingHours": [
    {"day": "Monday", "hours": "11 AM to 11 PM"},
    {"day": "Tuesday", "hours": "11 AM to 11 PM"}
  ],
  "placeId": "ChIJN1t_tDeuEmsRUsoyG83frY4"
}
```

---

## ⚡ Performance

| Métrica | Valor |
|---------|-------|
| **Latência** | ~30-120s (depende de resultados e reviews) |
| **Custo** | ~$0.01-$0.10 por run (varia com dados extraídos) |
| **Workers** | 3-5 paralelos (batch) |
| **Max resultados** | Ilimitado (configurável) |

**Dicas de otimização:**
- ✅ Sem reviews: ~30-60s para 20 lugares
- ⚠️ Com reviews (10/lugar): ~90-120s
- 🚀 Batch paralelo: 3+ buscas simultâneas

---

## 🎯 Casos de Uso Práticos

### 1. Geração de Leads B2B

```bash
# Extrair academias em SP para prospecção
python3 scripts/scraping/google_maps_basic.py \
  "academias" "São Paulo" --max 200 --csv

# Resultado: nome, telefone, website, endereço
```

### 2. Análise de Concorrência

```bash
# Monitorar restaurantes concorrentes com reviews
python3 scripts/scraping/google_maps_advanced.py \
  --search "restaurantes" \
  --location "Vila Madalena, São Paulo" \
  --reviews --max-reviews 50 --csv
```

### 3. Expansão de Mercado

```bash
# Identificar gaps de serviço em múltiplas cidades
python3 scripts/scraping/google_maps_batch.py \
  --search "academias" \
  --locations "São Paulo,Campinas,Santos,Sorocaba" \
  --max 100 --separate
```

### 4. Pesquisa de Mercado Regional

```bash
# Comparar categorias em diferentes regiões
python3 scripts/scraping/google_maps_batch.py \
  --searches "restaurantes,cafeterias,padarias" \
  --locations "Centro-SP,Pinheiros-SP,Vila Mariana-SP" \
  --csv
```

---

## 🤖 Regras para Claude Code

**SEMPRE que usuário pedir para extrair dados do Google Maps:**

1. ✅ **Identificar tipo de busca:**
   - **1 busca simples** → `google_maps_basic.py`
   - **1 busca com filtros/geo** → `google_maps_advanced.py`
   - **2+ buscas** → `google_maps_batch.py` (OBRIGATÓRIO)

2. ✅ **Usar template correto:**
   ```bash
   # ❌ ERRADO (2+ buscas)
   python3 scripts/scraping/google_maps_basic.py "restaurantes" "SP"
   python3 scripts/scraping/google_maps_basic.py "hotéis" "SP"

   # ✅ CORRETO (2+ buscas)
   python3 scripts/scraping/google_maps_batch.py \
     --searches "restaurantes,hotéis" --location "SP"
   ```

3. ✅ **Informar onde salvou:**
   - Sempre mostrar caminho completo do arquivo
   - Resumir primeiros resultados

**NUNCA:**
- ❌ Criar scripts temporários de scraping
- ❌ Executar múltiplos `basic.py` em sequência (usar `batch.py`)
- ❌ Usar ferramentas de `tools/` diretamente sem necessidade (templates são mais rápidos)

**Exemplos de identificação:**
- "Extrai restaurantes de SP e RJ" → `batch.py` ✅
- "Busca academias em BH" → `basic.py` ✅
- "Pega hotéis no centro com reviews" → `advanced.py` ✅

---

## 📚 Documentação Completa

- **Docs detalhada:** `docs/tools/apify_google_maps.md`
- **Ferramenta principal:** `tools/apify_google_maps.py`
- **Config:** `config/apify_config.py`
- **Templates:** `scripts/scraping/google_maps_*.py`

---

## 🐛 Troubleshooting

### Erro: "apify-client não instalado"

```bash
pip3 install apify-client
```

### Nenhum resultado encontrado

- Tente busca mais genérica
- Verifique localização (formato: "Cidade, Estado, País")
- Teste no Google Maps manualmente primeiro

### Timeout / Muito lento

- Reduza `--max`
- Desabilite `--reviews`
- Reduza `--max-reviews`
- Use menos `--workers` no batch

### Batch não combina resultados

- Use `--separate` para salvar arquivos individuais
- Verifique se buscas foram bem-sucedidas (veja resumo)

---

**Última atualização:** 2025-11-02
**Templates testados:** ✅ 3/3 funcionais
**Status:** Pronto para produção
