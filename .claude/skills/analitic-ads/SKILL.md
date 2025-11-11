---
name: analitic-ads
description: Busca métricas de campanhas Meta Ads ativas, analisa com framework Hormozi, e gera dashboard HTML visual (estilo MotherDuck) salvo em Downloads com nome do produto + data BR. Auto-invoca quando usuário pedir para analisar/puxar/ver métricas de anúncios Meta/Facebook.
---

# Analitic Ads - Dashboard Automático Meta Ads

Skill para análise completa e automatizada de campanhas Meta Ads com geração de dashboard visual.

## Overview

Automatiza o processo completo de buscar métricas de campanhas Meta Ads, analisar performance usando framework Hormozi + Andromeda 2025, apresentar resumo em texto com métricas que realmente importam, e gerar dashboard HTML visual (estilo MotherDuck) salvo em Downloads com nome do produto e data brasileira.

## Quando Usar

Auto-invocar quando o usuário:
- Pedir para "puxar métricas da campanha"
- Pedir para "analisar anúncios"
- Pedir para "ver performance dos ads"
- Mencionar "dashboard de anúncios"
- Pedir relatório de Meta Ads / Facebook Ads

## Workflow Completo

### Passo 1: Buscar Métricas

Executar o script `scripts/fetch_meta_ads.py` para buscar dados da API Meta Ads:

```bash
# Buscar todas as campanhas ativas
python3 scripts/fetch_meta_ads.py

# OU buscar campanha específica
python3 scripts/fetch_meta_ads.py <campaign_id>
```

**O que o script faz:**
- Conecta na API Meta Ads (conta act_1050347575979650)
- Busca métricas dos últimos 30 dias
- Extrai: spend, impressões, alcance, cliques, CPC, CPM, CTR, frequência, conversões
- Calcula custo por conversão
- Analisa com framework Hormozi (CTR, CPA, Volume, Frequência)
- **Imprime resumo em texto** formatado
- Salva JSON completo em `/tmp/meta_ads_data.json`

### Passo 2: Apresentar Resumo ao Usuário

**IMPORTANTE:** Após executar `fetch_meta_ads.py`, apresentar ao usuário um resumo conciso das métricas em formato de texto simples, destacando:

- Status geral (Winner / Promissor / Precisa atenção)
- Métricas-chave (Gasto, Conversões, Custo/Conversão, CTR)
- Análise Hormozi (o que está bom, o que precisa melhorar)
- Recomendações (escalar, pausar, criar variações, etc)

**Exemplo de resumo:**

```
✅ Sua campanha está PERFORMANDO MUITO BEM!

📊 Resumo:
- Investimento: R$ 150 (últimos 30 dias)
- Conversas WhatsApp: 51
- Custo/Conversa: R$ 2,94 ✅ EXCELENTE
- CTR: 5.28% ✅ MUITO ACIMA DA MÉDIA

🔥 Análise Hormozi:
✅ CTR 5.28% - Hook funciona, copy está ótima
✅ R$ 2,94/conversa - Muito competitivo para imóveis
✅ 51 conversões - Volume validado (meta: 10+)
✅ Frequência 1.69 - Audiência fresca, não saturada

💡 Recomendações:
1. ESCALAR: Aumentar budget de R$ 150 → R$ 300/mês
2. DUPLICAR: Criar 2-3 variações do criativo vencedor
3. TESTAR: Novo ângulo (Prova Social ou Quebra de Crença)
4. MONITORAR: Frequência (pausar se > 3.5)
```

### Passo 3: Gerar Dashboard HTML

Executar o script `scripts/generate_dashboard.py` para criar dashboard visual:

```bash
python3 scripts/generate_dashboard.py /tmp/meta_ads_data.json
```

**O que o script faz:**
- Lê o JSON gerado no Passo 1
- Gera dashboard HTML completo (estilo MotherDuck: beige, yellow, dark-gray)
- Inclui:
  - Resumo geral (4 cards principais)
  - Status da campanha (alert success/warning/danger)
  - Métricas primárias (CTR, CPA, Conversões, Frequência) com status visual
  - Métricas secundárias (Impressões, Alcance, CPM, Cliques)
- **Salva em Downloads** com nome: `{produto}_{data-br}.html`

**Exemplo de nome de arquivo:**
```
~/Downloads/imovel-premium_2025-11-11.html
```

### Passo 4: Informar ao Usuário

Após gerar o dashboard, informar ao usuário:

```
✅ Dashboard salvo em Downloads!

📁 Arquivo: imovel-premium_2025-11-11.html
📊 Dashboard visual com todas as métricas no estilo MotherDuck
🎨 Design limpo: beige, yellow, dark-gray com cards interativos

Para abrir: Vá em Downloads e clique duas vezes no arquivo.
```

## Métricas Analisadas (Framework Hormozi)

### Métricas Primárias (Decisivas)

1. **CTR (Click-Through Rate)** - Indica se hook/copy funciona
   - ✅ Excelente: 5%+
   - ✅ Bom: 3-5%
   - ⚠️ Médio: 1.5-3%
   - ❌ Ruim: < 1.5%

2. **CPA (Custo por Aquisição)** - Indica rentabilidade
   - ✅ Ótimo: ≤ R$ 5
   - ✅ Bom: R$ 5-10
   - ⚠️ Alto: R$ 10-20
   - ❌ Crítico: > R$ 20

3. **Volume de Conversões** - Indica se está validado
   - ✅ Validado: 10+ conversões
   - ⚠️ Aguardando: 5-9 conversões
   - ❌ Insuficiente: < 5 conversões

4. **Frequência** - Indica saturação de audiência
   - ✅ Saudável: < 2.0
   - ✅ Boa: 2.0-3.5
   - ⚠️ Alta: 3.5-5.0
   - ❌ Crítica: > 5.0

### Métricas Secundárias (Informativas)

- **Impressões** - Quantas vezes o anúncio foi visto
- **Alcance** - Quantas pessoas únicas viram
- **CPM** - Custo por mil impressões (normal: R$ 10-30)
- **CPC** - Custo por clique

## Resources

### scripts/

- **fetch_meta_ads.py** - Busca métricas da API Meta Ads e analisa com framework Hormozi
  - Funções: `fetch_campaign_metrics()`, `extract_key_metrics()`, `format_text_summary()`
  - Output: Resumo em texto + JSON em /tmp/meta_ads_data.json

- **generate_dashboard.py** - Gera dashboard HTML visual (estilo MotherDuck)
  - Funções: `generate_status_alert()`, `generate_metric_card()`, `generate_dashboard()`
  - Output: HTML salvo em Downloads com nome {produto}_{data-br}.html

- **update_skill.py** - Script de auto-correção para atualizar SKILL.md
- **log_learning.py** - Script para registrar correções em LEARNINGS.md

## Auto-Correction System

This skill includes an automatic error correction system that learns from mistakes and prevents them from happening again.

### How It Works

When a script or command in this skill fails:

1. **Detect the error** - The system identifies what went wrong
2. **Fix automatically** - Updates the skill's code/instructions
3. **Log the learning** - Records the fix in LEARNINGS.md
4. **Prevent recurrence** - Same error won't happen again

### Using Auto-Correction

**Scripts available:**

```bash
# Fix a problem in this skill's SKILL.md
python3 scripts/update_skill.py <old_text> <new_text>

# Log what was learned
python3 scripts/log_learning.py <error_description> <fix_description> [line]
```

**Example workflow when error occurs:**

```bash
# 1. Fix the error in SKILL.md
python3 scripts/update_skill.py \
    "--prompt" \
    ""

# 2. Log the learning
python3 scripts/log_learning.py \
    "Flag --prompt not recognized" \
    "Removed --prompt flag, using positional argument" \
    "SKILL.md:line_number"
```

### LEARNINGS.md

All fixes are automatically recorded in `LEARNINGS.md`:

```markdown
### 2025-01-07 - Flag --prompt not recognized

**Problema:** Script doesn't accept --prompt flag
**Correção:** Removed --prompt, now uses positional argument
**Linha afetada:** SKILL.md:97
**Status:** ✅ Corrigido
```

This creates a history of improvements and ensures mistakes don't repeat.
