#!/usr/bin/env python3
"""
KB Generator - Semantic Knowledge Base Creator

Creates knowledge base skills using semantic analysis rather than mechanical chunking.
Two-phase process: Analysis → Generation
"""

import argparse
import json
import os
import sys
from pathlib import Path

def create_analysis_workspace(name, sources, description):
    """Phase 1: Create analysis workspace and request"""
    workspace = Path.home() / ".claude" / "skills" / f"{name}-analysis"
    workspace.mkdir(parents=True, exist_ok=True)
    
    # Create samples directory
    samples_dir = workspace / "samples"
    samples_dir.mkdir(exist_ok=True)
    
    # Create ANALYSIS_REQUEST.md
    request_file = workspace / "ANALYSIS_REQUEST.md"
    request_content = f"""# Semantic Analysis Request

**Knowledge Base Name:** {name}
**Description:** {description}

## Your Task (Claude Code)

Perform semantic analysis of the source documents to create a hierarchical structure.

### Steps:

1. **Read source documents** from `samples/` directory
2. **Identify document structure:**
   - Document type (book, api_docs, legal, article, etc.)
   - Language
   - Major structural divisions (chapters, sections, articles, etc.)
3. **Create structure.json** with semantic boundaries
4. **Use line numbers** for precise extraction (0-indexed)
5. **Validate:** All leaf sections ≤5000 tokens

### structure.json Template:

```json
{{
  "description": "{description}",
  "document_info": {{
    "type": "technical_documentation",
    "language": "en",
    "total_lines": 1000,
    "tokens_per_line": 2.5
  }},
  "sections": [
    {{
      "id": "section_001",
      "title": "Section Title",
      "start_line": 0,
      "end_line": 200,
      "semantic_type": "introduction",
      "children": []
    }}
  ]
}}
```

### Guidelines:

- Use Grep with `-n` flag to find structural markers
- Store boundaries as line numbers (precise, unambiguous)
- System calculates tokens automatically - you only provide line ranges
- Keep subdividing until ALL leaf sections ≤5000 tokens
- No gaps or overlaps in line ranges

## Source Documents

{sources}

**Next:** Create structure.json in this workspace directory.
"""
    
    request_file.write_text(request_content)
    
    print(f"✓ Analysis workspace created: {workspace}")
    print(f"✓ Read ANALYSIS_REQUEST.md for instructions")
    print(f"\nNext steps:")
    print(f"1. Copy source documents to: {samples_dir}/")
    print(f"2. Read ANALYSIS_REQUEST.md")
    print(f"3. Analyze documents and create structure.json")
    print(f"4. Re-run with --analyze-only to validate")
    
    return workspace

def validate_structure(structure_path):
    """Validate structure.json and check for oversized sections"""
    with open(structure_path) as f:
        structure = json.load(f)
    
    doc_info = structure.get("document_info", {})
    tokens_per_line = doc_info.get("tokens_per_line", 2.5)
    
    oversized = []
    
    def check_section(section, path=""):
        section_path = f"{path}/{section['title']}" if path else section['title']
        
        if section.get("children"):
            for child in section["children"]:
                check_section(child, section_path)
        else:
            # Leaf section - check size
            lines = section["end_line"] - section["start_line"]
            tokens = lines * tokens_per_line
            
            if tokens > 5000:
                oversized.append({
                    "path": section_path,
                    "id": section["id"],
                    "tokens": int(tokens),
                    "start_line": section["start_line"],
                    "end_line": section["end_line"]
                })
    
    for section in structure.get("sections", []):
        check_section(section)
    
    return oversized

def create_subdivision_request(workspace, oversized):
    """Create SUBDIVISION_REQUEST.md with oversized sections"""
    request_file = workspace / "SUBDIVISION_REQUEST.md"
    
    content = f"""# Subdivision Request

## Oversized Sections Detected

The following sections exceed the 5000 token limit and need subdivision:

"""
    
    for section in oversized:
        content += f"""
### {section['path']}
- **ID:** {section['id']}
- **Tokens:** {section['tokens']}
- **Lines:** {section['start_line']}-{section['end_line']}

**Action needed:** Extract this section, identify logical subdivisions, and update structure.json with `children` array.

---
"""
    
    content += """
## Instructions:

1. For each oversized section:
   - Extract content from source document
   - Identify semantic subdivisions (chapters, subsections, endpoints, etc.)
   - Create children in structure.json
2. Update structure.json
3. Re-run validation: `python3 ... --analyze-only`
4. Repeat until all leaf sections ≤5000 tokens

## Example Fix:

```json
{
  "id": "section_002",
  "title": "Oversized Section",
  "start_line": 100,
  "end_line": 500,
  "children": [
    {
      "id": "section_002_001",
      "title": "First Subsection",
      "start_line": 100,
      "end_line": 250,
      "semantic_type": "subsection"
    },
    {
      "id": "section_002_002",
      "title": "Second Subsection",
      "start_line": 250,
      "end_line": 500,
      "semantic_type": "subsection"
    }
  ]
}
```
"""
    
    request_file.write_text(content)
    print(f"\n⚠️  Oversized sections detected!")
    print(f"✓ Created: {request_file}")
    print(f"\nRead SUBDIVISION_REQUEST.md and update structure.json")

def extract_lines(source_path, start_line, end_line):
    """Extract lines from source document (0-indexed)"""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return ''.join(lines[start_line:end_line])

def generate_skill(name, structure_path, source_path=None):
    """Phase 2: Generate final skill from structure.json"""
    print(f"\n🚧 Phase 2: Skill generation")

    # Load structure
    with open(structure_path) as f:
        structure = json.load(f)

    # Find source document
    if not source_path:
        workspace = Path(structure_path).parent
        request_file = workspace / "ANALYSIS_REQUEST.md"
        if request_file.exists():
            content = request_file.read_text()
            # Extract source path from ANALYSIS_REQUEST.md
            for line in content.split('\n'):
                if line.startswith('/') and line.endswith('.txt'):
                    source_path = line.strip()
                    break

    if not source_path or not Path(source_path).exists():
        print(f"Error: Source document not found. Provide --sources or check ANALYSIS_REQUEST.md")
        sys.exit(1)

    print(f"📄 Source: {source_path}")

    # Create skill directory in WORKSPACE .claude/skills/
    workspace_root = Path.home() / "Desktop" / "ClaudeCode-Workspace"
    skill_dir = workspace_root / ".claude" / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir = skill_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    # Generate chunks
    metadata = []

    def generate_chunks(sections, path="", parent_title=""):
        for section in sections:
            section_id = section['id']
            section_title = section['title']
            section_path = f"{path}/{section_title}" if path else section_title

            if section.get('children'):
                # Has children - recurse
                generate_chunks(section['children'], section_path, section_title)
            else:
                # Leaf section - extract and save
                content = extract_lines(source_path, section['start_line'], section['end_line'])

                # Create chunk file
                chunk_file = chunks_dir / f"{section_id}.md"
                chunk_content = f"""# {section_title}

**Path:** {section_path}
**Type:** {section.get('semantic_type', 'section')}

---

{content}
"""
                chunk_file.write_text(chunk_content)

                # Add metadata
                lines = section['end_line'] - section['start_line']
                tokens = int(lines * structure['document_info'].get('tokens_per_line', 3.5))

                metadata.append({
                    "id": section_id,
                    "title": section_title,
                    "path": section_path,
                    "type": section.get('semantic_type', 'section'),
                    "tokens": tokens,
                    "file": f"chunks/{section_id}.md"
                })

    generate_chunks(structure['sections'])

    # Save metadata.json
    metadata_file = skill_dir / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))

    # Copy structure.json
    structure_file = skill_dir / "structure.json"
    structure_file.write_text(json.dumps(structure, indent=2))

    # Generate index.md (TOC)
    index_content = f"""# {name.replace('-', ' ').title()} - Index

**Total Sections:** {len(metadata)}

## Table of Contents

"""

    for item in metadata:
        index_content += f"- [{item['title']}]({item['file']}) ({item['tokens']} tokens)\n"

    index_file = skill_dir / "index.md"
    index_file.write_text(index_content)

    # Generate SKILL.md (model-invoked ACTIVE format)
    doc_desc = structure.get('document_info', {})

    # Get KB metadata from structure
    kb_description = structure.get('description', f"Knowledge base from {name.replace('-', ' ')}")

    # Generate simple book name variations for trigger
    book_name = name.replace('-', ' ').replace('m ', 'M ')  # e.g., "100m offers" → "100M offers"
    book_name_variants = [
        name,  # "100m-offers"
        name.replace('-', ' '),  # "100m offers"
        book_name,  # "100M offers"
        book_name.replace(' ', ''),  # "100Moffers"
    ]

    skill_content = f"""name: {name}

description: {kb_description}

# {name.replace('-', ' ').title()}

**Type:** {doc_desc.get('type', 'knowledge_base')} (Model-Invoked Skill)
**Language:** {doc_desc.get('language', 'en')}
**Total Sections:** {len(metadata)}

## 🎯 When to Use This Skill

This knowledge base is **model-invoked** - Claude Code automatically activates it based on the description above.

**Common triggers:**
- User mentions book/document name variations: {', '.join(f'"{v}"' for v in book_name_variants)}
- User asks about topics covered in this knowledge base
- Context matches the description keywords

**When activated:**
1. Search relevant sections: `Grep pattern="keyword" path="~/.claude/skills/{name}/chunks"`
2. Read matching chunks
3. Answer using content from knowledge base

## How to Use

### Search by Keyword

```bash
Grep pattern="keyword" path="~/.claude/skills/{name}/chunks" output_mode="content" -C=3
```

### Browse Index

```bash
Read file_path="~/.claude/skills/{name}/index.md"
```

### Read Specific Section

```bash
Read file_path="~/.claude/skills/{name}/chunks/section_XXX.md"
```

## Table of Contents

"""

    for item in metadata:
        skill_content += f"- [{item['title']}]({item['file']}) - {item['type']}\n"

    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_content)

    print(f"✓ Generated {len(metadata)} chunks")
    print(f"✓ Created skill: .claude/skills/{name}/")
    print(f"\n📂 Files:")
    print(f"  • SKILL.md (main file - MODEL-INVOKED skill)")
    print(f"  • index.md (TOC)")
    print(f"  • metadata.json ({len(metadata)} sections)")
    print(f"  • chunks/ ({len(metadata)} files)")
    print(f"\n✅ Model-Invoked Skill ready:")
    print(f"  📁 Location: ~/Desktop/ClaudeCode-Workspace/.claude/skills/{name}/")
    print(f"  🎯 Auto-activates based on description triggers")
    print(f"  📖 Auto-discovered by Claude Code")

def main():
    parser = argparse.ArgumentParser(description="KB Generator - Semantic Knowledge Base Creator")
    parser.add_argument("--name", required=True, help="Knowledge base name")
    parser.add_argument("--sources", help="Source document path")
    parser.add_argument("--description", help="KB description")
    parser.add_argument("--analyze-only", action="store_true", help="Phase 1: Analysis only")
    parser.add_argument("--from-structure", help="Phase 2: Generate from structure.json")
    parser.add_argument("--max-chunk-tokens", type=int, default=5000, help="Max tokens per chunk")
    
    args = parser.parse_args()
    
    if args.analyze_only:
        # Phase 1: Analysis
        if not args.sources or not args.description:
            print("Error: --sources and --description required for --analyze-only")
            sys.exit(1)
        
        workspace = create_analysis_workspace(args.name, args.sources, args.description)
        
        # Check if structure.json exists for validation
        structure_path = workspace / "structure.json"
        if structure_path.exists():
            print(f"\n🔍 Validating structure.json...")
            oversized = validate_structure(structure_path)
            
            if oversized:
                create_subdivision_request(workspace, oversized)
                sys.exit(1)
            else:
                print(f"\n✓ All sections are ≤{args.max_chunk_tokens} tokens")
                print(f"✓ Ready for Phase 2: --from-structure {structure_path}")
        
    elif args.from_structure:
        # Phase 2: Generation
        structure_path = Path(args.from_structure).expanduser()
        
        if not structure_path.exists():
            print(f"Error: {structure_path} not found")
            sys.exit(1)
        
        print(f"🔍 Validating {structure_path}...")
        oversized = validate_structure(structure_path)
        
        if oversized:
            workspace = structure_path.parent
            create_subdivision_request(workspace, oversized)
            print("\nℹ️  You can proceed anyway (oversized chunks warning) or fix structure.json first")
        
        generate_skill(args.name, structure_path)
    
    else:
        print("Error: Use --analyze-only OR --from-structure")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
