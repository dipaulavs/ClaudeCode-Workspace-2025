#!/usr/bin/env python3
"""
Script para gerenciar tarefas no sistema Obsidian

Uso:
    python3 scripts/obsidian/manage_tasks.py create-task "Nome da Tarefa" --projeto "Canal YouTube" --prioridade urgente
    python3 scripts/obsidian/manage_tasks.py update-progress "App ChatLoop9" 75
    python3 scripts/obsidian/manage_tasks.py list-urgent
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import argparse

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

try:
    from obsidian_config import OBSIDIAN_VAULT_PATH, FOLDERS, DISPLAY_DATE_FORMAT
except ImportError:
    print("❌ Erro: obsidian_config.py não encontrado!")
    sys.exit(1)


# Caminhos
VAULT_PATH = Path(OBSIDIAN_VAULT_PATH)
TASKS_PATH = VAULT_PATH / "08 - Tarefas"
TEMPLATES_PATH = VAULT_PATH / "05 - Templates"


def get_priority_emoji(priority: str) -> str:
    """Retorna emoji de prioridade"""
    mapping = {
        'urgente': '🔥 urgente',
        'importante': '⭐ importante',
        'normal': '💡 normal'
    }
    return mapping.get(priority.lower(), '💡 normal')


def get_status_emoji(status: str) -> str:
    """Retorna emoji de status"""
    mapping = {
        'todo': '🔵 todo',
        'ativo': '🟡 ativo',
        'concluido': '✅ concluído',
        'bloqueado': '❌ bloqueado'
    }
    return mapping.get(status.lower(), '🔵 todo')


def create_task(name: str, projeto: str = '', prioridade: str = 'normal', due: str = ''):
    """Cria nova tarefa"""

    # Template da tarefa
    today = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  # ISO 8601 datetime (com T) para Dataview
    priority = get_priority_emoji(prioridade)

    content = f"""---
tipo: tarefa
projeto: {projeto}
area:
status: 🔵 todo
prioridade: {priority}
tags:
  - tarefa
created: {today}
due: {due}
---

# {name}

## 📋 Descrição

[Descreva a tarefa aqui]

## ✅ Critérios de Conclusão

- [ ]

## 🔗 Links Relacionados

-

## 📝 Notas

---

**Status:** `= this.status`
**Prioridade:** `= this.prioridade`
**Criado em:** `= this.created`
**Vencimento:** `= this.due`
"""

    # Salvar arquivo
    filename = name.replace('/', '-') + '.md'  # Mantém espaços para leitura visual mais limpa
    filepath = TASKS_PATH / filename

    filepath.write_text(content, encoding='utf-8')

    print(f"✅ Tarefa criada: {filepath}")
    print(f"   Projeto: {projeto}")
    print(f"   Prioridade: {priority}")
    if due:
        print(f"   Vencimento: {due}")


def update_project_progress(project_name: str, progress: int):
    """Atualiza progresso de um projeto"""

    # Buscar arquivo do projeto
    projects_path = TASKS_PATH / "Projetos"
    project_file = projects_path / f"{project_name}.md"

    if not project_file.exists():
        print(f"❌ Projeto não encontrado: {project_name}")
        print(f"   Caminho: {project_file}")
        return

    # Ler conteúdo
    content = project_file.read_text(encoding='utf-8')

    # Atualizar progress
    lines = content.split('\n')
    updated = False

    for i, line in enumerate(lines):
        if line.startswith('progress:'):
            lines[i] = f'progress: {progress}'
            updated = True
            break

    if updated:
        # Salvar
        project_file.write_text('\n'.join(lines), encoding='utf-8')
        print(f"✅ Progresso atualizado: {project_name} → {progress}%")
    else:
        print(f"⚠️ Campo 'progress' não encontrado no projeto")


def list_urgent_tasks():
    """Lista tarefas urgentes"""

    print("\n🔥 TAREFAS URGENTES\n")

    found = False
    for task_file in TASKS_PATH.rglob("*.md"):
        content = task_file.read_text(encoding='utf-8')

        # Verificar se é urgente e não está concluída
        if 'prioridade: 🔥 urgente' in content and 'status: ✅ concluído' not in content:
            # Extrair nome (primeira linha markdown H1)
            for line in content.split('\n'):
                if line.startswith('# '):
                    name = line.replace('# ', '').strip()
                    print(f"  • {name}")
                    print(f"    📁 {task_file.relative_to(VAULT_PATH)}")
                    found = True
                    break

    if not found:
        print("  Nenhuma tarefa urgente! 🎉")

    print()


def list_active_projects():
    """Lista projetos ativos"""

    print("\n📊 PROJETOS ATIVOS\n")

    projects_path = TASKS_PATH / "Projetos"

    if not projects_path.exists():
        print("  Nenhum projeto encontrado.")
        return

    for project_file in projects_path.glob("*.md"):
        content = project_file.read_text(encoding='utf-8')

        if 'status: 🟡 ativo' in content:
            # Extrair dados
            name = project_file.stem
            progress = '0'

            for line in content.split('\n'):
                if line.startswith('progress:'):
                    progress = line.split(':')[1].strip()
                    break

            print(f"  • {name}")
            print(f"    Progresso: {progress}%")

    print()


def main():
    parser = argparse.ArgumentParser(description='Gerenciar tarefas no Obsidian')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # create-task
    create_parser = subparsers.add_parser('create-task', help='Criar nova tarefa')
    create_parser.add_argument('name', help='Nome da tarefa')
    create_parser.add_argument('--projeto', default='', help='Projeto relacionado')
    create_parser.add_argument('--prioridade', default='normal', choices=['urgente', 'importante', 'normal'])
    create_parser.add_argument('--due', default='', help='Data de vencimento (YYYY-MM-DD)')

    # update-progress
    progress_parser = subparsers.add_parser('update-progress', help='Atualizar progresso de projeto')
    progress_parser.add_argument('project', help='Nome do projeto')
    progress_parser.add_argument('progress', type=int, help='Progresso (0-100)')

    # list-urgent
    subparsers.add_parser('list-urgent', help='Listar tarefas urgentes')

    # list-projects
    subparsers.add_parser('list-projects', help='Listar projetos ativos')

    args = parser.parse_args()

    # Executar comando
    if args.command == 'create-task':
        create_task(args.name, args.projeto, args.prioridade, args.due)

    elif args.command == 'update-progress':
        update_project_progress(args.project, args.progress)

    elif args.command == 'list-urgent':
        list_urgent_tasks()

    elif args.command == 'list-projects':
        list_active_projects()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
