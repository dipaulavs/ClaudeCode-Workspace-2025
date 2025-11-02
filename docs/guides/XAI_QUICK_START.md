# 🚀 xAI Live Search - Início Rápido

## ⚡ Uso Imediato

### Método 1: Script de Atalho (Mais Fácil)

```bash
./xai-search.sh "Sua pergunta aqui"
```

**Exemplos:**
```bash
./xai-search.sh "Últimas notícias sobre IA"
./xai-search.sh "O que as pessoas estão dizendo sobre xAI no Twitter?"
./xai-search.sh "Tendências de tecnologia em 2025"
```

### Método 2: Script Python Direto

```bash
python3.11 tools/xai_search.py "Sua pergunta aqui"
```

### Método 3: Exemplos Interativos

```bash
python3.11 tools/xai_search_examples.py
```

Este comando abre um menu interativo com 8 exemplos diferentes de uso.

## 📊 Configurações Atuais

✅ **Instalado e configurado com:**
- Modelo: **grok-4-fast** (rápido e eficiente)
- Máximo de fontes: **5** (limite de custo)
- Fontes habilitadas: **Web + Twitter/X**
- Citações: **Ativadas** (você verá as URLs das fontes)

## 💡 Casos de Uso Comuns

### 1. Notícias em Tempo Real
```bash
./xai-search.sh "Últimas notícias sobre [TEMA]"
```

### 2. Tendências no Twitter/X
```bash
./xai-search.sh "O que as pessoas estão falando sobre [TEMA]?"
```

### 3. Pesquisa de Mercado
```bash
./xai-search.sh "Análise do mercado de [SETOR] em 2025"
```

### 4. Monitoramento de Marca
```bash
./xai-search.sh "Menções sobre [MARCA] nas redes sociais"
```

### 5. Informações Técnicas
```bash
./xai-search.sh "Melhores práticas de [TECNOLOGIA] em 2025"
```

## 🔧 Customização Rápida

Para alterar as configurações padrão, edite: `config/xai_config.py`

```python
# Aumentar número de fontes
DEFAULT_MAX_SEARCH_RESULTS = 10

# Trocar modelo (se disponível)
DEFAULT_MODEL = "grok-4"  # ou outro modelo

# Forçar busca sempre ativa
DEFAULT_SEARCH_MODE = "on"  # "auto", "on", "off"
```

## 💰 Custos

- **$0.025 por fonte usada**
- Com 5 fontes: **~$0.125 por busca**
- Com 10 fontes: **~$0.25 por busca**

O número real de fontes usadas aparece no final de cada busca.

## 🆘 Problemas Comuns

### Erro: "command not found"
**Solução**: Use o caminho completo do Python:
```bash
/opt/homebrew/bin/python3.11 tools/xai_search.py "pergunta"
```

### Erro: "Module xai_sdk not found"
**Solução**: Instale o SDK:
```bash
/opt/homebrew/bin/python3.11 -m pip install xai-sdk
```

### Não retorna citações
**Resposta**: Isso é normal quando o modelo usa conhecimento interno ao invés de buscar. Tente perguntas que exijam informações recentes ou específicas.

## 📚 Documentação Completa

Para uso avançado, consulte: `tools/XAI_SEARCH_README.md`

## 🎯 Exemplos Testados

**Busca básica**:
```bash
./xai-search.sh "O que é o modelo Grok da xAI?"
```

**Busca em tempo real**:
```bash
./xai-search.sh "Quais são as últimas notícias sobre inteligência artificial hoje?"
```

---

**Pronto para usar!** 🎉

Para mais exemplos, execute: `python3.11 tools/xai_search_examples.py`
