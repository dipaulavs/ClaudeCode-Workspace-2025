#!/usr/bin/env python3
"""
Transcritor de Reels do Instagram via Apify + OpenAI
Transcreve automaticamente o áudio de vídeos Reels do Instagram
"""

import requests
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Configuração
APIFY_API_KEY = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
OPENAI_API_KEY = "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"
ACTOR_ID = "QDd59HBnZaQ89Rghe"
APIFY_API_URL = "https://api.apify.com/v2"
DOWNLOADS_DIR = Path.home() / "Downloads"

def run_transcription_actor(instagram_url, model="gpt-4o-mini-transcribe", response_format="json"):
    """
    Executa o actor do Apify para transcrever Reels do Instagram
    """
    url = f"{APIFY_API_URL}/acts/{ACTOR_ID}/runs"

    headers = {
        "Content-Type": "application/json"
    }

    # Prepara o input do Actor
    input_data = {
        "instagramUrl": instagram_url,
        "model": model,
        "openaiApiKey": OPENAI_API_KEY,
        "response_format": response_format,
        "task": "transcription"
    }

    params = {
        "token": APIFY_API_KEY
    }

    print(f"🎬 Iniciando transcrição do Reels...")
    print(f"📍 URL: {instagram_url}")
    print(f"🤖 Modelo: {model}")

    # Inicia o Actor
    response = requests.post(url, json=input_data, headers=headers, params=params)

    if response.status_code not in [200, 201]:
        print(f"❌ Erro ao iniciar Actor: {response.status_code}")
        print(response.text)
        return None

    run_data = response.json()
    run_id = run_data["data"]["id"]

    print(f"⏳ Aguardando transcrição (Run ID: {run_id})...")
    print("   (Isso pode levar alguns minutos...)")

    # Aguarda conclusão
    status_url = f"{APIFY_API_URL}/actor-runs/{run_id}"

    while True:
        status_response = requests.get(status_url, params=params)
        status_data = status_response.json()
        status = status_data["data"]["status"]

        if status == "SUCCEEDED":
            print("✅ Transcrição concluída!")
            return status_data["data"]["defaultDatasetId"]
        elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
            print(f"❌ Falha na transcrição: {status}")
            return None

        time.sleep(5)

def get_transcription_results(dataset_id):
    """
    Busca os resultados da transcrição
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

def save_transcription(instagram_url, transcription_data, model):
    """
    Salva a transcrição em arquivo
    """
    # Cria pasta com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = DOWNLOADS_DIR / f"reels_transcription_{timestamp}"
    output_dir.mkdir(exist_ok=True)

    print(f"\n📁 Salvando em: {output_dir}")

    # Salva transcrição formatada
    transcription_file = output_dir / "transcription.txt"

    with open(transcription_file, 'w', encoding='utf-8') as f:
        f.write(f"TRANSCRIÇÃO DE REELS DO INSTAGRAM\n")
        f.write(f"=" * 60 + "\n\n")
        f.write(f"URL: {instagram_url}\n")
        f.write(f"Modelo: {model}\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"\n" + "=" * 60 + "\n\n")

        if isinstance(transcription_data, list) and len(transcription_data) > 0:
            item = transcription_data[0]

            # Extrai texto da transcrição
            if 'text' in item:
                f.write("TRANSCRIÇÃO:\n\n")
                f.write(item['text'])
                f.write("\n\n")

            # Informações adicionais se disponíveis
            if 'duration' in item:
                f.write(f"\nDuração: {item['duration']}s\n")

            if 'language' in item:
                f.write(f"Idioma detectado: {item['language']}\n")

    print(f"💾 Transcrição salva: transcription.txt")

    # Salva JSON completo
    json_file = output_dir / "transcription_full.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(transcription_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Dados completos salvos: transcription_full.json")

    # Exibe transcrição no terminal
    if isinstance(transcription_data, list) and len(transcription_data) > 0:
        item = transcription_data[0]
        if 'text' in item:
            print(f"\n{'=' * 60}")
            print("📝 TRANSCRIÇÃO:")
            print(f"{'=' * 60}\n")
            print(item['text'])
            print(f"\n{'=' * 60}\n")

    print(f"\n✅ Transcrição completa!")
    print(f"📂 Arquivos salvos em: {output_dir}")

    return output_dir

def transcribe_reels(instagram_url, model="gpt-4o-mini-transcribe"):
    """
    Transcreve um Reels do Instagram
    """
    # Executa o Actor
    dataset_id = run_transcription_actor(instagram_url, model)

    if not dataset_id:
        return

    # Busca os resultados
    print("📥 Baixando transcrição...")
    results = get_transcription_results(dataset_id)

    if not results:
        print("❌ Nenhuma transcrição encontrada")
        return

    # Salva transcrição
    save_transcription(instagram_url, results, model)

def main():
    parser = argparse.ArgumentParser(
        description="Transcreve áudio de Reels do Instagram automaticamente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Transcrever um Reels
  python3 transcribe_instagram_reels.py "https://www.instagram.com/reel/ABC123/"

  # Usar modelo específico
  python3 transcribe_instagram_reels.py "URL" --model gpt-4o-mini-transcribe

Modelos disponíveis:
  - gpt-4o-mini-transcribe (padrão, rápido e econômico)
  - gpt-4o-transcribe (mais preciso)
        """
    )

    parser.add_argument(
        "url",
        help="URL do Reels do Instagram"
    )

    parser.add_argument(
        "--model",
        default="gpt-4o-mini-transcribe",
        help="Modelo de transcrição OpenAI (padrão: gpt-4o-mini-transcribe)"
    )

    args = parser.parse_args()

    transcribe_reels(args.url, args.model)

if __name__ == "__main__":
    main()
