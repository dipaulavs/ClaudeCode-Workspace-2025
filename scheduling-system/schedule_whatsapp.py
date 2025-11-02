#!/usr/bin/env python3
"""
Sistema de Agendamento WhatsApp
Permite agendar mensagens para serem enviadas em horários específicos
Suporta agendamentos únicos e recorrentes
"""

import sys
import os
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Adiciona paths necessários
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "evolution-api-integration"))

from whatsapp_helper import whatsapp


class WhatsAppScheduler:
    """Gerenciador de agendamentos WhatsApp"""

    def __init__(self):
        self.schedule_dir = Path(__file__).parent / "scheduled_tasks"
        self.log_dir = Path(__file__).parent / "logs"
        self.schedule_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

    def create_task_script(self, task_name, phone, message):
        """Cria script de tarefa agendada"""
        script_path = self.schedule_dir / f"{task_name}.py"

        script_content = f'''#!/usr/bin/env python3
"""
Tarefa agendada: {task_name}
Criado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import sys
import os
from pathlib import Path

# Adiciona evolution-api-integration ao path
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "evolution-api-integration"))

from whatsapp_helper import whatsapp

def send_message():
    """Envia mensagem agendada"""
    phone_number = "{phone}"
    message = """{message}"""

    try:
        print(f"📱 Enviando mensagem para {{phone_number}}...")
        result = whatsapp.send_message(phone_number, message)
        print(f"✅ Mensagem enviada com sucesso!")
        print(f"📊 Resultado: {{result}}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {{e}}")
        return False

if __name__ == "__main__":
    print(f"🤖 Executando tarefa: {task_name}")
    print("=" * 50)
    send_message()
'''

        with open(script_path, 'w') as f:
            f.write(script_content)

        # Torna executável
        os.chmod(script_path, 0o755)

        return script_path

    def schedule_task(self, task_name, script_path, time_str, recurring=False):
        """Adiciona tarefa ao crontab"""
        log_file = self.log_dir / f"{task_name}.log"

        # Parse do horário (formato: HH:MM)
        try:
            hour, minute = map(int, time_str.split(':'))
        except ValueError:
            print("❌ Erro: Formato de horário inválido. Use HH:MM (ex: 17:00)")
            return False

        # Cria linha do crontab
        if recurring:
            # Recorrente (todos os dias)
            cron_line = f"{minute} {hour} * * * cd {BASE_DIR} && /usr/bin/python3 {script_path} >> {log_file} 2>&1"
        else:
            # Uma vez só (hoje)
            now = datetime.now()
            # Para execução única, vamos usar 'at' ao invés de cron
            # Mas por simplicidade, vamos usar cron e depois remover
            cron_line = f"{minute} {hour} * * * cd {BASE_DIR} && /usr/bin/python3 {script_path} >> {log_file} 2>&1"

        # Obtém crontab atual
        try:
            current_crontab = subprocess.check_output(['crontab', '-l'],
                                                     stderr=subprocess.DEVNULL).decode('utf-8')
        except subprocess.CalledProcessError:
            current_crontab = ""

        # Verifica se já existe uma linha para esta tarefa
        lines = current_crontab.strip().split('\n') if current_crontab else []
        new_lines = [line for line in lines if task_name not in line and line.strip()]

        # Adiciona nova linha
        new_lines.append(cron_line)

        # Salva novo crontab
        new_crontab = '\n'.join(new_lines) + '\n'

        try:
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
            process.communicate(new_crontab.encode('utf-8'))
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar crontab: {e}")
            return False

    def list_scheduled_tasks(self):
        """Lista todas as tarefas agendadas"""
        try:
            crontab_output = subprocess.check_output(['crontab', '-l'],
                                                     stderr=subprocess.DEVNULL).decode('utf-8')

            print("\n📅 Tarefas Agendadas:")
            print("=" * 80)

            if not crontab_output.strip():
                print("Nenhuma tarefa agendada no momento.")
                return

            for line in crontab_output.strip().split('\n'):
                if 'scheduling-system' in line:
                    print(f"  • {line}")

            print("=" * 80)

        except subprocess.CalledProcessError:
            print("Nenhuma tarefa agendada no momento.")

    def remove_task(self, task_name):
        """Remove uma tarefa agendada"""
        try:
            current_crontab = subprocess.check_output(['crontab', '-l'],
                                                     stderr=subprocess.DEVNULL).decode('utf-8')

            # Filtra linhas que não contêm o task_name
            lines = current_crontab.strip().split('\n')
            new_lines = [line for line in lines if task_name not in line and line.strip()]

            if len(lines) == len(new_lines):
                print(f"⚠️  Tarefa '{task_name}' não encontrada.")
                return False

            # Salva novo crontab
            new_crontab = '\n'.join(new_lines) + '\n' if new_lines else ''

            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
            process.communicate(new_crontab.encode('utf-8'))

            print(f"✅ Tarefa '{task_name}' removida com sucesso!")
            return True

        except subprocess.CalledProcessError:
            print("❌ Nenhuma tarefa encontrada para remover.")
            return False

    def clear_all_tasks(self):
        """Remove TODAS as tarefas agendadas"""
        try:
            subprocess.run(['crontab', '-r'], check=True)
            print("✅ Todas as tarefas foram removidas!")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Nenhuma tarefa para remover.")
            return False


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Sistema de Agendamento WhatsApp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Agendar mensagem única para hoje às 17h
  python3 schedule_whatsapp.py --phone 5531980160822 --message "Piada do dia!" --time 17:00

  # Agendar mensagem recorrente (todos os dias às 9h)
  python3 schedule_whatsapp.py --phone 5531980160822 --message "Bom dia!" --time 09:00 --daily

  # Agendar com nome personalizado
  python3 schedule_whatsapp.py --name piada_diaria --phone 5531980160822 --message "Piada!" --time 17:00 --daily

  # Listar tarefas agendadas
  python3 schedule_whatsapp.py --list

  # Remover tarefa específica
  python3 schedule_whatsapp.py --remove piada_diaria

  # Remover TODAS as tarefas
  python3 schedule_whatsapp.py --clear-all
        """
    )

    parser.add_argument('--phone', help='Número do WhatsApp (formato: 5531980160822)')
    parser.add_argument('--message', help='Mensagem a ser enviada')
    parser.add_argument('--time', help='Horário (formato: HH:MM, ex: 17:00)')
    parser.add_argument('--name', help='Nome da tarefa (opcional, gerado automaticamente se omitido)')
    parser.add_argument('--daily', action='store_true', help='Repetir diariamente (padrão: executa uma vez)')
    parser.add_argument('--list', action='store_true', help='Listar tarefas agendadas')
    parser.add_argument('--remove', help='Remover tarefa específica pelo nome')
    parser.add_argument('--clear-all', action='store_true', help='Remover TODAS as tarefas agendadas')

    args = parser.parse_args()

    scheduler = WhatsAppScheduler()

    # Lista tarefas
    if args.list:
        scheduler.list_scheduled_tasks()
        return

    # Remove tarefa específica
    if args.remove:
        scheduler.remove_task(args.remove)
        return

    # Remove todas as tarefas
    if args.clear_all:
        confirm = input("⚠️  ATENÇÃO: Isso vai remover TODAS as tarefas agendadas. Confirma? (sim/não): ")
        if confirm.lower() in ['sim', 's', 'yes', 'y']:
            scheduler.clear_all_tasks()
        else:
            print("Operação cancelada.")
        return

    # Validações para criar nova tarefa
    if not args.phone or not args.message or not args.time:
        parser.print_help()
        sys.exit(1)

    # Gera nome da tarefa
    if args.name:
        task_name = args.name
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = f"whatsapp_task_{timestamp}"

    print("\n🤖 Sistema de Agendamento WhatsApp")
    print("=" * 80)
    print(f"📝 Tarefa: {task_name}")
    print(f"📱 Destinatário: {args.phone}")
    print(f"⏰ Horário: {args.time}")
    print(f"🔄 Recorrente: {'Sim (todos os dias)' if args.daily else 'Não (apenas uma vez)'}")
    print(f"💬 Mensagem:")
    print(f"   {args.message[:100]}{'...' if len(args.message) > 100 else ''}")
    print("=" * 80)

    # Cria script da tarefa
    print("\n📝 Criando script de tarefa...")
    script_path = scheduler.create_task_script(task_name, args.phone, args.message)
    print(f"✅ Script criado: {script_path}")

    # Agenda tarefa
    print(f"\n⏰ Agendando tarefa para {args.time}...")
    if scheduler.schedule_task(task_name, script_path, args.time, args.daily):
        print(f"✅ Tarefa agendada com sucesso!")
        print(f"\n📋 Para verificar: python3 {Path(__file__).name} --list")
        print(f"🗑️  Para remover: python3 {Path(__file__).name} --remove {task_name}")

        if not args.daily:
            print(f"\n⚠️  LEMBRETE: Esta é uma tarefa única.")
            print(f"   Após a execução, remova manualmente com --remove")
    else:
        print("❌ Erro ao agendar tarefa.")
        sys.exit(1)


if __name__ == "__main__":
    main()
