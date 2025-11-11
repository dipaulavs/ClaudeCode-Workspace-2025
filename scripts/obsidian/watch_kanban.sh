#!/bin/bash
# Watch Kanban file for changes and auto-sync status

KANBAN_FILE="$HOME/Documents/Obsidian/Claude-code-ios/📋 Tarefas/📊 Kanban.md"
SYNC_SCRIPT="$(dirname "$0")/sync_kanban_status.py"

echo "👀 Monitorando Kanban para sincronização automática..."
echo "📂 Arquivo: $KANBAN_FILE"
echo ""

# Executa sync inicial
python3 "$SYNC_SCRIPT"

# Monitora mudanças (macOS)
fswatch -o "$KANBAN_FILE" | while read change
do
    echo ""
    echo "🔄 Mudança detectada! Sincronizando..."
    python3 "$SYNC_SCRIPT"
done
