---
name: sobe-campanha-ads
description: Automate complete Meta Ads campaign creation with product input, strategy, copy, and creative assets. Auto-invokes when user requests to create/launch/upload Meta Ads campaigns, or mentions "subir campanha", "criar anúncio Meta", "campanha Facebook/Instagram". Integrates with hormozi-ads, exercito-hormozi-ads, and cria-carrossel skills for missing inputs. Applies standardized naming convention for campaigns, adsets, and creatives.
---

# Sobe Campanha Ads

## Overview

Automate the complete process of creating Meta Ads campaigns with a standardized naming system. This skill collects product information, marketing strategy, copy, and creative assets, then creates properly structured campaigns in Meta Ads following a consistent organizational framework.

## When to Use This Skill

Auto-invoke when user:
- Requests to create/launch/upload Meta Ads campaigns
- Says "subir campanha", "criar anúncio Meta", "campanha Facebook/Instagram"
- Wants to automate Meta Ads campaign creation
- Needs standardized campaign naming and organization

## Workflow Decision Tree

```
User requests campaign
    ↓
Collect 4 inputs ────> Missing strategy? ──YES──> Invoke hormozi-ads
    │                       │
    │                       NO
    │                       ↓
    │              Missing copy? ──YES──> Invoke exercito-hormozi-ads
    │                       │
    │                       NO
    │                       ↓
    │           Missing creatives? ──YES──> Invoke cria-carrossel
    │                       │
    │                       NO
    ↓                       ↓
All inputs collected ←──────┘
    ↓
Create campaign with naming system
    ↓
Campaign live ✅
```

## Step 1: Collect Campaign Inputs

Always start by collecting these 4 required inputs from the user:

### 1. Product Type (O que está vendendo?)

Ask: "O que você está vendendo nessa campanha?"

**Valid options:**
- **Lote** - Land lots, property parcels
- **Chácara** - Small farms, rural properties
- **Info produto** - Digital products, courses, ebooks
- **Produto lowticket** - Physical products under R$100

**Store as:** `product_type`

### 2. Campaign Strategy (Estratégia da campanha)

Ask: "Qual a estratégia dessa campanha?"

**If missing or unclear:**
```
User doesn't provide strategy
    ↓
Invoke skill: hormozi-ads
    ↓
Generate strategy based on product
    ↓
Present to user for approval
```

**Store as:** `campaign_strategy`

### 3. Ad Copy (Copy para o anúncio)

Ask: "Qual o copy/texto do anúncio?"

**If missing:**
```
User doesn't provide copy
    ↓
Invoke skill: exercito-hormozi-ads
    ↓
Generate 3 copy variations
    ↓
User selects preferred version
```

**Store as:** `ad_copy`

### 4. Creative Assets (Link dos criativos)

Ask: "Qual o link dos criativos? (imagens/vídeos/carrossel)"

**If missing:**
```
User doesn't provide creatives
    ↓
Invoke skill: cria-carrossel
    ↓
Generate carousel/creative assets
    ↓
Upload and get public URLs
```

**Store as:** `creative_urls` (array)

## Step 2: Apply Naming System

After collecting all inputs, apply the standardized naming convention:

### Campaign Name Format

```
{Produto} │ {Objetivo} - {Conversão} │ {Dia/Mês}
```

**Example:**
```
Lote Residencial │ engajamento - Wpp │ 15/01
Chácara Premium │ conversão - Lead │ 20/02
Curso Copy │ tráfego - DM │ 10/03
```

**Components:**
- `{Produto}` - Product name/type from input
- `{Objetivo}` - Campaign objective (engajamento, conversão, tráfego)
- `{Conversão}` - Conversion type (Wpp, Lead, DM, Site)
- `{Dia/Mês}` - Launch date (DD/MM format)

### Adset Name Format

```
{Localização} │ {Interesses} │ {Qtd criativos}
```

**Example:**
```
SP Capital │ imóveis+investimento │ 3 criativos
BR Nacional │ empreendedorismo │ 5 criativos
RJ+SP │ luxo+alto-padrão │ 2 criativos
```

**Components:**
- `{Localização}` - Geographic targeting (city, state, or country)
- `{Interesses}` - Audience interests (comma-separated)
- `{Qtd criativos}` - Number of creatives in adset

### Creative Name Format

```
{ID} │ {Formato} │ {CPC}
```

**Example:**
```
001 │ reels │ R$0.45
002 │ carrossel │ R$0.32
003 │ único │ R$0.58
```

**Components:**
- `{ID}` - Sequential creative ID (001, 002, 003...)
- `{Formato}` - Creative format (reels, carrossel, único, stories)
- `{CPC}` - Cost per click (if available, otherwise "R$-")

## Step 3: Create Campaign via Meta Ads API

### Prerequisites

Ensure Meta Ads credentials are configured:

**Check credentials location:**
```bash
# 1. Check Cofre de APIs in Obsidian
cat ~/Documents/Obsidian/Claude-code-ios/🔐\ Credenciais/🔑\ Cofre\ de\ APIs.md | grep -A 10 "Meta Ads"

# 2. Check environment variables
echo $META_ADS_ACCESS_TOKEN
echo $META_ADS_ACCOUNT_ID
```

**If credentials missing:**
- Consult `references/meta_ads_setup.md` for authentication flow
- Use script: `scripts/configure_meta_ads.py`

### Create Campaign Structure

Execute campaign creation using the Meta Marketing API:

```python
# Use script: scripts/create_campaign.py
python3 scripts/create_campaign.py \
    --product-type "lote" \
    --strategy "engajamento para WhatsApp" \
    --copy "copy_file.txt" \
    --creatives "url1,url2,url3" \
    --location "SP Capital" \
    --interests "imóveis,investimento" \
    --date "15/01"
```

**Script will:**
1. Create campaign with formatted name
2. Create adset with targeting and formatted name
3. Create ads for each creative with formatted names
4. Return campaign ID and preview URLs

### Campaign Creation Flow

```
scripts/create_campaign.py
    ↓
┌─────────────────────────────────────┐
│ 1. Validate inputs and credentials  │
│ 2. Format campaign name             │
│ 3. Create campaign via API          │
│ 4. Format adset name                │
│ 5. Create adset with targeting      │
│ 6. Format creative names (001, 002) │
│ 7. Create ads for each creative     │
│ 8. Return campaign URLs             │
└─────────────────────────────────────┘
    ↓
Campaign live ✅
```

## Step 4: Verify Campaign

After creation, verify the campaign structure:

```bash
# Use script: scripts/verify_campaign.py
python3 scripts/verify_campaign.py --campaign-id <campaign_id>
```

**Verification checklist:**
- ✅ Campaign name follows format: `{Produto} │ {Objetivo} - {Conversão} │ {Dia/Mês}`
- ✅ Adset name follows format: `{Localização} │ {Interesses} │ {Qtd criativos}`
- ✅ Creative names follow format: `{ID} │ {Formato} │ {CPC}`
- ✅ All creatives uploaded and active
- ✅ Targeting configured correctly

## Example Complete Workflow

**User request:** "Subir campanha para lote residencial"

**Step 1 - Collect inputs:**
```
Assistant: "O que você está vendendo nessa campanha?"
User: "Lote residencial de 300m²"
Assistant: "Qual a estratégia dessa campanha?"
User: [não responde]
Assistant: [Invokes hormozi-ads skill to generate strategy]
Assistant: "Gerada estratégia: engajamento para WhatsApp. Aprova?"
User: "Sim"Assistant: "Qual o copy do anúncio?"
User: [não responde]
Assistant: [Invokes exercito-hormozi-ads skill]
Assistant: "3 copys geradas. Qual prefere? (1/2/3)"
User: "A 2"Assistant: "Link dos criativos?"
User: [não responde]
Assistant: [Invokes cria-carrossel skill]
Assistant: "Carrossel gerado. URLs: url1, url2, url3"
```

**Step 2 - Apply naming:**
```
Product: "Lote Residencial"
Strategy: "engajamento para WhatsApp"
Date: "15/01"

Campaign name: "Lote Residencial │ engajamento - Wpp │ 15/01"
Adset name: "SP Capital │ imóveis+investimento │ 3 criativos"
Creative names:
  - "001 │ carrossel │ R$-"
  - "002 │ carrossel │ R$-"
  - "003 │ carrossel │ R$-"
```

**Step 3 - Create campaign:**
```bash
python3 scripts/create_campaign.py \
    --product-type "lote" \
    --strategy "engajamento para WhatsApp" \
    --copy "copy_v2.txt" \
    --creatives "url1,url2,url3" \
    --location "SP Capital" \
    --interests "imóveis,investimento" \
    --date "15/01"
```

**Step 4 - Verify:**
```bash
python3 scripts/verify_campaign.py --campaign-id 120123456789
✅ Campaign: Lote Residencial │ engajamento - Wpp │ 15/01
✅ Adset: SP Capital │ imóveis+investimento │ 3 criativos
✅ Creatives: 001 │ carrossel │ R$-  (3 total)
✅ Campaign live!
```

## Resources

### scripts/

**create_campaign.py** - Main script to create Meta Ads campaigns with standardized naming
**verify_campaign.py** - Verify campaign structure follows naming conventions
**configure_meta_ads.py** - Configure Meta Ads API credentials
**update_skill.py** - Auto-correction: update SKILL.md programmatically
**log_learning.py** - Auto-correction: log fixes in LEARNINGS.md

### references/

**meta_ads_setup.md** - Complete Meta Marketing API authentication and setup guide
**api_reference.md** - Meta Marketing API endpoints and parameters reference
**targeting_options.md** - Available targeting options for locations and interests

### assets/

**LEARNINGS_TEMPLATE.md** - Template for logging auto-corrections

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
