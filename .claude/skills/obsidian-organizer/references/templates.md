# Obsidian Content Templates

All templates use Brazilian datetime format: `DD/MM/YYYY HH:mm`

## Task Template

```markdown
---
criada: {DATETIME_BR}
status: aberta
---

# {TITLE}

## 📝 Detalhes
{DETAILS_OPTIONAL}

## ✅ Checklist
- [ ] {CHECKLIST_ITEMS}
```

**Required Fields:**
- `criada` - Current datetime in DD/MM/YYYY HH:mm
- `status` - Always "aberta" for new tasks
- `TITLE` - Clean task title

**Optional Fields:**
- `DETAILS_OPTIONAL` - Additional context (can be empty)
- `CHECKLIST_ITEMS` - Action items (at least one)

---

## Quick Note Template

```markdown
---
criada: {DATETIME_BR}
tags:
  - anotacao
---

# {TITLE}

{CONTENT}
```

**Required Fields:**
- `criada` - Current datetime in DD/MM/YYYY HH:mm
- `TITLE` - Note title
- `CONTENT` - Free-form content (any structure)

**Style Notes:**
- Ultra-minimal format
- No required sections beyond frontmatter
- User can add any markdown content freely

---

## YouTube Video Template

```markdown
---
assistido: {DATETIME_BR}
categoria: {CATEGORY}
link: {YOUTUBE_URL}
canvas: "[[{FILENAME}.canvas]]"
tags:
  - youtube
---

# {VIDEO_TITLE}

## 🎨 Resumo Visual

📊 **[Abrir Canvas Interativo]({FILENAME}.canvas)** - Explicação visual interativa

## 🎬 Informações
**Link:** {YOUTUBE_URL}
**Categoria:** {CATEGORY}
**Assistido em:** {DATETIME_BR}

## 📝 Resumo
{SUMMARY}

## 💡 Principais Aprendizados
{LEARNINGS_LIST}

> [!note]- 📄 Transcrição Completa (clique para expandir)
> {TRANSCRIPT_OPTIONAL}
```

**Required Fields:**
- `assistido` - Current datetime in DD/MM/YYYY HH:mm
- `categoria` - One of: notícia, tutorial, curso, aula, review, palestra, documentário
- `link` - Full YouTube URL
- `VIDEO_TITLE` - Video title (from URL or user description)
- `SUMMARY` - Brief summary (1-3 sentences)
- `LEARNINGS_LIST` - Bullet points of key takeaways

**Optional Fields:**
- `TRANSCRIPT_OPTIONAL` - Full video transcript (if available via estudar-video skill)

**Transcript Formatting:**
- Always use collapsible callout: `> [!note]- 📄 Transcrição Completa`
- Keeps note clean while preserving searchable content
- Hidden by default in Obsidian

---

## Template Variable Reference

| Variable | Format | Example |
|----------|--------|---------|
| `{DATETIME_BR}` | DD/MM/YYYY HH:mm | 07/11/2025 17:45 |
| `{TITLE}` | Clean string | Implementar autenticação |
| `{CATEGORY}` | Lowercase string | tutorial |
| `{YOUTUBE_URL}` | Full URL | https://youtube.com/watch?v=... |
| `{CONTENT}` | Markdown | Any valid markdown |

## Category Options (Videos Only)

Valid categories for YouTube videos:
- `notícia` - News/current events
- `tutorial` - How-to/instructional
- `curso` - Course/structured learning
- `aula` - Single lecture/lesson
- `review` - Product/service review
- `palestra` - Talk/presentation
- `documentário` - Documentary

Choose the most specific category that fits.
