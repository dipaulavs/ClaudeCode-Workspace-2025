#!/bin/bash

echo "================================================================================"
echo "🛑 PARANDO BOT V4 COMPLETO"
echo "================================================================================"
echo ""

echo "🔴 Parando Chatbot V4..."
pkill -f "chatbot_corretor_v4.py"
pkill -f "chatbot_corretor"

echo "🔴 Parando Middleware..."
pkill -f "webhook_middleware"

echo "🔴 Parando Ngrok..."
pkill ngrok

# Remove PIDs
rm -f .chatbot_v4_pid .middleware_v3_pid .ngrok_v3_pid .all_pids

echo ""
echo "✅ Todos os serviços foram parados!"
echo ""
echo "================================================================================"
