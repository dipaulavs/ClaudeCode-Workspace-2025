# KB Generator - Examples

## Example 1: Technical Book

**Source:** "Clean Architecture" PDF (400 pages)

**Phase 1:**
```bash
python3 ~/.claude/skills/rag-novo/scripts/generate_kb.py \
  --name "clean-architecture" \
  --sources "Clean_Architecture.pdf" \
  --description "Complete book Clean Architecture by Robert C. Martin - software design principles, SOLID, component cohesion, dependency rule, layered architecture, boundaries. Use when user asks about clean architecture, software design patterns, SOLID principles, or mentions 'Uncle Bob' or 'Clean Architecture book'." \
  --analyze-only
```

**Claude Code Analysis:**
1. Identified structure: Book with Parts → Chapters → Sections
2. Created initial structure.json with 6 Parts
3. Validation found Part 3 oversized (15,000 tokens)
4. Subdivided Part 3 into 8 chapters
5. Re-validated - all sections ≤5000 tokens ✓

**Phase 2:**
```bash
python3 ~/.claude/skills/rag-novo/scripts/generate_kb.py \
  --name "clean-architecture" \
  --from-structure "~/.claude/skills/clean-architecture-analysis/structure.json"
```

**Result:** 42 semantic chunks preserving book structure

## Example 2: API Documentation

**Source:** Stripe API docs (Markdown)

**Phase 1:**
```bash
python3 ~/.claude/skills/rag-novo/scripts/generate_kb.py \
  --name "stripe-api-docs" \
  --sources "stripe-api.md" \
  --description "Stripe Payment API complete documentation - authentication, charges, customers, subscriptions, refunds, webhooks, payment intents, setup intents. Use when user asks about Stripe integration, payment processing, Stripe API endpoints, or mentions Stripe payments." \
  --analyze-only
```

**Claude Code Analysis:**
1. Identified structure: API Reference with resource groups
2. Found 5 major sections (Authentication, Payments, Customers, Subscriptions, Webhooks)
3. Payments section oversized (18,000 tokens)
4. Subdivided by endpoint (Create, List, Retrieve, Update, Delete)
5. Final validation ✓

**Result:** 23 semantic chunks organized by API resources

## Example 3: Legal Document

**Source:** Terms of Service (PDF)

**Phase 1:**
```bash
python3 ~/.claude/skills/rag-novo/scripts/generate_kb.py \
  --name "tos-legal" \
  --sources "terms_of_service.pdf" \
  --description "Company Terms of Service legal document - user agreements, liability limitations, intellectual property, dispute resolution, termination clauses, privacy policy. Use when user asks about terms of service, legal agreements, user rights, company policies, or mentions ToS." \
  --analyze-only
```

**Claude Code Analysis:**
1. Identified structure: Articles → Sections → Subsections
2. Used legal markers (Article 1, §1.1, etc.)
3. Created hierarchical structure preserving legal references
4. All sections already ≤5000 tokens (dense legal text)

**Result:** 15 chunks with complete legal context

## Example 4: Consulting Generated KB

After generating any KB, the skill is automatically available:

```
~/Desktop/ClaudeCode-Workspace/.claude/skills/clean-architecture/
├── SKILL.md
├── index.md
├── structure.json
├── metadata.json
└── chunks/
    ├── section_001.md
    ├── section_002.md
    └── ...
```

### Querying the KB

**Search by keyword:**
```bash
Grep pattern="dependency rule" path="~/.claude/skills/clean-architecture/chunks" output_mode="content" -C=3
```

**Browse index:**
```bash
Read file_path="~/.claude/skills/clean-architecture/index.md"
```

**Read specific section:**
```bash
Read file_path="~/.claude/skills/clean-architecture/chunks/section_003.md"
```

**Auto-activation:** Just mention the book name:
- "What does Clean Architecture say about dependencies?"
- "According to clean-architecture..."
- "Search clean architecture for layered design"
