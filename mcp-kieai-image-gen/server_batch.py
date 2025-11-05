#!/usr/bin/env python3
"""
Handler para suporte a geração em lote (batch) paralela
"""
import asyncio
import json
from typing import Any


async def generate_single_image_async(prompt: str, output_format: str, image_size: str,
                                     wait_for_completion: bool, auto_download: bool,
                                     create_image_task_func, wait_for_task_completion_func,
                                     download_image_func, DOWNLOADS_PATH) -> dict:
    """
    Gera uma única imagem de forma assíncrona
    Retorna dict com resultado (não TextContent)
    """
    # Cria a task
    result = create_image_task_func(prompt, output_format, image_size)

    if result.get("code") != 200:
        return {"error": True, "data": result}

    task_id = result.get("data", {}).get("taskId")

    if not wait_for_completion:
        return {
            "status": "task_created",
            "task_id": task_id,
            "prompt": prompt,
            "message": "Task criada"
        }

    # Aguarda conclusão (síncrono, mas será chamado em paralelo via asyncio)
    final_result = wait_for_task_completion_func(task_id)

    if final_result.get("code") == 200:
        data = final_result.get("data", {})

        # resultJson pode ser string ou já estar parseado
        result_json = data.get("resultJson", {})
        if isinstance(result_json, str):
            result_json = json.loads(result_json)

        image_urls = result_json.get("resultUrls", [])
        response = {
            "status": "success",
            "prompt": prompt,
            "task_id": task_id,
            "image_urls": image_urls,
            "cost_time": data.get("costTime"),
            "consume_credits": data.get("consumeCredits")
        }

        # Download automático se solicitado
        if auto_download and image_urls:
            downloads = []
            for url in image_urls:
                download_result = download_image_func(url, prompt=prompt)
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
        return {"error": True, "data": final_result}


async def handle_batch_generation(prompts: list, output_format: str, image_size: str,
                                  wait_for_completion: bool, auto_download: bool,
                                  create_image_task_func, wait_for_task_completion_func,
                                  download_image_func, DOWNLOADS_PATH) -> dict:
    """
    Gera múltiplas imagens em PARALELO
    """
    # Cria tasks para todas as imagens simultaneamente
    tasks = []
    for prompt in prompts:
        task = generate_single_image_async(
            prompt, output_format, image_size,
            wait_for_completion, auto_download,
            create_image_task_func, wait_for_task_completion_func,
            download_image_func, DOWNLOADS_PATH
        )
        tasks.append(task)

    # Executa todas em paralelo
    results = await asyncio.gather(*tasks)

    # Monta resposta agregada
    batch_response = {
        "mode": "batch",
        "total": len(prompts),
        "results": results
    }

    # Estatísticas
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("error")]

    batch_response["successful"] = len(successful)
    batch_response["failed"] = len(failed)

    if successful:
        total_time = sum(r.get("cost_time", 0) for r in successful)
        batch_response["total_time"] = total_time

    return batch_response
