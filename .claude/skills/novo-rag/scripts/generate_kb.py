#!/usr/bin/env python3
"""
Knowledge Base Generator - Semantic Analysis Mode
Creates semantically-structured knowledge bases from documents.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

def count_tokens(text):
    """Estimate tokens (rough approximation: 1 token ≈ 4 chars)"""
    return len(text) // 4

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyPDF2"""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        print("⚠️  PyPDF2 not installed. Install with: pip install PyPDF2")
        sys.exit(1)

def extract_text_from_file(file_path):
    """Extract text from supported file formats"""
    ext = Path(file_path).suffix.lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['.md', '.txt']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"❌ Unsupported file format: {ext}")
        sys.exit(1)

def calculate_tokens_per_line(text):
    """Calculate average tokens per line for automatic token estimation"""
    lines = text.split('\n')
    total_tokens = count_tokens(text)
    total_lines = len(lines)
    return total_tokens / total_lines if total_lines > 0 else 0

def create_analysis_workspace(name, sources, description):
    """Phase 1: Create analysis workspace and ANALYSIS_REQUEST.md"""

    # Create workspace directory
    workspace_dir = Path.home() / ".claude" / "skills" / f"{name}-analysis"
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # Create samples directory
    samples_dir = workspace_dir / "samples"
    samples_dir.mkdir(exist_ok=True)

    # Copy source documents to samples
    for source in sources:
        source_path = Path(source).expanduser()
        if not source_path.exists():
            print(f"❌ Source not found: {source}")
            sys.exit(1)

        # Extract text and save as markdown
        text = extract_text_from_file(source_path)
        sample_file = samples_dir / f"{source_path.stem}.md"

        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"✅ Extracted: {sample_file}")

    # Calculate tokens per line (for automatic estimation)
    all_text = ""
    for md_file in samples_dir.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            all_text += f.read()

    tokens_per_line = calculate_tokens_per_line(all_text)

    # Create ANALYSIS_REQUEST.md
    analysis_request = f"""# Semantic Analysis Request

**Knowledge Base Name:** {name}
**Description:** {description}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Source Documents

{chr(10).join([f"- {Path(s).name}" for s in sources])}

All source documents have been extracted to: `{samples_dir}/`

## Document Density

**Tokens per line:** {tokens_per_line:.2f}

This metric is used for automatic token estimation. You DO NOT need to calculate `estimated_tokens` manually.
The system will automatically calculate: `(end_line - start_line) × {tokens_per_line:.2f}`

## Your Task (Claude Code)

Perform semantic analysis to create a hierarchical structure for this knowledge base:

### Step 1: Initial Analysis

1. Read the source documents from `samples/` directory
2. Identify document type and language
3. Find major structural divisions using Grep with `-n` flag:
   ```python
   # Example: Find chapters, sections, articles
   rg(pattern="^chapter|^# ", output_mode="content", -n=True)
   ```
4. Extract line numbers from Grep output for `start_line` and `end_line`
5. Create initial `structure.json` with major sections

### Step 2: Structure Format

Create `structure.json` with this format:

```json
{{
  "metadata": {{
    "name": "{name}",
    "description": "{description}",
    "document_type": "technical_documentation|legal_document|book|article|...",
    "language": "en|pt|es|...",
    "created": "{datetime.now().isoformat()}",
    "tokens_per_line": {tokens_per_line:.2f}
  }},
  "sections": [
    {{
      "id": "001",
      "title": "Section Title",
      "type": "chapter|section|article|procedure|...",
      "start_line": 0,
      "end_line": 150,
      "start_marker": "# Chapter 1",
      "children": [
        {{
          "id": "001_001",
          "title": "Subsection Title",
          "type": "subsection|paragraph|...",
          "start_line": 10,
          "end_line": 50
        }}
      ]
    }}
  ]
}}
```

### Step 3: Line Numbers (Critical)

- **Use Grep with `-n` flag** to get line numbers
- Store boundaries as `start_line` and `end_line` (0-indexed)
- Line numbers eliminate marker ambiguity
- Optional: Include `start_marker` for human reference
- **DO NOT calculate `estimated_tokens`** - System does this automatically

### Step 4: Subdivision Strategy

- Aim for leaf sections ≤5000 tokens
- Use semantic boundaries (chapters, sections, procedures)
- Subdivide recursively if needed
- Add `children` array for subsections
- Keep subdividing until ALL leaf sections are ≤5000 tokens

### Step 5: Save Structure

Save your analysis to: `{workspace_dir / 'structure.json'}`

Then re-run with `--analyze-only` to validate. System will:
- Automatically calculate token estimates
- Check all leaf sections are ≤5000 tokens
- Create SUBDIVISION_REQUEST.md if oversized sections found

## Validation

After creating structure.json, run:

```bash
python3 ~/.claude/skills/novo_rag/scripts/generate_kb.py \\
  --name "{name}" \\
  --from-structure "{workspace_dir / 'structure.json'}" \\
  --analyze-only
```

The system will validate and guide you through any needed subdivisions.
"""

    request_file = workspace_dir / "ANALYSIS_REQUEST.md"
    with open(request_file, 'w', encoding='utf-8') as f:
        f.write(analysis_request)

    print(f"\n✅ Analysis workspace created: {workspace_dir}")
    print(f"✅ Read this file: {request_file}")
    print(f"\n📋 Next steps:")
    print(f"1. Read ANALYSIS_REQUEST.md")
    print(f"2. Analyze documents in samples/")
    print(f"3. Create structure.json")
    print(f"4. Re-run with --analyze-only to validate")

def validate_structure(structure_path, max_chunk_tokens=5000):
    """Validate structure.json and check for oversized sections"""

    with open(structure_path, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    tokens_per_line = structure['metadata'].get('tokens_per_line', 1.0)
    oversized = []

    def check_section(section, path=""):
        section_path = f"{path}/{section['title']}" if path else section['title']

        if 'children' in section and section['children']:
            # Has children - check them recursively
            for child in section['children']:
                check_section(child, section_path)
        else:
            # Leaf section - check size
            start_line = section.get('start_line', 0)
            end_line = section.get('end_line', 0)
            estimated_tokens = int((end_line - start_line) * tokens_per_line)

            if estimated_tokens > max_chunk_tokens:
                oversized.append({
                    'path': section_path,
                    'id': section.get('id', 'unknown'),
                    'start_line': start_line,
                    'end_line': end_line,
                    'estimated_tokens': estimated_tokens,
                    'lines': end_line - start_line
                })

    for section in structure.get('sections', []):
        check_section(section)

    return oversized

def create_subdivision_request(structure_path, oversized_sections):
    """Create SUBDIVISION_REQUEST.md for oversized sections"""

    workspace_dir = Path(structure_path).parent

    subdivision_request = f"""# Subdivision Request

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Structure:** {structure_path}

## Oversized Sections Detected

The following sections exceed the 5000 token limit and need subdivision:

"""

    for idx, section in enumerate(oversized_sections, 1):
        subdivision_request += f"""
### {idx}. {section['path']}

- **Section ID:** `{section['id']}`
- **Lines:** {section['start_line']} - {section['end_line']} ({section['lines']} lines)
- **Estimated Tokens:** {section['estimated_tokens']} (limit: 5000)
- **Action Required:** Add `children` array to section `{section['id']}`

"""

    subdivision_request += """
## Your Task (Claude Code)

For each oversized section:

1. **Extract section content:**
   - Use line numbers to read exact section from source
   - Example: `Read(file_path, offset={start_line}, limit={lines})`

2. **Identify semantic subdivisions:**
   - Look for logical boundaries (subsections, procedures, paragraphs)
   - Use Grep with `-n` flag to find markers
   - Extract line numbers for each subdivision

3. **Update structure.json:**
   - Add `children` array to the oversized section
   - Each child should have: id, title, type, start_line, end_line
   - DO NOT calculate `estimated_tokens` (automatic)

4. **Example subdivision:**
   ```json
   {
     "id": "003",
     "title": "API Reference",
     "type": "chapter",
     "start_line": 500,
     "end_line": 2000,
     "children": [
       {
         "id": "003_001",
         "title": "Authentication",
         "type": "section",
         "start_line": 500,
         "end_line": 800
       },
       {
         "id": "003_002",
         "title": "Core Endpoints",
         "type": "section",
         "start_line": 800,
         "end_line": 1500
       },
       {
         "id": "003_003",
         "title": "Error Handling",
         "type": "section",
         "start_line": 1500,
         "end_line": 2000
       }
     ]
   }
   ```

5. **Re-validate:**
   - Save updated structure.json
   - Re-run with `--analyze-only` to validate
   - Repeat until all leaf sections are ≤5000 tokens

## Validation Command

```bash
python3 ~/.claude/skills/novo_rag/scripts/generate_kb.py \\
  --name "{Path(structure_path).parent.stem.replace('-analysis', '')}" \\
  --from-structure "{structure_path}" \\
  --analyze-only
```
"""

    request_file = workspace_dir / "SUBDIVISION_REQUEST.md"
    with open(request_file, 'w', encoding='utf-8') as f:
        f.write(subdivision_request)

    print(f"\n⚠️  Oversized sections detected!")
    print(f"📋 Read: {request_file}")
    print(f"\n{len(oversized_sections)} sections need subdivision:")
    for section in oversized_sections:
        print(f"  - {section['path']}: {section['estimated_tokens']} tokens")

def generate_skill(name, structure_path, max_chunk_tokens=5000):
    """Phase 2: Generate skill from structure.json"""

    # Validate structure first
    oversized = validate_structure(structure_path, max_chunk_tokens)

    if oversized:
        create_subdivision_request(structure_path, oversized)
        print(f"\n❌ Cannot generate skill with oversized sections")
        print(f"⚙️  Update structure.json and re-run")
        return

    # Load structure
    with open(structure_path, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    # Create skill directory
    skill_dir = Path.home() / ".claude" / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create chunks directory
    chunks_dir = skill_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    # Load source text
    workspace_dir = Path(structure_path).parent
    samples_dir = workspace_dir / "samples"

    source_text = ""
    source_lines = []
    for md_file in samples_dir.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()
            source_text += text
            source_lines.extend(text.split('\n'))

    # Generate chunks
    chunks_metadata = []

    def process_section(section, parent_path="", depth=0):
        section_path = f"{parent_path}/{section['title']}" if parent_path else section['title']

        if 'children' in section and section['children']:
            # Process children
            for child in section['children']:
                process_section(child, section_path, depth + 1)
        else:
            # Leaf section - create chunk
            start_line = section.get('start_line', 0)
            end_line = section.get('end_line', len(source_lines))

            chunk_text = '\n'.join(source_lines[start_line:end_line])
            actual_tokens = count_tokens(chunk_text)

            # Create chunk file
            chunk_id = section.get('id', '000')
            chunk_file = chunks_dir / f"section_{chunk_id}.md"

            chunk_content = f"""# {section['title']}

**Path:** {section_path}
**Type:** {section.get('type', 'section')}
**Lines:** {start_line} - {end_line}
**Tokens:** {actual_tokens}

---

{chunk_text}
"""

            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk_content)

            chunks_metadata.append({
                'id': chunk_id,
                'title': section['title'],
                'path': section_path,
                'type': section.get('type', 'section'),
                'start_line': start_line,
                'end_line': end_line,
                'tokens': actual_tokens,
                'file': f"chunks/section_{chunk_id}.md"
            })

            print(f"✅ Created chunk: section_{chunk_id}.md ({actual_tokens} tokens)")

    for section in structure.get('sections', []):
        process_section(section)

    # Save metadata
    metadata_file = skill_dir / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({
            'name': name,
            'description': structure['metadata']['description'],
            'document_type': structure['metadata']['document_type'],
            'language': structure['metadata']['language'],
            'created': datetime.now().isoformat(),
            'total_chunks': len(chunks_metadata),
            'chunks': chunks_metadata
        }, f, indent=2)

    # Create index.md
    index_content = f"""# {name.replace('-', ' ').title()} - Index

**Description:** {structure['metadata']['description']}
**Type:** {structure['metadata']['document_type']}
**Language:** {structure['metadata']['language']}
**Total Chunks:** {len(chunks_metadata)}

## Hierarchical Table of Contents

"""

    def create_toc(section, depth=0):
        indent = "  " * depth
        toc = f"{indent}- **{section['title']}** ({section.get('type', 'section')})\n"

        if 'children' in section and section['children']:
            for child in section['children']:
                toc += create_toc(child, depth + 1)
        else:
            chunk_id = section.get('id', '000')
            toc = f"{indent}- [{section['title']}](chunks/section_{chunk_id}.md) ({section.get('type', 'section')})\n"

        return toc

    for section in structure.get('sections', []):
        index_content += create_toc(section)

    index_file = skill_dir / "index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)

    # Create SKILL.md
    skill_content = f"""---
name: {name}
description: {structure['metadata']['description']}
---

# {name.replace('-', ' ').title()}

This knowledge base contains semantically-organized information extracted from source documents.

## Structure

- **Type:** {structure['metadata']['document_type']}
- **Language:** {structure['metadata']['language']}
- **Total Chunks:** {len(chunks_metadata)}

## Usage

To access information from this knowledge base:

1. **Read index.md** to see the hierarchical table of contents
2. **Identify relevant sections** based on the user's query
3. **Read specific chunks** from the `chunks/` directory

All chunks are semantically complete sections with hierarchical context.

## Files

- `index.md` - Hierarchical table of contents
- `metadata.json` - Complete chunk metadata
- `chunks/` - Individual semantic sections

---

Generated by novo_rag skill on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    skill_file = skill_dir / "SKILL.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill_content)

    print(f"\n✅ Knowledge base skill generated: {skill_dir}")
    print(f"📋 Index: {index_file}")
    print(f"📊 Metadata: {metadata_file}")
    print(f"📁 Chunks: {len(chunks_metadata)} files in {chunks_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Knowledge Base Generator - Semantic Analysis Mode"
    )
    parser.add_argument("--name", required=True, help="Knowledge base skill name")
    parser.add_argument("--sources", help="Comma-separated paths to source documents")
    parser.add_argument("--description", help="Description of the knowledge base")
    parser.add_argument("--analyze-only", action="store_true", help="Phase 1: Perform semantic analysis only")
    parser.add_argument("--from-structure", help="Phase 2: Generate from existing structure.json")
    parser.add_argument("--max-chunk-tokens", type=int, default=5000, help="Target tokens per chunk (default: 5000)")

    args = parser.parse_args()

    if args.from_structure:
        # Phase 2: Generate skill from structure
        structure_path = Path(args.from_structure).expanduser()

        if not structure_path.exists():
            print(f"❌ Structure file not found: {structure_path}")
            sys.exit(1)

        # Check if we're just validating
        if args.analyze_only:
            oversized = validate_structure(structure_path, args.max_chunk_tokens)
            if oversized:
                create_subdivision_request(structure_path, oversized)
            else:
                print("✅ All sections are within token limits!")
                print("🚀 Ready to generate skill (remove --analyze-only)")
        else:
            generate_skill(args.name, structure_path, args.max_chunk_tokens)
    else:
        # Phase 1: Create analysis workspace
        if not args.sources or not args.description:
            print("❌ --sources and --description required for Phase 1")
            sys.exit(1)

        sources = [s.strip() for s in args.sources.split(',')]
        create_analysis_workspace(args.name, sources, args.description)

if __name__ == "__main__":
    main()
