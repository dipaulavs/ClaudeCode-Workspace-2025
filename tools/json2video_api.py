#!/usr/bin/env python3
"""
🎬 Ferramenta: API JSON2Video
Cria e edita vídeos via JSON usando json2video.com
"""

import os
import requests
import json
import time
from pathlib import Path


# API Configuration
API_BASE_URL = "https://api.json2video.com/v2"
API_KEY = os.getenv("JSON2VIDEO_API_KEY")


def get_api_key():
    """Retorna API key do ambiente"""
    if not API_KEY:
        raise ValueError(
            "❌ JSON2VIDEO_API_KEY não encontrada!\n"
            "Configure: export JSON2VIDEO_API_KEY='sua_api_key'\n"
            "Obtenha em: https://json2video.com/dashboard"
        )
    return API_KEY


def create_video(movie_json, json_file_path=None):
    """
    Cria um novo vídeo a partir de definição JSON

    Args:
        movie_json (dict): Definição do vídeo em JSON
        json_file_path (str, optional): Caminho do arquivo JSON (para logging)

    Returns:
        str: Project ID se sucesso, None se falha
    """
    api_key = get_api_key()

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    print("🎬 Enviando para renderização...")
    if json_file_path:
        print(f"📄 Arquivo: {json_file_path}")

    try:
        response = requests.post(
            f"{API_BASE_URL}/movies",
            headers=headers,
            json=movie_json,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                project_id = data.get("project")
                print(f"✅ Tarefa criada: {project_id}")
                print(f"🕒 Timestamp: {data.get('timestamp')}")
                return project_id
            else:
                print(f"❌ Erro na resposta: {data}")
                return None

        elif response.status_code == 401:
            print("❌ API key inválida ou ausente")
            print("Configure: export JSON2VIDEO_API_KEY='sua_key'")
            return None

        elif response.status_code == 403:
            print("❌ Quota esgotada")
            print("Verifique seu plano em: https://json2video.com/pricing")
            return None

        elif response.status_code == 400:
            print(f"❌ JSON inválido ou parâmetros incorretos")
            print(f"Detalhes: {response.text}")
            return None

        else:
            print(f"❌ Erro HTTP {response.status_code}")
            print(f"Resposta: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("❌ Timeout ao conectar com API")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


def check_status(project_id):
    """
    Verifica status de renderização

    Args:
        project_id (str): ID do projeto

    Returns:
        dict: Dados do vídeo se sucesso, None se falha
    """
    api_key = get_api_key()

    headers = {
        "x-api-key": api_key
    }

    try:
        response = requests.get(
            f"{API_BASE_URL}/movies",
            headers=headers,
            params={"project": project_id},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data
            else:
                print(f"❌ Erro: {data}")
                return None

        elif response.status_code == 404:
            print(f"❌ Project ID não encontrado: {project_id}")
            return None

        else:
            print(f"❌ Erro HTTP {response.status_code}")
            print(f"Resposta: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Erro ao checar status: {e}")
        return None


def wait_for_completion(project_id, max_wait=600, poll_interval=10):
    """
    Aguarda conclusão da renderização

    Args:
        project_id (str): ID do projeto
        max_wait (int): Tempo máximo de espera em segundos (padrão: 10 min)
        poll_interval (int): Intervalo entre verificações (padrão: 10s)

    Returns:
        str: URL do vídeo se sucesso, None se falha/timeout
    """
    print(f"\n⏳ Aguardando renderização (máx {max_wait}s)...")
    print("Status: ", end="", flush=True)

    start_time = time.time()
    last_status = None

    while time.time() - start_time < max_wait:
        elapsed = int(time.time() - start_time)

        data = check_status(project_id)

        if not data:
            print(f"\n❌ Erro ao verificar status")
            return None

        movie = data.get("movie", {})
        status = movie.get("status")

        # Mostrar progresso
        if status != last_status:
            if last_status:
                print(f" → {status}", end="", flush=True)
            else:
                print(status, end="", flush=True)
            last_status = status

        if status == "done":
            url = movie.get("url")
            duration = movie.get("duration")
            width = movie.get("width")
            height = movie.get("height")
            remaining = data.get("remaining_quota", {}).get("time", "?")

            print(f" ✅ ({elapsed}s)\n")
            print(f"🎬 Vídeo renderizado:")
            print(f"   URL: {url}")
            print(f"   Duração: {duration}s")
            print(f"   Resolução: {width}x{height}")
            print(f"   Quota restante: {remaining}s")

            return url

        elif status == "error":
            message = movie.get("message", "Erro desconhecido")
            print(f" ❌\n")
            print(f"❌ Erro na renderização: {message}")
            return None

        # Aguardar próxima verificação
        time.sleep(poll_interval)

    # Timeout
    print(f" ⏱️\n")
    print(f"⚠️ Timeout após {max_wait}s")
    print(f"Status atual: {last_status}")
    print(f"Use: python3 tools/json2video_api.py --status {project_id}")
    return None


def download_video(url, output_path):
    """
    Faz download do vídeo

    Args:
        url (str): URL do vídeo
        output_path (str): Caminho local para salvar

    Returns:
        bool: True se sucesso, False se falha
    """
    print(f"\n⬇️  Baixando vídeo...")
    print(f"📂 Salvando em: {output_path}")

    try:
        response = requests.get(url, stream=True, timeout=120)

        if response.status_code == 200:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'wb') as f:
                total = int(response.headers.get('content-length', 0))
                downloaded = 0

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Progresso
                        if total > 0:
                            percent = (downloaded / total) * 100
                            print(f"\r⬇️  Progresso: {percent:.1f}%", end="", flush=True)

            print(f"\n✅ Vídeo salvo: {output_path}")
            return True

        else:
            print(f"❌ Erro ao baixar: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Erro no download: {e}")
        return False


def main():
    """CLI para testes diretos"""
    import sys

    if len(sys.argv) < 2:
        print("🎬 JSON2Video API Tool")
        print("\nUso:")
        print("  python3 tools/json2video_api.py video.json")
        print("  python3 tools/json2video_api.py --status PROJECT_ID")
        print("\nExemplos:")
        print("  python3 tools/json2video_api.py example.json")
        print("  python3 tools/json2video_api.py --status abc123")
        sys.exit(1)

    # Modo status
    if sys.argv[1] == "--status":
        if len(sys.argv) < 3:
            print("❌ Forneça o PROJECT_ID")
            sys.exit(1)

        project_id = sys.argv[2]
        data = check_status(project_id)

        if data:
            print(json.dumps(data, indent=2))
        sys.exit(0)

    # Modo criar vídeo
    json_file = sys.argv[1]

    if not os.path.exists(json_file):
        print(f"❌ Arquivo não encontrado: {json_file}")
        sys.exit(1)

    with open(json_file, 'r') as f:
        movie_json = json.load(f)

    project_id = create_video(movie_json, json_file)

    if project_id:
        url = wait_for_completion(project_id)

        if url:
            # Download
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(Path.home() / "Downloads" / f"json2video_{timestamp}.mp4")

            download_video(url, output_path)
            print("\n✨ Concluído!")


if __name__ == "__main__":
    main()
