#!/bin/bash
# Auto-test: Roda testes automaticamente após mudanças

FILE="${CLAUDE_TOOL_FILE_PATH:-}"
WORKDIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Detecta tipo de projeto e roda testes apropriados
if [[ -f "$WORKDIR/package.json" ]] && grep -q "\"test\"" "$WORKDIR/package.json" 2>/dev/null; then
    # Node.js project
    cd "$WORKDIR" && npm test --silent 2>&1 | tail -5 &
elif [[ -f "$WORKDIR/pytest.ini" ]] || [[ -f "$WORKDIR/setup.py" ]]; then
    # Python project
    cd "$WORKDIR" && pytest --quiet --tb=short 2>&1 | tail -10 &
elif [[ -f "$WORKDIR/go.mod" ]]; then
    # Go project
    cd "$WORKDIR" && go test ./... 2>&1 | tail -10 &
fi

exit 0
