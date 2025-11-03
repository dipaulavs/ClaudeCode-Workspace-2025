#!/usr/bin/env python3
"""
Template: Batch Edit para Thumbnails YouTube - 4 Variações

Gera 4 thumbnails com PROMPTS DIFERENTES testando estilos variados.
Ideal para encontrar o padrão visual ideal.

Uso:
    python3 scripts/image-generation/batch_edit_thumbnails.py --url URL
"""

import sys
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from edit_image_nanobanana import edit_image, check_status, download_image, upload_to_nextcloud
import os


def create_edit_task(prompt, image_url, output_format, image_size, task_number, variant_name):
    """Cria uma tarefa de edição"""
    print(f"   [{task_number}/4] {variant_name}...")

    try:
        task_id = edit_image(
            prompt=prompt,
            image_url=image_url,
            output_format=output_format,
            image_size=image_size,
            num_outputs=2  # 2 variações por prompt
        )

        if task_id:
            return {
                "task_id": task_id,
                "task_number": task_number,
                "variant_name": variant_name,
                "status": "created"
            }
        return None

    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None


def monitor_task(task_info):
    """Monitora uma tarefa até conclusão e baixa resultado"""
    task_id = task_info["task_id"]
    task_num = task_info["task_number"]
    variant_name = task_info["variant_name"]

    # Aguarda conclusão (checa a cada 2s)
    max_attempts = 90  # 3 minutos
    attempt = 0

    while attempt < max_attempts:
        status_info = check_status(task_id)
        status = status_info.get("status")

        if status == "success":
            image_urls = status_info.get("image_urls", [])
            if image_urls:
                print(f"   ✅ [{task_num}/4] {variant_name} ({len(image_urls)} imagens)")
                # Baixa TODAS as imagens
                filepaths = []
                for url in image_urls:
                    filepath = download_image(url)
                    filepaths.append(filepath)
                return {
                    "success": True,
                    "task_number": task_num,
                    "variant_name": variant_name,
                    "filepaths": filepaths
                }
            return {"success": False, "task_number": task_num, "variant_name": variant_name, "error": "Sem URLs"}

        elif status == "failed":
            return {"success": False, "task_number": task_num, "variant_name": variant_name, "error": "Falha"}

        time.sleep(2)
        attempt += 1

    return {"success": False, "task_number": task_num, "variant_name": variant_name, "error": "Timeout"}


def main():
    parser = argparse.ArgumentParser(
        description='Batch Edit para Thumbnails YouTube - 4 Variações Diferentes',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('image', nargs='?',
                        help='Caminho da imagem local (opcional se usar --url)')
    parser.add_argument('--url', '-u',
                        help='URL da imagem (alternativa ao caminho local)')
    parser.add_argument('--headline', default='DE R$60/MÊS → R$0',
                        help='Headline principal em PT-BR. Padrão: DE R$60/MÊS → R$0')
    parser.add_argument('--format', '-f', default='PNG', choices=['PNG', 'JPEG'],
                        help='Formato. Padrão: PNG')
    parser.add_argument('--size', '-s', default='16:9',
                        help='Proporção. Padrão: 16:9')

    args = parser.parse_args()

    if not args.url and not args.image:
        parser.error("É necessário fornecer --url ou caminho da imagem")

    if args.url and args.image:
        parser.error("Forneça apenas --url OU caminho, não ambos")

    print("🎬 Batch Thumbnails YouTube - 4 Estilos Diferentes")
    print("=" * 60)
    print(f"📐 {args.format} | 16:9")
    print(f"📝 Headline: {args.headline}")
    print("=" * 60)

    try:
        # URL da imagem
        if args.url:
            image_url = args.url
            print("🖼️  Usando URL fornecida")
        else:
            if not os.path.exists(args.image):
                print(f"❌ Arquivo não encontrado: {args.image}")
                sys.exit(1)
            print("📤 Upload da imagem...")
            image_url = upload_to_nextcloud(args.image, expire_days=1)

        # 4 PROMPTS DIFERENTES (variações de estilo)
        prompts = [
            # Variação 1: Expressão séria/confiante
            {
                "name": "Expressão Séria",
                "prompt": f"""YouTube thumbnail 16:9 CINEMATIC DARK style:

PERSON: Keep face similar but adjust to serious/confident expression (subtle change), dramatic split lighting (warm orange left, cool blue right)

BACKGROUND: Pure black, high contrast shadows

TYPOGRAPHY PT-BR:
- Top: '{args.headline}' (white → neon green)
- Bottom: 'SEM PERDER ARQUIVOS' (white)

ELEMENTS: Faded cloud icons (iCloud, Dropbox, Drive) with red X marks

STYLE: Cinematic YouTube thumbnail, professional, dark aesthetic, high contrast"""
            },

            # Variação 2: Expressão surpresa/choque
            {
                "name": "Expressão Chocada",
                "prompt": f"""YouTube thumbnail 16:9 CINEMATIC DARK style:

PERSON: Keep face similar but adjust to shocked/surprised expression with wide eyes (subtle change), dramatic split lighting (warm orange left, cool blue right)

BACKGROUND: Pure black, high contrast shadows

TYPOGRAPHY PT-BR:
- Top: '{args.headline}' (white → neon green #00FF00 huge)
- Bottom: 'SEM PERDER ARQUIVOS' (white)

ELEMENTS: Faded cloud icons with red X marks background

STYLE: Cinematic viral YouTube thumbnail, dramatic lighting, professional quality"""
            },

            # Variação 3: Expressão pensativa/reflexiva
            {
                "name": "Expressão Pensativa",
                "prompt": f"""YouTube thumbnail 16:9 CINEMATIC DARK style:

PERSON: Keep face similar but adjust to thoughtful/reflective expression (subtle change), dramatic split lighting (warm orange left, cool blue right)

BACKGROUND: Pure black, strong shadows

TYPOGRAPHY PT-BR:
- Top: '{args.headline}' (bold white → bright neon green)
- Bottom: 'SEM PERDER ARQUIVOS' (white smaller)

ELEMENTS: Cloud storage icons faded background with red X

STYLE: Cinematic YouTube thumbnail, professional dark aesthetic, high contrast"""
            },

            # Variação 4: Expressão determinada/focada
            {
                "name": "Expressão Determinada",
                "prompt": f"""YouTube thumbnail 16:9 CINEMATIC DARK style:

PERSON: Keep face similar but adjust to determined/focused expression (subtle change), dramatic split lighting (warm orange left, cool blue right)

BACKGROUND: Pure black, cinematic shadows

TYPOGRAPHY PT-BR:
- Top: '{args.headline}' (white bold → neon green #00FF00)
- Bottom: 'SEM PERDER ARQUIVOS' (white)

ELEMENTS: Faded cloud icons (iCloud, Dropbox, Drive) with red X marks

STYLE: Cinematic YouTube viral thumbnail, dramatic lighting, professional quality, dark aesthetic"""
            }
        ]

        # FASE 1: Criar 4 tarefas
        print(f"\n🚀 Fase 1: Criando 4 variações...")

        tasks = []
        for i, variant in enumerate(prompts, 1):
            task = create_edit_task(
                prompt=variant["prompt"],
                image_url=image_url,
                output_format=args.format,
                image_size=args.size,
                task_number=i,
                variant_name=variant["name"]
            )
            if task:
                tasks.append(task)

        if not tasks:
            print("❌ Falha ao criar tarefas")
            sys.exit(1)

        print(f"\n✅ {len(tasks)} tarefas criadas!")

        # FASE 2: Monitorar em paralelo
        print(f"\n⏳ Fase 2: Processando em paralelo...")

        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_task = {executor.submit(monitor_task, task): task for task in tasks}

            for future in as_completed(future_to_task):
                result = future.result()
                results.append(result)

                if result["success"]:
                    for filepath in result['filepaths']:
                        print(f"      💾 {filepath}")

        # Resumo
        success_count = sum(1 for r in results if r["success"])

        print(f"\n✅ Geradas: {success_count}/4 thumbnails")

        if success_count < 4:
            print(f"⚠️  Falhas: {4 - success_count}")
            for result in results:
                if not result["success"]:
                    print(f"   - {result['variant_name']}: {result.get('error', 'Erro')}")

        print(f"\n✅ Processo concluído!")
        print(f"📂 ~/Downloads")

        return 0

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
