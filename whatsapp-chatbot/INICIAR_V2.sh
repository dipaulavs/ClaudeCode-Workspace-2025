#!/bin/bash

###############################################################################
# 🚀 VERSÃO 2.0 - Bot recebe webhook do CHATWOOT (não Evolution)
#
# VANTAGENS:
# ✅ Chatwoot já processa mídias e disponibiliza URLs
# ✅ Não precisa descriptografar áudio
# ✅ Formato padronizado
# ✅ Mais simples e confiável
###############################################################################

echo "================================================================================"
echo "🚀 VERSÃO 2.0 - BOT RECEBE DO CHATWOOT"
echo "================================================================================"
echo ""

if [ ! -f "chatbot_corretor_v2.py" ]; then
    echo "❌ Erro: Execute este script no diretório do projeto!"
    exit 1
fi

check_port() {
    lsof -i:$1 > /dev/null 2>&1
    return $?
}

# Cria diretório de logs
mkdir -p logs

# 1. Inicia Bot V2 (porta 5001)
echo "📌 PASSO 1: Iniciando Chatbot V2 (porta 5001)..."
if check_port 5001; then
    echo "⚠️  Porta 5001 já em uso. Parando..."
    pkill -f "chatbot_corretor"
    sleep 2
fi

python3 chatbot_corretor_v2.py > logs/chatbot_v2.log 2>&1 &
CHATBOT_PID=$!
echo "✅ Chatbot V2 iniciado (PID: $CHATBOT_PID)"
sleep 3

# 2. Inicia Middleware V2 (porta 5002)
echo ""
echo "📌 PASSO 2: Iniciando Middleware V2 (porta 5002)..."
if check_port 5002; then
    echo "⚠️  Porta 5002 já em uso. Parando..."
    pkill -f "webhook_middleware"
    sleep 2
fi

python3 webhook_middleware_v2.py > logs/middleware_v2.log 2>&1 &
MIDDLEWARE_PID=$!
echo "✅ Middleware V2 iniciado (PID: $MIDDLEWARE_PID)"
sleep 3

# 3. Inicia ngrok (porta 5002)
echo ""
echo "📌 PASSO 3: Iniciando ngrok..."
pkill ngrok 2>/dev/null
sleep 2

ngrok http 5002 > /dev/null &
NGROK_PID=$!
echo "✅ Ngrok iniciado (PID: $NGROK_PID)"
sleep 5

# Pega URL do ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Erro ao obter URL do ngrok!"
    exit 1
fi

echo "📍 URL Pública: $NGROK_URL"
echo ""

# 4. Configura webhook na Evolution
echo "📌 PASSO 4: Configurando webhook na Evolution API..."
python3 configurar_webhook.py "${NGROK_URL}/webhook/evolution"

echo ""
echo "================================================================================"
echo "✅ VERSÃO 2.0 INICIADA COM SUCESSO!"
echo "================================================================================"
echo ""
echo "📊 RESUMO:"
echo "  🤖 Chatbot V2:    http://localhost:5001         (PID: $CHATBOT_PID)"
echo "  🔄 Middleware V2: http://localhost:5002         (PID: $MIDDLEWARE_PID)"
echo "  🌐 Ngrok:         $NGROK_URL   (PID: $NGROK_PID)"
echo ""
echo "📝 LOGS:"
echo "  Chatbot:     tail -f logs/chatbot_v2.log"
echo "  Middleware:  tail -f logs/middleware_v2.log"
echo ""
echo "🎯 NOVO FLUXO (V2):"
echo "  1. Evolution → Middleware → Cria mensagem no Chatwoot"
echo "  2. Chatwoot dispara webhook message_created → Middleware"
echo "  3. Middleware verifica: Tem atendente?"
echo "     👤 SIM → Humano responde"
echo "     🤖 NÃO → Bot responde (FORMATO CHATWOOT!)"
echo "  4. Bot recebe dados processados:"
echo "     ✅ URLs de mídia prontas"
echo "     ✅ Sem criptografia"
echo "     ✅ Formato padronizado"
echo ""
echo "⚠️  IMPORTANTE - Configure webhook do Chatwoot:"
echo "  1. Acesse: https://chatwoot.loop9.com.br"
echo "  2. Settings → Inboxes → LF IMOVEIS"
echo "  3. Webhook URL: ${NGROK_URL}/webhook/chatwoot"
echo "  4. Marque: Message Created + Message Updated"
echo ""
echo "🛑 PARA PARAR:"
echo "  ./PARAR_V2.sh"
echo ""
echo "================================================================================"

# Salva PIDs
echo "$CHATBOT_PID" > .pids_v2
echo "$MIDDLEWARE_PID" >> .pids_v2
echo "$NGROK_PID" >> .pids_v2

echo ""
echo "🔍 Monitorando logs (Ctrl+C para sair)..."
echo "================================================================================"
tail -f logs/middleware_v2.log
