# 🎵 Scripts TikTok - Templates Prontos

**5 templates testados para uso rápido da TikTok API23**

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Templates Disponíveis](#templates-disponíveis)
- [Exemplos de Uso](#exemplos-de-uso)
- [Boas Práticas](#boas-práticas)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Scripts wrappers otimizados para TikTok API23. Cada template é independente e pronto para uso.

### Características:
- ✅ **Prontos para executar** (zero configuração)
- ✅ **Formatação amigável** (output legível)
- ✅ **Tratamento de erros** robusto
- ✅ **Argumentos flexíveis** (help integrado)

### O que você pode fazer:
- 👤 Analisar perfis e usuários
- 🎬 Obter detalhes de vídeos
- 🔍 Buscar conteúdo (vídeos/usuários)
- 📈 Monitorar trending
- #️⃣ Analisar hashtags

---

## 📦 Templates Disponíveis

### 1. `get_user_info.py` - Info de Usuário

**Funcionalidade:** Obter informações completas de um perfil.

**Uso básico:**
```bash
python3 scripts/tiktok/get_user_info.py --username taylorswift
```

**Com posts populares:**
```bash
python3 scripts/tiktok/get_user_info.py --username taylorswift --posts 10
```

**Output completo (JSON):**
```bash
python3 scripts/tiktok/get_user_info.py --username tiktok --full
```

**Output:**
```
🔍 Buscando info do usuário @taylorswift...

👤 Nome: Taylor Swift
🔗 Username: @taylorswift
📝 Bio: Official TikTok

📊 Estatísticas:
  👥 Seguidores: 1,234,567
  👤 Seguindo: 123
  🎬 Vídeos: 89
  ❤️  Likes: 5,678,901

📹 Buscando 10 posts populares...
🎬 Top 10 posts:
  1. New album out now! (123,456 likes)
  2. Behind the scenes... (98,765 likes)
  ...
```

---

### 2. `get_video_info.py` - Info de Vídeo

**Funcionalidade:** Obter detalhes de um vídeo específico.

**Uso básico:**
```bash
python3 scripts/tiktok/get_video_info.py --video-id 7306132438047116586
```

**Com comentários:**
```bash
python3 scripts/tiktok/get_video_info.py --video-id 7306132438047116586 --comments 50
```

**Output:**
```
🎬 Buscando info do vídeo 7306132438047116586...

👤 Autor: Taylor Swift (@taylorswift)
📝 Descrição: Check out my new song!
🎵 Música: Song Title - Artist Name

📊 Estatísticas:
  👁️  Views: 1,234,567
  ❤️  Likes: 123,456
  💬 Comentários: 5,678
  🔄 Shares: 9,012

💬 Buscando 50 comentários...
📝 Top 50 comentários:
  1. User1: Amazing! (1,234 likes)
  2. User2: Love it! (987 likes)
  ...
```

---

### 3. `search_content.py` - Buscar Conteúdo

**Funcionalidade:** Buscar vídeos, usuários ou conteúdo geral.

**Buscar vídeos:**
```bash
python3 scripts/tiktok/search_content.py --keyword "cat" --type video
```

**Buscar usuários:**
```bash
python3 scripts/tiktok/search_content.py --keyword "taylor" --type account
```

**Busca geral:**
```bash
python3 scripts/tiktok/search_content.py --keyword "dance" --type general
```

**Com limite personalizado:**
```bash
python3 scripts/tiktok/search_content.py --keyword "cat" --type video --limit 50
```

**Output (vídeos):**
```
🔍 Buscando 'cat' (tipo: video)...

🎬 Encontrados 20 vídeos:

1. CatLover: Funny cat compilation...
   ❤️  123,456 likes

2. PetVideos: Cute kittens playing...
   ❤️  98,765 likes
...

💡 Sugestões relacionadas:
  - cat videos
  - cat funny
  - cat cute
  - cat compilation
  - cat memes
```

---

### 4. `get_trending.py` - Monitorar Trending

**Funcionalidade:** Obter conteúdo em alta (vídeos, hashtags, músicas, criadores, keywords).

**Vídeos em trending:**
```bash
python3 scripts/tiktok/get_trending.py --type videos
```

**Hashtags em alta (Brasil, últimas 24h):**
```bash
python3 scripts/tiktok/get_trending.py --type hashtags --country BR --period 1
```

**Músicas em alta:**
```bash
python3 scripts/tiktok/get_trending.py --type songs --country US --period 7
```

**Criadores em alta:**
```bash
python3 scripts/tiktok/get_trending.py --type creators --country BR
```

**Keywords em alta:**
```bash
python3 scripts/tiktok/get_trending.py --type keywords
```

**Output (hashtags):**
```
📈 Buscando hashtags em trending (BR)...

#️⃣ Top 20 hashtags em trending:

1. #fyp
   👁️  1,234,567,890 views

2. #viral
   👁️  987,654,321 views

3. #brasil
   👁️  567,890,123 views
...
```

---

### 5. `analyze_hashtag.py` - Analisar Hashtag

**Funcionalidade:** Analisar hashtag completa (info + posts + engajamento médio).

**Uso básico:**
```bash
python3 scripts/tiktok/analyze_hashtag.py --hashtag cat
```

**Com mais posts:**
```bash
python3 scripts/tiktok/analyze_hashtag.py --hashtag fyp --posts 50
```

**Output:**
```
#️⃣ Analisando hashtag #cat...

📝 Nome: #cat
📄 Descrição: All things cats!

📊 Estatísticas:
  👁️  Views: 123,456,789,012
  🎬 Posts: 5,678,901

🎬 Buscando top 20 posts da hashtag...

📹 Encontrados 20 posts:

1. CatLover: Funny cat moments...
   ❤️  12,345 | 💬 678 | 🔄 901

2. PetVideos: Kitten compilation...
   ❤️  10,987 | 💬 543 | 🔄 789
...

==================================================

📈 Média de engajamento por post:
  ❤️  Likes: 8,567
  💬 Comentários: 432
  🔄 Shares: 678
```

---

## 💡 Exemplos de Uso

### Caso 1: Analisar Concorrente

```bash
# 1. Info do perfil + 20 posts populares
python3 scripts/tiktok/get_user_info.py --username competitor --posts 20

# 2. Analisar hashtag mais usada
python3 scripts/tiktok/analyze_hashtag.py --hashtag viralhashtag --posts 30
```

---

### Caso 2: Pesquisa de Mercado

```bash
# 1. Buscar vídeos sobre produto
python3 scripts/tiktok/search_content.py --keyword "iphone 15" --type video --limit 50

# 2. Ver trending de produtos (últimos 7 dias)
python3 scripts/tiktok/get_trending.py --type keywords --period 7
```

---

### Caso 3: Monitorar Tendências

```bash
# 1. Vídeos em trending
python3 scripts/tiktok/get_trending.py --type videos --limit 30

# 2. Hashtags em alta (últimas 24h)
python3 scripts/tiktok/get_trending.py --type hashtags --period 1 --country BR

# 3. Músicas em alta
python3 scripts/tiktok/get_trending.py --type songs --period 7
```

---

### Caso 4: Análise de Vídeo Viral

```bash
# 1. Detalhes do vídeo + 100 comentários
python3 scripts/tiktok/get_video_info.py --video-id VIDEO_ID --comments 100

# 2. Analisar hashtag usada
python3 scripts/tiktok/analyze_hashtag.py --hashtag viral
```

---

## 🎯 Boas Práticas

### 1. Salvar resultados em arquivo

```bash
# Salvar JSON completo
python3 scripts/tiktok/get_user_info.py --username taylorswift --full > user.json

# Salvar output formatado
python3 scripts/tiktok/analyze_hashtag.py --hashtag cat > hashtag_analysis.txt
```

---

### 2. Loop para análise em massa

```bash
# Analisar múltiplos usuários
for user in user1 user2 user3; do
  python3 scripts/tiktok/get_user_info.py --username $user >> users.txt
done
```

---

### 3. Combinar com outras ferramentas

```bash
# Buscar vídeos e extrair IDs (usando jq)
python3 scripts/tiktok/search_content.py --keyword "cat" --full | jq '.data[].id'

# Analisar hashtag e contar posts
python3 scripts/tiktok/analyze_hashtag.py --hashtag fyp --full | jq '.challengeInfo.stats.videoCount'
```

---

## 🔧 Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'tools'`

**Causa:** Path incorreto.

**Solução:**
```bash
# Execute sempre do diretório raiz do workspace
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
python3 scripts/tiktok/get_user_info.py --username taylorswift
```

---

### Erro: `401 Unauthorized`

**Causa:** API key inválida.

**Solução:**
Verificar `config/tiktok_config.py` e renovar key se necessário.

---

### Erro: `User not found`

**Causa:** Username incorreto ou perfil deletado.

**Solução:**
- Verificar se username está correto (sem @)
- Testar com outro usuário conhecido (ex: `tiktok`)

---

### Erro: `Video not found`

**Causa:** Vídeo deletado ou ID incorreto.

**Solução:**
- Verificar se video_id está completo
- Testar com outro vídeo conhecido

---

### Output vazio

**Causa:** Perfil privado ou sem conteúdo público.

**Solução:**
- Verificar se perfil é público
- Alguns endpoints (liked_posts) só funcionam em perfis públicos

---

## 📊 Argumentos Comuns

Todos os scripts aceitam `--help` para ver argumentos disponíveis:

```bash
python3 scripts/tiktok/get_user_info.py --help
python3 scripts/tiktok/get_video_info.py --help
python3 scripts/tiktok/search_content.py --help
python3 scripts/tiktok/get_trending.py --help
python3 scripts/tiktok/analyze_hashtag.py --help
```

### Argumentos frequentes:

| Argumento | Descrição | Exemplo |
|-----------|-----------|---------|
| `--full` | Mostrar JSON completo | `--full` |
| `--username` | Username do TikTok (sem @) | `--username taylorswift` |
| `--video-id` | ID do vídeo | `--video-id 7306132438047116586` |
| `--keyword` | Termo de busca | `--keyword "cat"` |
| `--hashtag` | Nome da hashtag (sem #) | `--hashtag fyp` |
| `--type` | Tipo de busca/trending | `--type video` |
| `--country` | Código do país | `--country BR` |
| `--period` | Período (dias ou horas) | `--period 7` |
| `--limit` | Limite de resultados | `--limit 50` |
| `--posts` | Número de posts | `--posts 20` |
| `--comments` | Número de comentários | `--comments 100` |

---

## 📞 Suporte

**Ferramenta base:** `tools/tiktok_api23.py`
**Config:** `config/tiktok_config.py`
**Docs completa:** `docs/tools/tiktok_api23.md`
**Templates:** `scripts/tiktok/`

---

**Última atualização:** 2025-11-02
**Total de templates:** 5 (testados e funcionais)
