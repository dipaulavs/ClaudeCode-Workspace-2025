#!/bin/bash
# Script de instalação do MCP Nextcloud Upload

set -e

echo "📦 Instalando MCP Nextcloud Upload..."
echo ""

# 1. Instalar dependências
echo "1️⃣ Instalando dependências..."
pip3 install -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# 2. Criar pasta local de upload
UPLOAD_DIR="$HOME/Pictures/upload"
if [ ! -d "$UPLOAD_DIR" ]; then
    echo "2️⃣ Criando pasta de upload..."
    mkdir -p "$UPLOAD_DIR"
    echo "✅ Pasta criada: $UPLOAD_DIR"
else
    echo "2️⃣ Pasta de upload já existe: $UPLOAD_DIR"
fi
echo ""

# 3. Obter caminho absoluto do server
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_PATH="$SCRIPT_DIR/server.py"

echo "3️⃣ Configuração do Claude Desktop"
echo ""
echo "Adicione ao ~/.claude_desktop_config.json:"
echo ""
echo '{'
echo '  "mcpServers": {'
echo '    "nextcloud-upload": {'
echo '      "command": "python3",'
echo '      "args": ['
echo "        \"$SERVER_PATH\""
echo '      ]'
echo '    }'
echo '  }'
echo '}'
echo ""
echo "⚠️  IMPORTANTE: Use o caminho absoluto acima!"
echo ""

# 4. Verificar config do Nextcloud
CONFIG_FILE="$SCRIPT_DIR/../config/nextcloud_config.py"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Config do Nextcloud encontrado"
else
    echo "⚠️  Config do Nextcloud não encontrado em: $CONFIG_FILE"
fi
echo ""

echo "🎉 Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Adicionar configuração ao ~/.claude_desktop_config.json"
echo "2. Reiniciar Claude Desktop completamente"
echo "3. Testar com: \"Escaneia a pasta de upload\""
echo ""
