#!/usr/bin/env python3
"""
Template: Edição em Lote de Imagens com Nano Banana Edit

Gera múltiplas VARIAÇÕES da mesma edição em paralelo.
Cria 4 tarefas separadas com o mesmo prompt para obter variações criativas.

Uso:
    python3 scripts/image-generation/batch_edit_nanobanana.py --url URL "prompt de edição" --variations 4
    python3 scripts/image-generation/batch_edit_nanobanana.py foto.jpg "adicionar texto" --variations 4 --size 16:9
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


def create_edit_task(prompt, image_url, output_format, image_size, task_number):
    """Cria uma tarefa de edição (não aguarda conclusão)"""
    print(f"   [{task_number}/4] Criando tarefa...")

    try:
        task_id = edit_image(
            prompt=prompt,
            image_url=image_url,
            output_format=output_format,
            image_size=image_size,
            num_outputs=1  # 1 por tarefa, mas criamos 4 tarefas
        )

        if task_id:
            return {
                "task_id": task_id,
                "task_number": task_number,
                "status": "created"
            }
        return None

    except Exception as e:
        print(f"   ❌ Erro na tarefa {task_number}: {e}")
        return None


def monitor_task(task_info):
    """Monitora uma tarefa até conclusão e baixa resultado"""
    task_id = task_info["task_id"]
    task_num = task_info["task_number"]

    # Aguarda conclusão
    max_attempts = 120  # 4 minutos total (2s x 120)
    attempt = 0

    while attempt < max_attempts:
        status_info = check_status(task_id)
        status = status_info.get("status")

        if status == "success":
            image_urls = status_info.get("image_urls", [])
            if image_urls:
                print(f"   ✅ [{task_num}/4] Variação pronta!")
                # Baixa a imagem
                filepath = download_image(image_urls[0])
                return {
                    "success": True,
                    "task_number": task_num,
                    "filepath": filepath
                }
            return {"success": False, "task_number": task_num, "error": "Sem URLs"}

        elif status == "failed":
            return {"success": False, "task_number": task_num, "error": "Falha na geração"}

        # Continua aguardando
        time.sleep(2)
        attempt += 1

    return {"success": False, "task_number": task_num, "error": "Timeout"}


def main():
    """Função principal"""

    parser = argparse.ArgumentParser(
        description='Edição em lote de imagem com Nano Banana Edit (4 variações)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    # 4 variações de thumbnail 16:9
    python3 scripts/image-generation/batch_edit_nanobanana.py \\
        --url "https://example.com/foto.jpg" \\
        "Create YouTube thumbnail with text 'TÍTULO'" \\
        --size 16:9 --variations 4

    # 4 variações de edição local
    python3 scripts/image-generation/batch_edit_nanobanana.py \\
        minha_foto.png \\
        "add dramatic lighting" \\
        --variations 4

Características:
    - Gera 4 variações criativas do mesmo prompt
    - Processamento paralelo (todas ao mesmo tempo)
    - Salvamento automático em ~/Downloads
    - Nano Banana Edit (Gemini 2.5 Flash)
        """
    )

    parser.add_argument('image', nargs='?',
                        help='Caminho da imagem local (opcional se usar --url)')
    parser.add_argument('prompt',
                        help='Descrição da edição a ser aplicada')
    parser.add_argument('--url', '-u',
                        help='URL da imagem (alternativa ao caminho local)')
    parser.add_argument('--format', '-f', default='PNG', choices=['PNG', 'JPEG'],
                        help='Formato da imagem de saída. Padrão: PNG')
    parser.add_argument('--size', '-s', default='auto',
                        choices=['1:1', '9:16', '16:9', '3:4', '4:3', '3:2', '2:3', '5:4', '4:5', '21:9', 'auto'],
                        help='Proporção da imagem de saída. Padrão: auto')
    parser.add_argument('--variations', '-v', type=int, default=4, choices=[1, 2, 3, 4],
                        help='Número de variações a gerar (1-4). Padrão: 4')

    args = parser.parse_args()

    # Validação
    if not args.url and not args.image:
        parser.error("É necessário fornecer um caminho de imagem ou --url")

    if args.url and args.image:
        parser.error("Forneça apenas um caminho de imagem OU --url, não ambos")

    print("✏️  Nano Banana Batch Edit - Gerador de Variações")
    print("=" * 60)
    print(f"🎨 Gerando {args.variations} variações criativas")
    print(f"📐 Formato: {args.format} | Proporção: {args.size}")
    print("=" * 60)

    try:
        # Determina a URL da imagem
        if args.url:
            image_url = args.url
            print(f"🖼️  Usando URL fornecida")
        else:
            # Upload da imagem
            if not os.path.exists(args.image):
                print(f"❌ Erro: Arquivo não encontrado: {args.image}")
                sys.exit(1)

            print(f"📤 Fazendo upload da imagem...")
            image_url = upload_to_nextcloud(args.image, expire_days=1)

        # FASE 1: Criar todas as tarefas de uma vez
        print(f"\n🚀 Fase 1: Criando {args.variations} tarefas...")

        tasks = []
        for i in range(1, args.variations + 1):
            task = create_edit_task(
                prompt=args.prompt,
                image_url=image_url,
                output_format=args.format,
                image_size=args.size,
                task_number=i
            )
            if task:
                tasks.append(task)

        if not tasks:
            print("❌ Falha ao criar tarefas")
            sys.exit(1)

        print(f"\n✅ {len(tasks)} tarefas criadas com sucesso!")

        # FASE 2: Monitorar todas em paralelo
        print(f"\n⏳ Fase 2: Monitorando e baixando ({len(tasks)} em paralelo)...")

        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submete todas as tarefas para monitoramento
            future_to_task = {executor.submit(monitor_task, task): task for task in tasks}

            # Processa conforme ficam prontas
            for future in as_completed(future_to_task):
                result = future.result()
                results.append(result)

                if result["success"]:
                    print(f"      💾 {result['filepath']}")

        # Resumo final
        success_count = sum(1 for r in results if r["success"])

        print(f"\n✅ Geradas: {success_count}/{args.variations} variações")

        if success_count < args.variations:
            print(f"⚠️  Falhas: {args.variations - success_count}")
            for result in results:
                if not result["success"]:
                    print(f"   - Variação {result['task_number']}: {result.get('error', 'Erro desconhecido')}")

        print(f"\n✅ Processo concluído!")
        print(f"📂 Verifique suas imagens em: ~/Downloads")

        return 0

    except Exception as e:
        print(f"❌ Erro ao editar imagens em lote: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
