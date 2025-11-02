#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "════════════════════════════════════════════════"
echo "   🌍 Cloudflare Tunnel - Acesso Remoto"
echo "════════════════════════════════════════════════"
echo ""

# Verificar se cloudflared está instalado
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}❌ cloudflared não está instalado!${NC}"
    echo ""
    echo "Instale com:"
    echo -e "  ${BLUE}brew install cloudflare/cloudflare/cloudflared${NC}"
    echo "  ou execute: ${BLUE}bash setup.sh${NC}"
    exit 1
fi

# Verificar se os serviços estão rodando
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Frontend não está rodando!${NC}"
    echo -e "${YELLOW}   Execute primeiro: bash start-all.sh${NC}"
    echo ""
fi

if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Backend não está rodando!${NC}"
    echo -e "${YELLOW}   Execute primeiro: bash start-all.sh${NC}"
    echo ""
fi

# Criar arquivo de configuração temporário
CONFIG_FILE="/tmp/cloudflare-tunnel-config.yml"

cat > "$CONFIG_FILE" << EOF
ingress:
  - service: http://localhost:3000
EOF

echo -e "${BLUE}🚀 Iniciando Cloudflare Tunnel...${NC}"
echo ""
echo -e "${GREEN}Aguarde alguns segundos para obter a URL pública...${NC}"
echo ""

# Iniciar túnel
cloudflared tunnel --config "$CONFIG_FILE" --url http://localhost:3000

# Nota: O comando acima irá gerar uma URL temporária tipo:
# https://xxxxx.trycloudflare.com
# Essa URL será válida enquanto o túnel estiver ativo
