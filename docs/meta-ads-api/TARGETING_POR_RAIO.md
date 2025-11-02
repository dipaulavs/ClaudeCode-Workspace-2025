# Meta Ads - Targeting por Raio Geográfico

## ✅ Formato Correto para Targeting por Raio

Para criar campanhas com targeting por raio (quilômetros) ao redor de coordenadas específicas:

### Configuração de Targeting

```python
targeting = {
    "geo_locations": {
        "custom_locations": [
            {
                "latitude": -19.9167,      # Latitude da localização
                "longitude": -43.9345,     # Longitude da localização
                "radius": 2,               # Raio em quilômetros (qualquer valor)
                "distance_unit": "kilometer"  # ou "mile"
            }
        ]
    },
    "age_min": 30,
    "age_max": 60,
    "targeting_automation": {
        "advantage_audience": 0  # OBRIGATÓRIO! 0=desabilitado, 1=habilitado
    }
}
```

### Campos Obrigatórios

1. **`custom_locations`** - Array com objetos de localização
   - `latitude` - Coordenada de latitude (float)
   - `longitude` - Coordenada de longitude (float)
   - `radius` - Raio em km ou milhas (int)
   - `distance_unit` - Unidade: `"kilometer"` ou `"mile"`

2. **`targeting_automation`** - Objeto com configuração Advantage Audience
   - `advantage_audience` - **OBRIGATÓRIO**: `0` (desabilitado) ou `1` (habilitado)

### Exemplo Completo de Ad Set

```python
from meta_ads_adsets import MetaAdsAdSets

adsets_mgr = MetaAdsAdSets()

targeting = {
    "geo_locations": {
        "custom_locations": [
            {
                "latitude": -19.9167,
                "longitude": -43.9345,
                "radius": 5,  # 5km de raio
                "distance_unit": "kilometer"
            }
        ]
    },
    "age_min": 25,
    "age_max": 55,
    "targeting_automation": {
        "advantage_audience": 0
    }
}

adset_id = adsets_mgr.create_adset(
    campaign_id="123456789",
    name="Campanha BH - Raio 5km",
    daily_budget=None,  # Orçamento na campanha
    optimization_goal="LINK_CLICKS",
    billing_event="IMPRESSIONS",
    targeting=targeting,
    status="PAUSED"
)
```

## ⚠️ Restrições Importantes

### 1. Categorias Especiais (HOUSING, CREDIT, EMPLOYMENT)

**Anúncios com `special_ad_categories` NÃO PERMITEM targeting por raio personalizado.**

```python
# ❌ NÃO FUNCIONA com targeting por raio
campaign_id = campaigns_mgr.create_campaign(
    name="Campanha Imóveis",
    objective="OUTCOME_TRAFFIC",
    special_ad_categories=["HOUSING"]  # Bloqueia targeting por raio!
)
```

**Soluções:**

**Opção A:** Remover categoria especial (permite targeting por raio)
```python
# ✅ FUNCIONA com targeting por raio
special_ad_categories=[]  # Sem categoria especial
```

**Opção B:** Usar categoria especial (só permite país inteiro)
```python
# ✅ FUNCIONA mas só targeting por país
special_ad_categories=["HOUSING"]
targeting = {
    "geo_locations": {
        "countries": ["BR"]  # Apenas país
    }
}
```

### 2. Raio Mínimo

Para categorias especiais (HOUSING), quando permitido:
- **Raio mínimo:** 17km (10 milhas)

Para campanhas normais:
- **Raio mínimo:** Sem limite (pode usar 1km, 2km, etc.)

### 3. Coordenadas

Para encontrar coordenadas de cidades:
- Google Maps: Click direito → "O que há aqui?"
- Belo Horizonte, MG: `-19.9167, -43.9345`
- São Paulo, SP: `-23.5505, -46.6333`
- Rio de Janeiro, RJ: `-22.9068, -43.1729`

## 📝 Exemplos Práticos

### Exemplo 1: Raio de 2km no Centro de BH

```python
targeting = {
    "geo_locations": {
        "custom_locations": [
            {
                "latitude": -19.9167,
                "longitude": -43.9345,
                "radius": 2,
                "distance_unit": "kilometer"
            }
        ]
    },
    "age_min": 30,
    "age_max": 60,
    "targeting_automation": {
        "advantage_audience": 0
    }
}
```

### Exemplo 2: Raio de 10km em São Paulo

```python
targeting = {
    "geo_locations": {
        "custom_locations": [
            {
                "latitude": -23.5505,
                "longitude": -46.6333,
                "radius": 10,
                "distance_unit": "kilometer"
            }
        ]
    },
    "age_min": 25,
    "age_max": 50,
    "targeting_automation": {
        "advantage_audience": 0
    }
}
```

### Exemplo 3: Múltiplas Localizações

```python
targeting = {
    "geo_locations": {
        "custom_locations": [
            {
                "latitude": -19.9167,
                "longitude": -43.9345,
                "radius": 5,
                "distance_unit": "kilometer",
                "name": "Belo Horizonte Centro"
            },
            {
                "latitude": -19.8157,
                "longitude": -43.9542,
                "radius": 5,
                "distance_unit": "kilometer",
                "name": "Belo Horizonte Savassi"
            }
        ]
    },
    "age_min": 25,
    "age_max": 55,
    "targeting_automation": {
        "advantage_audience": 0
    }
}
```

## 🔧 Troubleshooting

### Erro: "advantage_audience é obrigatório"

**Solução:** Adicionar campo `targeting_automation`:
```python
"targeting_automation": {
    "advantage_audience": 0
}
```

### Erro: "localização fora dos países selecionados"

**Solução:** Remover `special_ad_categories` ou usar apenas países:
```python
# Opção 1: Sem categoria especial
special_ad_categories=[]

# Opção 2: Apenas países
targeting = {
    "geo_locations": {
        "countries": ["BR"]
    }
}
```

### Erro: "raio indisponível para categoria especial"

**Solução:** Aumentar raio para mínimo de 17km ou remover categoria especial:
```python
# Opção 1: Aumentar raio
"radius": 17  # Mínimo para HOUSING

# Opção 2: Remover categoria
special_ad_categories=[]
```

## 📚 Referências

- Meta Marketing API v24.0
- [Targeting Specs](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-specs)
- [Special Ad Categories](https://www.facebook.com/business/help/298000447747885)

---

**Última atualização:** 2025-10-31
