#!/bin/bash

echo "=============================================="
echo "🚀 INICIANDO CHATBOT AUTOMAIA V1"
echo "=============================================="

# Navega para o diretório do chatbot
cd "$(dirname "$0")"

# Verifica se chatwoot_config_automaia.json existe
if [ ! -f "chatwoot_config_automaia.json" ]; then
    echo ""
    echo "❌ ERRO: Arquivo chatwoot_config_automaia.json não encontrado!"
    echo ""
    echo "📝 Crie o arquivo com base no imobili-ria-premium:"
    echo "   cp chatwoot_config_automaia.json.imobili-ria-premium chatwoot_config_automaia.json"
    echo ""
    echo "   E configure as credenciais:"
    echo "   - Chatwoot URL, Token, Account ID, Inbox ID"
    echo "   - Evolution URL, API Key, Instance"
    echo ""
    exit 1
fi

# Cria diretório de logs se não existir
mkdir -p logs

# Para processos antigos (se existirem)
echo ""
echo "🔄 Verificando processos existentes..."
pkill -f "chatbot_automaia_v1.py" 2>/dev/null
pkill -f "webhook_middleware_automaia.py" 2>/dev/null
sleep 2

# Inicia o middleware em background
echo ""
echo "📡 Iniciando Middleware (porta 5008)..."
nohup python3 webhook_middleware_automaia.py > logs/middleware_automaia.log 2>&1 &
MIDDLEWARE_PID=$!
echo "   PID: $MIDDLEWARE_PID"

sleep 2

# Inicia o chatbot em background
echo ""
echo "🤖 Iniciando Chatbot Automaia (porta 5007)..."
nohup python3 chatbot_automaia_v1.py > logs/chatbot_automaia.log 2>&1 &
BOT_PID=$!
echo "   PID: $BOT_PID"

sleep 3

# Verifica se estão rodando
echo ""
echo "✅ Verificando status..."
echo ""

if ps -p $MIDDLEWARE_PID > /dev/null; then
   echo "   ✅ Middleware: ONLINE (PID $MIDDLEWARE_PID)"
else
   echo "   ❌ Middleware: FALHOU"
fi

if ps -p $BOT_PID > /dev/null; then
   echo "   ✅ Chatbot: ONLINE (PID $BOT_PID)"
else
   echo "   ❌ Chatbot: FALHOU"
fi

echo ""
echo "=============================================="
echo "📋 URLs importantes:"
echo "=============================================="
echo "   🤖 Bot:        http://localhost:5007/health"
echo "   📡 Middleware: http://localhost:5008/health"
echo ""
echo "📁 Logs:"
echo "   Bot:        tail -f logs/chatbot_automaia.log"
echo "   Middleware: tail -f logs/middleware_automaia.log"
echo ""
echo "🛑 Para parar: ./PARAR_BOT_AUTOMAIA.sh"
echo "=============================================="
