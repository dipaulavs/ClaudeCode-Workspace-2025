# Meta Ads Targeting Options Reference

Complete reference for location and interest targeting options in Meta Ads campaigns.

## Geographic Targeting (Locations)

### Brazil - States

```python
# Major states targeting
targeting = {
    'geo_locations': {
        'regions': [
            {'key': '3443'}, # São Paulo
            {'key': '3450'}, # Rio de Janeiro
            {'key': '3454'}, # Minas Gerais
            {'key': '3458'}, # Bahia
            {'key': '3449'}, # Rio Grande do Sul
            {'key': '3451'}, # Santa Catarina
            {'key': '3452'}, # Paraná
            {'key': '3442'}, # Goiás
            {'key': '3447'}, # Pernambuco
            {'key': '3441'}, # Ceará
        ]
    }
}
```

### Brazil - Major Cities

```python
# Top cities targeting
targeting = {
    'geo_locations': {
        'cities': [
            {'key': '2618425', 'radius': 25, 'distance_unit': 'kilometer'}, # São Paulo
            {'key': '2621009', 'radius': 25, 'distance_unit': 'kilometer'}, # Rio de Janeiro
            {'key': '2618684', 'radius': 20, 'distance_unit': 'kilometer'}, # Brasília
            {'key': '2619194', 'radius': 20, 'distance_unit': 'kilometer'}, # Belo Horizonte
            {'key': '2621217', 'radius': 20, 'distance_unit': 'kilometer'}, # Salvador
            {'key': '2621091', 'radius': 15, 'distance_unit': 'kilometer'}, # Fortaleza
            {'key': '2620961', 'radius': 15, 'distance_unit': 'kilometer'}, # Curitiba
            {'key': '2620870', 'radius': 15, 'distance_unit': 'kilometer'}, # Recife
            {'key': '2621285', 'radius': 15, 'distance_unit': 'kilometer'}, # Porto Alegre
        ]
    }
}
```

### National vs. Regional

```python
# Entire Brazil
targeting = {
    'geo_locations': {
        'countries': ['BR']
    }
}

# Multiple specific cities
targeting = {
    'geo_locations': {
        'cities': [
            {'key': '2618425', 'radius': 25, 'distance_unit': 'kilometer'}, # SP
            {'key': '2621009', 'radius': 25, 'distance_unit': 'kilometer'}, # RJ
        ]
    }
}
```

## Interest Targeting

### Real Estate (Imóveis)

```python
interests = [
    {'id': '6003020834693', 'name': 'Real estate'}, # Imóveis
    {'id': '6003139253285', 'name': 'Property investment'}, # Investimento imobiliário
    {'id': '6003013291990', 'name': 'Real estate investing'}, # Investimento em imóveis
    {'id': '6003034833250', 'name': 'Residential real estate'}, # Imóveis residenciais
    {'id': '6003138938086', 'name': 'Luxury real estate'}, # Imóveis de luxo
    {'id': '6003443922169', 'name': 'House'}, # Casa
    {'id': '6003443921969', 'name': 'Apartment'}, # Apartamento
]
```

### Investment (Investimentos)

```python
interests = [
    {'id': '6003011365850', 'name': 'Investing'}, # Investimentos
    {'id': '6003460538339', 'name': 'Financial literacy'}, # Educação financeira
    {'id': '6003147743851', 'name': 'Stock market'}, # Bolsa de valores
    {'id': '6003129862783', 'name': 'Entrepreneurship'}, # Empreendedorismo
    {'id': '6003150730693', 'name': 'Business'}, # Negócios
    {'id': '6003224901065', 'name': 'Passive income'}, # Renda passiva
]
```

### Luxury & High-End (Luxo & Alto-Padrão)

```python
interests = [
    {'id': '6003032146538', 'name': 'Luxury goods'}, # Produtos de luxo
    {'id': '6003139253286', 'name': 'Luxury vehicles'}, # Veículos de luxo
    {'id': '6003138938086', 'name': 'Luxury real estate'}, # Imóveis de luxo
    {'id': '6003231291983', 'name': 'High fashion'}, # Alta moda
    {'id': '6003149234289', 'name': 'Fine dining'}, # Gastronomia fina
    {'id': '6003020252819', 'name': 'Travel'}, # Viagens
]
```

### Rural & Farming (Chácara & Fazenda)

```python
interests = [
    {'id': '6003440682853', 'name': 'Agriculture'}, # Agricultura
    {'id': '6003068435986', 'name': 'Farming'}, # Fazenda
    {'id': '6003149822180', 'name': 'Livestock'}, # Pecuária
    {'id': '6003305458997', 'name': 'Gardening'}, # Jardinagem
    {'id': '6003018267957', 'name': 'Sustainability'}, # Sustentabilidade
    {'id': '6003304857949', 'name': 'Rural area'}, # Área rural
]
```

### Digital Products & Online Education (Infoprodutos)

```python
interests = [
    {'id': '6003115234698', 'name': 'Online courses'}, # Cursos online
    {'id': '6003129841684', 'name': 'E-learning'}, # E-learning
    {'id': '6003147743851', 'name': 'Online education'}, # Educação online
    {'id': '6003129862783', 'name': 'Entrepreneurship'}, # Empreendedorismo
    {'id': '6003150730693', 'name': 'Digital marketing'}, # Marketing digital
    {'id': '6003032055509', 'name': 'Personal development'}, # Desenvolvimento pessoal
]
```

## Age Targeting

```python
# Ages 18-65+ (default)
age_min = 18
age_max = 65

# Young adults (18-34)
age_min = 18
age_max = 34

# Adults (35-54)
age_min = 35
age_max = 54

# Mature adults (55+)
age_min = 55
age_max = None  # No upper limit
```

## Gender Targeting

```python
# All genders (default)
genders = [1, 2]  # 1=Male, 2=Female

# Male only
genders = [1]

# Female only
genders = [2]
```

## Complete Targeting Example

```python
# Real estate campaign targeting SP/RJ
targeting = {
    'geo_locations': {
        'cities': [
            {'key': '2618425', 'radius': 25, 'distance_unit': 'kilometer'}, # São Paulo
            {'key': '2621009', 'radius': 25, 'distance_unit': 'kilometer'}, # Rio de Janeiro
        ]
    },
    'age_min': 30,
    'age_max': 60,
    'genders': [1, 2],  # All genders
    'interests': [
        {'id': '6003020834693', 'name': 'Real estate'},
        {'id': '6003139253285', 'name': 'Property investment'},
        {'id': '6003011365850', 'name': 'Investing'},
    ]
}
```

## How to Find Interest IDs

### Method 1: Meta Ads Manager UI

1. Go to Ads Manager → Create Ad
2. Detailed Targeting → Search for interest
3. Inspect element to see interest ID in HTML

### Method 2: Marketing API

```bash
curl -G \
  -d "type=adinterest" \
  -d "q=real estate" \
  -d "limit=10" \
  -d "access_token=YOUR_TOKEN" \
  "https://graph.facebook.com/v18.0/search"
```

### Method 3: Python SDK

```python
from facebook_business.adobjects.targetingsearch import TargetingSearch

params = {
    'type': 'adinterest',
    'q': 'real estate',
    'limit': 10
}

interests = TargetingSearch.search(params=params)
for interest in interests:
    print(f"{interest['name']}: {interest['id']}")
```

## Best Practices

### Location Targeting

1. **Use radius** for cities (15-25km typical)
2. **Avoid overlap** between similar locations
3. **Test broad vs. narrow** geographic targeting
4. **Consider purchasing power** by region

### Interest Targeting

1. **Start narrow** (3-5 interests), then broaden
2. **Combine related interests** (real estate + investment)
3. **Avoid overly specific** combinations
4. **Test single interest** vs. multiple
5. **Monitor relevance score** to adjust interests

### Age Targeting

1. **Match product** to appropriate age range
2. **Luxury products:** 35-65+
3. **Digital products:** 18-45
4. **Investment products:** 30-60

### Gender Targeting

1. **Start with all genders** unless product-specific
2. **Test separately** to find better performing gender
3. **Adjust messaging** based on gender targeting

## Common Combinations for Product Types

### Lote (Land Lots)

```python
location: "SP Capital"
interests: "imóveis+investimento"
age: 35-60
```

### Chácara (Small Farms)

```python
location: "Interior SP"
interests: "agricultura+sustentabilidade+área rural"
age: 40-65
```

### Infoproduto (Digital Products)

```python
location: "BR Nacional"
interests: "empreendedorismo+marketing digital+cursos online"
age: 25-50
```

### Produto Lowticket (Low-ticket Products)

```python
location: "BR Nacional"
interests: [broad category interest]
age: 18-45
```

## Resources

- **Meta Targeting Options:** https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting
- **Interest Targeting:** https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-search
- **Location Targeting:** https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-location
- **Targeting Specs:** https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-specs
