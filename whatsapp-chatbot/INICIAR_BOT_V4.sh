#!/bin/bash

###############################################################################
# 🚀 INICIAR BOT V4 COMPLETO - Integração Híbrida Chatwoot
#
# Funcionalidades V4:
# ✅ Debounce 15s + 50s (análise IA)
# ✅ Fila no Redis
# ✅ Timers por número
# ✅ Resposta DIRETA via Evolution (sem loop)
# ✅ Mensagens humanizadas
###############################################################################

echo "================================================================================"
echo "🚀 INICIANDO BOT V4 COMPLETO - INTEGRAÇÃO HÍBRIDA"
echo "================================================================================"
echo ""

if [ ! -f "chatbot_corretor_v4.py" ]; then
    echo "❌ Erro: chatbot_corretor_v4.py não encontrado!"
    exit 1
fi

check_port() {
    lsof -i:$1 > /dev/null 2>&1
    return $?
}

mkdir -p logs

# Parar processos antigos
echo "🛑 Parando processos antigos..."
pkill -f "chatbot_corretor" 2>/dev/null
pkill -f "webhook_middleware" 2>/dev/null
pkill ngrok 2>/dev/null
sleep 2

# 1. Inicia Bot V4 (porta 5001)
echo ""
echo "📌 PASSO 1: Iniciando Chatbot V4..."
nohup python3 chatbot_corretor_v4.py > logs/chatbot_v4.log 2>&1 &
CHATBOT_PID=$!
echo $CHATBOT_PID > .chatbot_v4_pid
echo "✅ Chatbot V4 iniciado (PID: $CHATBOT_PID)"
sleep 3

# 2. Inicia Middleware V2 (porta 5002)
echo ""
echo "📌 PASSO 2: Iniciando Middleware..."
nohup python3 webhook_middleware_v2.py > logs/middleware_v3.log 2>&1 &
MIDDLEWARE_PID=$!
echo $MIDDLEWARE_PID > .middleware_v3_pid
echo "✅ Middleware iniciado (PID: $MIDDLEWARE_PID)"
sleep 3

# 3. Inicia ngrok (porta 5002)
echo ""
echo "📌 PASSO 3: Iniciando ngrok..."
nohup ngrok http 5002 > /dev/null 2>&1 &
NGROK_PID=$!
echo $NGROK_PID > .ngrok_v3_pid
echo "✅ Ngrok iniciado (PID: $NGROK_PID)"
sleep 5

# Pega URL do ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Erro ao obter URL do ngrok!"
    exit 1
fi

echo "📍 URL Pública: $NGROK_URL"

# 4. Configura webhook Evolution
echo ""
echo "📌 PASSO 4: Configurando webhook Evolution..."
python3 configurar_webhook.py "${NGROK_URL}/webhook/evolution"

echo ""
echo "================================================================================"
echo "✅ BOT V4 COMPLETO INICIADO COM SUCESSO!"
echo "================================================================================"
echo ""
echo "📊 RESUMO:"
echo "  🤖 Chatbot V4:    http://localhost:5001         (PID: $CHATBOT_PID)"
echo "  🔄 Middleware:    http://localhost:5002         (PID: $MIDDLEWARE_PID)"
echo "  🌐 Ngrok:         $NGROK_URL   (PID: $NGROK_PID)"
echo ""
echo "📝 LOGS:"
echo "  tail -f logs/chatbot_v4.log"
echo "  tail -f logs/middleware_v3.log"
echo ""
echo "🎯 RECURSOS V4:"
echo "  ⏳ Debounce 15s (agrupa mensagens)"
echo "  🧠 Análise IA de completude"
echo "  ⏱️ +50s se mensagem incompleta"
echo "  📦 Fila no Redis"
echo "  ✂️ Mensagens humanizadas e picotadas"
echo "  🤖 Claude Haiku 4.5 via OpenRouter"
echo "  💾 Contexto de 14 dias"
echo "  🔄 Sem loop (Evolution direto)"
echo ""
echo "📊 STATUS:"
curl -s http://localhost:5001/health 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"  Bot: {d['status']} | Versão: {d['version']} | Timers: {d['timers_ativos']}\")" 2>/dev/null || echo "  Bot: iniciando..."
echo ""
echo "🛑 PARA PARAR:"
echo "  ./PARAR_BOT_V4.sh"
echo ""
echo "================================================================================"

# Salva PIDs
echo "$CHATBOT_PID" > .all_pids
echo "$MIDDLEWARE_PID" >> .all_pids
echo "$NGROK_PID" >> .all_pids

echo ""
echo "🔍 Monitorando logs (Ctrl+C para sair)..."
echo "================================================================================"
tail -f logs/chatbot_v4.log
