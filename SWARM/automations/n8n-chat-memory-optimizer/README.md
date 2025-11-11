# 💰 N8N Chat Memory Optimizer - Economiza 70% de Tokens

## 🎯 O que faz

Reduz drasticamente o consumo de tokens em chatbots n8n usando **resumos inteligentes**:

```
Conversa normal (10 msgs × 100 tokens) = 1000 tokens
    ↓
Com otimizador (resumo 100 + 5 msgs × 100) = 600 tokens
    ↓
ECONOMIA: 40% ✅
```

## 🚀 Como funciona

```
Mensagem recebida
    │
    ├─ Contador < 10? → AI Agent (últimas 5 msgs + resumo anterior)
    │
    └─ Contador = 10? → Resumir tudo
                         │
                         ├─ Salvar resumo
                         ├─ Limpar histórico antigo
                         └─ Reset contador
```

## 📦 Instalação

### 1. Importar workflow no n8n

1. Abra n8n
2. Clique em **"+"** → **"Import from File"**
3. Selecione `workflow-economizar-tokens.json`
4. Ativar workflow

### 2. Configurar Redis

Certifique-se que o nó Redis está conectado:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=sua_senha
```

### 3. Configurar OpenAI

No nó **"AI Summarizer"**:
- Adicione suas credenciais OpenAI
- Modelo recomendado: `gpt-4o-mini` (mais barato para resumos)

## ⚙️ Ajustes Personalizados

### Window Size (quantas mensagens recentes manter)

No nó **"Redis Chat Memory (5 msgs)"**:

```javascript
contextWindowLength: 5  // Altere aqui (3-10 recomendado)
```

### Frequência de Resumo

No nó **"10+ mensagens?"**:

```javascript
value2: 10  // Resumir a cada X mensagens
```

### Prompt de Resumo

No nó **"AI Summarizer"** → Personalize o prompt:

```
RESUMA a conversa abaixo em 3-4 frases, mantendo:
✓ Assunto principal
✓ Informações críticas mencionadas
✓ Decisões ou acordos
✓ Status atual

ELIMINE:
✗ Saudações
✗ Mensagens repetidas
✗ Informações irrelevantes
```

## 📊 Comparação de Custos

| Cenário | Tokens/msg | Custo/1000 msgs* |
|---------|-----------|------------------|
| **Sem otimização** (10 msgs) | ~1000 | $1.50 |
| **Window 5 msgs** | ~500 | $0.75 |
| **Com resumos** | ~300 | $0.45 |

*Baseado em GPT-4o ($0.0015/1K tokens)

## 🔍 Monitoramento

### Ver quantas mensagens na sessão

```bash
redis-cli GET msg_count_SESSION_ID
```

### Ver resumo salvo

```bash
redis-cli GET summary_SESSION_ID
```

### Limpar tudo (reset)

```bash
redis-cli FLUSHDB
```

## 🐛 Troubleshooting

### Resumo não está sendo gerado

Verifique:
1. Nó "AI Summarizer" tem credenciais OpenAI válidas
2. Redis está rodando (`redis-cli ping` → PONG)
3. Contador chegou a 10 mensagens

### Erro "history undefined"

O nó "Get Full History" precisa:
- Mesmo `sessionKey` do Redis Memory principal
- `contextWindowLength: 10` (ou mais) para pegar histórico completo

### AI Agent não usa resumo

Certifique-se que o prompt do AI Agent inclui:

```javascript
text: "=CONTEXTO ANTERIOR:\n{{ $('Get Saved Summary').item.json.value || 'Primeira conversa' }}\n\n---\nUSUÁRIO: {{ $json.message }}"
```

## 🎨 Melhorias Futuras

- [ ] Resumo multinível (resumir resumos antigos)
- [ ] Compressão semântica com embeddings
- [ ] Dashboard de economia de tokens
- [ ] Auto-ajuste de window size baseado em custo

## 📚 Referências

- [n8n Memory Nodes](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.memorybuffermemory/)
- [Token Optimization Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

---

**v1.0** | Economize até 70% em tokens | Compatible with n8n 1.0+
