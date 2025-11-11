#!/usr/bin/env python3
"""
Obsidian Auto Manager
Gerencia automaticamente tarefas no Obsidian:
1. Detecta novos arquivos em 📋 Tarefas → Adiciona ao Kanban
2. Detecta mudanças no Kanban → Atualiza status no frontmatter
"""

import os
import re
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

VAULT_PATH = Path.home() / "Documents/Obsidian/Claude-code-ios"
TAREFAS_DIR = VAULT_PATH / "📋 Tarefas"
KANBAN_FILE = TAREFAS_DIR / "📊 Kanban.md"

class ObsidianAutoManager(FileSystemEventHandler):
    def __init__(self):
        self.last_kanban_content = self.read_kanban()

    def read_kanban(self):
        """Lê conteúdo do Kanban"""
        if KANBAN_FILE.exists():
            with open(KANBAN_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def extract_tasks_from_kanban(self):
        """Extrai tarefas do Kanban por coluna"""
        content = self.read_kanban()
        tasks = {
            'aberta': [],
            'em_andamento': [],
            'concluída': []
        }

        current_section = None
        for line in content.split('\n'):
            if '## aberta' in line:
                current_section = 'aberta'
            elif '## em_andamento' in line:
                current_section = 'em_andamento'
            elif '## concluída' in line:
                current_section = 'concluída'
            elif current_section and '[[' in line:
                match = re.search(r'\[\[([^\]]+)\]\]', line)
                if match:
                    tasks[current_section].append(match.group(1))

        return tasks

    def update_task_status(self, task_name, new_status):
        """Atualiza status no frontmatter da tarefa"""
        # Procura arquivo
        task_file = TAREFAS_DIR / f"{task_name}.md"

        if not task_file.exists():
            # Tenta buscar case-insensitive
            for file in TAREFAS_DIR.glob("*.md"):
                if file.stem.lower() == task_name.lower():
                    task_file = file
                    break

        if not task_file.exists() or task_file.name == "📊 Kanban.md":
            return

        # Lê conteúdo
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Atualiza status
        if 'status:' in content:
            content = re.sub(
                r'status:\s*\w+',
                f'status: {new_status}',
                content
            )
        else:
            # Adiciona status no frontmatter
            if '---' in content:
                content = re.sub(
                    r'(---\n)',
                    f'\\1status: {new_status}\n',
                    content,
                    count=1
                )

        # Salva
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {task_name} → status: {new_status}")

    def add_task_to_kanban(self, task_name):
        """Adiciona tarefa ao Kanban na coluna 'aberta'"""
        content = self.read_kanban()

        # Verifica se já existe
        if f"[[{task_name}]]" in content:
            return

        # Adiciona na coluna 'aberta'
        lines = content.split('\n')
        new_lines = []
        added = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if '## aberta' in line and not added:
                # Adiciona logo após o header
                new_lines.append(f"- [ ] [[{task_name}]]")
                added = True

        if added:
            with open(KANBAN_FILE, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print(f"📋 Tarefa adicionada ao Kanban: {task_name}")

    def on_created(self, event):
        """Detecta novo arquivo criado"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Se é arquivo .md em 📋 Tarefas (exceto Kanban)
        if (file_path.parent == TAREFAS_DIR and
            file_path.suffix == '.md' and
            file_path.name != '📊 Kanban.md'):

            task_name = file_path.stem
            print(f"\n🆕 Nova tarefa detectada: {task_name}")

            # Aguarda arquivo ser escrito completamente
            time.sleep(0.5)

            # Adiciona ao Kanban
            self.add_task_to_kanban(task_name)

    def on_modified(self, event):
        """Detecta arquivo modificado"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Se é o Kanban que mudou
        if file_path == KANBAN_FILE:
            print(f"\n🔄 Kanban modificado, sincronizando...")

            # Extrai tarefas
            tasks = self.extract_tasks_from_kanban()

            # Atualiza status de todas as tarefas
            for status, task_names in tasks.items():
                for task_name in task_names:
                    self.update_task_status(task_name, status)

def main():
    print("🚀 Obsidian Auto Manager iniciado!")
    print(f"📂 Monitorando: {TAREFAS_DIR}")
    print(f"📊 Kanban: {KANBAN_FILE}")
    print("\n✨ Funcionalidades:")
    print("  1. Nova tarefa em 📋 Tarefas → Adiciona ao Kanban (coluna 'aberta')")
    print("  2. Move tarefa no Kanban → Atualiza status automaticamente")
    print("\nPressione Ctrl+C para parar\n")

    event_handler = ObsidianAutoManager()
    observer = Observer()
    observer.schedule(event_handler, str(TAREFAS_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\n👋 Obsidian Auto Manager encerrado!")

    observer.join()

if __name__ == "__main__":
    main()
