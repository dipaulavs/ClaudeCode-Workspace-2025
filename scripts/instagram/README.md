# 📸 Instagram Templates - Graph API

Scripts prontos para automação de Instagram via Graph API.

**Status:** ✅ **7 templates funcionais e testados** (atualizado em 01/11/2025)

## ✨ Melhorias Recentes

### 🎯 Conversão Automática PNG → JPG
Todos os templates de publicação agora convertem PNG automaticamente para JPG!
- ✅ **publish_story.py** - Conversão automática implementada
- ✅ **publish_post.py** - Conversão automática implementada
- ✅ **publish_carousel.py** - Conversão automática implementada
- ✅ **publish_reel.py** - Aceita PNG na capa

**Benefício:** Não precisa mais converter manualmente ou se preocupar com formato!

### 📋 Testes Completos Realizados
Todos os templates foram testados em 01/11/2025:
- ✅ Post simples - Funcionando (PNG auto-convertido)
- ✅ Carrossel - Funcionando (3 PNG convertidos e publicados)
- ✅ Reel - Funcionando (vídeo + capa PNG)
- ✅ Story - Funcionando (PNG auto-convertido)
- ✅ Comentários - Funcionando (listar, responder, deletar, ocultar)
- ✅ Insights - Funcionando (métricas da conta)
- ⚠️ DMs - Script funcional, mas requer permissões adicionais da API

---

## 📋 Templates Disponíveis

### 1. publish_post.py - Publicar Post

Publica posts simples (imagem única) no Instagram.

#### Uso:
```bash
# Publicar imagem local
python3 scripts/instagram/publish_post.py \
  --image "/path/to/image.jpg" \
  --caption "Meu post no Instagram! #hashtag"

# Publicar via URL
python3 scripts/instagram/publish_post.py \
  --image "https://exemplo.com/imagem.jpg" \
  --caption "Post com imagem online #marketing"

# Publicar com location_id (localização)
python3 scripts/instagram/publish_post.py \
  --image "foto.jpg" \
  --caption "Visitando esse lugar incrível! 📍" \
  --location 123456789
```

#### Parâmetros:
- `--image`, `-i` (obrigatório): Caminho local ou URL da imagem
- `--caption`, `-c` (obrigatório): Texto do post (pode incluir hashtags)
- `--location`, `-l` (opcional): ID da localização do Instagram

#### Notas:
- Formato: JPG ou PNG
- Tamanho recomendado: 1080x1080px (quadrado) ou 1080x1350px (vertical)
- Máximo de 30 hashtags por post

---

### 2. publish_carousel.py - Publicar Carrossel

Publica carrosseis (álbuns) com 2-10 imagens no Instagram.

#### Uso:
```bash
# Carrossel com imagens locais
python3 scripts/instagram/publish_carousel.py \
  --images "foto1.jpg,foto2.jpg,foto3.jpg" \
  --caption "Veja essas fotos incríveis! 📸 #album"

# Carrossel com URLs
python3 scripts/instagram/publish_carousel.py \
  --images "https://site.com/img1.jpg,https://site.com/img2.jpg" \
  --caption "Galeria online #fotos"

# Carrossel com localização
python3 scripts/instagram/publish_carousel.py \
  --images "img1.jpg,img2.jpg,img3.jpg,img4.jpg" \
  --caption "Tour pela cidade! 🏙️" \
  --location 987654321
```

#### Parâmetros:
- `--images`, `-i` (obrigatório): Caminhos ou URLs separados por vírgula
- `--caption`, `-c` (obrigatório): Texto do carrossel
- `--location`, `-l` (opcional): ID da localização

#### Restrições:
- Mínimo: 2 imagens
- Máximo: 10 imagens
- Todas as imagens devem ter proporção similar
- Formatos: JPG ou PNG

---

### 3. publish_reel.py - Publicar Reel

Publica Reels (vídeos curtos) no Instagram.

#### Uso:
```bash
# Reel com vídeo local
python3 scripts/instagram/publish_reel.py \
  --video "/path/to/video.mp4" \
  --caption "Novo Reel! 🎥 #reels #viral"

# Reel via URL com capa personalizada
python3 scripts/instagram/publish_reel.py \
  --video "https://exemplo.com/video.mp4" \
  --caption "Confira esse conteúdo! #trending" \
  --cover "capa.jpg"

# Reel com localização
python3 scripts/instagram/publish_reel.py \
  --video "meu_reel.mp4" \
  --caption "Gravado aqui! 📍" \
  --location 555666777
```

#### Parâmetros:
- `--video`, `-v` (obrigatório): Caminho local ou URL do vídeo
- `--caption`, `-c` (obrigatório): Texto do Reel
- `--cover`, `-cv` (opcional): Imagem de capa (thumbnail)
- `--location`, `-l` (opcional): ID da localização

#### Especificações técnicas:
- Formato: MP4 ou MOV
- Duração: 3 segundos a 90 segundos
- Proporção: 9:16 (vertical)
- Resolução recomendada: 1080x1920px
- Taxa de quadros: 23-60 FPS
- Codec: H.264

---

### 4. publish_story.py - Publicar Story

Publica Stories (imagem ou vídeo que dura 24h) no Instagram.

#### Uso:
```bash
# Story com imagem
python3 scripts/instagram/publish_story.py \
  --media "story.jpg" \
  --type image

# Story com vídeo
python3 scripts/instagram/publish_story.py \
  --media "video_story.mp4" \
  --type video

# Story via URL
python3 scripts/instagram/publish_story.py \
  --media "https://exemplo.com/story.jpg" \
  --type image
```

#### Parâmetros:
- `--media`, `-m` (obrigatório): Caminho local ou URL da mídia
- `--type`, `-t` (obrigatório): Tipo de mídia (`image` ou `video`)

#### Especificações:
**Imagem:**
- Formato: JPG ou PNG
- Proporção: 9:16 (vertical)
- Resolução recomendada: 1080x1920px

**Vídeo:**
- Formato: MP4 ou MOV
- Duração: 3 segundos a 60 segundos
- Proporção: 9:16 (vertical)
- Resolução recomendada: 1080x1920px

#### Notas:
- Stories desaparecem após 24 horas
- Não é possível adicionar caption via API

---

### 5. get_insights.py - Obter Métricas

Obtém estatísticas e insights da conta ou posts específicos.

#### Uso:
```bash
# Insights da conta (últimos 30 dias)
python3 scripts/instagram/get_insights.py --scope account

# Insights de um post específico
python3 scripts/instagram/get_insights.py \
  --scope media \
  --media-id 17895695668004550

# Insights dos últimos posts publicados
python3 scripts/instagram/get_insights.py \
  --scope recent \
  --limit 10
```

#### Parâmetros:
- `--scope`, `-s` (obrigatório): Escopo das métricas (`account`, `media`, `recent`)
- `--media-id`, `-m` (condicional): ID do post (obrigatório se scope=media)
- `--limit`, `-l` (opcional): Número de posts recentes (padrão: 5, máx: 25)

#### Métricas retornadas:

**Account (conta):**
- `impressions` - Total de visualizações
- `reach` - Alcance único
- `follower_count` - Número de seguidores
- `profile_views` - Visualizações do perfil

**Media (post específico):**
- `impressions` - Visualizações do post
- `reach` - Alcance do post
- `engagement` - Curtidas + comentários + salvamentos
- `saved` - Número de salvamentos
- `video_views` - Visualizações (se for vídeo/reel)

**Recent (posts recentes):**
- Métricas de cada post recente
- Performance comparativa

---

### 6. manage_comments.py - Gerenciar Comentários

Gerencia comentários dos posts (listar, responder, ocultar, deletar).

#### Uso:
```bash
# Listar comentários de um post
python3 scripts/instagram/manage_comments.py \
  --action list \
  --media-id 17895695668004550

# Responder a um comentário
python3 scripts/instagram/manage_comments.py \
  --action reply \
  --comment-id 17856342768004550 \
  --text "Obrigado pelo comentário! 😊"

# Ocultar comentário (esconder de outros usuários)
python3 scripts/instagram/manage_comments.py \
  --action hide \
  --comment-id 17856342768004550

# Deletar comentário
python3 scripts/instagram/manage_comments.py \
  --action delete \
  --comment-id 17856342768004550
```

#### Parâmetros:
- `--action`, `-a` (obrigatório): Ação (`list`, `reply`, `hide`, `delete`)
- `--media-id`, `-m` (condicional): ID do post (obrigatório se action=list)
- `--comment-id`, `-c` (condicional): ID do comentário (obrigatório se action=reply/hide/delete)
- `--text`, `-t` (condicional): Texto da resposta (obrigatório se action=reply)

#### Ações disponíveis:

**list** - Listar comentários
- Retorna: username, texto, timestamp, ID do comentário

**reply** - Responder comentário
- Cria uma resposta ao comentário especificado

**hide** - Ocultar comentário
- Esconde comentário ofensivo (apenas você e o autor veem)

**delete** - Deletar comentário
- Remove permanentemente o comentário

---

### 7. manage_dms.py - Gerenciar Direct Messages

⚠️ **Requer permissões adicionais da API:** `instagram_manage_messages`, `pages_manage_metadata`

Gerencia conversas e mensagens diretas no Instagram.

#### Uso:
```bash
# Listar conversas (DMs)
python3 scripts/instagram/manage_dms.py --list --limit 10

# Ler mensagens de uma conversa
python3 scripts/instagram/manage_dms.py --read CONVERSATION_ID --limit 20

# Responder uma mensagem
python3 scripts/instagram/manage_dms.py --reply CONVERSATION_ID --text "Obrigado pela mensagem!"

# Marcar conversa como lida
python3 scripts/instagram/manage_dms.py --mark-read CONVERSATION_ID
```

#### Parâmetros:
- `--list` (ação): Listar conversas
- `--read CONV_ID` (ação): Ler mensagens de uma conversa
- `--reply CONV_ID` (ação): Responder mensagem
- `--mark-read CONV_ID` (ação): Marcar como lida
- `--text`, `-t` (condicional): Texto da resposta (obrigatório se reply)
- `--limit`, `-l` (opcional): Limite de resultados (padrão: 25)

#### Notas:
- Requer permissões adicionais no Facebook App
- Conta Instagram deve estar conectada a uma Página do Facebook
- Só pode responder mensagens iniciadas pelo usuário (limitação da API)

---

## 🎯 Casos de Uso Comuns

### 1. Publicar Post Promocional
```bash
python3 scripts/instagram/publish_post.py \
  --image "produto.jpg" \
  --caption "🔥 Promoção especial! 50% OFF em todos os produtos. Aproveite! #promo #desconto #loja"
```

### 2. Publicar Carrossel de Portfólio
```bash
python3 scripts/instagram/publish_carousel.py \
  --images "trabalho1.jpg,trabalho2.jpg,trabalho3.jpg,trabalho4.jpg" \
  --caption "Meus últimos trabalhos 🎨 Qual você mais gostou? #design #portfolio #arte"
```

### 3. Publicar Reel Viral
```bash
python3 scripts/instagram/publish_reel.py \
  --video "reel_engajamento.mp4" \
  --cover "capa_reel.jpg" \
  --caption "Dica rápida para aumentar suas vendas! 💰 #dicas #empreendedorismo #reels"
```

### 4. Publicar Story Diário
```bash
python3 scripts/instagram/publish_story.py \
  --media "bastidores.jpg" \
  --type image
```

### 5. Analisar Performance dos Posts
```bash
python3 scripts/instagram/get_insights.py \
  --scope recent \
  --limit 10
```

### 6. Moderar Comentários
```bash
# Listar comentários
python3 scripts/instagram/manage_comments.py \
  --action list \
  --media-id 17895695668004550

# Responder comentário positivo
python3 scripts/instagram/manage_comments.py \
  --action reply \
  --comment-id 17856342768004550 \
  --text "Muito obrigado! Fico feliz que tenha gostado! ❤️"

# Ocultar comentário ofensivo
python3 scripts/instagram/manage_comments.py \
  --action hide \
  --comment-id 17856342768004550
```

---

## 🔧 Configuração

### Pré-requisitos:

1. **Instagram Business/Creator Account**
   - Conta comercial ou de criador de conteúdo
   - Vinculada a uma Página do Facebook

2. **Facebook App configurado**
   - App criado no Meta Developers
   - Permissões necessárias configuradas

3. **Access Token com permissões:**
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
   - `instagram_manage_comments` (para manage_comments.py)
   - `instagram_manage_insights` (para get_insights.py)

4. **Python 3.9+**
   ```bash
   python3 --version
   ```

5. **Dependências instaladas**
   ```bash
   pip3 install requests
   ```

### Configurar credenciais:

Edite o arquivo `config/instagram_config.py`:

```python
INSTAGRAM_ACCESS_TOKEN = "seu_token_de_acesso"
INSTAGRAM_ACCOUNT_ID = "seu_instagram_account_id"
```

### Como obter credenciais:

1. Acesse [Meta Developers](https://developers.facebook.com/)
2. Crie um App (se ainda não tiver)
3. Adicione o produto "Instagram"
4. Gere um Access Token com permissões necessárias
5. Obtenha o Instagram Account ID via Graph API Explorer

### Verificar conexão:
```bash
python3 -c "from config.instagram_config import *; print(f'Token: {INSTAGRAM_ACCESS_TOKEN[:20]}...'); print(f'Account ID: {INSTAGRAM_ACCOUNT_ID}')"
```

---

## 📖 Integração com Claude Code

### Para o Agente Claude Code:

Quando o usuário pedir ações Instagram, **SEMPRE use estes templates** ao invés de criar scripts novos.

#### Exemplos de comandos do usuário:

**❌ NÃO fazer:**
```
Usuário: "Publique uma foto no Instagram"
Agente: Cria novo script test_instagram.py → Executa → Descarta
```

**✅ FAZER:**
```
Usuário: "Publique uma foto no Instagram"
Agente: python3 scripts/instagram/publish_post.py --image "foto.jpg" --caption "..."
```

#### Mapeamento de comandos:

| Pedido do usuário | Template a usar |
|-------------------|-----------------|
| "Publicar post/foto" | `publish_post.py` |
| "Publicar carrossel/álbum" | `publish_carousel.py` |
| "Publicar reel/vídeo" | `publish_reel.py` |
| "Publicar story" | `publish_story.py` |
| "Ver métricas/insights/estatísticas" | `get_insights.py` |
| "Gerenciar/responder comentários" | `manage_comments.py` |

---

## 🐛 Troubleshooting

### Erro: "Invalid access token"
```bash
# Verifique se o token está correto e não expirou
# Tokens de usuário expiram em 60 dias
# Considere usar token de longa duração ou refresh automático
```

### Erro: "Instagram account not found"
- Verifique se o `INSTAGRAM_ACCOUNT_ID` está correto
- Certifique-se de que é uma conta Business/Creator
- Verifique se a conta está vinculada a uma Página do Facebook

### Erro: "Media upload failed"
- Verifique se a imagem/vídeo atende aos requisitos de formato e tamanho
- Para URLs, certifique-se de que são acessíveis publicamente
- Vídeos grandes podem demorar mais para processar

### Erro: "Publishing permission denied"
- Verifique se o Access Token tem a permissão `instagram_content_publish`
- Regenere o token se necessário

### Erro: "Carrossel requires 2-10 images"
- Forneça pelo menos 2 imagens
- Máximo de 10 imagens por carrossel

### Erro: "Invalid media type for story"
- Use `--type image` para JPG/PNG
- Use `--type video` para MP4/MOV

---

## 📊 Limites da API

### Rate Limits (Instagram Graph API):
- **Posts:** 50 por dia
- **Stories:** 100 por dia
- **Requisições:** 200 por hora

### Recomendações:
- Espaçar publicações (evitar spam)
- Monitorar uso via Meta Developers Dashboard
- Implementar retry com backoff exponencial se necessário

---

## 📚 Documentação Oficial

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
- [Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [Insights](https://developers.facebook.com/docs/instagram-api/guides/insights)
- [Comment Moderation](https://developers.facebook.com/docs/instagram-api/guides/comment-moderation)

---

## 🔄 Próximas Funcionalidades

- [ ] `get_media.py` - Listar publicações recentes
- [ ] `schedule_post.py` - Agendar publicações
- [ ] `bulk_publish.py` - Publicações em lote
- [ ] `hashtag_search.py` - Buscar posts por hashtag
- [ ] `competitor_analysis.py` - Análise de concorrentes
- [ ] `auto_respond.py` - Respostas automáticas a comentários

---

**Última atualização:** 2025-11-01
**Versão:** 1.0
**Integração:** Instagram Graph API v24.0
