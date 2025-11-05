#!/bin/bash

echo "=============================================="
echo "🛑 PARANDO CHATBOT AUTOMAIA V1"
echo "=============================================="

# Para todos os processos relacionados
echo ""
echo "🔄 Parando processos..."

pkill -f "chatbot_automaia_v1.py"
pkill -f "webhook_middleware_automaia.py"

sleep 2

# Verifica se pararam
BOT_RUNNING=$(ps aux | grep "chatbot_automaia_v1.py" | grep -v grep)
MIDDLEWARE_RUNNING=$(ps aux | grep "webhook_middleware_automaia.py" | grep -v grep)

echo ""
if [ -z "$BOT_RUNNING" ]; then
    echo "   ✅ Chatbot: PARADO"
else
    echo "   ⚠️  Chatbot: Ainda rodando"
    echo "      Tente: pkill -9 -f chatbot_automaia_v1.py"
fi

if [ -z "$MIDDLEWARE_RUNNING" ]; then
    echo "   ✅ Middleware: PARADO"
else
    echo "   ⚠️  Middleware: Ainda rodando"
    echo "      Tente: pkill -9 -f webhook_middleware_automaia.py"
fi

echo ""
echo "=============================================="
echo "✅ Processo de parada concluído"
echo "=============================================="
