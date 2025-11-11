---
name: exercito-hormozi-ads
description: Orquestra 3-6 subagentes especializados usando hormozi-copywriter para criar Top 3 melhores copys para anúncios Meta Ads de milhão de dólares. Todos agentes aplicam metodologias Hormozi ($100M Leads, Offers, Money Models). Suporta carrossel, anúncio único, reels. AUTO-INVOCA quando usuário pedir copy Meta Ads, anúncio milhão, army of Hormozi, ou múltiplas versões de copy.
---

# Exército Hormozi - Meta Ads

## Overview

Deploy an army of 3-6 specialized Hormozi copywriter agents working in hierarchical command structure to produce Top 3 best-performing Meta Ads copies. All agents activate `hormozi-copywriter` skill and apply methodologies from Hormozi's knowledge base ($100M Leads, $100M Offers, $100M Money Models).

**Mission:** Create million-dollar Meta Ads copy through competitive agent collaboration.

## Workflow

### Step 1: Initial Input Collection

**Ask user two questions (in sequence):**

1. **O que você quer vender?**
   - Collect: Product/service, niche, avatar, price range
   - Examples: "Chácara em Itatiaiuçu R$ 70k", "Curso de inglês R$ 497", "Coaching emagrecimento R$ 3k"

2. **Qual formato do anúncio?**
   - **Opção A:** Carrossel (10 slides)
   - **Opção B:** Anúncio único (imagem + texto)
   - **Opção C:** Reels (15s script)

**Stop here. Wait for both answers before proceeding.**

### Step 2: Reference Search (Conditional)

**IF product is real estate (imóveis/chácara/terreno/apartamento):**

```bash
# Search reference examples
Read file_path="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/carrossel/Exemplo Carrossel - Alex Hormozi [Imoveis].md"
Read file_path="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/Criativo imagem unica Estatico imagem  e texto/BODYS hormozi - criativo meta ads .md"
Read file_path="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/exemplos reels:tiktok/Roteiro Horomozi - Storyes 15s.md"
```

Use these proven templates as inspiration baseline. Adapt structure, not copy verbatim.

### Step 3: Agent Hierarchy Activation

**Deploy 3-6 agents in hierarchical structure:**

```
┌─────────────────────────────────────┐
│   COMANDANTE (General Agent)        │
│   skill: hormozi-copywriter         │
│   Role: Final decision, strategy    │
└─────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───────────┐    ┌──────────────┐
│ESPECIALISTA│    │ESPECIALISTA  │
│1-3 agents  │    │REVISOR       │
│Copy creation│   │Critical eval │
│hormozi-    │    │hormozi-      │
│copywriter  │    │copywriter    │
└───────────┘    └──────────────┘
```

**Agent Breakdown:**

1. **Comandante (1 agent)**
   - Skill: `hormozi-copywriter`
   - Task: Define strategy, choose frameworks, final approval
   - Methodologies: Value Equation, Core Four, Grand Slam Offer

2. **Especialistas (3-5 agents)**
   - Skill: `hormozi-copywriter` (each)
   - Task: Create competing copy variations
   - Methodologies: Hook formulas, Lead Getters, Money Models
   - Each agent produces 1 complete copy

3. **Revisor Crítico (1 agent)**
   - Skill: `hormozi-copywriter`
   - Task: Brutal critique (Hormozi-style), eliminate weak copies
   - Methodologies: Value Equation audit, hook contradiction check

**Total agents: 3-6 (Comandante + 1-4 Especialistas + Revisor)**

### Step 4: Parallel Agent Execution

**Launch all agents in PARALLEL (single message, multiple Task calls):**

```python
# Comandante
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Product: {user_product}
    Format: {ad_format}
    References: {real_estate_examples if applicable}

    Role: COMANDANTE - Define estratégia copy Meta Ads

    Tasks:
    1. Analise produto usando Value Equation
    2. Escolha frameworks ($100M Leads/Offers/Money Models)
    3. Defina avatar, objeções top 3, ganchos vencedores
    4. Crie estrutura base para Especialistas seguirem
    5. Retorne estratégia completa + 1 copy modelo

    Output: Estratégia (avatar, objeções, frameworks) + 1 copy completa
    """
)

# Especialista 1
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Product: {user_product}
    Format: {ad_format}
    Strategy: {comandante_strategy}

    Role: ESPECIALISTA 1 - Copy focada em DOR

    Tasks:
    1. Aplique Hook Formula (contradiction, numbers, timeline)
    2. Foque em Pain of Silence (dor íntima/frustração)
    3. Use frameworks: Custo de Não Agir, Perda Acumulada
    4. Crie copy COMPLETA (headline + body + CTA)

    Output: 1 copy completa focada em dor máxima
    """
)

# Especialista 2
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Product: {user_product}
    Format: {ad_format}
    Strategy: {comandante_strategy}

    Role: ESPECIALISTA 2 - Copy focada em MATEMÁTICA

    Tasks:
    1. Aplique Value Equation (Dream Outcome / Time Delay)
    2. Foque em comparação brutal (antes/depois números)
    3. Use frameworks: ROI, Economia, Valorização
    4. Crie copy COMPLETA com números específicos

    Output: 1 copy completa focada em matemática brutal
    """
)

# Especialista 3
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Product: {user_product}
    Format: {ad_format}
    Strategy: {comandante_strategy}

    Role: ESPECIALISTA 3 - Copy focada em OBJEÇÃO

    Tasks:
    1. Identifique objeção #1 do avatar
    2. Destrua objeção com prova social + casos reais
    3. Use frameworks: Grand Slam Offer, Perceived Likelihood
    4. Crie copy COMPLETA que remove fricção total

    Output: 1 copy completa que destrói objeção principal
    """
)

# Revisor Crítico
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Product: {user_product}
    Copies to review: {all_specialist_copies}

    Role: REVISOR CRÍTICO - Crítica brutal Hormozi-style

    Tasks:
    1. Audite cada copy com Value Equation
    2. Verifique: números específicos? timeline? contradiction?
    3. Identifique fraquezas (vague claims, passive voice, emoji spam)
    4. Score cada copy (0-100) baseado em metodologias Hormozi
    5. Ranqueie Top 3 melhores copies

    Output: Ranking Top 3 + justificativa (scores + fraquezas eliminadas)
    """
)
```

**IMPORTANT:** All Task calls must be in a SINGLE message to run in parallel.

### Step 5: Output Delivery

**Final deliverable format:**

```markdown
# 🏆 TOP 3 MELHORES COPIES - {PRODUTO}
**Formato:** {Carrossel | Anúncio Único | Reels}
**Avatar:** {descrição}
**Objeções destruídas:** {lista}

---

## 🥇 COPY #1 - {ABORDAGEM}
**Score:** {0-100}
**Frameworks aplicados:** {lista}

{COPY COMPLETA}

**Por que funciona:**
- {razão 1}
- {razão 2}
- {razão 3}

---

## 🥈 COPY #2 - {ABORDAGEM}
**Score:** {0-100}
**Frameworks aplicados:** {lista}

{COPY COMPLETA}

**Por que funciona:**
- {razão 1}
- {razão 2}
- {razão 3}

---

## 🥉 COPY #3 - {ABORDAGEM}
**Score:** {0-100}
**Frameworks aplicados:** {lista}

{COPY COMPLETA}

**Por que funciona:**
- {razão 1}
- {razão 2}
- {razão 3}

---

## 📊 RECOMENDAÇÃO
**Testar primeiro:** Copy #{X}
**Razão:** {justificativa estratégica}
```

## Format-Specific Guidelines

### Carrossel (10 slides)

**Structure:**
1. Slide 1: Hook brutal (matemática/comparação/objeção)
2. Slides 2-3: Credibilidade (casos, números, prova)
3. Slides 4-7: Value stack (comparação, benefícios, destruição objeções)
4. Slide 8: Recapitulação (matemática final)
5. Slide 9: Urgência real (escassez verificável)
6. Slide 10: CTA específico + ação baixa fricção

**Specialists create:** Full 10-slide structure with visual notes

**References:** If real estate, use `/biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/carrossel/`

### Anúncio Único (imagem + texto)

**Structure:**
- **Hook:** Primeira linha (contradiction + números)
- **Body:** Matemática/comparação/objeção (150-300 palavras)
- **Offer:** Stack completo (core + bonuses + garantia)
- **CTA:** Ação específica + urgência

**Specialists create:** Headline + body copy + visual suggestions

**References:** If real estate, use `/biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/Criativo imagem unica Estatico imagem e texto/`

### Reels (15s script)

**Structure:**
- **0-3s:** Hook visual + verbal (contradiction brutal)
- **3-10s:** Setup problema → Solução simples
- **10-15s:** CTA direto + urgência

**Format:** Script para blogueira com milhões de seguidores
**Tom:** Casual, conversacional, números específicos, linguagem adequada ao público-alvo

**Specialists create:** Script completo 15s com timing marcado

**References:** If real estate, use `/biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/exemplos reels:tiktok/`

**Example Reels Script:**
```
[0-3s] VISUAL: Blogueira segurando iPhone
"Pergunta honesta... Você gastaria 9 mil num iPhone novo?"

[3-8s] VISUAL: Mostrar terreno
"iPhone: 9 mil. Daqui um ano vale 4 mil e quinhentos.
Chácara: 10 mil de entrada. Daqui um ano vale 130 mil."

[8-12s] VISUAL: Comparação lado a lado
"É literalmente a mesma quantidade de dinheiro.
Um vira lixo eletrônico. Outro vira patrimônio."

[12-15s] VISUAL: CTA na tela
"Qual você prefere? Chama. Link na bio."
```

## Metodologias Hormozi Aplicadas

**All agents MUST use these frameworks:**

### From $100M Leads (100m-leads KB)
- **Hook Formula:** Effort High + Result Low → Change Small + Result Massive
- **Core Four:** Warm outreach, cold outreach, paid ads, content
- **Lead Getters:** Lead magnets, CTAs específicos, baixa fricção
- **Hook-Retain-Reward:** Estrutura scripts/sequências

### From $100M Offers (100m-offers KB)
- **Value Equation:** (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort/Sacrifice)
- **Grand Slam Offer:** Core + Bonuses + Scarcity + Urgency + Guarantee + Name
- **Pricing Strategy:** Anchor, comparison, economia brutal

### From $100M Money Models (100m-money-models KB)
- **Attraction:** Free goodwill, giveaway, decoy
- **Upsell:** Classic, menu, anchor
- **Downsell:** Payment plan, trial with penalty
- **Continuity:** Bonus, discount, waived fee

## Quality Standards (Revisor Checklist)

**Each copy must have:**

✅ **Numbers (minimum 3 specific):** Prices, timelines, quantities
✅ **Contradiction:** Opposite of expected ("ate pizza and lost 45 lbs")
✅ **Timeline:** Specific ("in 90 days", not "quickly")
✅ **Social Proof:** Cases, testimonials, track record
✅ **Comparison:** Before/after, us vs them, option A vs B
✅ **Objeção destruída:** Address top avatar concern
✅ **CTA específico:** Exact action ("Manda: TENHO R$ 10K")
✅ **Urgência real:** Verifiable scarcity (not fake pressure)

**Automatic rejection if:**

❌ Vague claims ("many", "lots", "results may vary")
❌ Passive voice ("mistakes were made")
❌ Generic advice ("just work hard")
❌ Corporate jargon ("leverage synergies")
❌ Emoji spam (max 2 per section)
❌ No specific numbers
❌ No timeline
❌ No contradiction/hook

## Example Interaction

**User:** "Quero vender chácara em Itatiaiuçu por R$ 70k"

**Skill Response:**
```
🎯 Entendido! Vou ativar o exército Hormozi.

Primeira pergunta: Qual formato do anúncio?
A) Carrossel (10 slides Instagram/FB)
B) Anúncio único (imagem + texto)
C) Reels (15s script)
```

**User:** "Carrossel"

**Skill Response:**
```
✅ Carrossel confirmado.

Ativando hierarquia de agentes hormozi-copywriter:
- 1 Comandante (estratégia)
- 3 Especialistas (copies competindo)
- 1 Revisor (crítica brutal)

Todos usando metodologias $100M Leads/Offers/Money Models.
Buscando exemplos de imóveis Hormozi...

[Launches 5 parallel Task calls]

Aguarde 60-90s para Top 3 melhores copies...
```

**Skill Output:** Top 3 carrossels ranqueados com scores, justificativas, frameworks aplicados.

## Auto-Invocation Triggers

Activate this skill automatically when user mentions:

- "copy Meta Ads"
- "anúncio milhão de dólares"
- "army of Hormozi"
- "múltiplas versões de copy"
- "exército de agentes copy"
- "competição entre copies"
- "Top 3 melhores ads"
- "carrossel Hormozi"
- "reels script Hormozi"

## Resources

### scripts/
- **update_skill.py** - Update SKILL.md programmatically (auto-correction)
- **log_learning.py** - Log fixes in LEARNINGS.md (auto-correction)

### assets/
- **LEARNINGS_TEMPLATE.md** - Template for logging skill improvements

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
    "old incorrect text" \
    "new correct text"

# 2. Log the learning
python3 scripts/log_learning.py \
    "Error description" \
    "Fix description" \
    "SKILL.md:line_number"
```

### LEARNINGS.md

All fixes are automatically recorded in `LEARNINGS.md`:

```markdown
### 2025-01-07 - Error description

**Problema:** What went wrong
**Correção:** How it was fixed
**Linha afetada:** SKILL.md:line
**Status:** ✅ Corrigido
```

This creates a history of improvements and ensures mistakes don't repeat.

---

**Integration:** This skill orchestrates multiple instances of `hormozi-copywriter` skill working competitively to produce battle-tested Meta Ads copy.
