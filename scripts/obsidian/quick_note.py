#!/usr/bin/env python3
"""
Script: Quick Note - Captura rápida de notas no Obsidian

Uso:
    python3 scripts/obsidian/quick_note.py "Minha nota rápida"
    python3 scripts/obsidian/quick_note.py "Minha nota" --folder ideas
"""

import argparse
from obsidian_client import ObsidianClient, FOLDERS
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Criar nota rápida no Obsidian")
    parser.add_argument("content", help="Conteúdo da nota")
    parser.add_argument(
        "--folder",
        choices=list(FOLDERS.keys()),
        default="inbox",
        help="Pasta destino (padrão: inbox)"
    )
    parser.add_argument("--title", help="Título customizado (opcional)")

    args = parser.parse_args()

    try:
        client = ObsidianClient()

        # Gerar nome do arquivo
        if args.title:
            filename = args.title
        else:
            filename = f"Quick Note - {datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # Criar conteúdo
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = f"""# {args.title or 'Quick Note'}

{args.content}

---
Criado: {timestamp}
Via: quick_note.py
"""

        # Criar nota
        result = client.create_note(filename, content, folder=args.folder)

        print(f"✅ Nota criada com sucesso!")
        print(f"📍 Localização: {FOLDERS[args.folder]}/{filename}.md")

        # Log na daily note
        if args.folder != "daily":
            try:
                client.log_to_daily(
                    f"Criada nota rápida: [[{filename}]] em {FOLDERS[args.folder]}",
                    section="🤖 Automações Executadas"
                )
            except:
                pass  # Silenciar erro se daily note não existir

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
