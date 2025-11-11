#!/bin/bash
# ⚡ Comando rápido: Enviar comando para Claude Code via arquivo
# Uso: ./quick_command.sh "seu comando aqui"

WORKSPACE="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"
COMMANDS_FILE="$WORKSPACE/temp/obsidian/COMMANDS.txt"

mkdir -p "$WORKSPACE/temp/obsidian"

if [ -z "$1" ]; then
    echo "❌ Erro: Nenhum comando fornecido"
    echo "Uso: $0 \"seu comando aqui\""
    exit 1
fi

COMMAND="$1"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Adicionar comando ao arquivo
echo "[$TIMESTAMP] $COMMAND" >> "$COMMANDS_FILE"

echo "✅ Comando adicionado:"
echo "   $COMMAND"
echo ""
echo "📁 Arquivo: $COMMANDS_FILE"

# Notificação
osascript -e "display notification \"$COMMAND\" with title \"Comando adicionado\""
