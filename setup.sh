#!/bin/bash
# Script de configuração inicial do Claude Code Workspace

echo "🚀 Configurando Claude Code Workspace..."
echo ""

# Verificar se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale Python3 primeiro."
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dependências instaladas com sucesso!"
else
    echo ""
    echo "❌ Erro ao instalar dependências."
    exit 1
fi

# Tornar scripts executáveis
echo ""
echo "🔧 Configurando permissões..."
chmod +x tools/*.py 2>/dev/null
chmod +x *.sh 2>/dev/null

echo ""
echo "✨ Configuração concluída!"
echo ""
echo "Para usar o gerador de imagens:"
echo "  python3 tools/generate_image.py \"sua descrição aqui\""
echo ""
echo "Para ver todas as ferramentas disponíveis:"
echo "  ls -l tools/"
echo ""
