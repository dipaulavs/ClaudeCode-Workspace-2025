#!/bin/bash
# Inicia Obsidian Auto Manager em background

cd "$(dirname "$0")"

echo "🚀 Iniciando Obsidian Auto Manager..."

# Verifica se fswatch está instalado
if ! command -v fswatch &> /dev/null; then
    echo "❌ fswatch não está instalado"
    echo "📦 Instale com: brew install fswatch"
    exit 1
fi

# Inicia em background
nohup ./obsidian_auto_manager.sh > /tmp/obsidian_auto_manager.log 2>&1 &

PID=$!
echo $PID > /tmp/obsidian_auto_manager.pid

echo "✅ Obsidian Auto Manager iniciado (PID: $PID)"
echo "📝 Logs: /tmp/obsidian_auto_manager.log"
echo ""
echo "Para parar: ./PARAR_AUTO_MANAGER.sh"
echo "Ver logs: tail -f /tmp/obsidian_auto_manager.log"
