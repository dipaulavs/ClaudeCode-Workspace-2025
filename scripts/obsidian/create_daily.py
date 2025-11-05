#!/usr/bin/env python3
"""
Script: Create Daily Note - Cria daily note no Obsidian

Uso:
    python3 scripts/obsidian/create_daily.py           # Hoje
    python3 scripts/obsidian/create_daily.py --date 2025-11-01  # Data específica
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

from obsidian_config import DAILY_NOTE_FORMAT, DISPLAY_DATE_FORMAT, ensure_folder_exists


def create_daily_note(date: datetime = None) -> Path:
    """
    Cria daily note usando acesso direto ao filesystem

    Args:
        date: Data da daily note (None = hoje)

    Returns:
        Path: Caminho do arquivo criado
    """
    if date is None:
        date = datetime.now()

    # Garantir que a pasta existe
    daily_folder = ensure_folder_exists("daily")

    # Gerar nomes
    date_str = date.strftime(DAILY_NOTE_FORMAT)
    date_display = date.strftime(DISPLAY_DATE_FORMAT)
    weekday = date.strftime("%A")

    # Traduzir dia da semana
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

    # Criar conteúdo
    content = f"""# {date_display} - {weekday_pt}

## ✅ Tarefas
- [ ]

## 📝 Notas do Dia


## 🎯 Projetos
-

## 💡 Ideias


## 🤖 Automações Executadas


## 📊 Métricas


## 🧠 Reflexões


---
Tags: #daily-note
Criado: {datetime.now().strftime(f"{DISPLAY_DATE_FORMAT} %H:%M")}
"""

    # Escrever arquivo
    filepath = daily_folder / filename

    # Verificar se já existe
    if filepath.exists():
        raise FileExistsError(f"Daily note já existe: {filepath}")

    filepath.write_text(content, encoding='utf-8')

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Criar daily note no Obsidian")
    parser.add_argument(
        "--date",
        help="Data no formato YYYY-MM-DD (padrão: hoje)",
        default=None
    )

    args = parser.parse_args()

    try:
        # Processar data
        if args.date:
            date = datetime.strptime(args.date, "%Y-%m-%d")
        else:
            date = datetime.now()

        # Criar daily note
        filepath = create_daily_note(date)

        date_str = date.strftime("%Y-%m-%d")
        print(f"✅ Daily note criada com sucesso!")
        print(f"📅 Data: {date_str}")
        print(f"📍 Localização: {filepath.relative_to(Path.home())}")

    except FileExistsError as e:
        date_str = date.strftime("%Y-%m-%d")
        print(f"ℹ️  Daily note de {date_str} já existe!")
        # Encontrar o arquivo
        daily_folder = ensure_folder_exists("daily")
        weekday = date.strftime("%A")
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
        filename = f"{date.strftime(DAILY_NOTE_FORMAT)} - {weekday_pt}.md"
        filepath = daily_folder / filename
        print(f"📍 Localização: {filepath.relative_to(Path.home())}")
        return 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
