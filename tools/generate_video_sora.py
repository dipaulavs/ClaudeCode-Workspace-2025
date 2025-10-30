#!/usr/bin/env python3
"""
Script para gerar vídeos usando Sora 2 (OpenAI) via API Kie.ai
Vídeos são salvos automaticamente na pasta Downloads
"""

import requests
import time
import sys
import json
import os
from datetime import datetime
from pathlib import Path

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


def generate_video(prompt, aspect_ratio="portrait", remove_watermark=True):
    """
    Gera um vídeo usando Sora 2 API

    Args:
        prompt: Descrição do vídeo a ser gerado
        aspect_ratio: Proporção do vídeo (landscape, portrait, square)
        remove_watermark: Remove marca d'água (True/False)

    Returns:
        task_id se sucesso, None se erro
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

    print(f"\n🎬 Gerando vídeo com Sora 2 (OpenAI)...")
    print(f"📝 Prompt: {prompt}")
    print(f"🖼️  Proporção: {aspect_ratio} | Duração: ~15s")
    if remove_watermark:
        print(f"✨ Marca d'água removida")

    try:
        response = requests.post(GENERATE_ENDPOINT, headers=HEADERS, json=payload)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 200:
            task_id = data["data"]["taskId"]
            print(f"✅ Tarefa criada com sucesso!")
            print(f"🆔 Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ Erro: {data.get('msg', 'Erro desconhecido')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return None


def check_status(task_id):
    """
    Verifica o status de uma tarefa de geração de vídeo

    Args:
        task_id: ID da tarefa

    Returns:
        dict com status e URLs dos vídeos (se disponíveis)
    """
    try:
        params = {"taskId": task_id}
        response = requests.get(STATUS_ENDPOINT, headers=HEADERS, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao verificar status: {e}")
        return None


def wait_for_completion(task_id, max_wait=600, check_interval=10):
    """
    Aguarda a conclusão da geração do vídeo
    Vídeos demoram mais que imagens, então aumentamos o tempo de espera

    Args:
        task_id: ID da tarefa
        max_wait: Tempo máximo de espera em segundos (padrão: 10 minutos)
        check_interval: Intervalo entre verificações em segundos

    Returns:
        Lista de URLs dos vídeos gerados ou None se erro
    """
    print(f"\n⏳ Aguardando geração do vídeo (pode levar alguns minutos)...")

    start_time = time.time()
    last_status = None

    while time.time() - start_time < max_wait:
        result = check_status(task_id)

        if not result:
            return None

        status = result.get("data", {}).get("state")

        # Mostra mudanças de status
        if status != last_status:
            print(f"📊 Status: {status}")
            last_status = status

        if status == "success":
            print(f"\n✅ Vídeo gerado com sucesso!")
            # resultJson é uma string JSON que precisa ser parseada
            result_json_str = result.get("data", {}).get("resultJson", "{}")
            result_json = json.loads(result_json_str)
            video_urls = result_json.get("resultUrls", [])
            return video_urls

        elif status == "fail":
            fail_msg = result.get("data", {}).get("failMsg", "Erro desconhecido")
            print(f"\n❌ Falha na geração: {fail_msg}")
            return None

        elif status in ["processing", "pending", "waiting"]:
            elapsed = int(time.time() - start_time)
            print(f"⏳ Processando... ({elapsed}s)", end="\r")
            time.sleep(check_interval)

        else:
            time.sleep(check_interval)

    print(f"\n⚠️  Timeout: A geração demorou mais de {max_wait} segundos")
    return None


def download_video(url, output_path=None):
    """
    Baixa um vídeo da URL fornecida e salva na pasta Downloads

    Args:
        url: URL do vídeo
        output_path: Caminho onde salvar o vídeo (opcional)

    Returns:
        Caminho do arquivo salvo
    """
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DOWNLOADS_PATH, f"sora_video_{timestamp}.mp4")

        print(f"\n📥 Baixando vídeo...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    progress = (downloaded / total_size) * 100
                    print(f"📥 Baixando: {progress:.1f}%", end="\r")

        print(f"\n💾 Vídeo salvo em: {output_path}")

        # Mostra tamanho do arquivo
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        print(f"📊 Tamanho: {file_size:.2f} MB")

        return output_path

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao baixar vídeo: {e}")
        return None


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("🎬 Gerador de Vídeos - Sora 2 (OpenAI)\n")
        print("Uso: python3 generate_video_sora.py \"seu prompt aqui\" [opções]")
        print("\nOpções:")
        print("  --aspect RATIO  Proporção do vídeo (landscape, portrait, square). Padrão: portrait")
        print("  --watermark    Mantém a marca d'água (padrão: remove)")
        print("\nExemplos:")
        print('  python3 generate_video_sora.py "Um gato brincando com um novelo de lã"')
        print('  python3 generate_video_sora.py "Paisagem de montanha ao amanhecer" --aspect portrait')
        print('  python3 generate_video_sora.py "Cidade futurista" --aspect square')
        print(f"\n🎬 Usando Sora 2 (OpenAI) para geração de vídeos")
        print(f"📂 Vídeos serão salvos em: {DOWNLOADS_PATH}")
        print(f"⚠️  Geração de vídeos pode levar alguns minutos")
        sys.exit(1)

    # Parse dos argumentos
    prompt = sys.argv[1]
    aspect_ratio = "portrait"
    remove_watermark = True

    if "--aspect" in sys.argv:
        idx = sys.argv.index("--aspect")
        if idx + 1 < len(sys.argv):
            ratio = sys.argv[idx + 1].lower()
            if ratio in ["landscape", "portrait", "square"]:
                aspect_ratio = ratio
            else:
                print("⚠️  Proporção inválida. Usando landscape.")

    if "--watermark" in sys.argv:
        remove_watermark = False

    # Gera o vídeo
    task_id = generate_video(prompt, aspect_ratio=aspect_ratio, remove_watermark=remove_watermark)

    if not task_id:
        sys.exit(1)

    # Aguarda conclusão
    video_urls = wait_for_completion(task_id)

    if not video_urls:
        sys.exit(1)

    # Baixa os vídeos
    print(f"\n🎬 {len(video_urls)} vídeo(s) gerado(s):")
    for i, url in enumerate(video_urls, 1):
        print(f"\n{i}. {url}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if len(video_urls) > 1:
            output_path = os.path.join(DOWNLOADS_PATH, f"sora_video_{timestamp}_v{i}.mp4")
        else:
            output_path = os.path.join(DOWNLOADS_PATH, f"sora_video_{timestamp}.mp4")

        download_video(url, output_path)

    print("\n✨ Concluído!")
    print(f"📂 Verifique seu(s) vídeo(s) em: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
