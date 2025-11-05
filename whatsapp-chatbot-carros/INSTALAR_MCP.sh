#!/bin/bash
# 🔧 INSTALAR MCP - Instala dependências do MCP Server

echo "🔧 Instalando MCP Server..."
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale primeiro."
    exit 1
fi

echo "✅ Python3: $(python3 --version)"
echo ""

# Instala dependências MCP
echo "📦 Instalando dependências MCP..."
cd mcp-server
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ MCP Server instalado com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Testar: python3 ../testar_sistema_hibrido.py"
    echo "   2. Usar no chatbot: Atualizar chatbot_automaia_v4.py"
    echo ""
else
    echo ""
    echo "❌ Erro na instalação. Verifique os logs acima."
    exit 1
fi
