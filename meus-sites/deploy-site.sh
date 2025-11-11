#!/bin/bash
# 🚀 Deploy de Sites - Sistema Meta-Config
# Uso: ./deploy-site.sh casanova

set -e

VPS_HOST="root@82.25.68.132"
VPS_PATH="/root/swarm-sites"
CONFIGS_DIR="$HOME/meus-sites/configs"
SWARM_DIR="$HOME/Desktop/ClaudeCode-Workspace/SWARM"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[DEPLOY]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

if [ -z "$1" ]; then
    error "Uso: ./deploy-site.sh <nome-do-site>\n   Exemplo: ./deploy-site.sh casanova"
fi

SITE_NAME="$1"
CONFIG_FILE="$CONFIGS_DIR/${SITE_NAME}.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    error "Config não encontrada: $CONFIG_FILE\n   Crie o arquivo primeiro!"
fi

log "Lendo config: $CONFIG_FILE"

# Ler YAML (simples parser)
DOMINIO=$(grep "^dominio:" "$CONFIG_FILE" | sed 's/dominio: *//' | tr -d '"' | tr -d "'")
PROJETO=$(grep "^projeto:" "$CONFIG_FILE" | sed 's/projeto: *//' | tr -d '"' | tr -d "'" | sed "s|~|$HOME|")
BUILD_CMD=$(grep "^build:" "$CONFIG_FILE" | sed 's/build: *//')
PASTA_BUILD=$(grep "^pasta_build:" "$CONFIG_FILE" | sed 's/pasta_build: *//' | tr -d '"' | tr -d "'")
WWW=$(grep "^www:" "$CONFIG_FILE" | sed 's/www: *//' | tr -d '"' | tr -d "'")

if [ -z "$DOMINIO" ] || [ -z "$PROJETO" ] || [ -z "$BUILD_CMD" ] || [ -z "$PASTA_BUILD" ]; then
    error "Config incompleta! Verifique:\n   - dominio\n   - projeto\n   - build\n   - pasta_build"
fi

log "Site: $SITE_NAME"
log "Domínio: $DOMINIO"
log "Projeto: $PROJETO"

# 0. Configurar DNS automaticamente (se for subdomínio loop9.com.br)
if [[ "$DOMINIO" == *.loop9.com.br ]]; then
    log "Detectado subdomínio loop9.com.br - Configurando DNS..."

    CF_SCRIPT="$HOME/meus-sites/cloudflare-dns.sh"
    if [ -f "$CF_SCRIPT" ]; then
        # Adicionar DNS via Cloudflare API
        "$CF_SCRIPT" add "$DOMINIO" || log "DNS já existe ou falhou (continuando...)"

        # Se www=true, adicionar também o www
        if [ "$WWW" = "true" ]; then
            "$CF_SCRIPT" add "www.$DOMINIO" || log "DNS www já existe ou falhou (continuando...)"
        fi

        success "DNS configurado!"
        log "Aguardando 5s para propagação..."
        sleep 5
    else
        log "Script cloudflare-dns.sh não encontrado - pulando configuração DNS"
    fi
fi

# 1. Build local
log "Executando build..."
cd "$PROJETO" || error "Pasta do projeto não encontrada: $PROJETO"
eval "$BUILD_CMD" || error "Build falhou!"

BUILD_PATH="$PROJETO/$PASTA_BUILD"
if [ ! -d "$BUILD_PATH" ]; then
    error "Pasta de build não encontrada: $BUILD_PATH"
fi

# 2. Preparar estrutura no SWARM
SWARM_SITE="$SWARM_DIR/automations/$SITE_NAME"
log "Criando estrutura SWARM..."
mkdir -p "$SWARM_SITE/dist"

# 3. Copiar build
log "Copiando build para SWARM..."
rsync -a --delete "$BUILD_PATH/" "$SWARM_SITE/dist/"

# 4. Criar docker-compose.yml
log "Gerando docker-compose.yml..."
HOST_RULE="Host(\`$DOMINIO\`)"
if [ "$WWW" = "true" ]; then
    HOST_RULE="Host(\`$DOMINIO\`) || Host(\`www.$DOMINIO\`)"
fi

cat > "$SWARM_SITE/docker-compose.yml" << EOF
version: '3.8'

services:
  web:
    image: nginx:alpine
    volumes:
      - ./dist:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - loop9Net
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.${SITE_NAME}-http.rule=$HOST_RULE"
        - "traefik.http.routers.${SITE_NAME}-http.entrypoints=web"
        - "traefik.http.routers.${SITE_NAME}-http.middlewares=redirect-to-https"
        - "traefik.http.routers.${SITE_NAME}.rule=$HOST_RULE"
        - "traefik.http.routers.${SITE_NAME}.entrypoints=websecure"
        - "traefik.http.routers.${SITE_NAME}.tls.certresolver=letsencrypt"
        - "traefik.http.services.${SITE_NAME}.loadbalancer.server.port=80"
        - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"
        - "traefik.http.middlewares.redirect-to-https.redirectscheme.permanent=true"

networks:
  loop9Net:
    external: true
EOF

# 5. Copiar nginx.conf
if [ ! -f "$SWARM_SITE/nginx.conf" ]; then
    log "Copiando nginx.conf..."
    cp "$SWARM_DIR/templates/static-site/nginx.conf" "$SWARM_SITE/nginx.conf"
fi

# 6. Deploy na VPS
log "Enviando para VPS..."
ssh "$VPS_HOST" "mkdir -p $VPS_PATH/$SITE_NAME"

rsync -avz --delete \
    "$SWARM_SITE/dist/" \
    "$VPS_HOST:$VPS_PATH/$SITE_NAME/dist/"

scp "$SWARM_SITE/docker-compose.yml" "$VPS_HOST:$VPS_PATH/$SITE_NAME/"
scp "$SWARM_SITE/nginx.conf" "$VPS_HOST:$VPS_PATH/$SITE_NAME/"

# 7. Deploy stack
log "Deployando stack no Swarm..."
ssh "$VPS_HOST" "cd $VPS_PATH/$SITE_NAME && docker stack deploy -c docker-compose.yml $SITE_NAME"

sleep 2

success "Deploy concluído!"
echo ""
echo "🌐 Acesso: https://$DOMINIO"
echo "⚠️  Aguarde 30-60s para SSL (Let's Encrypt)"
echo ""
echo "📊 Comandos:"
echo "   Logs: ssh $VPS_HOST 'docker service logs ${SITE_NAME}_web -f'"
echo "   Status: ssh $VPS_HOST 'docker stack ps $SITE_NAME'"
