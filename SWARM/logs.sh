#!/bin/bash
# 📊 Logs Script - Docker Swarm
# Uso: ./logs.sh <nome-automacao> [linhas]

VPS_HOST="root@82.25.68.132"

if [ -z "$1" ]; then
    echo "Uso: ./logs.sh <nome-automacao> [linhas]"
    echo ""
    echo "Stacks disponíveis:"
    ssh $VPS_HOST "docker stack ls --format '{{.Name}}' 2>/dev/null || echo 'Nenhuma stack encontrada'"
    exit 1
fi

STACK_NAME="$1"
LINES="${2:-50}"

echo "📊 Logs de: $STACK_NAME (últimas $LINES linhas)"
echo "Press CTRL+C to exit"
echo "---"

# Pegar ID do serviço
SERVICE_ID=$(ssh $VPS_HOST "docker stack services $STACK_NAME -q 2>/dev/null | head -1")

if [ -z "$SERVICE_ID" ]; then
    echo "❌ Stack não encontrada: $STACK_NAME"
    exit 1
fi

# Seguir logs
ssh $VPS_HOST "docker service logs -f --tail $LINES $SERVICE_ID"
