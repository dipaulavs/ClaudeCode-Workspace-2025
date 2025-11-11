#!/bin/bash
# 🌐 Iniciar servidor webhook para iPad → MacBook
# Uso: ./start_webhook_server.sh

WORKSPACE="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"
cd "$WORKSPACE"

echo "🌐 Iniciando webhook server..."
echo "📡 IP Local: 192.168.18.11"
echo "🔗 URL: http://192.168.18.11:8000"
echo ""
echo "📱 No iPad, usar:"
echo "   http://192.168.18.11:8000/obsidian/process"
echo "   http://192.168.18.11:8000/obsidian/task"
echo ""
echo "🛑 Para parar: Ctrl+C"
echo ""

python3 SCRIPTS/obsidian/webhook_listener.py
