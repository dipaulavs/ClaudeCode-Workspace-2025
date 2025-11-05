#!/usr/bin/env python3
"""
Script: Capture Idea - Captura de ideias estruturadas no Obsidian

Uso:
    python3 scripts/obsidian/capture_idea.py "Título da Ideia"
    python3 scripts/obsidian/capture_idea.py "App de Fitness" --desc "App para treinos" --tags negocio,app
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

from obsidian_config import FOLDERS, DISPLAY_DATE_FORMAT, ensure_folder_exists


def capture_idea(title: str, desc: str = "", tags: str = "", context: str = "") -> Path:
    """
    Captura uma ideia estruturada no Obsidian

    Args:
        title: Título da ideia
        desc: Descrição da ideia
        tags: Tags separadas por vírgula
        context: Contexto adicional

    Returns:
        Path: Caminho do arquivo criado
    """
    # Garantir que a pasta existe
    ideas_folder = ensure_folder_exists("ideas")

    # Processar tags
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else []
    tags_list.insert(0, "ideia")  # Sempre adicionar tag #ideia
    tags_str = " ".join([f"#{tag}" for tag in tags_list])

    # Criar conteúdo
    timestamp = datetime.now().strftime(f"{DISPLAY_DATE_FORMAT} %H:%M")

    content = f"""# {title}

## 💡 Descrição

{desc or "_Adicione descrição aqui_"}

## 🎯 Contexto

{context or "_Adicione contexto aqui_"}

## ✨ Próximos Passos

- [ ] Pesquisar viabilidade
- [ ] Detalhar funcionalidades
- [ ] Criar protótipo/MVP

## 🔗 Links Relacionados

-

## 📊 Status

**Status:** 🌱 Semente (não validada)

---
Tags: {tags_str}
Criado: {timestamp}
Via: capture_idea.py
"""

    # Escrever arquivo
    filename = f"{title}.md"
    filepath = ideas_folder / filename
    filepath.write_text(content, encoding='utf-8')

    return filepath


def log_to_daily(message: str, section: str = "💡 Ideias"):
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

        # Se daily note não existe, não fazer nada
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
    parser = argparse.ArgumentParser(description="Capturar ideia estruturada no Obsidian")
    parser.add_argument("title", help="Título da ideia")
    parser.add_argument("--desc", "--description", help="Descrição da ideia", default="")
    parser.add_argument("--tags", help="Tags separadas por vírgula (ex: negocio,app)", default="")
    parser.add_argument("--context", help="Contexto adicional", default="")

    args = parser.parse_args()

    try:
        # Capturar ideia
        filepath = capture_idea(args.title, desc=args.desc, tags=args.tags, context=args.context)

        # Processar tags para exibição
        tags_list = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
        tags_list.insert(0, "ideia")
        tags_str = " ".join([f"#{tag}" for tag in tags_list])

        print(f"✅ Ideia capturada com sucesso!")
        print(f"💡 Título: {args.title}")
        print(f"📍 Localização: {filepath.relative_to(Path.home())}")
        print(f"🏷️  Tags: {tags_str}")

        # Log na daily note
        log_to_daily(f"💡 Nova ideia: [[{args.title}]]")

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
