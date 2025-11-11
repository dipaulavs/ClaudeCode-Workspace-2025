#!/usr/bin/env python3
"""
Template: Batch de Imagens com Nano Banana via OpenRouter

Gera múltiplas imagens em paralelo usando google/gemini-2.5-flash-image via OpenRouter.

Uso:
    python3 batch_openrouter_nanobanana.py "prompt1" "prompt2" "prompt3"
    python3 batch_openrouter_nanobanana.py --ratio 16:9 "banner1" "banner2"
    python3 batch_openrouter_nanobanana.py --output ./uniformes "uniforme1" "uniforme2"
"""

import sys
import os
import argparse
import requests
import base64
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_api_key():
    """Obtém a chave da API do OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY não encontrada")
        print("💡 Configure: export OPENROUTER_API_KEY='sua-chave'")
        sys.exit(1)
    return api_key


def generate_image(prompt, aspect_ratio="2:3", index=None):
    """
    Gera imagem usando OpenRouter API

    Args:
        prompt: Descrição da imagem
        aspect_ratio: Proporção (1:1, 16:9, 4:3, 9:16, 2:3, 3:2, etc)
        index: Número da imagem no batch (para log)

    Returns:
        tuple: (prompt, base64_data) ou (prompt, None) em caso de erro
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

    prefix = f"[{index}]" if index else ""
    print(f"{prefix} 🚀 Gerando: {prompt[:60]}...")

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
                    base64_data = image_data.split(",", 1)[1]
                else:
                    base64_data = image_data

                print(f"{prefix} ✅ Concluído")
                return (prompt, base64_data)
            else:
                print(f"{prefix} ❌ Nenhuma imagem retornada")
                return (prompt, None)
        else:
            print(f"{prefix} ❌ Resposta inválida")
            return (prompt, None)

    except requests.exceptions.RequestException as e:
        print(f"{prefix} ❌ Erro na requisição: {e}")
        return (prompt, None)
    except Exception as e:
        print(f"{prefix} ❌ Erro inesperado: {e}")
        return (prompt, None)


def save_image(base64_data, prompt, index, output_dir=None):
    """
    Salva imagem base64 em arquivo PNG

    Args:
        base64_data: String base64 da imagem
        prompt: Prompt usado (para nome do arquivo)
        index: Número da imagem
        output_dir: Diretório de saída (padrão: ~/Downloads)

    Returns:
        output_path: Caminho do arquivo salvo
    """
    if output_dir is None:
        output_dir = str(Path.home() / "Downloads")

    # Cria diretório se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Cria nome descritivo do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Limpa o prompt para nome de arquivo
    clean_prompt = prompt[:40].replace(" ", "_").replace("/", "_")
    clean_prompt = "".join(c for c in clean_prompt if c.isalnum() or c in "_-")

    filename = f"{index:02d}_nanobanana_{clean_prompt}_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)

    # Decodifica e salva
    try:
        image_bytes = base64.b64decode(base64_data)

        with open(output_path, "wb") as f:
            f.write(image_bytes)

        return output_path

    except Exception as e:
        print(f"❌ Erro ao salvar imagem {index}: {e}")
        return None


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Gerar múltiplas imagens com Nano Banana via OpenRouter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python3 batch_openrouter_nanobanana.py "uniforme indústria" "uniforme saúde" "uniforme segurança"
    python3 batch_openrouter_nanobanana.py --ratio 16:9 "banner1" "banner2" "banner3"
    python3 batch_openrouter_nanobanana.py --output ./results "prompt1" "prompt2"

Configuração:
    export OPENROUTER_API_KEY='sk-or-v1-...'

Características:
    - Processa múltiplas imagens em paralelo
    - Aspect ratio configurável
    - Nomes de arquivo numerados e descritivos
    - Salva automaticamente em ~/Downloads (ou pasta especificada)
        """
    )

    parser.add_argument('prompts', nargs='+', help='Lista de prompts para gerar imagens')
    parser.add_argument('--ratio', '-r', default='2:3',
                        help='Aspect ratio para todas as imagens (padrão: 2:3 portrait)')
    parser.add_argument('--output', '-o',
                        help='Diretório de saída (padrão: ~/Downloads)')
    parser.add_argument('--workers', '-w', type=int, default=3,
                        help='Número de workers paralelos (padrão: 3)')

    args = parser.parse_args()

    print("🍌 Batch Nano Banana via OpenRouter")
    print("=" * 60)
    print(f"📊 Total de imagens: {len(args.prompts)}")
    print(f"📐 Aspect ratio: {args.ratio}")
    print(f"⚙️  Workers paralelos: {args.workers}")
    print()

    # Gera as imagens em paralelo
    results = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submete todas as tarefas
        futures = {
            executor.submit(generate_image, prompt, args.ratio, i+1): (i+1, prompt)
            for i, prompt in enumerate(args.prompts)
        }

        # Coleta os resultados conforme vão completando
        for future in as_completed(futures):
            index, original_prompt = futures[future]
            try:
                prompt, base64_data = future.result()
                results.append((index, prompt, base64_data))
            except Exception as e:
                print(f"❌ Erro ao processar imagem {index}: {e}")
                results.append((index, original_prompt, None))

    # Ordena resultados por índice
    results.sort(key=lambda x: x[0])

    # Salva as imagens
    print("\n" + "=" * 60)
    print("💾 Salvando imagens...")
    print()

    saved_count = 0
    failed_count = 0

    for index, prompt, base64_data in results:
        if base64_data:
            output_path = save_image(base64_data, prompt, index, args.output)
            if output_path:
                print(f"✅ [{index:02d}] {os.path.basename(output_path)}")
                saved_count += 1
            else:
                print(f"❌ [{index:02d}] Falha ao salvar")
                failed_count += 1
        else:
            print(f"❌ [{index:02d}] Não gerada")
            failed_count += 1

    # Resumo final
    print("\n" + "=" * 60)
    print(f"✅ Salvas: {saved_count}")
    print(f"❌ Falhas: {failed_count}")
    print(f"📂 Localização: {args.output or '~/Downloads'}")

    if saved_count > 0:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
