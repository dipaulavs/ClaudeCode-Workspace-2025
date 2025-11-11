# Instagram AI Carousel - Workflow Automático 🚀

Workflow completo com auto-healing que cria e publica carrosséis no Instagram diariamente.

## 📋 Fluxo do Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Agente 1  │ → │   Agente 2  │ → │   Agente 3  │ → │   Script    │ → │  Instagram  │
│  Pesquisa   │    │  Hormozi    │    │  Documento  │    │   Imagens   │    │   Publish   │
│   (Haiku)   │    │  (Haiku)    │    │   (Haiku)   │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │                  │
   Notícia          Hook+Corpo          PDF com           5 imagens          Post ✅
    Tech/IA          +CTA+            link compra          slides           +Legenda
                   5 Slides                                                 +Hashtags
```

## 🤖 Auto-Healing

O orquestrador usa Claude API (Sonnet) para:
- ✅ Detectar erros em cada etapa
- ✅ Analisar causa raiz
- ✅ Sugerir correção
- ✅ Retentar automaticamente (até 3x)

## 🔧 Setup Local

### 1. Instalar dependências

```bash
cd SWARM/automations/instagram-ai-carousel
pip3 install -r requirements.txt
```

### 2. Configurar .env

Edite `.env` e adicione suas chaves:

```bash
ANTHROPIC_API_KEY=sk-ant-...         # Para auto-healing
OPENROUTER_API_KEY=sk-or-...         # Para agentes (Haiku)
INSTAGRAM_ACCESS_TOKEN=...           # Token Instagram Graph API
INSTAGRAM_ACCOUNT_ID=...             # ID da conta
```

### 3. Testar localmente

```bash
python3 orchestrator.py
```

## 📅 Configurar Cron (Execução Diária 18h)

### Na VPS (após deploy):

```bash
# Editar crontab
crontab -e

# Adicionar linha (executa todo dia às 18h):
0 18 * * * /path/to/run_daily.sh

# Ou usar horário específico do Brasil (GMT-3):
0 21 * * * /path/to/run_daily.sh  # 21h UTC = 18h BRT
```

## 🐳 Deploy na VPS

### 1. Deploy via SWARM

```bash
cd SWARM
./deploy.sh instagram-ai-carousel
```

### 2. Verificar status

```bash
./manage.sh status instagram-ai-carousel
```

### 3. Ver logs

```bash
./logs.sh instagram-ai-carousel
```

### 4. URL pública

https://insta-ai.loop9.com.br

## 📂 Estrutura de Arquivos

```
instagram-ai-carousel/
├── orchestrator.py      # Orquestrador principal com auto-healing
├── app.py              # Flask API (webhook/manual trigger)
├── run_daily.sh        # Script para cron
├── requirements.txt    # Dependências Python
├── .env               # Credenciais (NÃO commitar)
├── logs/              # Logs de execução
│   ├── workflow_*.log
│   ├── state_*.json
│   └── cron_*.log
└── output/            # Outputs gerados
    ├── hormozi_*.json
    ├── content_*.md
    ├── content_*.pdf
    └── slide_*.txt
```

## 🔍 Logs e Debugging

### Ver logs do workflow

```bash
tail -f logs/workflow_*.log
```

### Ver estado da última execução

```bash
cat logs/state_$(ls -t logs/state_*.json | head -1 | xargs basename).json
```

### Ver tentativas de auto-healing

Cada etapa falha registra:
- Erro original
- Causa raiz (análise Claude)
- Sugestão de correção
- Tentativas de retry

## 🎯 Personalização

### Alterar horário do agente de pesquisa

Edite `orchestrator.py:334` - método `_search_news()`

### Alterar framework Hormozi

Edite `orchestrator.py:358` - método `_create_hormozi_copy()`

### Adicionar API de imagens real

Edite `orchestrator.py:449` - método `_generate_slide_images()`

Exemplo com nanobanana:

```python
def _generate_slide_images(self, hormozi_data: dict):
    from tools.generate_nanobanana import generate_image

    image_paths = []
    for slide in hormozi_data['slides']:
        img_path = generate_image(slide['prompt_imagem'])
        image_paths.append(img_path)

    return image_paths
```

## 📊 Métricas

Cada execução gera:
- `state_*.json` - Estado completo do workflow
- `workflow_*.log` - Log detalhado
- `hormozi_*.json` - Copy gerado

## 🚨 Troubleshooting

### Erro: ANTHROPIC_API_KEY não configurada

Configure no `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

### Erro: OpenRouter 401

Verifique chave no `.env`:
```bash
OPENROUTER_API_KEY=sk-or-...
```

### Erro: Instagram API

Certifique-se que:
1. Token não expirou
2. Conta é Business/Creator
3. Permissões corretas (instagram_content_publish)

## 🔗 Links Úteis

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [Claude API](https://docs.anthropic.com/claude/reference)
- [SWARM Docs](../../../SWARM/README.md)

## 📝 Roadmap

- [ ] Integrar API real de imagens
- [ ] Webhook para trigger manual
- [ ] Dashboard de métricas
- [ ] Responder comentários automático
- [ ] DM automático com PDF

---

**Status:** ✅ Pronto para deploy
**URL:** https://insta-ai.loop9.com.br
**Cron:** Diário às 18h (configure após deploy)
