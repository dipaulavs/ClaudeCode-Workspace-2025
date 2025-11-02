# 📚 Documentação - ClaudeCode Workspace

Índice de toda a documentação de APIs e integrações disponíveis no workspace.

---

## 🗂️ Documentações Disponíveis

### 1. [Meta Ads API](./meta-ads-api/)
**Documentação completa da Meta (Facebook/Instagram) Ads API**

📄 **Arquivo principal:** [`META_ADS_API_DOCUMENTATION.md`](./meta-ads-api/META_ADS_API_DOCUMENTATION.md)

**Conteúdo:**
- ✅ Autenticação e autorização completa
- ✅ Criação de campanhas, ad sets, ads e creatives
- ✅ Todos os parâmetros e opções disponíveis
- ✅ Exemplos práticos em cURL
- ✅ Fluxo end-to-end de criação
- ✅ Otimização e monitoramento
- ✅ Best practices e troubleshooting

**Versão da API:** v24.0
**Última atualização:** 31 de Outubro de 2025

**Quando usar:**
- Criar campanhas programaticamente no Facebook/Instagram
- Automatizar gerenciamento de anúncios
- Integrar Meta Ads com outras ferramentas
- Consultar parâmetros e endpoints da API

---

### 2. [Instagram API](./instagram-api/)
**Documentação completa da Instagram Platform API**

📄 **Arquivo principal:** [`INSTAGRAM_API_DOCUMENTATION.md`](./instagram-api/INSTAGRAM_API_DOCUMENTATION.md)

**Conteúdo:**
- ✅ Autenticação (Instagram Login e Facebook Login)
- ✅ Publicação de Posts, Carrosséis, Reels e Stories
- ✅ Moderação de comentários e respostas privadas
- ✅ Gerenciamento de mensagens diretas (DMs)
- ✅ Insights e métricas de conta e mídia
- ✅ Configuração completa de webhooks
- ✅ Rate limits e otimização
- ✅ Best practices e troubleshooting

**Versão da API:** Instagram Platform (Latest)
**Total de Páginas:** 77 páginas extraídas (548KB)
**Última atualização:** 31 de Outubro de 2025

**Quando usar:**
- Publicar posts, carrosséis, Reels e Stories programaticamente
- Gerenciar comentários e interações
- Enviar e receber mensagens diretas (DMs)
- Obter métricas e insights de performance
- Automatizar moderação de conteúdo
- Integrar Instagram com outras ferramentas

---

## 📋 Como Usar Esta Documentação

### Para Desenvolvedores

Ao criar ferramentas ou integrações que usem as APIs documentadas:

1. **Consulte o README** de cada pasta para visão geral
2. **Abra o arquivo de documentação completo** para detalhes técnicos
3. **Use os exemplos práticos** como base para seu código
4. **Consulte as seções de troubleshooting** quando encontrar erros

### Para Claude Code (Agentes)

Quando precisar criar ou editar campanhas/integrações:

1. **Consulte primeiro o README** da API específica
2. **Busque na documentação completa** os parâmetros necessários
3. **Use os exemplos** como referência para requests
4. **Verifique best practices** antes de implementar

### Estrutura dos Arquivos

Cada documentação de API segue esta estrutura:

```
docs/
├── README.md (este arquivo - índice geral)
└── [nome-da-api]/
    ├── README.md (visão geral e quick reference)
    └── [NOME]_API_DOCUMENTATION.md (documentação completa)
```

---

## 🔍 Quick Reference

### Meta Ads API

**Base URL:** `https://graph.facebook.com/v24.0`

**Principais Endpoints:**
```bash
# Campaigns
POST /act_<AD_ACCOUNT_ID>/campaigns

# Ad Sets
POST /act_<AD_ACCOUNT_ID>/adsets

# Ads
POST /act_<AD_ACCOUNT_ID>/ads

# Ad Creatives
POST /act_<AD_ACCOUNT_ID>/adcreatives

# Insights (Analytics)
GET /act_<AD_ACCOUNT_ID>/insights
```

**Documentação completa:** [`meta-ads-api/META_ADS_API_DOCUMENTATION.md`](./meta-ads-api/META_ADS_API_DOCUMENTATION.md)

---

### Instagram API

**Base URLs:**
- Instagram Login: `https://graph.instagram.com/v24.0`
- Facebook Login: `https://graph.facebook.com/v24.0`

**Principais Endpoints:**
```bash
# Criar Container (Post/Reel/Story)
POST /{ig-user-id}/media

# Publicar Container
POST /{ig-user-id}/media_publish

# Obter Comentários
GET /{media-id}/comments

# Responder Comentário
POST /{comment-id}/replies

# Enviar Mensagem
POST /{ig-user-id}/messages

# Insights de Conta
GET /{ig-user-id}/insights

# Insights de Mídia
GET /{media-id}/insights
```

**Documentação completa:** [`instagram-api/INSTAGRAM_API_DOCUMENTATION.md`](./instagram-api/INSTAGRAM_API_DOCUMENTATION.md)

---

## 📝 Contribuindo

Para adicionar nova documentação de API:

1. Crie uma pasta em `docs/` com o nome da API (ex: `google-ads-api`)
2. Adicione um `README.md` com overview e quick reference
3. Adicione a documentação completa (ex: `GOOGLE_ADS_API_DOCUMENTATION.md`)
4. Atualize este índice (`docs/README.md`)

### Template de Estrutura

```
docs/
└── nova-api/
    ├── README.md
    │   - Overview da API
    │   - Quick reference
    │   - Exemplos rápidos
    │   - Links úteis
    │
    └── NOVA_API_DOCUMENTATION.md
        - Introdução
        - Autenticação
        - Endpoints completos
        - Parâmetros detalhados
        - Exemplos práticos
        - Best practices
        - Troubleshooting
```

---

## 🔗 Links Úteis

### Meta/Facebook
- [Meta for Developers](https://developers.facebook.com/)
- [Marketing API Docs](https://developers.facebook.com/docs/marketing-api/)
- [Instagram Platform Docs](https://developers.facebook.com/docs/instagram-platform/)
- [Instagram Graph API Reference](https://developers.facebook.com/docs/instagram-api/reference)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken)
- [Webhooks Debugger](https://developers.facebook.com/tools/webhooks/)

### Ferramentas
- [Meta Ads Manager](https://adsmanager.facebook.com/)
- [Meta Business Manager](https://business.facebook.com/)
- [Meta App Dashboard](https://developers.facebook.com/apps)

---

## 📅 Changelog

### 2025-10-31
- ✅ Adicionada documentação completa da Instagram API (77 páginas, 548KB)
- ✅ Adicionada documentação completa da Meta Ads API v24.0
- ✅ Criada estrutura organizada de documentação
- ✅ Adicionado índice geral e quick references

---

💡 **Dica:** Use Ctrl+F (ou Cmd+F) para buscar rapidamente por termos específicos dentro das documentações.
