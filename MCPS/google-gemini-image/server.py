#!/usr/bin/env python3
"""
Google Gemini Image Generation MCP Server

Provides tools for generating images using Google's Gemini 2.5 Flash Image model
(nicknamed "Nanobanana"). Supports both single and batch image generation with
async concurrent processing.

Model: gemini-2.5-flash-image
Pricing: ~$0.039 per image (1290 tokens)
Max concurrent: 10 images
"""

import os
import sys
import re
import asyncio
from pathlib import Path
from io import BytesIO
from typing import Literal

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed. Run: pip install pillow", file=sys.stderr)
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai", file=sys.stderr)
    sys.exit(1)

try:
    from mcp.server.fastmcp import FastMCP
    from pydantic import BaseModel, Field, field_validator
except ImportError:
    print("Error: MCP or Pydantic not installed. Run: pip install mcp pydantic", file=sys.stderr)
    sys.exit(1)


# Constants
CHARACTER_LIMIT = 25000
MAX_CONCURRENT_IMAGES = 10
DEFAULT_OUTPUT_DIR = "~/Downloads"
DEFAULT_ASPECT_RATIO = "4:5"
DEFAULT_FORMAT = "png"

# Initialize MCP server
mcp = FastMCP("google-gemini-image")


# ============================================================================
# Shared Utilities
# ============================================================================

def slugify(text: str, max_length: int = 50) -> str:
    """
    Convert text to a filesystem-safe slug.

    Args:
        text: Input text to slugify
        max_length: Maximum length of slug

    Returns:
        Filesystem-safe slug

    Example:
        >>> slugify("A Beautiful Sunset!")
        "a-beautiful-sunset"
    """
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')

    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]

    return text or "image"


def get_api_key() -> str:
    """
    Get Google API key from environment or default.

    Returns:
        API key string

    Raises:
        ValueError: If no API key is available
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    # Fallback to default key
    if not api_key:
        api_key = "AIzaSyAz2Jbiir_0-D3RvQGPk-e5Mb4HzvlerXA"

    if not api_key:
        raise ValueError(
            "No API key available. Set GOOGLE_API_KEY environment variable or "
            "configure a default key in the server."
        )

    return api_key


async def generate_single_image_internal(
    client: genai.Client,
    prompt: str,
    index: int,
    aspect_ratio: str,
    output_format: str,
) -> tuple[int, bytes | None, dict, str]:
    """
    Internal function to generate a single image (async).

    Args:
        client: Google GenAI client
        prompt: Image description
        index: Image index for batch generation
        aspect_ratio: Aspect ratio (1:1, 16:9, etc)
        output_format: Output format (png, jpeg, webp)

    Returns:
        Tuple of (index, image_bytes, metadata, prompt)
    """
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                ),
            ),
        )

        # Extract image from response
        image_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                break

        if image_bytes is None:
            raise ValueError("No image data in response")

        # Convert to requested format
        img = Image.open(BytesIO(image_bytes))
        output_buffer = BytesIO()

        if output_format.lower() == 'png':
            img.save(output_buffer, format='PNG')
        elif output_format.lower() == 'jpeg':
            img = img.convert('RGB')
            img.save(output_buffer, format='JPEG', quality=95)
        elif output_format.lower() == 'webp':
            img.save(output_buffer, format='WEBP', quality=95)

        image_bytes = output_buffer.getvalue()

        # Extract metadata
        metadata = {
            "model": "gemini-2.5-flash-image",
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
        }

        if hasattr(response, "usage_metadata"):
            metadata["usage"] = {
                "total_tokens": response.usage_metadata.total_token_count,
            }

        return (index, image_bytes, metadata, prompt)

    except Exception as e:
        return (index, None, {"error": str(e)}, prompt)


# ============================================================================
# Pydantic Models for Input Validation
# ============================================================================

AspectRatio = Literal["1:1", "16:9", "9:16", "3:2", "2:3", "4:3", "3:4", "4:5"]
OutputFormat = Literal["png", "jpeg", "webp"]


class GenerateImageInput(BaseModel):
    """Input model for single image generation."""

    prompt: str = Field(
        ...,
        description=(
            "Text description of the desired image. Be descriptive and specific. "
            "Examples: 'A cute baby sea otter floating on its back', "
            "'A futuristic city skyline at sunset with flying cars', "
            "'Abstract geometric patterns in blue and purple tones'"
        ),
        min_length=3,
        max_length=1000,
    )

    aspect_ratio: AspectRatio = Field(
        default=DEFAULT_ASPECT_RATIO,
        description=(
            "Image aspect ratio. Options: "
            "1:1 (1024x1024 square), "
            "16:9 (1344x768 widescreen), "
            "9:16 (768x1344 portrait/stories), "
            "4:5 (1080x1350 Instagram feed - default), "
            "3:2, 2:3, 4:3, 3:4 (photo formats)"
        ),
    )

    output_format: OutputFormat = Field(
        default=DEFAULT_FORMAT,
        description=(
            "Output image format. Options: "
            "png (default, supports transparency), "
            "jpeg (smaller size, no transparency), "
            "webp (best compression)"
        ),
    )

    output_dir: str = Field(
        default=DEFAULT_OUTPUT_DIR,
        description=(
            "Directory to save the generated image. Defaults to ~/Downloads. "
            "Example: ~/Pictures/ai-art"
        ),
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "A serene mountain lake at sunrise with fog",
                    "aspect_ratio": "16:9",
                    "output_format": "png",
                    "output_dir": "~/Downloads"
                }
            ]
        }
    }


class GenerateBatchImagesInput(BaseModel):
    """Input model for batch image generation."""

    prompts: list[str] = Field(
        ...,
        description=(
            "List of text descriptions for images to generate (1-10 prompts). "
            "Images are generated concurrently for maximum speed. "
            "Examples: ['A sunset over mountains', 'A futuristic city', 'A serene lake']"
        ),
        min_length=1,
        max_length=MAX_CONCURRENT_IMAGES,
    )

    aspect_ratio: AspectRatio = Field(
        default=DEFAULT_ASPECT_RATIO,
        description="Image aspect ratio (applies to all images in batch)",
    )

    output_format: OutputFormat = Field(
        default=DEFAULT_FORMAT,
        description="Output image format (applies to all images in batch)",
    )

    output_dir: str = Field(
        default=DEFAULT_OUTPUT_DIR,
        description="Directory to save generated images (creates subfolder for batch)",
    )

    @field_validator('prompts')
    @classmethod
    def validate_prompts(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("At least one prompt is required")
        if len(v) > MAX_CONCURRENT_IMAGES:
            raise ValueError(f"Maximum {MAX_CONCURRENT_IMAGES} prompts allowed")
        for prompt in v:
            if len(prompt) < 3:
                raise ValueError("Each prompt must be at least 3 characters")
            if len(prompt) > 1000:
                raise ValueError("Each prompt must be at most 1000 characters")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompts": [
                        "A sunset over mountains",
                        "A futuristic city at night",
                        "A serene lake with reflections"
                    ],
                    "aspect_ratio": "16:9",
                    "output_format": "png",
                    "output_dir": "~/Downloads"
                }
            ]
        }
    }


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool(
    description=(
        "Generate a single image using Google Gemini 2.5 Flash Image (Nanobanana). "
        "Returns the file path of the generated image. "
        "Cost: ~$0.039 per image. "
        "Supports multiple aspect ratios (square, widescreen, portrait) and formats (PNG, JPEG, WebP). "
        "Use this tool when you need to create one image. For multiple images, use generate_batch_images."
    ),
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def generate_image(
    prompt: str,
    aspect_ratio: AspectRatio = DEFAULT_ASPECT_RATIO,
    output_format: OutputFormat = DEFAULT_FORMAT,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> dict:
    """
    Generate a single image with Google Gemini 2.5 Flash Image.

    Args:
        prompt: Text description of desired image
        aspect_ratio: Image aspect ratio (default: 4:5 for Instagram)
        output_format: Output format (default: png)
        output_dir: Directory to save image (default: ~/Downloads)

    Returns:
        Dictionary containing:
        - success: bool
        - path: str (file path if successful)
        - metadata: dict (model info, tokens used)
        - error: str (if failed)

    Example usage:
        When user asks: "Create an image of a sunset over mountains"
        Call: generate_image(prompt="A beautiful sunset over mountains with dramatic clouds")

    Error handling:
        - If API key is invalid, returns error with instructions to set GOOGLE_API_KEY
        - If prompt is too short/long, returns error with valid length requirements
        - If generation fails, returns error with API error message
    """
    try:
        # Validate input
        input_data = GenerateImageInput(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            output_format=output_format,
            output_dir=output_dir,
        )

        # Get API key and initialize client
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

        # Expand output directory
        output_path = Path(input_data.output_dir).expanduser()
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate image
        index, image_bytes, metadata, _ = await generate_single_image_internal(
            client=client,
            prompt=input_data.prompt,
            index=0,
            aspect_ratio=input_data.aspect_ratio,
            output_format=input_data.output_format,
        )

        if image_bytes is None:
            error_msg = metadata.get("error", "Unknown error")
            return {
                "success": False,
                "error": f"Failed to generate image: {error_msg}",
            }

        # Save image with descriptive filename
        prompt_slug = slugify(input_data.prompt, max_length=50)
        filename = f"{prompt_slug}.{input_data.output_format}"
        file_path = output_path / filename

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return {
            "success": True,
            "path": str(file_path),
            "metadata": metadata,
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
        }


@mcp.tool(
    description=(
        "Generate multiple images concurrently using Google Gemini 2.5 Flash Image (Nanobanana). "
        "Supports 1-10 images with async concurrent processing for maximum speed (~2.1s per image). "
        "All images are saved in a descriptive folder with numbered filenames. "
        "Cost: ~$0.039 per image. "
        "Use this tool when you need to create multiple images at once (e.g., variations, series, batch generation)."
    ),
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def generate_batch_images(
    prompts: list[str],
    aspect_ratio: AspectRatio = DEFAULT_ASPECT_RATIO,
    output_format: OutputFormat = DEFAULT_FORMAT,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> dict:
    """
    Generate multiple images concurrently with Google Gemini 2.5 Flash Image.

    Args:
        prompts: List of text descriptions (1-10 prompts)
        aspect_ratio: Image aspect ratio (applies to all images)
        output_format: Output format (applies to all images)
        output_dir: Directory to save images (creates subfolder)

    Returns:
        Dictionary containing:
        - success: bool
        - total: int (total images requested)
        - generated: int (successfully generated)
        - failed: int (failed to generate)
        - paths: list[str] (file paths of generated images)
        - folder: str (folder containing all images)
        - metadata: dict (aggregate metadata)
        - errors: list[str] (error messages for failed images)

    Example usage:
        When user asks: "Create 3 variations of a logo design"
        Call: generate_batch_images(
            prompts=[
                "Minimalist tech logo with blue gradient",
                "Geometric abstract logo in purple tones",
                "Modern circular logo with mountain silhouette"
            ]
        )

    Error handling:
        - If more than 10 prompts provided, returns error (API concurrent limit)
        - If any prompt is invalid, returns error with details
        - Individual image failures don't stop batch - continue generating others
        - Returns list of errors for failed images in the response
    """
    try:
        # Validate input
        input_data = GenerateBatchImagesInput(
            prompts=prompts,
            aspect_ratio=aspect_ratio,
            output_format=output_format,
            output_dir=output_dir,
        )

        # Get API key and initialize client
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

        # Expand output directory
        base_output_path = Path(input_data.output_dir).expanduser()

        # Create descriptive folder for batch
        if len(input_data.prompts) > 1:
            folder_slugs = [slugify(p, max_length=20) for p in input_data.prompts[:3]]
            folder_name = "-".join(folder_slugs)
            if len(input_data.prompts) > 3:
                folder_name += f"-and-{len(input_data.prompts) - 3}-more"
            output_path = base_output_path / folder_name
        else:
            output_path = base_output_path

        output_path.mkdir(parents=True, exist_ok=True)

        # Generate images concurrently
        tasks = [
            generate_single_image_internal(
                client=client,
                prompt=prompt,
                index=i,
                aspect_ratio=input_data.aspect_ratio,
                output_format=input_data.output_format,
            )
            for i, prompt in enumerate(input_data.prompts)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        saved_files = []
        errors = []
        total_tokens = 0

        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
                continue

            img_index, image_bytes, metadata, img_prompt = result

            if image_bytes is None:
                error_msg = metadata.get("error", "Unknown error")
                errors.append(f"Image {img_index + 1}: {error_msg}")
                continue

            # Generate filename
            prompt_slug = slugify(img_prompt, max_length=50)
            if len(input_data.prompts) == 1:
                filename = f"{prompt_slug}.{input_data.output_format}"
            else:
                filename = f"{img_index + 1:02d}_{prompt_slug}.{input_data.output_format}"

            file_path = output_path / filename

            # Save image
            with open(file_path, "wb") as f:
                f.write(image_bytes)

            saved_files.append(str(file_path))

            # Aggregate tokens
            if "usage" in metadata:
                total_tokens += metadata["usage"].get("total_tokens", 0)

        return {
            "success": True,
            "total": len(input_data.prompts),
            "generated": len(saved_files),
            "failed": len(errors),
            "paths": saved_files,
            "folder": str(output_path) if len(input_data.prompts) > 1 else None,
            "metadata": {
                "model": "gemini-2.5-flash-image",
                "aspect_ratio": input_data.aspect_ratio,
                "output_format": input_data.output_format,
                "total_tokens": total_tokens,
            },
            "errors": errors if errors else None,
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
        }


# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
