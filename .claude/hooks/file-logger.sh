#!/bin/bash
# File Change Logger: Auditoria completa de mudanças

LOGFILE="/tmp/claude-changes.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
TOOL="${CLAUDE_TOOL_NAME:-unknown}"
FILE="${CLAUDE_TOOL_FILE_PATH:-unknown}"
USER="${USER:-unknown}"

# Cria log estruturado
echo "[$TIMESTAMP] $USER → $TOOL → $FILE" >> "$LOGFILE"

# Mantém apenas últimas 1000 linhas
tail -1000 "$LOGFILE" > "${LOGFILE}.tmp" 2>/dev/null && mv "${LOGFILE}.tmp" "$LOGFILE"

exit 0
