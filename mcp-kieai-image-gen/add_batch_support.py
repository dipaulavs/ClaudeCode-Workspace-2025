#!/usr/bin/env python3
"""
Script para adicionar suporte a batch no server.py
"""

# Código a ser inserido antes do @app.call_tool()

BATCH_FUNCTIONS = '''
async def generate_single_async(prompt: str, output_format: str, image_size: str,
                               wait_for_completion: bool, auto_download: bool) -> dict:
    """Gera uma única imagem de forma assíncrona (retorna dict, não TextContent)"""
    result = create_image_task(prompt, output_format, image_size)

    if result.get("code") != 200:
        return {"error": True, "prompt": prompt, "data": result}

    task_id = result.get("data", {}).get("taskId")

    if not wait_for_completion:
        return {
            "status": "task_created",
            "prompt": prompt,
            "task_id": task_id
        }

    # Aguarda conclusão
    final_result = wait_for_task_completion(task_id)

    if final_result.get("code") == 200:
        data = final_result.get("data", {})
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


async def generate_batch_async(prompts: list, output_format: str, image_size: str,
                              wait_for_completion: bool, auto_download: bool) -> dict:
    """Gera múltiplas imagens EM PARALELO"""
    import asyncio

    # Cria tasks para todas as imagens
    tasks = [
        generate_single_async(p, output_format, image_size, wait_for_completion, auto_download)
        for p in prompts
    ]

    # Executa TODAS em paralelo
    results = await asyncio.gather(*tasks)

    # Estatísticas
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("error")]

    return {
        "mode": "batch_parallel",
        "total": len(prompts),
        "successful": len(successful),
        "failed": len(failed),
        "results": results,
        "total_time": sum(r.get("cost_time", 0) for r in successful) if successful else 0
    }
'''

print("Adicione este código no server.py antes do @app.call_tool():")
print(BATCH_FUNCTIONS)
print("\n" + "="*60)
print("Depois, modifique o handler para detectar 'prompt' vs 'prompts'")
