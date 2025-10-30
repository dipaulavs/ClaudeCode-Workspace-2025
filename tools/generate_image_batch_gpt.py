#!/usr/bin/env python3
"""
Script para gerar múltiplas imagens simultaneamente usando GPT-4o Image
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
GENERATE_ENDPOINT = f"{BASE_URL}/api/v1/gpt4o-image/generate"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/gpt4o-image/record-info"

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Headers para autenticação
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def create_task(prompt, n_variants=1, enhance=False):
    """
    Cria uma tarefa de geração de imagem (não aguarda conclusão)

    Args:
        prompt: Descrição da imagem
        n_variants: Número de variações (1, 2 ou 4)
        enhance: Se True, ativa o refinamento do prompt

    Returns:
        dict com task_id e prompt, ou None se erro
    """
    payload = {
        "prompt": prompt,
        "size": "2:3",  # Modo portrait
        "nVariants": n_variants,
        "isEnhance": enhance
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
                "n_variants": n_variants,
                "enhance": enhance,
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
        status = result.get("data", {}).get("status")
        progress = result.get("data", {}).get("progress", "0.00")

        if status == "SUCCESS":
            image_urls = result.get("data", {}).get("response", {}).get("resultUrls", [])
            return {
                "status": "success",
                "image_urls": image_urls
            }
        elif status in ["CREATE_TASK_FAILED", "GENERATE_FAILED"]:
            return {"status": "failed"}
        elif status == "GENERATING":
            return {
                "status": "processing",
                "progress": float(progress) * 100
            }
        else:
            return {"status": "processing", "progress": 0}

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


def monitor_and_download(task_info):
    """
    Monitora uma tarefa até conclusão e baixa as imagens

    Args:
        task_info: dict com task_id, prompt e n_variants

    Returns:
        dict com resultado
    """
    task_id = task_info["task_id"]
    prompt = task_info["prompt"]
    n_variants = task_info["n_variants"]

    max_wait = 300
    check_interval = 3
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)

        if result["status"] == "success":
            image_urls = result["image_urls"]
            if not image_urls:
                return {"success": False, "prompt": prompt, "error": "No image URL"}

            # Baixa todas as variações
            downloaded_paths = []
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')

            for i, url in enumerate(image_urls, 1):
                if len(image_urls) > 1:
                    output_path = os.path.join(DOWNLOADS_PATH, f"batch_gpt_{safe_prompt}_{timestamp}_v{i}.png")
                else:
                    output_path = os.path.join(DOWNLOADS_PATH, f"batch_gpt_{safe_prompt}_{timestamp}.png")

                downloaded = download_image(url, output_path)
                if downloaded:
                    downloaded_paths.append(downloaded)

            if downloaded_paths:
                return {
                    "success": True,
                    "prompt": prompt,
                    "paths": downloaded_paths,
                    "urls": image_urls
                }
            else:
                return {"success": False, "prompt": prompt, "error": "Download failed"}

        elif result["status"] == "failed":
            return {"success": False, "prompt": prompt, "error": "Generation failed"}

        time.sleep(check_interval)

    return {"success": False, "prompt": prompt, "error": "Timeout"}


def generate_batch(prompts, n_variants=1, enhance=False):
    """
    Gera múltiplas imagens em paralelo

    Args:
        prompts: lista de prompts
        n_variants: número de variações por prompt
        enhance: ativar refinamento de prompt

    Returns:
        lista de resultados
    """
    print(f"\n🎨 Gerador de Imagens em Lote - GPT-4o Image")
    print(f"📝 {len(prompts)} prompt(s) para gerar")
    print(f"🖼️  Formato: Portrait (2:3) | Variações: {n_variants} por prompt")
    if enhance:
        print(f"✨ Refinamento de prompt ativado")
    print(f"⚡ Modo: Paralelo (todas ao mesmo tempo)\n")

    # Fase 1: Criar todas as tarefas
    print("🚀 Fase 1: Criando todas as tarefas...")
    tasks = []

    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i}/{len(prompts)}] {prompt[:50]}...")
        task = create_task(prompt, n_variants=n_variants, enhance=enhance)
        if task:
            tasks.append(task)
            print(f"   ✅ Task ID: {task['task_id']}")
        else:
            print(f"   ❌ Falha ao criar tarefa")

    if not tasks:
        print("\n❌ Nenhuma tarefa foi criada com sucesso")
        return []

    total_images = sum(task['n_variants'] for task in tasks)
    print(f"\n✅ {len(tasks)} tarefa(s) criada(s) com sucesso!")
    print(f"📊 Total de imagens esperadas: {total_images}")
    print(f"\n⏳ Fase 2: Monitorando e baixando ({len(tasks)} em paralelo)...")

    # Fase 2: Monitorar todas as tarefas em paralelo
    results = []
    completed = 0

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_task = {
            executor.submit(monitor_and_download, task): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            completed += 1
            result = future.result()
            results.append(result)

            if result["success"]:
                num_images = len(result.get("paths", []))
                print(f"   ✅ [{completed}/{len(tasks)}] {result['prompt'][:40]}... ({num_images} imagens)")
                for path in result.get("paths", []):
                    print(f"      💾 {os.path.basename(path)}")
            else:
                print(f"   ❌ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      ⚠️  {result.get('error', 'Unknown error')}")

    return results


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("🎨 Gerador de Imagens em Lote - GPT-4o Image\n")
        print("Uso:")
        print('  python3 generate_image_batch_gpt.py "prompt1" "prompt2" "prompt3" [opções]\n')
        print("Opções:")
        print("  --variants N    Número de variações por prompt (1, 2 ou 4). Padrão: 1")
        print("  --enhance       Ativa refinamento do prompt para melhor qualidade\n")
        print("Exemplos:")
        print('  python3 generate_image_batch_gpt.py "gato" "cachorro" "pássaro"')
        print('  python3 generate_image_batch_gpt.py "telefone" "computador" --variants 2')
        print('  python3 generate_image_batch_gpt.py "paisagem 1" "paisagem 2" --enhance')
        print('  python3 generate_image_batch_gpt.py "arte 1" "arte 2" --variants 4 --enhance\n')
        print("💡 Todas as tarefas são criadas e processadas em paralelo!")
        print(f"📂 Imagens são salvas em: {DOWNLOADS_PATH}")
        sys.exit(1)

    # Parse dos argumentos
    prompts = []
    n_variants = 1
    enhance = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--variants":
            if i + 1 < len(sys.argv):
                try:
                    n_variants = int(sys.argv[i + 1])
                    if n_variants not in [1, 2, 4]:
                        print("⚠️  Número de variações deve ser 1, 2 ou 4. Usando 1.")
                        n_variants = 1
                except ValueError:
                    print("⚠️  Número de variações inválido. Usando 1.")
                i += 2
            else:
                i += 1
        elif arg == "--enhance":
            enhance = True
            i += 1
        else:
            prompts.append(arg)
            i += 1

    if not prompts:
        print("❌ Erro: Nenhum prompt fornecido")
        sys.exit(1)

    # Gera as imagens em lote
    start_time = time.time()
    results = generate_batch(prompts, n_variants=n_variants, enhance=enhance)
    elapsed = time.time() - start_time

    # Resumo
    print(f"\n{'='*60}")
    print(f"✨ Processamento concluído em {elapsed:.1f}s")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    total_images = sum(len(r.get("paths", [])) for r in successful)

    print(f"✅ Sucesso: {len(successful)}/{len(results)} tarefas")
    print(f"🖼️  Total de imagens geradas: {total_images}")
    if successful:
        for r in successful:
            for path in r.get("paths", []):
                print(f"   📁 {os.path.basename(path)}")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
