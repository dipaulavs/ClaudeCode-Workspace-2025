# Integration with obsidian-organizer

## Overview

The `estudar-video` skill now **automatically integrates** with `obsidian-organizer` to save analyzed videos with visual Canvas diagrams.

## Workflow Integration

```
estudar-video invoked
       ↓
Step 1: Transcribe YouTube video (Whisper)
       ↓
Step 2: Analyze transcription content
       ↓
Step 3: Call obsidian-organizer skill
       ↓
obsidian-organizer:
   ├─ Creates markdown note (📺 Vídeos/)
   ├─ Generates Canvas visual (.canvas)
   └─ Links Canvas in note
       ↓
estudar-video confirms completion
```

## Why This Integration?

**Before (manual):**
- estudar-video created markdown file directly
- No Canvas generation
- Duplicate template maintenance
- Inconsistent formatting

**After (integrated):**
- estudar-video focuses on transcription + analysis
- obsidian-organizer handles file creation + Canvas
- Single source of truth for templates
- Automatic visual diagrams

## How to Call obsidian-organizer

After analyzing transcription in Step 2, invoke `obsidian-organizer` skill:

```python
# Example invocation (conceptual)
Skill("obsidian-organizer")

# Then provide extracted data:
# - YouTube URL
# - Title
# - Category
# - Summary
# - Learnings (list)
# - Transcription text
```

**obsidian-organizer will:**
1. Detect YouTube URL → use Video template
2. Create markdown note with frontmatter
3. Generate Canvas JSON with visual layout
4. Save both files to `📺 Vídeos/`
5. Link Canvas in markdown note

## Data Extraction Requirements

Before calling obsidian-organizer, estudar-video must extract:

| Field | Type | Example |
|-------|------|---------|
| `url` | String | https://youtube.com/watch?v=abc123 |
| `title` | String | Tutorial Async Python - AsyncIO |
| `category` | String | tutorial (noticia\|curso\|aula\|review) |
| `summary` | String | Brief 2-3 line summary |
| `learnings` | List[String] | ["Learning 1", "Learning 2", ...] |
| `transcription` | String | Full video transcript |

## Canvas Generation (Automatic)

obsidian-organizer automatically generates Canvas with AI-generated illustrations:

**Visual Structure:**
```
    🎬 Video Title
          ↓
     📝 Summary
          ↓
  ┌─────┬─────┐
  │ 💡1 │ 💡2 │  Learnings grid (2 cols)
  ├─────┼─────┤
  │ 💡3 │ 💡4 │
  └─────┴─────┘
          ↓
  ┌─────┬─────┬─────┐
  │ 🎨1 │ 🎨2 │ 🎨3 │  Childlike drawings (3 cols)
  └─────┴─────┴─────┘
```

**Node Layout:**
- Title: Top center (-200, -400)
- Summary: Below title (-200, -200)
- Learnings: Grid starting at y=100 (2 columns)
- **Images: Grid starting at y=450 (3 columns)**
- Colors: Rotating palette (1-6)
- Edges: Connected with colored arrows

**Image Generation:**
- Uses google-gemini-image skill
- Style: Childlike pencil sketches
- 3 images per video (main concept, process, takeaway)
- Uploaded to Nextcloud for permanent links
- Embedded as file nodes in Canvas

## Response Format

After obsidian-organizer completes, estudar-video responds:

```
✅ Vídeo estudado e salvo com Canvas visual!

📺 [Video Title]
📍 Salvo em: 📺 Vídeos/[filename].md
📊 Canvas: 📺 Vídeos/[filename].canvas
⏰ Assistido: DD/MM/YYYY HH:mm
🏷️ Categoria: [categoria]

💡 Principais aprendizados: [one-line summary]
```

## Error Handling

If obsidian-organizer fails:
1. estudar-video catches error
2. Falls back to legacy manual creation
3. Logs error for debugging
4. Still saves transcription (no data loss)

## Benefits

✅ **Single responsibility:** estudar-video = transcribe/analyze, obsidian-organizer = save/organize
✅ **Visual learning:** Every video gets interactive Canvas with AI illustrations
✅ **Childlike drawings:** Simple pencil sketches enhance understanding and memory
✅ **Consistency:** Same template/formatting for all videos
✅ **Maintainability:** Update template once in obsidian-organizer
✅ **Discoverability:** Canvas makes content easier to review
✅ **Multi-modal learning:** Text + visuals = better retention

## Migration Notes

**Old behavior (deprecated):**
- estudar-video manually created markdown files
- No Canvas generation
- Template hardcoded in SKILL.md

**New behavior (current):**
- estudar-video calls obsidian-organizer
- Canvas auto-generated
- Template in obsidian-organizer/references/templates.md

**Legacy template:** Kept in SKILL.md for reference but NOT used for file creation.

## Testing

To test integration:

```bash
# 1. Invoke estudar-video with YouTube URL
# 2. Verify transcription completes
# 3. Verify obsidian-organizer is called
# 4. Check files created:
ls ~/Documents/Obsidian/Claude-code-ios/📺\ Vídeos/

# Should see:
# - [video-title].md (markdown note)
# - [video-title].canvas (visual diagram)
```

## Future Enhancements

Potential improvements:
- Add transcript chunks as separate Canvas nodes
- Generate concept map from key terms
- Link related videos in Canvas
- Add thumbnail images to Canvas nodes

---

**Created:** 08/11/2025
**Purpose:** Document estudar-video + obsidian-organizer integration
**Status:** ✅ Active
