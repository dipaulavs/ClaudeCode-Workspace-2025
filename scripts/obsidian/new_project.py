#!/usr/bin/env python3
"""
Script: New Project - Cria estrutura completa de projeto no Obsidian

Uso:
    python3 scripts/obsidian/new_project.py "Nome do Projeto"
    python3 scripts/obsidian/new_project.py "App Fitness" --desc "App de treinos"
"""

import argparse
from obsidian_client import ObsidianClient, FOLDERS, DISPLAY_DATE_FORMAT
from datetime import datetime
import os


def main():
    parser = argparse.ArgumentParser(description="Criar novo projeto no Obsidian")
    parser.add_argument("name", help="Nome do projeto")
    parser.add_argument("--desc", "--description", help="Descrição do projeto", default="")
    parser.add_argument("--goal", help="Objetivo/Meta do projeto", default="")

    args = parser.parse_args()

    try:
        client = ObsidianClient()

        # Criar pasta do projeto
        project_folder = f"{FOLDERS['projects']}/{args.name}"

        timestamp = datetime.now().strftime(f"{DISPLAY_DATE_FORMAT} %H:%M")

        # 1. README do Projeto
        readme_content = f"""# {args.name}

## 📋 Visão Geral

{args.desc or "_Adicione descrição do projeto_"}

## 🎯 Objetivo

{args.goal or "_Defina o objetivo/meta do projeto_"}

## 📊 Status

**Status Atual:** 🟡 Em Planejamento

**Última Atualização:** {timestamp}

## 📂 Estrutura

- [[Tarefas]] - Lista de tarefas e to-dos
- [[Recursos]] - Links, arquivos, referências
- [[Notas de Reunião]] - Pasta com notas de reuniões

## 🔗 Links Relacionados

-

## 📝 Notas


---
Criado: {timestamp}
Via: new_project.py
"""

        # 2. Tarefas
        tasks_content = f"""# Tarefas - {args.name}

## 🔥 Prioridade Alta

- [ ]

## 📌 Tarefas Pendentes

- [ ]

## ✅ Concluídas

-

---
Atualizado: {timestamp}
"""

        # 3. Recursos
        resources_content = f"""# Recursos - {args.name}

## 🔗 Links Úteis

-

## 📄 Documentos

-

## 🎨 Design/Assets

-

## 💻 Código/Repos

-

## 📚 Referências

-

---
Atualizado: {timestamp}
"""

        # Criar notas
        client.create_note(f"{args.name}/README", readme_content, folder="projects")
        client.create_note(f"{args.name}/Tarefas", tasks_content, folder="projects")
        client.create_note(f"{args.name}/Recursos", resources_content, folder="projects")

        print(f"✅ Projeto criado com sucesso!")
        print(f"📂 Nome: {args.name}")
        print(f"📍 Localização: {FOLDERS['projects']}/{args.name}/")
        print(f"\n📄 Arquivos criados:")
        print(f"  - README.md")
        print(f"  - Tarefas.md")
        print(f"  - Recursos.md")

        # Log na daily note
        try:
            client.log_to_daily(
                f"📂 Novo projeto criado: [[{args.name}/README|{args.name}]]",
                section="🎯 Projetos"
            )
        except:
            pass

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
