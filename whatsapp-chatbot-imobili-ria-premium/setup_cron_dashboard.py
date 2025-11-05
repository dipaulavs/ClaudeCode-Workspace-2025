#!/usr/bin/env python3
"""
⏰ SETUP CRON - Dashboard Diário às 8h

Configura cron job para enviar dashboard automaticamente.
"""

import os
import sys
from pathlib import Path
from subprocess import run, PIPE


def setup_cron():
    """Configura cron job para dashboard diário"""
    print("\n" + "="*70)
    print("⏰ SETUP CRON - Dashboard Diário")
    print("="*70 + "\n")

    # Caminho do script
    base_dir = Path(__file__).parent.absolute()
    script_path = base_dir / "componentes" / "relatorios" / "enviar_dashboard_diario.py"

    if not script_path.exists():
        print(f"❌ Script não encontrado: {script_path}")
        return 1

    # Comando cron (às 8h da manhã, todos os dias)
    cron_command = f"0 8 * * * cd {base_dir} && /usr/bin/python3 {script_path} >> {base_dir}/logs/dashboard.log 2>&1"

    print("📋 Cron job que será criado:")
    print(f"   Horário: Todos os dias às 08:00")
    print(f"   Comando: {cron_command}\n")

    # Confirma
    resposta = input("Deseja criar este cron job? (s/N): ").strip().lower()

    if resposta != 's':
        print("\n❌ Cancelado pelo usuário\n")
        return 1

    # Cria diretório de logs
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ Diretório de logs criado: {logs_dir}")

    # Adiciona ao crontab
    try:
        # Lista crontab atual
        result = run(['crontab', '-l'], capture_output=True, text=True)
        crontab_atual = result.stdout if result.returncode == 0 else ""

        # Verifica se já existe
        if "enviar_dashboard_diario.py" in crontab_atual:
            print("\n⚠️ Cron job já existe no crontab!")
            print("Para atualizar, remova manualmente: crontab -e")
            return 1

        # Adiciona novo cron
        novo_crontab = crontab_atual.strip() + "\n\n# Dashboard Chatbot\n" + cron_command + "\n"

        # Salva
        result = run(['crontab', '-'], input=novo_crontab, text=True, capture_output=True)

        if result.returncode == 0:
            print("\n✅ Cron job criado com sucesso!")
            print(f"\n📅 Dashboard será enviado automaticamente:")
            print(f"   • Horário: Todos os dias às 08:00")
            print(f"   • Número: Ver em enviar_dashboard_diario.py (NUMERO_GESTOR)")
            print(f"   • Logs: {logs_dir}/dashboard.log")
            print()

            print("📝 Comandos úteis:")
            print("   • Ver cron jobs: crontab -l")
            print("   • Editar cron: crontab -e")
            print("   • Ver logs: tail -f logs/dashboard.log")
            print("   • Testar agora: python3 componentes/relatorios/enviar_dashboard_diario.py")
            print()

            return 0
        else:
            print(f"\n❌ Erro ao criar cron: {result.stderr}")
            return 1

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(setup_cron())
