#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for Image Generation Tools
Provides tools for generating, editing, and managing images using various APIs.
"""

import json
import sys
import asyncio
import os
import re
import time
import random
import string
import httpx
from typing import Any, Dict, Optional, List
from datetime import datetime
from pathlib import Path

from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult
import mcp.server.stdio


# Configuracao Nano Banana
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai"
GENERATE_ENDPOINT = f"{BASE_URL}/api/v1/jobs/createTask"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/jobs/recordInfo"
DOWNLOADS_PATH = str(Path.home() / "Downloads")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Initialize MCP Server
app = Server("image-generation-tools")


# ============================================================================
# NANO BANANA HELPER FUNCTIONS
# ============================================================================

def translate_to_portuguese(text: str) -> str:
    """Traduz texto para portugues usando Google Translate API gratuita"""
    try:
        import requests
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "pt",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result[0][0][0]
        return text
    except Exception:
        return text


def create_descriptive_filename(prompt: str, extension: str = "png", max_length: int = 50) -> str:
    """Cria nome descritivo baseado no prompt em portugues"""
    translated_text = translate_to_portuguese(prompt)
    clean_text = re.sub(r'[^\w\s]', '', translated_text)
    words = clean_text.lower().split()[:6]
    descriptive_part = '_'.join(words)

    if len(descriptive_part) > max_length:
        descriptive_part = descriptive_part[:max_length]

    random_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    filename = f"{descriptive_part}_{random_code}.{extension}"
    return filename


async def generate_image_async(prompt: str, output_format: str = "PNG", image_urls: Optional[List[str]] = None) -> Optional[str]:
    """
    Gera uma imagem usando Nano Banana API (async)

    Args:
        prompt: Descricao da imagem
        output_format: PNG ou JPEG
        image_urls: URLs de referencia (opcional)

    Returns:
        task_id se sucesso, None se erro
    """
    payload = {
        "model": "google/nano-banana",
        "input": {
            "prompt": prompt,
            "image_size": "2:3",
            "output_format": output_format.lower()
        }
    }

    if image_urls:
        payload["input"]["image_urls"] = image_urls if isinstance(image_urls, list) else [image_urls]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GENERATE_ENDPOINT, headers=HEADERS, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 200:
                return data["data"]["taskId"]
            return None
    except Exception:
        return None


async def check_status_async(task_id: str) -> Optional[Dict]:
    """Verifica status da tarefa (async)"""
    try:
        params = {"taskId": task_id}
        async with httpx.AsyncClient() as client:
            response = await client.get(STATUS_ENDPOINT, headers=HEADERS, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
    except Exception:
        return None


async def wait_for_completion_async(task_id: str, max_wait: int = 300, check_interval: int = 5) -> Optional[List[str]]:
    """
    Aguarda conclusao da geracao de imagem (async)

    Args:
        task_id: ID da tarefa
        max_wait: Timeout em segundos
        check_interval: Intervalo de verificacao

    Returns:
        Lista de URLs das imagens ou None
    """
    start_time = time.time()
    while time.time() - start_time < max_wait:
        result = await check_status_async(task_id)

        if not result:
            return None

        status = result.get("data", {}).get("state")

        if status == "success":
            result_json_str = result.get("data", {}).get("resultJson", "{}")
            result_json = json.loads(result_json_str)
            return result_json.get("resultUrls", [])

        elif status == "fail":
            return None

        elif status in ["processing", "pending"]:
            await asyncio.sleep(check_interval)
        else:
            await asyncio.sleep(check_interval)

    return None


async def download_image_async(url: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Baixa imagem e salva em Downloads (async)

    Args:
        url: URL da imagem
        output_path: Caminho de saida (opcional)

    Returns:
        Caminho do arquivo ou None
    """
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DOWNLOADS_PATH, f"nanobanana_image_{timestamp}.png")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60)
            response.raise_for_status()

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)

            return output_path
    except Exception:
        return None


async def generate_nanobanana_image(prompt: str, format: str = "PNG") -> Dict:
    """
    Funcao principal: orquestra geracao de imagem com Nano Banana

    Args:
        prompt: Descricao da imagem
        format: Formato (PNG ou JPEG)

    Returns:
        {"success": bool, "image_url": str, "file_path": str, "error": str}
    """
    try:
        format = format.upper()
        if format not in ["PNG", "JPEG"]:
            format = "PNG"

        # Gerar imagem
        task_id = await generate_image_async(prompt, output_format=format)

        if not task_id:
            return {
                "success": False,
                "image_url": "",
                "file_path": "",
                "error": "Falha ao criar tarefa de geracao"
            }

        # Aguardar conclusao
        image_urls = await wait_for_completion_async(task_id, max_wait=300, check_interval=5)

        if not image_urls:
            return {
                "success": False,
                "image_url": "",
                "file_path": "",
                "error": "Timeout ou falha na geracao da imagem"
            }

        # Baixar primeira imagem
        primary_url = image_urls[0]
        extension = format.lower()
        filename = create_descriptive_filename(prompt, extension=extension)
        output_path = os.path.join(DOWNLOADS_PATH, filename)

        file_path = await download_image_async(primary_url, output_path)

        if not file_path:
            return {
                "success": False,
                "image_url": primary_url,
                "file_path": "",
                "error": "Falha ao fazer download da imagem"
            }

        # Baixar imagens adicionais se houver
        if len(image_urls) > 1:
            for i, url in enumerate(image_urls[1:], 2):
                name_parts = filename.rsplit('.', 1)
                additional_path = os.path.join(DOWNLOADS_PATH, f"{name_parts[0]}_v{i}.{name_parts[1]}")
                await download_image_async(url, additional_path)

        return {
            "success": True,
            "image_url": primary_url,
            "file_path": file_path,
            "error": ""
        }

    except Exception as e:
        return {
            "success": False,
            "image_url": "",
            "file_path": "",
            "error": str(e)
        }


# ============================================================================
# Tool Definitions
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available image generation tools.
    Returns metadata for each tool that clients can discover and use.
    """
    return [
        Tool(
            name="generate_nanobanana",
            description="Gera imagem usando Nano Banana (Gemini 2.5 Flash). Portrait 2:3 fixo. Salva em ~/Downloads com nome descritivo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Descricao detalhada da imagem a ser gerada"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["PNG", "JPEG"],
                        "default": "PNG",
                        "description": "Formato de saida da imagem"
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="generate_image",
            description="Generate an image using the specified API and prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Detailed description of the image to generate"
                    },
                    "api": {
                        "type": "string",
                        "enum": ["nanobanana", "gpt4o", "sora"],
                        "description": "Which API to use for image generation"
                    },
                    "quality": {
                        "type": "string",
                        "enum": ["standard", "high"],
                        "description": "Quality level for the generated image"
                    }
                },
                "required": ["prompt", "api"]
            }
        ),
        Tool(
            name="edit_image",
            description="Edit an existing image using various transformation techniques",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_url": {
                        "type": "string",
                        "description": "URL of the image to edit"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["resize", "crop", "enhance", "remove_bg"],
                        "description": "Type of edit operation to perform"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Operation-specific parameters"
                    }
                },
                "required": ["image_url", "operation"]
            }
        ),
        Tool(
            name="batch_generate",
            description="Generate multiple images in batch mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of prompts for batch generation"
                    },
                    "api": {
                        "type": "string",
                        "enum": ["nanobanana", "gpt4o"],
                        "description": "API to use for batch generation"
                    }
                },
                "required": ["prompts", "api"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[ToolResult]:
    """
    Execute a tool call and return the result.
    Routes the request to appropriate handler based on tool name.
    """

    if name == "generate_nanobanana":
        return await handle_generate_nanobanana(arguments)
    elif name == "generate_image":
        return await handle_generate_image(arguments)
    elif name == "edit_image":
        return await handle_edit_image(arguments)
    elif name == "batch_generate":
        return await handle_batch_generate(arguments)
    else:
        return [
            ToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"})
                )],
                isError=True
            )
        ]


async def handle_generate_nanobanana(arguments: dict) -> list[ToolResult]:
    """Handle Nano Banana image generation"""
    prompt = arguments.get("prompt", "")
    format_arg = arguments.get("format", "PNG")

    if not prompt or not isinstance(prompt, str):
        return [ToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"success": False, "error": "Prompt invalido ou vazio"}, ensure_ascii=False)
            )],
            isError=True
        )]

    result = await generate_nanobanana_image(prompt, format_arg)

    return [ToolResult(
        content=[TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )],
        isError=not result.get("success", False)
    )]


async def handle_generate_image(arguments: dict) -> list[TextContent]:
    """
    Handle image generation requests.
    Currently returns placeholder response.
    Implementation will integrate with actual APIs.
    """
    prompt = arguments.get("prompt", "")
    api = arguments.get("api", "nanobanana")
    quality = arguments.get("quality", "standard")

    response = {
        "status": "pending_implementation",
        "tool": "generate_image",
        "api": api,
        "prompt": prompt,
        "quality": quality,
        "message": "Image generation endpoint not yet implemented. Framework is ready for API integration."
    }

    return [
        TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )
    ]


async def handle_edit_image(arguments: dict) -> list[TextContent]:
    """
    Handle image editing requests.
    Currently returns placeholder response.
    Implementation will integrate with actual APIs.
    """
    image_url = arguments.get("image_url", "")
    operation = arguments.get("operation", "")

    response = {
        "status": "pending_implementation",
        "tool": "edit_image",
        "operation": operation,
        "image_url": image_url,
        "message": "Image editing endpoint not yet implemented. Framework is ready for API integration."
    }

    return [
        TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )
    ]


async def handle_batch_generate(arguments: dict) -> list[TextContent]:
    """
    Handle batch image generation requests.
    Currently returns placeholder response.
    Implementation will integrate with actual APIs.
    """
    prompts = arguments.get("prompts", [])
    api = arguments.get("api", "nanobanana")

    response = {
        "status": "pending_implementation",
        "tool": "batch_generate",
        "api": api,
        "prompts_count": len(prompts),
        "message": "Batch generation endpoint not yet implemented. Framework is ready for API integration."
    }

    return [
        TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )
    ]


async def main():
    """
    Main entry point for the MCP server.
    Starts stdio server for communication with MCP clients.
    """
    async with app.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)
