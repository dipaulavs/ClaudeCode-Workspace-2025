#!/usr/bin/env python3
"""
Script para sincronizar status das tarefas entre Kanban e frontmatter
Atualiza automaticamente status="concluída" quando tarefa está em "✅ Concluído"
"""

import re
import os
from pathlib import Path

VAULT_PATH = Path.home() / "Documents/Obsidian/Claude-code-ios"
KANBAN_FILE = VAULT_PATH / "📋 Tarefas/📊 Kanban.md"
TAREFAS_DIR = VAULT_PATH / "📋 Tarefas"

def extract_tasks_from_kanban():
    """Extrai tarefas de cada coluna do Kanban"""
    with open(KANBAN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = {
        'a_fazer': [],
        'em_andamento': [],
        'concluido': []
    }

    # Regex para encontrar links de tarefas
    current_section = None

    for line in content.split('\n'):
        if '## aberta' in line:
            current_section = 'a_fazer'
        elif '## em_andamento' in line:
            current_section = 'em_andamento'
        elif '## concluída' in line:
            current_section = 'concluido'
        elif current_section and '[[' in line:
            # Extrai nome do arquivo do link
            match = re.search(r'\[\[([^\]]+)\]\]', line)
            if match:
                task_name = match.group(1)
                tasks[current_section].append(task_name)

    return tasks

def update_task_status(task_file, new_status):
    """Atualiza o status no frontmatter da tarefa"""
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Atualiza status no frontmatter
    if 'status:' in content:
        content = re.sub(
            r'status:\s*\w+',
            f'status: {new_status}',
            content
        )
    else:
        # Adiciona status se não existir
        content = re.sub(
            r'(---\n)',
            f'\\1status: {new_status}\n',
            content,
            count=1
        )

    with open(task_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Atualizado: {task_file.name} → status: {new_status}")

def sync_tasks():
    """Sincroniza status das tarefas"""
    print("🔄 Sincronizando status das tarefas...\n")

    kanban_tasks = extract_tasks_from_kanban()

    # Mapeia status
    status_map = {
        'a_fazer': 'aberta',
        'em_andamento': 'em_andamento',
        'concluido': 'concluída'
    }

    updated = 0

    for section, task_names in kanban_tasks.items():
        for task_name in task_names:
            # Procura arquivo da tarefa
            task_file = TAREFAS_DIR / f"{task_name}.md"

            if not task_file.exists():
                # Tenta encontrar com Title Case
                for file in TAREFAS_DIR.glob("*.md"):
                    if file.stem.lower() == task_name.lower():
                        task_file = file
                        break

            if task_file.exists() and task_file.name != "📊 Kanban.md":
                new_status = status_map[section]
                update_task_status(task_file, new_status)
                updated += 1

    print(f"\n✅ {updated} tarefas atualizadas!")

if __name__ == "__main__":
    sync_tasks()
