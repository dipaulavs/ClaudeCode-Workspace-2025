---
name: hormozi-exercito-viral
description: Orquestra 3-6 subagentes especializados Hormozi para criar carrosséis educativos ultra-virais projetados para máximo engajamento via comentários com palavra-chave. Combina conteúdo de altíssimo valor + copy Hormozi + estratégia de comentários. Auto-invoca quando usuário pedir carrossel viral, conteúdo educativo, ou estratégia de comentários.
---

# Exército Hormozi - Carrosseis Virais Educativos

## Overview

Deploy an army of 3-6 specialized Hormozi copywriter agents working in hierarchical command structure to produce ultra-viral educational carousels designed for maximum comment engagement with keyword triggers. All agents activate `hormozi-copywriter` skill and apply methodologies from Hormozi's knowledge base ($100M Leads, $100M Offers, $100M Money Models).

**Mission:** Create educational carousels that generate massive comment volume with specific keywords through high-value content + Hormozi frameworks.

**Differentiation from exercito-hormozi-ads:**
- **exercito-hormozi-ads:** Sales-focused, designed to convert with offers
- **hormozi-exercito-viral:** Education-focused, designed to go viral with comments + keywords

## Viral Comment Strategy

### Core Principle: Hook-Educate-Trigger

Educational content that delivers immense value while strategically triggering keyword comments.

**Formula:**
```
High-Value Education (90%) + Strategic Comment Trigger (10%) = Viral Explosion
```

**Comment Trigger Mechanisms:**

1. **Opinion Poll Trigger**
   - Present two valid options
   - Ask: "Qual você prefere? Comenta [PALAVRA1] ou [PALAVRA2]"
   - Example: "Qual melhor? Comenta TERRENO ou APARTAMENTO"

2. **Quiz/Test Trigger**
   - Educational content with correct answer reveal
   - Ask: "Acertou? Comenta SIM ou NAO"
   - Example: "90% erra. Você acertou? Comenta ACERTEI ou ERREI"

3. **Personal Experience Trigger**
   - Relatable scenario question
   - Ask: "Aconteceu com você? Comenta [PALAVRA]"
   - Example: "Já passou por isso? Comenta JA PASSEI"

4. **Challenge Trigger**
   - Dare/challenge framework
   - Ask: "Vai tentar? Comenta [PALAVRA]"
   - Example: "Desafio você a testar. Vai tentar? Comenta VOU TENTAR"

5. **Save for Later Trigger**
   - High-value tip/method
   - Ask: "Salvou? Comenta [PALAVRA]"
   - Example: "Guarda esse método. Salvou? Comenta SALVEI"

**Keyword Selection Rules:**
- 2-4 words max (never long phrases)
- Easy to type (no special characters)
- Natural/organic (not forced)
- Related to content theme
- Distinct options (TERRENO ≠ APARTAMENTO, clear choice)

## Workflow

### Step 1: Initial Input Collection

**Ask user three questions (in sequence):**

1. **Qual o tema/nicho do conteúdo educativo?**
   - Collect: Topic, target audience, main teaching goal
   - Examples: "Investimentos para iniciantes", "Marketing digital orgânico", "Mindset empreendedor"

2. **Qual objetivo principal?**
   - **Opção A:** Ensinar método/framework específico
   - **Opção B:** Quebrar crença/mito comum
   - **Opção C:** Comparação educativa (X vs Y)

3. **Qual palavra-chave você quer nos comentários?**
   - If user doesn't know: "Deixa eu sugerir baseado no conteúdo"
   - Get keyword preference or autonomy to suggest

**Stop here. Wait for all three answers before proceeding.**

### Step 2: Strategic Analysis (Viral + Educational)

**BEFORE launching agents, analyze:**

1. **Avatar Educational Profile:**
   - What do they NOT know yet?
   - What misconception do they have?
   - What simple shift would blow their mind?

2. **Value Bomb Content:**
   - What single insight is worth gold?
   - What method can be taught in 10 slides?
   - What comparison reveals truth?

3. **Hormozi Hook for Education:**
   - Contradiction: "Everyone says X. Truth is Y."
   - Timeline: "Took me 5 years to learn. You'll get it in 60 seconds."
   - Numbers: "97% don't know this. Those 3% are rich."

4. **Comment Trigger Design:**
   - Which trigger mechanism fits? (poll, quiz, experience, challenge, save)
   - What keywords make sense? (2-4 word max, organic)
   - Where to place trigger? (usually Slide 9-10, after value delivery)

5. **Educational Value Stack:**
   - Slide 1: Hook (contradiction/stat)
   - Slides 2-4: Problem education (why most fail)
   - Slides 5-7: Solution education (framework/method)
   - Slide 8: Proof/validation (cases, results)
   - Slide 9: Recap with CTA
   - Slide 10: Comment trigger

### Step 3: Agent Hierarchy Activation

**Deploy 3-6 agents in hierarchical structure:**

```
┌─────────────────────────────────────┐
│   COMANDANTE (General Agent)        │
│   skill: hormozi-copywriter         │
│   Role: Strategy + value architecture│
└─────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───────────┐    ┌──────────────┐
│ESPECIALISTA│    │ESPECIALISTA  │
│2-4 agents  │    │REVISOR       │
│Copy creation│   │Critical eval │
│hormozi-    │    │hormozi-      │
│copywriter  │    │copywriter    │
└───────────┘    └──────────────┘
```

**Agent Breakdown:**

1. **Comandante (1 agent)**
   - Skill: `hormozi-copywriter`
   - Task: Define educational strategy, value architecture, comment trigger placement
   - Methodologies: Hook-Retain-Reward, Value Equation, Educational frameworks

2. **Especialistas (2-4 agents)**
   - Skill: `hormozi-copywriter` (each)
   - Task: Create competing carousel versions with different educational angles
   - Focus areas:
     - **Especialista 1:** Method/Framework education
     - **Especialista 2:** Myth-busting education
     - **Especialista 3:** Comparison education
     - **Especialista 4 (optional):** Story-based education
   - Each agent produces 1 complete 10-slide carousel

3. **Revisor Crítico (1 agent)**
   - Skill: `hormozi-copywriter`
   - Task: Audit educational value + viral potential + comment trigger effectiveness
   - Checks:
     - Does it ACTUALLY educate? (not just hype)
     - Is value immense? (save-worthy content)
     - Does comment trigger feel natural?
     - Will people share + comment?

**Total agents: 4-6 (Comandante + 2-4 Especialistas + Revisor)**

### Step 4: Parallel Agent Execution

**Launch all agents in PARALLEL (single message, multiple Task calls):**

```python
# Comandante
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Topic: {user_topic}
    Goal: {educational_goal}
    Keyword: {target_keyword}
    Strategic Analysis: {viral_educational_analysis}

    Role: COMANDANTE - Define estratégia carrossel educativo viral

    Tasks:
    1. Analyze educational opportunity (what insight to teach)
    2. Design value architecture (how to structure teaching)
    3. Apply Hormozi frameworks (Hook-Retain-Reward for education)
    4. Design comment trigger (mechanism + keyword placement)
    5. Create 1 complete carousel modelo (10 slides)

    Educational principles:
    - Value FIRST, trigger LAST (90% education / 10% trigger)
    - Teach ONE thing brilliantly (not many things poorly)
    - Use Hormozi contradiction/numbers for hooks
    - Make trigger feel natural (not forced)

    Output: Estratégia completa + 1 carousel educativo viral
    """
)

# Especialista 1: Method Education
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Topic: {user_topic}
    Strategy: {comandante_strategy}
    Keyword: {target_keyword}

    Role: ESPECIALISTA 1 - Carrossel educativo MÉTODO

    Tasks:
    1. Teach specific method/framework (step-by-step)
    2. Use Hormozi hook (timeline, effort reduction)
    3. Break down into actionable steps (Slides 5-7)
    4. Provide proof/validation (Slide 8)
    5. Integrate comment trigger naturally (Slide 10)

    Example structure:
    Slide 1: "Levei 3 anos pra aprender isso. Você vai entender em 60s."
    Slides 2-4: Por que método tradicional falha
    Slides 5-7: Framework passo a passo
    Slide 8: Casos de quem aplicou
    Slide 9: Recapitulação
    Slide 10: "Salvou? Comenta SALVEI"

    Output: 1 carousel completo focado em método
    """
)

# Especialista 2: Myth-Busting Education
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Topic: {user_topic}
    Strategy: {comandante_strategy}
    Keyword: {target_keyword}

    Role: ESPECIALISTA 2 - Carrossel educativo QUEBRA DE CRENÇA

    Tasks:
    1. Identify common misconception/belief
    2. Use Hormozi contradiction hook
    3. Educate on why belief is wrong (Slides 2-4)
    4. Reveal truth with evidence (Slides 5-7)
    5. Integrate comment trigger (opinion poll style)

    Example structure:
    Slide 1: "97% acreditam em X. Todos estão errados. Vou provar."
    Slides 2-4: Por que crença existe (histórico/cultura)
    Slides 5-7: Verdade com evidência
    Slide 8: Comparação brutal (crença vs verdade)
    Slide 9: Conclusão
    Slide 10: "Você acreditava nisso? Comenta SIM ou NAO"

    Output: 1 carousel completo focado em quebra de crença
    """
)

# Especialista 3: Comparison Education
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Topic: {user_topic}
    Strategy: {comandante_strategy}
    Keyword: {target_keyword}

    Role: ESPECIALISTA 3 - Carrossel educativo COMPARAÇÃO

    Tasks:
    1. Present two valid options (X vs Y)
    2. Educate on pros/cons of each (Slides 3-7)
    3. Use Hormozi math (numbers, timelines, outcomes)
    4. Integrate opinion poll trigger naturally

    Example structure:
    Slide 1: "X ou Y? 90% escolhem errado."
    Slides 2-3: Opção X (prós, contras, casos)
    Slides 4-5: Opção Y (prós, contras, casos)
    Slides 6-7: Comparação direta (matemática brutal)
    Slide 8: Contextos onde cada funciona
    Slide 9: Conclusão educativa
    Slide 10: "Qual você prefere? Comenta [PALAVRA1] ou [PALAVRA2]"

    Output: 1 carousel completo focado em comparação educativa
    """
)

# Revisor Crítico
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Activate skill: hormozi-copywriter

    Topic: {user_topic}
    Carousels to review: {all_specialist_carousels}
    Keyword: {target_keyword}

    Role: REVISOR CRÍTICO - Auditoria viral + educacional

    Tasks:
    1. Audit educational value (does it ACTUALLY teach something gold?)
    2. Audit Hormozi frameworks applied (hook, numbers, contradiction)
    3. Audit viral potential (will people save + share?)
    4. Audit comment trigger (natural? effective? keyword fits?)
    5. Score each carousel (0-100) on:
       - Educational value (0-40 pts)
       - Viral potential (0-30 pts)
       - Hormozi quality (0-20 pts)
       - Comment trigger (0-10 pts)
    6. Rank Top 3 best carousels

    Rejection criteria:
    ❌ Vague/generic education (everyone knows this)
    ❌ No Hormozi frameworks applied
    ❌ Forced/unnatural comment trigger
    ❌ Low save/share potential

    Output: Ranking Top 3 + scores breakdown + justification
    """
)
```

**IMPORTANT:** All Task calls must be in a SINGLE message to run in parallel.

### Step 5: Output Delivery

**Final deliverable format:**

```markdown
# 🏆 TOP 3 CARROSSEIS VIRAIS - {TEMA}
**Objetivo:** {Educativo}
**Palavra-chave:** {KEYWORD}
**Trigger:** {Mechanism}

---

## 🥇 CARROSSEL #1 - {ABORDAGEM}
**Score Total:** {0-100}
- Educational Value: {/40}
- Viral Potential: {/30}
- Hormozi Quality: {/20}
- Comment Trigger: {/10}

**Frameworks aplicados:** {lista}

### Slides:

**[Slide 1] Hook**
{copy}

**[Slide 2] Context**
{copy}

...

**[Slide 10] Comment Trigger**
{copy com keyword}

**Por que funciona:**
- {razão educacional}
- {razão viral}
- {razão Hormozi}

---

## 🥈 CARROSSEL #2 - {ABORDAGEM}
{same structure}

---

## 🥉 CARROSSEL #3 - {ABORDAGEM}
{same structure}

---

## 📊 RECOMENDAÇÃO
**Testar primeiro:** Carrossel #{X}
**Razão:** {justificativa estratégica}

**Expectativa de performance:**
- Saves: {estimativa}
- Shares: {estimativa}
- Comments com keyword: {estimativa}
```

## Educational Content Quality Standards

**Each carousel must have:**

✅ **High Value Education:** Teaches something non-obvious, actionable, specific
✅ **Hormozi Frameworks:** Hook formula, numbers, contradiction, timeline
✅ **Actionable Insight:** Reader can apply immediately after reading
✅ **Save-Worthy:** Content deserves to be bookmarked/referenced
✅ **Natural Trigger:** Comment keyword feels organic, not forced
✅ **Clear Structure:** Hook → Problem → Solution → Proof → Trigger

**Automatic rejection if:**

❌ Generic/obvious content ("work hard", "be consistent")
❌ No specific numbers/timelines
❌ Vague teaching (what to do, not HOW)
❌ Forced comment trigger ("Comenta XYZ123 se concorda")
❌ Low educational value (fluff, motivation only)
❌ Missing Hormozi frameworks

## Viral Mechanics Explained

### Why Educational Content Goes Viral

1. **Save-and-Share Reflex:**
   - High-value education triggers "I need to save this"
   - People share to look smart/helpful to followers

2. **Comment-to-Engage:**
   - After receiving value, people want to participate
   - Simple keyword comment = low-friction engagement
   - Triggers algorithm boost (Instagram/LinkedIn prioritize comments)

3. **Social Proof Loop:**
   - High comment count → more people check carousel
   - More saves → Instagram shows to more people
   - Viral loop: Comments → Views → Saves → More Comments

### Comment Trigger Science

**Optimal placement:** Slide 10 (after full value delivery)

**Psychology:**
- Reciprocity: "You gave me value, I'll comment"
- Ease: "Just type one word? Easy."
- Belonging: "Others are commenting, I'll join"
- Curiosity: "Let me see what others chose"

**Keyword requirements:**
- Short (1-3 words, max 4)
- Natural to content
- Easy to type (no accents, numbers, symbols)
- Clear options (if poll-style)

## Example Interaction

**User:** "Quero criar carrossel viral sobre investimento em terrenos"

**Skill Response:**
```
🎯 Entendido! Vou ativar o exército Hormozi para carrossel educativo viral.

Primeira pergunta: Qual objetivo principal?
A) Ensinar método de análise de terrenos
B) Quebrar mito "terreno não valoriza"
C) Comparação: Terreno vs Apartamento

Segunda pergunta: Qual palavra-chave quer nos comentários?
(Se não souber, posso sugerir baseado no conteúdo)
```

**User:** "B) Quebrar mito. Palavra-chave pode sugerir."

**Skill Response:**
```
✅ Objetivo: Quebrar mito "terreno não valoriza"
✅ Palavra-chave sugerida: TERRENO ou APARTAMENTO (opinion poll)

Fazendo análise estratégica viral + educacional...

ANÁLISE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Avatar: Pessoa 25-40 anos, quer investir mas ouve "terreno não vale a pena"

Crença falsa: "Terreno não valoriza, só apartamento pronto"

Verdade: Terrenos valorizam 2-3x mais que apartamentos (dados)

Hook Hormozi: "Amigo comprou apartamento R$ 300k. Comprei terreno R$ 70k.
              3 anos depois: Apartamento vale R$ 320k (+6%). Terreno vale
              R$ 180k (+157%). Mesma cidade. Qual investimento ruim?"

Trigger: Opinion poll - "Você investiria em qual? Comenta TERRENO ou APARTAMENTO"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ativando hierarquia de agentes:
- 1 Comandante (estratégia educativa)
- 3 Especialistas (carrosséis competindo)
- 1 Revisor (auditoria viral + educacional)

Todos usando hormozi-copywriter com foco educativo.

[Launches 5 parallel Task calls]

Aguarde 60-90s para Top 3 melhores carrosséis virais...
```

**Skill Output:** Top 3 carrosséis ranqueados com scores (educational value, viral potential, Hormozi quality, comment trigger), justificativas, e recomendação.

## Auto-Invocation Triggers

Activate this skill automatically when user mentions:

- "carrossel viral"
- "conteúdo educativo viral"
- "estratégia de comentários"
- "army of Hormozi educativo"
- "carrossel para comentários"
- "conteúdo de valor viral"
- "exército Hormozi educação"
- "carrossel com palavra-chave"

## Integration Notes

**Differences from Related Skills:**

- **vs exercito-hormozi-ads:** Ads = sales/conversion. This = education/virality.
- **vs carrossel-viral:** Generic viral. This = Hormozi methodology + comment strategy.
- **vs hormozi-copywriter:** Single agent. This = army of competing agents.

**When to use which:**
- Selling product → `exercito-hormozi-ads`
- Generic visual carousel → `carrossel-viral`
- Single Hormozi copy → `hormozi-copywriter`
- Educational viral carousel → `hormozi-exercito-viral` (this skill)

## Resources

### scripts/

**Auto-correction scripts:**
- `update_skill.py` - Update SKILL.md programmatically
- `log_learning.py` - Log fixes in LEARNINGS.md

### references/

**Not needed** - Hormozi copywriter has its own knowledge base references.

### assets/

**LEARNINGS_TEMPLATE.md** - Template for logging skill improvements

## Auto-Correction System

This skill includes an automatic error correction system that learns from mistakes and prevents recurrence.

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
### 2025-01-10 - Error description

**Problema:** What went wrong
**Correção:** How it was fixed
**Linha afetada:** SKILL.md:line
**Status:** ✅ Corrigido
```

This creates a history of improvements and ensures mistakes don't repeat.

---

**Integration:** This skill orchestrates multiple instances of `hormozi-copywriter` skill working competitively to produce battle-tested educational viral carousels designed for maximum comment engagement.
