# 📱 Instagram API - Documentação Completa

**Versão da API:** Instagram Platform (Latest)
**Data de Coleta:** 31 de Outubro de 2025
**Total de Páginas Documentadas:** 77
**Fonte:** https://developers.facebook.com/docs/instagram-platform/

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Configuração da API](#configuração-da-api)
   - [Instagram API com Instagram Login](#instagram-api-com-instagram-login)
   - [Instagram API com Facebook Login](#instagram-api-com-facebook-login)
3. [Autenticação](#autenticação)
4. [Publicação de Conteúdo](#publicação-de-conteúdo)
   - [Posts (Imagens e Vídeos)](#posts-imagens-e-vídeos)
   - [Carrosséis](#carrosséis)
   - [Reels](#reels)
   - [Stories](#stories)
5. [Moderação de Comentários](#moderação-de-comentários)
6. [Respostas Privadas](#respostas-privadas)
7. [Mensagens Diretas (DMs)](#mensagens-diretas-dms)
8. [Insights e Métricas](#insights-e-métricas)
9. [Webhooks](#webhooks)
10. [Rate Limits](#rate-limits)
11. [Erros Comuns](#erros-comuns)
12. [Best Practices](#best-practices)

---

## 🎯 Visão Geral

A Instagram Platform API permite que aplicativos gerenciem contas profissionais do Instagram (Business e Creator accounts). Com esta API você pode:

### Funcionalidades Principais

- ✅ **Publicar Conteúdo** - Posts, Carrosséis, Reels, Stories
- ✅ **Moderar Comentários** - Obter, responder, deletar, ocultar comentários
- ✅ **Gerenciar Mensagens** - Enviar e receber DMs
- ✅ **Obter Insights** - Métricas de conta e mídia
- ✅ **Identificar Menções** - Detectar @menções em posts de outros usuários
- ✅ **Respostas Privadas** - Responder comentários via DM

### Requisitos

**Tipo de Conta:**
- Instagram Business Account OU
- Instagram Creator Account

**Conexão com Facebook Page (opcional):**
- Obrigatório para Instagram API com Facebook Login
- Não necessário para Instagram API com Instagram Login

---

## ⚙️ Configuração da API

Existem duas formas de configurar a Instagram API:

### Instagram API com Instagram Login

**Características:**
- ✅ App users fazem login com credenciais do Instagram
- ✅ Não requer Facebook Page linkada
- ✅ Base URL: `graph.instagram.com`
- ✅ Access Tokens: Instagram User access token

**Permissões Disponíveis:**
- `instagram_business_basic`
- `instagram_business_content_publish`
- `instagram_business_manage_comments`
- `instagram_business_manage_messages`
- `instagram_business_manage_insights`

**Limitações:**
- ❌ Não pode acessar ads ou tagging de produtos

---

### Instagram API com Facebook Login

**Características:**
- ✅ App users fazem login com credenciais do Facebook
- ✅ Requer Facebook Page linkada à conta Instagram
- ✅ Base URL: `graph.facebook.com`
- ✅ Access Tokens: Facebook Page access token

**Permissões Disponíveis:**
- `instagram_basic`
- `instagram_content_publish`
- `instagram_manage_comments`
- `instagram_manage_insights`
- `instagram_manage_messages`
- `pages_show_list`
- `pages_read_engagement`

**Funcionalidades Extras:**
- ✅ Business Discovery (dados de outras contas)
- ✅ Hashtag Search
- ✅ Product Tagging
- ✅ Partnership Ads

---

## 🔐 Autenticação

### Fluxo de Autenticação (OAuth 2.0)

**Passo 1: Authorization Code**
```
Usuário clica no embed URL → Meta abre janela de autorização →
Usuário concede permissões → Meta redireciona com Authorization Code
```

**Validade:** 1 hora

**Passo 2: Short-Lived Access Token**
```
POST https://graph.instagram.com/oauth/access_token
  ?client_id={app-id}
  &client_secret={app-secret}
  &grant_type=authorization_code
  &redirect_uri={redirect-uri}
  &code={code}
```

**Validade:** 1 hora

**Passo 3: Long-Lived Access Token**
```
GET https://graph.instagram.com/access_token
  ?grant_type=ig_exchange_token
  &client_secret={app-secret}
  &access_token={short-lived-token}
```

**Validade:** 60 dias (renovável)

**Passo 4: Refresh Long-Lived Token**
```
GET https://graph.instagram.com/refresh_access_token
  ?grant_type=ig_refresh_token
  &access_token={long-lived-token}
```

---

## 📝 Publicação de Conteúdo

### Posts (Imagens e Vídeos)

#### Processo de Publicação (2 etapas)

**Etapa 1: Criar Container**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media
  ?image_url={image-url}
  &caption={caption}
  &access_token={access-token}
```

**Parâmetros Obrigatórios:**
- `image_url` ou `video_url` - URL pública do arquivo

**Parâmetros Opcionais:**
- `caption` - Legenda do post
- `location_id` - ID da localização
- `user_tags` - Tags de usuários
- `alt_text` - Texto alternativo para acessibilidade (NOVO - 24/03/2025)

**Response:**
```json
{
  "id": "17895695668004550"  // Container ID
}
```

**Etapa 2: Publicar Container**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media_publish
  ?creation_id={container-id}
  &access_token={access-token}
```

**Response:**
```json
{
  "id": "90010778622384"  // Media ID (post publicado)
}
```

---

### Carrosséis

**Processo:**
1. Criar containers para cada imagem/vídeo (até 10 itens)
2. Criar container de carrossel
3. Publicar

**Etapa 1: Criar Containers de Itens**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media
  ?image_url={image-url}
  &is_carousel_item=true
  &access_token={access-token}
```

Repetir para cada item (imagem ou vídeo)

**Etapa 2: Criar Container de Carrossel**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media
  ?media_type=CAROUSEL
  &children={container-id-1},{container-id-2},{container-id-3}
  &caption={caption}
  &access_token={access-token}
```

**Limitações:**
- Máximo 10 itens por carrossel
- Todos os itens são cortados com base no primeiro
- Aspect ratio padrão: 1:1

**Etapa 3: Publicar**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media_publish
  ?creation_id={carousel-container-id}
  &access_token={access-token}
```

---

### Reels

**Criar Container:**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media
  ?media_type=REELS
  &video_url={video-url}
  &caption={caption}
  &share_to_feed=true
  &access_token={access-token}
```

**Parâmetros Importantes:**
- `media_type=REELS` - Define como Reel
- `share_to_feed` - true/false (compartilhar no feed)
- `cover_url` - URL da imagem de capa (opcional)
- `audio_name` - Nome do áudio (opcional)

**Upload Resumível (para vídeos grandes):**

**1. Criar Sessão:**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media
  ?media_type=REELS
  &upload_type=resumable
  &access_token={access-token}
```

**2. Upload do Vídeo:**
```bash
POST https://rupload.facebook.com/ig-api-upload/v24.0/{container-id}
  -H "Authorization: OAuth {access-token}"
  -H "offset: 0"
  -H "file_size: {bytes}"
  --data-binary "@video.mp4"
```

**3. Publicar:**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/media_publish
  ?creation_id={container-id}
  &access_token={access-token}
```

---

### Stories

**Criar e Publicar Story:**
```bash
# Etapa 1: Criar Container
POST https://graph.instagram.com/v24.0/{ig-user-id}/media
  ?image_url={image-url}  # ou video_url
  &media_type=STORIES
  &access_token={access-token}

# Etapa 2: Publicar
POST https://graph.instagram.com/v24.0/{ig-user-id}/media_publish
  ?creation_id={container-id}
  &access_token={access-token}
```

**Limitações:**
- Stories expiram em 24 horas
- Apenas para Business Accounts (não Creator)
- Insights disponíveis apenas nas primeiras 24 horas

---

## 💬 Moderação de Comentários

### Obter Comentários

**Via API:**
```bash
GET https://graph.instagram.com/v24.0/{media-id}/comments
  ?fields=id,text,timestamp,username,like_count,replies
  &access_token={access-token}
```

**Response:**
```json
{
  "data": [
    {
      "id": "17870913679156914",
      "text": "This is awesome!",
      "timestamp": "2017-08-31T19:16:02+0000",
      "username": "johndoe",
      "like_count": 5
    }
  ]
}
```

**Via Webhooks (Recomendado):**

Payload recebido quando há novo comentário:
```json
{
  "object": "instagram",
  "entry": [{
    "id": "{instagram-account-id}",
    "time": 1520383571,
    "changes": [{
      "field": "comments",
      "value": {
        "from": {
          "id": "{instagram-scoped-user-id}",
          "username": "johndoe"
        },
        "comment_id": "{comment-id}",
        "text": "Amazing post!",
        "media": {
          "id": "{media-id}",
          "media_product_type": "FEED"
        }
      }
    }]
  }]
}
```

---

### Responder a Comentários

```bash
POST https://graph.instagram.com/v24.0/{comment-id}/replies
  ?message={reply-text}
  &access_token={access-token}
```

**Response:**
```json
{
  "id": "17873440459141029"  // Reply comment ID
}
```

---

### Deletar Comentários

```bash
DELETE https://graph.instagram.com/v24.0/{comment-id}
  ?access_token={access-token}
```

**Response:**
```json
{
  "success": true
}
```

---

### Ocultar/Mostrar Comentários

```bash
POST https://graph.instagram.com/v24.0/{comment-id}
  ?hide=true  # ou false para mostrar
  &access_token={access-token}
```

---

### Desabilitar Comentários em Post

```bash
POST https://graph.instagram.com/v24.0/{media-id}
  ?comment_enabled=false
  &access_token={access-token}
```

---

## 📨 Respostas Privadas

Enviar DM para quem comentou em um post:

```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/messages
  -H "Content-Type: application/json"
  -d '{
    "recipient": {
      "comment_id": "{comment-id}"
    },
    "message": {
      "text": "Thanks for your comment!"
    }
  }'
```

**Limitações:**
- ✅ Apenas 1 mensagem pode ser enviada
- ✅ Deve ser enviada dentro de 7 dias do comentário
- ✅ Para Instagram Live: apenas durante a transmissão
- ✅ Follow-up somente se o destinatário responder (24h)

**Response:**
```json
{
  "recipient_id": "526...",
  "message_id": "aWdfZ..."
}
```

---

## 💬 Mensagens Diretas (DMs)

### Via Instagram API com Instagram Login

**Enviar Mensagem:**
```bash
POST https://graph.instagram.com/v24.0/{ig-user-id}/messages
  -H "Content-Type: application/json"
  -d '{
    "recipient": {
      "id": "{instagram-scoped-user-id}"
    },
    "message": {
      "text": "Hello! How can I help you?"
    }
  }'
```

**Tipos de Mensagem Suportados:**
- Texto
- Imagem
- Vídeo
- Stickers
- Links
- Reações

---

### Via Messenger Platform (Instagram API com Facebook Login)

**Endpoint:** `graph.facebook.com`

Consultar documentação completa: [Messenger Platform Instagram Messaging](https://developers.facebook.com/docs/messenger-platform/instagram)

**Principais Recursos:**
- ✅ Ice Breakers
- ✅ Botões de Resposta Rápida
- ✅ Generic Templates
- ✅ Handover Protocol
- ✅ Tags (human_agent, etc)

---

## 📊 Insights e Métricas

### Insights de Conta

```bash
GET https://graph.instagram.com/v24.0/{ig-user-id}/insights
  ?metric=impressions,reach,profile_views
  &period=day
  &access_token={access-token}
```

**Métricas Disponíveis:**

| Métrica | Descrição | Período |
|---------|-----------|---------|
| `impressions` | Total de visualizações | day, week, days_28 |
| `reach` | Contas únicas alcançadas | day, week, days_28 |
| `profile_views` | Visualizações de perfil | day |
| `follower_count` | Total de seguidores | day |
| `email_contacts` | Cliques em email | day |
| `phone_call_clicks` | Cliques em telefone | day |
| `text_message_clicks` | Cliques em mensagem | day |
| `get_directions_clicks` | Cliques em direções | day |
| `website_clicks` | Cliques em website | day |

**Response:**
```json
{
  "data": [{
    "name": "impressions",
    "period": "day",
    "values": [{
      "value": 32,
      "end_time": "2018-01-11T08:00:00+0000"
    }],
    "title": "Impressions",
    "description": "Total de visualizações",
    "id": "{account-id}/insights/impressions/day"
  }]
}
```

---

### Insights de Mídia

```bash
GET https://graph.instagram.com/v24.0/{media-id}/insights
  ?metric=engagement,impressions,reach,saved
  &access_token={access-token}
```

**Métricas Disponíveis:**

**Para Posts e Reels:**
- `engagement` - Total de interações
- `impressions` - Total de visualizações
- `reach` - Contas únicas alcançadas
- `saved` - Total de saves
- `video_views` - Visualizações de vídeo (apenas vídeos)
- `likes` - Total de likes
- `comments` - Total de comentários
- `shares` - Total de compartilhamentos

**Para Stories:**
- `exits` - Saídas da story
- `impressions` - Visualizações
- `reach` - Contas únicas
- `replies` - Respostas
- `taps_forward` - Taps para frente
- `taps_back` - Taps para trás

**Limitações:**
- Requer mínimo 100 seguidores para algumas métricas
- Dados armazenados por até 90 dias
- Stories: insights apenas nas primeiras 24 horas

---

## 🔔 Webhooks

### Configuração

**1. Criar Endpoint no seu servidor**

Seu endpoint deve processar:
- **Verificação (GET)** - Validação inicial pela Meta
- **Notificações (POST)** - Eventos recebidos

**Exemplo de Verificação:**
```
GET https://seu-dominio.com/webhooks
  ?hub.mode=subscribe
  &hub.challenge=1158201444
  &hub.verify_token=seu-token-secreto
```

Seu servidor deve responder com `hub.challenge`

**2. Assinar Webhooks no App Dashboard**

Campos disponíveis:
- `comments` - Novos comentários
- `live_comments` - Comentários em Live
- `mentions` - Menções (@)
- `messages` - Novas mensagens
- `message_reactions` - Reações em mensagens
- `messaging_seen` - Mensagens vistas
- `story_insights` - Insights de stories

**3. Habilitar Subscrições via API**

```bash
POST https://graph.instagram.com/v24.0/me/subscribed_apps
  ?subscribed_fields=comments,messages
  &access_token={access-token}
```

**Response:**
```json
{
  "success": true
}
```

---

### Validação de Payloads

**Verificar Assinatura:**

Toda notificação inclui header `X-Hub-Signature-256`:
```
X-Hub-Signature-256: sha256={signature}
```

**Validar:**
1. Gerar SHA256 do payload usando App Secret
2. Comparar com signature do header
3. Aceitar apenas se forem idênticas

**Resposta:**
Sempre responder com `200 OK` para todas as notificações

---

### Payload de Comentário

```json
{
  "object": "instagram",
  "entry": [{
    "id": "{account-id}",
    "time": 1520383571,
    "changes": [{
      "field": "comments",
      "value": {
        "from": {
          "id": "{user-id}",
          "username": "johndoe"
        },
        "comment_id": "{comment-id}",
        "text": "Amazing!",
        "media": {
          "id": "{media-id}",
          "media_product_type": "FEED"
        }
      }
    }]
  }]
}
```

---

### Payload de Mensagem

```json
{
  "object": "instagram",
  "entry": [{
    "id": "{account-id}",
    "time": 1520383571,
    "messaging": [{
      "sender": {
        "id": "{user-id}"
      },
      "recipient": {
        "id": "{account-id}"
      },
      "timestamp": 1520383571,
      "message": {
        "mid": "{message-id}",
        "text": "Hello!"
      }
    }]
  }]
}
```

---

## ⏱️ Rate Limits

### Publicação de Conteúdo

**Limite:** 100 posts via API por 24 horas (rolling window)

**Verificar uso atual:**
```bash
GET https://graph.instagram.com/v24.0/{ig-user-id}/content_publishing_limit
  ?access_token={access-token}
```

**Response:**
```json
{
  "data": [{
    "quota_usage": 25,  // Posts publicados nas últimas 24h
    "config": {
      "quota_total": 100,
      "quota_duration": 86400  // segundos (24h)
    }
  }]
}
```

---

### Chamadas de API Gerais

**Fórmula:**
```
Calls em 24h = 4800 * Número de Impressions
```

Onde "Impressions" = vezes que conteúdo da conta apareceu em telas nas últimas 24h

**Exceções (Platform Rate Limits):**
- Business Discovery
- Hashtag Search

---

### Messaging Rate Limits

**Conversations API:**
- 2 calls/segundo por conta Instagram

**Private Replies API:**
- 100 calls/segundo para Live comments
- 750 calls/hora para posts/reels comments

**Send API:**
- 100 calls/segundo para texto/links/reações/stickers
- 10 calls/segundo para áudio/vídeo

---

## ⚠️ Erros Comuns

### Erro: Container Publishing Failed

**Causa:** Container não completou processamento

**Verificar Status:**
```bash
GET https://graph.instagram.com/v24.0/{container-id}
  ?fields=status_code
  &access_token={access-token}
```

**Status Codes:**
- `EXPIRED` - Container expirou (24h sem publicar)
- `ERROR` - Falha no processamento
- `FINISHED` - Pronto para publicar
- `IN_PROGRESS` - Ainda processando
- `PUBLISHED` - Já publicado

**Solução:** Aguardar `FINISHED` antes de publicar

---

### Erro: (#100) Invalid media ID

**Causa:** Media ID inválido ou container ID usado no lugar de media ID

**Solução:**
- Container ID: usado para publicar
- Media ID: recebido após publicação (para queries)

---

### Erro: Rate Limit Exceeded

**Causa:** Excedeu limite de chamadas

**Solução:**
- Implementar exponential backoff
- Usar webhooks para reduzir queries
- Cachear dados quando possível
- Verificar `content_publishing_limit` antes de publicar

---

### Erro: Page Publishing Authorization Required

**Causa:** Facebook Page requer PPA

**Solução:**
- Completar PPA no Business Manager
- Orientar usuários a completar PPA preventivamente

---

### Erro: Invalid Access Token

**Causa:** Token expirado ou inválido

**Solução:**
- Renovar long-lived token antes de expirar (60 dias)
- Implementar refresh automático
- Solicitar novo token via login flow

---

## ✅ Best Practices

### 1. Use Webhooks em Vez de Polling

**❌ Evitar:**
```bash
# Polling a cada minuto para novos comentários
while true; do
  curl "https://graph.instagram.com/v24.0/{media-id}/comments"
  sleep 60
done
```

**✅ Recomendado:**
```javascript
// Receber notificação via webhook
app.post('/webhooks', (req, res) => {
  const data = req.body;
  if (data.field === 'comments') {
    processNewComment(data.value);
  }
  res.status(200).send('OK');
});
```

---

### 2. Valide Containers Antes de Publicar

```bash
# 1. Criar container
POST /media (retorna container-id)

# 2. Verificar status
GET /{container-id}?fields=status_code

# 3. Publicar somente se FINISHED
if status_code == "FINISHED":
  POST /media_publish?creation_id={container-id}
```

---

### 3. Implementar Retry com Exponential Backoff

```python
import time

def publish_with_retry(container_id, max_retries=5):
    for attempt in range(max_retries):
        try:
            return api.publish(container_id)
        except RateLimitError:
            wait = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

---

### 4. Renovar Tokens Automaticamente

```javascript
// Renovar 7 dias antes de expirar
async function refreshTokenIfNeeded(token, expiresAt) {
  const daysUntilExpiry = (expiresAt - Date.now()) / (1000 * 60 * 60 * 24);

  if (daysUntilExpiry < 7) {
    const newToken = await refreshLongLivedToken(token);
    saveToken(newToken);
    return newToken;
  }

  return token;
}
```

---

### 5. Armazene Media URLs Permanentemente

**Problema:** CDN URLs podem expirar

**Solução:**
```javascript
// Ao receber webhook de novo media
async function onNewMedia(mediaId) {
  const media = await api.getMedia(mediaId, ['media_url']);

  // Download e armazenamento permanente
  const localPath = await downloadAndStore(media.media_url);

  db.save({
    media_id: mediaId,
    cdn_url: media.media_url,  // Pode expirar
    local_path: localPath       // Permanente
  });
}
```

---

### 6. Gerencie Limites de Publicação

```javascript
async function schedulePost(igUserId, postData, scheduledTime) {
  // Verificar limite antes de agendar
  const limit = await api.getPublishingLimit(igUserId);

  if (limit.quota_usage >= 95) {
    throw new Error('Approaching rate limit, schedule for later');
  }

  // Agendar publicação
  scheduleJob(scheduledTime, () => publishPost(postData));
}
```

---

### 7. Sempre Defina `status=PAUSED` para Testes

**Para containers de teste:**
```bash
POST /media
  ?image_url={url}
  &caption=Test post
  # Não publicar automaticamente, apenas criar container
```

---

### 8. Use Resumable Upload para Vídeos Grandes

**Para vídeos > 100MB ou conexões instáveis:**
```bash
# 1. Criar sessão resumível
POST /media?upload_type=resumable&media_type=REELS

# 2. Upload em chunks
POST https://rupload.facebook.com/ig-api-upload/{container-id}
  -H "offset: 0"
  -H "file_size: {total-bytes}"
  --data-binary @video-chunk-1.mp4

# 3. Continuar upload se houver falha
POST https://rupload.facebook.com/ig-api-upload/{container-id}
  -H "offset: {bytes-uploaded}"
  -H "file_size: {total-bytes}"
  --data-binary @video-chunk-2.mp4
```

---

### 9. Implemente Logs Estruturados

```javascript
logger.info('Publishing post', {
  ig_user_id: userId,
  container_id: containerId,
  media_type: 'IMAGE',
  caption_length: caption.length,
  timestamp: Date.now()
});

logger.error('Publishing failed', {
  error_code: error.code,
  error_message: error.message,
  container_id: containerId,
  retry_count: retries
});
```

---

### 10. Monitore Webhooks Health

```javascript
// Track webhook delivery rate
const webhookMetrics = {
  received: 0,
  processed: 0,
  failed: 0,
  avgProcessingTime: 0
};

app.post('/webhooks', async (req, res) => {
  const startTime = Date.now();
  webhookMetrics.received++;

  try {
    await processWebhook(req.body);
    webhookMetrics.processed++;
  } catch (error) {
    webhookMetrics.failed++;
    logger.error('Webhook processing failed', error);
  }

  webhookMetrics.avgProcessingTime =
    (Date.now() - startTime + webhookMetrics.avgProcessingTime) / 2;

  res.status(200).send('OK');
});
```

---

## 📚 Recursos Adicionais

### Links Oficiais

- **Documentação Completa:** https://developers.facebook.com/docs/instagram-platform/
- **Instagram Graph API Reference:** https://developers.facebook.com/docs/instagram-api/reference
- **App Dashboard:** https://developers.facebook.com/apps
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer
- **Webhooks Tester:** https://developers.facebook.com/tools/webhooks/

### Exemplos de Código

- **GitHub Samples:** https://github.com/fbsamples/
- **Reels Publishing Sample:** https://github.com/fbsamples/reels_publishing_apis
- **Webhooks Sample:** https://github.com/fbsamples/graph-api-webhooks-samples

### Suporte

- **Developer Community:** https://developers.facebook.com/community/
- **Bug Reports:** https://developers.facebook.com/support/bugs/
- **Feature Requests:** https://developers.facebook.com/community/feature-requests/

---

## 📝 Changelog

### 2025-10-31
- ✅ Documentação completa extraída e organizada
- ✅ 77 páginas de documentação consolidadas
- ✅ Exemplos práticos em todos os endpoints
- ✅ Best practices e troubleshooting

### 2025-03-24
- ✅ Novo campo `alt_text` para acessibilidade em posts de imagem

---

**Nota:** Esta documentação foi gerada a partir da extração completa da documentação oficial do Instagram Platform em 31 de Outubro de 2025.

Para informações sempre atualizadas, consulte a [documentação oficial](https://developers.facebook.com/docs/instagram-platform/).
