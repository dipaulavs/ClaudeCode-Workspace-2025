---
name: google-gemini-image
description: Generate professional images with Google Gemini 2.5 Flash Image (Nanobanana). Supports async batch generation (1-10 images concurrently). Auto-invokes when user requests image generation using Google/Gemini, multiple images, or mentions Nanobanana.
---

# Google Gemini Image Generator

Generate high-quality images using Google's Gemini 2.5 Flash Image model (nicknamed "Nanobanana") with support for async batch processing (1-10 images concurrently).

## When to Use This Skill

Auto-invoke when user requests:
- **Image generation with Google**: "Use Gemini to create...", "Generate with Google AI..."
- **Multiple images**: "Generate 5 images of...", "Create several variations of..."
- **Nanobanana-specific requests**: "Use Nanobanana to create...", "Gemini 2.5 Flash Image of..."
- **Batch processing**: "Generate images for these prompts: ..."

## Model Information

**Model:** `gemini-2.5-flash-image`
- **Nickname:** Nanobanana
- **Type:** Fast, cost-efficient image generation
- **Input:** Text prompts (conversational)
- **Output:** High-quality images (up to 1024x1024px base, extended formats up to 1344x768)
- **Pricing:** $0.039 per image (~3.5x cheaper than GPT-4 Image high quality)

## Core Workflow

### Single Image Generation

```bash
python3 scripts/generate.py "A cute baby sea otter"
```

**Output:**
```
🎨 Generating 1 image(s) with gemini-2.5-flash-image...
📁 Output: /Users/user/Downloads
⚙️  Settings: aspect_ratio=4:5, format=png

✅ Image 1/1: a-cute-baby-sea-otter.png
   Tokens: 1290

🎉 Generated 1/1 images successfully
```

**Note:** Single images are saved with descriptive filenames based on the prompt.

### Batch Generation (2-10 Images)

```bash
python3 scripts/generate.py \
    "A sunset over mountains" \
    "A futuristic city at night" \
    "A serene lake with reflections"
```

**Output:**
```
🎨 Generating 3 image(s) with gemini-2.5-flash-image...
📁 Output: /Users/user/Downloads/a-sunset-over-a-futuristic-city-a-serene-lake-with
⚙️  Settings: aspect_ratio=4:5, format=png

✅ Image 1/3: 01_a-sunset-over-mountains.png
   Tokens: 1290
✅ Image 2/3: 02_a-futuristic-city-at-night.png
   Tokens: 1290
✅ Image 3/3: 03_a-serene-lake-with-reflections.png
   Tokens: 1290

🎉 Generated 3/3 images successfully
```

**Note:** Multiple images are automatically organized in a descriptive folder. All images are generated concurrently using asyncio for maximum speed (~2.1s per image with 10+ concurrent requests).

## Advanced Options

### Aspect Ratios

```bash
# Square (1024x1024)
python3 scripts/generate.py --aspect-ratio 1:1 "A logo design"

# Widescreen (1344x768)
python3 scripts/generate.py --aspect-ratio 16:9 "A wide panorama"

# Portrait (768x1344)
python3 scripts/generate.py --aspect-ratio 9:16 "A tall building"

# Other supported ratios
python3 scripts/generate.py --aspect-ratio 3:2 "A landscape photo"
python3 scripts/generate.py --aspect-ratio 4:3 "A classic photo"
```

**Supported aspect ratios:**
- 4:5 (1080x1350) - Instagram feed posts (DEFAULT)
- 1:1 (1024x1024) - Square
- 16:9 (1344x768) - Widescreen
- 9:16 (768x1344) - Stories/Reels
- 3:2, 2:3 - Photo formats
- 4:3, 3:4 - Classic formats

### Output Formats

```bash
# PNG (default, supports transparency)
python3 scripts/generate.py --format png "A logo with transparent background"

# JPEG (smaller file size, no transparency)
python3 scripts/generate.py --format jpeg "A photograph"

# WebP (best compression)
python3 scripts/generate.py --format webp "An optimized image"
```

### Custom Output Directory

```bash
# Save to specific directory
python3 scripts/generate.py --output ~/Pictures/ai-art "A masterpiece"

# Multiple images to custom location
python3 scripts/generate.py --output ~/Desktop/batch \
    "Image 1" "Image 2" "Image 3"
```

### Using Custom API Key

```bash
# Pass API key directly (overrides GOOGLE_API_KEY env var)
python3 scripts/generate.py --api-key "YOUR_API_KEY" "A beautiful sunset"
```

**Default API Key:** The script uses `GOOGLE_API_KEY` environment variable by default.

## Common Use Cases

### 1. Generate Marketing Assets

```bash
python3 scripts/generate.py \
    --aspect-ratio 16:9 \
    --format webp \
    --output ~/Marketing/assets \
    "A modern tech startup office" \
    "A team collaborating on a project" \
    "A sleek product showcase"
```

**Result:** Creates folder `~/Marketing/assets/a-modern-tech-a-team-collaborating-a-sleek-product/` containing:
- `01_a-modern-tech-startup-office.webp`
- `02_a-team-collaborating-on-a-project.webp`
- `03_a-sleek-product-showcase.webp`

### 2. Create Logo Variations

```bash
python3 scripts/generate.py \
    --aspect-ratio 1:1 \
    --format png \
    --output ~/Logos \
    "Minimalist tech logo with blue gradient" \
    "Geometric abstract logo in purple tones" \
    "Modern circular logo with mountain silhouette"
```

### 3. Generate Social Media Content

```bash
python3 scripts/generate.py \
    --aspect-ratio 9:16 \
    --format jpeg \
    --output ~/Social \
    "Inspirational quote over sunrise landscape" \
    "Product showcase flatlay photography" \
    "Behind the scenes office culture"
```

### 4. Batch Generate Illustrations

```bash
python3 scripts/generate.py \
    --output ~/Illustrations \
    "Watercolor forest scene" \
    "Digital art cyberpunk city" \
    "Oil painting style sunset" \
    "Pencil sketch portrait" \
    "Abstract geometric patterns"
```

## Technical Details

### Async Batch Processing

The script uses Python's `asyncio` to process multiple images simultaneously:

```
User provides 5 prompts
↓
asyncio.gather() creates 5 concurrent tasks
├─> API call 1 (async)
├─> API call 2 (async)
├─> API call 3 (async)
├─> API call 4 (async)
└─> API call 5 (async)
↓
Images saved as they complete
```

**Benefits:**
- **Speed**: ~2.1s per image with 10+ concurrent requests (vs 3.2s sequential)
- **Efficiency**: Maximizes API throughput
- **Reliability**: Individual failures don't block other images

### Rate Limits

**Google Gemini API Rate Limits:**
- **Standard accounts**: 1,000 requests/minute
- **Concurrent requests**: Up to 10 per API key
- **Enterprise accounts**: Higher limits via quota adjustment

**Recommendation:** The script supports up to 10 concurrent images to respect API limits.

### Pricing Comparison

**Gemini 2.5 Flash Image:**
- $0.039 per image (1290 tokens fixed)
- ~$30 per 1M tokens

**vs OpenAI GPT-4 Image:**
- High quality: $0.036-$0.052 per image
- Medium quality: $0.011-$0.015 per image

**Winner:** Gemini is ~3.5x cheaper than GPT-4 high quality

### Environment Setup

```bash
# Install dependencies
pip install google-genai pillow

# Set API key
export GOOGLE_API_KEY="your-api-key-here"

# Or pass directly to script
python3 scripts/generate.py --api-key "your-key" "prompt"
```

### Error Handling

The script gracefully handles errors:
- **Individual failures**: Skipped, other images continue
- **API errors**: Logged with clear error messages
- **Rate limits**: Caught and reported
- **Invalid prompts**: Validated before API calls

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
    'python3 script.py --prompt "text"' \
    'python3 script.py "text"'

# 2. Log the learning
python3 scripts/log_learning.py \
    "Flag --prompt not recognized" \
    "Removed --prompt flag, using positional argument" \
    "SKILL.md:97"
```

This creates a history of improvements and ensures mistakes don't repeat.
