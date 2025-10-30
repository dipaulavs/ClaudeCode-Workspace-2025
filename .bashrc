# Claude Code Workspace - Configuração automática

# Exibir boas-vindas ao abrir terminal nesta pasta
if [ "$PWD" = "$HOME/Desktop/ClaudeCode-Workspace" ]; then
    bash iniciar.sh 2>/dev/null || true
fi

# Aliases úteis
alias gerar-imagem='python3 tools/generate_image.py'
alias ver-imagens='open ~/Downloads'
alias workspace-help='cat README.md'

# Mensagem de ajuda rápida
alias ajuda='echo "
Comandos rápidos:
  gerar-imagem \"sua descrição\" [--variants N] [--enhance]
  ver-imagens
  workspace-help
"'
