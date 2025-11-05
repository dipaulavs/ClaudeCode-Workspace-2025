#!/bin/bash

echo "=============================================="
echo "🛑 PARANDO CHATBOT LF IMÓVEIS"
echo "=============================================="

# Para todos os processos relacionados
echo ""
echo "🔄 Parando processos..."

pkill -f "chatbot_imobili-ria-premium_v4.py"
pkill -f "webhook_middleware_imobili-ria-premium.py"

sleep 2

# Verifica se pararam
BOT_RUNNING=$(ps aux | grep "chatbot_imobili-ria-premium_v4.py" | grep -v grep)
MIDDLEWARE_RUNNING=$(ps aux | grep "webhook_middleware_imobili-ria-premium.py" | grep -v grep)

echo ""
if [ -z "$BOT_RUNNING" ]; then
    echo "   ✅ Chatbot: PARADO"
else
    echo "   ⚠️  Chatbot: Ainda rodando"
    echo "      Tente: pkill -9 -f chatbot_imobili-ria-premium_v4.py"
fi

if [ -z "$MIDDLEWARE_RUNNING" ]; then
    echo "   ✅ Middleware: PARADO"
else
    echo "   ⚠️  Middleware: Ainda rodando"
    echo "      Tente: pkill -9 -f webhook_middleware_imobili-ria-premium.py"
fi

echo ""
echo "=============================================="
echo "✅ Processo de parada concluído"
echo "=============================================="
