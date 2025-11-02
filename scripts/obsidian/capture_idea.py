#!/usr/bin/env python3
"""
Script: Capture Idea - Captura de ideias estruturadas no Obsidian

Uso:
    python3 scripts/obsidian/capture_idea.py "Título da Ideia"
    python3 scripts/obsidian/capture_idea.py "App de Fitness" --desc "App para treinos" --tags negocio,app
"""

import argparse
from obsidian_client import ObsidianClient, FOLDERS
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Capturar ideia estruturada no Obsidian")
    parser.add_argument("title", help="Título da ideia")
    parser.add_argument("--desc", "--description", help="Descrição da ideia", default="")
    parser.add_argument("--tags", help="Tags separadas por vírgula (ex: negocio,app)", default="")
    parser.add_argument("--context", help="Contexto adicional", default="")

    args = parser.parse_args()

    try:
        client = ObsidianClient()

        # Processar tags
        tags_list = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
        tags_list.insert(0, "ideia")  # Sempre adicionar tag #ideia
        tags_str = " ".join([f"#{tag}" for tag in tags_list])

        # Criar conteúdo
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        content = f"""# {args.title}

## 💡 Descrição

{args.desc or "_Adicione descrição aqui_"}

## 🎯 Contexto

{args.context or "_Adicione contexto aqui_"}

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

        # Criar nota
        result = client.create_note(args.title, content, folder="ideas")

        print(f"✅ Ideia capturada com sucesso!")
        print(f"💡 Título: {args.title}")
        print(f"📍 Localização: {FOLDERS['ideas']}/{args.title}.md")
        print(f"🏷️  Tags: {tags_str}")

        # Log na daily note
        try:
            client.log_to_daily(
                f"💡 Nova ideia: [[{args.title}]]",
                section="💡 Ideias"
            )
        except:
            pass

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
