#!/bin/bash
# Obsidian Auto Manager (versão Shell)
# Gerencia automaticamente tarefas no Obsidian

VAULT_PATH="$HOME/Documents/Obsidian/Claude-code-ios"
TAREFAS_DIR="$VAULT_PATH/📋 Tarefas"
KANBAN_FILE="$TAREFAS_DIR/📊 Kanban.md"
SYNC_SCRIPT="$(dirname "$0")/sync_kanban_status.py"

echo "🚀 Obsidian Auto Manager iniciado!"
echo "📂 Monitorando: $TAREFAS_DIR"
echo ""
echo "✨ Funcionalidades:"
echo "  1. Nova tarefa → Adiciona ao Kanban (coluna 'aberta')"
echo "  2. Move no Kanban → Atualiza status automaticamente"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

# Função para adicionar tarefa ao Kanban
add_to_kanban() {
    local task_file="$1"
    local task_name=$(basename "$task_file" .md)

    # Ignora Kanban
    if [ "$task_name" = "📊 Kanban" ]; then
        return
    fi

    # Verifica se já existe no Kanban
    if grep -q "\[\[$task_name\]\]" "$KANBAN_FILE" 2>/dev/null; then
        return
    fi

    # Adiciona na coluna 'aberta'
    echo "📋 Nova tarefa detectada: $task_name"

    # Backup
    cp "$KANBAN_FILE" "$KANBAN_FILE.bak"

    # Adiciona após linha "## aberta"
    awk -v task="- [ ] [[$task_name]]" '
        /^## aberta/ { print; print task; next }
        { print }
    ' "$KANBAN_FILE.bak" > "$KANBAN_FILE"

    rm "$KANBAN_FILE.bak"
    echo "✅ Tarefa adicionada ao Kanban"
}

# Sincroniza status quando Kanban mudar
sync_status() {
    echo "🔄 Kanban modificado, sincronizando status..."
    python3 "$SYNC_SCRIPT"
}

# Monitora pasta de tarefas
echo "👀 Monitorando mudanças..."
fswatch -0 "$TAREFAS_DIR" | while read -d "" event; do
    # Se é novo arquivo .md
    if [[ "$event" == *.md ]] && [ -f "$event" ]; then
        if [[ "$event" == *"📊 Kanban.md" ]]; then
            # Kanban mudou → sincroniza status
            sync_status
        else
            # Nova tarefa → adiciona ao Kanban
            sleep 0.5  # Aguarda arquivo ser escrito
            add_to_kanban "$event"
        fi
    fi
done
