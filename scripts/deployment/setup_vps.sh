#!/bin/bash
# Claude Code Workspace - Setup VPS
# Configura workspace remoto na VPS
# Uso: bash setup_vps.sh

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

VPS_HOST="root@82.25.68.132"
VPS_PATH="/root/claude-workspace"

echo -e "${BLUE}🚀 Configurando Claude Workspace na VPS${NC}"
echo ""

# 1. Criar diretórios necessários
echo -e "${BLUE}==>${NC} Criando estrutura de diretórios..."
ssh $VPS_HOST "cd $VPS_PATH && mkdir -p logs tmp backups"

# 2. Configurar Git
echo -e "${BLUE}==>${NC} Configurando Git..."
ssh $VPS_HOST "cd $VPS_PATH && git config user.name 'Claude VPS' && git config user.email 'claude@loop9.com.br'"

# 3. Criar script de sync automático (simplificado para VPS)
echo -e "${BLUE}==>${NC} Criando script de pull automático..."
ssh $VPS_HOST "cat > $VPS_PATH/scripts/deployment/auto_pull.sh << 'EOF'
#!/bin/bash
# Auto-pull do GitHub
cd /root/claude-workspace
git pull origin main >> /root/claude-workspace/logs/sync.log 2>&1
echo \"[$(date)] Sync completo\" >> /root/claude-workspace/logs/sync.log
EOF"

ssh $VPS_HOST "chmod +x $VPS_PATH/scripts/deployment/auto_pull.sh"

# 4. Configurar cronjob (sync a cada 15 minutos)
echo -e "${BLUE}==>${NC} Configurando cronjob para sync automático..."
ssh $VPS_HOST "crontab -l 2>/dev/null | grep -v 'claude-workspace/scripts/deployment/auto_pull.sh' > /tmp/cron_tmp || true"
ssh $VPS_HOST "echo '*/15 * * * * /root/claude-workspace/scripts/deployment/auto_pull.sh' >> /tmp/cron_tmp"
ssh $VPS_HOST "crontab /tmp/cron_tmp && rm /tmp/cron_tmp"

# 5. Criar arquivo de environment variables
echo -e "${BLUE}==>${NC} Criando arquivo de environment..."
ssh $VPS_HOST "cat > $VPS_PATH/.env.vps << 'EOF'
# Claude Workspace VPS Environment
WORKSPACE_PATH=/root/claude-workspace
NODE_ENV=production
PYTHONUNBUFFERED=1
TZ=America/Sao_Paulo
EOF"

# 6. Testar sync
echo -e "${BLUE}==>${NC} Testando sync inicial..."
ssh $VPS_HOST "$VPS_PATH/scripts/deployment/auto_pull.sh"

echo ""
echo -e "${GREEN}✅ Setup VPS completo!${NC}"
echo ""
echo "📍 Configurações:"
echo "   Workspace: $VPS_PATH"
echo "   Sync: A cada 15 minutos (cronjob)"
echo "   Logs: $VPS_PATH/logs/sync.log"
echo ""
echo "🔧 Comandos úteis:"
echo "   ssh $VPS_HOST 'cd $VPS_PATH && git status'"
echo "   ssh $VPS_HOST 'tail -f $VPS_PATH/logs/sync.log'"
echo ""
