# Orçamento Profissional - Skill

Generate professional budget proposals using value-based pricing methodology with ROI calculations, psychological pricing techniques, and persuasive HTML presentations.

## What This Skill Does

Automatically creates comprehensive budget proposals that:
- Price based on **value generated** (not hours worked)
- Calculate realistic **ROI scenarios** (conservative/realistic/optimistic)
- Apply **psychological pricing** (broken values ending in 7/9)
- Generate **professional HTML presentations** (MotherDuck design)
- Create **anchoring comparisons** (vs employee, vs manual, vs opportunity)

## When to Use

The skill auto-invokes when you ask Claude to:
- "Preciso fazer orçamento para [cliente/projeto]"
- "Quanto cobrar por [serviço]?"
- "Criar proposta para [projeto]"
- "Precificar [automação/sistema/etc]"

## Structure

```
orcamento-profissional/
├── SKILL.md                        # Main skill instructions (184 lines)
├── README.md                       # This file
├── scripts/
│   ├── calcular_precificacao.py   # Interactive pricing calculator
│   ├── update_skill.py            # Auto-correction: fix SKILL.md
│   └── log_learning.py            # Auto-correction: log fixes
├── references/
│   ├── metodologia.md             # Full pricing methodology (710 lines)
│   ├── examples.md                # 3 real-world examples
│   └── troubleshooting.md         # Common issues & solutions
└── assets/
    ├── template-proposta.html     # HTML presentation template
    └── LEARNINGS_TEMPLATE.md      # Auto-correction log template
```

## Quick Start

### 1. Using the Skill

Just ask Claude:
```
"Preciso fazer orçamento para automatizar WhatsApp de uma imobiliária"
```

Claude will:
1. Ask project details (scope, client, problem, expected result)
2. Map reusable resources from your codebase
3. Calculate value-based price
4. Generate HTML presentation
5. Provide anchoring comparisons and ROI calculations

### 2. Using the Calculator Directly

Run the pricing calculator:
```bash
python3 scripts/calcular_precificacao.py
```

Input monthly values:
- New revenue generated: R$ 10,000
- Cost savings: R$ 5,000
- Hours saved: 40h × R$ 50/h = R$ 2,000
- Opportunity cost: R$ 3,000

Output:
```
💰 RESULTADO DA PRECIFICAÇÃO

1️⃣ VALOR GERADO (ANO 1): R$ 240,000

2️⃣ PRECIFICAÇÃO SUGERIDA
   Preço base (5%): R$ 12,000
   Valor quebrado: R$ 11,997

3️⃣ ANCORAGEM COM DESCONTOS
   TABELA: R$ 16,391
   ├─ Desconto parceria: -R$ 2,637
   ├─ Desconto combo: -R$ 1,757
   └─ INVESTIMENTO FINAL: R$ 11,997 ⭐

4️⃣ ROI E PAYBACK
   ROI: 20x
   Payback: 18 dias
```

### 3. Customizing the HTML Template

Edit `assets/template-proposta.html` and replace placeholders:
- `[CLIENTE]` → Client name
- `[NOME DO PROJETO]` → Project name
- `[SEU NOME/EMPRESA]` → Your name
- `[DATA]` → Current date
- `[Dor específica X]` → Client pain points
- `[Benefício X]` → Solution benefits
- `[VALOR]` → Calculated prices
- etc.

Open in browser, press:
- `→` or click to advance/reveal items
- `←` to go back
- `F` for fullscreen

## Key Methodology

### Value-Based Pricing Formula

```
Fair Price = 2-10% of Year 1 Value Generated

Where:
- 2% = Commoditized, low complexity
- 5% = Custom, medium complexity (DEFAULT)
- 10% = Strategic, high complexity
```

### Psychological Pricing (Broken Values)

Always end prices in 7 or 9:
- ✅ R$ 5.997 (looks like "R$ 5 thousand")
- ❌ R$ 6.000 (looks expensive)

Create high anchor (+37%) with named discounts:
```
TABELA EMPRESAS: R$ 8.391
├─ Desconto parceria: -R$ 1.200
├─ Desconto combo: -R$ 1.194
└─ INVESTIMENTO: R$ 5.997 ⭐
```

### ROI Scenarios (Always Show 3)

```
🟢 Conservative (3x): Minimum guaranteed return
🟡 Realistic (5x): Expected market benchmark
🔵 Optimistic (10x): Best-case scenario
```

## Auto-Correction System

When errors occur:

```bash
# 1. Fix SKILL.md
python3 scripts/update_skill.py \
    /path/to/orcamento-profissional \
    "old text" \
    "new text"

# 2. Log the learning
python3 scripts/log_learning.py \
    /path/to/orcamento-profissional \
    "Error description" \
    "Fix applied" \
    "SKILL.md:line"
```

This creates/updates `LEARNINGS.md` with the fix, preventing future recurrence.

## Resources

### Full Documentation
- **Methodology:** `references/metodologia.md` (710 lines)
  - Value calculation formulas
  - Broken values technique (detailed)
  - Anchoring frameworks (Hormozi's Value Equation)
  - Named discounts psychology

- **Examples:** `references/examples.md`
  - WhatsApp automation for real estate (R$ 21,600)
  - Meta Ads lead system for dentist (R$ 10,000)
  - Instagram automation for infoproducer (R$ 25,000)

- **Troubleshooting:** `references/troubleshooting.md`
  - Common pricing mistakes
  - ROI calculation errors
  - Presentation issues

### Related Skills
- **hormozi-leads:** Value Equation, anchoring frameworks
- **visual-explainer:** MotherDuck design system
- **product-designer:** Professional UI/UX guidelines

## Version

**v2.0** - Improved with skill-creator2
- ✅ Auto-correction system added
- ✅ Progressive disclosure (SKILL.md → references/)
- ✅ Pricing calculator script
- ✅ HTML template included
- ✅ Imperative language throughout
- ✅ 184-line concise SKILL.md (vs 209 before)

## License

MIT - Created with skill-creator2
