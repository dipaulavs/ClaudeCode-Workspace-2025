#!/bin/bash
# Auto-backup: Git commit automático em cada Edit/Write

FILE="${CLAUDE_TOOL_FILE_PATH:-unknown}"
TOOL="${CLAUDE_TOOL_NAME:-unknown}"

# Só commita se estiver em repo git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    exit 0
fi

# Commit silencioso
cd "$(git rev-parse --show-toplevel)" 2>/dev/null || exit 0

git add "$FILE" 2>/dev/null
git commit -m "🤖 auto-backup: $TOOL → $FILE" --quiet 2>/dev/null || true

exit 0
