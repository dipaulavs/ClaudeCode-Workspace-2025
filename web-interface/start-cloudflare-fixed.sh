#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║      🌍 Cloudflare Tunnel - Link Fixo Ativo! 🚀          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 URL Fixa: https://claude.loop9.com.br"
echo "📍 Apontando para: http://localhost:3000"
echo ""
echo "⚠️  IMPORTANTE: Mantenha este terminal aberto!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cloudflared tunnel run claude-workspace
