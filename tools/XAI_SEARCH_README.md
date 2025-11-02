# 🔍 xAI Live Search - Guia de Uso

Ferramenta de busca na web e Twitter/X usando a API xAI com o modelo Grok.

## 📋 Configurações Padrão

- **Modelo**: grok-4-fast
- **Máximo de fontes**: 5
- **Fontes**: Web e Twitter/X
- **Citações**: Habilitadas por padrão

## 🚀 Instalação

O xAI SDK já foi instalado com Python 3.11. Para usar, certifique-se de que está usando Python 3.11:

```bash
/opt/homebrew/bin/python3.11 -m pip install xai-sdk
```

## 📁 Arquivos

- `config/xai_config.py` - Configurações e API key
- `tools/xai_search.py` - Script principal de busca
- `tools/xai_search_examples.py` - Exemplos de uso

## 🎯 Uso Básico

### Linha de Comando

```bash
# Busca simples
python3.11 tools/xai_search.py 'Quais são as últimas notícias sobre IA?'

# Busca com citações
python3.11 tools/xai_search.py 'O que as pessoas estão falando sobre xAI no Twitter?'
```

### Uso Programático

```python
from tools.xai_search import XAISearch

# Criar instância
searcher = XAISearch()

# Busca básica
result = searcher.search("Sua pergunta aqui")
print(result['content'])
print(result['citations'])
```

## 📚 Exemplos Avançados

Execute o script de exemplos interativo:

```bash
python3.11 tools/xai_search_examples.py
```

### Exemplos disponíveis:

1. **Busca básica** - Web e Twitter/X
2. **Busca apenas na web**
3. **Busca apenas no Twitter/X**
4. **Busca com handles específicos**
5. **Busca com filtro de período**
6. **Busca customizada** (mais resultados)
7. **Posts populares** (filtro por curtidas/views)
8. **Busca em notícias**

## 🔧 Configurações Customizadas

### Alterar número de resultados

```python
searcher = XAISearch(max_results=10)
result = searcher.search("Sua pergunta")
```

### Buscar apenas na web

```python
result = searcher.search_web_only("Melhores práticas de Python 2025")
```

### Buscar apenas no Twitter/X

```python
result = searcher.search_x_only("Últimas tendências em tecnologia")
```

### Buscar em handles específicos

```python
result = searcher.search_with_handles(
    "Últimas atualizações",
    included_handles=["xai", "elonmusk"]
)
```

### Buscar com filtro de data

```python
from datetime import datetime

result = searcher.search(
    "Eventos de tecnologia",
    from_date=datetime(2025, 10, 1),
    to_date=datetime(2025, 10, 31)
)
```

### Buscar posts populares

```python
from xai_sdk.search import x_source

x_src = x_source(
    post_favorite_count=1000,  # Mínimo 1000 curtidas
    post_view_count=10000      # Mínimo 10000 visualizações
)

result = searcher.search("Memes virais", sources=[x_src])
```

## 🎛️ Parâmetros Disponíveis

### SearchParameters

- `mode`: "auto", "on", "off" (padrão: "auto")
- `max_search_results`: Número máximo de fontes (padrão: 5)
- `return_citations`: Retornar citações (padrão: True)
- `from_date`: Data inicial (ISO8601)
- `to_date`: Data final (ISO8601)

### Web Source

```python
from xai_sdk.search import web_source

web_source(
    country="BR",  # Código ISO do país
    excluded_websites=["site1.com", "site2.com"],  # Máx 5
    allowed_websites=["site3.com"],  # Máx 5
    safe_search=True
)
```

### X/Twitter Source

```python
from xai_sdk.search import x_source

x_source(
    included_x_handles=["handle1", "handle2"],  # Máx 10
    excluded_x_handles=["handle3"],  # Máx 10
    post_favorite_count=100,  # Mínimo de curtidas
    post_view_count=1000  # Mínimo de visualizações
)
```

### News Source

```python
from xai_sdk.search import news_source

news_source(
    country="BR",
    excluded_websites=["site.com"],
    safe_search=True
)
```

## 💰 Preços

- **Live Search**: $25 por 1.000 fontes usadas ($0.025 por fonte)
- O número de fontes usadas está em `response.usage.num_sources_used`

## 🔐 Segurança

A API key está armazenada em `config/xai_config.py`. Para produção, considere usar variáveis de ambiente:

```python
import os
XAI_API_KEY = os.getenv("XAI_API_KEY")
```

## 📊 Estrutura de Resposta

```python
{
    'content': 'Resposta do modelo...',
    'citations': ['url1', 'url2', ...],
    'num_sources_used': 3
}
```

## ⚠️ Limitações

- **Web/News**: Máximo 5 websites para incluir/excluir
- **X/Twitter**: Máximo 10 handles para incluir/excluir
- **RSS**: Apenas 1 link RSS por vez
- **Handles excluídos por padrão**: "grok" (para evitar auto-citação)

## 🆘 Troubleshooting

### Erro: Python version

O xAI SDK requer Python >= 3.10. Use Python 3.11:

```bash
/opt/homebrew/bin/python3.11 tools/xai_search.py "sua busca"
```

### Erro: Module not found

Certifique-se de que o xAI SDK está instalado:

```bash
/opt/homebrew/bin/python3.11 -m pip install xai-sdk
```

### Erro: API Key inválida

Verifique se a API key em `config/xai_config.py` está correta.

## 📝 Exemplos Práticos

### Pesquisa de mercado

```python
searcher = XAISearch(max_results=10)
result = searcher.search("Tendências do mercado de e-commerce no Brasil 2025")
```

### Monitoramento de marca

```python
result = searcher.search_with_handles(
    "O que estão falando sobre nossa marca?",
    excluded_handles=["competidor1", "competidor2"]
)
```

### Análise de sentimento

```python
result = searcher.search_x_only("Reações ao novo produto da empresa X")
```

### Notícias recentes

```python
from xai_sdk.search import news_source
result = searcher.search(
    "Últimas notícias sobre inteligência artificial",
    sources=[news_source(country="BR")]
)
```

## 🔗 Recursos Adicionais

- [Documentação oficial xAI](https://docs.x.ai/)
- [API Reference](https://docs.x.ai/api)
- [xAI SDK no GitHub](https://github.com/xai-org/xai-sdk)

---

**Última atualização**: Outubro 2025
**Versão**: 1.0.0
