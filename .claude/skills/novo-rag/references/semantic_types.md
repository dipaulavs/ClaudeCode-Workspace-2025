# Semantic Section Types

Reference guide for classifying sections during semantic analysis.

## Document Types

Choose the most appropriate document type for the `metadata.document_type` field:

- **technical_documentation** - API docs, technical manuals, reference guides
- **legal_document** - Contracts, terms of service, legal agreements
- **book** - Published books, e-books, long-form content
- **article** - Blog posts, articles, papers
- **manual** - User manuals, instruction guides
- **guide** - How-to guides, tutorials
- **specification** - Technical specifications, standards
- **policy** - Company policies, procedures, guidelines

## Section Types

Classify each section with the most appropriate semantic type:

### Structural Types

- **chapter** - Major divisions of a document (typically top-level)
- **part** - Large divisions containing multiple chapters
- **section** - Primary subdivision within a chapter
- **subsection** - Subdivision of a section
- **paragraph** - Smallest logical unit

### Functional Types

- **article** - Numbered articles in legal/formal documents (Article 1, Article 2)
- **procedure** - Step-by-step instructions
- **definition** - Definitions or glossary entries
- **example** - Example code, use cases, demonstrations
- **appendix** - Supplementary material
- **reference** - Reference material, lookup tables
- **introduction** - Introductory or overview sections
- **conclusion** - Concluding or summary sections
- **abstract** - Document abstracts or summaries

### Technical Types

- **endpoint** - API endpoint documentation
- **function** - Function/method documentation
- **class** - Class documentation
- **module** - Module/package documentation
- **configuration** - Configuration or settings documentation

## Language Codes

Use ISO 639-1 two-letter codes for the `metadata.language` field:

- **en** - English
- **pt** - Portuguese
- **es** - Spanish
- **fr** - French
- **de** - German
- **it** - Italian
- **ja** - Japanese
- **zh** - Chinese
- **ru** - Russian
- **ar** - Arabic

## Best Practices

1. **Be consistent:** Use the same type for similar sections
2. **Be specific:** Choose the most specific type that fits
3. **Consider hierarchy:** Types should reflect the document's structure
4. **Think semantically:** Focus on what the section *is*, not just its position

## Examples

**API Documentation:**
```json
{
  "document_type": "technical_documentation",
  "sections": [
    {"type": "chapter", "title": "Introduction"},
    {"type": "chapter", "title": "Authentication"},
    {"type": "section", "title": "API Keys"},
    {"type": "endpoint", "title": "POST /auth/login"}
  ]
}
```

**Legal Document:**
```json
{
  "document_type": "legal_document",
  "sections": [
    {"type": "article", "title": "Article 1 - Definitions"},
    {"type": "article", "title": "Article 2 - Scope"},
    {"type": "subsection", "title": "2.1 Applicability"}
  ]
}
```

**Technical Manual:**
```json
{
  "document_type": "manual",
  "sections": [
    {"type": "chapter", "title": "Getting Started"},
    {"type": "procedure", "title": "Installation Steps"},
    {"type": "section", "title": "Troubleshooting"}
  ]
}
```
