# 🔍 Scripts de Busca (xAI Search)

Templates prontos para busca em tempo real usando **xAI Grok** com Live Search.

## 📋 Índice

- [Templates Disponíveis](#-templates-disponíveis)
- [Configuração](#-configuração)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Parâmetros Comuns](#-parâmetros-comuns)
- [Casos de Uso](#-casos-de-uso)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Templates Disponíveis

| Template | Descrição | Fontes |
|----------|-----------|--------|
| **xai_web.py** | Busca web geral | Web (exclui redes sociais) |
| **xai_twitter.py** | Busca no Twitter/X | Twitter/X (posts em tempo real) |
| **xai_news.py** | Busca em notícias | Fontes de notícias + Web |

---

## ⚙️ Configuração

### Requisitos

1. **Python 3.11+** (obrigatório para xAI SDK)
2. **xAI API Key** configurada em `config/xai_config.py`
3. **xAI SDK instalado:**
   ```bash
   python3.11 -m pip install xai-sdk --user
   ```

### Verificar Instalação

```bash
# Verificar Python 3.11
python3.11 --version

# Testar importação do SDK
python3.11 -c "from xai_sdk import Client; print('✅ xAI SDK instalado')"
```

---

## 🚀 Exemplos de Uso

### 1. Busca Web (`xai_web.py`)

Ideal para pesquisas técnicas, documentação, tutoriais.

```bash
# Busca básica
python3.11 scripts/search/xai_web.py "melhores práticas Python 2025"

# Com mais resultados
python3.11 scripts/search/xai_web.py "tutoriais React hooks" --max-results 10

# Usando modelo mais poderoso
python3.11 scripts/search/xai_web.py "arquitetura microserviços" --model grok-4

# Sem exibir URLs das fontes
python3.11 scripts/search/xai_web.py "documentação Node.js" --no-citations
```

**Quando usar:**
- ✅ Documentação técnica
- ✅ Tutoriais e guias
- ✅ Pesquisas acadêmicas
- ✅ Artigos e blogs

---

### 2. Busca Twitter/X (`xai_twitter.py`)

Ideal para monitorar tendências, opiniões públicas, breaking news.

```bash
# Busca básica
python3.11 scripts/search/xai_twitter.py "opinião sobre IA"

# Posts das últimas 24h
python3.11 scripts/search/xai_twitter.py "breaking news tech" --recent

# Filtrar por handles específicos (max 10)
python3.11 scripts/search/xai_twitter.py "AI updates" --handles elonmusk,gdb,sama

# Excluir handles
python3.11 scripts/search/xai_twitter.py "python tips" --exclude-handles spambot1,spambot2

# Posts virais (min. curtidas e visualizações)
python3.11 scripts/search/xai_twitter.py "viral memes" --min-likes 1000 --min-views 10000

# Combinando filtros
python3.11 scripts/search/xai_twitter.py "AI art" --recent --min-likes 500 --handles midjourney,runwayml
```

**Quando usar:**
- ✅ Monitorar trending topics
- ✅ Análise de sentimento público
- ✅ Acompanhar influenciadores
- ✅ Breaking news em tempo real
- ✅ Pesquisa de mercado (opinião sobre produtos)

---

### 3. Busca Notícias (`xai_news.py`)

Ideal para acompanhar cobertura jornalística, análises profissionais.

```bash
# Busca básica
python3.11 scripts/search/xai_news.py "inteligência artificial"

# Notícias das últimas 24h
python3.11 scripts/search/xai_news.py "eleições Brasil" --24h

# Notícias da última semana
python3.11 scripts/search/xai_news.py "mercado financeiro" --last-week

# Apenas fontes de notícias (sem web geral)
python3.11 scripts/search/xai_news.py "política internacional" --news-only

# Com mais fontes
python3.11 scripts/search/xai_news.py "tecnologia startups" --max-results 10
```

**Quando usar:**
- ✅ Cobertura jornalística profissional
- ✅ Análises de especialistas
- ✅ Breaking news verificadas
- ✅ Pesquisa sobre eventos recentes
- ✅ Comparação de fontes confiáveis

---

## 🎛️ Parâmetros Comuns

### Todos os Templates

| Parâmetro | Descrição | Padrão | Exemplo |
|-----------|-----------|--------|---------|
| `--max-results N` | Número máximo de fontes | 5 | `--max-results 10` |
| `--model` | Modelo xAI | `grok-4-fast` | `--model grok-4` |
| `--no-citations` | Não mostrar URLs | Mostrar | `--no-citations` |

### xai_twitter.py (Específicos)

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `--recent` | Apenas últimas 24h | `--recent` |
| `--handles` | Incluir handles (max 10) | `--handles elonmusk,gdb` |
| `--exclude-handles` | Excluir handles (max 10) | `--exclude-handles spambot` |
| `--min-likes N` | Mínimo de curtidas | `--min-likes 1000` |
| `--min-views N` | Mínimo de visualizações | `--min-views 10000` |

### xai_news.py (Específicos)

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `--24h` | Apenas últimas 24h | `--24h` |
| `--last-week` | Apenas última semana | `--last-week` |
| `--news-only` | Apenas fontes de notícias | `--news-only` |

---

## 💡 Casos de Uso

### 1. Pesquisa de Mercado

```bash
# Opinião pública sobre produto
python3.11 scripts/search/xai_twitter.py "opinião sobre iPhone 16" --recent --min-likes 100

# Notícias sobre concorrentes
python3.11 scripts/search/xai_news.py "lançamento Samsung Galaxy" --24h

# Análise técnica
python3.11 scripts/search/xai_web.py "review iPhone 16 vs Samsung S24" --max-results 10
```

### 2. Monitoramento de Tendências

```bash
# Trending topics tech
python3.11 scripts/search/xai_twitter.py "AI trends 2025" --recent --min-views 10000

# Notícias mais recentes
python3.11 scripts/search/xai_news.py "breaking news technology" --24h

# Análise profunda
python3.11 scripts/search/xai_web.py "future of AI" --model grok-4
```

### 3. Pesquisa Técnica

```bash
# Documentação
python3.11 scripts/search/xai_web.py "React 19 new features documentation"

# Community insights
python3.11 scripts/search/xai_twitter.py "React 19 developer experience" --handles dan_abramov,reactjs

# Tutoriais recentes
python3.11 scripts/search/xai_web.py "React 19 migration guide 2025" --max-results 10
```

### 4. Análise de Crise/Reputação

```bash
# Sentimento público
python3.11 scripts/search/xai_twitter.py "problema com [marca]" --recent --min-likes 50

# Cobertura jornalística
python3.11 scripts/search/xai_news.py "crise [empresa]" --24h --news-only

# Análise completa
python3.11 scripts/search/xai_web.py "análise crise [empresa]" --max-results 10
```

### 5. Competitive Intelligence

```bash
# Monitorar concorrente no Twitter
python3.11 scripts/search/xai_twitter.py "lançamento produto" --handles empresa_rival

# Notícias sobre setor
python3.11 scripts/search/xai_news.py "mercado SaaS Brasil" --last-week

# Análise de mercado
python3.11 scripts/search/xai_web.py "market share SaaS 2025" --model grok-4
```

---

## ⚡ Performance

| Template | Latência Média | Fontes Consultadas | Custo Estimado |
|----------|----------------|---------------------|----------------|
| **xai_web.py** | ~2-3s | 5 (padrão) | ~$0.125/busca |
| **xai_twitter.py** | ~2-4s | 5 (padrão) | ~$0.125/busca |
| **xai_news.py** | ~2-3s | 5 (padrão) | ~$0.125/busca |

**Modelos disponíveis:**
- `grok-4-fast`: Mais rápido, menor custo (padrão)
- `grok-4`: Mais preciso, maior contexto

---

## 🔧 Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'xai_sdk'`

```bash
# Instalar SDK no Python 3.11
python3.11 -m pip install xai-sdk --user
```

### Erro: `API Key inválida`

Verificar `config/xai_config.py`:
```python
XAI_API_KEY = "sua-key-aqui"
```

### Erro: `Python version not supported`

Templates requerem Python 3.11+:
```bash
# Verificar versão
python3.11 --version

# Se não tiver instalado (macOS)
brew install python@3.11
```

### Busca não retorna resultados

1. Verificar conexão com internet
2. Testar com query mais simples
3. Aumentar `--max-results`
4. Tentar modelo `--model grok-4`

### Timeout ou lentidão

1. Reduzir `--max-results`
2. Usar `grok-4-fast` (padrão)
3. Simplificar query
4. Verificar uso da API (rate limits)

---

## 📚 Documentação Relacionada

- **Ferramenta base:** `tools/xai_search.py`
- **Exemplos avançados:** `tools/xai_search_examples.py`
- **Configuração:** `config/xai_config.py`
- **Docs completa:** `docs/tools/xai_search.md`

---

## 🤖 Integração com Claude Code

**Claude Code reconhece automaticamente quando usar cada template:**

```
Usuário: "Busca notícias sobre IA das últimas 24h"
Claude: [executa python3.11 scripts/search/xai_news.py "IA" --24h]

Usuário: "O que estão falando no Twitter sobre Python?"
Claude: [executa python3.11 scripts/search/xai_twitter.py "Python" --recent]

Usuário: "Pesquisa tutoriais de React hooks"
Claude: [executa python3.11 scripts/search/xai_web.py "tutoriais React hooks"]
```

---

## 📝 Notas Importantes

1. **Python 3.11+ obrigatório** - xAI SDK não funciona em versões anteriores
2. **Rate limits** - Verifique limites da API xAI
3. **Custo** - ~$0.125 por busca (varia por modelo e fontes)
4. **Citações** - URLs fornecidas como referência, verificar confiabilidade
5. **Tempo real** - Dados atualizados, mas resultados podem variar

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
**Status:** ✅ Todos templates testados e funcionais
