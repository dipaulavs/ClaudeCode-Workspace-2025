---
name: army-of-agents
description: Orchestrate multiple specialized AI agents to produce high-quality creative content through iterative feedback. Auto-invokes when user requests content requiring multiple perspectives, high quality output, or mentions "multiple agents", "army of agents", or creative tasks like hooks, headlines, landing pages, email sequences, or video scripts.
---

# Army of Agents

## Purpose

Orchestrate multiple specialized AI agents (Researcher, Copywriter, Critic, Director, etc.) to produce creative content through multi-perspective iteration and feedback. Each agent contributes their expertise, critiques others' work, and refines output until high-quality results are achieved.

## When to Use

Auto-invoke when user requests:
- Content requiring multiple perspectives or high quality
- Mentions "army of agents", "multiple agents", or "several perspectives"
- Creative tasks: hooks, headlines, CTAs, landing pages, email sequences, video scripts, proposals

Do NOT use for:
- Simple/trivial tasks
- First drafts only
- Internal copy (non-sales)
- Tight deadlines (<5min)

## How to Use

### 1. Analyze Task

Determine:
- Objective (hook, landing page, email, etc.)
- Required knowledge (market research, frameworks, data)
- Number of perspectives needed (3-5 roles)
- Execution order (parallel vs sequential)

### 2. Select Roles

Choose 3-5 roles from library in `references/roles.md`:
- Researcher, Copywriter, Critic Hormozi, Director, Revisor, Strategist, Content Designer

### 3. Execute Multi-Agent Flow

Launch agents using Task tool with `subagent_type: "general-purpose"`:

```
Round 1: Initial execution (parallel when possible)
Round 2: Feedback + refinement
Round 3: Final approval (if needed)
```

**Limit:** Maximum 3 rounds (prevents infinite loops)

### 4. Show Process to User

Always display:
- Roles activated
- Process summary (what each agent did)
- Iterations (feedback + changes)
- Final result

## Bundled Resources

- **references/roles.md** - Role library with prompts (Researcher, Copywriter, Critic, etc.)
- **references/flows.md** - Recommended workflows for common tasks
- **references/examples.md** - Complete examples with inputs/outputs/timings
- **assets/role_prompts/** - Pre-built prompt templates for each role

## Cost & Time

| Task | Roles | Iterations | Cost | Time |
|------|-------|------------|------|------|
| Hook | 3 | 1 | ~$0.03 | 2min |
| Landing page | 5 | 2 | ~$0.10 | 5min |
| Email sequence | 4 | 2 | ~$0.08 | 4min |
| Video script | 6 | 3 | ~$0.15 | 8min |

## Auto-Correction

When errors occur in this skill:

```bash
# 1. Fix SKILL.md
python3 scripts/update_skill.py "<old-text>" "<new-text>"

# 2. Log learning
python3 scripts/log_learning.py "<error>" "<fix>" "[line]"
```

See `LEARNINGS.md` for fix history.
