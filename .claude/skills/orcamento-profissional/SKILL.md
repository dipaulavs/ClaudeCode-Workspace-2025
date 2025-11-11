---
name: orcamento-profissional
description: Generate professional budget proposals with value-based pricing, ROI calculations, and persuasive HTML presentations. Auto-invokes when user asks to create budgets, price projects, or needs pricing strategy for client work.
---

# Orçamento Profissional

Generate professional budget proposals using value-based pricing (not time-based) with ROI calculations, psychological pricing, and persuasive HTML presentations.

## When to Use

Auto-invoke when user:
- "Preciso fazer orçamento para [cliente/projeto]"
- "Quanto cobrar por [serviço]?"
- "Criar proposta para [projeto]"
- "Precificar [automação/sistema/etc]"

## Workflow (5 Steps)

### Step 1: Collect Project Data

Ask user to provide:
1. **Project scope:** What will be delivered?
2. **Client context:** Industry, size, current situation
3. **Current problem:** What pain does client have today?
4. **Expected result:** What transformation/value will be generated?
5. **Required processes:** What technical steps are needed?

### Step 2: Map Available Resources

Analyze codebase automatically to identify reusable assets:

```bash
# Search for relevant scripts
grep -r "keyword" scripts/*/README.md

# List applicable skills
ls .claude/skills/ | grep "keyword"

# Find low-level tools
ls tools/ | grep "keyword"
```

Categorize effort:
- ✅ **Green (0-20%):** Ready to use, only config needed
- 🟡 **Yellow (20-50%):** Exists but needs adaptation
- 🔴 **Red (50-100%):** Build from scratch

Present mapping to user showing what's reusable vs what needs building.

### Step 3: Calculate Value-Based Price

Use pricing calculator script:

```bash
python3 scripts/calcular_precificacao.py
```

The script guides through:
1. Monthly revenue generated for client
2. Monthly cost savings
3. Time saved (hours × client's hourly value)
4. Opportunity cost avoided

**Pricing formula:**
```
Fair Price = 2-10% of Year 1 Value Generated

Where:
- 2% = Commoditized, low complexity
- 5% = Custom, medium complexity (DEFAULT)
- 10% = Strategic, high complexity
```

Apply **psychological pricing** (broken values):
- Always end in 7 or 9 (R$ 5.997, not R$ 6.000)
- Create high anchor (+37%) with named discounts
- See `references/metodologia.md` for full technique

### Step 4: Generate HTML Presentation

Use template from `assets/template-proposta.html` with 10 slides:

1. **Cover** → Project title + client name
2. **Current Situation** → 4 specific pain points
3. **Proposed Solution** → 6 benefits/deliverables
4. **How It Works** → Process flow diagram
5. **Resources** → Show reusable assets (builds trust)
6. **Timeline** → Realistic delivery schedule
7. **Investment** → Price with anchoring comparisons
8. **ROI** → 3 scenarios (conservative/realistic/optimistic)
9. **What's Included** → Guarantees, support, training
10. **Next Steps** → Clear CTA

Template features:
- Progressive reveal animations (click to show items)
- MotherDuck design (beige + yellow + dark gray)
- Keyboard navigation (→ next, ← prev, F fullscreen)
- Investment slide reveals price in 10 steps (yellow box last!)

### Step 5: Create Realistic Anchoring

Apply Hormozi's Value Equation frameworks from `hormozi-leads` skill:

**Investment slide must include:**
```
💰 Investment: R$ 5.997

Realistic Comparisons:
├─ Vs Hire employee: Save R$ 36k/year
├─ Vs Manual work: Free 960h/year
└─ Vs Miss opportunity: Avoid losing R$ 80k/year

Payback: 27 days 📈
```

**ROI slide must show 3 scenarios:**
```
🟢 Conservative (3x): R$ 5.997 → R$ 18k return
🟡 Realistic (5x): R$ 5.997 → R$ 30k return
🔵 Optimistic (10x): R$ 5.997 → R$ 60k return
```

**NEVER exaggerate:** Use real data, research, market benchmarks.

## Output Format

```
✅ Professional Budget Created!

📊 Presentation: orcamento_[client]_[project].html
💰 Suggested price: R$ 5.997 (ROI 50x)
🎯 Anchoring: Vs Employee, Vs Manual, Vs Opportunity

🎬 Next steps:
  1. Open HTML in browser (F = fullscreen)
  2. Review slides (arrow keys ← →)
  3. Schedule video call with client
  4. Present with confidence!

Good luck! 🚀
```

## Golden Rules

### ✅ ALWAYS:
- Price by VALUE (not by time/hour)
- Map existing resources BEFORE estimating effort
- Calculate realistic ROI (don't exaggerate)
- Use MotherDuck template for visual consistency
- Create mathematical anchors (comparisons)
- Show 3 scenarios (conservative/realistic/optimistic)
- Apply broken values (ending in 7 or 9)

### ❌ NEVER:
- Charge by hour (employee mindset)
- Ignore available scripts/skills when estimating
- Exaggerate ROI (maintain credibility)
- Create ugly/generic presentation
- Forget guarantees slide
- Leave price without context (always anchor)

## Resources

- **Full methodology:** `references/metodologia.md`
- **Real examples:** `references/examples.md`
- **Troubleshooting:** `references/troubleshooting.md`
- **Pricing calculator:** `scripts/calcular_precificacao.py`
- **HTML template:** `assets/template-proposta.html`

## Auto-Correction System

When errors occur in this skill:

```bash
# 1. Fix SKILL.md
python3 scripts/update_skill.py /path/to/skill "old text" "new text"

# 2. Log learning
python3 scripts/log_learning.py /path/to/skill "error desc" "fix desc" "line"
```

See `assets/LEARNINGS_TEMPLATE.md` for format. This prevents repeating same mistakes.
