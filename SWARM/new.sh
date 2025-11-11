#!/bin/bash
# 🐳 New Automation - Docker Swarm + Traefik
# Uso: ./new.sh <nome> [template] [subdominio]

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[NEW]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Validações
if [ -z "$1" ]; then
    echo "Uso: ./new.sh <nome-automacao> [template] [subdominio]"
    echo ""
    echo "Templates disponíveis:"
    ls -1 templates/ 2>/dev/null | sed 's/^/  - /'
    echo ""
    echo "Exemplos:"
    echo "  ./new.sh chatbot-vendas webhook-api chatbot"
    echo "  ./new.sh scraper-imoveis cronjob scraper"
    echo ""
    echo "Subdomínio será: <subdominio>.loop9.com.br"
    echo "Se não informar, usa o nome da automação"
    exit 1
fi

AUTOMATION_NAME="$1"
TEMPLATE="${2:-webhook-api}"
SUBDOMAIN="${3:-$AUTOMATION_NAME}"
TEMPLATE_PATH="templates/$TEMPLATE"
TARGET_PATH="automations/$AUTOMATION_NAME"

# Validar template
if [ ! -d "$TEMPLATE_PATH" ]; then
    echo "❌ Template não encontrado: $TEMPLATE"
    echo ""
    echo "Templates disponíveis:"
    ls -1 templates/ 2>/dev/null | sed 's/^/  - /'
    exit 1
fi

# Verificar se já existe
if [ -d "$TARGET_PATH" ]; then
    warn "Automação já existe: $AUTOMATION_NAME"
    echo -n "Sobrescrever? (s/N): "
    read -r response
    if [ "$response" != "s" ]; then
        echo "Cancelado."
        exit 0
    fi
    rm -rf "$TARGET_PATH"
fi

log "Criando nova automação: $AUTOMATION_NAME"
log "Template: $TEMPLATE"
log "Subdomínio: $SUBDOMAIN.loop9.com.br"

# Copiar template
cp -r "$TEMPLATE_PATH" "$TARGET_PATH"

# Configurar .env
if [ -f "$TARGET_PATH/.env.example" ]; then
    cp "$TARGET_PATH/.env.example" "$TARGET_PATH/.env"

    # Substituir variáveis
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/AUTOMATION_NAME=.*/AUTOMATION_NAME=$AUTOMATION_NAME/" "$TARGET_PATH/.env"
        sed -i '' "s/SUBDOMAIN=.*/SUBDOMAIN=$SUBDOMAIN/" "$TARGET_PATH/.env"
    else
        sed -i "s/AUTOMATION_NAME=.*/AUTOMATION_NAME=$AUTOMATION_NAME/" "$TARGET_PATH/.env"
        sed -i "s/SUBDOMAIN=.*/SUBDOMAIN=$SUBDOMAIN/" "$TARGET_PATH/.env"
    fi
fi

# Substituir variáveis no docker-compose.yml
if [ -f "$TARGET_PATH/docker-compose.yml" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/AUTOMATION_NAME/$AUTOMATION_NAME/g" "$TARGET_PATH/docker-compose.yml"
        sed -i '' "s/SUBDOMAIN/$SUBDOMAIN/g" "$TARGET_PATH/docker-compose.yml"
    else
        sed -i "s/AUTOMATION_NAME/$AUTOMATION_NAME/g" "$TARGET_PATH/docker-compose.yml"
        sed -i "s/SUBDOMAIN/$SUBDOMAIN/g" "$TARGET_PATH/docker-compose.yml"
    fi
fi

# Criar pastas necessárias
mkdir -p "$TARGET_PATH/data"
mkdir -p "$TARGET_PATH/logs"

success "Automação criada: $TARGET_PATH"
echo ""
echo "📝 Próximos passos:"
echo "   1. Edite os arquivos em: $TARGET_PATH"
echo "   2. Configure variáveis em: $TARGET_PATH/.env"
echo "   3. Teste localmente (opcional)"
echo "   4. Deploy: ./deploy.sh $AUTOMATION_NAME"
echo ""
echo "🌐 URL final: https://$SUBDOMAIN.loop9.com.br"
echo ""
echo "💡 Dica: Use Claude Code para desenvolver a automação!"
