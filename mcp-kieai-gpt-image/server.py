#!/usr/bin/env python3
"""
MCP Server para Geração de Imagens com KIE.AI (GPT-4o Image)
"""
import asyncio
import json
import os
from typing import Any
from pathlib import Path
import requests
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuração da API
API_KEY = os.getenv("KIEAI_API_KEY", "fa32b7ea4ff0e9b5acce83abe09d2b06")
API_BASE_URL = "https://api.kie.ai/api/v1"
DOWNLOADS_PATH = str(Path.home() / "Downloads")

app = Server("kie-gpt-image")


def create_image_task(prompt: str, size: str = "1:1", files_url: list = None,
                      n_variants: int = 1, mask_url: str = None, is_enhance: bool = False,
                      enable_fallback: bool = True, fallback_model: str = "GPT_IMAGE_1") -> dict:
    """
    Cria uma task de geração de imagem com GPT-4o Image na API KIE.AI
    - files_url: lista de URLs de imagens de referência (opcional)
    - mask_url: URL da máscara para inpainting (opcional)
    """
    url = f"{API_BASE_URL}/gpt4o-image/generate"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "prompt": prompt,
        "size": size,
        "nVariants": n_variants,
        "isEnhance": is_enhance,
        "enableFallback": enable_fallback,
        "fallbackModel": fallback_model
    }

    # Adiciona parâmetros opcionais
    if files_url:
        payload["filesUrl"] = files_url
    if mask_url:
        payload["maskUrl"] = mask_url

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def query_task(task_id: str) -> dict:
    """Consulta o status de uma task"""
    url = f"{API_BASE_URL}/gpt4o-image/record-info"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {"taskId": task_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def wait_for_task_completion(task_id: str, max_wait: int = 60) -> dict:
    """Aguarda a conclusão da task com polling"""
    import time

    waited = 0
    while waited < max_wait:
        result = query_task(task_id)

        if result.get("code") != 200:
            return result

        data = result.get("data", {})
        status = data.get("status")

        if status == "SUCCESS":
            return result
        elif status == "FAILED":
            return result

        time.sleep(2)
        waited += 2

    return {"code": 408, "message": "Timeout waiting for task completion"}


def translate_to_portuguese(text: str) -> str:
    """Traduz texto para português usando Google Translate API"""
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "pt",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=3)
        if response.status_code == 200:
            result = response.json()
            translated = result[0][0][0]
            return translated.lower()
        return text.lower()
    except:
        return text.lower()


def remove_accents(text: str) -> str:
    """Remove acentos de um texto"""
    import unicodedata
    # Normaliza para NFD (decomposição) e remove marcas diacríticas
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')


def create_descriptive_filename(prompt: str, extension: str = "png") -> str:
    """Cria um nome de arquivo descritivo baseado no prompt (em português, sem acentos)"""
    import re
    import random
    import string

    # Remove pontuação e caracteres especiais
    clean_prompt = re.sub(r'[^\w\s]', '', prompt.lower())

    # Remove palavras comuns (stopwords) em inglês e português
    stopwords = {'a', 'an', 'the', 'in', 'on', 'at', 'of', 'for', 'with', 'and', 'or', 'but',
                 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
                 'beautiful', 'cute', 'nice', 'pretty', 'digital', 'art', 'photorealistic',
                 'image', 'picture', 'photo', 'style', 'lighting', 'natural',
                 'o', 'uma', 'um', 'de', 'da', 'do', 'em', 'na', 'no', 'com', 'e', 'ou',
                 'bonito', 'bonita', 'fofo', 'fofa', 'lindo', 'linda', 'realista', 'digital',
                 'sobre', 'para', 'travesseiro'}

    # Pega as primeiras 2-3 palavras significativas
    words = [w for w in clean_prompt.split() if w not in stopwords][:3]

    if not words:
        # Fallback se não houver palavras válidas
        words = clean_prompt.split()[:2]

    # Junta as palavras
    key_phrase = ' '.join(words)

    # Traduz para português
    translated = translate_to_portuguese(key_phrase)

    # Remove acentos
    translated_no_accents = remove_accents(translated)

    # Limpa novamente após tradução
    translated_clean = re.sub(r'[^\w\s]', '', translated_no_accents)

    # Remove stopwords em português novamente
    final_words = [w for w in translated_clean.split() if w not in stopwords]

    if not final_words:
        final_words = translated_clean.split()[:2]

    # Junta com underscore
    descriptive_part = '_'.join(final_words[:3])

    # Limita a 30 caracteres
    if len(descriptive_part) > 30:
        descriptive_part = descriptive_part[:30]

    # Adiciona código aleatório curto (3 caracteres)
    random_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

    # Nome final
    filename = f"{descriptive_part}_{random_code}.{extension}"

    return filename


def download_image(url: str, filename: str = None, prompt: str = None) -> dict:
    """Baixa uma imagem da URL e salva na pasta Downloads"""
    try:
        # Extrai extensão da URL
        url_extension = url.split('.')[-1].lower()
        if url_extension not in ['png', 'jpg', 'jpeg']:
            url_extension = 'png'

        if not filename:
            if prompt:
                # Cria nome descritivo baseado no prompt
                filename = create_descriptive_filename(prompt, url_extension)
            else:
                # Fallback: usa nome da URL
                filename = url.split("/")[-1]

        output_path = os.path.join(DOWNLOADS_PATH, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return {
            "success": True,
            "path": output_path,
            "filename": filename
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """Lista as ferramentas disponíveis"""
    return [
        Tool(
            name="generate_image",
            description="Gera imagens com GPT-4o Image. Suporta geração com referências, variantes múltiplas, inpainting com máscaras. Suporta 1-15 imagens em paralelo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt único descrevendo a imagem desejada. Use este OU 'prompts'.",
                        "maxLength": 5000
                    },
                    "prompts": {
                        "type": "array",
                        "description": "Lista de prompts para múltiplas imagens em PARALELO (1-15). Use este OU 'prompt'.",
                        "items": {
                            "type": "string",
                            "maxLength": 5000
                        },
                        "minItems": 1,
                        "maxItems": 15
                    },
                    "files_url": {
                        "type": "array",
                        "description": "URLs de imagens de referência (opcional). Para edição/variações de uma imagem.",
                        "items": {
                            "type": "string",
                            "format": "uri"
                        }
                    },
                    "size": {
                        "type": "string",
                        "description": "Proporção da imagem",
                        "enum": ["1:1", "3:2", "2:3"],
                        "default": "1:1"
                    },
                    "n_variants": {
                        "type": "integer",
                        "description": "Número de variantes a gerar (1, 2 ou 4)",
                        "enum": [1, 2, 4],
                        "default": 1
                    },
                    "mask_url": {
                        "type": "string",
                        "description": "URL da máscara para inpainting (opcional)",
                        "format": "uri"
                    },
                    "is_enhance": {
                        "type": "boolean",
                        "description": "Se true, melhora a qualidade da imagem",
                        "default": False
                    },
                    "enable_fallback": {
                        "type": "boolean",
                        "description": "Se true, usa modelo fallback em caso de falha",
                        "default": True
                    },
                    "fallback_model": {
                        "type": "string",
                        "description": "Modelo fallback a usar",
                        "enum": ["GPT_IMAGE_1", "FLUX_MAX"],
                        "default": "GPT_IMAGE_1"
                    },
                    "wait_for_completion": {
                        "type": "boolean",
                        "description": "Se true, aguarda a conclusão da geração (até 60s). Se false, retorna apenas o task_id",
                        "default": True
                    },
                    "auto_download": {
                        "type": "boolean",
                        "description": "Se true, baixa automaticamente as imagens para ~/Downloads",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="download_image",
            description="Baixa uma imagem da URL e salva na pasta ~/Downloads",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL da imagem a ser baixada"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Nome do arquivo (opcional). Se não fornecido, usa o nome da URL"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="check_task_status",
            description="Verifica o status de uma task de geração de imagem",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID da task a ser consultada"
                    }
                },
                "required": ["task_id"]
            }
        )
    ]


async def wait_for_task_completion_async(task_id: str, max_wait: int = 60) -> dict:
    """Aguarda a conclusão da task de forma ASSÍNCRONA (não bloqueia)"""
    waited = 0
    while waited < max_wait:
        result = query_task(task_id)

        if result.get("code") != 200:
            return result

        data = result.get("data", {})
        status = data.get("status")

        if status == "SUCCESS":
            return result
        elif status == "FAILED":
            return result

        await asyncio.sleep(2)  # ASYNC sleep - não bloqueia!
        waited += 2

    return {"code": 408, "message": "Timeout waiting for task completion"}


async def generate_single_async(prompt: str, size: str, wait_for_completion: bool,
                               auto_download: bool, files_url: list = None,
                               n_variants: int = 1, mask_url: str = None,
                               is_enhance: bool = False, enable_fallback: bool = True,
                               fallback_model: str = "GPT_IMAGE_1") -> dict:
    """
    Gera uma única imagem de forma assíncrona com GPT-4o Image
    """
    result = create_image_task(prompt, size, files_url, n_variants, mask_url,
                              is_enhance, enable_fallback, fallback_model)

    if result.get("code") != 200:
        return {"error": True, "prompt": prompt, "data": result}

    task_id = result.get("data", {}).get("taskId")

    if not wait_for_completion:
        return {"status": "task_created", "prompt": prompt, "task_id": task_id}

    # Aguarda conclusão de forma ASSÍNCRONA
    final_result = await wait_for_task_completion_async(task_id)

    if final_result.get("code") == 200:
        data = final_result.get("data", {})
        response_data = data.get("response", {})
        image_urls = response_data.get("resultUrls", [])
        response = {
            "status": "success",
            "prompt": prompt,
            "task_id": task_id,
            "image_urls": image_urls,
            "cost_time": data.get("costTime"),
            "consume_credits": data.get("consumeCredits")
        }

        if auto_download and image_urls:
            downloads = []
            for url in image_urls:
                download_result = download_image(url, prompt=prompt)
                if download_result.get("success"):
                    downloads.append({
                        "url": url,
                        "path": download_result["path"],
                        "filename": download_result["filename"]
                    })
            response["downloads"] = downloads
            response["downloads_path"] = DOWNLOADS_PATH

        return response
    else:
        return {"error": True, "prompt": prompt, "data": final_result}


async def generate_batch_parallel(prompts: list, size: str, wait_for_completion: bool,
                                  auto_download: bool, n_variants: int = 1,
                                  is_enhance: bool = False, enable_fallback: bool = True,
                                  fallback_model: str = "GPT_IMAGE_1") -> dict:
    """
    Gera múltiplas imagens EM PARALELO - TODAS AO MESMO TEMPO com GPT-4o Image
    """

    # FASE 1: Cria TODAS as tasks na API de uma vez (rápido, ~1s por task)
    task_ids = []
    for prompt in prompts:
        result = create_image_task(prompt, size, None, n_variants, None,
                                  is_enhance, enable_fallback, fallback_model)
        if result.get("code") == 200:
            task_id = result.get("data", {}).get("taskId")
            task_ids.append({
                "prompt": prompt,
                "task_id": task_id
            })
        else:
            task_ids.append({"prompt": prompt, "error": True, "data": result})

    if not wait_for_completion:
        return {
            "mode": "batch_parallel",
            "total": len(prompts),
            "tasks_created": len([t for t in task_ids if "task_id" in t]),
            "task_ids": task_ids
        }

    # FASE 2: Aguarda TODAS em paralelo (asyncio.gather não bloqueia)
    async def wait_and_download(task_info):
        """Aguarda uma task e faz download se necessário"""
        if task_info.get("error"):
            return task_info

        task_id = task_info["task_id"]
        prompt = task_info["prompt"]

        # Aguarda de forma assíncrona
        final_result = await wait_for_task_completion_async(task_id)

        if final_result.get("code") == 200:
            data = final_result.get("data", {})
            response_data = data.get("response", {})
            image_urls = response_data.get("resultUrls", [])
            response = {
                "status": "success",
                "prompt": prompt,
                "task_id": task_id,
                "image_urls": image_urls,
                "cost_time": data.get("costTime"),
                "consume_credits": data.get("consumeCredits")
            }

            if auto_download and image_urls:
                downloads = []
                for url in image_urls:
                    download_result = download_image(url, prompt=prompt)
                    if download_result.get("success"):
                        downloads.append({
                            "url": url,
                            "path": download_result["path"],
                            "filename": download_result["filename"]
                        })
                response["downloads"] = downloads
                response["downloads_path"] = DOWNLOADS_PATH

            return response
        else:
            return {"error": True, "prompt": prompt, "data": final_result}

    # Executa TODAS em paralelo
    results = await asyncio.gather(*[wait_and_download(t) for t in task_ids])

    # Estatísticas
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("error")]

    return {
        "mode": "batch_parallel",
        "total": len(prompts),
        "successful": len(successful),
        "failed": len(failed),
        "results": results,
        "total_time": sum((r.get("cost_time") or 0) for r in successful) if successful else 0
    }


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Executa uma ferramenta"""

    if name == "generate_image":
        prompt = arguments.get("prompt")
        prompts = arguments.get("prompts")
        files_url = arguments.get("files_url")
        size = arguments.get("size", "1:1")
        n_variants = arguments.get("n_variants", 1)
        mask_url = arguments.get("mask_url")
        is_enhance = arguments.get("is_enhance", False)
        enable_fallback = arguments.get("enable_fallback", True)
        fallback_model = arguments.get("fallback_model", "GPT_IMAGE_1")
        wait_for_completion = arguments.get("wait_for_completion", True)
        auto_download = arguments.get("auto_download", False)

        # Verifica se é batch ou single
        if prompts:
            # MODO BATCH (1-15 imagens em paralelo)
            batch_result = await generate_batch_parallel(
                prompts, size, wait_for_completion, auto_download,
                n_variants, is_enhance, enable_fallback, fallback_model
            )

            return [TextContent(
                type="text",
                text=json.dumps(batch_result, indent=2)
            )]

        elif prompt:
            # MODO SINGLE (1 imagem)
            result = create_image_task(prompt, size, files_url, n_variants, mask_url,
                                      is_enhance, enable_fallback, fallback_model)

            if result.get("code") != 200:
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]

            task_id = result.get("data", {}).get("taskId")

            if not wait_for_completion:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "task_created",
                        "task_id": task_id,
                        "message": "Task criada"
                    }, indent=2)
                )]

            # Aguarda conclusão
            final_result = wait_for_task_completion(task_id)

            if final_result.get("code") == 200:
                data = final_result.get("data", {})
                response_data = data.get("response", {})
                image_urls = response_data.get("resultUrls", [])
                response = {
                    "status": "success",
                    "task_id": task_id,
                    "image_urls": image_urls,
                    "cost_time": data.get("costTime"),
                    "consume_credits": data.get("consumeCredits")
                }

                if auto_download and image_urls:
                    downloads = []
                    for url in image_urls:
                        download_result = download_image(url, prompt=prompt)
                        if download_result.get("success"):
                            downloads.append({
                                "url": url,
                                "path": download_result["path"],
                                "filename": download_result["filename"]
                            })
                    response["downloads"] = downloads
                    response["downloads_path"] = DOWNLOADS_PATH

                return [TextContent(
                    type="text",
                    text=json.dumps(response, indent=2)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=json.dumps(final_result, indent=2)
                )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Forneça 'prompt' (1 imagem) ou 'prompts' (2-4 imagens)"}, indent=2)
            )]

    elif name == "download_image":
        url = arguments.get("url")
        filename = arguments.get("filename")

        if not url:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "URL é obrigatória"}, indent=2)
            )]

        result = download_image(url, filename)

        if result.get("success"):
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "message": "Imagem baixada com sucesso",
                    "path": result["path"],
                    "filename": result["filename"],
                    "downloads_folder": DOWNLOADS_PATH
                }, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "error": result["error"]
                }, indent=2)
            )]

    elif name == "check_task_status":
        task_id = arguments.get("task_id")

        if not task_id:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "task_id é obrigatório"}, indent=2)
            )]

        result = query_task(task_id)

        if result.get("code") == 200:
            data = result.get("data", {})
            status = data.get("status")
            progress = data.get("progress")

            response = {
                "task_id": task_id,
                "status": status,
                "progress": progress,
                "create_time": data.get("createTime"),
                "update_time": data.get("updateTime")
            }

            if status == "SUCCESS":
                response_data = data.get("response", {})
                response["image_urls"] = response_data.get("resultUrls", [])
                response["cost_time"] = data.get("costTime")
                response["consume_credits"] = data.get("consumeCredits")
            elif status == "FAILED":
                response["fail_code"] = data.get("failCode")
                response["fail_msg"] = data.get("failMsg")

            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Ferramenta desconhecida: {name}"}, indent=2)
        )]


async def main():
    """Inicia o servidor MCP"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kie-gpt-image",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
