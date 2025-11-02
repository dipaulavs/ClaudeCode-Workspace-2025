#!/bin/bash

###############################################################################
# 🚀 SCRIPT DE INICIALIZAÇÃO - INTEGRAÇÃO HÍBRIDA CHATWOOT + BOT
###############################################################################

echo "================================================================================"
echo "🚀 INICIALIZANDO INTEGRAÇÃO HÍBRIDA - CHATWOOT + BOT WHATSAPP"
echo "================================================================================"
echo ""

# Verifica se está no diretório correto
if [ ! -f "chatbot_corretor.py" ]; then
    echo "❌ Erro: Execute este script no diretório do projeto!"
    exit 1
fi

# Função para verificar se porta está em uso
check_port() {
    lsof -i:$1 > /dev/null 2>&1
    return $?
}

# 1. Inicia o Bot Original (porta 5001)
echo "📌 PASSO 1: Iniciando Chatbot Original (porta 5001)..."
if check_port 5001; then
    echo "⚠️  Porta 5001 já está em uso. Parando processo..."
    pkill -f "chatbot_corretor.py"
    sleep 2
fi

python3 chatbot_corretor.py > logs/chatbot.log 2>&1 &
CHATBOT_PID=$!
echo "✅ Chatbot iniciado (PID: $CHATBOT_PID)"
sleep 3

# 2. Inicia o Webhook Middleware (porta 5002)
echo ""
echo "📌 PASSO 2: Iniciando Webhook Middleware (porta 5002)..."
if check_port 5002; then
    echo "⚠️  Porta 5002 já está em uso. Parando processo..."
    pkill -f "webhook_middleware.py"
    sleep 2
fi

python3 webhook_middleware.py > logs/middleware.log 2>&1 &
MIDDLEWARE_PID=$!
echo "✅ Middleware iniciado (PID: $MIDDLEWARE_PID)"
sleep 3

# 3. Inicia ngrok (porta 5002 - expõe o middleware)
echo ""
echo "📌 PASSO 3: Iniciando ngrok (expondo middleware)..."
pkill ngrok 2>/dev/null
sleep 2

ngrok http 5002 > /dev/null &
NGROK_PID=$!
echo "✅ Ngrok iniciado (PID: $NGROK_PID)"
sleep 5

# Pega URL pública do ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Erro ao obter URL do ngrok!"
    echo "Verifique se ngrok está instalado e configurado."
    exit 1
fi

echo "📍 URL Pública: $NGROK_URL"
echo ""

# 4. Configura webhook na Evolution API
echo "📌 PASSO 4: Configurando webhook na Evolution API..."
python3 configurar_webhook.py "${NGROK_URL}/webhook/evolution"

echo ""
echo "================================================================================"
echo "✅ INTEGRAÇÃO HÍBRIDA INICIADA COM SUCESSO!"
echo "================================================================================"
echo ""
echo "📊 RESUMO:"
echo "  🤖 Chatbot:       http://localhost:5001         (PID: $CHATBOT_PID)"
echo "  🔄 Middleware:    http://localhost:5002         (PID: $MIDDLEWARE_PID)"
echo "  🌐 Ngrok:         $NGROK_URL   (PID: $NGROK_PID)"
echo ""
echo "📝 LOGS:"
echo "  Chatbot:     tail -f logs/chatbot.log"
echo "  Middleware:  tail -f logs/middleware.log"
echo ""
echo "🎯 COMO FUNCIONA:"
echo "  1. Cliente manda mensagem → Evolution API"
echo "  2. Evolution → Middleware ($NGROK_URL/webhook/evolution)"
echo "  3. Middleware envia para Chatwoot"
echo "  4. Middleware verifica: Tem atendente ativo?"
echo "     👤 SIM → Humano responde (bot fica quieto)"
echo "     🤖 NÃO → Bot responde automaticamente"
echo ""
echo "🛑 PARA PARAR TUDO:"
echo "  ./PARAR_INTEGRACAO.sh"
echo ""
echo "================================================================================"

# Salva PIDs em arquivo para parar depois
echo "$CHATBOT_PID" > .pids
echo "$MIDDLEWARE_PID" >> .pids
echo "$NGROK_PID" >> .pids

# Monitora logs em tempo real
echo ""
echo "🔍 Monitorando logs (Ctrl+C para sair)..."
echo "================================================================================"
tail -f logs/middleware.log
