---
name: grok-image
description: Generate professional images using xAI's Grok Imagine API. Supports single and batch generation with text-to-image capabilities. Auto-invokes when user requests image generation using Grok, multiple images, or mentions Grok Imagine.
---

# Grok Image Generator

Generate professional images using xAI's Grok Imagine text-to-image model.

## Purpose

This skill provides image generation capabilities using xAI's Grok Imagine API. It supports:
- Single image generation from text prompts
- Batch generation of multiple images in parallel
- Configurable aspect ratios (2:3, 3:2, 1:1)
- Automatic download and organization of generated images
- Each generation costs 4 credits ($0.02) and returns 6 images

## When to Use This Skill

Auto-invoke this skill when the user:
- Requests image generation using Grok or Grok Imagine
- Asks to generate multiple images simultaneously
- Mentions "grok image" or "grok imagine"
- Needs professional image generation with specific aspect ratios
- Wants to create images from text descriptions

**Examples:**
- "Generate an image of a sunset using Grok"
- "Create 5 images with Grok Imagine"
- "Use Grok to make an image of a cat"
- "Generate portraits with Grok in 3:2 ratio"

## How to Use This Skill

### Single Image Generation

For generating a single image, use the `generate_grok_image.py` script:

```bash
python3 scripts/generate_grok_image.py <prompt> [aspect_ratio] [output_dir]
```

**Arguments:**
- `prompt` (required): Text description of the image to generate
- `aspect_ratio` (optional): Image ratio - `2:3`, `3:2`, or `1:1` (default: `1:1`)
- `output_dir` (optional): Directory to save images (default: `~/Downloads`)

**Examples:**
```bash
# Basic usage with default settings
python3 scripts/generate_grok_image.py "A serene sunset over the ocean"

# With custom aspect ratio
python3 scripts/generate_grok_image.py "Portrait of a woman in vintage style" 3:2

# With custom output directory
python3 scripts/generate_grok_image.py "Mountain landscape with snow" 16:9 ~/Pictures
```

**Workflow:**
```
User provides prompt
↓
Create task via API
↓
Poll for completion (5s intervals)
↓
Download 6 generated images
↓
Save to output directory
```

### Batch Image Generation

For generating multiple images in parallel, use the `batch_generate_grok.py` script:

```bash
python3 scripts/batch_generate_grok.py <prompt1> [prompt2] [prompt3] ... [--aspect-ratio=1:1] [--output-dir=~/Downloads] [--base-name=image] [--workers=5]
```

**Arguments:**
- `prompt1, prompt2, ...` (required): Multiple text descriptions
- `--aspect-ratio` (optional): Aspect ratio for all images (default: `1:1`)
- `--output-dir` (optional): Main directory to save images (default: `~/Downloads`)
- `--base-name` (optional): Base name for image files (default: `image`)
- `--workers` (optional): Max parallel tasks (default: `5`)

**Folder Structure:**
Each batch generates organized folders:
```
output-dir/
├── Conjunto 1/
│   ├── image_1.jpg
│   ├── image_2.jpg
│   ├── ... (6 images total)
│   └── image_6.jpg
├── Conjunto 2/
│   ├── image_1.jpg
│   └── ... (6 images)
└── Conjunto 3/
    └── ... (6 images)
```

**Examples:**
```bash
# Generate 3 conjuntos in parallel
python3 scripts/batch_generate_grok.py "A sunset" "A cat playing" "A mountain landscape"

# With custom aspect ratio
python3 scripts/batch_generate_grok.py "Portrait 1" "Portrait 2" "Portrait 3" --aspect-ratio=3:2

# With custom output, base name and workers
python3 scripts/batch_generate_grok.py "Person 1" "Person 2" --output-dir=~/Pictures/pessoas --base-name=pessoa --workers=3
```

**Workflow:**
```
User provides multiple prompts
↓
Create all tasks in parallel
↓
Poll each task independently
↓
Download images as tasks complete
↓
Report final statistics
```

### When to Use Batch vs Single

**Use single generation when:**
- User requests only one image
- Immediate feedback is important
- Testing prompts or aspect ratios

**Use batch generation when:**
- User requests 2+ images
- Prompts are variations of a theme
- Time efficiency is important
- Generating at scale (5-10+ images)

### Aspect Ratio Guidelines

Choose aspect ratios based on use case:

- **1:1** (square): Social media posts, profile pictures, thumbnails
- **3:2** (landscape): Photography, presentations, website headers
- **2:3** (portrait): Phone wallpapers, posters, vertical displays

### Output Organization

Generated images are saved with descriptive filenames:

**Single generation:**
```
grok_{task_id}_{image_number}.jpg
Example: grok_e989621f54392584_1.jpg
```

**Batch generation:**
```
grok_batch_{prompt_index}_{task_id}_{image_number}.jpg
Example: grok_batch_1_e989621f54392584_1.jpg
```

This naming ensures:
- Easy identification of generation batches
- Chronological ordering
- No filename conflicts

### API Reference

For detailed API documentation, including endpoints, request/response formats, and error handling, refer to:

```bash
references/grok_api_docs.md
```

Key API details:
- **Endpoint:** `https://api.kie.ai/api/v1/jobs`
- **Model:** `grok-imagine/text-to-image`
- **Pricing:** 4 credits ($0.02) per generation
- **Output:** 6 images per generation
- **Max prompt length:** 5000 characters

### Best Practices

1. **Prompt Quality:**
   - Be specific and descriptive
   - Include style, lighting, mood details
   - Use cinematic/photographic terminology for better results
   - Example: "Cinematic portrait of a woman, soft ambient lighting, warm earthy tones, vintage editorial photography style"

2. **Batch Processing:**
   - Use `--workers=5` for optimal performance
   - Don't exceed 10 parallel tasks to avoid rate limits
   - Group similar prompts together

3. **Error Handling:**
   - Scripts automatically retry on transient failures
   - Check output for failed generations
   - Review API documentation for error codes

4. **Cost Management:**
   - Each generation = 4 credits ($0.02)
   - 6 images per generation
   - Monitor credit usage for large batches

### Troubleshooting

**Task times out:**
- Increase polling attempts in script
- Check API status
- Verify prompt is under 5000 characters

**No images downloaded:**
- Check network connectivity
- Verify output directory permissions
- Review task failure message

**Rate limit errors:**
- Reduce `--workers` count
- Add delays between batch submissions
- Check API rate limits

**Invalid aspect ratio:**
- Use only supported ratios: `2:3`, `3:2`, `1:1`
- Check for typos in command

## Auto-Correction System

This skill includes automatic error correction to prevent recurring issues.

**When errors occur:**

```
Error detected
↓
1. Fix SKILL.md programmatically
   python3 scripts/update_skill.py <old_text> <new_text>
↓
2. Log the learning
   python3 scripts/log_learning.py <error> <fix> [affected_line]
↓
3. LEARNINGS.md updated
↓
4. Error prevented in future
```

**Scripts:**
- `scripts/update_skill.py` - Update SKILL.md automatically
- `scripts/log_learning.py` - Log fixes in LEARNINGS.md
- `assets/LEARNINGS_TEMPLATE.md` - Template for learning entries

**Example:**
```bash
# Fix a command error
python3 scripts/update_skill.py \
    'python3 script.py --prompt "text"' \
    'python3 script.py "text"'

# Log the fix
python3 scripts/log_learning.py \
    "Flag --prompt not recognized" \
    "Removed --prompt flag, using positional argument" \
    "SKILL.md:97"
```

This ensures the same mistake never happens twice and maintains a history of all corrections.

## Configuration

**API Key:** Pre-configured in scripts
- Key: `fa32b7ea4ff0e9b5acce83abe09d2b06`
- Location: Hardcoded in `generate_grok_image.py` and `batch_generate_grok.py`
- Security: For production use, migrate to environment variables

**To use custom API key:**
1. Edit scripts and replace `API_KEY` value, or
2. Set environment variable `GROK_API_KEY` (requires script modification)

## Technical Details

**Dependencies:**
- `requests` - HTTP client for API calls
- Python 3.6+ - Standard library only

**Install dependencies:**
```bash
pip3 install requests
```

**API Configuration:**
- Base URL: `https://api.kie.ai/api/v1/jobs`
- Model: `grok-imagine/text-to-image`
- Authentication: Bearer token
- Timeout: 5 minutes max per task
- Polling interval: 5 seconds

## Examples

### Example 1: Simple Image
```bash
python3 scripts/generate_grok_image.py "A golden retriever playing in a sunny park"
```

### Example 2: Styled Portrait
```bash
python3 scripts/generate_grok_image.py \
    "Cinematic portrait, film noir style, dramatic lighting, black and white" \
    3:2
```

### Example 3: Batch Marketing Assets
```bash
python3 scripts/batch_generate_grok.py \
    "Modern minimalist logo design with geometric shapes" \
    "Vibrant abstract background with gradient colors" \
    "Professional product photo on white background" \
    --aspect-ratio=1:1 \
    --output-dir=~/Projects/marketing-assets
```

### Example 4: Large Scale Generation
```bash
python3 scripts/batch_generate_grok.py \
    "Sunset landscape 1" "Sunset landscape 2" "Sunset landscape 3" \
    "Ocean waves 1" "Ocean waves 2" "Ocean waves 3" \
    "Mountain vista 1" "Mountain vista 2" "Mountain vista 3" \
    --aspect-ratio=3:2 \
    --workers=5
```

## Integration with Other Tools

**Use with file upload tools:**
```bash
# Generate image
python3 scripts/generate_grok_image.py "A cat" 1:1 ~/Downloads

# Upload to cloud (example)
python3 ~/tools/upload_tool.py ~/Downloads/grok_*.jpg
```

**Use in automation workflows:**
```python
from scripts.generate_grok_image import generate_image

# Generate image programmatically
files = generate_image(
    prompt="A professional headshot",
    aspect_ratio="3:2",
    output_dir="/path/to/output"
)

# Use generated files
for file in files:
    process_image(file)
```

## Conclusion

This skill provides a complete workflow for generating professional images using Grok Imagine. It handles API interaction, polling, download, and organization automatically, allowing focus on creative prompt engineering rather than technical implementation.

For detailed API documentation, refer to `references/grok_api_docs.md`.
