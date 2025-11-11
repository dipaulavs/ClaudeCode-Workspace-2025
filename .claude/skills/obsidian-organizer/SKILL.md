---
name: obsidian-organizer
description: Automatically captures and organizes content in Obsidian vault with intelligent type detection (tasks, notes, videos). Uses user's minimalist system with Brazilian date format. Auto-invokes when user asks to save, note, organize, or capture anything.
---

# Obsidian Organizer

Automatically detect content type and create formatted notes in the correct Obsidian vault location using the user's minimalist organization system.

## 🚨 CRITICAL RULES (Must Follow)

1. **Title Case Filenames:** Always use Title Case with spaces
   - ✅ "Minha Nova Tarefa.md"
   - ❌ "minha-nova-tarefa.md"

2. **Frontmatter Field:** Always use `criada:` (not `created:`)
   - ✅ `criada: 11/11/2025 10:30`
   - ❌ `created: 11/11/2025 10:30`

3. **Task Status:** All new tasks must have `status: aberta`
   - ✅ `status: aberta`
   - ❌ `status: pendente` or missing status

4. **Kanban Integration:** ALWAYS add tasks to Kanban in `## aberta` section
   - ✅ Add line: `- [ ] [[Filename]]`
   - ❌ Skip Kanban step

5. **Brazilian DateTime:** Always use DD/MM/YYYY HH:mm format
   - ✅ `11/11/2025 10:30`
   - ❌ `2025-11-11 10:30`

## When to Use This Skill

Auto-invoke when user requests:
- "Anota isso" / "Save this" / "Note this"
- "Salva no Obsidian" / "Add to Obsidian"
- "Registra essa ideia" / "Capture this idea"
- "Organiza isso" / "Organize this"
- "Organize minhas notas" / "Organiza minhas notas soltas"
- Shares YouTube URL with context of learning
- Mentions task/todo/action item
- Shares unorganized/messy note content
- **NEW:** "Salva esse áudio/foto/vídeo no Obsidian"
- **NEW:** Mentions media file to be saved (auto-uploads to Nextcloud)

## User's Organization System

The vault uses 3 main categories with emoji prefixes:

### 📋 Tarefas (Tasks)
**Detect when:** Action items, todos, checklists, things to do, deadlines
**Keywords:** "preciso fazer", "tenho que", "tarefa", "lembrar de", "to-do"
**Location:** `📋 Tarefas/`
**Template:** See `references/templates.md` → Task Template

### 💡 Anotações (Quick Notes)
**Detect when:** Ideas, thoughts, quick captures, interesting links, drafts
**Keywords:** "ideia rápida", "vi isso", "quero lembrar", "anota rapidamente"
**Location:** `💡 Anotações/`
**Template:** See `references/templates.md` → Quick Note Template
**Style:** Ultra-minimal, no required structure

### 📺 Vídeos (YouTube Learning)
**Detect when:** YouTube URL mentioned with learning context
**Keywords:** "assisti vídeo", "vi tutorial", "aprendi com", YouTube URL present
**Location:** `📺 Vídeos/`
**Template:** See `references/templates.md` → YouTube Video Template
**Required:** Category (notícia, tutorial, curso, aula, review)
**AUTO-GENERATE:** Visual Canvas explanation (interactive diagram)

## Content Type Detection Flow

```
User input received
       │
       ▼
┌──────────────────┐
│ Analyze keywords │
│ and context      │
└────────┬─────────┘
         │
         ├──> Contains YouTube URL? ──YES──> 📺 Vídeos
         │
         ├──> Action/todo keywords? ──YES──> 📋 Tarefas
         │
         └──> Default/idea/quick? ───YES──> 💡 Anotações
```

## Execution Workflow (Step-by-Step)

**IMPORTANT:** Always execute ALL steps below. Never skip steps.

### Step 1: Analyze Content Type
- Read user's request
- Identify keywords: tarefa/task → 📋 Tarefas | ideia/nota → 💡 Anotações | YouTube URL → 📺 Vídeos
- Determine target folder

### Step 2: Generate Filename
- Extract title from content
- Convert to **Title Case** (capitalize first letter of each word)
- Use spaces (not hyphens)
- Example: "Minha Nova Tarefa" (NOT "minha-nova-tarefa")

### Step 3: Get Current DateTime
- Format: **DD/MM/YYYY HH:mm** (Brazilian format)
- Use `date +"%d/%m/%Y %H:%M"` command
- Example: `11/11/2025 10:30`

### Step 4: Load Template
- Read appropriate template from `references/templates.md`
- Task → Task Template (with `status: aberta`)
- Note → Quick Note Template
- Video → YouTube Video Template

### Step 5: Fill Template
- Replace `{DATETIME_BR}` with current datetime
- Replace `{TITLE}` with Title Case filename
- Replace other placeholders with content
- **CRITICAL:** Use `criada:` field (NOT `created:`)
- **CRITICAL:** For tasks, always include `status: aberta`

### Step 6: Write File
```bash
Write(
  file_path="~/Documents/Obsidian/Claude-code-ios/{CATEGORY}/{Filename}.md",
  content=filled_template
)
```

### Step 7: Add to Kanban (TASKS ONLY)
**If type is 📋 Tarefas:**
1. Read Kanban file: `📋 Tarefas/📊 Kanban.md`
2. Find section `## aberta`
3. Add new line: `- [ ] [[Filename]]` (without `.md` extension)
4. Write updated Kanban

**Example:**
```markdown
## aberta

- [ ] [[Minha Nova Tarefa]]
- [ ] [[Outra Tarefa]]
```

### Step 8: Confirm Creation
Show user concise confirmation:
```
✅ {Type} criada: {Category}/{Filename}.md
```

**Example outputs:**
- ✅ Tarefa criada: 📋 Tarefas/Implementar Feature X.md
- ✅ Nota criada: 💡 Anotações/Ideia Startup.md
- ✅ Vídeo salvo: 📺 Vídeos/Tutorial Python.md

## Technical Implementation

**Vault Path:** `~/Documents/Obsidian/Claude-code-ios/`

**Access Method:**
- Use Write/Read tools (direct filesystem access)
- Works with Obsidian closed
- Syncs automatically via iCloud
- No REST API or Obsidian process required

**File Creation:**
```
Write(
  file_path=VAULT_PATH + CATEGORY_FOLDER + filename,
  content=filled_template
)
```

**Example Paths:**
- `~/Documents/Obsidian/Claude-code-ios/📋 Tarefas/Implementar Feature X.md`
- `~/Documents/Obsidian/Claude-code-ios/💡 Anotações/Ideia Rapida 2024.md`
- `~/Documents/Obsidian/Claude-code-ios/📺 Vídeos/Tutorial Python Async.md`

**Filename Format:**
- **Title Case** (capitalize first letter of each word)
- **Spaces** instead of hyphens
- **No special chars** (except spaces)
- Example: "Buscar Template Instructions Claude"

**Kanban Integration (Tasks Only):**

When creating a task (📋 Tarefas):
1. Create markdown file with Title Case filename
2. Add frontmatter with `criada` field and `status: aberta`
3. Read Kanban file: `📋 Tarefas/📊 Kanban.md`
4. Find section `## aberta`
5. Add new line: `- [ ] [[Filename]]` (without `.md` extension)
6. Write updated Kanban back

**Example Kanban Update:**
```markdown
## aberta

- [ ] [[Minha Nova Tarefa]]  ← Add this line
- [ ] [[Outra Tarefa Existente]]
```

## ✅ Final Checklist (MUST VERIFY)

Before confirming to user, verify ALL items:

- [ ] Filename is in Title Case with spaces
- [ ] Frontmatter has `criada:` field (DD/MM/YYYY HH:mm)
- [ ] If task: `status: aberta` in frontmatter
- [ ] If task: Added to Kanban `## aberta` section
- [ ] File written to correct category folder
- [ ] Confirmation message sent to user

**Confirmation Format:**
```
✅ {Type} criada: {Category}/{Filename}.md
```

## Media Upload (Nextcloud Integration)

**When to upload:**
- User saves content with attached media (áudio, foto, vídeo, PDF, etc)
- File is in Downloads or specified path
- User explicitly mentions media file

**Upload Workflow:**
```bash
# Auto-detect media file and upload
python3 SCRIPTS/nextcloud/upload_rapido.py [file_path]

# Returns: Public permanent link
# Example: https://media.loop9.com.br/s/abc123/download/audio.mp3
```

**Integration:**
1. Detect media file in user's request
2. Upload to Nextcloud using `upload_rapido.py`
3. Get public permanent link
4. Insert link in markdown content
5. Create note in Obsidian with embedded media link

**Nextcloud Config:**
- URL: `https://media.loop9.com.br`
- User: `dipaula`
- Folder: `imagens/upload/` (permanent storage)
- Links: Permanent (no expiration)

**Markdown Media Embedding:**
```markdown
# Áudio
🎙️ [audio_file.mp3](https://media.loop9.com.br/s/token/download/audio.mp3)

# Imagem
![image_name](https://media.loop9.com.br/s/token/download/image.jpg)

# Vídeo
🎬 [video_name.mp4](https://media.loop9.com.br/s/token/download/video.mp4)

# PDF
📄 [document.pdf](https://media.loop9.com.br/s/token/download/document.pdf)
```

**File Detection:**
- Audio: `.mp3`, `.wav`, `.m4a`, `.ogg`
- Image: `.jpg`, `.png`, `.gif`, `.webp`
- Video: `.mp4`, `.mov`, `.avi`, `.mkv`
- Document: `.pdf`, `.docx`, `.txt`

## Visual Canvas Generation (YouTube Videos Only)

When creating a YouTube video note, automatically generate an interactive Canvas diagram with AI-generated illustrations.

**Complete Workflow:**
```
YouTube video detected
       ↓
Create markdown note (📺 Vídeos/)
       ↓
Extract: title, summary, learnings
       ↓
Generate 3 childlike pencil drawings (google-gemini-image)
   ├─ Drawing 1: Main concept illustration
   ├─ Drawing 2: Key process/workflow
   └─ Drawing 3: Important takeaway
       ↓
Upload images to Nextcloud (permanent links)
       ↓
Generate Canvas JSON with:
   ├─ Text nodes (title, summary, learnings)
   └─ Image nodes (3 pencil drawings)
       ↓
Save as: {same-filename}.canvas
       ↓
Link Canvas in markdown note
```

**Canvas Structure:**
```
         🎬 TITLE
              ↓
         📝 RESUMO
              ↓
    ┌────┬────┬────┐
    │ 💡 │ 💡 │ 💡 │  Key learnings (grid layout)
    │ 1  │ 2  │ 3  │
    └────┴────┴────┘
              ↓
    ┌────┬────┬────┐
    │ 🎨 │ 🎨 │ 🎨 │  Pencil drawings (visual aids)
    │ 1  │ 2  │ 3  │
    └────┴────┴────┘
```

**Implementation:**

Use Write tool to create Canvas JSON directly (no external script needed).

**Canvas Generation Steps:**
1. Extract content from markdown note (title, summary, learnings)
2. **Generate 3 pencil drawings** using google-gemini-image skill:
   ```bash
   python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/.claude/skills/google-gemini-image/scripts/generate.py \
       --aspect-ratio 1:1 \
       --format png \
       --output ~/Downloads \
       "Simple childlike pencil sketch of [main concept]" \
       "Hand-drawn crayon illustration of [key process]" \
       "Kids drawing style showing [important takeaway]"
   ```
3. **Save images to organized asset folder** (Canvas requires local files):
   ```bash
   # Create organized folder structure
   VAULT="/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/📺 Vídeos"
   mkdir -p "$VAULT/Assets"
   mkdir -p "$VAULT/Canvas"

   # Move generated images to assets folder
   mv ~/Downloads/[folder]/01_*.png "$VAULT/Assets/[video-slug]-img-1.png"
   mv ~/Downloads/[folder]/02_*.png "$VAULT/Assets/[video-slug]-img-2.png"
   mv ~/Downloads/[folder]/03_*.png "$VAULT/Assets/[video-slug]-img-3.png"
   ```

   **NEW STRUCTURE:**
   ```
   📺 Vídeos/
   ├── [video-name].md          ← Nota principal
   ├── Canvas/                  ← Canvas files organizados (VISÍVEL)
   │   └── [video-name].canvas
   └── Assets/                  ← Imagens organizadas (VISÍVEL)
       ├── [video-name]-img-1.png
       ├── [video-name]-img-2.png
       └── [video-name]-img-3.png
   ```

   **IMPORTANT:** Canvas only supports local file paths, NOT external URLs. Images must be in vault folder.
4. Create Canvas JSON structure with nodes and edges
5. Layout nodes in visual grid:
   - Title: Top center (-200, -400)
   - Summary: Below title (-200, -200)
   - Learnings: Grid layout (2 columns, starting at y=100)
   - Images: Grid layout (3 columns, starting at y=450)
   - Each text node: width=350-500, height=200-260
   - Each image node: width=300, height=300
6. Connect nodes with colored edges (match node colors)
7. Save as `{video-filename}.canvas` in `📺 Vídeos/Canvas/`
8. Add Canvas link in markdown note (relative path: `Canvas/[filename].canvas`)

**Canvas JSON Template (with Images):**
```json
{
  "nodes": [
    {
      "id": "title",
      "type": "text",
      "text": "# 🎬 {TITLE}\n\n**Resumo Visual com Ilustrações**",
      "x": -200,
      "y": -400,
      "width": 500,
      "height": 140,
      "color": "5"
    },
    {
      "id": "summary",
      "type": "text",
      "text": "## 📝 RESUMO\n\n{SUMMARY}",
      "x": -200,
      "y": -200,
      "width": 500,
      "height": 200,
      "color": "3"
    },
    {
      "id": "learning-0",
      "type": "text",
      "text": "## 💡 Aprendizado 1\n\n{LEARNING_1}",
      "x": -600,
      "y": 100,
      "width": 350,
      "height": 200,
      "color": "1"
    },
    {
      "id": "image-0",
      "type": "file",
      "file": "📺 Vídeos/Assets/{video-slug}-img-1.png",
      "x": -600,
      "y": 450,
      "width": 300,
      "height": 300
    },
    {
      "id": "image-1",
      "type": "file",
      "file": "📺 Vídeos/Assets/{video-slug}-img-2.png",
      "x": -150,
      "y": 450,
      "width": 300,
      "height": 300
    },
    {
      "id": "image-2",
      "type": "file",
      "file": "📺 Vídeos/Assets/{video-slug}-img-3.png",
      "x": 300,
      "y": 450,
      "width": 300,
      "height": 300
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "title",
      "fromSide": "bottom",
      "toNode": "summary",
      "toSide": "top",
      "color": "5"
    },
    {
      "id": "e-img-1",
      "fromNode": "summary",
      "fromSide": "bottom",
      "toNode": "image-0",
      "toSide": "top",
      "color": "2"
    }
  ]
}
```

**Node Colors (Obsidian):**
- `"1"` = Red
- `"2"` = Orange
- `"3"` = Yellow
- `"4"` = Green
- `"5"` = Cyan
- `"6"` = Purple

**Layout Math:**
```python
# Grid layout for learnings (text nodes)
cols = 2
x_start = -600
y_start = 100
node_width = 350
node_height = 200
x_gap = 100
y_gap = 50

for idx, learning in enumerate(learnings):
    col = idx % cols
    row = idx // cols
    x = x_start + col * (node_width + x_gap)
    y = y_start + row * (node_height + y_gap)

# Grid layout for images (3 columns below learnings)
img_cols = 3
img_x_start = -600
img_y_start = 450
img_width = 300
img_height = 300
img_x_gap = 150

for idx in range(3):
    x = img_x_start + idx * (img_width + img_x_gap)
    y = img_y_start
```

**Canvas Linking:**

Add to markdown note frontmatter:
```yaml
canvas: "[[Canvas/{filename}.canvas]]"
```

Or add visual link in note body:
```markdown
## 🎨 Resumo Visual

📊 **[Abrir Canvas Interativo](Canvas/{filename}.canvas)**

> Canvas e imagens organizados em:
> - Canvas: `Canvas/{filename}.canvas`
> - Assets: `Assets/{filename}-img-*.png`
```

## Golden Rules

1. **Always use Brazilian datetime** - DD/MM/YYYY HH:mm (never ISO format)
2. **Minimize friction** - Create immediately, don't ask unnecessary questions
3. **Clean filenames** - Lowercase, hyphens, remove special characters
4. **Maintain minimalism** - No visual pollution, simple structure
5. **Latest first** - Newest content at top of lists
6. **Use correct emoji** - Match folder structure exactly (📋 📺 💡)

## Communication Style

Keep responses ultra-concise:
```
✅ Tarefa criada: 📋 Tarefas/implementar-login.md
```

Do not repeat request, explain process, or add unnecessary details unless user asks.

## Additional Resources

- **Templates:** `references/templates.md` - All markdown templates
- **Canvas Images:** `references/CANVAS_IMAGES.md` - **Guide for generating childlike illustrations**
- **Examples:** `EXAMPLES.md` - Real usage examples
- **Reference:** `REFERENCE.md` - Technical details
- **Troubleshooting:** `TROUBLESHOOTING.md` - Common issues
