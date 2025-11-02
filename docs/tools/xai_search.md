# 🔍 xAI Live Search (Grok)

Busca em tempo real na Web, Twitter/X e News usando Grok.

## 🚀 Comando

```bash
# Script direto
./xai-search.sh "sua pergunta"

# Python
python3.11 tools/xai_search.py "sua pergunta"

# Menu interativo (8 exemplos)
python3.11 tools/xai_search_examples.py
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `pergunta` | ✅ | Pergunta ou termo de busca |

## 💡 Exemplos

```bash
# Notícias
./xai-search.sh "últimas notícias sobre IA"

# Tendências
./xai-search.sh "o que está em alta no Twitter hoje"

# Pesquisa de mercado
./xai-search.sh "startups de IA no Brasil 2025"

# Informação específica
./xai-search.sh "como funciona o Grok da xAI"
```

## ⚙️ Recursos

- **Fontes:** Web + Twitter/X + News
- **Modelo:** Grok-4-fast
- **Limite:** Máximo 5 fontes por busca
- **Custo:** ~$0.125 por busca
- **Citações:** Retorna fontes com links

## 📦 Saída

- Resposta formatada no terminal
- Links das fontes citadas
- Dados em tempo real

## 🔧 Config

API Key configurada em `tools/xai_search.py`

## 📖 Docs

- `XAI_QUICK_START.md`
- `tools/XAI_SEARCH_README.md`
