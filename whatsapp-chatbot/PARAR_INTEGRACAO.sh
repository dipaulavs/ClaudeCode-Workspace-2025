#!/bin/bash

###############################################################################
# 🛑 SCRIPT PARA PARAR INTEGRAÇÃO HÍBRIDA
###############################################################################

echo "================================================================================"
echo "🛑 PARANDO INTEGRAÇÃO HÍBRIDA"
echo "================================================================================"
echo ""

# Para todos os processos relacionados
echo "🔴 Parando Chatbot..."
pkill -f "chatbot_corretor.py"

echo "🔴 Parando Middleware..."
pkill -f "webhook_middleware.py"

echo "🔴 Parando Ngrok..."
pkill ngrok

# Remove arquivo de PIDs
rm -f .pids

echo ""
echo "✅ Todos os serviços foram parados!"
echo ""
echo "================================================================================"
