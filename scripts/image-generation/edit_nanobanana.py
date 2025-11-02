#!/usr/bin/env python3
"""
Template: Editar Imagem com Nano Banana

Wrapper simplificado para editar imagens usando Nano Banana Edit via Kie.ai API.
Permite fornecer imagem local ou URL e aplicar transformações com IA.

Uso:
    python3 scripts/image-generation/edit_nanobanana.py imagem.jpg "trocar fundo"
    python3 scripts/image-generation/edit_nanobanana.py --url https://exemplo.com/foto.jpg "adicionar flores"
    python3 scripts/image-generation/edit_nanobanana.py foto.png "mudar cor" --size 1:1
"""

import sys
import argparse
from pathlib import Path

# Adiciona o diretório tools ao path para importar as ferramentas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from edit_image_nanobanana import edit_image, wait_for_completion, download_image, upload_to_nextcloud
import os


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Editar imagem com Nano Banana Edit (Gemini 2.5 Flash)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    # Editar imagem local
    python3 scripts/image-generation/edit_nanobanana.py foto.jpg "remover fundo"

    # Editar com URL
    python3 scripts/image-generation/edit_nanobanana.py --url https://exemplo.com/img.jpg "adicionar chapéu"

    # Editar com formato e proporção específicos
    python3 scripts/image-generation/edit_nanobanana.py imagem.png "mudar cor para azul" --format JPEG --size 16:9

Características:
    - Modelo: Gemini 2.5 Flash (Nano Banana Edit)
    - Suporte a imagens locais ou URLs
    - Múltiplas proporções (1:1, 16:9, 9:16, 4:3, etc)
    - Formatos: PNG ou JPEG
    - Salvamento automático em ~/Downloads
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

    args = parser.parse_args()

    # Validação
    if not args.url and not args.image:
        parser.error("É necessário fornecer um caminho de imagem ou --url")

    if args.url and args.image:
        parser.error("Forneça apenas um caminho de imagem OU --url, não ambos")

    print("✏️  Nano Banana Image Edit (Gemini 2.5 Flash)")
    print("=" * 60)

    try:
        # Determina a URL da imagem
        if args.url:
            image_url = args.url
            print(f"🖼️  Usando URL fornecida")
        else:
            # Verifica se o arquivo existe
            if not os.path.exists(args.image):
                print(f"❌ Erro: Arquivo não encontrado: {args.image}")
                sys.exit(1)

            print(f"📤 Fazendo upload da imagem...")
            image_url = upload_to_nextcloud(args.image, expire_days=1)

        # Edita a imagem
        task_id = edit_image(
            prompt=args.prompt,
            image_url=image_url,
            output_format=args.format,
            image_size=args.size
        )

        if not task_id:
            print("❌ Falha ao criar tarefa de edição")
            sys.exit(1)

        # Aguarda conclusão
        image_urls = wait_for_completion(task_id)

        if not image_urls:
            print("❌ Falha ao editar imagem")
            sys.exit(1)

        # Baixa as imagens editadas
        print(f"\n🖼️  {len(image_urls)} imagem(ns) editada(s)")

        for i, url in enumerate(image_urls, 1):
            print(f"\n📥 Baixando imagem {i}/{len(image_urls)}...")
            download_image(url)

        print("\n✅ Edição concluída com sucesso!")
        print(f"📂 Verifique suas imagens em: ~/Downloads")

        return 0

    except Exception as e:
        print(f"❌ Erro ao editar imagem: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
