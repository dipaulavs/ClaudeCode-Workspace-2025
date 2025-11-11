#!/usr/bin/env python3
"""
Grok Imagine Image Generator
Generates images using xAI's Grok Imagine API (text-to-image)
"""

import requests
import json
import time
import sys
from pathlib import Path

# API Configuration
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai/api/v1/jobs"
MODEL = "grok-imagine/text-to-image"

def create_task(prompt: str, aspect_ratio: str = "1:1", callback_url: str = None) -> str:
    """
    Create a new image generation task

    Args:
        prompt: Text description of the image to generate
        aspect_ratio: Image aspect ratio (2:3, 3:2, 1:1)
        callback_url: Optional callback URL for task completion notifications

    Returns:
        task_id: The task ID to query for results
    """
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

    if callback_url:
        payload["callBackUrl"] = callback_url

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()

        if result.get("code") == 200:
            task_id = result["data"]["taskId"]
            print(f"✅ Task created successfully: {task_id}")
            return task_id
        else:
            print(f"❌ Error creating task: {result.get('message')}")
            return None

    except Exception as e:
        print(f"❌ Exception during task creation: {e}")
        return None

def query_task(task_id: str, max_attempts: int = 60, interval: int = 5) -> dict:
    """
    Query task status and wait for completion

    Args:
        task_id: The task ID to query
        max_attempts: Maximum number of polling attempts
        interval: Seconds between polling attempts

    Returns:
        Task result data including image URLs
    """
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
                    print(f"✅ Task completed successfully!")
                    return data
                elif state == "fail":
                    print(f"❌ Task failed: {data.get('failMsg', 'Unknown error')}")
                    return None
                elif state in ["waiting", "pending", "processing"]:
                    print(f"⏳ Task {state}... (attempt {attempts + 1}/{max_attempts})")
                    time.sleep(interval)
                    attempts += 1
                else:
                    print(f"⚠️ Unknown state: {state}")
                    time.sleep(interval)
                    attempts += 1
            else:
                print(f"❌ Error querying task: {result.get('message')}")
                return None

        except Exception as e:
            print(f"❌ Exception during task query: {e}")
            return None

    print(f"⏱️ Timeout: Task did not complete within {max_attempts * interval} seconds")
    return None

def download_images(result_data: dict, output_dir: str = "~/Downloads") -> list:
    """
    Download generated images from result URLs

    Args:
        result_data: Task result data containing image URLs
        output_dir: Directory to save images (default: ~/Downloads)

    Returns:
        List of saved file paths
    """
    output_path = Path(output_dir).expanduser()
    output_path.mkdir(parents=True, exist_ok=True)

    result_json = json.loads(result_data.get("resultJson", "{}"))
    result_urls = result_json.get("resultUrls", [])

    if not result_urls:
        print("❌ No result URLs found")
        return []

    saved_files = []
    for i, url in enumerate(result_urls):
        try:
            print(f"📥 Downloading image {i+1}/{len(result_urls)}...")
            response = requests.get(url)

            if response.status_code == 200:
                # Generate filename from task_id and index
                task_id = result_data.get("taskId", "unknown")
                filename = f"grok_{task_id}_{i+1}.jpg"
                file_path = output_path / filename

                with open(file_path, "wb") as f:
                    f.write(response.content)

                print(f"✅ Saved: {file_path}")
                saved_files.append(str(file_path))
            else:
                print(f"❌ Failed to download image {i+1}: HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Exception downloading image {i+1}: {e}")

    return saved_files

def generate_image(prompt: str, aspect_ratio: str = "1:1", output_dir: str = "~/Downloads") -> list:
    """
    Complete workflow: create task, wait for completion, download images

    Args:
        prompt: Text description of the image to generate
        aspect_ratio: Image aspect ratio (2:3, 3:2, 1:1)
        output_dir: Directory to save images

    Returns:
        List of saved file paths
    """
    print(f"🚀 Starting Grok Imagine generation...")
    print(f"📝 Prompt: {prompt}")
    print(f"📐 Aspect ratio: {aspect_ratio}")
    print()

    # Step 1: Create task
    task_id = create_task(prompt, aspect_ratio)
    if not task_id:
        return []

    print()

    # Step 2: Wait for completion
    result_data = query_task(task_id)
    if not result_data:
        return []

    print()

    # Step 3: Download images
    saved_files = download_images(result_data, output_dir)

    if saved_files:
        print()
        print(f"🎉 Generated {len(saved_files)} image(s) successfully!")
        for file in saved_files:
            print(f"   {file}")

    return saved_files

def main():
    """CLI interface for Grok Imagine image generation"""
    if len(sys.argv) < 2:
        print("Usage: python3 generate_grok_image.py <prompt> [aspect_ratio] [output_dir]")
        print()
        print("Arguments:")
        print("  prompt       : Text description of the image to generate (required)")
        print("  aspect_ratio : 2:3, 3:2, or 1:1 (default: 1:1)")
        print("  output_dir   : Directory to save images (default: ~/Downloads)")
        print()
        print("Examples:")
        print('  python3 generate_grok_image.py "A sunset over the ocean"')
        print('  python3 generate_grok_image.py "Portrait of a cat" 3:2')
        print('  python3 generate_grok_image.py "Mountain landscape" 16:9 ~/Pictures')
        sys.exit(1)

    prompt = sys.argv[1]
    aspect_ratio = sys.argv[2] if len(sys.argv) > 2 else "1:1"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "~/Downloads"

    generate_image(prompt, aspect_ratio, output_dir)

if __name__ == "__main__":
    main()
