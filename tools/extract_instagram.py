#!/usr/bin/env python3
"""
Extrator de Conteúdo do Instagram via Apify
Baixa imagens e legendas de posts/carrosséis do Instagram
"""

import requests
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
import os

# Configuração
APIFY_API_KEY = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
ACTOR_ID = "nH2AHrwxeTRJoN5hX"
APIFY_API_URL = "https://api.apify.com/v2"
DOWNLOADS_DIR = Path.home() / "Downloads"

def run_actor(instagram_url, results_limit=30):
    """
    Executa o actor do Apify para extrair dados do Instagram
    """
    url = f"{APIFY_API_URL}/acts/{ACTOR_ID}/runs"

    headers = {
        "Content-Type": "application/json"
    }

    # Prepara o input do Actor
    input_data = {
        "username": [instagram_url],
        "resultsLimit": results_limit
    }

    params = {
        "token": APIFY_API_KEY
    }

    print(f"🚀 Iniciando extração do Instagram...")
    print(f"📍 URL: {instagram_url}")

    # Inicia o Actor
    response = requests.post(url, json=input_data, headers=headers, params=params)

    if response.status_code not in [200, 201]:
        print(f"❌ Erro ao iniciar Actor: {response.status_code}")
        print(response.text)
        return None

    run_data = response.json()
    run_id = run_data["data"]["id"]

    print(f"⏳ Aguardando processamento (Run ID: {run_id})...")

    # Aguarda conclusão
    status_url = f"{APIFY_API_URL}/actor-runs/{run_id}"

    while True:
        status_response = requests.get(status_url, params=params)
        status_data = status_response.json()
        status = status_data["data"]["status"]

        if status == "SUCCEEDED":
            print("✅ Extração concluída!")
            return status_data["data"]["defaultDatasetId"]
        elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
            print(f"❌ Falha na extração: {status}")
            return None

        time.sleep(3)

def get_dataset_items(dataset_id):
    """
    Busca os itens do dataset
    """
    url = f"{APIFY_API_URL}/datasets/{dataset_id}/items"
    params = {
        "token": APIFY_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Erro ao buscar dados: {response.status_code}")
        return []

    return response.json()

def download_image(url, filepath):
    """
    Baixa uma imagem
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            print(f"   ⚠️  Status {response.status_code} ao baixar")
            return False
    except Exception as e:
        print(f"   ⚠️  Erro: {str(e)[:50]}")
        return False

def extract_content(instagram_url, results_limit=30):
    """
    Extrai conteúdo do Instagram: imagens e legenda
    """
    # Executa o Actor
    dataset_id = run_actor(instagram_url, results_limit)

    if not dataset_id:
        return

    # Busca os dados
    print("📥 Baixando dados...")
    items = get_dataset_items(dataset_id)

    if not items:
        print("❌ Nenhum dado encontrado")
        return

    # Cria pasta com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = DOWNLOADS_DIR / f"instagram_extract_{timestamp}"
    output_dir.mkdir(exist_ok=True)

    print(f"\n📁 Salvando em: {output_dir}")

    # Processa cada item (post)
    for idx, item in enumerate(items, 1):
        print(f"\n--- Post {idx} ---")

        # Extrai informações básicas
        caption = item.get("caption", "")
        owner_username = item.get("ownerUsername", "unknown")
        likes = item.get("likesCount", 0)
        comments = item.get("commentsCount", 0)
        post_url = item.get("url", "")

        print(f"👤 Autor: @{owner_username}")
        print(f"❤️  Likes: {likes:,}")
        print(f"💬 Comentários: {comments:,}")
        print(f"🔗 URL: {post_url}")

        # Salva legenda
        caption_file = output_dir / f"post_{idx:02d}_caption.txt"
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {post_url}\n")
            f.write(f"Autor: @{owner_username}\n")
            f.write(f"Likes: {likes:,}\n")
            f.write(f"Comentários: {comments:,}\n")
            f.write(f"\n--- LEGENDA ---\n\n")
            f.write(caption)

        print(f"💾 Legenda salva: {caption_file.name}")

        # Baixa imagens
        images = []

        # Verifica childPosts (carrossel)
        child_posts = item.get("childPosts", [])
        if child_posts:
            print(f"🎠 Carrossel detectado com {len(child_posts)} itens")
            for child in child_posts:
                if child.get("displayUrl"):
                    images.append(child.get("displayUrl"))

        # Se não tem childPosts, pega da lista images ou displayUrl
        if not images:
            images = item.get("images", [])
            if not images and item.get("displayUrl"):
                images = [item.get("displayUrl")]

        if images:
            print(f"🖼️  Baixando {len(images)} imagem(ns)...")
            for img_idx, img_url in enumerate(images, 1):
                img_filename = f"post_{idx:02d}_img_{img_idx:02d}.jpg"
                img_filepath = output_dir / img_filename

                if download_image(img_url, img_filepath):
                    print(f"   ✅ {img_filename}")
                else:
                    print(f"   ❌ Erro ao baixar {img_filename}")
        else:
            print("⚠️  Nenhuma imagem encontrada")

        # Salva dados completos em JSON
        json_file = output_dir / f"post_{idx:02d}_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(item, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Extração completa!")
    print(f"📂 {len(items)} post(s) salvos em: {output_dir}")

    return output_dir

def main():
    parser = argparse.ArgumentParser(
        description="Extrai imagens e legendas de posts do Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Extrair um post específico
  python3 extract_instagram.py "https://www.instagram.com/p/DLNsnpUTdVS/"

  # Extrair posts de um perfil (últimos 30)
  python3 extract_instagram.py "https://www.instagram.com/natgeo/"

  # Extrair apenas username
  python3 extract_instagram.py "natgeo"

  # Limitar quantidade de posts
  python3 extract_instagram.py "natgeo" --limit 10
        """
    )

    parser.add_argument(
        "url",
        help="URL do Instagram (post, perfil ou username)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Limite de resultados (padrão: 30)"
    )

    args = parser.parse_args()

    extract_content(args.url, args.limit)

if __name__ == "__main__":
    main()
