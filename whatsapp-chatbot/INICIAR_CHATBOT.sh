#!/bin/bash

# Script de início rápido do Chatbot Corretor

echo "=========================================="
echo "🤖 CHATBOT CORRETOR DE IMÓVEIS"
echo "=========================================="
echo ""

# Verificar se ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "⚠️  ngrok não encontrado. Instalando..."
    brew install ngrok/ngrok/ngrok
fi

echo "📋 PASSO 1: Iniciar servidor Flask"
echo "   python3 chatbot_corretor.py"
echo ""

echo "📋 PASSO 2: Em outro terminal, iniciar ngrok"
echo "   ngrok http 5000"
echo ""

echo "📋 PASSO 3: Copiar URL do ngrok e configurar webhook"
echo "   python3 configurar_webhook.py https://SUA-URL-NGROK.ngrok-free.app/webhook"
echo ""

echo "📋 PASSO 4: Testar enviando mensagem para 5531980160822"
echo ""

echo "=========================================="
echo ""

read -p "Deseja iniciar o servidor Flask agora? (s/n): " resposta

if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    echo ""
    echo "🚀 Iniciando servidor Flask..."
    echo ""
    python3 chatbot_corretor.py
else
    echo ""
    echo "✅ Para iniciar manualmente: python3 chatbot_corretor.py"
    echo ""
fi
