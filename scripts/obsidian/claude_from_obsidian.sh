#!/bin/bash
# 🤖 Atalho rápido: Abrir Claude Code do Obsidian
# Uso no Terminal Plugin: ./claude_from_obsidian.sh

WORKSPACE="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace"

echo "🤖 Abrindo Claude Code Workspace..."

# Abrir VS Code
cd "$WORKSPACE"
code .

echo "✅ VS Code aberto em: $WORKSPACE"

# Notificação macOS
osascript -e 'display notification "Workspace aberto no VS Code" with title "Claude Code"'
