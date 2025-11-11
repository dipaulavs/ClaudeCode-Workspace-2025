# Canvas Image Generation Guide

## Overview

When creating Canvas diagrams for YouTube videos, automatically generate 3 childlike pencil drawings to enhance visual learning.

## Image Generation Workflow

```
Extract video content (title, summary, learnings)
       ↓
Identify 3 key concepts to illustrate
       ↓
Generate prompts for childlike drawings
       ↓
Call google-gemini-image skill (3 images)
       ↓
Upload to Nextcloud (permanent links)
       ↓
Embed in Canvas as file nodes
```

## Prompt Engineering for Childlike Drawings

**Style keywords to use:**
- "Simple childlike pencil sketch"
- "Hand-drawn crayon illustration"
- "Kids drawing style"
- "Kindergarten art style"
- "Naive art pencil drawing"
- "Scribbled with colored pencils"

**What to avoid:**
- Professional/polished artwork
- Realistic photography
- Complex digital art
- Too many details

## Example Prompts

### Video: "How Photosynthesis Works"

**Image 1 - Main Concept:**
```
Simple childlike pencil sketch of a smiling sun shining on a happy green leaf, kindergarten art style, crayon drawing on white paper
```

**Image 2 - Process:**
```
Hand-drawn crayon illustration of water drops going up a plant stem with arrows, kids drawing style, simple and colorful
```

**Image 3 - Result:**
```
Kids drawing style showing a tree releasing oxygen bubbles, naive art with colored pencils, happy tree character
```

### Video: "Async Python Tutorial"

**Image 1 - Main Concept:**
```
Simple childlike pencil sketch of multiple tasks running at the same time with arrows, kindergarten art style
```

**Image 2 - Event Loop:**
```
Hand-drawn crayon illustration of a circular loop with tasks inside, kids drawing style, colorful and simple
```

**Image 3 - Benefit:**
```
Kids drawing style showing a fast rocket representing speed, naive art pencil drawing, happy rocket character
```

## Generation Commands

### Using google-gemini-image skill

```bash
# Generate 3 images with childlike style
python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/.claude/skills/google-gemini-image/scripts/generate.py \
    --aspect-ratio 1:1 \
    --format png \
    --output ~/Downloads \
    "Simple childlike pencil sketch of [CONCEPT_1]" \
    "Hand-drawn crayon illustration of [CONCEPT_2]" \
    "Kids drawing style showing [CONCEPT_3]"
```

**Settings:**
- **Aspect ratio:** `1:1` (square, perfect for Canvas nodes)
- **Format:** `png` (supports transparency if needed)
- **Output:** `~/Downloads` (temporary, will upload to Nextcloud)

## Upload to Nextcloud

After generation, upload images to get permanent links:

```bash
# Upload each image
python3 SCRIPTS/nextcloud/upload_rapido.py ~/Downloads/simple-childlike-pencil-sketch-of-concept-1.png
python3 SCRIPTS/nextcloud/upload_rapido.py ~/Downloads/hand-drawn-crayon-illustration-of-concept-2.png
python3 SCRIPTS/nextcloud/upload_rapido.py ~/Downloads/kids-drawing-style-showing-concept-3.png
```

**Result:** Permanent public URLs
```
https://media.loop9.com.br/s/abc123/download/image1.png
https://media.loop9.com.br/s/def456/download/image2.png
https://media.loop9.com.br/s/ghi789/download/image3.png
```

## Canvas Integration

### Image Node Structure

```json
{
  "id": "image-0",
  "type": "file",
  "file": "https://media.loop9.com.br/s/abc123/download/image1.png",
  "x": -600,
  "y": 450,
  "width": 300,
  "height": 300
}
```

**Key fields:**
- `type`: Must be `"file"` for images
- `file`: Full Nextcloud public URL
- `width/height`: `300x300` works well for square images

### Layout Grid (3 images)

```
     Image 1           Image 2           Image 3
   x: -600           x: -150            x: 300
   y: 450            y: 450             y: 450
   300x300           300x300            300x300
```

**Spacing:** 150px gap between images

## Content Selection Strategy

Choose 3 key concepts from the video to illustrate:

**Priority order:**
1. **Main concept/topic** - What is the video fundamentally about?
2. **Key process/workflow** - How does it work?
3. **Important takeaway** - What's the practical benefit/result?

**Example mapping:**

| Video Type | Image 1 | Image 2 | Image 3 |
|------------|---------|---------|---------|
| Tutorial | Main feature | Step-by-step process | End result |
| Concept explanation | Core idea | How it works | Real-world example |
| News/update | What changed | Impact | Future implications |

## Quality Guidelines

**Good childlike drawings have:**
- ✅ Simple shapes (circles, squares, stick figures)
- ✅ Bright, primary colors
- ✅ Imperfect lines (hand-drawn feel)
- ✅ Happy/smiling characters
- ✅ Minimal details
- ✅ Clear single focus

**Avoid:**
- ❌ Photorealistic rendering
- ❌ Complex perspectives
- ❌ Too many elements
- ❌ Dark/serious tones
- ❌ Abstract concepts without visual metaphors

## Error Handling

**If image generation fails:**
1. Continue with text-only Canvas
2. Log error for debugging
3. Don't block Canvas creation

**If upload fails:**
1. Use local file path (temporary fallback)
2. Warn user about non-permanent link
3. Canvas still functional

## Performance Considerations

**Timing:**
- Image generation: ~6-8 seconds (3 images concurrent)
- Upload: ~2-3 seconds (3 files)
- Total overhead: ~10 seconds per video

**Cost:**
- 3 images × $0.039 = $0.117 per video
- Affordable for enhanced learning experience

## Future Enhancements

Potential improvements:
- Generate image variations (A/B testing visuals)
- Add text captions to images
- Create GIF animations for processes
- Link images to specific learning nodes
- Generate concept maps from keywords

---

**Created:** 08/11/2025
**Purpose:** Guide for generating childlike illustrations in Canvas
**Status:** ✅ Active
