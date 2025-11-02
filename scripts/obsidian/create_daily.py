#!/usr/bin/env python3
"""
Script: Create Daily Note - Cria daily note no Obsidian

Uso:
    python3 scripts/obsidian/create_daily.py           # Hoje
    python3 scripts/obsidian/create_daily.py --date 2025-11-01  # Data específica
"""

import argparse
from obsidian_client import ObsidianClient
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Criar daily note no Obsidian")
    parser.add_argument(
        "--date",
        help="Data no formato YYYY-MM-DD (padrão: hoje)",
        default=None
    )

    args = parser.parse_args()

    try:
        client = ObsidianClient()

        # Processar data
        if args.date:
            date = datetime.strptime(args.date, "%Y-%m-%d")
        else:
            date = datetime.now()

        # Criar daily note
        result = client.create_daily_note(date)

        date_str = date.strftime("%Y-%m-%d")
        print(f"✅ Daily note criada com sucesso!")
        print(f"📅 Data: {date_str}")
        print(f"📍 Localização: {client.get_today_daily_note()}")

    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"ℹ️  Daily note de {date_str} já existe!")
            print(f"📍 Localização: {client.get_today_daily_note()}")
            return 0
        else:
            print(f"❌ Erro: {e}")
            return 1

    return 0


if __name__ == "__main__":
    exit(main())
