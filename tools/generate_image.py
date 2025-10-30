#!/usr/bin/env python3
"""
Script para gerar imagens usando a API Kie.ai 4o Image Generation
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
GENERATE_ENDPOINT = f"{BASE_URL}/api/v1/gpt4o-image/generate"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/gpt4o-image/record-info"

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


def generate_image(prompt, n_variants=1, enhance=False, files_url=None):
    """
    Gera uma imagem usando a API

    Args:
        prompt: Descrição da imagem a ser gerada
        n_variants: Número de variações (1, 2 ou 4)
        enhance: Se True, ativa o refinamento do prompt
        files_url: Lista de URLs de imagens de referência (opcional)

    Returns:
        task_id se sucesso, None se erro
    """
    # Payload da requisição - sempre em modo portrait (2:3)
    payload = {
        "prompt": prompt,
        "size": "2:3",  # Modo portrait
        "nVariants": n_variants,
        "isEnhance": enhance
    }

    # Adiciona URLs de arquivos se fornecidas
    if files_url:
        payload["filesUrl"] = files_url if isinstance(files_url, list) else [files_url]

    print(f"\n🎨 Gerando imagem em modo portrait...")
    print(f"📝 Prompt: {prompt}")
    if enhance:
        print("✨ Refinamento de prompt ativado")

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

        status = result.get("data", {}).get("status")
        progress = result.get("data", {}).get("progress", "0.00")

        if status == "SUCCESS":
            print(f"\n✅ Imagem gerada com sucesso!")
            image_urls = result.get("data", {}).get("response", {}).get("resultUrls", [])
            return image_urls

        elif status in ["CREATE_TASK_FAILED", "GENERATE_FAILED"]:
            print(f"\n❌ Falha na geração: {status}")
            return None

        elif status == "GENERATING":
            progress_percent = float(progress) * 100
            print(f"⏳ Progresso: {progress_percent:.1f}%", end="\r")
            time.sleep(check_interval)

        else:
            print(f"📊 Status: {status}")
            time.sleep(check_interval)

    print(f"\n⚠️  Timeout: A geração demorou mais de {max_wait} segundos")
    return None


def download_image(url, output_path=None, prompt="generated_image"):
    """
    Baixa uma imagem da URL fornecida e salva na pasta Downloads

    Args:
        url: URL da imagem
        output_path: Caminho onde salvar a imagem (opcional)
        prompt: Prompt usado para gerar nome descritivo

    Returns:
        Caminho do arquivo salvo
    """
    try:
        if not output_path:
            filename = create_descriptive_filename(prompt, extension="png")
            output_path = os.path.join(DOWNLOADS_PATH, filename)

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
        print("Uso: python3 generate_image.py \"seu prompt aqui\" [--variants N] [--enhance]")
        print("\nOpções:")
        print("  --variants N    Número de variações (1, 2 ou 4). Padrão: 1")
        print("  --enhance       Ativa o refinamento do prompt")
        print("\nExemplo:")
        print('  python3 generate_image.py "Um gato fofo em um jardim" --variants 2 --enhance')
        print(f"\nImagens serão salvas em: {DOWNLOADS_PATH}")
        sys.exit(1)

    # Parse dos argumentos
    prompt = sys.argv[1]
    n_variants = 1
    enhance = False

    if "--variants" in sys.argv:
        idx = sys.argv.index("--variants")
        if idx + 1 < len(sys.argv):
            try:
                n_variants = int(sys.argv[idx + 1])
                if n_variants not in [1, 2, 4]:
                    print("⚠️  Número de variações deve ser 1, 2 ou 4. Usando 1.")
                    n_variants = 1
            except ValueError:
                print("⚠️  Número de variações inválido. Usando 1.")

    if "--enhance" in sys.argv:
        enhance = True

    # Gera a imagem
    task_id = generate_image(prompt, n_variants=n_variants, enhance=enhance)

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

        if len(image_urls) > 1:
            # Para múltiplas variantes, adiciona _v1, _v2, etc
            base_filename = create_descriptive_filename(prompt, extension="png")
            name_parts = base_filename.rsplit('.', 1)
            output_path = os.path.join(DOWNLOADS_PATH, f"{name_parts[0]}_v{i}.{name_parts[1]}")
        else:
            output_path = None

        download_image(url, output_path, prompt=prompt)

    print("\n✨ Concluído!")
    print(f"📂 Verifique suas imagens em: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
