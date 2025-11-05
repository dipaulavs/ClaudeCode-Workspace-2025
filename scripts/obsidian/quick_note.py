#!/usr/bin/env python3
"""
Script: Quick Note - Captura rápida de notas no Obsidian

Uso:
    python3 scripts/obsidian/quick_note.py "Minha nota rápida"
    python3 scripts/obsidian/quick_note.py "Minha nota" --folder ideas
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

from obsidian_config import FOLDERS, get_folder_path, ensure_folder_exists, DISPLAY_DATE_FORMAT


def create_quick_note(content: str, folder: str = "inbox", title: str = None) -> Path:
    """
    Cria uma nota rápida no Obsidian usando acesso direto ao filesystem

    Args:
        content: Conteúdo da nota
        folder: Pasta destino (chave do FOLDERS)
        title: Título customizado (opcional)

    Returns:
        Path: Caminho do arquivo criado
    """
    # Garantir que a pasta existe
    folder_path = ensure_folder_exists(folder)

    # Gerar nome do arquivo
    if title:
        filename = f"{title}.md"
    else:
        filename = f"Quick Note - {datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

    # Criar conteúdo
    timestamp = datetime.now().strftime(f"{DISPLAY_DATE_FORMAT} %H:%M")
    note_content = f"""# {title or 'Quick Note'}

{content}

---
Criado: {timestamp}
Via: quick_note.py
"""

    # Escrever arquivo
    filepath = folder_path / filename
    filepath.write_text(note_content, encoding='utf-8')

    return filepath


def log_to_daily(message: str, section: str = "🤖 Automações Executadas"):
    """
    Adiciona entrada na daily note de hoje

    Args:
        message: Mensagem a adicionar
        section: Seção onde adicionar
    """
    try:
        # Obter daily note de hoje
        daily_folder = ensure_folder_exists("daily")

        # Nome do arquivo da daily note
        date_str = datetime.now().strftime("%Y-%m-%d")
        weekday = datetime.now().strftime("%A")

        weekdays_pt = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        weekday_pt = weekdays_pt.get(weekday, weekday)

        filename = f"{date_str} - {weekday_pt}.md"
        daily_path = daily_folder / filename

        # Se daily note não existe, não fazer nada (não criar automaticamente)
        if not daily_path.exists():
            return

        # Adicionar entrada
        timestamp = datetime.now().strftime("%H:%M")
        entry = f"\n- **{timestamp}** - {message}"

        # Ler conteúdo existente
        content = daily_path.read_text(encoding='utf-8')

        # Adicionar ao final
        content += entry

        # Salvar
        daily_path.write_text(content, encoding='utf-8')

    except Exception:
        pass  # Silenciar erros no log


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
        # Criar nota
        filepath = create_quick_note(args.content, folder=args.folder, title=args.title)

        print(f"✅ Nota criada com sucesso!")
        print(f"📍 Localização: {filepath.relative_to(Path.home())}")

        # Log na daily note
        if args.folder != "daily":
            log_to_daily(
                f"Criada nota rápida: [[{filepath.stem}]] em {FOLDERS[args.folder]}"
            )

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
