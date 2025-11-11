#!/bin/bash
# 📤 Send Obsidian note to Claude Code
# Uso: ./send_to_claude.sh "/path/to/note.md"

set -e

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

# Ler conteúdo da nota
CONTENT=$(cat "$NOTE_PATH")
FILENAME=$(basename "$NOTE_PATH")

# Criar arquivo temporário para Claude Code processar
WORKSPACE="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"
TEMP_DIR="$WORKSPACE/temp/obsidian"
mkdir -p "$TEMP_DIR"

TEMP_FILE="$TEMP_DIR/$FILENAME"
cp "$NOTE_PATH" "$TEMP_FILE"

echo "✅ Nota copiada para Claude Code workspace"
echo "📁 Local: $TEMP_FILE"
echo "📝 Arquivo: $FILENAME"

# Notificação macOS
osascript -e "display notification \"$FILENAME enviado para Claude Code\" with title \"Obsidian → Claude Code\""

exit 0
