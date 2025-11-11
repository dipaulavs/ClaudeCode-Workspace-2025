#!/bin/bash
# Para Obsidian Auto Manager

PID_FILE="/tmp/obsidian_auto_manager.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        rm "$PID_FILE"
        echo "✅ Obsidian Auto Manager parado (PID: $PID)"
    else
        echo "⚠️  Processo não está rodando"
        rm "$PID_FILE"
    fi
else
    echo "⚠️  PID file não encontrado. Processo pode não estar rodando."
    echo "Para matar manualmente: ps aux | grep obsidian_auto_manager"
fi
