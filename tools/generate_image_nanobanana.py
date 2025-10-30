#!/usr/bin/env python3
"""
Script para gerar imagens usando o Nano Banana (Gemini 2.5 Flash Image Preview) via API Kie.ai
Configurado para sempre gerar imagens em modo portrait (2:3)
Imagens são salvas automaticamente na pasta Downloads
"""

import requests
import time
import sys
import json
import os
import re
import random
import string
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


def translate_to_portuguese(text):
    """
    Traduz texto para português usando Google Translate API gratuita
    """
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "pt",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            result = response.json()
            translated = result[0][0][0]
            return translated
        return text
    except:
        return text  # Se falhar, retorna o texto original


def create_descriptive_filename(prompt, extension="png", max_length=50):
    """
    Cria um nome de arquivo descritivo baseado no prompt em português
    """
    # Traduz para português
    translated_text = translate_to_portuguese(prompt)

    # Remove caracteres especiais, mantém acentos
    clean_text = re.sub(r'[^\w\s]', '', translated_text)

    # Pega as primeiras palavras
    words = clean_text.lower().split()[:6]  # Primeiras 6 palavras

    # Junta com underscore
    descriptive_part = '_'.join(words)

    # Limita o tamanho
    if len(descriptive_part) > max_length:
        descriptive_part = descriptive_part[:max_length]

    # Gera código aleatório curto (4 caracteres)
    random_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    # Monta o nome final
    filename = f"{descriptive_part}_{random_code}.{extension}"

    return filename


def generate_image(prompt, output_format="PNG", image_urls=None):
    """
    Gera uma imagem usando o Nano Banana API

    Args:
        prompt: Descrição da imagem a ser gerada
        output_format: Formato da imagem (PNG ou JPEG)
        image_urls: Lista de URLs de imagens de referência para edição (opcional)

    Returns:
        task_id se sucesso, None se erro
    """
    # Payload da requisição - sempre em modo portrait (2:3)
    payload = {
        "model": "google/nano-banana",
        "input": {
            "prompt": prompt,
            "image_size": "2:3",  # Modo portrait
            "output_format": output_format.lower()
        }
    }

    # Adiciona URLs de imagens se fornecidas (para edição)
    if image_urls:
        payload["input"]["image_urls"] = image_urls if isinstance(image_urls, list) else [image_urls]

    print(f"\n🍌 Gerando imagem com Nano Banana (Gemini 2.5 Flash)...")
    print(f"📝 Prompt: {prompt}")
    print(f"🖼️  Formato: {output_format} | Tamanho: Portrait (2:3)")

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
    Verifica o status de uma tarefa de geração de imagem

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
    Aguarda a conclusão da geração da imagem

    Args:
        task_id: ID da tarefa
        max_wait: Tempo máximo de espera em segundos
        check_interval: Intervalo entre verificações em segundos

    Returns:
        Lista de URLs das imagens geradas ou None se erro
    """
    print(f"\n⏳ Aguardando geração da imagem...")

    start_time = time.time()
    while time.time() - start_time < max_wait:
        result = check_status(task_id)

        if not result:
            return None

        status = result.get("data", {}).get("state")

        if status == "success":
            print(f"\n✅ Imagem gerada com sucesso!")
            # resultJson é uma string JSON que precisa ser parseada
            result_json_str = result.get("data", {}).get("resultJson", "{}")
            result_json = json.loads(result_json_str)
            image_urls = result_json.get("resultUrls", [])
            return image_urls

        elif status == "fail":
            fail_msg = result.get("data", {}).get("failMsg", "Erro desconhecido")
            print(f"\n❌ Falha na geração: {fail_msg}")
            return None

        elif status in ["processing", "pending"]:
            print(f"⏳ Processando...", end="\r")
            time.sleep(check_interval)

        else:
            print(f"📊 Status: {status}")
            time.sleep(check_interval)

    print(f"\n⚠️  Timeout: A geração demorou mais de {max_wait} segundos")
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
            output_path = os.path.join(DOWNLOADS_PATH, f"nanobanana_image_{timestamp}.png")

        print(f"\n📥 Baixando imagem...")
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
    if len(sys.argv) < 2:
        print("Uso: python3 generate_image_nanobanana.py \"seu prompt aqui\" [--format FORMAT]")
        print("\nOpções:")
        print("  --format FORMAT  Formato da imagem (PNG ou JPEG). Padrão: PNG")
        print("\nExemplo:")
        print('  python3 generate_image_nanobanana.py "Um gato fofo em um jardim"')
        print('  python3 generate_image_nanobanana.py "Cidade futurista" --format JPEG')
        print(f"\n🍌 Usando Nano Banana (Gemini 2.5 Flash Image Preview)")
        print(f"📂 Imagens serão salvas em: {DOWNLOADS_PATH}")
        print(f"🖼️  Todas as imagens são geradas em formato portrait (2:3)")
        sys.exit(1)

    # Parse dos argumentos
    prompt = sys.argv[1]
    output_format = "PNG"

    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            fmt = sys.argv[idx + 1].upper()
            if fmt in ["PNG", "JPEG"]:
                output_format = fmt
            else:
                print("⚠️  Formato inválido. Usando PNG.")

    # Gera a imagem
    task_id = generate_image(prompt, output_format=output_format)

    if not task_id:
        sys.exit(1)

    # Aguarda conclusão
    image_urls = wait_for_completion(task_id)

    if not image_urls:
        sys.exit(1)

    # Baixa as imagens
    print(f"\n🖼️  {len(image_urls)} imagem(ns) gerada(s):")
    for i, url in enumerate(image_urls, 1):
        print(f"\n{i}. {url}")

        # Usa nome descritivo baseado no prompt
        extension = output_format.lower()
        if len(image_urls) > 1:
            base_filename = create_descriptive_filename(prompt, extension=extension)
            name_parts = base_filename.rsplit('.', 1)
            output_path = os.path.join(DOWNLOADS_PATH, f"{name_parts[0]}_v{i}.{name_parts[1]}")
        else:
            filename = create_descriptive_filename(prompt, extension=extension)
            output_path = os.path.join(DOWNLOADS_PATH, filename)

        download_image(url, output_path)

    print("\n✨ Concluído!")
    print(f"📂 Verifique suas imagens em: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
