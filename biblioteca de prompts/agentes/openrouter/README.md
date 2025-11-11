# 🤖 Sistema de Agentes via OpenRouter

Sistema de subagentes especializados que economiza tokens do Claude Code. As instruções dos agentes ficam armazenadas localmente e só são enviadas para a API da OpenRouter quando necessário.

## 🎯 Conceito

- **Zero tokens no Claude Code**: Instruções não são carregadas aqui
- **Agentes especializados**: Cada agente tem expertise específica
- **Flexibilidade**: Use qualquer modelo da OpenRouter
- **Escalável**: Adicione quantos agentes quiser

## 📁 Estrutura

```
agentes/openrouter/
├── config.json              # API Key e configurações
├── README.md               # Esta documentação
├── copywriter-vendas.md    # Agente: Copy de vendas
└── analista-negocios.md    # Agente: Análise de negócios
```

## 🚀 Como Usar

### Uso Básico

```bash
python3 tools/agent_openrouter.py <agente> "<seu input>"
```

**Exemplo:**
```bash
python3 tools/agent_openrouter.py copywriter-vendas "Crie um título para curso de Python"
```

### Listar Agentes Disponíveis

```bash
python3 tools/agent_openrouter.py --list
```

### Escolher Modelo Específico

```bash
python3 tools/agent_openrouter.py copywriter-vendas "Seu prompt" --model openai/gpt-4o
```

### Ajustar Temperature (Criatividade)

```bash
python3 tools/agent_openrouter.py analista-negocios "Analise este mercado" --temp 0.3
```

## 🎨 Modelos Disponíveis

### Seus Modelos Favoritos (Configurados)

Modelos configurados no `config.json` e sempre visíveis no help:

- `anthropic/claude-haiku-4.5` ⭐ **(padrão)** - Rápido, eficiente e econômico
- `anthropic/claude-sonnet-4.5` - Excelente custo-benefício
- `openai/gpt-4o` - GPT-4 Omni
- `openai/gpt-4.1-mini` - Mini rápido
- `openai/gpt-5` - GPT-5 (próxima geração)
- `openai/gpt-5-mini` - GPT-5 versão econômica
- `google/gemini-2.5-pro` - Gemini Pro avançado
- `x-ai/grok-4-fast` - Grok 4 veloz
- `z-ai/glm-4.6` - GLM modelo chinês
- `deepseek/deepseek-chat-v3.1` - DeepSeek otimizado

## 📝 Criar Novo Agente

1. **Crie o arquivo do agente:**
```bash
nano agentes/openrouter/meu-agente.md
```

2. **Estrutura recomendada:**
```markdown
# AGENTE: [Nome do Agente]

[Descrição breve da expertise]

## Suas Competências Principais
- Competência 1
- Competência 2

## Metodologia
[Como o agente trabalha]

## Tom de Voz
[Estilo de comunicação]

## O Que Você NÃO Faz
[Limitações e limites]

---
[Instrução final de como responder]
```

3. **Use o agente:**
```bash
python3 tools/agent_openrouter.py meu-agente "Seu input aqui"
```

## 🎯 Agentes Disponíveis

### copywriter-vendas
**Especialidade**: Copy persuasivo e textos de vendas de alto impacto
**Quando usar**: Criar headlines, VSLs, anúncios, emails de venda, CTAs
**Modelo sugerido**: `anthropic/claude-sonnet-4.5`

```bash
python3 tools/agent_openrouter.py copywriter-vendas "Crie um headline para produto de emagrecimento que promete perder 5kg em 21 dias"
```

### analista-negocios
**Especialidade**: Análise estratégica, SWOT, business intelligence
**Quando usar**: Analisar mercados, validar ideias, criar estratégias
**Modelo sugerido**: `openai/gpt-4o` ou `anthropic/claude-sonnet-4.5`

```bash
python3 tools/agent_openrouter.py analista-negocios "Analise a viabilidade de abrir uma cafeteria em bairro residencial de classe média"
```

## ⚙️ Configuração

As configurações estão em `agentes/openrouter/config.json`:

```json
{
  "api_key": "sk-or-v1-...",
  "api_endpoint": "https://openrouter.ai/api/v1/chat/completions",
  "default_model": "anthropic/claude-haiku-4.5",
  "site_url": "https://github.com/felipemdepaula",
  "site_name": "Claude Code Workspace",
  "favorite_models": [
    "anthropic/claude-haiku-4.5",
    "anthropic/claude-sonnet-4.5",
    "openai/gpt-4o",
    "openai/gpt-4.1-mini",
    "openai/gpt-5",
    "openai/gpt-5-mini",
    "google/gemini-2.5-pro",
    "x-ai/grok-4-fast",
    "z-ai/glm-4.6",
    "deepseek/deepseek-chat-v3.1"
  ]
}
```

### Personalizar Configurações:

**Alterar modelo padrão:**
```bash
nano agentes/openrouter/config.json
# Mude "default_model" para o modelo desejado
```

**Editar modelos favoritos:**
```bash
nano agentes/openrouter/config.json
# Edite o array "favorite_models" com seus modelos preferidos
# Esses modelos aparecem no help do script
```

## 💡 Dicas de Uso

### Quando usar cada modelo:

**Claude Haiku 4.5** ⭐ (padrão)
- Uso geral, rápido e econômico
- Excelente para 90% das tarefas
- Resposta rápida, boa qualidade

**Claude Sonnet 4.5**
- Análises mais complexas
- Copy criativo e persuasivo
- Quando precisa de mais profundidade que o Haiku

**GPT-4o / GPT-5**
- Tarefas com formatos específicos
- Raciocínio estruturado avançado
- Quando precisa das capabilities OpenAI

**Gemini 2.5 Pro**
- Tarefas com contexto muito longo
- Multimodal avançado
- Alternativa ao GPT-4o

**DeepSeek Chat v3.1**
- Programação e código
- Raciocínio matemático
- Econômico para tarefas técnicas

**Grok 4 Fast**
- Respostas ultra-rápidas
- Conversação casual
- Brainstorming ágil

### Temperature:

- **0.0 - 0.3**: Tarefas analíticas, factuais, precisas
- **0.4 - 0.7**: Balanceado (padrão)
- **0.8 - 1.0**: Criativo, brainstorming, ideias originais

### Exemplos práticos:

```bash
# Copy criativo com temperature alta
python3 tools/agent_openrouter.py copywriter-vendas "Crie 5 headlines diferentes" --temp 0.9

# Análise precisa com temperature baixa
python3 tools/agent_openrouter.py analista-negocios "Calcule ROI desta estratégia" --temp 0.2

# Usar GPT-4o para tarefa específica
python3 tools/agent_openrouter.py copywriter-vendas "Escreva email de vendas" --model openai/gpt-4o
```

## 🔧 Troubleshooting

**Erro: Agente não encontrado**
```bash
# Liste os agentes disponíveis
python3 tools/agent_openrouter.py --list
```

**Erro de API Key**
```bash
# Verifique o config.json
cat agentes/openrouter/config.json
```

**Timeout**
```bash
# Modelos grandes podem demorar. O timeout padrão é 120s.
# Se necessário, edite o script agent_openrouter.py
```

## 💰 Custos

A OpenRouter cobra por tokens usados. Custos variam por modelo:

- **Claude Haiku 4.5**: Mais econômico, rápido
- **Claude Sonnet 4.5**: Custo-benefício intermediário
- **GPT-4o / GPT-5**: Mais caros, alta qualidade
- **DeepSeek / Grok**: Econômicos para tarefas específicas

**Dica**: Use Claude Haiku 4.5 para a maioria das tarefas. Reserve modelos premium para análises complexas.

**Ver preços atualizados**: https://openrouter.ai/models

## 🔗 Links Úteis

- **OpenRouter Dashboard**: https://openrouter.ai/
- **Lista de Modelos**: https://openrouter.ai/models
- **Documentação API**: https://openrouter.ai/docs
- **Preços**: https://openrouter.ai/models (veja "Pricing" em cada modelo)

---

**Criado para**: Claude Code Workspace
**Mantido por**: Felipe M de Paula
