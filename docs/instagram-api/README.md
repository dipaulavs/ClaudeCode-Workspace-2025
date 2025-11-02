# Instagram API - Documentação

Documentação completa da Instagram Platform API para criação e gerenciamento de conteúdo no Instagram de forma programática.

## 📚 Arquivos Disponíveis

### [INSTAGRAM_API_DOCUMENTATION.md](./INSTAGRAM_API_DOCUMENTATION.md)
**Documentação principal completa e atualizada**

Contém:
- ✅ Guia completo de autenticação (Instagram Login e Facebook Login)
- ✅ Publicação de Posts, Carrosséis, Reels e Stories
- ✅ Moderação de comentários e respostas privadas
- ✅ Gerenciamento de mensagens diretas (DMs)
- ✅ Insights e métricas de conta e mídia
- ✅ Configuração completa de webhooks
- ✅ Rate limits e otimização
- ✅ Best practices e troubleshooting
- ✅ Exemplos práticos em todos os endpoints

## 🎯 Quando Consultar Esta Documentação

**Use esta documentação quando precisar:**

1. **Publicar Conteúdo no Instagram**
   - Consulte a seção "Publicação de Conteúdo"
   - Veja exemplos de Posts, Carrosséis, Reels e Stories

2. **Gerenciar Comentários**
   - Consulte a seção "Moderação de Comentários"
   - Veja como obter, responder, deletar e ocultar comentários

3. **Enviar Mensagens Diretas**
   - Consulte a seção "Mensagens Diretas (DMs)"
   - Veja "Respostas Privadas" para responder comentários via DM

4. **Obter Métricas e Insights**
   - Consulte a seção "Insights e Métricas"
   - Veja métricas de conta e mídia

5. **Configurar Webhooks**
   - Consulte a seção "Webhooks"
   - Veja exemplos de payloads e validação

6. **Resolver Erros**
   - Consulte a seção "Erros Comuns"
   - Veja "Troubleshooting" para soluções

7. **Otimizar sua Aplicação**
   - Consulte "Best Practices"
   - Veja "Rate Limits" para gestão de quotas

## 📊 Estrutura da API

```
Instagram Platform API
├── Autenticação
│   ├── Instagram Login (Instagram User tokens)
│   └── Facebook Login (Facebook Page tokens)
│
├── Publicação de Conteúdo
│   ├── Posts (Imagens e Vídeos)
│   ├── Carrosséis (até 10 itens)
│   ├── Reels (vídeos curtos)
│   └── Stories (24h de duração)
│
├── Interações
│   ├── Comentários (obter, responder, deletar, ocultar)
│   ├── Respostas Privadas (DM após comentário)
│   └── Mensagens Diretas (Conversations API)
│
├── Insights
│   ├── Métricas de Conta (impressions, reach, followers)
│   └── Métricas de Mídia (engagement, saves, shares)
│
└── Webhooks
    ├── comments (novos comentários)
    ├── mentions (menções @)
    ├── messages (novas mensagens)
    └── story_insights (métricas de stories)
```

## 🔑 Quick Reference

### Base URLs

**Instagram Login:**
```
https://graph.instagram.com/v24.0
```

**Facebook Login:**
```
https://graph.facebook.com/v24.0
```

### Principais Endpoints

| Funcionalidade | Método | Endpoint |
|----------------|--------|----------|
| **Criar Container (Post/Reel)** | POST | `/{ig-user-id}/media` |
| **Publicar Container** | POST | `/{ig-user-id}/media_publish` |
| **Obter Comentários** | GET | `/{media-id}/comments` |
| **Responder Comentário** | POST | `/{comment-id}/replies` |
| **Enviar Mensagem** | POST | `/{ig-user-id}/messages` |
| **Insights de Conta** | GET | `/{ig-user-id}/insights` |
| **Insights de Mídia** | GET | `/{media-id}/insights` |
| **Verificar Rate Limit** | GET | `/{ig-user-id}/content_publishing_limit` |

### Permissões Principais

**Instagram Login:**
- `instagram_business_basic`
- `instagram_business_content_publish`
- `instagram_business_manage_comments`
- `instagram_business_manage_messages`
- `instagram_business_manage_insights`

**Facebook Login:**
- `instagram_basic`
- `instagram_content_publish`
- `instagram_manage_comments`
- `instagram_manage_insights`
- `instagram_manage_messages`
- `pages_show_list`
- `pages_read_engagement`

## 📝 Exemplo Rápido - Publicar Post

```bash
# 1. Criar Container
curl -X POST \
  "https://graph.instagram.com/v24.0/90010177253934/media" \
  -F "image_url=https://example.com/image.jpg" \
  -F "caption=Minha primeira publicação via API!" \
  -F "access_token=YOUR_ACCESS_TOKEN"

# Response: { "id": "17895695668004550" }

# 2. Publicar
curl -X POST \
  "https://graph.instagram.com/v24.0/90010177253934/media_publish" \
  -F "creation_id=17895695668004550" \
  -F "access_token=YOUR_ACCESS_TOKEN"

# Response: { "id": "90010778622384" }  ← Media ID do post publicado
```

## 📝 Exemplo Rápido - Responder Comentário

```bash
# Responder a um comentário
curl -X POST \
  "https://graph.instagram.com/v24.0/17870913679156914/replies" \
  -F "message=Obrigado pelo feedback!" \
  -F "access_token=YOUR_ACCESS_TOKEN"

# Response: { "id": "17873440459141029" }
```

## 📝 Exemplo Rápido - Obter Insights

```bash
# Insights de conta (últimas 24h)
curl -X GET \
  "https://graph.instagram.com/v24.0/17841405822304914/insights \
   ?metric=impressions,reach,profile_views \
   &period=day \
   &access_token=YOUR_ACCESS_TOKEN"
```

## ⚠️ Limitações Importantes

### Rate Limits

- **Publicação:** 100 posts via API por 24 horas
- **API Geral:** 4800 * número de impressions (rolling 24h)
- **Messaging:** 2 calls/segundo por conta

### Tipos de Conta

- ✅ Instagram Business Account
- ✅ Instagram Creator Account
- ❌ Instagram Personal Account (não suportado)

### Formatos de Mídia

**Imagens:**
- ✅ JPEG
- ❌ PNG (não suportado)
- ❌ GIF (não suportado)

**Vídeos:**
- ✅ MP4, MOV
- ⏱️ Duração: 3s - 60s (Reels até 90s)
- 📏 Tamanho: até 100MB (use resumable upload para maiores)

## 🔗 Links Úteis

- [Instagram Platform API Docs](https://developers.facebook.com/docs/instagram-platform/)
- [Instagram Graph API Reference](https://developers.facebook.com/docs/instagram-api/reference)
- [Meta App Dashboard](https://developers.facebook.com/apps)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Webhooks Debugger](https://developers.facebook.com/tools/webhooks/)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken)

## 📅 Informações da Documentação

- **Data de Coleta:** 31 de Outubro de 2025
- **Total de Páginas:** 77 páginas extraídas
- **Tamanho:** 548KB de conteúdo consolidado
- **Status:** Completa e atualizada
- **Fonte:** https://developers.facebook.com/docs/instagram-platform/

---

💡 **Dica:** Sempre use webhooks para receber notificações em tempo real e reduzir chamadas de API, evitando rate limiting.
