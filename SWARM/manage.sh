#!/bin/bash
# 🔧 Manage Script - Docker Swarm
# Uso: ./manage.sh <comando> [nome-stack]

VPS_HOST="root@82.25.68.132"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${BLUE}[MANAGE]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# Lista comandos disponíveis
show_help() {
    echo "Uso: ./manage.sh <comando> [nome-stack]"
    echo ""
    echo "Comandos:"
    echo "  list              - Lista todas stacks"
    echo "  status <nome>     - Status da stack"
    echo "  restart <nome>    - Reinicia stack (force update)"
    echo "  scale <nome> <n>  - Escala replicas"
    echo "  remove <nome>     - Remove stack (com confirmação)"
    echo ""
}

# Lista todas stacks
list_stacks() {
    log "Stacks no Swarm:"
    ssh $VPS_HOST "docker stack ls"
    echo ""
    log "Serviços:"
    ssh $VPS_HOST "docker service ls"
}

# Status da stack
status_stack() {
    local STACK_NAME="$1"
    log "Status de $STACK_NAME:"
    ssh $VPS_HOST "docker stack ps $STACK_NAME --no-trunc"
}

# Restart stack
restart_stack() {
    local STACK_NAME="$1"
    log "Reiniciando $STACK_NAME..."

    # Force update de todos os serviços da stack
    SERVICES=$(ssh $VPS_HOST "docker stack services $STACK_NAME -q")

    for SERVICE_ID in $SERVICES; do
        ssh $VPS_HOST "docker service update --force $SERVICE_ID" > /dev/null
    done

    success "Reiniciado!"
}

# Scale stack
scale_stack() {
    local STACK_NAME="$1"
    local REPLICAS="$2"

    if [ -z "$REPLICAS" ]; then
        error "Número de réplicas não especificado"
    fi

    log "Escalando $STACK_NAME para $REPLICAS réplicas..."

    SERVICES=$(ssh $VPS_HOST "docker stack services $STACK_NAME -q")

    for SERVICE_ID in $SERVICES; do
        ssh $VPS_HOST "docker service scale $SERVICE_ID=$REPLICAS" > /dev/null
    done

    success "Escalado!"
}

# Remove stack
remove_stack() {
    local STACK_NAME="$1"

    echo -e "${RED}⚠️  ATENÇÃO: Isso vai REMOVER permanentemente a stack: $STACK_NAME${NC}"
    echo -n "Confirma? (digite 'sim' para confirmar): "
    read confirmation

    if [ "$confirmation" = "sim" ]; then
        log "Removendo $STACK_NAME..."
        ssh $VPS_HOST "docker stack rm $STACK_NAME" || error "Falha ao remover"
        success "Removido!"
    else
        echo "Cancelado."
    fi
}

# Validações
if [ -z "$1" ]; then
    show_help
    exit 1
fi

COMMAND="$1"
STACK_NAME="$2"

# Comandos sem nome de stack
if [ "$COMMAND" = "list" ]; then
    list_stacks
    exit 0
fi

if [ -z "$STACK_NAME" ]; then
    error "Nome da stack não especificado"
fi

# Executar comando
case "$COMMAND" in
    status)
        status_stack "$STACK_NAME"
        ;;
    restart)
        restart_stack "$STACK_NAME"
        ;;
    scale)
        scale_stack "$STACK_NAME" "$3"
        ;;
    remove)
        remove_stack "$STACK_NAME"
        ;;
    *)
        error "Comando desconhecido: $COMMAND"
        show_help
        ;;
esac
