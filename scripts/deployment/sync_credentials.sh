#!/bin/bash
# Claude Code Workspace - Sincronizar Credenciais para VPS
# Autor: Claude Code + Felipe
# Data: 2025-11-11
# Descrição: Sincroniza arquivo de credenciais local com VPS de forma segura

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configurações
LOCAL_CREDS="config/CREDENCIAIS.env"
VPS_HOST="root@82.25.68.132"
VPS_PATH="/root/claude-workspace/config/CREDENCIAIS.env"
WORKSPACE_DIR="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"

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

echo -e "${BLUE}🔐 Sincronizando Credenciais para VPS${NC}"
echo ""

# Verificar se está no workspace
if [ "$PWD" != "$WORKSPACE_DIR" ]; then
    print_step "Mudando para diretório do workspace..."
    cd "$WORKSPACE_DIR"
fi

# Verificar se arquivo existe
if [ ! -f "$LOCAL_CREDS" ]; then
    print_error "Arquivo $LOCAL_CREDS não encontrado!"
    exit 1
fi

# Criar backup na VPS antes de sobrescrever
print_step "Criando backup das credenciais antigas na VPS..."
ssh $VPS_HOST "[ -f $VPS_PATH ] && cp $VPS_PATH ${VPS_PATH}.backup.$(date +%Y%m%d_%H%M%S) || true"

# Copiar arquivo para VPS
print_step "Copiando credenciais para VPS..."
scp "$LOCAL_CREDS" "$VPS_HOST:$VPS_PATH"

# Configurar permissões (somente root pode ler)
print_step "Configurando permissões de segurança..."
ssh $VPS_HOST "chmod 600 $VPS_PATH"

# Verificar se copiou corretamente
print_step "Verificando integridade..."
LOCAL_SIZE=$(wc -c < "$LOCAL_CREDS" | tr -d ' ')
REMOTE_SIZE=$(ssh $VPS_HOST "wc -c < $VPS_PATH" | tr -d ' ')

if [ "$LOCAL_SIZE" == "$REMOTE_SIZE" ]; then
    print_success "Arquivo copiado com sucesso! ($LOCAL_SIZE bytes)"
else
    print_error "Tamanhos diferentes! Local: $LOCAL_SIZE | Remoto: $REMOTE_SIZE"
    exit 1
fi

echo ""
print_success "🎉 Credenciais sincronizadas com sucesso!"
echo ""
echo "📍 Localização VPS: $VPS_PATH"
echo "🔒 Permissões: 600 (somente root)"
echo ""
echo "💡 Para usar em scripts na VPS:"
echo "   source /root/claude-workspace/config/CREDENCIAIS.env"
echo ""
