#!/bin/bash

echo "================================================================================"
echo "🛑 PARANDO INTEGRAÇÃO V2"
echo "================================================================================"
echo ""

echo "🔴 Parando Chatbot V2..."
pkill -f "chatbot_corretor_v2.py"

echo "🔴 Parando Middleware V2..."
pkill -f "webhook_middleware_v2.py"

echo "🔴 Parando Ngrok..."
pkill ngrok

rm -f .pids_v2

echo ""
echo "✅ Todos os serviços V2 foram parados!"
echo ""
echo "================================================================================"
