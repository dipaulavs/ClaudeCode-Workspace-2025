#!/bin/bash
# Para todos os serviços do terminal web

echo "🛑 Parando Web Terminal..."

# Matar processos
pkill -f "python3.*main.py" 2>/dev/null && echo "✅ Backend parado"
pkill -f "python3.*server.py" 2>/dev/null && echo "✅ Frontend parado"
pkill ttyd 2>/dev/null && echo "✅ Terminal parado"
pkill cloudflared 2>/dev/null && echo "✅ Cloudflare parado"

echo "✅ Todos os serviços foram parados"
