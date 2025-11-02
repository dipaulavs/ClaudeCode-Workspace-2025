#!/bin/bash
#
# Script de atalho para xAI Live Search
# Uso: ./xai-search.sh "sua pergunta aqui"
#

# Caminho do Python 3.11
PYTHON="/opt/homebrew/bin/python3.11"

# Caminho do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XAI_SCRIPT="$SCRIPT_DIR/tools/xai_search.py"

# Verifica se foi fornecida uma pergunta
if [ -z "$1" ]; then
    echo "❌ Erro: Nenhuma pergunta fornecida"
    echo ""
    echo "Uso: ./xai-search.sh 'sua pergunta aqui'"
    echo ""
    echo "Exemplos:"
    echo "  ./xai-search.sh 'Quais são as últimas notícias sobre IA?'"
    echo "  ./xai-search.sh 'O que as pessoas estão dizendo sobre xAI no Twitter?'"
    echo ""
    echo "Para exemplos avançados, execute:"
    echo "  $PYTHON tools/xai_search_examples.py"
    echo ""
    exit 1
fi

# Executa a busca
$PYTHON "$XAI_SCRIPT" "$@"
