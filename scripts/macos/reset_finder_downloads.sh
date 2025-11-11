#!/bin/bash
# Script para resetar preferências do Finder na pasta Downloads
# Força ordenação por data de modificação (mais recentes primeiro)

echo "🔧 Resetando preferências do Finder para Downloads..."

# Fechar Finder (vai reabrir automaticamente)
killall Finder 2>/dev/null

# Remover preferências específicas da pasta Downloads
# O Finder armazena preferências em .DS_Store
rm -f ~/Downloads/.DS_Store

# Limpar cache de preferências do Finder
defaults delete com.apple.finder FXPreferredViewStyle 2>/dev/null
defaults delete com.apple.finder FXPreferredGroupBy 2>/dev/null

# Configurar visualização padrão como lista
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"

# Desabilitar agrupamento
defaults write com.apple.finder FXPreferredGroupBy -string "None"

# Forçar ordenação por data de modificação
defaults write com.apple.finder FXArrangeGroupViewBy -string "dateModified"

# Aplicar mudanças
killall Finder

echo ""
echo "✅ Preferências resetadas!"
echo ""
echo "📋 Próximos passos manuais no Finder:"
echo "   1. Abra a pasta Downloads"
echo "   2. Pressione ⌘J (View Options)"
echo "   3. Ordenar por: Data de Modificação"
echo "   4. Clique na seta ↓ para inverter (mais recentes no topo)"
echo "   5. Clique 'Usar como padrões' no final da janela"
echo ""
echo "🔍 Dica: Na visualização em lista, clique 2x na coluna"
echo "   'Data de Modificação' para garantir ordenação ↓"
