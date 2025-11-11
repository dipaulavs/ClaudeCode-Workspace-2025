# Google Gemini Image MCP Server

MCP server for generating images using Google's Gemini 2.5 Flash Image model (nicknamed "Nanobanana").

## Features

- **Single image generation** with `generate_image` tool
- **Batch generation** (1-10 images) with `generate_batch_images` tool
- **Async concurrent processing** for maximum speed (~2.1s per image)
- **Multiple aspect ratios**: 1:1, 16:9, 9:16, 4:5, 3:2, 2:3, 4:3, 3:4
- **Multiple formats**: PNG, JPEG, WebP
- **Automatic file organization** with descriptive names

## Model Information

- **Model**: `gemini-2.5-flash-image`
- **Nickname**: Nanobanana
- **Pricing**: ~$0.039 per image (1290 tokens)
- **Max concurrent**: 10 images per API key
- **Output**: Up to 1344x768 resolution

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export GOOGLE_API_KEY="your-api-key-here"
```

## Claude Desktop Configuration

Add to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google-gemini-image": {
      "command": "python",
      "args": [
        "/absolute/path/to/MCPS/google-gemini-image/server.py"
      ],
      "env": {
        "GOOGLE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tools

### generate_image

Generate a single image with Google Gemini 2.5 Flash Image.

**Parameters:**
- `prompt` (required): Text description of desired image
- `aspect_ratio` (optional): Image aspect ratio (default: 4:5)
  - Options: 1:1, 16:9, 9:16, 4:5, 3:2, 2:3, 4:3, 3:4
- `output_format` (optional): Output format (default: png)
  - Options: png, jpeg, webp
- `output_dir` (optional): Directory to save image (default: ~/Downloads)

**Returns:**
```json
{
  "success": true,
  "path": "/Users/user/Downloads/a-beautiful-sunset.png",
  "metadata": {
    "model": "gemini-2.5-flash-image",
    "aspect_ratio": "16:9",
    "output_format": "png",
    "usage": {
      "total_tokens": 1290
    }
  }
}
```

**Example usage:**
```
User: "Create an image of a sunset over mountains"
Assistant calls: generate_image(prompt="A beautiful sunset over mountains with dramatic clouds")
```

### generate_batch_images

Generate multiple images concurrently (1-10 images).

**Parameters:**
- `prompts` (required): List of text descriptions (1-10 prompts)
- `aspect_ratio` (optional): Image aspect ratio (default: 4:5)
- `output_format` (optional): Output format (default: png)
- `output_dir` (optional): Directory to save images (default: ~/Downloads)

**Returns:**
```json
{
  "success": true,
  "total": 3,
  "generated": 3,
  "failed": 0,
  "paths": [
    "/Users/user/Downloads/batch-folder/01_sunset-over-mountains.png",
    "/Users/user/Downloads/batch-folder/02_futuristic-city.png",
    "/Users/user/Downloads/batch-folder/03_serene-lake.png"
  ],
  "folder": "/Users/user/Downloads/batch-folder",
  "metadata": {
    "model": "gemini-2.5-flash-image",
    "aspect_ratio": "16:9",
    "output_format": "png",
    "total_tokens": 3870
  },
  "errors": null
}
```

**Example usage:**
```
User: "Create 3 logo variations"
Assistant calls: generate_batch_images(
  prompts=[
    "Minimalist tech logo with blue gradient",
    "Geometric abstract logo in purple tones",
    "Modern circular logo with mountain silhouette"
  ]
)
```

## Use Cases

### Marketing Assets
Generate multiple images for campaigns:
```
generate_batch_images(
  prompts=["Modern office space", "Team collaboration", "Product showcase"],
  aspect_ratio="16:9",
  output_format="webp"
)
```

### Social Media Content
Create Instagram-optimized images:
```
generate_image(
  prompt="Inspirational quote over sunrise landscape",
  aspect_ratio="4:5",
  output_format="jpeg"
)
```

### Logo Variations
Generate multiple logo concepts:
```
generate_batch_images(
  prompts=[
    "Minimalist tech logo",
    "Geometric abstract logo",
    "Modern circular logo"
  ],
  aspect_ratio="1:1",
  output_format="png"
)
```

## Aspect Ratio Guide

| Ratio | Dimensions | Use Case |
|-------|------------|----------|
| 1:1   | 1024x1024  | Square images, logos |
| 16:9  | 1344x768   | Widescreen, presentations |
| 9:16  | 768x1344   | Stories, Reels, vertical video |
| 4:5   | 1080x1350  | Instagram feed posts (default) |
| 3:2   | 1280x853   | Classic photo format |
| 4:3   | 1280x960   | Traditional photo format |

## Error Handling

The server handles errors gracefully:

- **Invalid API key**: Returns error with setup instructions
- **Invalid prompts**: Returns validation error with requirements
- **Rate limits**: Caught and reported with API error
- **Individual failures**: In batch mode, other images continue generating
- **Network errors**: Logged with clear error messages

## Pricing Comparison

**Gemini 2.5 Flash Image:**
- $0.039 per image (1290 tokens)
- ~$30 per 1M tokens

**vs OpenAI GPT-4 Image:**
- High quality: $0.036-$0.052 per image
- Medium quality: $0.011-$0.015 per image

Gemini is ~3.5x cheaper than GPT-4 high quality.

## Testing

Run the MCP server:

```bash
# Test server loads without errors
python server.py
# (Server will wait for stdio requests - Ctrl+C to stop)
```

Verify with Claude Desktop by checking the MCP icon in the bottom-right.

## Troubleshooting

**Server won't start:**
- Check Python version (3.10+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check API key is set: `echo $GOOGLE_API_KEY`

**Images not generating:**
- Verify API key is valid
- Check internet connection
- Review error messages in response

**Rate limit errors:**
- Reduce concurrent images (max 10)
- Wait a few seconds between batches
- Check API quota in Google Cloud Console

## License

MIT
