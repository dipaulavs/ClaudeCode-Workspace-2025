# 📢 Meta Ads - Campanha Regional com Raio

Cria campanha completa com targeting por raio geográfico (km).

## 🚀 Comando Completo

```bash
python3 tools/meta_ads_regional_campaign.py \
  IMAGEM \
  "CIDADE, ESTADO" \
  LATITUDE \
  LONGITUDE \
  RAIO_KM \
  "NOME_CAMPANHA" \
  "MENSAGEM_ANUNCIO" \
  "URL_DESTINO"
```

## 📝 Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `IMAGEM` | arquivo/URL | Caminho para imagem do anúncio |
| `"CIDADE, ESTADO"` | string | Nome da localização (ex: "Belo Horizonte, MG") |
| `LATITUDE` | float | Coordenada (ex: -19.9167) |
| `LONGITUDE` | float | Coordenada (ex: -43.9345) |
| `RAIO_KM` | int | Raio em quilômetros (ex: 2, 5, 10) |
| `"NOME_CAMPANHA"` | string | Nome da campanha |
| `"MENSAGEM_ANUNCIO"` | string | Texto do anúncio |
| `"URL_DESTINO"` | string | Link para onde o anúncio direciona |

## 💡 Exemplo

```bash
python3 tools/meta_ads_regional_campaign.py \
  ~/Downloads/anuncio.jpg \
  "Belo Horizonte, MG" \
  -19.9167 \
  -43.9345 \
  2 \
  "Promoção Imóveis BH" \
  "Apartamentos incríveis no bairro Savassi! Confira." \
  "https://exemplo.com/imoveis"
```

## ⚙️ Recursos

- Upload automático da imagem
- Cria: Campanha → Ad Set → Criativo → Anúncio
- Targeting: `custom_locations` com lat/long + raio
- Raio personalizável (2km, 5km, 10km, etc.)

## ⚠️ Importante

**NÃO funciona com `special_ad_categories`:**
- HOUSING (imóveis)
- CREDIT (crédito)
- EMPLOYMENT (emprego)

Para essas categorias, use targeting por cidade completa (sem raio).

## 📖 Docs

`docs/meta-ads-api/TARGETING_POR_RAIO.md`

## 🔧 Config

`config/meta_ads_config.py`
