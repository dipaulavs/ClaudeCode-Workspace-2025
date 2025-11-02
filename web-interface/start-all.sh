#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "════════════════════════════════════════════════"
echo "   🤖 Claude Code Workspace - Interface Web"
echo "════════════════════════════════════════════════"
echo ""

# Diretório base
DIR="$(cd "$(dirname "$0")" && pwd)"

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Encerrando todos os serviços...${NC}"
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo -e "${BLUE}🚀 Iniciando Backend API (porta 8000)...${NC}"
cd "$DIR/backend"
python3 main.py > /tmp/claude-backend.log 2>&1 &
BACKEND_PID=$!

sleep 2

# Iniciar Frontend
echo -e "${BLUE}🌐 Iniciando Frontend Web (porta 3000)...${NC}"
cd "$DIR/frontend"
python3 server.py > /tmp/claude-frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 2

# Iniciar Terminal Web (se ttyd estiver instalado)
if command -v ttyd &> /dev/null; then
    echo -e "${BLUE}💻 Iniciando Terminal Web (porta 7681)...${NC}"
    ttyd -W -p 7681 -t fontSize=16 -t theme='{"background":"#1e1e1e","foreground":"#d4d4d4"}' bash > /tmp/claude-terminal.log 2>&1 &
    TERMINAL_PID=$!
else
    echo -e "${YELLOW}⚠️  ttyd não instalado. Terminal web não será iniciado.${NC}"
    echo -e "${YELLOW}   Execute 'bash setup.sh' para instalar.${NC}"
fi

sleep 2

echo ""
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ Todos os serviços foram iniciados!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo ""
echo "📱 Acesse no navegador:"
echo ""
echo -e "   🎨 Interface Web:     ${BLUE}http://localhost:3000${NC}"
echo -e "   💻 Terminal Claude:   ${BLUE}http://localhost:7681${NC}"
echo -e "   🔌 API Backend:       ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo "🌍 Para acesso remoto (celular), abra outro terminal e execute:"
echo -e "   ${BLUE}cd web-interface && bash start-cloudflare.sh${NC}"
echo ""
echo -e "${YELLOW}Pressione Ctrl+C para encerrar todos os serviços${NC}"
echo ""

# Logs em tempo real
echo "📊 Logs:"
tail -f /tmp/claude-backend.log /tmp/claude-frontend.log /tmp/claude-terminal.log 2>/dev/null &

# Manter o script rodando
wait
