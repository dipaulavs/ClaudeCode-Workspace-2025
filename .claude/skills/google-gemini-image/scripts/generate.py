#!/usr/bin/env python3
"""
Google Gemini 2.5 Flash Image Generation Script
Supports batch generation (1-10 images) with async concurrent requests
"""

import os
import sys
import base64
import argparse
import asyncio
import re
from pathlib import Path
from datetime import datetime
from PIL import Image
from io import BytesIO

# Lazy import for google-genai
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Error: google-genai package not installed", file=sys.stderr)
    print("Install with: pip install google-genai", file=sys.stderr)
    sys.exit(1)


def slugify(text: str, max_length: int = 50) -> str:
    """
    Convert text to a filesystem-safe slug.

    Args:
        text: Input text to slugify
        max_length: Maximum length of slug

    Returns:
        Filesystem-safe slug
    """
    # Remove special characters, keep alphanumeric and spaces
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Trim hyphens from edges
    text = text.strip('-')
    # Truncate to max_length
    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]
    return text or "image"


async def generate_single_image(
    client: genai.Client,
    prompt: str,
    index: int,
    aspect_ratio: str = "4:5",
    output_format: str = "png",
) -> tuple[int, bytes, dict, str]:
    """
    Generate a single image with Gemini 2.5 Flash Image (async).

    Args:
        client: Google GenAI client instance
        prompt: Text description of the desired image
        index: Image index (for batch generation)
        aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 3:2, 2:3, 4:3, 3:4)
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

        # Convert to requested format if needed
        img = Image.open(BytesIO(image_bytes))
        output_buffer = BytesIO()

        if output_format.lower() == 'png':
            img.save(output_buffer, format='PNG')
        elif output_format.lower() == 'jpeg':
            img = img.convert('RGB')  # JPEG doesn't support transparency
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

        # Add usage if available
        if hasattr(response, "usage_metadata"):
            metadata["usage"] = {
                "total_tokens": response.usage_metadata.total_token_count,
            }

        return (index, image_bytes, metadata, prompt)

    except Exception as e:
        print(f"❌ Error generating image {index + 1}: {str(e)}", file=sys.stderr)
        return (index, None, {"error": str(e)}, prompt)


async def generate_batch(
    prompts: list[str],
    output_dir: str = "~/Downloads",
    aspect_ratio: str = "1:1",
    output_format: str = "png",
    api_key: str = None,
) -> list[str]:
    """
    Generate multiple images concurrently using async.

    Args:
        prompts: List of text prompts (1-10 prompts)
        output_dir: Directory to save images
        aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 3:2, 2:3, 4:3, 3:4)
        output_format: Output format (png, jpeg, webp)
        api_key: Google API key

    Returns:
        List of saved file paths
    """
    # Validate input
    if not prompts:
        raise ValueError("At least one prompt is required")
    if len(prompts) > 10:
        raise ValueError("Maximum 10 prompts allowed (API concurrent limit)")

    # Initialize Google GenAI client
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    # Fallback to default API key
    if not api_key:
        api_key = "AIzaSyAz2Jbiir_0-D3RvQGPk-e5Mb4HzvlerXA"

    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set and no API key provided")

    client = genai.Client(api_key=api_key)

    # Expand output directory
    base_output_path = Path(output_dir).expanduser()

    # If multiple images, create a folder with descriptive name
    if len(prompts) > 1:
        # Create folder name from all prompts
        folder_slugs = [slugify(p, max_length=20) for p in prompts[:3]]  # Use first 3 prompts
        folder_name = "-".join(folder_slugs)
        if len(prompts) > 3:
            folder_name += f"-and-{len(prompts) - 3}-more"

        output_path = base_output_path / folder_name
    else:
        output_path = base_output_path

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Generating {len(prompts)} image(s) with gemini-2.5-flash-image...")
    print(f"📁 Output: {output_path}")
    print(f"⚙️  Settings: aspect_ratio={aspect_ratio}, format={output_format}")
    print()

    # Generate images concurrently using asyncio.gather
    tasks = [
        generate_single_image(client, prompt, i, aspect_ratio, output_format)
        for i, prompt in enumerate(prompts)
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results and save images
    saved_files = []
    for img_index, image_bytes, metadata, img_prompt in results:
        if isinstance(results[img_index], Exception):
            print(f"⚠️  Image {img_index + 1}/{len(prompts)} failed")
            continue

        if image_bytes is None:
            print(f"⚠️  Image {img_index + 1}/{len(prompts)} failed")
            continue

        # Generate descriptive filename from prompt
        prompt_slug = slugify(img_prompt, max_length=50)

        if len(prompts) == 1:
            # Single image: descriptive name only
            filename = f"{prompt_slug}.{output_format}"
        else:
            # Multiple images: number + descriptive name
            filename = f"{img_index + 1:02d}_{prompt_slug}.{output_format}"

        file_path = output_path / filename

        # Save image
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        saved_files.append(str(file_path))

        # Print success with metadata
        print(f"✅ Image {img_index + 1}/{len(prompts)}: {file_path.name}")
        if "usage" in metadata:
            usage = metadata["usage"]
            print(f"   Tokens: {usage['total_tokens']}")

    print()
    print(f"🎉 Generated {len(saved_files)}/{len(prompts)} images successfully")

    return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Generate images with Google Gemini 2.5 Flash Image (batch support: 1-10 images)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single image
  %(prog)s "A cute baby sea otter"

  # Multiple images (batch)
  %(prog)s "A sunset over mountains" "A futuristic city" "A serene lake"

  # Custom aspect ratio
  %(prog)s --aspect-ratio 16:9 "A wide panoramic landscape"

  # Different format
  %(prog)s --format webp "An abstract painting"

  # Custom output directory
  %(prog)s --output ~/Pictures/ai-art "An abstract painting"
        """,
    )

    parser.add_argument(
        "prompts",
        nargs="+",
        help="Text descriptions of desired images (1-10 prompts)",
    )

    parser.add_argument(
        "-o", "--output",
        default="~/Downloads",
        help="Output directory (default: ~/Downloads)",
    )

    parser.add_argument(
        "-a", "--aspect-ratio",
        choices=["1:1", "16:9", "9:16", "3:2", "2:3", "4:3", "3:4", "4:5"],
        default="4:5",
        help="Image aspect ratio (default: 4:5 - 1080x1350, ideal for Instagram feed posts)",
    )

    parser.add_argument(
        "-f", "--format",
        choices=["png", "jpeg", "webp"],
        default="png",
        help="Output format (default: png)",
    )

    parser.add_argument(
        "-k", "--api-key",
        help="Google API key (default: uses GOOGLE_API_KEY env var)",
    )

    args = parser.parse_args()

    try:
        saved_files = asyncio.run(generate_batch(
            prompts=args.prompts,
            output_dir=args.output,
            aspect_ratio=args.aspect_ratio,
            output_format=args.format,
            api_key=args.api_key,
        ))

        return 0

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
