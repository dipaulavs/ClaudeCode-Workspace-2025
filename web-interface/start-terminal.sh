#!/bin/bash
echo "💻 Iniciando Terminal Web (porta 7681)..."
echo "   Acesse: http://localhost:7681"
echo ""

# Verificar se ttyd está instalado
if ! command -v ttyd &> /dev/null; then
    echo "❌ ttyd não está instalado!"
    echo "   Execute: bash setup.sh"
    exit 1
fi

# Verificar se claude está disponível
if ! command -v claude &> /dev/null; then
    echo "⚠️  Comando 'claude' não encontrado no PATH"
    echo "   O terminal será aberto no zsh, você pode iniciar o claude manualmente"
    ttyd --writable -p 7681 -t fontSize=20 -t rendererType=webgl -t disableLeaveAlert=true -t theme='{"background":"#1e1e1e","foreground":"#d4d4d4"}' /bin/zsh
else
    # Iniciar ttyd com o claude
    ttyd --writable -p 7681 -t fontSize=20 -t rendererType=webgl -t disableLeaveAlert=true -t theme='{"background":"#1e1e1e","foreground":"#d4d4d4"}' claude
fi
