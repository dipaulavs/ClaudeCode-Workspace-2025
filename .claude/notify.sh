#!/bin/bash
# Notificação sonora confiável para Claude Code

# Log para debug
echo "[$(date)] Hook chamado - Tool: ${CLAUDE_TOOL_NAME:-Unknown}" >> /tmp/claude-notify.log

TOOL_NAME="${CLAUDE_TOOL_NAME:-Unknown}"

# Notificação visual
osascript -e "display notification \"Tool: $TOOL_NAME completed\" with title \"Claude Code\"" 2>/dev/null &

# Som (não-bloqueante)
afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &

exit 0
