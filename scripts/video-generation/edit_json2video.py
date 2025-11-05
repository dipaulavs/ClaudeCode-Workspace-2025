#!/usr/bin/env python3
"""
🎬 TEMPLATE: Edição de Vídeo via JSON (JSON2Video)

Cria e edita vídeos programaticamente usando JSON2Video API
Vídeos são salvos automaticamente em ~/Downloads/

Uso:
    python3 scripts/video-generation/edit_json2video.py video.json
    python3 scripts/video-generation/edit_json2video.py video.json --output ~/Desktop/result.mp4
    python3 scripts/video-generation/edit_json2video.py --status PROJECT_ID

Argumentos:
    video.json: Arquivo JSON com definição do vídeo
    --output: Caminho customizado para salvar (opcional)
    --status: Verificar status de renderização existente

Estrutura JSON mínima:
    {
      "scenes": [
        {
          "elements": [
            {
              "type": "text",
              "text": "Hello World"
            }
          ]
        }
      ]
    }

Retorna:
    Vídeo salvo em ~/Downloads/ no formato: json2video_YYYYMMDD_HHMMSS.mp4

Documentação completa:
    .claude/skills/json2video/SKILL.md
    .claude/skills/json2video/EXAMPLES.md
    .claude/skills/json2video/REFERENCE.md

API Key:
    export JSON2VIDEO_API_KEY='sua_api_key'
    Obtenha em: https://json2video.com/dashboard
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao path para importar ferramentas
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.json2video_api import (
    create_video,
    check_status,
    wait_for_completion,
    download_video
)

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")


def validate_json(movie_json):
    """
    Valida estrutura básica do JSON

    Args:
        movie_json (dict): JSON a validar

    Returns:
        tuple: (bool, str) - (válido, mensagem de erro)
    """
    # Verificar scenes
    if "scenes" not in movie_json:
        return False, "❌ Campo obrigatório 'scenes' ausente"

    if not isinstance(movie_json["scenes"], list):
        return False, "❌ 'scenes' deve ser um array"

    if len(movie_json["scenes"]) == 0:
        return False, "❌ 'scenes' não pode estar vazio"

    # Verificar elements em cada scene
    for i, scene in enumerate(movie_json["scenes"]):
        if "elements" not in scene:
            return False, f"❌ Scene {i+1}: campo 'elements' ausente"

        if not isinstance(scene["elements"], list):
            return False, f"❌ Scene {i+1}: 'elements' deve ser um array"

        if len(scene["elements"]) == 0:
            return False, f"❌ Scene {i+1}: 'elements' não pode estar vazio"

        # Verificar type em cada element
        for j, element in enumerate(scene["elements"]):
            if "type" not in element:
                return False, f"❌ Scene {i+1}, Element {j+1}: campo 'type' ausente"

            valid_types = ["text", "image", "video", "audio", "voice", "subtitles", "audiogram", "composition"]
            if element["type"] not in valid_types:
                return False, f"❌ Scene {i+1}, Element {j+1}: type '{element['type']}' inválido. Válidos: {valid_types}"

    return True, "✅ JSON válido"


def show_examples():
    """Mostra exemplos de uso"""
    print("\n📚 Exemplos de JSON:")
    print("\n1️⃣ Texto simples:")
    print("""
{
  "scenes": [
    {
      "background-color": "#000000",
      "elements": [
        {
          "type": "text",
          "text": "Hello World",
          "style": "001",
          "x": "center",
          "y": "center"
        }
      ]
    }
  ]
}
""")

    print("\n2️⃣ Imagem com texto:")
    print("""
{
  "resolution": "portrait",
  "quality": "high",
  "scenes": [
    {
      "elements": [
        {
          "type": "image",
          "src": "https://example.com/image.jpg",
          "width": "100%",
          "height": "100%"
        },
        {
          "type": "text",
          "text": "Legenda da imagem",
          "style": "002",
          "x": "center",
          "y": "bottom",
          "ys": -100
        }
      ]
    }
  ]
}
""")

    print("\n3️⃣ Vídeo com legendas automáticas:")
    print("""
{
  "resolution": "portrait",
  "scenes": [
    {
      "elements": [
        {
          "type": "video",
          "src": "https://example.com/video.mp4"
        },
        {
          "type": "subtitles",
          "auto": true,
          "style": "001",
          "max-words": 4
        }
      ]
    }
  ]
}
""")

    print("\n📖 Mais exemplos em: .claude/skills/json2video/EXAMPLES.md")


def main():
    """Executa criação de vídeo via JSON"""

    # Help
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("🎬 Editor de Vídeo JSON - JSON2Video")
        print("\n📋 Uso:")
        print("  python3 scripts/video-generation/edit_json2video.py video.json")
        print("  python3 scripts/video-generation/edit_json2video.py video.json --output ~/Desktop/result.mp4")
        print("  python3 scripts/video-generation/edit_json2video.py --status PROJECT_ID")
        print("\n📝 Opções:")
        print("  --output PATH   Caminho customizado para salvar o vídeo")
        print("  --status ID     Verificar status de projeto existente")
        print("  --examples      Mostrar exemplos de JSON")
        print("\n🔑 Configuração:")
        print("  export JSON2VIDEO_API_KEY='sua_api_key'")
        print("  Obtenha em: https://json2video.com/dashboard")
        print("\n📚 Documentação:")
        print("  .claude/skills/json2video/SKILL.md")
        print("  .claude/skills/json2video/EXAMPLES.md")
        print("  .claude/skills/json2video/REFERENCE.md")
        print(f"\n📂 Vídeos salvos em: {DOWNLOADS_PATH}")
        print("⚠️  Renderização pode levar 1-5 minutos")
        sys.exit(0)

    # Exemplos
    if sys.argv[1] == "--examples":
        show_examples()
        sys.exit(0)

    # Status check
    if sys.argv[1] == "--status":
        if len(sys.argv) < 3:
            print("❌ Forneça o PROJECT_ID")
            print("Uso: python3 scripts/video-generation/edit_json2video.py --status PROJECT_ID")
            sys.exit(1)

        project_id = sys.argv[2]
        print(f"🔍 Verificando status: {project_id}")

        data = check_status(project_id)

        if data:
            movie = data.get("movie", {})
            status = movie.get("status")

            print(f"\n📊 Status: {status}")

            if status == "done":
                print(f"✅ Vídeo concluído!")
                print(f"🎬 URL: {movie.get('url')}")
                print(f"⏱️  Duração: {movie.get('duration')}s")
                print(f"📐 Resolução: {movie.get('width')}x{movie.get('height')}")

                # Oferecer download
                print("\n⬇️  Fazer download? (y/n): ", end="")
                if input().lower() == 'y':
                    url = movie.get('url')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = os.path.join(DOWNLOADS_PATH, f"json2video_{timestamp}.mp4")
                    download_video(url, output_path)

            elif status == "error":
                print(f"❌ Erro: {movie.get('message')}")

            else:
                print(f"⏳ Renderizando... (status: {status})")
                print(f"Use novamente para verificar")

            # Quota
            remaining = data.get("remaining_quota", {}).get("time")
            if remaining is not None:
                print(f"\n💰 Quota restante: {remaining}s")

        sys.exit(0)

    # Modo criar vídeo
    json_file = sys.argv[1]

    # Output path customizado
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = os.path.expanduser(sys.argv[idx + 1])

    # Verificar arquivo
    if not os.path.exists(json_file):
        print(f"❌ Arquivo não encontrado: {json_file}")
        print("\n💡 Use --examples para ver exemplos de JSON")
        sys.exit(1)

    # Carregar JSON
    print(f"📄 Carregando: {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            movie_json = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}")
        print("\n💡 Valide o JSON em: https://jsonlint.com/")
        sys.exit(1)

    # Validar estrutura
    valid, message = validate_json(movie_json)
    print(message)

    if not valid:
        print("\n💡 Estrutura mínima:")
        print('{"scenes": [{"elements": [{"type": "text", "text": "Hello"}]}]}')
        print("\n📖 Ver exemplos: python3 scripts/video-generation/edit_json2video.py --examples")
        sys.exit(1)

    # Mostrar resumo
    num_scenes = len(movie_json.get("scenes", []))
    resolution = movie_json.get("resolution", "auto")
    quality = movie_json.get("quality", "medium")

    print(f"\n📊 Resumo:")
    print(f"   Scenes: {num_scenes}")
    print(f"   Resolução: {resolution}")
    print(f"   Qualidade: {quality}")

    # Criar vídeo
    project_id = create_video(movie_json, json_file)

    if not project_id:
        print("\n❌ Falha ao criar tarefa")
        sys.exit(1)

    # Aguardar conclusão
    video_url = wait_for_completion(project_id, max_wait=600)

    if not video_url:
        print(f"\n⚠️  Use para verificar status:")
        print(f"python3 scripts/video-generation/edit_json2video.py --status {project_id}")
        sys.exit(1)

    # Download
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(DOWNLOADS_PATH, f"json2video_{timestamp}.mp4")

    success = download_video(video_url, output_path)

    if success:
        print("\n✨ Concluído!")
        print(f"📂 Vídeo: {output_path}")
        print(f"🔗 URL: {video_url}")
    else:
        print(f"\n⚠️  Download falhou, mas vídeo está disponível em:")
        print(f"🔗 {video_url}")


if __name__ == "__main__":
    main()
