#!/usr/bin/env python3
"""
Script para gerar múltiplas imagens simultaneamente usando Nano Banana (Gemini 2.5 Flash)
Cria todas as tarefas de uma vez e monitora em paralelo para máxima eficiência
"""

import requests
import time
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração da API
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai"
GENERATE_ENDPOINT = f"{BASE_URL}/api/v1/jobs/createTask"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/jobs/recordInfo"

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Headers para autenticação
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def create_task(prompt, output_format="PNG"):
    """
    Cria uma tarefa de geração de imagem (não aguarda conclusão)

    Args:
        prompt: Descrição da imagem
        output_format: Formato da imagem (PNG ou JPEG)

    Returns:
        dict com task_id e prompt, ou None se erro
    """
    payload = {
        "model": "google/nano-banana",
        "input": {
            "prompt": prompt,
            "image_size": "2:3",  # Modo portrait
            "output_format": output_format.lower()
        }
    }

    try:
        response = requests.post(GENERATE_ENDPOINT, headers=HEADERS, json=payload)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 200:
            task_id = data["data"]["taskId"]
            return {
                "task_id": task_id,
                "prompt": prompt,
                "status": "created"
            }
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def check_task_status(task_id):
    """
    Verifica o status de uma tarefa

    Returns:
        dict com status e image_urls (se pronto)
    """
    try:
        params = {"taskId": task_id}
        response = requests.get(STATUS_ENDPOINT, headers=HEADERS, params=params)
        response.raise_for_status()

        result = response.json()
        status = result.get("data", {}).get("state")

        if status == "success":
            result_json_str = result.get("data", {}).get("resultJson", "{}")
            result_json = json.loads(result_json_str)
            return {
                "status": "success",
                "image_urls": result_json.get("resultUrls", [])
            }
        elif status == "fail":
            return {"status": "failed"}
        else:
            return {"status": "processing"}

    except Exception:
        return {"status": "error"}


def download_image(url, output_path):
    """Baixa uma imagem da URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return output_path
    except Exception:
        return None


def monitor_and_download(task_info, output_format="PNG"):
    """
    Monitora uma tarefa até conclusão e baixa a imagem

    Args:
        task_info: dict com task_id e prompt
        output_format: formato da imagem

    Returns:
        dict com resultado
    """
    task_id = task_info["task_id"]
    prompt = task_info["prompt"]

    max_wait = 300
    check_interval = 3
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)

        if result["status"] == "success":
            image_urls = result["image_urls"]
            if image_urls:
                url = image_urls[0]

                # Define nome do arquivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Sanitiza o prompt para nome de arquivo
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_prompt = safe_prompt.replace(' ', '_')

                ext = ".jpg" if output_format.upper() == "JPEG" else ".png"
                output_path = os.path.join(DOWNLOADS_PATH, f"batch_{safe_prompt}_{timestamp}{ext}")

                # Baixa a imagem
                downloaded = download_image(url, output_path)

                if downloaded:
                    return {
                        "success": True,
                        "prompt": prompt,
                        "path": output_path,
                        "url": url
                    }

            return {"success": False, "prompt": prompt, "error": "No image URL"}

        elif result["status"] == "failed":
            return {"success": False, "prompt": prompt, "error": "Generation failed"}

        time.sleep(check_interval)

    return {"success": False, "prompt": prompt, "error": "Timeout"}


def generate_batch(prompts, output_format="PNG"):
    """
    Gera múltiplas imagens em paralelo

    Args:
        prompts: lista de prompts
        output_format: formato das imagens

    Returns:
        lista de resultados
    """
    print(f"\n🍌 Gerador de Imagens em Lote - Nano Banana")
    print(f"📝 {len(prompts)} imagens para gerar")
    print(f"🖼️  Formato: {output_format} | Tamanho: Portrait (2:3)")
    print(f"⚡ Modo: Paralelo (todas ao mesmo tempo)\n")

    # Fase 1: Criar todas as tarefas
    print("🚀 Fase 1: Criando todas as tarefas...")
    tasks = []

    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i}/{len(prompts)}] {prompt[:50]}...")
        task = create_task(prompt, output_format)
        if task:
            tasks.append(task)
            print(f"   ✅ Task ID: {task['task_id']}")
        else:
            print(f"   ❌ Falha ao criar tarefa")

    if not tasks:
        print("\n❌ Nenhuma tarefa foi criada com sucesso")
        return []

    print(f"\n✅ {len(tasks)} tarefas criadas com sucesso!")
    print(f"\n⏳ Fase 2: Monitorando e baixando ({len(tasks)} em paralelo)...")

    # Fase 2: Monitorar todas as tarefas em paralelo
    results = []
    completed = 0

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_task = {
            executor.submit(monitor_and_download, task, output_format): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            completed += 1
            result = future.result()
            results.append(result)

            if result["success"]:
                print(f"   ✅ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      💾 {result['path']}")
            else:
                print(f"   ❌ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      ⚠️  {result.get('error', 'Unknown error')}")

    return results


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("🍌 Gerador de Imagens em Lote - Nano Banana\n")
        print("Uso:")
        print('  python3 generate_image_batch.py "prompt1" "prompt2" "prompt3" [--format FORMAT]\n')
        print("Opções:")
        print("  --format FORMAT  Formato das imagens (PNG ou JPEG). Padrão: PNG\n")
        print("Exemplos:")
        print('  python3 generate_image_batch.py "gato" "cachorro" "pássaro"')
        print('  python3 generate_image_batch.py "telefone" "computador" --format JPEG')
        print('  python3 generate_image_batch.py "paisagem 1" "paisagem 2" "paisagem 3" "paisagem 4"\n')
        print("💡 Todas as tarefas são criadas e processadas em paralelo!")
        print(f"📂 Imagens são salvas em: {DOWNLOADS_PATH}")
        sys.exit(1)

    # Parse dos argumentos
    prompts = []
    output_format = "PNG"

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--format":
            if i + 1 < len(sys.argv):
                fmt = sys.argv[i + 1].upper()
                if fmt in ["PNG", "JPEG"]:
                    output_format = fmt
                i += 2
            else:
                i += 1
        else:
            prompts.append(arg)
            i += 1

    if not prompts:
        print("❌ Erro: Nenhum prompt fornecido")
        sys.exit(1)

    # Gera as imagens em lote
    start_time = time.time()
    results = generate_batch(prompts, output_format)
    elapsed = time.time() - start_time

    # Resumo
    print(f"\n{'='*60}")
    print(f"✨ Processamento concluído em {elapsed:.1f}s")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"✅ Sucesso: {len(successful)}/{len(results)}")
    if successful:
        for r in successful:
            print(f"   📁 {os.path.basename(r['path'])}")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
