---
name: estudar-video
description: Automatiza o estudo completo de vídeos do YouTube - transcreve com Whisper, analisa conteúdo com IA, extrai insights, classifica por tipo, e salva no Obsidian Knowledge Base. Use APENAS quando usuário pedir explicitamente para estudar vídeo (ex "estuda esse vídeo pra mim").
allowed-tools: Bash, Read, Write, Edit
---

# Estudar Vídeo YouTube

## Purpose

Automate complete YouTube video analysis workflow: transcribe audio with Whisper, analyze content with AI, extract insights, classify by type, and save structured notes in Obsidian vault using MCP filesystem.

Transform any YouTube video into a searchable, organized knowledge base entry with minimal user effort.

## When to Use

Use this skill **ONLY** when the user **explicitly requests** video study using phrases like:
- "Estuda esse vídeo pra mim"
- "Preciso que você estude esse vídeo"
- "Analisa esse vídeo completamente e salva no Obsidian"

**DO NOT auto-invoke** when user:
- Simply shares a YouTube URL without requesting study
- Mentions YouTube video in casual conversation
- Only wants transcription (use transcribe_video.py directly)

**IMPORTANT:** Execute automatically without confirmation once user explicitly requests video study.

## How to Use the Skill

### Complete Workflow (3 Steps)

#### Step 1: Transcribe Video

Use the transcription script to extract audio and convert to text:

```bash
python3 scripts/extraction/transcribe_video.py "YOUTUBE_URL"
```

**Script location:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/extraction/transcribe_video.py`

**What it does:**
- Downloads audio from YouTube using yt-dlp
- Transcribes using OpenAI Whisper API
- Saves transcription to `~/Downloads/transcription_youtube_[TIMESTAMP]/`
- Returns path to `transcription.txt` file

**Cost:** ~$0.006/minute | **Time:** ~2-3min for 60min video

#### Step 2: Analyze Content

After transcription completes:

1. **Read transcription file** using Read tool
2. **Analyze content** and extract:
   - Descriptive title (from context)
   - Category (tutorial|noticia|curso|aula|review)
   - Brief summary (2-3 lines)
   - Main learnings (3-5 practical points)
   - Relevant tags (based on content)

#### Step 3: Save to Obsidian with Visual Canvas

**ALWAYS use obsidian-organizer skill** to save the analyzed video.

**Why:** obsidian-organizer automatically:
- Creates formatted markdown note in `📺 Vídeos/`
- Generates interactive Canvas visual diagram
- Links Canvas in the note
- Uses correct Brazilian date format
- Applies minimalist template

**How to call:**

After analyzing transcription, invoke obsidian-organizer skill with the extracted data:
- YouTube URL
- Title
- Category
- Summary
- Learnings list
- Transcription text

**DO NOT manually create files.** Let obsidian-organizer handle file creation and Canvas generation.

**Legacy template (for reference only):**

```markdown
---
assistido: DD/MM/YYYY HH:mm
categoria: [tutorial|noticia|curso|aula|review]
link: [YOUTUBE_URL]
tags:
  - youtube
  - [tag1]
  - [tag2]
---

# [Descriptive Title]

## 🎬 Informações

**Link:** [URL]
**Categoria:** [categoria]
**Assistido em:** DD/MM/YYYY HH:mm

---

## 📝 Resumo

[Brief 2-3 line summary]

---

## 💡 Principais Aprendizados

- [Learning 1]
- [Learning 2]
- [Learning 3]

---

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Full transcription content here]
```

### Template Rules

**Required fields:**
- `assistido`: Brazilian date format DD/MM/YYYY HH:mm (current datetime)
- `categoria`: Choose most appropriate (tutorial|noticia|curso|aula|review)
- `link`: Original YouTube URL
- `tags`: Relevant content tags (always include `youtube`)

**Content guidelines:**
- Summary: Concise and direct (2-3 lines maximum)
- Learnings: Practical and actionable (3-5 items)
- Transcription: ALWAYS use collapsible callout `> [!note]-`
- Title: Descriptive, based on video content

### Category Definitions

Choose the most appropriate category:

- **tutorial** - Step-by-step practical instructions
- **noticia** - News, launches, technology updates
- **curso** - Course lesson/educational training
- **aula** - Single educational lecture/class
- **review** - Critical analysis of tool/product

For detailed category criteria and analysis templates, see [references/REFERENCE.md](references/REFERENCE.md).

### Output Format for User

After completing the workflow, inform the user with this minimalist format:

```
✅ Vídeo estudado e salvo com Canvas visual!

📺 [Video Title]
📍 Salvo em: 📺 Vídeos/[filename].md
📊 Canvas: 📺 Vídeos/Canvas/[filename].canvas
⏰ Assistido: DD/MM/YYYY HH:mm
🏷️ Categoria: [categoria]

💡 Principais aprendizados: [one-line summary]
```

## Important Rules

### DO:
- Execute immediately without confirmation
- Analyze the complete transcription
- Classify category (required: tutorial|noticia|curso|aula|review)
- Extract practical learnings (3-5 items)
- **ALWAYS call obsidian-organizer skill** to save the video
- **ALWAYS generate Canvas visual** (automatic via obsidian-organizer)
- Provide minimalist response to user

### DON'T:
- **DON'T** ask for user confirmation
- **DON'T** skip transcription (always use Whisper)
- **DON'T** manually create markdown files (use obsidian-organizer)
- **DON'T** skip Canvas generation (automatic via obsidian-organizer)
- **DON'T** use old structure (09 - YouTube Knowledge/)
- **DON'T** forget required category
- **DON'T** create subfolders by type

## Configuration

**Obsidian Vault:**
```
/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/
```

**Destination folder:**
```
📺 Vídeos/
```

**Temporary transcriptions:**
```
/Users/felipemdepaula/Downloads/transcription_youtube_[TIMESTAMP]/
```

**Python:** `python3` (system default)

## Bundled Resources

### Scripts

**Transcription script:**
- Location: `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/extraction/transcribe_video.py`
- Purpose: Download YouTube audio and transcribe with Whisper
- Usage: `python3 scripts/extraction/transcribe_video.py "URL"`

**Auto-correction scripts:**
- `scripts/update_skill.py` - Update SKILL.md programmatically
- `scripts/log_learning.py` - Log fixes in LEARNINGS.md

### References

**Detailed documentation (load as needed):**
- `references/REFERENCE.md` - System architecture, technical details, category analysis templates
- `references/EXAMPLES.md` - Example analyses for different video types
- `references/INTEGRATION.md` - **Integration with obsidian-organizer skill** (Canvas generation)
- `references/TROUBLESHOOTING.md` - Common issues and solutions

Load references when:
- Need detailed category classification criteria
- Want to see example analyses
- Understanding obsidian-organizer integration
- Troubleshooting errors

## Auto-Correction System

When errors occur during skill execution:

```
Error detected
↓
1. Identify what went wrong
2. Fix SKILL.md: python3 scripts/update_skill.py <old> <new>
3. Log learning: python3 scripts/log_learning.py <error> <fix> [line]
4. Error prevented in future executions
```

**Example workflow:**

```bash
# 1. Fix the error in SKILL.md
python3 scripts/update_skill.py \
    'python3 script.py --flag "text"' \
    'python3 script.py "text"'

# 2. Log the learning
python3 scripts/log_learning.py \
    "Flag --flag not recognized" \
    "Removed --flag, using positional argument" \
    "SKILL.md:97"
```

**Benefits:**
- Zero repeat errors - Same mistake never happens twice
- Automatic documentation - All fixes logged in LEARNINGS.md
- Skill evolution - Skills improve over time automatically
- Debugging history - Full record of what was fixed and when

## Troubleshooting

**Error: Write tool failed (Permission denied)**
- Verify absolute vault path exists
- Ensure `📺 Vídeos/` folder exists in vault
- MCP filesystem doesn't require Obsidian to be open

**Error: Transcription failed**
- Verify YouTube URL is valid
- Check Whisper API connection (OpenAI)
- Verify OpenAI API balance

**Error: Category not defined**
- ALWAYS choose one of 5 valid categories
- Don't create custom categories

**Error: Wrong date format**
- ALWAYS use DD/MM/YYYY HH:mm (Brazilian)
- Don't use MM/DD/YYYY (American)

For detailed troubleshooting, see [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md).

---

**Created:** 02/11/2025
**Updated:** 08/11/2025
**Status:** ✅ Active | MCP filesystem | Auto-correction enabled | Canvas visual integration
