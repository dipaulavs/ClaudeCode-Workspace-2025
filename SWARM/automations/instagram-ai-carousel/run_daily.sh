#!/bin/bash
# Script para cron - Executa workflow diariamente

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"

# Cria diretório de logs
mkdir -p "$LOG_DIR"

# Timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/cron_$TIMESTAMP.log"

echo "=== Instagram AI Carousel - Execução Diária ===" | tee "$LOG_FILE"
echo "Início: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Carrega variáveis de ambiente
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(cat "$SCRIPT_DIR/.env" | grep -v '^#' | xargs)
fi

# Executa workflow
cd "$SCRIPT_DIR"
python3 orchestrator.py 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=$?

echo "" | tee -a "$LOG_FILE"
echo "Fim: $(date)" | tee -a "$LOG_FILE"
echo "Exit code: $EXIT_CODE" | tee -a "$LOG_FILE"

# Limpa logs antigos (mantém últimos 30 dias)
find "$LOG_DIR" -name "cron_*.log" -mtime +30 -delete

exit $EXIT_CODE
