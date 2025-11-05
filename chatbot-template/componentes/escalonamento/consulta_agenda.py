"""
Consulta de Agenda para Agendamento de Visitas
Integração com Google Sheets (+ mock para testes)
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class ConsultaAgenda:
    """
    Consulta disponibilidade de horários para visitas
    Suporta Google Sheets API ou modo MOCK
    """

    def __init__(self, use_mock: bool = True, sheet_id: Optional[str] = None):
        """
        Args:
            use_mock: Se True, usa dados mockados. Se False, usa Google API
            sheet_id: ID da planilha Google Sheets (obrigatório se use_mock=False)
        """
        self.use_mock = use_mock
        self.sheet_id = sheet_id

        if not use_mock:
            if not sheet_id:
                print("⚠️ sheet_id não fornecido. Usando MOCK mode.")
                self.use_mock = True
                self.sheet_id = "MOCK_MODE"
                self.service = None
            else:
                self._init_google_api()
        else:
            self.service = None
            self.sheet_id = "MOCK_MODE"

    def _init_google_api(self):
        """Inicializa Google Sheets API (se credenciais existirem)"""
        try:
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build

            config_path = os.path.join(
                os.path.dirname(__file__),
                '../../config/google_service_account.json'
            )

            if not os.path.exists(config_path):
                print("⚠️ Credenciais Google não encontradas. Usando MOCK mode.")
                self.use_mock = True
                return

            self.creds = Credentials.from_service_account_file(
                config_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )

            self.service = build('sheets', 'v4', credentials=self.creds)

            # Sheet ID (pode ser configurado posteriormente)
            # from config.config import GOOGLE_SHEET_ID
            self.sheet_id = None  # Deve ser definido via parâmetro ou config

        except ImportError:
            print("⚠️ Google API não instalada. Use: pip install google-api-python-client google-auth")
            self.use_mock = True
        except Exception as e:
            print(f"⚠️ Erro ao inicializar Google API: {e}. Usando MOCK mode.")
            self.use_mock = True

    def buscar_horarios_disponiveis(self, dias_frente: int = 3, limite: int = 3) -> List[Dict]:
        """
        Busca horários disponíveis nos próximos N dias

        Args:
            dias_frente: Quantos dias à frente buscar
            limite: Máximo de horários a retornar

        Returns:
            Lista de horários disponíveis
        """
        if self.use_mock:
            return self._buscar_horarios_mock(dias_frente, limite)
        else:
            return self._buscar_horarios_google(dias_frente, limite)

    def _buscar_horarios_mock(self, dias_frente: int = 3, limite: int = 3) -> List[Dict]:
        """Mock de horários disponíveis (para testes sem Google API)"""

        hoje = datetime.now()
        horarios = []

        # Gera horários para os próximos dias
        for dia_offset in range(1, dias_frente + 1):
            data = hoje + timedelta(days=dia_offset)

            # Horários disponíveis por dia
            slots = ["10:00", "14:00", "15:00", "16:00"]

            for i, hora in enumerate(slots):
                if len(horarios) >= limite:
                    break

                # Dias da semana em PT-BR
                dias_semana = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
                dia_semana = dias_semana[data.weekday()]

                horarios.append({
                    "data": data.date(),
                    "hora": hora,
                    "corretor": "Bruno",
                    "data_formatada": data.strftime(f'%d/%m ({dia_semana})'),
                    "row_index": None,  # Mock não tem row
                    "mock": True
                })

            if len(horarios) >= limite:
                break

        return horarios[:limite]

    def _buscar_horarios_google(self, dias_frente: int = 3, limite: int = 3) -> List[Dict]:
        """Busca horários na planilha Google Sheets"""

        try:
            # Ler planilha
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Agenda!A2:F100'  # Aba "Agenda", linhas 2-100
            ).execute()

            rows = result.get('values', [])

            horarios_disponiveis = []
            hoje = datetime.now().date()
            data_limite = hoje + timedelta(days=dias_frente)

            for idx, row in enumerate(rows):
                if len(row) < 4:
                    continue

                data_str, hora_str, corretor, status = row[:4]

                # Parse data (formato: DD/MM/YYYY)
                try:
                    data = datetime.strptime(data_str, '%d/%m/%Y').date()
                except ValueError:
                    continue

                # Filtros
                if status.lower() != "disponível":
                    continue
                if data < hoje:
                    continue
                if data > data_limite:
                    continue

                # Dias da semana em PT-BR
                dias_semana = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
                dia_semana = dias_semana[data.weekday()]

                horarios_disponiveis.append({
                    "data": data,
                    "hora": hora_str,
                    "corretor": corretor,
                    "data_formatada": data.strftime(f'%d/%m ({dia_semana})'),
                    "row_index": idx + 2,  # +2 por causa do header (linha 1) e índice 0
                    "mock": False
                })

                if len(horarios_disponiveis) >= limite:
                    break

            return horarios_disponiveis

        except Exception as e:
            print(f"❌ Erro ao consultar Google Sheets: {e}")
            # Fallback para mock
            return self._buscar_horarios_mock(dias_frente, limite)

    def agendar_visita(
        self,
        cliente_numero: str,
        imovel_id: str,
        horario: Dict
    ) -> bool:
        """
        Marca horário como agendado

        Args:
            cliente_numero: Número do cliente
            imovel_id: ID do imóvel
            horario: Horário escolhido (dict retornado por buscar_horarios_disponiveis)

        Returns:
            True se agendado com sucesso
        """
        if horario.get("mock", False):
            # Mock mode - só simula
            print(f"✅ [MOCK] Agendado: {cliente_numero} | {imovel_id} | {horario['data_formatada']} {horario['hora']}")
            return True
        else:
            return self._agendar_google(cliente_numero, imovel_id, horario)

    def _agendar_google(
        self,
        cliente_numero: str,
        imovel_id: str,
        horario: Dict
    ) -> bool:
        """Agenda na planilha Google Sheets"""

        try:
            row_index = horario['row_index']

            # Atualizar linha (colunas D, E, F)
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f'Agenda!D{row_index}:F{row_index}',
                valueInputOption='RAW',
                body={
                    'values': [[
                        'agendado',
                        cliente_numero,
                        imovel_id
                    ]]
                }
            ).execute()

            print(f"✅ Agendado no Google Sheets: {cliente_numero} | {imovel_id} | Linha {row_index}")
            return True

        except Exception as e:
            print(f"❌ Erro ao agendar no Google Sheets: {e}")
            return False

    def cancelar_agendamento(self, horario: Dict) -> bool:
        """
        Cancela agendamento (marca como disponível novamente)

        Args:
            horario: Horário a cancelar

        Returns:
            True se cancelado
        """
        if horario.get("mock", False):
            print(f"✅ [MOCK] Cancelado: {horario['data_formatada']} {horario['hora']}")
            return True

        try:
            row_index = horario['row_index']

            # Limpar linha (colunas D, E, F)
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f'Agenda!D{row_index}:F{row_index}',
                valueInputOption='RAW',
                body={
                    'values': [['disponível', '', '']]
                }
            ).execute()

            return True

        except Exception as e:
            print(f"❌ Erro ao cancelar: {e}")
            return False
