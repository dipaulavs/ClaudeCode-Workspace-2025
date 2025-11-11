#!/bin/bash
# Claude Code Workspace - Script de Sincronização Git Automática
# Autor: Claude Code + Felipe
# Data: 2025-11-11
# Descrição: Sincroniza workspace local com GitHub e VPS

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configurações
WORKSPACE_DIR="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"
REPO_NAME="claude-workspace"
GITHUB_USER="dipaulavs"
VPS_HOST="root@82.25.68.132"
VPS_PATH="/root/claude-workspace"

# Funções
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Verificar se está no diretório correto
if [ "$PWD" != "$WORKSPACE_DIR" ]; then
    print_step "Mudando para diretório do workspace..."
    cd "$WORKSPACE_DIR"
fi

# Verificar status do Git
print_step "Verificando status do Git..."
git status --short

# Perguntar mensagem de commit
if [ -z "$1" ]; then
    echo ""
    read -p "💬 Mensagem do commit (Enter para 'sync workspace'): " COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"sync workspace"}
else
    COMMIT_MSG="$1"
fi

# Adicionar mudanças
print_step "Adicionando mudanças ao Git..."
git add .

# Verificar se há mudanças
if git diff --staged --quiet; then
    print_warning "Nenhuma mudança para commitar"
else
    # Fazer commit
    print_step "Criando commit: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
    print_success "Commit criado"
fi

# Push para GitHub
print_step "Enviando para GitHub..."
if git push origin main; then
    print_success "Push para GitHub completo"
else
    print_error "Erro no push para GitHub"
    exit 1
fi

# Sincronizar com VPS (se estiver configurado)
print_step "Sincronizando com VPS..."
if ssh "$VPS_HOST" "[ -d $VPS_PATH ]"; then
    ssh "$VPS_HOST" "cd $VPS_PATH && git pull origin main"
    print_success "VPS sincronizado"
else
    print_warning "VPS ainda não configurado (será feito na Fase 2)"
fi

echo ""
print_success "🎉 Sincronização completa!"
echo ""
echo "📍 Status:"
echo "   Local:  $WORKSPACE_DIR"
echo "   GitHub: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "   VPS:    $VPS_HOST:$VPS_PATH"
