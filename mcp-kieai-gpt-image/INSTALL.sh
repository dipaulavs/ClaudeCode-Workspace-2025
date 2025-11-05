#!/bin/bash

echo "================================================"
echo "🎨 Instalando MCP Server KIE.AI"
echo "================================================"

# Detecta Python 3.10+
PYTHON_CMD=""

if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v /opt/homebrew/bin/python3.11 &> /dev/null; then
    PYTHON_CMD="/opt/homebrew/bin/python3.11"
else
    echo "❌ Python 3.10+ não encontrado!"
    echo ""
    echo "Instale Python 3.11+ e tente novamente:"
    echo "  brew install python@3.11"
    exit 1
fi

echo "✅ Python encontrado: $PYTHON_CMD"
echo ""

# Verifica versão
VERSION=$($PYTHON_CMD --version | cut -d ' ' -f 2)
echo "📦 Versão: $VERSION"

# Instala dependências
echo ""
echo "📥 Instalando dependências..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Instalação concluída!"
    echo "================================================"
    echo ""
    echo "🧪 Para testar, execute:"
    echo "   $PYTHON_CMD test_simple.py"
    echo ""
    echo "🚀 Para teste completo com geração de imagem:"
    echo "   $PYTHON_CMD test_client.py"
    echo ""
else
    echo ""
    echo "❌ Erro na instalação"
    exit 1
fi
