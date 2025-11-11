#!/bin/bash

# Script para criar CNAME no Cloudflare DNS
# Uso: ./create_cloudflare_cname.sh <subdomain>
# Exemplo: ./create_cloudflare_cname.sh obrigado

set -e

SUBDOMAIN=$1
ZONE_ID="e28ff35f0f4e5ba0da93688f8352dd9f"
CF_EMAIL="felipidipaula@gmail.com"
CF_API_KEY="7e720179db9ea1041b9a030a531250750ce17"

if [ -z "$SUBDOMAIN" ]; then
    echo "❌ Erro: Subdomínio não especificado"
    echo "Uso: $0 <subdomain>"
    echo "Exemplo: $0 obrigado"
    exit 1
fi

echo "🌐 Criando CNAME: ${SUBDOMAIN}.loop9.com.br → vps.loop9.com.br"

# Criar registro CNAME
RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "X-Auth-Email: ${CF_EMAIL}" \
  -H "X-Auth-Key: ${CF_API_KEY}" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"CNAME\",\"name\":\"${SUBDOMAIN}\",\"content\":\"vps.loop9.com.br\",\"ttl\":1,\"proxied\":false}")

# Verificar sucesso
SUCCESS=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['success'])")

if [ "$SUCCESS" = "True" ]; then
    echo "✅ CNAME criado com sucesso!"
    echo "   ${SUBDOMAIN}.loop9.com.br → vps.loop9.com.br"
else
    # Verificar se já existe
    ERROR_CODE=$(echo $RESPONSE | python3 -c "import sys, json; errors = json.load(sys.stdin).get('errors', []); print(errors[0]['code'] if errors else '')" 2>/dev/null || echo "")

    if [ "$ERROR_CODE" = "81057" ]; then
        echo "⚠️  CNAME já existe para ${SUBDOMAIN}.loop9.com.br"
        echo "   Continuando com deploy..."
        exit 0
    else
        echo "❌ Erro ao criar CNAME:"
        echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
        exit 1
    fi
fi

echo ""
echo "⏳ Aguardando propagação DNS (5 segundos)..."
sleep 5
echo "✅ DNS propagado!"
