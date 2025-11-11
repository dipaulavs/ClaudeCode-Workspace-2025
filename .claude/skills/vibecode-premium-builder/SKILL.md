---
name: vibecode-premium-builder
description: Generate complete VibeCode prompts and backend plans for iOS apps. Auto-invokes when user requests creating iOS apps, replicating existing apps, or needs native iOS UI components (Large Headers, Context Menus, Bottom Sheets, Date Pickers, Switches, Haptics). Always consults official VibeCode docs first, then produces sequential prompts + backend architecture.
---

# VibeCode Premium Builder

## Purpose

Generate production-ready iOS app plans with VibeCode prompts and backend architecture. This skill transforms app ideas into structured implementation plans using native iOS components and modern patterns.

## When to Use

Auto-invoke when user requests:
- Creating iOS apps from ideas
- Replicating existing apps
- Adding native iOS components to projects

## Core Workflow

### Step 0: Fetch Official Documentation (MANDATORY)

ALWAYS start by consulting current VibeCode documentation:

```
WebFetch(https://vibecodeapp.com/docs/prompting/native-ui-components)
↓
Extract EXACT prompts for components needed
↓
Adapt ONLY context-specific variables (screen names, items, etc.)
❌ NEVER invent prompt structure
✅ ALWAYS use official documentation text
```

**Rationale:** Documentation updates frequently. Exact prompts ensure reliability.

### Step 1: Detect Scenario

```
User mentions creating OR replicating app?
├─ CREATE NEW → Scenario A
└─ REPLICATE → Scenario B (ask method)
```

### Scenario A: Create from Scratch

1. Fetch documentation (Step 0)
2. Analyze idea (purpose, main features)
3. Generate sequential VibeCode prompts using exact docs:
   - Base structure + tabs (if multi-screen)
   - Large Headers (copy exact prompt + adapt screen name)
   - Context Menus (copy exact + adapt menu items)
   - Bottom Sheets (copy exact + adapt snap points)
   - Date/Time Pickers (copy exact + adapt mode)
   - Switches (copy exact)
   - Haptics (manual instructions, not prompt)
4. Plan backend: endpoints, schema, auth
5. Present complete plan

### Scenario B: Replicate Existing App

1. Fetch documentation (Step 0)
2. Ask analysis method:
   - 📸 Screenshot
   - 🔗 App Store link
   - 🎥 YouTube demo
   - 🌐 Website/Landing page

3. Process based on method:
   - Screenshots: analyze layout, colors, components
   - App Store: WebFetch official screenshots
   - YouTube: transcribe demo video
   - Website: invoke `website-cloner` skill → extract design system → adapt web to iOS

4. Generate VibeCode prompts (exact docs + design adaptation)
5. Plan backend (same as Scenario A)

For detailed analysis methods, consult `references/analysis-methods.md`.

## Premium Features to Include

Always apply all 7 iOS premium elements:

1. Large Headers (scroll animation)
2. Context Menus (long-press)
3. Bottom Tab Bar (multi-screen apps)
4. Bottom Sheets (sliding modals)
5. Date/Time Pickers (when handling dates)
6. Liquid Glass Switches (native toggles)
7. Haptics (tactical feedback)

## Output Format

Deliver structured plan with:

```
✅ [APP NAME] VibeCode Premium Plan

📱 FRONTEND (VibeCode):
  Prompt 1: [base structure]
  Prompt 2: [large headers]
  Prompt 3: [context menus]
  Prompt 4: [bottom sheets]
  Prompt 5: [switches + haptics]

🔧 BACKEND (Claude Code):
  Endpoints: [list]
  Database: [schema]
  Auth: [method]

🎯 Next Steps:
  1. Paste prompts in VibeCode (sequential order!)
  2. Wait for frontend completion
  3. Confirm to build backend
```

## Using Bundled Resources

### References

- `references/prompts-library.md` - Complete prompt templates with latest updates
- `references/backend-framework.md` - Standard backend architecture patterns
- `references/analysis-methods.md` - Detailed app analysis techniques
- `references/troubleshooting.md` - Common issues and solutions

Load references when:
- Generating specific component prompts → read `prompts-library.md`
- Planning backend → read `backend-framework.md`
- Analyzing existing apps → read `analysis-methods.md`
- Debugging issues → read `troubleshooting.md`

### Scripts

Execute auto-correction scripts when errors occur:

```bash
# Update SKILL.md with corrections
python3 scripts/update_skill.py "old_text" "new_text"

# Log learning to prevent recurrence
python3 scripts/log_learning.py "error" "fix" "location"
```

## Auto-Correction System

When VibeCode prompts fail or produce unexpected results:

1. Identify what went wrong
2. Update SKILL.md: `python3 scripts/update_skill.py <old> <new>`
3. Log learning: `python3 scripts/log_learning.py <error> <fix> [line]`
4. Error prevented in future executions

All corrections are logged in `LEARNINGS.md` for continuous improvement.

## Integration

- **website-cloner skill**: Auto-invoke when user provides website URL (Scenario B, Method 4)
- **VibeCode docs**: https://vibecodeapp.com/docs/prompting/native-ui-components

## Notes

- Prompts must be applied in sequential order
- Haptics are configured manually in VibeCode UI (not via prompt)
- Backend planning uses standard REST patterns (see `references/backend-framework.md`)
- Always check documentation for latest prompt syntax
