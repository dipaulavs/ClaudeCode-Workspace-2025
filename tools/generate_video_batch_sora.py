#!/usr/bin/env python3
"""
Script para gerar múltiplos vídeos simultaneamente usando Sora 2 (OpenAI)
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


def create_task(prompt, aspect_ratio="portrait", remove_watermark=True):
    """
    Cria uma tarefa de geração de vídeo (não aguarda conclusão)

    Args:
        prompt: Descrição do vídeo
        aspect_ratio: Proporção (landscape, portrait, square)
        remove_watermark: Remove marca d'água

    Returns:
        dict com task_id e prompt, ou None se erro
    """
    payload = {
        "model": "sora-2-text-to-video",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "n_frames": "15",
            "remove_watermark": remove_watermark
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
                "aspect_ratio": aspect_ratio,
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
        dict com status e video_urls (se pronto)
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
                "video_urls": result_json.get("resultUrls", [])
            }
        elif status == "fail":
            return {"status": "failed"}
        else:
            return {"status": "processing"}

    except Exception:
        return {"status": "error"}


def download_video(url, output_path):
    """Baixa um vídeo da URL"""
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
    Monitora uma tarefa até conclusão e baixa o vídeo

    Args:
        task_info: dict com task_id e prompt

    Returns:
        dict com resultado
    """
    task_id = task_info["task_id"]
    prompt = task_info["prompt"]

    max_wait = 600  # 10 minutos para vídeos
    check_interval = 10
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)

        if result["status"] == "success":
            video_urls = result["video_urls"]
            if not video_urls:
                return {"success": False, "prompt": prompt, "error": "No video URL"}

            # Baixa o vídeo
            url = video_urls[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')

            output_path = os.path.join(DOWNLOADS_PATH, f"batch_sora_{safe_prompt}_{timestamp}.mp4")

            downloaded = download_video(url, output_path)

            if downloaded:
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                return {
                    "success": True,
                    "prompt": prompt,
                    "path": output_path,
                    "url": url,
                    "size_mb": file_size
                }

            return {"success": False, "prompt": prompt, "error": "Download failed"}

        elif result["status"] == "failed":
            return {"success": False, "prompt": prompt, "error": "Generation failed"}

        time.sleep(check_interval)

    return {"success": False, "prompt": prompt, "error": "Timeout"}


def generate_batch(prompts, aspect_ratio="portrait", remove_watermark=True):
    """
    Gera múltiplos vídeos em paralelo

    Args:
        prompts: lista de prompts
        aspect_ratio: proporção dos vídeos
        remove_watermark: remover marca d'água

    Returns:
        lista de resultados
    """
    print(f"\n🎬 Gerador de Vídeos em Lote - Sora 2 (OpenAI)")
    print(f"📝 {len(prompts)} vídeo(s) para gerar")
    print(f"🖼️  Proporção: {aspect_ratio} | Duração: ~15s")
    if remove_watermark:
        print(f"✨ Marca d'água removida")
    print(f"⚡ Modo: Paralelo (todos ao mesmo tempo)")
    print(f"⚠️  Geração de vídeos pode levar vários minutos\n")

    # Fase 1: Criar todas as tarefas
    print("🚀 Fase 1: Criando todas as tarefas...")
    tasks = []

    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i}/{len(prompts)}] {prompt[:50]}...")
        task = create_task(prompt, aspect_ratio=aspect_ratio, remove_watermark=remove_watermark)
        if task:
            tasks.append(task)
            print(f"   ✅ Task ID: {task['task_id']}")
        else:
            print(f"   ❌ Falha ao criar tarefa")

    if not tasks:
        print("\n❌ Nenhuma tarefa foi criada com sucesso")
        return []

    print(f"\n✅ {len(tasks)} tarefa(s) criada(s) com sucesso!")
    print(f"\n⏳ Fase 2: Monitorando e baixando ({len(tasks)} em paralelo)...")
    print(f"⏱️  Estimativa: 2-5 minutos por vídeo\n")

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
                print(f"   ✅ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      💾 {os.path.basename(result['path'])}")
                print(f"      📊 Tamanho: {result['size_mb']:.2f} MB")
            else:
                print(f"   ❌ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      ⚠️  {result.get('error', 'Unknown error')}")

    return results


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("🎬 Gerador de Vídeos em Lote - Sora 2 (OpenAI)\n")
        print("Uso:")
        print('  python3 generate_video_batch_sora.py "prompt1" "prompt2" "prompt3" [opções]\n')
        print("Opções:")
        print("  --aspect RATIO  Proporção (landscape, portrait, square). Padrão: portrait")
        print("  --watermark    Mantém a marca d'água (padrão: remove)\n")
        print("Exemplos:")
        print('  python3 generate_video_batch_sora.py "Gato brincando" "Cachorro correndo"')
        print('  python3 generate_video_batch_sora.py "Paisagem 1" "Paisagem 2" --aspect portrait')
        print('  python3 generate_video_batch_sora.py "Cena 1" "Cena 2" "Cena 3" --aspect square\n')
        print("💡 Todas as tarefas são criadas e processadas em paralelo!")
        print(f"📂 Vídeos são salvos em: {DOWNLOADS_PATH}")
        print(f"⚠️  Geração pode levar 2-5 minutos por vídeo")
        sys.exit(1)

    # Parse dos argumentos
    prompts = []
    aspect_ratio = "portrait"
    remove_watermark = True

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--aspect":
            if i + 1 < len(sys.argv):
                ratio = sys.argv[i + 1].lower()
                if ratio in ["landscape", "portrait", "square"]:
                    aspect_ratio = ratio
                else:
                    print("⚠️  Proporção inválida. Usando landscape.")
                i += 2
            else:
                i += 1
        elif arg == "--watermark":
            remove_watermark = False
            i += 1
        else:
            prompts.append(arg)
            i += 1

    if not prompts:
        print("❌ Erro: Nenhum prompt fornecido")
        sys.exit(1)

    # Gera os vídeos em lote
    start_time = time.time()
    results = generate_batch(prompts, aspect_ratio=aspect_ratio, remove_watermark=remove_watermark)
    elapsed = time.time() - start_time

    # Resumo
    print(f"\n{'='*60}")
    print(f"✨ Processamento concluído em {elapsed/60:.1f} minutos ({elapsed:.1f}s)")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    total_size = sum(r.get("size_mb", 0) for r in successful)

    print(f"✅ Sucesso: {len(successful)}/{len(results)} vídeos")
    if successful:
        print(f"📊 Tamanho total: {total_size:.2f} MB\n")
        for r in successful:
            print(f"   📁 {os.path.basename(r['path'])} ({r['size_mb']:.2f} MB)")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
