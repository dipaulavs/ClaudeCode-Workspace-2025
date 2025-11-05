#!/usr/bin/env python3
"""
🔄 Atualizar Agenda Automática
Adiciona horários disponíveis para os próximos N dias

USO:
    python3 atualizar_agenda.py                  # Próximos 7 dias
    python3 atualizar_agenda.py --dias 14        # Próximos 14 dias
    python3 atualizar_agenda.py --vendedor Bruno # Só para Bruno
"""

import argparse
from datetime import datetime, timedelta
import sys
import os

# Adiciona path do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    GOOGLE_API_DISPONIVEL = True
except ImportError:
    print("⚠️  Google API não instalada. Instale: pip install google-api-python-client google-auth")
    GOOGLE_API_DISPONIVEL = False


class AtualizadorAgenda:
    """Atualiza planilha de agenda com novos horários"""

    # Configurações padrão
    HORARIOS_PADRAO = ["10:00", "14:00", "15:00", "16:00"]
    VENDEDORES = ["Bruno", "Fernanda"]

    def __init__(self, sheet_id: str):
        """
        Args:
            sheet_id: ID da planilha Google Sheets
        """
        if not GOOGLE_API_DISPONIVEL:
            raise RuntimeError("Google API não disponível")

        self.sheet_id = sheet_id
        self._init_google_api()

    def _init_google_api(self):
        """Inicializa Google Sheets API"""
        config_path = os.path.join(
            os.path.dirname(__file__),
            '../../config/google_service_account.json'
        )

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Credenciais não encontradas: {config_path}\n"
                "Veja PLANILHA_AGENDA_IMOBILI-RIA-PREMIUM.md para instruções"
            )

        self.creds = Credentials.from_service_account_file(
            config_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )

        self.service = build('sheets', 'v4', credentials=self.creds)

    def buscar_ultimas_datas(self) -> datetime:
        """
        Busca última data na planilha para não duplicar

        Returns:
            Data mais recente encontrada
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Agenda!A2:A1000'
            ).execute()

            rows = result.get('values', [])

            if not rows:
                # Planilha vazia, começar de hoje
                return datetime.now().date()

            # Parsear datas e encontrar a mais recente
            datas = []
            for row in rows:
                if not row or not row[0]:
                    continue

                try:
                    data = datetime.strptime(row[0], '%d/%m/%Y').date()
                    datas.append(data)
                except ValueError:
                    continue

            if datas:
                return max(datas)
            else:
                return datetime.now().date()

        except Exception as e:
            print(f"⚠️ Erro ao buscar datas: {e}")
            return datetime.now().date()

    def adicionar_horarios(
        self,
        dias_frente: int = 7,
        vendedores: list = None,
        horarios: list = None
    ):
        """
        Adiciona horários disponíveis para próximos dias

        Args:
            dias_frente: Quantos dias adicionar
            vendedores: Lista de vendedores (None = todos)
            horarios: Lista de horários (None = padrão)
        """
        if vendedores is None:
            vendedores = self.VENDEDORES

        if horarios is None:
            horarios = self.HORARIOS_PADRAO

        # Busca última data na planilha
        ultima_data = self.buscar_ultimas_datas()
        print(f"📅 Última data na planilha: {ultima_data.strftime('%d/%m/%Y')}")

        # Começa do dia seguinte
        data_inicio = ultima_data + timedelta(days=1)

        # Gera novos horários
        novas_linhas = []

        for dia_offset in range(dias_frente):
            data = data_inicio + timedelta(days=dia_offset)

            # Pula finais de semana (opcional)
            # if data.weekday() >= 5:  # 5=Sábado, 6=Domingo
            #     continue

            for hora in horarios:
                for vendedor in vendedores:
                    novas_linhas.append([
                        data.strftime('%d/%m/%Y'),
                        hora,
                        vendedor,
                        'disponível',
                        '',  # Cliente vazio
                        ''   # Veículo vazio
                    ])

        if not novas_linhas:
            print("⚠️ Nenhuma linha nova para adicionar")
            return

        # Adiciona na planilha
        print(f"\n📝 Adicionando {len(novas_linhas)} horários...")

        try:
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range='Agenda!A2',
                valueInputOption='USER_ENTERED',
                body={'values': novas_linhas}
            ).execute()

            added = result.get('updates', {}).get('updatedRows', 0)
            print(f"✅ {added} horários adicionados!")

            # Resumo
            print(f"\n📊 Resumo:")
            print(f"   • De: {data_inicio.strftime('%d/%m/%Y')}")
            print(f"   • Até: {(data_inicio + timedelta(days=dias_frente-1)).strftime('%d/%m/%Y')}")
            print(f"   • Vendedores: {', '.join(vendedores)}")
            print(f"   • Horários/dia: {len(horarios)}")

        except Exception as e:
            print(f"❌ Erro ao adicionar: {e}")

    def limpar_horarios_passados(self):
        """Remove horários de datas passadas"""
        print("\n🗑️ Limpando horários passados...")

        try:
            # Busca todas linhas
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Agenda!A2:F1000'
            ).execute()

            rows = result.get('values', [])
            hoje = datetime.now().date()

            linhas_manter = []

            for row in rows:
                if not row or len(row) < 1:
                    continue

                try:
                    data = datetime.strptime(row[0], '%d/%m/%Y').date()

                    # Manter só se for hoje ou futuro
                    if data >= hoje:
                        linhas_manter.append(row)

                except ValueError:
                    # Data inválida, manter
                    linhas_manter.append(row)

            removidas = len(rows) - len(linhas_manter)

            if removidas > 0:
                # Limpa sheet inteira
                self.service.spreadsheets().values().clear(
                    spreadsheetId=self.sheet_id,
                    range='Agenda!A2:F1000'
                ).execute()

                # Re-escreve só linhas válidas
                if linhas_manter:
                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.sheet_id,
                        range='Agenda!A2',
                        valueInputOption='USER_ENTERED',
                        body={'values': linhas_manter}
                    ).execute()

                print(f"✅ {removidas} horários passados removidos")
            else:
                print("✅ Nenhum horário passado encontrado")

        except Exception as e:
            print(f"❌ Erro ao limpar: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Atualiza planilha de agenda com novos horários'
    )

    parser.add_argument(
        '--sheet-id',
        type=str,
        required=True,
        help='ID da planilha Google Sheets'
    )

    parser.add_argument(
        '--dias',
        type=int,
        default=7,
        help='Quantos dias adicionar (padrão: 7)'
    )

    parser.add_argument(
        '--vendedor',
        type=str,
        help='Adicionar só para vendedor específico (ex: Bruno)'
    )

    parser.add_argument(
        '--limpar',
        action='store_true',
        help='Limpar horários passados antes de adicionar'
    )

    args = parser.parse_args()

    if not GOOGLE_API_DISPONIVEL:
        print("❌ Google API não disponível")
        print("Instale: pip install google-api-python-client google-auth")
        return

    print("=" * 60)
    print("🔄 ATUALIZADOR DE AGENDA")
    print("=" * 60)

    try:
        atualizador = AtualizadorAgenda(args.sheet_id)

        # Limpar horários passados (se solicitado)
        if args.limpar:
            atualizador.limpar_horarios_passados()

        # Adicionar novos horários
        vendedores = [args.vendedor] if args.vendedor else None

        atualizador.adicionar_horarios(
            dias_frente=args.dias,
            vendedores=vendedores
        )

        print("\n✅ Atualização concluída!")

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
