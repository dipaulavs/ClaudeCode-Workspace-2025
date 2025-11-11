# OpenAI GPT Image 1 Mini - Complete API Reference

This document provides comprehensive API documentation for OpenAI's GPT Image 1 Mini model.

## Model Overview

**Model ID:** `gpt-image-1-mini`
- **Type:** Cost-efficient image generation
- **Performance:** Higher quality than DALL-E 2, lower cost than GPT Image 1
- **Speed:** Slowest (higher quality takes time)
- **Input:** Text prompts (up to 32,000 characters) + optional images (for edits)
- **Output:** Base64-encoded images (PNG, JPEG, WEBP)

## Pricing

### Image Generation (per image)

**Low Quality:**
- 1024x1024: $0.005
- 1024x1536: $0.006
- 1536x1024: $0.006

**Medium Quality:**
- 1024x1024: $0.011
- 1024x1536: $0.015
- 1536x1024: $0.015

**High Quality:**
- 1024x1024: $0.036
- 1024x1536: $0.052
- 1536x1024: $0.052

### Token Usage

**Text Tokens (per 1M tokens):**
- Input: $2.00
- Cached input: $0.20

**Image Tokens (per 1M tokens):**
- Input: $2.50
- Cached input: $0.25
- Output: $8.00

## API Endpoints

### 1. Image Generation

**Endpoint:** `POST https://api.openai.com/v1/images/generations`

**Purpose:** Create new images from text prompts

**Request Body:**

```json
{
  "model": "gpt-image-1-mini",
  "prompt": "A cute baby sea otter",
  "n": 1,
  "size": "1024x1024",
  "quality": "auto",
  "background": "auto",
  "output_format": "png",
  "output_compression": 100,
  "partial_images": 0,
  "stream": false,
  "moderation": "auto"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | Yes | - | Must be "gpt-image-1-mini" |
| `prompt` | string | Yes | - | Text description (max 32,000 chars) |
| `n` | integer | No | 1 | Number of images (1-10) |
| `size` | string | No | "auto" | "1024x1024", "1536x1024", "1024x1536", "auto" |
| `quality` | string | No | "auto" | "low", "medium", "high", "auto" |
| `background` | string | No | "auto" | "transparent", "opaque", "auto" |
| `output_format` | string | No | "png" | "png", "jpeg", "webp" |
| `output_compression` | integer | No | 100 | 0-100 (WebP/JPEG only) |
| `partial_images` | integer | No | 0 | 0-3 (streaming only) |
| `stream` | boolean | No | false | Enable streaming mode |
| `moderation` | string | No | "auto" | "low", "auto" |
| `user` | string | No | - | Unique identifier for end-user |

**Response:**

```json
{
  "created": 1713833628,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "background": "transparent",
  "output_format": "png",
  "size": "1024x1024",
  "quality": "high",
  "usage": {
    "total_tokens": 100,
    "input_tokens": 50,
    "output_tokens": 50,
    "input_tokens_details": {
      "text_tokens": 10,
      "image_tokens": 40
    }
  }
}
```

**Python Example:**

```python
import base64
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="gpt-image-1-mini",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024",
    quality="high",
    background="transparent",
    output_format="png"
)

# Decode and save
image_bytes = base64.b64decode(response.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

### 2. Image Edit

**Endpoint:** `POST https://api.openai.com/v1/images/edits`

**Purpose:** Edit or extend existing images with text prompts

**Request Body (multipart/form-data):**

```
image: [binary file or array of files]
prompt: "Add a hat to the person"
mask: [optional binary file]
model: "gpt-image-1-mini"
n: 1
size: "1024x1024"
quality: "auto"
background: "auto"
output_format: "png"
input_fidelity: "low"
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | file/array | Yes | - | PNG/WebP/JPG < 50MB (up to 16 images) |
| `prompt` | string | Yes | - | Text description (max 32,000 chars) |
| `mask` | file | No | - | Transparent areas = edit zones (PNG) |
| `model` | string | No | "dall-e-2" | "gpt-image-1-mini" or "dall-e-2" |
| `n` | integer | No | 1 | Number of images (1-10) |
| `size` | string | No | "1024x1024" | Same as generation |
| `quality` | string | No | "auto" | "low", "medium", "high", "auto" |
| `background` | string | No | "auto" | "transparent", "opaque", "auto" |
| `output_format` | string | No | "png" | "png", "jpeg", "webp" |
| `input_fidelity` | string | No | "low" | "low", "high" (GPT Image 1 only) |
| `stream` | boolean | No | false | Enable streaming mode |

**Python Example:**

```python
import base64
from openai import OpenAI

client = OpenAI()

result = client.images.edit(
    model="gpt-image-1-mini",
    image=[
        open("body-lotion.png", "rb"),
        open("bath-bomb.png", "rb"),
        open("incense-kit.png", "rb"),
        open("soap.png", "rb"),
    ],
    prompt="Create a gift basket with all these items on white background"
)

# Save result
image_bytes = base64.b64decode(result.data[0].b64_json)
with open("gift-basket.png", "wb") as f:
    f.write(image_bytes)
```

## Advanced Features

### Transparent Backgrounds

**Requirements:**
- `background: "transparent"`
- `output_format: "png"` or `"webp"` (NOT jpeg)

**Example:**

```python
response = client.images.generate(
    model="gpt-image-1-mini",
    prompt="Minimalist tech logo",
    background="transparent",
    output_format="png"
)
```

### Streaming Mode

**Purpose:** Get partial images during generation

**Parameters:**
- `stream: true`
- `partial_images: 1-3` (number of partial images to receive)

**Events:**
- `image_generation.partial_image` - Progressive image updates
- `image_generation.completed` - Final image

**Python Example:**

```python
stream = client.images.generate(
    model="gpt-image-1-mini",
    prompt="A landscape painting",
    stream=True,
    partial_images=3
)

for event in stream:
    if event.type == "image_generation.partial_image":
        print(f"Received partial image {event.partial_image_index}")
        # Decode and display partial image
        image_bytes = base64.b64decode(event.b64_json)

    elif event.type == "image_generation.completed":
        print("Final image received")
        final_image = base64.b64decode(event.b64_json)
```

### Batch Generation with Custom Compression

**Example:**

```python
from concurrent.futures import ThreadPoolExecutor

def generate_image(prompt):
    return client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        quality="medium",
        output_format="webp",
        output_compression=80  # 80% quality = smaller files
    )

prompts = [
    "Product photo 1",
    "Product photo 2",
    "Product photo 3"
]

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(generate_image, prompts))
```

## Rate Limits

### Limits by Tier (gpt-image-1-mini)

| Tier | TPM (Tokens/min) | IPM (Images/min) |
|------|------------------|------------------|
| Free | Not supported | Not supported |
| 1 | 100,000 | 5 |
| 2 | 250,000 | 20 |
| 3 | 800,000 | 50 |
| 4 | 3,000,000 | 150 |
| 5 | 8,000,000 | 250 |

**Note:** Rate limits apply per organization, not per API key.

### Handling Rate Limits

**Error Response:**

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "param": null,
    "code": "rate_limit_exceeded"
  }
}
```

**Best Practices:**
1. Implement exponential backoff
2. Match concurrent workers to your tier
3. Monitor usage via OpenAI dashboard
4. Cache results when possible

## Content Moderation

### Moderation Levels

**`moderation: "auto"` (default):**
- Standard OpenAI content policy
- Blocks harmful, violent, sexual, hateful content

**`moderation: "low"`:**
- Less restrictive filtering
- Allows more artistic freedom
- Still blocks clearly harmful content

**Moderation Errors:**

```json
{
  "error": {
    "message": "Your request was rejected as a result of our safety system",
    "type": "content_policy_violation",
    "code": "content_policy_violation"
  }
}
```

## Error Handling

### Common Errors

**Authentication Error:**

```json
{
  "error": {
    "message": "Incorrect API key provided",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

**Invalid Parameters:**

```json
{
  "error": {
    "message": "Invalid value for 'size'. Must be one of: 1024x1024, 1536x1024, 1024x1536, auto",
    "type": "invalid_request_error",
    "param": "size"
  }
}
```

**Image Too Large:**

```json
{
  "error": {
    "message": "Image file size must be less than 50MB",
    "type": "invalid_request_error",
    "param": "image"
  }
}
```

### Python Error Handling

```python
from openai import OpenAI, OpenAIError, RateLimitError, APIError

client = OpenAI()

try:
    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt="A beautiful landscape"
    )
except RateLimitError:
    print("Rate limit exceeded. Please try again later.")
except APIError as e:
    print(f"API error occurred: {e}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

## Best Practices

### 1. Prompt Engineering

**Good prompts:**
- Specific: "Photorealistic portrait of a woman in her 30s with brown hair"
- Detailed: Include style, lighting, composition details
- Contextual: "Product photo on white background with soft shadows"

**Poor prompts:**
- Vague: "A person"
- Too short: "Tree"
- Contradictory: "Bright dark night scene"

### 2. Quality vs Cost

**Use `quality: "high"` when:**
- Print materials needed
- Professional photography
- Marketing hero images

**Use `quality: "medium"` when:**
- Social media posts
- Web graphics
- General use

**Use `quality: "low"` when:**
- Rapid prototyping
- Thumbnails
- Testing prompts

### 3. Format Selection

**PNG:**
- Best for: Logos, graphics, transparency
- Pros: Lossless, supports transparency
- Cons: Large file size

**JPEG:**
- Best for: Photographs, web images
- Pros: Small file size
- Cons: No transparency, lossy compression

**WebP:**
- Best for: Modern web applications
- Pros: Best compression, supports transparency
- Cons: Limited older browser support

### 4. Background Optimization

**Transparent backgrounds:**
- Perfect for: Logos, icons, overlays
- Requirement: PNG or WebP format

**Opaque backgrounds:**
- Better for: Photographs, hero images
- Smaller file size with JPEG

**Auto:**
- Model decides best option
- Good for general use

## Security Considerations

### API Key Management

**DO:**
- Store in environment variables
- Use separate keys per environment
- Rotate keys regularly
- Monitor usage dashboard

**DON'T:**
- Hardcode in source code
- Commit to version control
- Share publicly
- Reuse across projects

### User Input Validation

**Always validate:**
- Prompt length (< 32,000 chars)
- Number of images (1-10)
- File sizes (< 50MB for edits)
- File types (PNG, WebP, JPG only)

**Example:**

```python
def validate_prompt(prompt: str) -> bool:
    if len(prompt) > 32000:
        raise ValueError("Prompt too long (max 32,000 characters)")
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    return True
```

## Migration Guide

### From DALL-E 2 to GPT Image 1 Mini

**Key Differences:**

| Feature | DALL-E 2 | GPT Image 1 Mini |
|---------|----------|------------------|
| Prompt length | 1,000 chars | 32,000 chars |
| Quality options | "standard" only | "low", "medium", "high", "auto" |
| Response format | URL or base64 | Base64 only |
| Transparency | No | Yes |
| Streaming | No | Yes |
| Pricing | Higher | Lower (for same quality) |

**Migration Example:**

```python
# DALL-E 2 (old)
response = client.images.generate(
    model="dall-e-2",
    prompt="A cute otter",
    size="1024x1024",
    response_format="url"
)
url = response.data[0].url

# GPT Image 1 Mini (new)
response = client.images.generate(
    model="gpt-image-1-mini",
    prompt="A cute otter",
    size="1024x1024",
    quality="medium"  # Similar to DALL-E 2 quality
)
image_bytes = base64.b64decode(response.data[0].b64_json)
```

## Additional Resources

- **OpenAI Documentation:** https://platform.openai.com/docs/guides/images
- **API Reference:** https://platform.openai.com/docs/api-reference/images
- **Pricing Calculator:** https://openai.com/pricing
- **Community Forum:** https://community.openai.com/
- **Status Page:** https://status.openai.com/
