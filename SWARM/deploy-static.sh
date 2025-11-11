#!/bin/bash
# 🌐 Deploy Script - Sites Estáticos (sem Docker build)
# Uso: ./deploy-static.sh <nome-site>

set -e

VPS_HOST="root@82.25.68.132"
VPS_PATH="/root/swarm-sites"
LOCAL_AUTOMATIONS="./automations"
DOMAIN="loop9.com.br"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[DEPLOY]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

if [ -z "$1" ]; then
    error "Uso: ./deploy-static.sh <nome-site>"
fi

SITE_NAME="$1"
SITE_PATH="$LOCAL_AUTOMATIONS/$SITE_NAME"
STACK_NAME="$SITE_NAME"

if [ ! -d "$SITE_PATH" ]; then
    error "Site não encontrado: $SITE_PATH"
fi

log "Iniciando deploy de site estático: $SITE_NAME"

# 1. Validar estrutura
log "Validando estrutura..."
if [ ! -d "$SITE_PATH/dist" ] || [ -z "$(ls -A $SITE_PATH/dist)" ]; then
    error "Pasta dist/ vazia ou não encontrada. Build o site primeiro!"
fi

if [ ! -f "$SITE_PATH/docker-compose.yml" ]; then
    error "docker-compose.yml não encontrado"
fi

# 2. Criar pasta na VPS
log "Preparando VPS..."
ssh $VPS_HOST "mkdir -p $VPS_PATH/$SITE_NAME"

# 3. Enviar arquivos
log "Enviando arquivos estáticos..."
rsync -avz --delete \
    "$SITE_PATH/dist/" \
    "$VPS_HOST:$VPS_PATH/$SITE_NAME/dist/"

log "Enviando configurações..."
scp "$SITE_PATH/docker-compose.yml" "$VPS_HOST:$VPS_PATH/$SITE_NAME/"
scp "$SITE_PATH/nginx.conf" "$VPS_HOST:$VPS_PATH/$SITE_NAME/"

if [ -f "$SITE_PATH/.env" ]; then
    scp "$SITE_PATH/.env" "$VPS_HOST:$VPS_PATH/$SITE_NAME/"
fi

# 4. Deploy no Swarm
log "Deployando stack no Swarm..."
ssh $VPS_HOST "cd $VPS_PATH/$SITE_NAME && \
    docker stack deploy -c docker-compose.yml $STACK_NAME"

sleep 3

# 5. Verificar status
log "Verificando status..."
ssh $VPS_HOST "docker stack ps $STACK_NAME --no-trunc"

success "Deploy concluído!"
echo ""
echo "📊 Comandos úteis:"
echo "   Logs:     ./logs.sh $SITE_NAME"
echo "   Status:   ./manage.sh status $SITE_NAME"
echo "   Remove:   ./manage.sh remove $SITE_NAME"
echo ""

SUBDOMAIN=$(grep "^SUBDOMAIN=" "$SITE_PATH/.env" 2>/dev/null | cut -d'=' -f2 || echo "$SITE_NAME")

echo "🌐 Acesso: https://$SUBDOMAIN.$DOMAIN"
echo ""
warn "Aguarde 30-60s para o Traefik gerar o certificado SSL"
echo ""
echo "🔄 Para atualizar o site:"
echo "   1. Rebuild local: npm run build"
echo "   2. Copia: cp -r build/* $SITE_PATH/dist/"
echo "   3. Re-deploy: ./deploy-static.sh $SITE_NAME"
