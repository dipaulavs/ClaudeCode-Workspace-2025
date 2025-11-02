#!/bin/bash

# 🤖 Claude Code - Inicialização Automática
# Inicia Claude Code sem pedir permissões

echo "🚀 Iniciando Claude Code (sem permissões)..."
echo "📁 Workspace: ClaudeCode-Workspace"
echo "📋 Auto-load: CLAUDE.md"
echo ""

cd ~/Desktop/ClaudeCode-Workspace
claude --dangerously-skip-permissions
