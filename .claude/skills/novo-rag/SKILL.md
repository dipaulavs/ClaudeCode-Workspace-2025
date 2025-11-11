---
name: novo-rag
description: Generate semantically-structured knowledge base skills from documents using Claude Code's analysis. Creates discoverable, hierarchically-organized knowledge bases from PDF, Markdown, and text files. Use when the user wants to create a knowledge base that preserves logical document structure.
---

# Knowledge Base Generator Skill

Generate knowledge bases using **semantic analysis** rather than mechanical chunking. Analyze document structure and create chunks based on logical boundaries, preserving the document's natural organization.

## Two-Phase Process

### Phase 1: Semantic Analysis (Iterative)

Create analysis workspace and perform semantic analysis:

```bash
python3 ~/.claude/skills/novo_rag/scripts/generate_kb.py \
  --name "kb-name" \
  --sources "path/to/document.pdf" \
  --description "Description of the knowledge base" \
  --analyze-only
```

**This creates:**
- Analysis workspace at `~/.claude/skills/kb-name-analysis/`
- `ANALYSIS_REQUEST.md` with instructions
- `samples/` directory with extracted source text

**Then (Claude Code):**

1. **Read ANALYSIS_REQUEST.md** for complete instructions
2. **Read source documents** from `samples/` directory
3. **Perform progressive refinement analysis:**
   - Identify document type and language
   - Find major structural divisions using Grep with `-n` flag
   - Extract line numbers for section boundaries
   - Recursively identify subdivisions
   - Create `structure.json` with hierarchical structure
4. **Automatic validation:** System checks all leaf sections are ≤5000 tokens
5. **Iterative subdivision (if needed):**
   - If oversized sections found, system creates `SUBDIVISION_REQUEST.md`
   - Read subdivision request for details
   - For each oversized section:
     - Extract section content using line numbers
     - Identify semantic subdivisions
     - Update `structure.json` by adding `children` array
   - Re-run with `--analyze-only` to validate
   - **Repeat until all leaf sections are ≤5000 tokens**

### Phase 2: Skill Generation

Generate final skill from validated structure:

```bash
python3 ~/.claude/skills/novo_rag/scripts/generate_kb.py \
  --name "kb-name" \
  --from-structure "~/.claude/skills/kb-name-analysis/structure.json"
```

**This generates:**
- Complete skill at `~/.claude/skills/kb-name/`
- `SKILL.md` with skill metadata
- `index.md` with hierarchical table of contents
- `metadata.json` with chunk metadata
- `chunks/` directory with semantic sections

**Note:** Phase 2 also validates and creates subdivision requests if oversized sections are found. Can either:
- Proceed with generation (accepts warning, may have oversized chunks)
- Or update `structure.json` and re-run Phase 2 with refined subdivisions

Both phases support iterative subdivision - use whichever fits the workflow.

## Parameters

- `--name`: Knowledge base skill name (lowercase, hyphens only, max 64 chars)
- `--sources`: Comma-separated paths to source documents (PDF, MD, TXT)
- `--description`: What this knowledge base contains (max 1024 chars)
- `--analyze-only`: Phase 1 - perform semantic analysis only (flag)
- `--from-structure`: Phase 2 - generate from existing structure.json
- `--max-chunk-tokens`: Target tokens per chunk (default 5000, flexible for semantics)

## Generated Structure

```
kb-name/
├── SKILL.md                    # Main skill file (auto-discoverable)
├── index.md                    # Hierarchical table of contents
├── structure.json              # Complete semantic analysis
├── metadata.json               # Chunk metadata
└── chunks/                     # Semantic sections
    ├── section_001.md          # First major section
    ├── section_002.md          # Second major section
    ├── section_002_001.md      # Subsection of section_002
    └── ...
```

**Each chunk contains:**
- Hierarchical path (breadcrumb)
- Semantic type (chapter, article, procedure, etc.)
- Actual token count
- Complete section content

## Features

- **Hierarchical structure:** Preserves document's logical organization
- **Semantic boundaries:** Chunks follow meaning, not token counts
- **Context preservation:** Each section knows its place in hierarchy
- **Type classifications:** Sections tagged by semantic purpose
- **Token-optimized:** Aims for ~5000 tokens but prioritizes completeness
- **Iterative subdivisions:** Automatic detection and guided subdivision
- **Line number precision:** Uses line ranges for 100% accurate extraction
- **Automatic token estimation:** Calculates estimated tokens based on document density

## Semantic Analysis Guidelines

When performing semantic analysis:

1. **Sample first:** Read beginning, middle, end to understand document type
2. **Identify top level:** Find major structural markers using Grep with `-n` flag
   - Example: `Grep(pattern="^chapter|^# ", output_mode="content", -n=True)`
   - Extract line numbers from output for `start_line` and `end_line`
3. **Use line numbers:** Store section boundaries as line numbers (0-indexed)
   - Line numbers eliminate marker ambiguity
   - More precise than text markers
   - Optional: Include `start_marker` field for human reference
4. **Token estimation is automatic:** DO NOT calculate `estimated_tokens`
   - System automatically calculates based on document density (tokens/line)
   - Formula: `(end_line - start_line) × tokens_per_line`
   - Only provide `start_line` and `end_line`
5. **Recursive subdivisions:** For large sections, find logical subsections
   - ⚠️ Keep subdividing until ALL leaf sections are ≤5000 tokens
   - Don't stop at first-level subdivision if sections are still oversized
6. **Semantic boundaries:** Split based on meaning and document structure
7. **Atomic sections:** Stop when sections are complete units
8. **Validate chunk sizes:**
   - Review each leaf section against ~5000 token target
   - Subdivide oversized sections further
   - Store atomic sections that cannot be split (in analyzer_notes)
9. **Final validation:** Ensure no gaps or overlaps in line ranges

## Example Workflow

**Creating an API documentation knowledge base:**

```bash
# Phase 1: Start semantic analysis
python3 ~/.claude/skills/novo_rag/scripts/generate_kb.py \
  --name "payment-api-docs" \
  --sources "payment-api-documentation.pdf" \
  --description "Complete API documentation for payment processing platform" \
  --analyze-only
```

**Initial Analysis (Claude Code):**

1. Read `ANALYSIS_REQUEST.md`
2. Read documentation from `samples/` directory
3. Identify structure:
   - Document type: technical_documentation
   - Language: en
   - Major sections: Introduction, Authentication, Core Concepts, API Reference
   - Subsections: Endpoints grouped by resource
4. Create initial `structure.json`

**Automatic validation detects oversized sections** → Creates `SUBDIVISION_REQUEST.md`

**Iterative Subdivision (Claude Code):**

5. Read `SUBDIVISION_REQUEST.md` (lists oversized sections)
6. For each oversized section (e.g., "API Reference - Payments" with 12,000 tokens):
   - Extract full section content
   - Identify logical subdivisions: Create Payment, List Payments, etc.
   - Group related endpoints semantically
   - Update `structure.json` with `children` array
7. Re-run to validate: `python3 ... --analyze-only`
8. Repeat until all sections ≤5000 tokens ✓

```bash
# Phase 2: Generate the skill
python3 ~/.claude/skills/novo_rag/scripts/generate_kb.py \
  --name "payment-api-docs" \
  --from-structure "~/.claude/skills/payment-api-docs-analysis/structure.json"
```

**Result:** Semantically-organized knowledge base following the documentation's natural hierarchical structure, with all sections properly sized.

## Structure Format

**structure.json format:**

```json
{
  "metadata": {
    "name": "payment-api-docs",
    "description": "Complete API documentation",
    "document_type": "technical_documentation",
    "language": "en",
    "created": "2025-01-07T10:30:00",
    "tokens_per_line": 12.5
  },
  "sections": [
    {
      "id": "001",
      "title": "Introduction",
      "type": "chapter",
      "start_line": 0,
      "end_line": 150,
      "start_marker": "# Introduction"
    },
    {
      "id": "002",
      "title": "API Reference",
      "type": "chapter",
      "start_line": 150,
      "end_line": 2000,
      "start_marker": "# API Reference",
      "children": [
        {
          "id": "002_001",
          "title": "Payments",
          "type": "section",
          "start_line": 150,
          "end_line": 800
        },
        {
          "id": "002_002",
          "title": "Customers",
          "type": "section",
          "start_line": 800,
          "end_line": 1400
        }
      ]
    }
  ]
}
```

## Dependencies

- Python 3.6+
- PyPDF2 (for PDF extraction): `pip install PyPDF2`

## Resources

### scripts/

- **generate_kb.py** - Main script for creating knowledge base skills
- **update_skill.py** - Auto-correction script to update SKILL.md
- **log_learning.py** - Auto-correction script to log fixes in LEARNINGS.md

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
