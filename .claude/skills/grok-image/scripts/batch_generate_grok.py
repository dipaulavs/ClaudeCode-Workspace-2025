#!/usr/bin/env python3
"""
Batch Grok Imagine Image Generator
Generates multiple images in parallel using xAI's Grok Imagine API
"""

import requests
import json
import time
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# API Configuration
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai/api/v1/jobs"
MODEL = "grok-imagine/text-to-image"

def create_task(prompt: str, aspect_ratio: str = "1:1") -> str:
    """Create a new image generation task"""
    url = f"{BASE_URL}/createTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": MODEL,
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()

        if result.get("code") == 200:
            task_id = result["data"]["taskId"]
            return task_id
        else:
            print(f"❌ Error creating task for '{prompt[:50]}...': {result.get('message')}")
            return None

    except Exception as e:
        print(f"❌ Exception during task creation: {e}")
        return None

def query_task(task_id: str, max_attempts: int = 60, interval: int = 5) -> dict:
    """Query task status and wait for completion"""
    url = f"{BASE_URL}/recordInfo"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(f"{url}?taskId={task_id}", headers=headers)
            result = response.json()

            if result.get("code") == 200:
                data = result.get("data", {})
                state = data.get("state", "")

                if state == "success":
                    return data
                elif state == "fail":
                    return None
                elif state in ["waiting", "pending", "processing"]:
                    time.sleep(interval)
                    attempts += 1
                else:
                    time.sleep(interval)
                    attempts += 1
            else:
                return None

        except Exception as e:
            return None

    return None

def download_images(result_data: dict, output_dir: str, prompt_index: int, base_folder_name: str) -> list:
    """Download generated images from result URLs"""
    # Create main folder
    main_path = Path(output_dir).expanduser()
    main_path.mkdir(parents=True, exist_ok=True)

    # Create subfolder for this batch (Conjunto 1, Conjunto 2, etc)
    conjunto_name = f"Conjunto {prompt_index + 1}"
    conjunto_path = main_path / conjunto_name
    conjunto_path.mkdir(parents=True, exist_ok=True)

    result_json = json.loads(result_data.get("resultJson", "{}"))
    result_urls = result_json.get("resultUrls", [])

    if not result_urls:
        return []

    saved_files = []
    task_id = result_data.get("taskId", "unknown")

    for i, url in enumerate(result_urls):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                # Nome simplificado: só o número da foto
                filename = f"{base_folder_name}_{i+1}.jpg"
                file_path = conjunto_path / filename

                with open(file_path, "wb") as f:
                    f.write(response.content)

                saved_files.append(str(file_path))

        except Exception as e:
            pass

    return saved_files

def generate_single_image(prompt: str, aspect_ratio: str, output_dir: str, index: int, base_folder_name: str) -> dict:
    """Generate a single image (used in parallel execution)"""
    print(f"🚀 [{index+1}] Creating task for: {prompt[:60]}...")

    task_id = create_task(prompt, aspect_ratio)
    if not task_id:
        return {"success": False, "prompt": prompt, "index": index}

    print(f"⏳ [{index+1}] Waiting for completion (task: {task_id})...")

    result_data = query_task(task_id)
    if not result_data:
        return {"success": False, "prompt": prompt, "index": index}

    saved_files = download_images(result_data, output_dir, index, base_folder_name)

    if saved_files:
        print(f"✅ [{index+1}] Generated {len(saved_files)} image(s) in Conjunto {index+1}")
        return {"success": True, "prompt": prompt, "index": index, "files": saved_files}
    else:
        return {"success": False, "prompt": prompt, "index": index}

def batch_generate_images(prompts: list, aspect_ratio: str = "1:1", output_dir: str = "~/Downloads", base_folder_name: str = "image", max_workers: int = 5) -> dict:
    """
    Generate multiple images in parallel

    Args:
        prompts: List of text descriptions
        aspect_ratio: Image aspect ratio (2:3, 3:2, 1:1)
        output_dir: Directory to save images
        base_folder_name: Base name for image files
        max_workers: Maximum number of parallel tasks

    Returns:
        Dict with success/failure counts and file paths
    """
    print(f"🎨 Starting batch generation for {len(prompts)} prompt(s)")
    print(f"📐 Aspect ratio: {aspect_ratio}")
    print(f"📁 Main folder: {output_dir}")
    print(f"⚙️  Max parallel tasks: {max_workers}")
    print()

    results = {
        "total": len(prompts),
        "success": 0,
        "failed": 0,
        "files": [],
        "main_folder": output_dir
    }

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(generate_single_image, prompt, aspect_ratio, output_dir, i, base_folder_name): i
            for i, prompt in enumerate(prompts)
        }

        # Process completed tasks
        for future in as_completed(futures):
            result = future.result()

            if result["success"]:
                results["success"] += 1
                results["files"].extend(result.get("files", []))
            else:
                results["failed"] += 1

    print()
    print("=" * 60)
    print(f"🎉 Batch generation completed!")
    print(f"   Total: {results['total']} conjuntos")
    print(f"   ✅ Success: {results['success']}")
    print(f"   ❌ Failed: {results['failed']}")
    print(f"   📁 Total images: {len(results['files'])}")
    print(f"   📂 Main folder: {Path(output_dir).expanduser()}")
    print()

    # Show folder structure
    if results["success"] > 0:
        print("📂 Folder structure:")
        print(f"   {Path(output_dir).expanduser().name}/")
        for i in range(results['success']):
            print(f"   ├── Conjunto {i+1}/ (6 images)")

    return results

def main():
    """CLI interface for batch Grok Imagine generation"""
    if len(sys.argv) < 2:
        print("Usage: python3 batch_generate_grok.py <prompt1> [prompt2] [prompt3] ... [--aspect-ratio=1:1] [--output-dir=~/Downloads] [--base-name=image] [--workers=5]")
        print()
        print("Arguments:")
        print("  prompt1, prompt2, ... : Text descriptions of images to generate (required)")
        print("  --aspect-ratio        : 2:3, 3:2, or 1:1 (default: 1:1)")
        print("  --output-dir          : Directory to save images (default: ~/Downloads)")
        print("  --base-name           : Base name for image files (default: image)")
        print("  --workers             : Max parallel tasks (default: 5)")
        print()
        print("Examples:")
        print('  python3 batch_generate_grok.py "A sunset" "A cat" "A mountain"')
        print('  python3 batch_generate_grok.py "Portrait 1" "Portrait 2" --aspect-ratio=3:2')
        print('  python3 batch_generate_grok.py "Image 1" "Image 2" --output-dir=~/Pictures --base-name=person --workers=3')
        sys.exit(1)

    # Parse arguments
    prompts = []
    aspect_ratio = "1:1"
    output_dir = "~/Downloads"
    base_folder_name = "image"
    max_workers = 5

    for arg in sys.argv[1:]:
        if arg.startswith("--aspect-ratio="):
            aspect_ratio = arg.split("=")[1]
        elif arg.startswith("--output-dir="):
            output_dir = arg.split("=")[1]
        elif arg.startswith("--base-name="):
            base_folder_name = arg.split("=")[1]
        elif arg.startswith("--workers="):
            max_workers = int(arg.split("=")[1])
        else:
            prompts.append(arg)

    if not prompts:
        print("❌ Error: At least one prompt is required")
        sys.exit(1)

    batch_generate_images(prompts, aspect_ratio, output_dir, base_folder_name, max_workers)

if __name__ == "__main__":
    main()
