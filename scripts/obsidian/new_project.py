#!/usr/bin/env python3
"""
Script: New Project - Cria estrutura completa de projeto no Obsidian

Uso:
    python3 scripts/obsidian/new_project.py "Nome do Projeto"
    python3 scripts/obsidian/new_project.py "App Fitness" --desc "App de treinos"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

from obsidian_config import FOLDERS, DISPLAY_DATE_FORMAT, ensure_folder_exists


def create_project(name: str, desc: str = "", goal: str = "") -> dict:
    """
    Cria estrutura completa de projeto no Obsidian

    Args:
        name: Nome do projeto
        desc: Descrição do projeto
        goal: Objetivo/Meta do projeto

    Returns:
        dict: Informações sobre os arquivos criados
    """
    # Garantir que a pasta de projetos existe
    projects_folder = ensure_folder_exists("projects")

    # Criar pasta do projeto
    project_folder = projects_folder / name
    project_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(f"{DISPLAY_DATE_FORMAT} %H:%M")

    # 1. README do Projeto
    readme_content = f"""# {name}

## 📋 Visão Geral

{desc or "_Adicione descrição do projeto_"}

## 🎯 Objetivo

{goal or "_Defina o objetivo/meta do projeto_"}

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
    tasks_content = f"""# Tarefas - {name}

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
    resources_content = f"""# Recursos - {name}

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

    # Escrever arquivos
    readme_path = project_folder / "README.md"
    tasks_path = project_folder / "Tarefas.md"
    resources_path = project_folder / "Recursos.md"

    readme_path.write_text(readme_content, encoding='utf-8')
    tasks_path.write_text(tasks_content, encoding='utf-8')
    resources_path.write_text(resources_content, encoding='utf-8')

    return {
        "name": name,
        "folder": project_folder,
        "files": ["README.md", "Tarefas.md", "Recursos.md"]
    }


def log_to_daily(message: str, section: str = "🎯 Projetos"):
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
    parser = argparse.ArgumentParser(description="Criar novo projeto no Obsidian")
    parser.add_argument("name", help="Nome do projeto")
    parser.add_argument("--desc", "--description", help="Descrição do projeto", default="")
    parser.add_argument("--goal", help="Objetivo/Meta do projeto", default="")

    args = parser.parse_args()

    try:
        # Criar projeto
        result = create_project(args.name, desc=args.desc, goal=args.goal)

        print(f"✅ Projeto criado com sucesso!")
        print(f"📂 Nome: {result['name']}")
        print(f"📍 Localização: {result['folder'].relative_to(Path.home())}")
        print(f"\n📄 Arquivos criados:")
        for file in result['files']:
            print(f"  - {file}")

        # Log na daily note
        log_to_daily(f"📂 Novo projeto criado: [[{args.name}/README|{args.name}]]")

    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
