#!/usr/bin/env python3
"""
MCP Server para Geração de Imagens com KIE.AI (NanoBanana)
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

app = Server("kie-nanobanana-create")


def create_image_task(prompt: str, output_format: str = "png", image_size: str = "1:1") -> dict:
    """Cria uma task de geração de imagem na API KIE.AI"""
    url = f"{API_BASE_URL}/jobs/createTask"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "google/nano-banana",
        "input": {
            "prompt": prompt,
            "output_format": output_format,
            "image_size": image_size
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def query_task(task_id: str) -> dict:
    """Consulta o status de uma task"""
    url = f"{API_BASE_URL}/jobs/recordInfo"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {"taskId": task_id}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def wait_for_task_completion(task_id: str, max_wait: int = 60) -> dict:
    """Aguarda a conclusão da task com polling"""
    import time
    import json as json_module

    waited = 0
    while waited < max_wait:
        result = query_task(task_id)

        if result.get("code") != 200:
            return result

        data = result.get("data", {})
        state = data.get("state")

        if state == "success":
            # Parse do resultJson se for string
            result_json_str = data.get("resultJson", "{}")
            if isinstance(result_json_str, str):
                data["resultJson"] = json_module.loads(result_json_str)
            return result
        elif state == "fail":
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
            description="Gera uma ou múltiplas imagens em paralelo usando o modelo NanoBanana. Use 'prompt' para 1 imagem ou 'prompts' para 2-4 imagens simultâneas.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt único para gerar 1 imagem (máx 5000 caracteres). Use este OU 'prompts', não ambos.",
                        "maxLength": 5000
                    },
                    "prompts": {
                        "type": "array",
                        "description": "Lista de 2-4 prompts para gerar múltiplas imagens em PARALELO (simultâneo). Use este OU 'prompt', não ambos.",
                        "items": {
                            "type": "string",
                            "maxLength": 5000
                        },
                        "minItems": 2,
                        "maxItems": 4
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Formato de saída da imagem",
                        "enum": ["png", "jpeg"],
                        "default": "png"
                    },
                    "image_size": {
                        "type": "string",
                        "description": "Proporção da imagem",
                        "enum": ["1:1", "9:16", "16:9", "3:4", "4:3", "3:2", "2:3", "5:4", "4:5", "21:9", "auto"],
                        "default": "4:5"
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
                },
                "required": ["prompt"]
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


async def generate_single_image(prompt: str, output_format: str, image_size: str,
                               wait_for_completion: bool, auto_download: bool) -> dict:
    """Gera uma única imagem (função auxiliar)"""
    # Cria a task
    result = create_image_task(prompt, output_format, image_size)

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
                    "message": "Task criada. Use check_task_status para verificar o progresso."
                }, indent=2)
            )]

        # Aguarda conclusão
        final_result = wait_for_task_completion(task_id)

        if final_result.get("code") == 200:
            data = final_result.get("data", {})

            # resultJson pode ser string ou já estar parseado
            result_json = data.get("resultJson", {})
            if isinstance(result_json, str):
                result_json = json.loads(result_json)

            image_urls = result_json.get("resultUrls", [])
            response = {
                "status": "success",
                "task_id": task_id,
                "image_urls": image_urls,
                "cost_time": data.get("costTime"),
                "consume_credits": data.get("consumeCredits")
            }

            # Download automático se solicitado
            if auto_download and image_urls:
                downloads = []
                for i, url in enumerate(image_urls, 1):
                    download_result = download_image(url, prompt=prompt)  # Passa o prompt
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
            state = data.get("state")

            response = {
                "task_id": task_id,
                "state": state,
                "create_time": data.get("createTime"),
                "update_time": data.get("updateTime")
            }

            if state == "success":
                # resultJson pode ser string ou já estar parseado
                result_json = data.get("resultJson", {})
                if isinstance(result_json, str):
                    result_json = json.loads(result_json)

                response["image_urls"] = result_json.get("resultUrls", [])
                response["cost_time"] = data.get("costTime")
                response["consume_credits"] = data.get("consumeCredits")
            elif state == "fail":
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
                server_name="kie-nanobanana-create",
                server_version="2.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
