#!/usr/bin/env python3
"""
OpenAI GPT Image Generation Script
Supports batch generation (1-20 images) with concurrent requests
"""

import os
import sys
import base64
import argparse
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from openai import OpenAI


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


def generate_single_image(
    client: OpenAI,
    prompt: str,
    index: int,
    quality: str = "auto",
    size: str = "auto",
    output_format: str = "png",
    background: str = "auto",
    output_compression: int = 100,
) -> tuple[int, bytes, dict, str]:
    """
    Generate a single image with OpenAI GPT Image 1 Mini.

    Args:
        client: OpenAI client instance
        prompt: Text description of the desired image
        index: Image index (for batch generation)
        quality: Image quality (low, medium, high, auto)
        size: Image size (1024x1024, 1536x1024, 1024x1536, auto)
        output_format: Output format (png, jpeg, webp)
        background: Background type (transparent, opaque, auto)
        output_compression: Compression level (0-100)

    Returns:
        Tuple of (index, image_bytes, metadata, prompt)
    """
    try:
        response = client.images.generate(
            model="gpt-image-1-mini",
            prompt=prompt,
            n=1,
            size=size,
            quality=quality,
            output_format=output_format,
            background=background,
            output_compression=output_compression,
        )

        # Decode base64 image
        image_bytes = base64.b64decode(response.data[0].b64_json)

        # Extract metadata
        metadata = {
            "created": response.created,
            "size": response.size,
            "quality": response.quality,
            "background": response.background,
            "output_format": response.output_format,
        }

        # Add usage if available
        if hasattr(response, "usage"):
            metadata["usage"] = {
                "total_tokens": response.usage.total_tokens,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }

        return (index, image_bytes, metadata, prompt)

    except Exception as e:
        print(f"❌ Error generating image {index + 1}: {str(e)}", file=sys.stderr)
        return (index, None, {"error": str(e)}, prompt)


def generate_batch(
    prompts: list[str],
    output_dir: str = "~/Downloads",
    quality: str = "medium",
    size: str = "auto",
    output_format: str = "png",
    background: str = "auto",
    output_compression: int = 100,
    max_workers: int = 10,
) -> list[str]:
    """
    Generate multiple images concurrently.

    Args:
        prompts: List of text prompts (1-20 prompts)
        output_dir: Directory to save images
        quality: Image quality (low, medium, high, auto)
        size: Image size (1024x1024, 1536x1024, 1024x1536, auto)
        output_format: Output format (png, jpeg, webp)
        background: Background type (transparent, opaque, auto)
        output_compression: Compression level (0-100)
        max_workers: Maximum concurrent API calls

    Returns:
        List of saved file paths
    """
    # Validate input
    if not prompts:
        raise ValueError("At least one prompt is required")
    if len(prompts) > 20:
        raise ValueError("Maximum 20 prompts allowed")

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY") or "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"

    client = OpenAI(api_key=api_key)

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

    print(f"🎨 Generating {len(prompts)} image(s) with gpt-image-1-mini...")
    print(f"📁 Output: {output_path}")
    print(f"⚙️  Settings: quality={quality}, size={size}, format={output_format}")
    print()

    # Generate images concurrently
    saved_files = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(
                generate_single_image,
                client,
                prompt,
                i,
                quality,
                size,
                output_format,
                background,
                output_compression,
            ): (i, prompt)
            for i, prompt in enumerate(prompts)
        }

        # Collect results as they complete
        for future in as_completed(futures):
            index, prompt = futures[future]
            img_index, image_bytes, metadata, img_prompt = future.result()

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
                print(f"   Tokens: {usage['total_tokens']} (in: {usage['input_tokens']}, out: {usage['output_tokens']})")

    print()
    print(f"🎉 Generated {len(saved_files)}/{len(prompts)} images successfully")

    return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Generate images with OpenAI GPT Image 1 Mini (batch support: 1-20 images)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single image
  %(prog)s "A cute baby sea otter"

  # Multiple images (batch)
  %(prog)s "A sunset over mountains" "A futuristic city" "A serene lake"

  # High quality with custom format
  %(prog)s --quality high --format webp "A photorealistic portrait"

  # Transparent background
  %(prog)s --background transparent --format png "A logo design"

  # Custom output directory
  %(prog)s --output ~/Pictures/ai-art "An abstract painting"
        """,
    )

    parser.add_argument(
        "prompts",
        nargs="+",
        help="Text descriptions of desired images (1-20 prompts)",
    )

    parser.add_argument(
        "-o", "--output",
        default="~/Downloads",
        help="Output directory (default: ~/Downloads)",
    )

    parser.add_argument(
        "-q", "--quality",
        choices=["auto", "low", "medium", "high"],
        default="medium",
        help="Image quality (default: medium)",
    )

    parser.add_argument(
        "-s", "--size",
        choices=["auto", "1024x1024", "1536x1024", "1024x1536"],
        default="1024x1536",
        help="Image size (default: 1024x1536 - vertical 2:3, ideal for Instagram carousel)",
    )

    parser.add_argument(
        "-f", "--format",
        choices=["png", "jpeg", "webp"],
        default="png",
        help="Output format (default: png)",
    )

    parser.add_argument(
        "-b", "--background",
        choices=["auto", "transparent", "opaque"],
        default="auto",
        help="Background type (default: auto)",
    )

    parser.add_argument(
        "-c", "--compression",
        type=int,
        default=100,
        choices=range(0, 101),
        metavar="0-100",
        help="Output compression level for webp/jpeg (default: 100)",
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=10,
        help="Maximum concurrent API calls (default: 10)",
    )

    args = parser.parse_args()

    try:
        saved_files = generate_batch(
            prompts=args.prompts,
            output_dir=args.output,
            quality=args.quality,
            size=args.size,
            output_format=args.format,
            background=args.background,
            output_compression=args.compression,
            max_workers=args.workers,
        )

        return 0

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
