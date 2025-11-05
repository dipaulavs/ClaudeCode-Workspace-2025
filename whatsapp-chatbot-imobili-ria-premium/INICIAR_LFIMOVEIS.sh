#!/bin/bash

echo "=============================================="
echo "🏠 INICIANDO CHATBOT LF IMÓVEIS COM NGROK"
echo "=============================================="

cd "$(dirname "$0")"

# Verifica config
if [ ! -f "chatwoot_config_imobili-ria-premium.json" ]; then
    echo "❌ Config não encontrado!"
    exit 1
fi

mkdir -p logs

# Para processos antigos
echo ""
echo "🔄 Parando processos anteriores..."
pkill -f "chatbot_imobili-ria-premium" 2>/dev/null
pkill -f "webhook_middleware_imobili-ria-premium" 2>/dev/null
pkill -f "ngrok http 5008" 2>/dev/null
sleep 2

# Portas LF Imóveis: 5007 (bot) | 5008 (middleware)

# Inicia middleware
echo ""
echo "📡 Iniciando Middleware (porta 5008)..."
nohup python3 webhook_middleware_imobili-ria-premium.py > logs/middleware_lfimoveis.log 2>&1 &
MIDDLEWARE_PID=$!
echo "   PID: $MIDDLEWARE_PID"
sleep 2

# Inicia chatbot
echo ""
echo "🤖 Iniciando Chatbot LF Imóveis (porta 5007)..."
nohup python3 chatbot_imobili-ria-premium_v4.py > logs/chatbot_lfimoveis.log 2>&1 &
BOT_PID=$!
echo "   PID: $BOT_PID"
sleep 3

# Inicia ngrok
echo ""
echo "🌐 Iniciando Ngrok (porta 5008)..."
nohup ngrok http 5008 > /tmp/ngrok_lfimoveis.log 2>&1 &
NGROK_PID=$!
echo "   PID: $NGROK_PID"

echo ""
echo "⏳ Aguardando ngrok (5 segundos)..."
sleep 5

# Obtém URL ngrok
echo ""
echo "🔍 Obtendo URL pública..."
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for tunnel in data.get('tunnels', []):
        if tunnel.get('proto') == 'https':
            print(tunnel.get('public_url'))
            break
except:
    print('')
" 2>/dev/null)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Erro ao obter URL ngrok"
    exit 1
fi

echo "✅ Ngrok URL: $NGROK_URL"

# Lê config
CHATWOOT_URL=$(python3 -c "import json; f=open('chatwoot_config_imobili-ria-premium.json'); c=json.load(f); print(c['chatwoot']['url'])")
CHATWOOT_TOKEN=$(python3 -c "import json; f=open('chatwoot_config_imobili-ria-premium.json'); c=json.load(f); print(c['chatwoot']['token'])")
ACCOUNT_ID=$(python3 -c "import json; f=open('chatwoot_config_imobili-ria-premium.json'); c=json.load(f); print(c['chatwoot']['account_id'])")
EVOLUTION_URL=$(python3 -c "import json; f=open('chatwoot_config_imobili-ria-premium.json'); c=json.load(f); print(c['evolution']['url'])")
EVOLUTION_API_KEY=$(python3 -c "import json; f=open('chatwoot_config_imobili-ria-premium.json'); c=json.load(f); print(c['evolution']['api_key'])")
EVOLUTION_INSTANCE=$(python3 -c "import json; f=open('chatwoot_config_imobili-ria-premium.json'); c=json.load(f); print(c['evolution']['instance'])")

# Configura webhook Evolution
echo ""
echo "⚙️  Configurando webhook Evolution..."
curl -s -X POST "${EVOLUTION_URL}/webhook/set/${EVOLUTION_INSTANCE}" \
  -H "apikey: ${EVOLUTION_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d "{\"webhook\":{\"enabled\":true,\"url\":\"${NGROK_URL}/webhook/evolution\",\"webhook_by_events\":false,\"webhook_base64\":false,\"events\":[\"MESSAGES_UPSERT\"]}}" > /dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ Webhook Evolution configurado"
    echo "   URL: ${NGROK_URL}/webhook/evolution"
else
    echo "   ⚠️  Erro webhook Evolution"
fi

# Configura webhook Chatwoot
echo ""
echo "⚙️  Configurando webhook Chatwoot..."

# Deleta webhooks localhost antigos
python3 << EOF
import requests
chatwoot_url = '${CHATWOOT_URL}'
access_token = '${CHATWOOT_TOKEN}'
account_id = '${ACCOUNT_ID}'

url = f'{chatwoot_url}/api/v1/accounts/{account_id}/webhooks'
headers = {'api_access_token': access_token}

response = requests.get(url, headers=headers, timeout=30)
if response.status_code == 200:
    webhooks = response.json().get('payload', {}).get('webhooks', [])
    for webhook in webhooks:
        if 'localhost' in webhook.get('url', ''):
            webhook_id = webhook.get('id')
            delete_url = f'{chatwoot_url}/api/v1/accounts/{account_id}/webhooks/{webhook_id}'
            requests.delete(delete_url, headers=headers, timeout=30)
EOF

# Cria webhook com ngrok
python3 << EOF
import requests
chatwoot_url = '${CHATWOOT_URL}'
access_token = '${CHATWOOT_TOKEN}'
account_id = '${ACCOUNT_ID}'
ngrok_url = '${NGROK_URL}'

url = f'{chatwoot_url}/api/v1/accounts/{account_id}/webhooks'
headers = {'api_access_token': access_token, 'Content-Type': 'application/json'}
payload = {'url': f'{ngrok_url}/webhook/chatwoot', 'subscriptions': ['message_created']}

response = requests.post(url, headers=headers, json=payload, timeout=30)
if response.status_code in [200, 201]:
    print('   ✅ Webhook Chatwoot configurado')
    print(f'   URL: {ngrok_url}/webhook/chatwoot')
else:
    print(f'   ⚠️  Erro: {response.status_code}')
EOF

# Status
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

if ps -p $NGROK_PID > /dev/null; then
   echo "   ✅ Ngrok: ONLINE (PID $NGROK_PID)"
else
   echo "   ❌ Ngrok: FALHOU"
fi

echo ""
echo "=============================================="
echo "📋 URLs:"
echo "=============================================="
echo "   🌐 Ngrok:      $NGROK_URL"
echo "   🤖 Bot:        http://localhost:5007/health"
echo "   📡 Middleware: http://localhost:5008/health"
echo ""
echo "📁 Logs:"
echo "   Bot:        tail -f logs/chatbot_lfimoveis.log"
echo "   Middleware: tail -f logs/middleware_lfimoveis.log"
echo ""
echo "🛑 Parar: pkill -f 'imobili-ria-premium' && pkill -f ngrok"
echo "=============================================="
