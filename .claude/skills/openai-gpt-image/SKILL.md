---
name: openai-gpt-image
description: Generate professional images with OpenAI GPT Image 1 Mini. Supports batch generation (1-20 images simultaneously) with concurrent API calls. Auto-invokes when user requests image generation, multiple images, or mentions OpenAI/GPT image generation.
---

# OpenAI GPT Image Generator

Generate high-quality images using OpenAI's GPT Image 1 Mini model with support for batch processing (1-20 images concurrently).

## When to Use This Skill

Auto-invoke when user requests:
- **Image generation**: "Create an image of...", "Generate a picture of..."
- **Multiple images**: "Generate 5 images of...", "Create several variations of..."
- **OpenAI-specific requests**: "Use OpenAI to create...", "GPT image of..."
- **Batch processing**: "Generate images for these prompts: ..."

## Model Information

**Model:** `gpt-image-1-mini`
- **Type:** Cost-efficient image generation
- **Input:** Text prompts (up to 32,000 characters)
- **Output:** Base64-encoded images (PNG, JPEG, WEBP)
- **Pricing:** $0.005-$0.052 per image (quality/size dependent)

## Core Workflow

### Single Image Generation

```bash
python3 scripts/generate.py "A cute baby sea otter"
```

**Output:**
```
🎨 Generating 1 image(s) with gpt-image-1-mini...
📁 Output: /Users/user/Downloads
⚙️  Settings: quality=medium, size=auto, format=png

✅ Image 1/1: a-cute-baby-sea-otter.png
   Tokens: 1593 (in: 9, out: 1584)

🎉 Generated 1/1 images successfully
```

**Note:** Single images are saved with descriptive filenames based on the prompt.

### Batch Generation (2-20 Images)

```bash
python3 scripts/generate.py \
    "A sunset over mountains" \
    "A futuristic city at night" \
    "A serene lake with reflections"
```

**Output:**
```
🎨 Generating 3 image(s) with gpt-image-1-mini...
📁 Output: /Users/user/Downloads/a-sunset-over-a-futuristic-city-a-serene-lake-with
⚙️  Settings: quality=medium, size=auto, format=png

✅ Image 1/3: 01_a-sunset-over-mountains.png
   Tokens: 1593 (in: 9, out: 1584)
✅ Image 2/3: 02_a-futuristic-city-at-night.png
   Tokens: 1593 (in: 9, out: 1584)
✅ Image 3/3: 03_a-serene-lake-with-reflections.png
   Tokens: 1593 (in: 9, out: 1584)

🎉 Generated 3/3 images successfully
```

**Note:** Multiple images are automatically organized in a descriptive folder. The folder name is created from the prompts (first 3 prompts, or "+ N more" if more than 3).

## Advanced Options

### Quality Levels

```bash
# High quality ($0.036-$0.052 per image)
python3 scripts/generate.py --quality high "A photorealistic portrait"

# Medium quality ($0.011-$0.015 per image)
python3 scripts/generate.py --quality medium "A landscape painting"

# Low quality ($0.005-$0.006 per image)
python3 scripts/generate.py --quality low "A quick sketch"

# Auto (model chooses best quality)
python3 scripts/generate.py --quality auto "An abstract art piece"
```

### Image Sizes

```bash
# Square (1024x1024)
python3 scripts/generate.py --size 1024x1024 "A logo design"

# Landscape (1536x1024)
python3 scripts/generate.py --size 1536x1024 "A wide panorama"

# Portrait (1024x1536)
python3 scripts/generate.py --size 1024x1536 "A tall building"

# Auto (model chooses best size)
python3 scripts/generate.py --size auto "A general image"
```

### Output Formats

```bash
# PNG (default, supports transparency)
python3 scripts/generate.py --format png "A logo with transparent background"

# JPEG (smaller file size)
python3 scripts/generate.py --format jpeg "A photograph"

# WebP (best compression)
python3 scripts/generate.py --format webp --compression 80 "An optimized image"
```

### Background Types

```bash
# Transparent background (PNG/WebP only)
python3 scripts/generate.py --background transparent --format png "A logo design"

# Opaque background
python3 scripts/generate.py --background opaque "A solid background image"

# Auto (model decides)
python3 scripts/generate.py --background auto "An image"
```

### Custom Output Directory

```bash
# Save to specific directory
python3 scripts/generate.py --output ~/Pictures/ai-art "A masterpiece"

# Multiple images to custom location
python3 scripts/generate.py --output ~/Desktop/batch \
    "Image 1" "Image 2" "Image 3"
```

### Concurrent Workers

```bash
# Maximum 20 concurrent API calls (faster but higher API load)
python3 scripts/generate.py --workers 20 "Prompt 1" "Prompt 2" ... "Prompt 20"

# Conservative 5 workers (slower but lower API load)
python3 scripts/generate.py --workers 5 "Prompt 1" "Prompt 2" "Prompt 3"
```

## Common Use Cases

### 1. Generate Marketing Assets

```bash
python3 scripts/generate.py \
    --quality high \
    --size 1536x1024 \
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
    --background transparent \
    --format png \
    --output ~/Logos \
    "Minimalist tech logo with blue gradient" \
    "Geometric abstract logo in purple tones" \
    "Modern circular logo with mountain silhouette"
```

### 3. Generate Social Media Content

```bash
python3 scripts/generate.py \
    --size 1024x1536 \
    --quality medium \
    --output ~/Social/Instagram \
    "Inspirational quote on mountain background" \
    "Product flatlay photography style" \
    "Cozy coffee shop aesthetic"
```

### 4. Batch Generate Illustrations

```bash
python3 scripts/generate.py \
    --quality high \
    --workers 15 \
    --output ~/Illustrations \
    "Watercolor forest scene" \
    "Digital art cyberpunk city" \
    "Oil painting style sunset" \
    "Pencil sketch portrait" \
    "Abstract geometric patterns"
```

## Technical Details

### Batch Processing Architecture

The script uses Python's `concurrent.futures.ThreadPoolExecutor` to process multiple images simultaneously:

```
User provides 10 prompts
↓
ThreadPoolExecutor (max_workers=10)
├─> API call 1 (concurrent)
├─> API call 2 (concurrent)
├─> API call 3 (concurrent)
├─> ... (all run simultaneously)
└─> API call 10 (concurrent)
↓
Images saved as they complete
```

**Benefits:**
- **Speed**: 10x faster than sequential generation
- **Efficiency**: Maximizes API throughput
- **Reliability**: Individual failures don't block other images

### Rate Limits

**OpenAI API Rate Limits (gpt-image-1-mini):**
- **Tier 1**: 5 images/min
- **Tier 2**: 20 images/min
- **Tier 3**: 50 images/min
- **Tier 4**: 150 images/min
- **Tier 5**: 250 images/min

**Recommendation:** Adjust `--workers` based on your tier to avoid rate limit errors.

### Environment Setup

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-..."

# Install dependencies
pip install openai
```

### Error Handling

The script gracefully handles errors:
- **Individual failures**: Skipped, other images continue
- **API errors**: Logged with clear error messages
- **Rate limits**: Caught and reported
- **Invalid prompts**: Validated before API calls

## Reference Documentation

For detailed API parameters, pricing, and advanced features, see:
- `references/api_reference.md` - Complete OpenAI GPT Image API documentation
- `references/pricing.md` - Detailed pricing breakdown by quality/size

## Auto-Correction System

This skill includes automatic error correction:

### When a Command Fails

```bash
# 1. Fix SKILL.md
python3 scripts/update_skill.py "<old_text>" "<new_text>"

# 2. Log the learning
python3 scripts/log_learning.py "<error>" "<fix>" "SKILL.md:line"
```

**Example:**

```bash
# Error: Wrong parameter name
python3 scripts/update_skill.py \
    '--output-format png' \
    '--format png'

python3 scripts/log_learning.py \
    "Parameter --output-format not recognized" \
    "Changed to --format (correct parameter name)" \
    "SKILL.md:145"
```

This creates/updates `LEARNINGS.md` with all fixes, preventing repeat errors.

## Troubleshooting

### Issue: "OPENAI_API_KEY environment variable not set"

**Fix:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Issue: Rate limit exceeded

**Fix:**
```bash
# Reduce workers to match your tier
python3 scripts/generate.py --workers 5 "prompt"
```

### Issue: Transparent background not working

**Fix:**
```bash
# Use PNG or WebP format
python3 scripts/generate.py --background transparent --format png "logo"
```

### Issue: File size too large

**Fix:**
```bash
# Use WebP with compression
python3 scripts/generate.py --format webp --compression 80 "image"
```

## Best Practices

1. **Batch efficiently**: Group similar prompts together
2. **Choose quality wisely**: Use `high` only when necessary (3-10x more expensive)
3. **Optimize format**: WebP offers best compression, PNG for transparency
4. **Match workers to tier**: Don't exceed your API rate limits
5. **Use descriptive prompts**: More detail = better results
6. **Set appropriate size**: Match your use case (social media, print, web)

## Limitations

- **Maximum prompts**: 20 per batch
- **Prompt length**: 32,000 characters max
- **No streaming**: Images returned when complete (no partial images with `n=1`)
- **API key required**: Must have valid OpenAI API key
- **Rate limits**: Depend on your OpenAI tier

## Examples

### Generate 10 Product Images

```bash
python3 scripts/generate.py \
    --quality medium \
    --size 1024x1024 \
    --format webp \
    --workers 10 \
    --output ~/Products \
    "Wireless headphones on white background" \
    "Smartwatch with black band closeup" \
    "Laptop on minimalist desk" \
    "Phone with gradient wallpaper" \
    "Camera with prime lens" \
    "Tablet showing design app" \
    "Mechanical keyboard RGB lighting" \
    "Gaming mouse on mousepad" \
    "USB-C hub with cables" \
    "Portable speaker on wood surface"
```

### Create 5 Logo Variations

```bash
python3 scripts/generate.py \
    --background transparent \
    --quality high \
    --format png \
    --output ~/Logos/variations \
    "Modern letter A logo geometric blue gradient" \
    "Abstract mountain peak logo minimalist green" \
    "Tech startup logo circuit board pattern purple" \
    "Coffee shop logo steaming cup brown tones" \
    "Fitness brand logo dynamic motion red orange"
```

### Generate Social Media Posts

```bash
python3 scripts/generate.py \
    --size 1024x1536 \
    --quality medium \
    --format jpeg \
    --output ~/Social \
    "Motivational quote over sunrise landscape" \
    "Product showcase flatlay photography" \
    "Behind the scenes office culture" \
    "Customer testimonial with happy person" \
    "New product announcement with spotlight"
```
