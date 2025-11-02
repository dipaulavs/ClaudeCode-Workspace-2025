# Meta Ads API - Documentação

Documentação completa da Meta Ads API para criação e gerenciamento de campanhas publicitárias programaticamente.

## 📚 Arquivos Disponíveis

### [META_ADS_API_DOCUMENTATION.md](./META_ADS_API_DOCUMENTATION.md)
**Documentação principal completa e atualizada**

Contém:
- ✅ Guia completo de autenticação e autorização
- ✅ Todos os endpoints (Campaigns, Ad Sets, Ads, Ad Creatives)
- ✅ Todos os parâmetros obrigatórios e opcionais
- ✅ Exemplos práticos em cURL
- ✅ Fluxo end-to-end de criação de campanhas
- ✅ Best practices e otimização
- ✅ Troubleshooting e erros comuns
- ✅ Rate limits e gestão de quotas

## 🎯 Quando Consultar Esta Documentação

**Use esta documentação quando precisar:**

1. **Criar campanhas via API**
   - Consulte a seção "Campaigns Endpoint"
   - Veja "Fluxo de Criação de Campanhas"

2. **Configurar Ad Sets**
   - Consulte a seção "Ad Sets Endpoint"
   - Veja parâmetros de targeting, budget e bidding

3. **Criar anúncios e criativos**
   - Consulte "Ads Endpoint" e "Ad Creatives Endpoint"
   - Veja exemplos de object_story_spec

4. **Resolver erros**
   - Consulte a seção "Erros Comuns"
   - Veja "Troubleshooting"

5. **Otimizar campanhas**
   - Consulte "Otimização e Monitoramento"
   - Veja "Best Practices"

6. **Entender autenticação**
   - Consulte a seção "Autenticação"
   - Veja tipos de access tokens

## 📊 Estrutura da API

```
Ad Account
└── Campaign
    ├── objective (CONVERSIONS, LINK_CLICKS, etc.)
    ├── budget (daily_budget ou lifetime_budget)
    └── Ad Set
        ├── targeting (geo, demographics, interests)
        ├── placement (Facebook, Instagram, etc.)
        ├── budget/bid
        └── Ad
            └── Ad Creative
                ├── images/videos
                ├── text (message, headline, description)
                └── call-to-action (SHOP_NOW, LEARN_MORE, etc.)
```

## 🔑 Quick Reference

### Endpoints Base
```
https://graph.facebook.com/v24.0
```

### Principais Endpoints

| Endpoint | Método | URL |
|----------|--------|-----|
| Criar Campaign | POST | `/act_<AD_ACCOUNT_ID>/campaigns` |
| Criar Ad Set | POST | `/act_<AD_ACCOUNT_ID>/adsets` |
| Criar Ad | POST | `/act_<AD_ACCOUNT_ID>/ads` |
| Criar Creative | POST | `/act_<AD_ACCOUNT_ID>/adcreatives` |
| Insights | GET | `/act_<AD_ACCOUNT_ID>/insights` |

### Parâmetros Obrigatórios

**Campaign:**
- `name`, `objective`, `special_ad_categories`

**Ad Set:**
- `name`, `campaign_id`, `daily_budget` OU `lifetime_budget`, `targeting`, `billing_event`, `optimization_goal`

**Ad:**
- `name`, `adset_id`, `creative`

**Ad Creative:**
- `name`, `object_story_spec`

## 📝 Exemplo Rápido

```bash
# 1. Criar Campaign
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/campaigns" \
  -F "name=Minha Campanha" \
  -F "objective=CONVERSIONS" \
  -F "status=PAUSED" \
  -F "special_ad_categories=[\"NONE\"]" \
  -F "access_token=<ACCESS_TOKEN>"

# 2. Criar Ad Set
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/adsets" \
  -F "name=Meu Ad Set" \
  -F "campaign_id=<CAMPAIGN_ID>" \
  -F "daily_budget=1000" \
  -F "targeting={\"geo_locations\":{\"countries\":[\"BR\"]}}" \
  -F "billing_event=IMPRESSIONS" \
  -F "optimization_goal=LINK_CLICKS" \
  -F "access_token=<ACCESS_TOKEN>"

# 3. Criar Creative
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/adcreatives" \
  -F "name=Meu Creative" \
  -F "object_story_spec={...}" \
  -F "access_token=<ACCESS_TOKEN>"

# 4. Criar Ad
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/ads" \
  -F "name=Meu Anúncio" \
  -F "adset_id=<AD_SET_ID>" \
  -F "creative={\"creative_id\":\"<CREATIVE_ID>\"}" \
  -F "status=PAUSED" \
  -F "access_token=<ACCESS_TOKEN>"
```

## 🔗 Links Úteis

- [Meta for Developers](https://developers.facebook.com/docs/marketing-api/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken)
- [Meta Ads Manager](https://adsmanager.facebook.com/)
- [Business Manager](https://business.facebook.com/)

## 📅 Informações da Documentação

- **Data de Coleta:** 31 de Outubro de 2025
- **Versão da API:** v24.0
- **Status:** Completa e atualizada
- **Fonte:** https://developers.facebook.com/docs/marketing-api/

---

💡 **Dica:** Sempre use `status=PAUSED` ao criar objetos para testes e `execution_options=validate_only` para validar parâmetros sem criar objetos reais.
