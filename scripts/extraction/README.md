# 🔍 Templates de Extração de Conteúdo

Scripts prontos para extração, transcrição e scraping de conteúdo de múltiplas plataformas.

---

## 📋 Templates Disponíveis

| Template | Função | Plataformas |
|----------|--------|-------------|
| **transcribe_video.py** | Transcreve vídeos | YouTube, TikTok, Instagram, LinkedIn, X/Twitter, Vimeo |
| **extract_instagram.py** | Extrai posts IG | Instagram (posts, carrosséis, perfis) |
| **scrape_website.py** | Scraping de sites | Qualquer site (conversão para Markdown) |
| **scrape_batch.py** | Scraping em batch | Múltiplos sites em sequência |

---

## 🎬 Transcrição de Vídeos

### transcribe_video.py

Transcreve vídeos de múltiplas plataformas usando RapidAPI.

#### Uso Básico

```bash
# YouTube em português
python3 scripts/extraction/transcribe_video.py "https://youtu.be/VIDEO_ID" --lang pt

# TikTok em inglês (padrão)
python3 scripts/extraction/transcribe_video.py "https://tiktok.com/@user/video/123"

# Instagram Reel em espanhol
python3 scripts/extraction/transcribe_video.py "https://instagram.com/reel/ABC/" --lang es

# Traduzir para inglês
python3 scripts/extraction/transcribe_video.py "URL" --task translate
```

#### Plataformas Suportadas

- ✅ YouTube (youtube.com, youtu.be)
- ✅ TikTok (tiktok.com)
- ✅ Instagram (instagram.com/reel, instagram.com/p)
- ✅ LinkedIn (linkedin.com)
- ✅ X/Twitter (x.com, twitter.com)
- ✅ Vimeo (vimeo.com)

#### Idiomas Suportados

| Código | Idioma | Código | Idioma |
|--------|--------|--------|--------|
| `pt` | Português | `en` | Inglês |
| `es` | Espanhol | `fr` | Francês |
| `de` | Alemão | `it` | Italiano |
| `ja` | Japonês | `ko` | Coreano |
| `zh` | Chinês | `ru` | Russo |

#### Saída

Arquivos salvos em: `~/Downloads/transcription_PLATFORM_TIMESTAMP/`

- `transcription.txt` - Transcrição formatada
- `transcription_full.json` - Dados completos da API

---

## 📸 Extração de Posts do Instagram

### extract_instagram.py

Extrai imagens, vídeos e legendas de posts do Instagram via Apify.

#### Uso Básico

```bash
# Extrair um post específico
python3 scripts/extraction/extract_instagram.py "https://www.instagram.com/p/ABC123/"

# Extrair posts de um perfil (últimos 30)
python3 scripts/extraction/extract_instagram.py "natgeo"

# Limitar quantidade de posts
python3 scripts/extraction/extract_instagram.py "natgeo" --limit 10

# Extrair carrossel completo
python3 scripts/extraction/extract_instagram.py "https://www.instagram.com/p/XYZ789/"
```

#### Recursos

- ✅ Extrai imagens em alta qualidade
- ✅ Baixa TODAS as imagens de carrosséis
- ✅ Salva legendas completas
- ✅ Inclui metadados (likes, comentários, autor)
- ✅ Suporta posts individuais e perfis
- ✅ Suporta vídeos (URLs extraídas)

#### Saída

Arquivos salvos em: `~/Downloads/instagram_extract_TIMESTAMP/`

**Por post:**
- `post_01_img_01.jpg` - Primeira imagem
- `post_01_img_02.jpg` - Segunda imagem (se carrossel)
- `post_01_caption.txt` - Legenda e metadados
- `post_01_data.json` - Dados completos

---

## 🌐 Web Scraping de Sites

### scrape_website.py

Extrai conteúdo completo de sites e converte para Markdown via Apify.

#### Uso Básico

```bash
# Scraping básico (ilimitado)
python3 scripts/extraction/scrape_website.py "https://docs.example.com"

# Limitar quantidade de páginas
python3 scripts/extraction/scrape_website.py "https://docs.site.com" --max-pages 50

# Controlar profundidade de crawling
python3 scripts/extraction/scrape_website.py "https://site.com" --max-depth 3

# Combinar limites
python3 scripts/extraction/scrape_website.py "https://site.com" --max-pages 100 --max-depth 5

# Pular preview e executar direto
python3 scripts/extraction/scrape_website.py "https://site.com" --no-preview
```

#### Recursos

- ✅ Preview automático antes de executar
- ✅ Segue links internos automaticamente
- ✅ Converte HTML para Markdown
- ✅ Salva páginas individuais + conteúdo completo
- ✅ Inclui metadata (títulos, URLs, timestamps)
- ✅ Ideal para documentações técnicas

#### Saída

Arquivos salvos em: `~/Downloads/apify_scrape_DOMAIN_TIMESTAMP/`

- `page_001.md`, `page_002.md`, etc - Páginas individuais
- `full_content.md` - Conteúdo completo concatenado
- `metadata.json` - Informações de todas as páginas

#### Casos de Uso

- 📚 Extrair documentações técnicas completas
- 🔍 Fazer backup de sites para análise offline
- 📖 Converter sites para formato legível (Markdown)
- 🤖 Preparar dados para treinamento de LLMs

---

## 🔄 Web Scraping em Batch

### scrape_batch.py

Extrai conteúdo de múltiplos sites em sequência via Apify.

#### Uso Básico

```bash
# Scraping de 2 sites
python3 scripts/extraction/scrape_batch.py 'https://docs.site1.com' 'https://docs.site2.com'

# Scraping de múltiplas documentações
python3 scripts/extraction/scrape_batch.py \
  'https://docs.react.dev' \
  'https://docs.python.org/3' \
  'https://nodejs.org/docs'

# Múltiplas páginas de produtos
python3 scripts/extraction/scrape_batch.py \
  'https://site.com/product1' \
  'https://site.com/product2' \
  'https://site.com/product3'
```

#### Recursos

- ✅ Processa cada URL em sequência
- ✅ Salva cada site em pasta separada
- ✅ Preview automático para cada site
- ✅ Resumo final com estatísticas
- ✅ Tratamento de erros individual
- ✅ Pode ser interrompido (Ctrl+C) sem perder progresso

#### Saída

Cada site é salvo em sua própria pasta:

```
~/Downloads/
├── apify_scrape_react_20250102_120000/
│   ├── page_001.md
│   ├── full_content.md
│   └── metadata.json
├── apify_scrape_python_20250102_120530/
│   ├── page_001.md
│   ├── full_content.md
│   └── metadata.json
└── apify_scrape_nodejs_20250102_121045/
    ├── page_001.md
    ├── full_content.md
    └── metadata.json
```

#### Resumo Final

Ao concluir, o script exibe:

```
📊 RESUMO FINAL
⏱️  Tempo total: 325.4 segundos
📋 URLs processadas: 3/3

✅ Sucessos: 3
   • https://docs.react.dev (127 páginas)
     └─ /Users/user/Downloads/apify_scrape_react_20250102_120000
   • https://docs.python.org/3 (243 páginas)
     └─ /Users/user/Downloads/apify_scrape_python_20250102_120530
   • https://nodejs.org/docs (89 páginas)
     └─ /Users/user/Downloads/apify_scrape_nodejs_20250102_121045
```

---

## ⚙️ Configuração Necessária

### APIs Requeridas

| Template | API Necessária | Config |
|----------|----------------|--------|
| transcribe_video.py | RapidAPI (Speech-to-Text AI) | Hardcoded em `tools/transcribe_universal.py` |
| extract_instagram.py | Apify | Hardcoded em `tools/extract_instagram.py` |
| scrape_website.py | Apify | `config/apify_config.py` |
| scrape_batch.py | Apify | `config/apify_config.py` |

### Verificar Configurações

```bash
# Verificar config Apify
cat config/apify_config.py

# Verificar API RapidAPI
grep "RAPIDAPI_KEY" tools/transcribe_universal.py
```

---

## 📊 Performance e Custos

| Template | Tempo Médio | Custo Estimado | Notas |
|----------|-------------|----------------|-------|
| **transcribe_video.py** | 1-5 min | ~$0.02/vídeo | Depende da duração do vídeo |
| **extract_instagram.py** | 30-60s | ~$0.05/30 posts | Tempo de Apify |
| **scrape_website.py** | 1-10 min | ~$0.10-0.50/site | Depende do tamanho |
| **scrape_batch.py** | 5-30 min | ~$0.50-2.00/batch | Múltiplos sites |

**Nota:** Custos são estimativas baseadas em uso médio das APIs.

---

## 🚨 Troubleshooting

### Erro: "Não foi possível importar X"

```bash
# Verificar se arquivo existe
ls -la tools/transcribe_universal.py
ls -la tools/extract_instagram.py
ls -la tools/apify_scraper.py

# Verificar dependências
pip3 install --user requests apify-client
```

### Erro 401 - API Key Inválida

```bash
# Apify
vim config/apify_config.py

# RapidAPI
vim tools/transcribe_universal.py
# Procurar por RAPIDAPI_KEY e atualizar
```

### Timeout em Transcrição

Vídeos muito longos podem dar timeout. Soluções:

1. Usar vídeos menores (< 10 min)
2. Baixar o vídeo e enviar direto (não implementado ainda)

### Instagram não retorna posts

1. Verificar se URL está correta
2. Verificar se perfil é público
3. Aumentar timeout em `tools/extract_instagram.py`

### Scraping retorna poucas páginas

1. Aumentar `--max-pages` e `--max-depth`
2. Site pode ter bloqueio anti-bot
3. Verificar se links internos estão corretos

---

## 💡 Casos de Uso Reais

### 1. Análise de Concorrentes (Instagram)

```bash
# Extrair últimos 50 posts de 3 concorrentes
python3 scripts/extraction/extract_instagram.py "concorrente1" --limit 50
python3 scripts/extraction/extract_instagram.py "concorrente2" --limit 50
python3 scripts/extraction/extract_instagram.py "concorrente3" --limit 50

# Analisar padrões de conteúdo, hashtags, engajamento
```

### 2. Transcrever Webinars para Blog

```bash
# Transcrever webinar do YouTube
python3 scripts/extraction/transcribe_video.py "https://youtu.be/WEBINAR_ID" --lang pt

# Usar transcrição como base para artigo de blog
```

### 3. Backup de Documentação

```bash
# Fazer backup de múltiplas docs técnicas
python3 scripts/extraction/scrape_batch.py \
  'https://docs.nossa-api.com' \
  'https://docs.nossa-plataforma.com' \
  'https://wiki.interna.com'
```

### 4. Análise de Tendências (TikTok)

```bash
# Transcrever vídeos virais para análise
python3 scripts/extraction/transcribe_video.py "https://tiktok.com/@user/video/123" --lang pt
python3 scripts/extraction/transcribe_video.py "https://tiktok.com/@user/video/456" --lang pt

# Analisar padrões de linguagem, hooks, CTAs
```

---

## 🔗 Recursos Relacionados

- **Ferramentas originais:** `tools/`
  - `transcribe_universal.py` (transcrição)
  - `extract_instagram.py` (Instagram)
  - `apify_scraper.py` (web scraping)
  - `apify_scraper_batch.py` (batch scraping)

- **Documentação:**
  - `docs/tools/transcribe_universal.md` (transcrição)
  - `docs/tools/extract_instagram.md` (Instagram - se existir)
  - `docs/tools/apify_scraper.md` (scraping - se existir)

- **Configurações:**
  - `config/apify_config.py` (Apify API)

---

## 📞 Suporte

**Problemas com templates?**
1. Verificar logs de erro
2. Confirmar API keys configuradas
3. Testar ferramenta original em `tools/`
4. Reportar issue com detalhes

---

**Última atualização:** 2025-11-02
**Total de templates:** 4 (todos testados e funcionais)
