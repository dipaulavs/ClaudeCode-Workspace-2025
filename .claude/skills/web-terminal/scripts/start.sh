#!/bin/bash
# Inicia terminal web completo (backend + frontend + ttyd + cloudflare)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_INTERFACE_DIR="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface"

echo "🚀 Iniciando Web Terminal..."

# Verificar se está no diretório correto
if [ ! -d "$WEB_INTERFACE_DIR" ]; then
    echo "❌ Erro: Diretório web-interface não encontrado em $WEB_INTERFACE_DIR"
    exit 1
fi

cd "$WEB_INTERFACE_DIR"

# Executar script de inicialização
if [ -f "./iniciar-tudo.sh" ]; then
    ./iniciar-tudo.sh
else
    echo "❌ Erro: Script iniciar-tudo.sh não encontrado"
    exit 1
fi
