#!/bin/bash
# 🚀 Deploy Script - Docker Swarm + Traefik
# Uso: ./deploy.sh <nome-automacao>

set -e

# Configurações
VPS_HOST="root@82.25.68.132"
VPS_PATH="/root/swarm-automations"
LOCAL_AUTOMATIONS="./automations"
DOMAIN="loop9.com.br"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Funções
log() { echo -e "${BLUE}[DEPLOY]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# Validações
if [ -z "$1" ]; then
    error "Uso: ./deploy.sh <nome-automacao>"
fi

AUTOMATION_NAME="$1"
AUTOMATION_PATH="$LOCAL_AUTOMATIONS/$AUTOMATION_NAME"
STACK_NAME="$AUTOMATION_NAME"

if [ ! -d "$AUTOMATION_PATH" ]; then
    error "Automação não encontrada: $AUTOMATION_PATH"
fi

log "Iniciando deploy de: $AUTOMATION_NAME"

# 1. Validar estrutura
log "Validando estrutura..."
if [ ! -f "$AUTOMATION_PATH/docker-compose.yml" ]; then
    error "docker-compose.yml não encontrado em $AUTOMATION_PATH"
fi

if [ ! -f "$AUTOMATION_PATH/Dockerfile" ]; then
    error "Dockerfile não encontrado em $AUTOMATION_PATH"
fi

# 2. Build da imagem Docker localmente
log "Buildando imagem Docker..."
cd "$AUTOMATION_PATH"
docker build -t "loop9/$AUTOMATION_NAME:latest" . || error "Falha no build da imagem"
cd - > /dev/null

# 3. Criar pasta na VPS
log "Preparando VPS..."
ssh $VPS_HOST "mkdir -p $VPS_PATH/$AUTOMATION_NAME" || error "Falha ao criar pasta na VPS"

# 4. Salvar imagem e enviar para VPS
log "Enviando imagem para VPS..."
docker save "loop9/$AUTOMATION_NAME:latest" | ssh $VPS_HOST "docker load" || error "Falha ao enviar imagem"

# 5. Enviar docker-compose.yml e .env
log "Enviando configurações..."
scp "$AUTOMATION_PATH/docker-compose.yml" "$VPS_HOST:$VPS_PATH/$AUTOMATION_NAME/" || error "Falha ao enviar docker-compose"
if [ -f "$AUTOMATION_PATH/.env" ]; then
    scp "$AUTOMATION_PATH/.env" "$VPS_HOST:$VPS_PATH/$AUTOMATION_NAME/" || error "Falha ao enviar .env"
fi

# 6. Deploy no Swarm
log "Deployando stack no Swarm..."
ssh $VPS_HOST "cd $VPS_PATH/$AUTOMATION_NAME && \
    docker stack deploy -c docker-compose.yml $STACK_NAME" || error "Falha ao deployar stack"

# 7. Aguardar deploy
sleep 5

# 8. Verificar status
log "Verificando status..."
ssh $VPS_HOST "docker stack ps $STACK_NAME --no-trunc"

success "Deploy concluído!"
echo ""
echo "📊 Comandos úteis:"
echo "   Logs:     ./logs.sh $AUTOMATION_NAME"
echo "   Status:   ./manage.sh status $AUTOMATION_NAME"
echo "   Remove:   ./manage.sh remove $AUTOMATION_NAME"
echo "   List:     ./manage.sh list"
echo ""

# Pegar subdomínio do .env
SUBDOMAIN=$(grep "^SUBDOMAIN=" "$AUTOMATION_PATH/.env" 2>/dev/null | cut -d'=' -f2 || echo "$AUTOMATION_NAME")

echo "🌐 Acesso: https://$SUBDOMAIN.$DOMAIN"
echo ""
warn "Aguarde 30-60s para o Traefik gerar o certificado SSL"
