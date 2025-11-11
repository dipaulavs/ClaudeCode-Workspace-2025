#!/usr/bin/env python3
"""
🐍 Process Obsidian note with Python
Uso: python3 process_note.py "/path/to/note.md"
"""

import sys
import os
from pathlib import Path

def process_note(note_path: str):
    """Processa nota do Obsidian"""

    if not os.path.exists(note_path):
        print(f"❌ Erro: Arquivo não encontrado: {note_path}")
        sys.exit(1)

    # Ler conteúdo
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = Path(note_path).name

    # Análise básica
    lines = content.split('\n')
    words = content.split()
    chars = len(content)

    # Contar elementos Markdown
    headers = [line for line in lines if line.startswith('#')]
    links = [word for word in words if '[[' in word or 'http' in word]
    tasks = [line for line in lines if '- [ ]' in line or '- [x]' in line]

    # Resultado
    print(f"📄 {filename}")
    print(f"📊 Estatísticas:")
    print(f"   • Linhas: {len(lines)}")
    print(f"   • Palavras: {len(words)}")
    print(f"   • Caracteres: {chars}")
    print(f"   • Headers: {len(headers)}")
    print(f"   • Links: {len(links)}")
    print(f"   • Tarefas: {len(tasks)}")

    # Salvar análise
    workspace = "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"
    output_dir = Path(workspace) / "temp" / "obsidian"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{Path(filename).stem}_analysis.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Análise: {filename}\n")
        f.write(f"Linhas: {len(lines)}\n")
        f.write(f"Palavras: {len(words)}\n")
        f.write(f"Headers: {len(headers)}\n")
        f.write(f"Links: {len(links)}\n")
        f.write(f"Tarefas: {len(tasks)}\n")

    print(f"\n✅ Análise salva: {output_file}")

    # Notificação macOS
    os.system(f'osascript -e \'display notification "Análise concluída" with title "{filename}"\'')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Erro: Caminho da nota não fornecido")
        print(f"Uso: {sys.argv[0]} /path/to/note.md")
        sys.exit(1)

    note_path = sys.argv[1]
    process_note(note_path)
