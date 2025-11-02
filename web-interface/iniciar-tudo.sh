#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                                                            ║${NC}"
echo -e "${PURPLE}║      🤖 Claude Code Workspace - Iniciando Tudo! 🚀        ║${NC}"
echo -e "${PURPLE}║                                                            ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Diretório base
DIR="$(cd "$(dirname "$0")" && pwd)"

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Encerrando todos os serviços...${NC}"
    pkill -f "python3 main.py"
    pkill -f "python3 server.py"
    pkill -f "ttyd"
    pkill -f "cloudflared tunnel run"
    echo -e "${GREEN}✅ Serviços encerrados!${NC}"
    exit
}

trap cleanup SIGINT SIGTERM

# Verificar e matar processos existentes
echo -e "${YELLOW}🧹 Limpando processos anteriores...${NC}"
pkill -f "python3 main.py" 2>/dev/null
pkill -f "python3 server.py" 2>/dev/null
pkill -f "ttyd" 2>/dev/null
sleep 2

# 1. Iniciar Backend API
echo -e "${BLUE}🔌 [1/4] Iniciando Backend API (porta 8000)...${NC}"
cd "$DIR/backend"
python3 main.py > /tmp/backend.log 2>&1 &
sleep 3

# 2. Iniciar Frontend Web
echo -e "${BLUE}🌐 [2/4] Iniciando Frontend Web (porta 3000)...${NC}"
cd "$DIR/frontend"
python3 server.py > /tmp/frontend.log 2>&1 &
sleep 3

# 3. Iniciar Terminal Web (ttyd)
if command -v ttyd &> /dev/null; then
    echo -e "${BLUE}💻 [3/4] Iniciando Terminal Web (porta 7681)...${NC}"
    cd "$DIR"
    bash start-terminal.sh > /tmp/ttyd.log 2>&1 &
    sleep 3
else
    echo -e "${YELLOW}⚠️  ttyd não instalado!${NC}"
    echo -e "${YELLOW}   Execute: brew install ttyd${NC}"
fi

# 4. Iniciar Cloudflare Tunnel
echo -e "${BLUE}🌍 [4/4] Iniciando Cloudflare Tunnel (acesso remoto)...${NC}"
cloudflared tunnel run claude-workspace > /tmp/cloudflare.log 2>&1 &
sleep 3

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║         ✅ TUDO PRONTO! Sistema 100% Online! 🎉           ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${PURPLE}📱 ACESSO LOCAL (seu Mac):${NC}"
echo ""
echo -e "   🎨 Dashboard:      ${BLUE}http://localhost:3000${NC}"
echo -e "   💬 Chat:           ${BLUE}http://localhost:3000/chat.html${NC}"
echo -e "   💻 Terminal:       ${BLUE}http://localhost:7681${NC}"
echo ""
echo -e "${PURPLE}🌍 ACESSO REMOTO (celular, outro computador):${NC}"
echo ""
echo -e "   🎨 Dashboard:      ${BLUE}https://claude.loop9.com.br${NC}"
echo -e "   💬 Chat:           ${BLUE}https://claude.loop9.com.br/chat.html${NC}"
echo -e "   💻 Terminal:       ${BLUE}https://terminal.loop9.com.br${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}⚠️  IMPORTANTE: Mantenha este terminal aberto!${NC}"
echo -e "${YELLOW}    Pressione Ctrl+C para encerrar tudo${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Mostrar logs em tempo real
echo -e "${PURPLE}📊 Logs em tempo real:${NC}"
echo ""
tail -f /tmp/backend.log /tmp/frontend.log /tmp/ttyd.log /tmp/cloudflare.log 2>/dev/null
