#!/bin/bash

echo "════════════════════════════════════════════════"
echo "   🚀 Setup da Interface Web"
echo "════════════════════════════════════════════════"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Instalar dependências Python do backend
echo -e "${BLUE}📦 Instalando dependências do backend...${NC}"
pip3 install --user -r backend/requirements.txt

# 2. Instalar ttyd para terminal web
echo ""
echo -e "${BLUE}💻 Instalando ttyd (terminal web)...${NC}"
if ! command -v ttyd &> /dev/null; then
    if command -v brew &> /dev/null; then
        brew install ttyd
    else
        echo -e "${YELLOW}⚠️  Homebrew não encontrado. Por favor, instale manualmente:${NC}"
        echo "   brew install ttyd"
        echo "   ou visite: https://github.com/tsl0922/ttyd"
    fi
else
    echo -e "${GREEN}✓ ttyd já está instalado${NC}"
fi

# 3. Instalar Cloudflare Tunnel (cloudflared)
echo ""
echo -e "${BLUE}🌐 Instalando Cloudflare Tunnel...${NC}"
if ! command -v cloudflared &> /dev/null; then
    if command -v brew &> /dev/null; then
        brew install cloudflare/cloudflare/cloudflared
    else
        echo -e "${YELLOW}⚠️  Homebrew não encontrado. Por favor, instale manualmente:${NC}"
        echo "   brew install cloudflare/cloudflare/cloudflared"
    fi
else
    echo -e "${GREEN}✓ cloudflared já está instalado${NC}"
fi

# 4. Dar permissão de execução aos scripts
echo ""
echo -e "${BLUE}🔧 Configurando permissões...${NC}"
chmod +x backend/main.py
chmod +x frontend/server.py
chmod +x start.sh
chmod +x start-terminal.sh
chmod +x start-all.sh

echo ""
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✨ Setup concluído!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo ""
echo "📝 Próximos passos:"
echo ""
echo "1. Iniciar a interface web:"
echo "   ${BLUE}bash start-all.sh${NC}"
echo ""
echo "2. Acessar no navegador:"
echo "   ${BLUE}http://localhost:3000${NC} - Interface web"
echo "   ${BLUE}http://localhost:7681${NC} - Terminal Claude Code"
echo ""
echo "3. Para acesso remoto (celular):"
echo "   ${BLUE}bash start-cloudflare.sh${NC}"
echo ""
