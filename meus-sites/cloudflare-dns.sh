#!/bin/bash
# 🌐 Gerenciador de DNS via Cloudflare API
# Uso: ./cloudflare-dns.sh add testesite.loop9.com.br
#      ./cloudflare-dns.sh list loop9.com.br
#      ./cloudflare-dns.sh delete testesite.loop9.com.br

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[CLOUDFLARE]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Arquivo de configuração
CONFIG_FILE="$HOME/.cloudflare-credentials"

# Função para configurar credenciais
setup_credentials() {
    echo ""
    warn "Credenciais da Cloudflare não encontradas!"
    echo ""
    echo "Para obter suas credenciais:"
    echo "1. Acesse: https://dash.cloudflare.com/profile/api-tokens"
    echo "2. Clique em 'Create Token'"
    echo "3. Use o template 'Edit zone DNS'"
    echo "4. Ou use sua Global API Key (menos seguro)"
    echo ""

    read -p "Email da Cloudflare: " CF_EMAIL
    read -p "API Token ou Global API Key: " CF_API_KEY

    echo "CF_EMAIL=\"$CF_EMAIL\"" > "$CONFIG_FILE"
    echo "CF_API_KEY=\"$CF_API_KEY\"" >> "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"

    success "Credenciais salvas em $CONFIG_FILE"
    echo ""
}

# Carregar credenciais
if [ ! -f "$CONFIG_FILE" ]; then
    setup_credentials
fi

source "$CONFIG_FILE"

if [ -z "$CF_EMAIL" ] || [ -z "$CF_API_KEY" ]; then
    error "Credenciais inválidas! Delete $CONFIG_FILE e rode novamente."
fi

VPS_IP="82.25.68.132"

# Função para obter Zone ID
get_zone_id() {
    local domain=$1

    log "Buscando Zone ID para $domain..."

    response=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$domain" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json")

    zone_id=$(echo $response | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

    if [ -z "$zone_id" ]; then
        error "Domínio $domain não encontrado na Cloudflare!\nVerifique se o domínio está adicionado na sua conta."
    fi

    echo $zone_id
}

# Função para adicionar registro DNS
add_record() {
    local full_domain=$1

    # Extrair domínio base e subdomínio
    # Ex: testesite.loop9.com.br -> subdomain=testesite, domain=loop9.com.br
    if [[ $full_domain =~ ^([^.]+)\.(.+)$ ]]; then
        subdomain="${BASH_REMATCH[1]}"
        base_domain="${BASH_REMATCH[2]}"
    else
        error "Formato inválido! Use: subdominio.dominio.com.br"
    fi

    log "Subdomínio: $subdomain"
    log "Domínio base: $base_domain"

    zone_id=$(get_zone_id "$base_domain")
    log "Zone ID: $zone_id"

    # Verificar se já existe
    log "Verificando se registro já existe..."
    existing=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records?name=$full_domain" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json")

    record_id=$(echo $existing | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

    if [ ! -z "$record_id" ]; then
        warn "Registro já existe! Atualizando..."

        response=$(curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records/$record_id" \
            -H "X-Auth-Email: $CF_EMAIL" \
            -H "X-Auth-Key: $CF_API_KEY" \
            -H "Content-Type: application/json" \
            --data "{\"type\":\"A\",\"name\":\"$full_domain\",\"content\":\"$VPS_IP\",\"ttl\":300,\"proxied\":false}")
    else
        log "Criando novo registro DNS..."

        response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records" \
            -H "X-Auth-Email: $CF_EMAIL" \
            -H "X-Auth-Key: $CF_API_KEY" \
            -H "Content-Type: application/json" \
            --data "{\"type\":\"A\",\"name\":\"$full_domain\",\"content\":\"$VPS_IP\",\"ttl\":300,\"proxied\":false}")
    fi

    # Verificar sucesso
    if echo $response | grep -q '"success":true'; then
        success "Registro DNS criado/atualizado!"
        echo ""
        echo "📋 Detalhes:"
        echo "   Tipo: A"
        echo "   Nome: $full_domain"
        echo "   IP: $VPS_IP"
        echo "   TTL: 300s (5 min)"
        echo "   Proxy: Desativado (DNS only)"
        echo ""
        success "DNS configurado! Aguarde 1-5 minutos para propagação."
    else
        error=$(echo $response | grep -o '"message":"[^"]*' | cut -d'"' -f4)
        error "Falha ao criar registro: $error"
    fi
}

# Função para listar registros
list_records() {
    local domain=$1

    zone_id=$(get_zone_id "$domain")

    log "Listando registros DNS de $domain..."
    echo ""

    response=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json")

    echo $response | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data['success']:
    for record in data['result']:
        print(f\"{record['type']:6} {record['name']:40} -> {record['content']:20} (TTL: {record['ttl']})\")
else:
    print('Erro ao listar registros')
" 2>/dev/null || echo "$response" | grep -o '"name":"[^"]*","type":"[^"]*","content":"[^"]*' | sed 's/"name":"//g' | sed 's/","type":"/ - /g' | sed 's/","content":"/ -> /g'
}

# Função para deletar registro
delete_record() {
    local full_domain=$1

    # Extrair domínio base
    if [[ $full_domain =~ ^([^.]+)\.(.+)$ ]]; then
        base_domain="${BASH_REMATCH[2]}"
    else
        error "Formato inválido!"
    fi

    zone_id=$(get_zone_id "$base_domain")

    # Buscar ID do registro
    log "Buscando registro $full_domain..."
    existing=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records?name=$full_domain" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json")

    record_id=$(echo $existing | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

    if [ -z "$record_id" ]; then
        error "Registro não encontrado!"
    fi

    log "Deletando registro..."
    response=$(curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records/$record_id" \
        -H "X-Auth-Email: $CF_EMAIL" \
        -H "X-Auth-Key: $CF_API_KEY" \
        -H "Content-Type: application/json")

    if echo $response | grep -q '"success":true'; then
        success "Registro deletado: $full_domain"
    else
        error "Falha ao deletar registro"
    fi
}

# Menu principal
case "$1" in
    add)
        if [ -z "$2" ]; then
            error "Uso: $0 add subdominio.dominio.com.br"
        fi
        add_record "$2"
        ;;
    list)
        if [ -z "$2" ]; then
            error "Uso: $0 list dominio.com.br"
        fi
        list_records "$2"
        ;;
    delete)
        if [ -z "$2" ]; then
            error "Uso: $0 delete subdominio.dominio.com.br"
        fi
        delete_record "$2"
        ;;
    *)
        echo "🌐 Gerenciador de DNS Cloudflare"
        echo ""
        echo "Uso:"
        echo "  $0 add <subdominio.dominio.com.br>    - Adicionar/atualizar registro DNS"
        echo "  $0 list <dominio.com.br>              - Listar todos os registros"
        echo "  $0 delete <subdominio.dominio.com.br> - Deletar registro"
        echo ""
        echo "Exemplos:"
        echo "  $0 add testesite.loop9.com.br"
        echo "  $0 list loop9.com.br"
        echo "  $0 delete testesite.loop9.com.br"
        exit 1
        ;;
esac
