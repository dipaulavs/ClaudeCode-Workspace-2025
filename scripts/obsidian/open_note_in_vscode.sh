#!/bin/bash
# 📝 Abrir nota atual do Obsidian no VS Code
# Uso: ./open_note_in_vscode.sh "/path/to/note.md"

NOTE_PATH="$1"

if [ -z "$NOTE_PATH" ]; then
    echo "❌ Erro: Caminho da nota não fornecido"
    echo "Uso: $0 /path/to/note.md"
    exit 1
fi

if [ ! -f "$NOTE_PATH" ]; then
    echo "❌ Erro: Arquivo não encontrado: $NOTE_PATH"
    exit 1
fi

echo "📝 Abrindo nota no VS Code..."
code "$NOTE_PATH"

FILENAME=$(basename "$NOTE_PATH")
echo "✅ $FILENAME aberto no VS Code"

# Notificação
osascript -e "display notification \"$FILENAME aberto\" with title \"VS Code\""
