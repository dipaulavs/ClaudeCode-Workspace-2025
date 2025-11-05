#!/usr/bin/env python3
"""
⏰ ENVIO AUTOMÁTICO DE DASHBOARD DIÁRIO

Executado via cron às 8h da manhã.
Gera dashboard do dia anterior e envia por WhatsApp.

SETUP:
1. Configure número do gestor abaixo (NUMERO_GESTOR)
2. Execute: python3 setup_cron_dashboard.py
3. Cron enviará automaticamente às 8h

TESTE MANUAL:
python3 enviar_dashboard_diario.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona paths
base_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(base_dir))

from componentes.relatorios.dashboard_visual import DashboardVisual
from upstash_redis import Redis


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

# ⚠️ CUSTOMIZAR: Número do WhatsApp do gestor
NUMERO_GESTOR = "5531986549366"  # ← ALTERE AQUI


def main():
    """Envia dashboard diário"""
    print(f"\n{'='*70}")
    print(f"📊 DASHBOARD DIÁRIO - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*70}\n")

    try:
        # 1. Carrega configuração
        config_file = base_dir / "chatwoot_config_automaia.json"

        if not config_file.exists():
            print(f"❌ Config não encontrado: {config_file}")
            print(f"💡 Crie chatwoot_config.json com Evolution API")
            return 1

        with open(config_file, 'r') as f:
            config = json.load(f)

        # 2. Conecta Redis
        # TODO: Ler de .env
        redis = Redis(
            url="https://legible-collie-9537.upstash.io",
            token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
        )

        print("✅ Redis conectado")

        # 3. Gera e envia dashboard
        dashboard = DashboardVisual(redis, config)

        # Relatório de ontem (executado às 8h de hoje)
        data_relatorio = (datetime.now() - timedelta(days=1)).date()

        print(f"📅 Gerando relatório de {data_relatorio.strftime('%d/%m/%Y')}...")

        dashboard.gerar_e_enviar(NUMERO_GESTOR, data_relatorio)

        print(f"\n✅ Dashboard enviado para {NUMERO_GESTOR}")
        print(f"⏰ Próximo envio: amanhã às 08:00\n")

        return 0

    except Exception as e:
        print(f"\n❌ Erro ao enviar dashboard: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
