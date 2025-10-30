#!/usr/bin/env python3
"""
Script para editar imagens usando o Nano Banana (Gemini 2.5 Flash Image Preview) via API Kie.ai
Permite fornecer uma imagem de referência e um prompt de edição
"""

import requests
import time
import sys
import json
import os
import argparse
from datetime import datetime
from pathlib import Path
import subprocess

# Configuração da API
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai"
GENERATE_ENDPOINT = f"{BASE_URL}/api/v1/jobs/createTask"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/jobs/recordInfo"

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Path do script de upload
UPLOAD_SCRIPT = os.path.join(os.path.dirname(__file__), "upload_to_nextcloud.py")

# Headers para autenticação
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def upload_to_nextcloud(image_path, expire_days=1):
    """
    Faz upload da imagem para o Nextcloud e retorna a URL pública

    Args:
        image_path: Caminho da imagem local
        expire_days: Dias até expiração do link

    Returns:
        URL pública da imagem
    """
    print(f"\n📤 Fazendo upload da imagem para Nextcloud...")

    try:
        # Executa o script de upload
        result = subprocess.run(
            ["python3", UPLOAD_SCRIPT, image_path, "--days", str(expire_days)],
            capture_output=True,
            text=True,
            check=True
        )

        # Extrai a URL da saída
        output = result.stdout
        for line in output.split('\n'):
            if line.startswith('http'):
                url = line.strip()
                print(f"✅ Upload concluído: {url}")
                return url

        raise Exception("URL não encontrada na saída do upload")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no upload: {e.stderr}")
        raise
    except Exception as e:
        print(f"❌ Erro: {e}")
        raise


def edit_image(prompt, image_url, output_format="PNG", image_size="auto"):
    """
    Edita uma imagem usando o Nano Banana Edit API

    Args:
        prompt: Descrição da edição a ser feita
        image_url: URL da imagem de referência
        output_format: Formato da imagem (PNG ou JPEG)
        image_size: Proporção da imagem (1:1, 9:16, 16:9, 3:4, 4:3, 3:2, 2:3, 5:4, 4:5, 21:9, auto)

    Returns:
        task_id se sucesso, None se erro
    """
    # Payload da requisição
    payload = {
        "model": "google/nano-banana-edit",
        "input": {
            "prompt": prompt,
            "image_urls": [image_url],
            "image_size": image_size,
            "output_format": output_format.lower()
        }
    }

    print(f"\n✏️  Editando imagem com Nano Banana Edit (Gemini 2.5 Flash)...")
    print(f"📝 Prompt: {prompt}")
    print(f"🖼️  Imagem de referência: {image_url[:60]}...")
    print(f"📐 Formato: {output_format} | Proporção: {image_size}")

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
    Verifica o status de uma tarefa de edição de imagem

    Args:
        task_id: ID da tarefa

    Returns:
        dict com status e URLs das imagens (se disponíveis)
    """
    try:
        params = {"taskId": task_id}
        response = requests.get(STATUS_ENDPOINT, headers=HEADERS, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao verificar status: {e}")
        return None


def wait_for_completion(task_id, max_wait=300, check_interval=5):
    """
    Aguarda a conclusão da edição da imagem

    Args:
        task_id: ID da tarefa
        max_wait: Tempo máximo de espera em segundos
        check_interval: Intervalo entre verificações em segundos

    Returns:
        Lista de URLs das imagens geradas ou None se erro
    """
    print(f"\n⏳ Aguardando processamento da edição...")

    start_time = time.time()
    while time.time() - start_time < max_wait:
        result = check_status(task_id)

        if not result:
            return None

        status = result.get("data", {}).get("state")

        if status == "success":
            print(f"\n✅ Imagem editada com sucesso!")
            # resultJson é uma string JSON que precisa ser parseada
            result_json_str = result.get("data", {}).get("resultJson", "{}")
            result_json = json.loads(result_json_str)
            image_urls = result_json.get("resultUrls", [])
            return image_urls

        elif status == "fail":
            fail_msg = result.get("data", {}).get("failMsg", "Erro desconhecido")
            print(f"\n❌ Falha na edição: {fail_msg}")
            return None

        elif status in ["processing", "pending"]:
            print(f"⏳ Processando...", end="\r")
            time.sleep(check_interval)

        else:
            print(f"📊 Status: {status}")
            time.sleep(check_interval)

    print(f"\n⚠️  Timeout: A edição demorou mais de {max_wait} segundos")
    return None


def download_image(url, output_path=None):
    """
    Baixa uma imagem da URL fornecida e salva na pasta Downloads

    Args:
        url: URL da imagem
        output_path: Caminho onde salvar a imagem (opcional)

    Returns:
        Caminho do arquivo salvo
    """
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(DOWNLOADS_PATH, f"nanobanana_edited_{timestamp}.png")

        print(f"\n📥 Baixando imagem editada...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"💾 Imagem salva em: {output_path}")
        return output_path

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao baixar imagem: {e}")
        return None


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Edita imagens usando Nano Banana (Gemini 2.5 Flash)',
        epilog='Exemplos:\n'
               '  %(prog)s imagem.jpg "trocar cachorro por gato"\n'
               '  %(prog)s foto.png "adicionar flores no fundo" --format JPEG\n'
               '  %(prog)s --url https://example.com/image.jpg "mudar cor para azul"\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('image_source', nargs='?', help='Caminho da imagem local')
    parser.add_argument('prompt', help='Descrição da edição a ser feita')
    parser.add_argument('--url', help='URL da imagem (alternativa ao caminho local)')
    parser.add_argument('--format', choices=['PNG', 'JPEG'], default='PNG',
                        help='Formato da imagem de saída (padrão: PNG)')
    parser.add_argument('--size', default='auto',
                        choices=['1:1', '9:16', '16:9', '3:4', '4:3', '3:2', '2:3', '5:4', '4:5', '21:9', 'auto'],
                        help='Proporção da imagem de saída (padrão: auto)')
    parser.add_argument('--expire-days', type=int, default=1,
                        help='Dias até expiração do link no Nextcloud (padrão: 1)')

    args = parser.parse_args()

    # Validação
    if not args.url and not args.image_source:
        parser.error("É necessário fornecer um caminho de imagem ou --url")

    if args.url and args.image_source:
        parser.error("Forneça apenas um caminho de imagem OU --url, não ambos")

    try:
        # Determina a URL da imagem
        if args.url:
            image_url = args.url
            print(f"🖼️  Usando URL fornecida: {image_url}")
        else:
            # Verifica se o arquivo existe
            if not os.path.exists(args.image_source):
                print(f"❌ Erro: Arquivo não encontrado: {args.image_source}")
                sys.exit(1)

            # Faz upload para Nextcloud
            image_url = upload_to_nextcloud(args.image_source, args.expire_days)

        # Edita a imagem
        task_id = edit_image(args.prompt, image_url, output_format=args.format, image_size=args.size)

        if not task_id:
            sys.exit(1)

        # Aguarda conclusão
        image_urls = wait_for_completion(task_id)

        if not image_urls:
            sys.exit(1)

        # Baixa as imagens
        print(f"\n🖼️  {len(image_urls)} imagem(ns) editada(s):")
        for i, url in enumerate(image_urls, 1):
            print(f"\n{i}. {url}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if len(image_urls) > 1:
                output_path = os.path.join(DOWNLOADS_PATH, f"nanobanana_edited_{timestamp}_v{i}.png")
            else:
                output_path = os.path.join(DOWNLOADS_PATH, f"nanobanana_edited_{timestamp}.png")

            download_image(url, output_path)

        print("\n✨ Edição concluída!")
        print(f"📂 Verifique sua imagem editada em: {DOWNLOADS_PATH}")

    except Exception as e:
        print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
