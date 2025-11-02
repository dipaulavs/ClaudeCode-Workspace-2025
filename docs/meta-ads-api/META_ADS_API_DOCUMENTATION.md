# Meta Ads API - Documentação Completa para Criação de Campanhas

**Data de Coleta:** 31 de Outubro de 2025
**Versão da API:** v24.0
**Fonte:** https://developers.facebook.com/docs/marketing-api/

---

## Índice

1. [Introdução](#introdução)
2. [Requisitos](#requisitos)
3. [Autenticação](#autenticação)
4. [Autorização](#autorização)
5. [Estrutura de Campanhas](#estrutura-de-campanhas)
6. [API Endpoints](#api-endpoints)
   - [Campaigns](#1-campaigns-endpoint)
   - [Ad Sets](#2-ad-sets-endpoint)
   - [Ads](#3-ads-endpoint)
   - [Ad Creatives](#4-ad-creatives-endpoint)
7. [Fluxo de Criação](#fluxo-de-criação-de-campanhas)
8. [Gerenciamento de Campanhas](#gerenciamento-de-campanhas)
9. [Otimização e Monitoramento](#otimização-e-monitoramento)
10. [Best Practices](#best-practices)
11. [Rate Limits](#rate-limits)

---

## Introdução

A Marketing API do Meta permite criar, gerenciar e otimizar campanhas publicitárias programaticamente no Facebook, Instagram e outras propriedades da Meta.

### URL Base da API
```
https://graph.facebook.com/v24.0
```

---

## Requisitos

### 1. Ad Account (Conta de Anúncios)
- **Requisito obrigatório:** Uma [conta de anúncios ativa](https://www.facebook.com/business/help/910137316041095)
- Necessária para gerenciar campanhas, configurar billing e definir limites de gastos
- Encontre seu Ad Account ID no [Meta Ads Manager](https://adsmanager.facebook.com/)

**Como localizar seu Ad Account ID:**
1. Faça login no Facebook com sua conta business
2. Acesse o Ads Manager (menu superior direito)
3. Clique em Settings (configurações) no menu inferior esquerdo
4. Seu Ad Account ID estará listado junto com informações de billing

### 2. Criar um App
- Crie um app no [App Dashboard](https://developers.facebook.com/docs/development/create-an-app)
- Configure o tipo de app adequado para seu caso de uso
- Veja [Autorização](#autorização) para informações sobre permissões necessárias

---

## Autenticação

### Tipos de Access Tokens

#### 1. User Access Tokens

**Via Graph API Explorer:**
1. No campo **Meta App**, selecione seu app
2. Em **User or Page**, selecione **User Token**
3. Em **Add a Permission**, selecione as permissões necessárias (ex: `ads_read`, `ads_management`)
4. Clique em **Generate Access Token**
5. Armazene o token de forma segura

**Debugar o Token:**
- Use o [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken)
- Verifique: App ID, Data de Expiração, Scopes (permissões)

**Estender Token (Long-Lived):**
1. Cole seu token no Access Token Debugger
2. Clique em **Extend Access Token**
3. O novo token terá validade de 60 dias ou permanente

#### 2. System User Access Tokens

**Características:**
- Associado a uma conta de sistema no Business Manager
- **Não expira** (ideal para scripts long-running)
- Menos sujeito a invalidação comparado a user tokens
- Fornece separação entre atividade pessoal e business

**Documentação:** [System Users](https://developers.facebook.com/docs/marketing-api/system-users)

### Fluxo de Autenticação OAuth

Após o owner da ad account clicar em **Allow**:

```
http://YOUR_URL?code=<AUTHORIZATION_CODE>
```

Construa a URL para obter o access token:

```
https://graph.facebook.com/v24.0/oauth/access_token?
  client_id=<YOUR_APP_ID>
  &redirect_uri=<YOUR_URL>
  &client_secret=<YOUR_APP_SECRET>
  &code=<AUTHORIZATION_CODE>
```

**Resposta:**
- **Server-side flow:** Token persistente
- **Client-side flow:** Token com validade de 1-2 horas (pode ser estendido)

### Armazenamento Seguro de Tokens

**Best Practices:**
- ✅ Sempre transmitir tokens via HTTPS
- ✅ Armazenar em databases criptografadas
- ✅ Verificar validade regularmente
- ✅ Implementar re-autenticação quando inválido
- ✅ Solicitar apenas permissões mínimas necessárias
- ✅ Implementar expiração e refresh de tokens

**Tokens podem ser invalidados se:**
- Senha da conta for alterada
- Permissões forem revogadas
- Outros motivos de segurança

---

## Autorização

### App Roles
- **Admin:** Controle total do app
- **Developer:** Desenvolvimento e testes
- **Tester:** Apenas testes

### Access Levels

#### Marketing API Access vs Ads Management Standard Access

| Marketing API Access | Ads Management Standard Access | Ação |
|----------------------|--------------------------------|------|
| Development access | Standard access | Padrão |
| Standard access | Advanced access | Requer aprovação via App Review |

**Verificar nível atual:** App Dashboard → App Review → Permissions and Features

### Permissões Necessárias

#### Para gerenciar apenas suas próprias ad accounts:
- `ads_read` (Standard Access)
- `ads_management` (Standard Access)

#### Para gerenciar ad accounts de outras pessoas:
- `ads_read` (Advanced Access)
- `ads_management` (Advanced Access)

### Features (Recursos)

**Ads Management Standard Access** é a feature mais comum para gerenciar anúncios.

#### Standard Access
- ✅ Aprovação automática
- ✅ Acesso ilimitado a ad accounts
- ✅ Ideal para começar
- ⚠️ Rate limits mais restritivos (apenas para desenvolvimento)
- ⚠️ Algumas chamadas de API podem não estar disponíveis

#### Advanced Access

**Requisitos para Advanced Access:**
- Mínimo de 1500 chamadas de Marketing API nos últimos 15 dias
- Taxa de erro menor que 15% nos últimos 15 dias

**Benefícios:**
- ✅ Rate limits mais generosos (produção)
- ✅ Acesso total à Business Manager API e Catalog API
- ✅ Até 10 system users (vs 1 em standard)
- ✅ Gerenciar número ilimitado de ad accounts

### Solicitar Permissões do Usuário

Prompt para permissões via URL OAuth:

```
https://www.facebook.com/v24.0/dialog/oauth?
  client_id=<YOUR_APP_ID>
  &redirect_uri=<YOUR_URL>/
  &scope=ads_management
```

⚠️ **Importante:** Ao inserir `YOUR_URL`, adicione uma trailing `/` (ex: `http://www.facebook.com/`)

### Business Verification

Apps que acessam dados sensíveis devem passar por [Business Verification](https://developers.facebook.com/docs/apps/business-verification).

### Special Ad Categories

Campanhas com categorias especiais devem especificar:

```json
{
  "special_ad_categories": ["EMPLOYMENT", "HOUSING", "CREDIT", "ISSUES_ELECTIONS_POLITICS"],
  "special_ad_category_country": ["US", "BR", "GB"]
}
```

---

## Estrutura de Campanhas

A hierarquia de objetos da Marketing API:

```
Ad Account
└── Campaign (Campanha)
    ├── objective
    ├── budget
    └── Ad Set (Conjunto de Anúncios)
        ├── targeting
        ├── placement
        ├── budget/bid
        └── Ad (Anúncio)
            └── Ad Creative (Criativo)
                ├── images/videos
                ├── text
                └── call-to-action
```

### Relações
1. **Campaign** define o objetivo geral (ex: CONVERSIONS, LINK_CLICKS)
2. **Ad Set** define targeting, budget e scheduling
3. **Ad** contém o creative (visual + texto)
4. **Ad Creative** define a aparência do anúncio

---

## API Endpoints

### 1. Campaigns Endpoint

**Base URL:**
```
POST /act_<AD_ACCOUNT_ID>/campaigns
GET  /act_<AD_ACCOUNT_ID>/campaigns
POST /<CAMPAIGN_ID>
```

#### Parâmetros Obrigatórios (Create)

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `name` | string | Nome da campanha (max 400 chars, suporta emoji) |
| `objective` | enum | Objetivo da campanha |
| `special_ad_categories` | array | Categorias especiais (REQUIRED) |

#### Objectives (Objetivos)

**Objetivos Disponíveis:**
- `APP_INSTALLS` - Instalações de app
- `BRAND_AWARENESS` - Reconhecimento de marca
- `CONVERSIONS` - Conversões
- `EVENT_RESPONSES` - Respostas a eventos
- `LEAD_GENERATION` - Geração de leads
- `LINK_CLICKS` - Cliques em links
- `LOCAL_AWARENESS` - Reconhecimento local
- `MESSAGES` - Mensagens
- `OFFER_CLAIMS` - Reivindicações de oferta
- `OUTCOME_APP_PROMOTION` - Promoção de app (ODAX)
- `OUTCOME_AWARENESS` - Reconhecimento (ODAX)
- `OUTCOME_ENGAGEMENT` - Engajamento (ODAX)
- `OUTCOME_LEADS` - Leads (ODAX)
- `OUTCOME_SALES` - Vendas (ODAX)
- `OUTCOME_TRAFFIC` - Tráfego (ODAX)
- `PAGE_LIKES` - Curtidas na página
- `POST_ENGAGEMENT` - Engajamento em publicação
- `PRODUCT_CATALOG_SALES` - Vendas de catálogo
- `REACH` - Alcance
- `STORE_VISITS` - Visitas à loja
- `VIDEO_VIEWS` - Visualizações de vídeo

#### Parâmetros Opcionais (Campaign)

| Parâmetro | Tipo | Descrição | Default |
|-----------|------|-----------|---------|
| `status` | enum | ACTIVE, PAUSED, DELETED, ARCHIVED | - |
| `buying_type` | string | AUCTION ou RESERVED | AUCTION |
| `bid_strategy` | enum | LOWEST_COST_WITHOUT_CAP, LOWEST_COST_WITH_BID_CAP, COST_CAP, LOWEST_COST_WITH_MIN_ROAS | - |
| `daily_budget` | int64 | Orçamento diário (em centavos) | - |
| `lifetime_budget` | int64 | Orçamento total (em centavos) | - |
| `spend_cap` | int64 | Limite máximo de gasto | - |
| `start_time` | datetime | Data/hora de início | - |
| `stop_time` | datetime | Data/hora de término | - |
| `special_ad_category_country` | array | Países para categorias especiais | - |
| `promoted_object` | Object | Objeto sendo promovido | - |
| `source_campaign_id` | int | ID da campanha original (se copiada) | - |
| `is_skadnetwork_attribution` | boolean | iOS 14+ SKAdNetwork attribution | false |
| `execution_options` | array | validate_only, include_recommendations | - |

#### Promoted Object (promoted_object)

Objeto sendo promovido pela campanha. Campos variam conforme objetivo:

```json
{
  "application_id": 123456,
  "pixel_id": 789012,
  "custom_event_type": "PURCHASE",
  "page_id": "PAGE_ID",
  "product_catalog_id": 456789,
  "object_store_url": "https://apps.apple.com/app/id123456"
}
```

**Campos disponíveis:**
- `application_id` - ID do app Facebook
- `pixel_id` - ID do pixel de conversão
- `custom_event_type` - Tipo de evento customizado
- `object_store_url` - URL da app store
- `page_id` - ID da página Facebook
- `product_catalog_id` - ID do catálogo de produtos
- `event_id` - ID do evento Facebook
- `offer_id` - ID da oferta
- `instagram_profile_id` - ID do perfil Instagram
- `offline_conversion_data_set_id` - ID do dataset offline
- `conversion_goal_id` - ID do goal de conversão
- E muitos outros...

#### Budget Schedule Specs

Para criar períodos de alta demanda:

```json
{
  "budget_schedule_specs": [{
    "time_start": 1699081200,
    "time_end": 1699167600,
    "budget_value": 100,
    "budget_value_type": "ABSOLUTE",
    "recurrence_type": "ONE_TIME"
  }]
}
```

#### Exemplo: Criar Campaign

```bash
curl -X POST \
  https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/campaigns \
  -F 'name=Minha Campanha de Conversões' \
  -F 'objective=CONVERSIONS' \
  -F 'status=PAUSED' \
  -F 'special_ad_categories=["NONE"]' \
  -F 'daily_budget=5000' \
  -F 'access_token=<ACCESS_TOKEN>'
```

---

### 2. Ad Sets Endpoint

**Base URL:**
```
POST /act_<AD_ACCOUNT_ID>/adsets
GET  /act_<AD_ACCOUNT_ID>/adsets
POST /<AD_SET_ID>
```

#### Parâmetros Obrigatórios (Create)

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `name` | string | Nome do ad set (max 400 chars) |
| `campaign_id` | int64 | ID da campanha pai |
| `daily_budget` OU `lifetime_budget` | int64 | Orçamento (um dos dois obrigatório) |
| `targeting` | Object | Especificação de targeting |
| `billing_event` | enum | Evento de cobrança |
| `optimization_goal` | enum | Meta de otimização |

#### Budget (Orçamento)

**Escolher um dos dois:**
- `daily_budget` - Orçamento diário (para campanhas > 24h)
- `lifetime_budget` - Orçamento total (requer `end_time`)

**Controles adicionais:**
- `daily_min_spend_target` - Meta mínima de gasto diário
- `daily_spend_cap` - Limite máximo de gasto diário
- `lifetime_min_spend_target` - Meta mínima de gasto total
- `lifetime_spend_cap` - Limite máximo de gasto total

#### Bid Strategy

| Estratégia | Descrição |
|------------|-----------|
| `LOWEST_COST_WITHOUT_CAP` | Maximiza resultados sem limite de bid (automático) |
| `LOWEST_COST_WITH_BID_CAP` | Maximiza resultados com limite de bid (manual) |
| `COST_CAP` | Mantém custo por resultado próximo ao valor especificado |
| `LOWEST_COST_WITH_MIN_ROAS` | Otimiza para ROAS mínimo |

**Nota:** Se Campaign Budget Optimization (CBO) estiver ativo, configure `bid_strategy` no nível da campanha.

#### Billing Event

Evento pelo qual você será cobrado:

- `APP_INSTALLS` - Instalações do app
- `CLICKS` - Cliques (deprecated)
- `IMPRESSIONS` - Impressões
- `LINK_CLICKS` - Cliques em links
- `OFFER_CLAIMS` - Reivindicações de oferta
- `PAGE_LIKES` - Curtidas na página
- `POST_ENGAGEMENT` - Engajamento
- `THRUPLAY` - Vídeo até conclusão ou 15s
- `PURCHASE` - Compras
- `LISTING_INTERACTION` - Interação com listagem

#### Optimization Goal

O que otimizar no ad set:

- `NONE`
- `APP_INSTALLS` - Instalações de app
- `AD_RECALL_LIFT` - Recall do anúncio
- `ENGAGED_USERS` - Usuários engajados
- `EVENT_RESPONSES` - Respostas a eventos
- `IMPRESSIONS` - Impressões
- `LEAD_GENERATION` - Geração de leads
- `QUALITY_LEAD` - Leads de qualidade
- `LINK_CLICKS` - Cliques em links
- `OFFSITE_CONVERSIONS` - Conversões offsite
- `PAGE_LIKES` - Curtidas na página
- `POST_ENGAGEMENT` - Engajamento
- `REACH` - Alcance
- `LANDING_PAGE_VIEWS` - Visualizações de landing page
- `VALUE` - Valor total de compra
- `THRUPLAY` - Reproduções de vídeo
- `VISIT_INSTAGRAM_PROFILE` - Visitas ao perfil Instagram
- `CONVERSATIONS` - Conversas
- E muitos outros...

#### Targeting

Objeto de targeting define a audiência:

```json
{
  "geo_locations": {
    "countries": ["US", "BR"],
    "cities": [{"key": "2466256"}],
    "regions": [{"key": "3847"}]
  },
  "age_min": 18,
  "age_max": 65,
  "genders": [1, 2],
  "interests": [{"id": 6003139266461, "name": "Movies"}],
  "behaviors": [{"id": 6002714895372, "name": "Mobile device user"}],
  "custom_audiences": [{"id": "123456789"}],
  "excluded_custom_audiences": [{"id": "987654321"}],
  "locales": [6],
  "publisher_platforms": ["facebook", "instagram"],
  "facebook_positions": ["feed", "right_hand_column"],
  "instagram_positions": ["stream", "story"]
}
```

#### Destination Type

Onde o usuário será direcionado ao clicar:

- `WEBSITE`
- `APP`
- `MESSENGER`
- `WHATSAPP`
- `INSTAGRAM_DIRECT`
- `FACEBOOK`
- `INSTAGRAM_PROFILE`
- `FACEBOOK_PAGE`
- `ON_AD`
- `ON_POST`
- `ON_VIDEO`
- `SHOP_AUTOMATIC`
- E outros...

#### Ad Set Schedule

Agendar delivery do ad set por hora do dia:

```json
{
  "adset_schedule": [{
    "start_minute": 480,
    "end_minute": 1020,
    "days": [0, 1, 2, 3, 4],
    "timezone_type": "USER"
  }]
}
```

**start_minute/end_minute:** Minutos do dia (0-1439)
**days:** 0=Domingo, 1=Segunda, ..., 6=Sábado

#### Attribution Spec

Janela de atribuição para conversões:

```json
{
  "attribution_spec": [{
    "event_type": "CLICK_THROUGH",
    "window_days": 7
  },
  {
    "event_type": "VIEW_THROUGH",
    "window_days": 1
  }]
}
```

#### Frequency Control

Controle de frequência (apenas para REACH e THRUPLAY):

```json
{
  "frequency_control_specs": [{
    "event": "IMPRESSIONS",
    "interval_days": 7,
    "max_frequency": 2
  }]
}
```

#### Promoted Object (Ad Set Level)

Similar ao campaign level, mas específico para o ad set.

#### Exemplo: Criar Ad Set

```bash
curl -X POST \
  https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/adsets \
  -F 'name=Meu Ad Set Brasil' \
  -F 'campaign_id=<CAMPAIGN_ID>' \
  -F 'daily_budget=1000' \
  -F 'billing_event=IMPRESSIONS' \
  -F 'optimization_goal=LINK_CLICKS' \
  -F 'bid_amount=100' \
  -F 'targeting={"geo_locations":{"countries":["BR"]},"age_min":18,"age_max":65}' \
  -F 'status=PAUSED' \
  -F 'access_token=<ACCESS_TOKEN>'
```

---

### 3. Ads Endpoint

**Base URL:**
```
POST /act_<AD_ACCOUNT_ID>/ads
GET  /act_<AD_ACCOUNT_ID>/ads
POST /<AD_ID>
```

#### Parâmetros Obrigatórios (Create)

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `name` | string | Nome do anúncio |
| `adset_id` | int64 | ID do ad set pai |
| `creative` | Object | ID ou spec do creative |

#### Status

- `ACTIVE` - Anúncio ativo (após review)
- `PAUSED` - Anúncio pausado
- `DELETED` - Anúncio deletado
- `ARCHIVED` - Anúncio arquivado

**Durante criação, use apenas ACTIVE ou PAUSED.**

**Ad Review:** Anúncios criados passam por revisão e ficam com status `PENDING_REVIEW` até aprovação.

⚠️ **Recomendação para testes:** Crie ads com status `PAUSED` para evitar gastos acidentais.

#### Creative

**Opção 1 - Usar Creative ID existente:**
```json
{
  "creative": {
    "creative_id": "<CREATIVE_ID>"
  }
}
```

**Opção 2 - Criar creative inline:**
```json
{
  "creative": {
    "name": "Meu Creative",
    "object_story_spec": {
      "page_id": "PAGE_ID",
      "link_data": {
        "message": "Confira nossa oferta!",
        "link": "https://www.example.com",
        "picture": "https://www.example.com/image.jpg",
        "call_to_action": {
          "type": "SHOP_NOW"
        }
      }
    }
  }
}
```

#### Parâmetros Opcionais

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `ad_schedule_start_time` | datetime | Hora de início (apenas sales/app promotion) |
| `ad_schedule_end_time` | datetime | Hora de término (apenas sales/app promotion) |
| `conversion_domain` | string | Domínio de conversão (ex: facebook.com) |
| `display_sequence` | int64 | Sequência dentro da campanha |
| `engagement_audience` | boolean | Criar audiência de engajamento |
| `source_ad_id` | int | ID do ad original (se copiado) |
| `tracking_specs` | Object | Especificações de tracking |
| `execution_options` | array | validate_only, synchronous_ad_review |

#### Exemplo: Criar Ad

```bash
curl -X POST \
  https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/ads \
  -F 'name=Meu Anúncio' \
  -F 'adset_id=<AD_SET_ID>' \
  -F 'creative={"creative_id": "<CREATIVE_ID>"}' \
  -F 'status=PAUSED' \
  -F 'access_token=<ACCESS_TOKEN>'
```

---

### 4. Ad Creatives Endpoint

**Base URL:**
```
POST /act_<AD_ACCOUNT_ID>/adcreatives
GET  /act_<AD_ACCOUNT_ID>/adcreatives
```

#### Parâmetros Principais

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `name` | string | Nome do creative |
| `object_story_spec` | Object | Especificação da história |
| `asset_feed_spec` | Object | Assets para Dynamic Creative |
| `degrees_of_freedom_spec` | Object | Especificação de liberdade |
| `actor_id` | int64 | Page ID do creative |
| `applink_treatment` | enum | Tratamento de app link |

#### Object Story Spec

Define como o anúncio aparece:

**Link Ad:**
```json
{
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "link_data": {
      "message": "Confira nosso novo produto!",
      "link": "https://www.example.com/product",
      "caption": "example.com",
      "picture": "https://www.example.com/image.jpg",
      "name": "Novo Produto Incrível",
      "description": "Descrição do produto aqui",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": {
          "link": "https://www.example.com/product"
        }
      }
    }
  }
}
```

**Video Ad:**
```json
{
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "video_data": {
      "message": "Assista nosso novo vídeo!",
      "video_id": "VIDEO_ID",
      "image_url": "https://www.example.com/thumbnail.jpg",
      "call_to_action": {
        "type": "LEARN_MORE",
        "value": {
          "link": "https://www.example.com"
        }
      }
    }
  }
}
```

**Image Ad:**
```json
{
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "photo_data": {
      "image_hash": "IMAGE_HASH",
      "caption": "Nossa nova coleção!",
      "page_welcome_message": "Olá! Como posso ajudar?",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": {
          "link": "https://www.example.com"
        }
      }
    }
  }
}
```

#### Call to Action Types

Botões disponíveis:

- `OPEN_LINK`, `LIKE_PAGE`, `SHOP_NOW`, `PLAY_GAME`
- `INSTALL_APP`, `USE_APP`, `CALL`, `CALL_ME`
- `VIDEO_CALL`, `INSTALL_MOBILE_APP`, `USE_MOBILE_APP`
- `MOBILE_DOWNLOAD`, `BOOK_TRAVEL`, `LISTEN_MUSIC`
- `WATCH_VIDEO`, `LEARN_MORE`, `SIGN_UP`, `DOWNLOAD`
- `WATCH_MORE`, `NO_BUTTON`, `CALL_NOW`, `APPLY_NOW`
- `CONTACT`, `BUY_NOW`, `GET_OFFER`, `GET_OFFER_VIEW`
- `BUY_TICKETS`, `UPDATE_APP`, `GET_DIRECTIONS`, `BUY`
- `MESSAGE_PAGE`, `DONATE`, `SUBSCRIBE`, `SAY_THANKS`
- `SELL_NOW`, `SHARE`, `DONATE_NOW`, `GET_QUOTE`
- `CONTACT_US`, `ORDER_NOW`, `ADD_TO_CART`, `VIEW_CART`
- `SEND_WHATSAPP_MESSAGE`, `BOOK_NOW`, `PAY_TO_ACCESS`
- E muitos outros...

#### Asset Feed Spec (Dynamic Creative)

Para criar variações automáticas do anúncio:

```json
{
  "asset_feed_spec": {
    "images": [
      {"hash": "IMAGE_HASH_1"},
      {"hash": "IMAGE_HASH_2"}
    ],
    "videos": [
      {"video_id": "VIDEO_ID_1"},
      {"video_id": "VIDEO_ID_2"}
    ],
    "bodies": [
      {"text": "Texto do corpo 1"},
      {"text": "Texto do corpo 2"}
    ],
    "titles": [
      {"text": "Título 1"},
      {"text": "Título 2"}
    ],
    "descriptions": [
      {"text": "Descrição 1"},
      {"text": "Descrição 2"}
    ],
    "link_urls": [
      {"website_url": "https://example.com/page1"},
      {"website_url": "https://example.com/page2"}
    ],
    "call_to_action_types": ["SHOP_NOW", "LEARN_MORE"]
  }
}
```

#### Applink Treatment

Para Dynamic Ads, define comportamento quando app não está instalado:

- `automatic` - Decisão automática
- `deeplink_with_web_fallback` - Deep link com fallback web
- `deeplink_with_appstore_fallback` - Deep link com fallback app store
- `web_only` - Apenas web

#### Exemplo: Criar Ad Creative

```bash
curl -X POST \
  https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/adcreatives \
  -F 'name=Meu Creative Link Ad' \
  -F 'object_story_spec={
    "page_id": "YOUR_PAGE_ID",
    "link_data": {
      "message": "Confira nossa nova oferta!",
      "link": "https://www.example.com/offer",
      "caption": "example.com",
      "picture": "https://www.example.com/image.jpg",
      "name": "Oferta Especial",
      "description": "50% de desconto por tempo limitado",
      "call_to_action": {
        "type": "SHOP_NOW"
      }
    }
  }' \
  -F 'access_token=<ACCESS_TOKEN>'
```

---

## Fluxo de Criação de Campanhas

### Ordem Correta de Criação

```
1. Campaign
   ↓
2. Ad Set
   ↓
3. Ad Creative
   ↓
4. Ad
```

### Exemplo Completo: Criar Campanha End-to-End

#### Passo 1: Criar Campaign

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_123456789/campaigns" \
  -F "name=Campanha Black Friday 2025" \
  -F "objective=CONVERSIONS" \
  -F "status=PAUSED" \
  -F "special_ad_categories=[\"NONE\"]" \
  -F "daily_budget=10000" \
  -F "access_token=YOUR_ACCESS_TOKEN"
```

**Resposta:**
```json
{
  "id": "120210000000001"
}
```

#### Passo 2: Criar Ad Set

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_123456789/adsets" \
  -F "name=Ad Set Brasil 18-45" \
  -F "campaign_id=120210000000001" \
  -F "daily_budget=5000" \
  -F "billing_event=IMPRESSIONS" \
  -F "optimization_goal=OFFSITE_CONVERSIONS" \
  -F "bid_amount=200" \
  -F "targeting={\"geo_locations\":{\"countries\":[\"BR\"]},\"age_min\":18,\"age_max\":45}" \
  -F "status=PAUSED" \
  -F "access_token=YOUR_ACCESS_TOKEN"
```

**Resposta:**
```json
{
  "id": "120210000000002"
}
```

#### Passo 3: Criar Ad Creative

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_123456789/adcreatives" \
  -F "name=Creative Black Friday" \
  -F "object_story_spec={\"page_id\":\"YOUR_PAGE_ID\",\"link_data\":{\"message\":\"Black Friday! 50% OFF em tudo\",\"link\":\"https://exemplo.com/blackfriday\",\"picture\":\"https://exemplo.com/banner.jpg\",\"call_to_action\":{\"type\":\"SHOP_NOW\"}}}" \
  -F "access_token=YOUR_ACCESS_TOKEN"
```

**Resposta:**
```json
{
  "id": "120210000000003"
}
```

#### Passo 4: Criar Ad

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_123456789/ads" \
  -F "name=Anúncio Black Friday Principal" \
  -F "adset_id=120210000000002" \
  -F "creative={\"creative_id\":\"120210000000003\"}" \
  -F "status=PAUSED" \
  -F "access_token=YOUR_ACCESS_TOKEN"
```

**Resposta:**
```json
{
  "id": "120210000000004"
}
```

### Ativar Campanha

Após revisar tudo, ative a campanha:

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/120210000000001" \
  -F "status=ACTIVE" \
  -F "access_token=YOUR_ACCESS_TOKEN"
```

---

## Gerenciamento de Campanhas

### Atualizar Campaign

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/<CAMPAIGN_ID>" \
  -F "objective=CONVERSIONS" \
  -F "daily_budget=2000" \
  -F "status=ACTIVE" \
  -F "access_token=<ACCESS_TOKEN>"
```

### Pausar Campaign

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/<CAMPAIGN_ID>" \
  -F "status=PAUSED" \
  -F "access_token=<ACCESS_TOKEN>"
```

### Arquivar Campaign

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/<CAMPAIGN_ID>" \
  -F "status=ARCHIVED" \
  -F "access_token=<ACCESS_TOKEN>"
```

⚠️ **Nota:** Campanhas arquivadas podem ser reativadas mudando status para `ACTIVE`.

### Deletar Campaign

```bash
curl -X DELETE \
  "https://graph.facebook.com/v24.0/<CAMPAIGN_ID>" \
  -F "access_token=<ACCESS_TOKEN>"
```

⚠️ **ATENÇÃO:** Deletion é **permanente e irreversível**. Sempre verifique o Campaign ID antes de deletar.

---

## Otimização e Monitoramento

### Insights API

Para obter métricas de performance:

```bash
curl -X GET \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/insights" \
  -d "fields=impressions,clicks,spend,cpc,cpm,ctr,reach" \
  -d "time_range={'since':'2025-01-01','until':'2025-01-31'}" \
  -d "level=campaign" \
  -d "access_token=<ACCESS_TOKEN>"
```

### Campos de Insights Disponíveis

**Métricas Básicas:**
- `impressions` - Número de impressões
- `reach` - Alcance único
- `clicks` - Cliques totais
- `spend` - Gasto total

**Métricas de Custo:**
- `cpc` - Custo por clique
- `cpm` - Custo por mil impressões
- `cpp` - Custo por pessoa alcançada
- `ctr` - Taxa de cliques

**Métricas de Conversão:**
- `actions` - Ações tomadas
- `conversions` - Conversões
- `conversion_values` - Valor das conversões
- `cost_per_action_type` - Custo por tipo de ação

**Métricas de Vídeo:**
- `video_play_actions` - Reproduções de vídeo
- `video_avg_time_watched_actions` - Tempo médio assistido
- `video_p25_watched_actions` - 25% assistido
- `video_p50_watched_actions` - 50% assistido
- `video_p75_watched_actions` - 75% assistido
- `video_p100_watched_actions` - 100% assistido

### Níveis de Breakdown

- `level=account` - Nível de conta
- `level=campaign` - Nível de campanha
- `level=adset` - Nível de ad set
- `level=ad` - Nível de anúncio

### Custom Audiences

Criar audiências customizadas para retargeting:

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/customaudiences" \
  -F "name=Minha Audiência Custom" \
  -F "subtype=CUSTOM" \
  -F "description=Visitantes do site" \
  -F "access_token=<ACCESS_TOKEN>"
```

### Lookalike Audiences

Criar audiências similares:

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/customaudiences" \
  -F "name=Lookalike Brasil 1%" \
  -F "subtype=LOOKALIKE" \
  -F "origin_audience_id=<CUSTOM_AUDIENCE_ID>" \
  -F "lookalike_spec={'country':'BR','ratio':0.01}" \
  -F "access_token=<ACCESS_TOKEN>"
```

---

## Best Practices

### 1. Audience Targeting

✅ **Use Custom Audiences** baseadas em interações com seu negócio (visitantes do site, usuários do app)

✅ **Segmente sua audiência** usando filtros demográficos (idade, gênero, localização, interesses)

✅ **Crie Lookalike Audiences** para alcançar novos clientes similares aos seus melhores clientes

### 2. Budget Allocation

✅ **Defina objetivos claros** para cada campanha (brand awareness, lead generation, etc.)

✅ **Monitore performance regularmente** e ajuste budgets para os ads/ad sets com melhor performance

✅ **Use daily budgets** para controlar gastos e permitir ajustes baseados em tendências

### 3. Ad Creatives

✅ **Invista em visuais de alta qualidade** - Imagens e vídeos atraentes aumentam CTR

✅ **Faça A/B Testing** continuamente - Teste diferentes creatives, headlines e CTAs

✅ **Use Dynamic Creatives** para personalização automática baseada no comportamento do usuário

### 4. Real-Time Optimization

✅ **Use Insights API** para coletar dados em tempo real sobre performance

✅ **Ajuste targeting dinamicamente** se certas demographics performam melhor

✅ **Configure dashboards de relatório** regulares para identificar tendências e oportunidades

### 5. Conversions API

✅ **Implemente Conversions API** para criar conexão entre seus dados de marketing e sistemas da Meta

✅ **Melhora targeting de ads**, diminui custo por resultado e mede outcomes com mais precisão

### 6. Segurança

✅ **Armazene access tokens de forma segura** em databases criptografadas

✅ **Use HTTPS** para todas as comunicações com a API

✅ **Valide tokens regularmente** e implemente re-autenticação quando necessário

✅ **Implemente rate limiting** para evitar exceder limites da API

### 7. Testing

✅ **Sempre crie ads com status=PAUSED** durante testes para evitar gastos acidentais

✅ **Use execution_options=validate_only** para validar parâmetros sem criar objetos

✅ **Teste em Development Access** antes de solicitar Advanced Access

---

## Rate Limits

### Standard Access vs Advanced Access

| Tipo | Standard Access | Advanced Access |
|------|-----------------|-----------------|
| **Uso** | Desenvolvimento e testes | Produção |
| **Ad Accounts** | Ilimitado | Ilimitado |
| **Rate Limits** | Muito restritivos (não para produção) | Generosos (produção) |
| **System Users** | 1 regular + 1 admin | 10 regulares + 1 admin |
| **Business Manager API** | Acesso limitado | Acesso completo |
| **Catalog API** | Acesso limitado | Acesso completo |

### Requisitos para Manter Advanced Access

Para manter Advanced Access, seu app deve:

✅ Fazer pelo menos **1500 chamadas de Marketing API** nos últimos 15 dias

✅ Ter **taxa de erro menor que 15%** nos últimos 15 dias

### Headers de Rate Limit

Verifique headers na resposta da API:

```
x-business-use-case-usage: {"ad_account_id":{"call_count":50,"total_cputime":100,"total_time":200}}
x-app-usage: {"call_count":25,"total_cputime":50,"total_time":100}
```

### Handling Rate Limits

Se você exceder rate limits:

1. A API retornará erro `80004` (Application request limit reached)
2. Aguarde alguns minutos antes de tentar novamente
3. Implemente exponential backoff em seu código
4. Distribua chamadas ao longo do tempo (não faça bursts)

---

## Execution Options

Use `execution_options` para validação sem criar objetos:

### validate_only

Valida parâmetros sem criar o objeto:

```bash
curl -X POST \
  "https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/campaigns" \
  -F "name=Test Campaign" \
  -F "objective=CONVERSIONS" \
  -F "execution_options=['validate_only']" \
  -F "access_token=<ACCESS_TOKEN>"
```

**Resposta se válido:**
```json
{
  "success": true
}
```

**Resposta se inválido:**
```json
{
  "error": {
    "message": "Invalid parameter",
    "code": 100
  }
}
```

### include_recommendations

Inclui recomendações de configuração:

```bash
-F "execution_options=['include_recommendations']"
```

### synchronous_ad_review

Para Ads, valida regras de integridade (texto em imagem, linguagem, etc.):

```bash
-F "execution_options=['validate_only','synchronous_ad_review']"
```

---

## Erros Comuns

### 1. Invalid OAuth 2.0 Access Token

**Erro:**
```json
{
  "error": {
    "message": "Invalid OAuth 2.0 Access Token",
    "code": 190
  }
}
```

**Solução:**
- Verifique se o token está correto
- Verifique se o token não expirou
- Gere um novo token se necessário

### 2. Insufficient Permission

**Erro:**
```json
{
  "error": {
    "message": "Insufficient permission",
    "code": 200
  }
}
```

**Solução:**
- Verifique se tem permissões `ads_management` ou `ads_read`
- Verifique se tem acesso ao ad account
- Solicite Advanced Access se necessário

### 3. Application Request Limit Reached

**Erro:**
```json
{
  "error": {
    "message": "Application request limit reached",
    "code": 80004
  }
}
```

**Solução:**
- Aguarde alguns minutos antes de tentar novamente
- Implemente rate limiting em seu código
- Considere solicitar Advanced Access para rate limits mais generosos

### 4. Invalid Parameter

**Erro:**
```json
{
  "error": {
    "message": "Invalid parameter",
    "code": 100
  }
}
```

**Solução:**
- Verifique a documentação do parâmetro
- Use `execution_options=validate_only` para identificar o problema
- Verifique tipos de dados (string vs int, etc.)

---

## Recursos Adicionais

### Documentação Oficial
- [Marketing API Overview](https://developers.facebook.com/docs/marketing-api/)
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/reference/)
- [Business Manager API](https://developers.facebook.com/docs/business-manager-api)

### Ferramentas
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken)
- [Ads Manager](https://adsmanager.facebook.com/)
- [Business Manager](https://business.facebook.com/)

### Changelog
- [API Changelog](https://developers.facebook.com/docs/graph-api/changelog)
- [Marketing API Changelog](https://developers.facebook.com/docs/marketing-api/changelog)

---

## Conclusão

Esta documentação cobre os principais aspectos da Meta Ads API para criação e gerenciamento de campanhas programaticamente.

**Próximos Passos:**

1. Configure autenticação e obtenha access token
2. Crie uma campanha de teste com status=PAUSED
3. Teste os endpoints com execution_options=validate_only
4. Monitore performance via Insights API
5. Otimize baseado em dados reais
6. Solicite Advanced Access quando estiver pronto para produção

**Lembre-se:**
- Sempre teste em ambiente de desenvolvimento primeiro
- Use status=PAUSED ao criar objetos para evitar gastos acidentais
- Monitore rate limits e implemente retry logic
- Mantenha access tokens seguros
- Documente suas implementações

---

**Última Atualização:** 31 de Outubro de 2025
**Versão da API:** v24.0
**Status:** Documentação completa e pronta para implementação

---
