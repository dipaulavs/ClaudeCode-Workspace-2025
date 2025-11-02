# 📢 Meta Ads - Gerenciar Campanhas

Cria, lista, atualiza e deleta campanhas no Meta Ads.

## 🚀 Comandos

```bash
# Listar campanhas
python3 tools/meta_ads_campaigns.py list

# Criar campanha
python3 tools/meta_ads_campaigns.py create "Nome da Campanha" "OBJETIVO" --daily-budget VALOR

# Atualizar status
python3 tools/meta_ads_campaigns.py update CAMPAIGN_ID --status ACTIVE|PAUSED

# Deletar campanha
python3 tools/meta_ads_campaigns.py delete CAMPAIGN_ID
```

## 📝 Parâmetros

### Criar Campanha

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `nome` | ✅ | Nome da campanha |
| `objetivo` | ✅ | Ver "Objetivos" abaixo |
| `--daily-budget` | ❌ | Orçamento diário em $ (ex: 10.00) |
| `--lifetime-budget` | ❌ | Orçamento total em $ |
| `--status` | ❌ | ACTIVE ou PAUSED. Padrão: PAUSED |

### Objetivos Disponíveis

- `OUTCOME_TRAFFIC` - Tráfego para site
- `OUTCOME_AWARENESS` - Reconhecimento de marca
- `OUTCOME_ENGAGEMENT` - Engajamento
- `OUTCOME_LEADS` - Geração de leads
- `OUTCOME_SALES` - Conversões/vendas

## 💡 Exemplos

```bash
# Criar campanha de tráfego
python3 tools/meta_ads_campaigns.py create "Promoção Verão" "OUTCOME_TRAFFIC" --daily-budget 50

# Criar campanha de leads
python3 tools/meta_ads_campaigns.py create "Captura Leads" "OUTCOME_LEADS" --daily-budget 100 --status ACTIVE

# Pausar campanha
python3 tools/meta_ads_campaigns.py update 123456789 --status PAUSED

# Ativar campanha
python3 tools/meta_ads_campaigns.py update 123456789 --status ACTIVE
```

## 🔧 Config

`config/meta_ads_config.py`

## 📖 Docs Completa

`docs/meta-ads-api/META_ADS_API_DOCUMENTATION.md`
