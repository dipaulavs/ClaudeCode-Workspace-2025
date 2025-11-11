#!/usr/bin/env python3
"""
Template: Gerar Imagem com Nano Banana via OpenRouter

Gera imagens usando google/gemini-2.5-flash-image via OpenRouter API.
Suporta diferentes aspect ratios e salva automaticamente em ~/Downloads.

Uso:
    python3 scripts/image-generation/generate_openrouter_nanobanana.py "seu prompt aqui"
    python3 scripts/image-generation/generate_openrouter_nanobanana.py "logo minimalista" --ratio 1:1
    python3 scripts/image-generation/generate_openrouter_nanobanana.py "banner site" --ratio 16:9
"""

import sys
import os
import argparse
import requests
import base64
from pathlib import Path
from datetime import datetime


def get_api_key():
    """Obtém a chave da API do OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY não encontrada")
        print("💡 Configure: export OPENROUTER_API_KEY='sua-chave'")
        sys.exit(1)
    return api_key


def generate_image(prompt, aspect_ratio="2:3"):
    """
    Gera imagem usando OpenRouter API

    Args:
        prompt: Descrição da imagem
        aspect_ratio: Proporção (1:1, 16:9, 4:3, 9:16, 2:3, 3:2, etc)

    Returns:
        base64_data: String base64 da imagem PNG
    """
    api_key = get_api_key()

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.5-flash-image",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": aspect_ratio
        }
    }

    print(f"🚀 Gerando imagem...")
    print(f"📐 Aspect ratio: {aspect_ratio}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # Extrai a imagem da resposta
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0]["message"]

            if "images" in message and len(message["images"]) > 0:
                image_data = message["images"][0]["image_url"]["url"]

                # Remove o prefixo "data:image/png;base64,"
                if image_data.startswith("data:image/png;base64,"):
                    return image_data.split(",", 1)[1]
                else:
                    return image_data
            else:
                print("❌ Nenhuma imagem retornada na resposta")
                return None
        else:
            print("❌ Resposta inválida da API")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None


def save_image(base64_data, prompt, output_dir=None):
    """
    Salva imagem base64 em arquivo PNG

    Args:
        base64_data: String base64 da imagem
        prompt: Prompt usado (para nome do arquivo)
        output_dir: Diretório de saída (padrão: ~/Downloads)

    Returns:
        output_path: Caminho do arquivo salvo
    """
    if output_dir is None:
        output_dir = str(Path.home() / "Downloads")

    # Cria nome descritivo do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Limpa o prompt para nome de arquivo
    clean_prompt = prompt[:50].replace(" ", "_").replace("/", "_")
    clean_prompt = "".join(c for c in clean_prompt if c.isalnum() or c in "_-")

    filename = f"nanobanana_{clean_prompt}_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)

    # Decodifica e salva
    try:
        image_bytes = base64.b64decode(base64_data)

        with open(output_path, "wb") as f:
            f.write(image_bytes)

        print(f"✅ Imagem salva: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Erro ao salvar imagem: {e}")
        return None


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gerar imagem com Nano Banana via OpenRouter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python3 generate_openrouter_nanobanana.py "gato astronauta"
    python3 generate_openrouter_nanobanana.py "logo empresa" --ratio 1:1
    python3 generate_openrouter_nanobanana.py "banner site" --ratio 16:9
    python3 generate_openrouter_nanobanana.py "thumbnail youtube" --ratio 16:9

Aspect Ratios suportados:
    1:1, 16:9, 4:3, 9:16, 2:3, 3:2, 21:9, 5:4, etc.

Configuração:
    export OPENROUTER_API_KEY='sk-or-v1-...'
        """
    )

    parser.add_argument('prompt', help='Descrição da imagem a ser gerada')
    parser.add_argument('--ratio', '-r', default='2:3',
                        help='Aspect ratio (padrão: 2:3 portrait)')
    parser.add_argument('--output', '-o',
                        help='Diretório de saída (padrão: ~/Downloads)')

    args = parser.parse_args()

    print("🍌 Nano Banana via OpenRouter")
    print("=" * 60)
    print(f"📝 Prompt: {args.prompt}")

    # Gera a imagem
    base64_data = generate_image(args.prompt, args.ratio)

    if not base64_data:
        print("❌ Falha ao gerar imagem")
        sys.exit(1)

    # Salva a imagem
    output_path = save_image(base64_data, args.prompt, args.output)

    if output_path:
        print("\n✅ Concluído com sucesso!")
        print(f"📂 Arquivo: {output_path}")
        return 0
    else:
        print("❌ Falha ao salvar imagem")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
