#!/usr/bin/env python3
"""
Processador de Follow-ups Pendentes

Executado via cron a cada 5 minutos.
Busca e envia follow-ups agendados cujo timestamp já passou.

Cron job:
*/5 * * * * /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/followup/processador_cron.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log 2>&1
"""

import sys
from datetime import datetime
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from componentes.followup import SistemaFollowUp


def main():
    """
    Processa follow-ups pendentes.
    """
    print(f"\n{'='*60}")
    print(f"🔔 Processador de Follow-ups | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        sistema = SistemaFollowUp()

        # Processar follow-ups pendentes
        enviados = sistema.processar_pendentes()

        if enviados > 0:
            print(f"\n✅ {enviados} follow-up(s) enviado(s) com sucesso")
        else:
            print(f"\n✓ Nenhum follow-up pendente no momento")

    except Exception as e:
        print(f"\n❌ Erro ao processar follow-ups: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print(f"\n{'='*60}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
