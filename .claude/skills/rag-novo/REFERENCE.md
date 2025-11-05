# KB Generator - Technical Reference

## Architecture

The rag-novo skill uses a two-phase semantic analysis approach:

### Phase 1: Semantic Analysis
- Creates analysis workspace in `~/.claude/skills/{name}-analysis/`
- Generates `ANALYSIS_REQUEST.md` with instructions for Claude Code
- Claude Code performs iterative semantic analysis
- Creates `structure.json` with hierarchical document structure
- Validates all leaf sections are ≤5000 tokens
- Creates `SUBDIVISION_REQUEST.md` if oversized sections found

### Phase 2: Skill Generation
- Reads validated `structure.json`
- Extracts content using line number ranges
- Creates **MODEL-INVOKED** KB skill in `~/Desktop/ClaudeCode-Workspace/.claude/skills/{name}/`
- Creates hierarchical index and metadata
- Generates SKILL.md with model-invoked description
- **Auto-discovery:** Claude Code automatically discovers and activates skill based on description

## Model-Invoked Activation

All generated KBs are **model-invoked** skills. Claude Code automatically activates them based on:

1. **Description keywords:** Main topics, concepts, technologies mentioned
2. **Document name variations:** Different ways users might reference the document
3. **Context triggers:** "Use when..." clause in description
4. **Natural language:** User questions matching description content

**Example:**
```
description: "Complete book $100M Leads by Alex Hormozi - comprehensive guide
on lead generation (Core Four: warm outreach, content, cold outreach, paid ads)
and lead getters (referrals, employees, agencies, affiliates). Use when user
asks about lead generation strategies, Core Four methods, lead magnets,
advertising, or mentions '100M Leads' or 'Hormozi leads'."
```

**Triggers:**
- "Como funciona o Core Four?"
- "Me explica sobre lead generation do Hormozi"
- "O que 100M Leads fala sobre paid ads?"
- "Estratégias de warm outreach"

## structure.json Format

```json
{
  "document_info": {
    "type": "technical_documentation",
    "language": "en",
    "total_lines": 5000,
    "tokens_per_line": 2.3
  },
  "sections": [
    {
      "id": "section_001",
      "title": "Introduction",
      "start_line": 0,
      "end_line": 150,
      "semantic_type": "introduction",
      "children": []
    }
  ]
}
```

## Semantic Types

Common semantic types for sections:
- `title` - Document title/cover
- `introduction` - Introductory content
- `chapter` - Major division
- `section` - Mid-level division
- `subsection` - Detailed subdivision
- `procedure` - Step-by-step instructions
- `reference` - API/technical reference
- `appendix` - Supplementary material

## Token Calculation

The system automatically calculates tokens using document density:
- `tokens_per_line = total_tokens / total_lines`
- `estimated_tokens = (end_line - start_line) × tokens_per_line`

Claude Code does NOT need to manually count tokens.

## Validation Rules

1. All leaf sections must be ≤5000 tokens
2. Line ranges must not overlap
3. Line ranges must not have gaps
4. All sections must have valid `start_line` and `end_line`
5. Hierarchical IDs must follow pattern: `section_XXX` or `section_XXX_YYY`
