#!/usr/bin/env python3
"""
Script para editar múltiplas imagens de anúncios de imóveis simultaneamente usando Nano Banana Edit
Cria todas as tarefas de uma vez e monitora em paralelo para máxima eficiência
Aspect ratio: 4:5 (Instagram Feed Portrait)
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


def create_edit_task(prompt, image_url, output_format="PNG", image_size="4:5"):
    """
    Cria uma tarefa de edição de anúncio (não aguarda conclusão)

    Args:
        prompt: Descrição da edição
        image_url: URL da imagem base (foto do imóvel)
        output_format: Formato da imagem (PNG ou JPEG)
        image_size: Proporção (4:5 para Instagram Feed)

    Returns:
        dict com task_id e prompt, ou None se erro
    """
    payload = {
        "model": "google/nano-banana-edit",
        "input": {
            "prompt": prompt,
            "image_urls": [image_url],
            "image_size": image_size,
            "output_format": output_format.lower(),
            "num_outputs": 1
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
                # Sanitiza o prompt para nome de arquivo (primeiras palavras)
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_prompt = safe_prompt.replace(' ', '_')

                ext = ".jpg" if output_format.upper() == "JPEG" else ".png"
                output_path = os.path.join(DOWNLOADS_PATH, f"ad_realestate_{safe_prompt}_{timestamp}{ext}")

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
            return {"success": False, "prompt": prompt, "error": "Edit failed"}

        time.sleep(check_interval)

    return {"success": False, "prompt": prompt, "error": "Timeout"}


def edit_batch(prompts, image_url, output_format="PNG", image_size="4:5"):
    """
    Edita múltiplas imagens de anúncios em paralelo

    Args:
        prompts: lista de prompts (hooks + descrição)
        image_url: URL da imagem base (foto do imóvel)
        output_format: formato das imagens
        image_size: proporção das imagens (4:5 para Instagram Feed)

    Returns:
        lista de resultados
    """
    print(f"\n🏠 Gerador de Anúncios de Imóveis - Nano Banana Edit")
    print(f"📝 {len(prompts)} criativos para gerar")
    print(f"🖼️  Formato: {output_format} | Proporção: {image_size} (Instagram Feed)")
    print(f"📷 Foto do imóvel: {image_url[:60]}...")
    print(f"⚡ Modo: Paralelo (todos ao mesmo tempo)\n")

    # Fase 1: Criar todas as tarefas
    print("🚀 Fase 1: Criando todas as tarefas de edição...")
    tasks = []

    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i}/{len(prompts)}] {prompt[:60]}...")
        task = create_edit_task(prompt, image_url, output_format, image_size)
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
                print(f"      🔗 {result['url']}")
            else:
                print(f"   ❌ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      ⚠️  {result.get('error', 'Unknown error')}")

    return results


def main():
    """Função principal com suporte a argumentos"""

    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Gerar criativos de anúncios de imóveis em lote (4:5 portrait)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    # Gerar 4 criativos com prompts diferentes
    python3 tools/batch_edit_ads_portrait.py \\
      --image-url "https://exemplo.com/imovel.jpg" \\
      "prompt criativo 1..." \\
      "prompt criativo 2..." \\
      "prompt criativo 3..." \\
      "prompt criativo 4..."

    # Com formato JPEG
    python3 tools/batch_edit_ads_portrait.py \\
      --image-url "https://exemplo.com/imovel.jpg" \\
      --format JPEG \\
      "prompt 1" "prompt 2"
        """
    )

    parser.add_argument('--image-url', '-u', required=True,
                        help='URL da foto do imóvel (obrigatório)')
    parser.add_argument('--format', '-f', default='PNG', choices=['PNG', 'JPEG'],
                        help='Formato da imagem de saída. Padrão: PNG')
    parser.add_argument('--size', '-s', default='4:5',
                        choices=['4:5', '9:16'],
                        help='Proporção da imagem (4:5=Feed, 9:16=Stories). Padrão: 4:5')
    parser.add_argument('prompts', nargs='+',
                        help='Prompts de edição (um por criativo)')

    args = parser.parse_args()

    print(f"🏠 Gerador de Anúncios de Imóveis - Modo Produção")
    print("="*60)

    # Gera os criativos
    start_time = time.time()
    results = edit_batch(args.prompts, args.image_url, args.format, args.size)
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
            print(f"   🔗 {r['url']}\n")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {DOWNLOADS_PATH}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
