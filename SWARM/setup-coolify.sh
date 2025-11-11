#!/bin/bash
# 🚀 Instalar Coolify na VPS
# Coolify = Netlify/Vercel self-hosted

set -e

VPS_HOST="root@82.25.68.132"

echo "🚀 Instalando Coolify na VPS..."
echo ""
echo "⚠️  ATENÇÃO:"
echo "   - Coolify vai usar a porta 8000 (padrão)"
echo "   - Configure Traefik depois para usar domínio"
echo "   - Acesse via: http://82.25.68.132:8000"
echo ""
read -p "Continuar? (s/N): " -r
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Cancelado."
    exit 0
fi

# Instalar Coolify
ssh $VPS_HOST 'curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash'

echo ""
echo "✅ Coolify instalado!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Acesse: http://82.25.68.132:8000"
echo "   2. Crie conta admin"
echo "   3. Configure GitHub/GitLab"
echo "   4. Deploy seu primeiro site!"
echo ""
echo "🌐 Para usar domínio (coolify.loop9.com.br):"
echo "   Configure no Traefik ou use Coolify Proxy"
echo ""
