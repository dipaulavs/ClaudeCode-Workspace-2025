#!/usr/bin/env python3
"""
🚀 CRIAR AGENDA PÚBLICA - Google Sheets
Cria planilha de agenda automaticamente e torna pública

USO:
    python3 criar_agenda_publica.py
    python3 criar_agenda_publica.py --nome "Agenda Automaia 2025"
    python3 criar_agenda_publica.py --dias 14 --vendedores "Bruno,Fernanda,Carlos"
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict

# Adiciona path do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    GOOGLE_API_DISPONIVEL = True
except ImportError:
    print("❌ Google API não instalada")
    print("Instale: pip install google-api-python-client google-auth")
    GOOGLE_API_DISPONIVEL = False


class CriadorAgendaPublica:
    """Cria planilha de agenda Google Sheets e torna pública"""

    # Configurações padrão
    HORARIOS_PADRAO = ["10:00", "14:00", "15:00", "16:00"]
    VENDEDORES_PADRAO = ["Bruno", "Fernanda"]

    def __init__(self):
        """Inicializa com credenciais Google"""
        if not GOOGLE_API_DISPONIVEL:
            raise RuntimeError("Google API não disponível")

        self._init_google_api()

    def _init_google_api(self):
        """Inicializa Google Sheets e Drive API"""
        config_path = os.path.join(
            os.path.dirname(__file__),
            '../../config/google_service_account.json'
        )

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"❌ Credenciais Google não encontradas: {config_path}\n\n"
                "COMO OBTER CREDENCIAIS:\n"
                "1. Acesse: https://console.cloud.google.com\n"
                "2. Criar projeto (ex: 'automaia-bot')\n"
                "3. Habilitar APIs:\n"
                "   - Google Sheets API\n"
                "   - Google Drive API\n"
                "4. Criar credenciais:\n"
                "   - Tipo: Service Account\n"
                "   - Role: Editor\n"
                "5. Baixar JSON e salvar em:\n"
                "   config/google_service_account.json\n"
            )

        # Scopes necessários
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        self.creds = Credentials.from_service_account_file(
            config_path,
            scopes=scopes
        )

        # Serviços
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def criar_planilha(
        self,
        nome: str = "Agenda Automaia",
        dias_frente: int = 7,
        vendedores: List[str] = None,
        horarios: List[str] = None
    ) -> Dict[str, str]:
        """
        Cria planilha de agenda completa e torna pública

        Args:
            nome: Nome da planilha
            dias_frente: Quantos dias adicionar
            vendedores: Lista de vendedores
            horarios: Lista de horários

        Returns:
            Dict com 'id', 'url', 'url_edit'
        """
        if vendedores is None:
            vendedores = self.VENDEDORES_PADRAO

        if horarios is None:
            horarios = self.HORARIOS_PADRAO

        print("\n" + "=" * 60)
        print("🚀 CRIANDO PLANILHA DE AGENDA")
        print("=" * 60)
        print(f"📝 Nome: {nome}")
        print(f"📅 Dias: {dias_frente}")
        print(f"👥 Vendedores: {', '.join(vendedores)}")
        print(f"⏰ Horários: {', '.join(horarios)}")
        print()

        # 1. CRIAR PLANILHA
        print("1️⃣ Criando planilha...")

        spreadsheet_body = {
            'properties': {
                'title': nome
            },
            'sheets': [{
                'properties': {
                    'title': 'Agenda',
                    'gridProperties': {
                        'frozenRowCount': 1  # Congela header
                    }
                }
            }]
        }

        spreadsheet = self.sheets_service.spreadsheets().create(
            body=spreadsheet_body
        ).execute()

        sheet_id = spreadsheet['spreadsheetId']
        print(f"✅ Planilha criada: {sheet_id}")

        # 2. ADICIONAR HEADER
        print("\n2️⃣ Adicionando header...")

        header = [['Data', 'Hora', 'Vendedor', 'Status', 'Cliente', 'Veículo']]

        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Agenda!A1:F1',
            valueInputOption='USER_ENTERED',
            body={'values': header}
        ).execute()

        # Formatar header (negrito)
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [{
                    'repeatCell': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'textFormat': {'bold': True},
                                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
                            }
                        },
                        'fields': 'userEnteredFormat(textFormat,backgroundColor)'
                    }
                }]
            }
        ).execute()

        print("✅ Header adicionado")

        # 3. ADICIONAR DADOS
        print("\n3️⃣ Adicionando horários disponíveis...")

        dados = self._gerar_dados_agenda(dias_frente, vendedores, horarios)

        self.sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Agenda!A2',
            valueInputOption='USER_ENTERED',
            body={'values': dados}
        ).execute()

        print(f"✅ {len(dados)} horários adicionados")

        # 4. FORMATAR COLUNAS
        print("\n4️⃣ Formatando colunas...")

        # Ajustar largura das colunas
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [
                    # Coluna A (Data) - 120px
                    {
                        'updateDimensionProperties': {
                            'range': {'sheetId': 0, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
                            'properties': {'pixelSize': 120},
                            'fields': 'pixelSize'
                        }
                    },
                    # Coluna B (Hora) - 80px
                    {
                        'updateDimensionProperties': {
                            'range': {'sheetId': 0, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2},
                            'properties': {'pixelSize': 80},
                            'fields': 'pixelSize'
                        }
                    },
                    # Coluna C (Vendedor) - 100px
                    {
                        'updateDimensionProperties': {
                            'range': {'sheetId': 0, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3},
                            'properties': {'pixelSize': 100},
                            'fields': 'pixelSize'
                        }
                    },
                    # Coluna D (Status) - 120px
                    {
                        'updateDimensionProperties': {
                            'range': {'sheetId': 0, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4},
                            'properties': {'pixelSize': 120},
                            'fields': 'pixelSize'
                        }
                    },
                    # Coluna E (Cliente) - 150px
                    {
                        'updateDimensionProperties': {
                            'range': {'sheetId': 0, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5},
                            'properties': {'pixelSize': 150},
                            'fields': 'pixelSize'
                        }
                    },
                    # Coluna F (Veículo) - 120px
                    {
                        'updateDimensionProperties': {
                            'range': {'sheetId': 0, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6},
                            'properties': {'pixelSize': 120},
                            'fields': 'pixelSize'
                        }
                    }
                ]
            }
        ).execute()

        # 5. VALIDAÇÃO DE DADOS (Status)
        print("\n5️⃣ Adicionando validação de status...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [{
                    'setDataValidation': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 1,
                            'endRowIndex': 1000,
                            'startColumnIndex': 3,
                            'endColumnIndex': 4
                        },
                        'rule': {
                            'condition': {
                                'type': 'ONE_OF_LIST',
                                'values': [
                                    {'userEnteredValue': 'disponível'},
                                    {'userEnteredValue': 'agendado'},
                                    {'userEnteredValue': 'cancelado'},
                                    {'userEnteredValue': 'realizado'}
                                ]
                            },
                            'showCustomUi': True
                        }
                    }
                }]
            }
        ).execute()

        print("✅ Validação adicionada (coluna Status)")

        # 6. FORMATAÇÃO CONDICIONAL (Cores por Status)
        print("\n6️⃣ Adicionando formatação condicional...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [
                    # Verde para "disponível"
                    {
                        'addConditionalFormatRule': {
                            'rule': {
                                'ranges': [{'sheetId': 0, 'startRowIndex': 1, 'endRowIndex': 1000}],
                                'booleanRule': {
                                    'condition': {
                                        'type': 'TEXT_EQ',
                                        'values': [{'userEnteredValue': '=D2="disponível"'}]
                                    },
                                    'format': {
                                        'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}
                                    }
                                }
                            },
                            'index': 0
                        }
                    },
                    # Amarelo para "agendado"
                    {
                        'addConditionalFormatRule': {
                            'rule': {
                                'ranges': [{'sheetId': 0, 'startRowIndex': 1, 'endRowIndex': 1000}],
                                'booleanRule': {
                                    'condition': {
                                        'type': 'TEXT_EQ',
                                        'values': [{'userEnteredValue': '=D2="agendado"'}]
                                    },
                                    'format': {
                                        'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.8}
                                    }
                                }
                            },
                            'index': 1
                        }
                    },
                    # Azul para "realizado"
                    {
                        'addConditionalFormatRule': {
                            'rule': {
                                'ranges': [{'sheetId': 0, 'startRowIndex': 1, 'endRowIndex': 1000}],
                                'booleanRule': {
                                    'condition': {
                                        'type': 'TEXT_EQ',
                                        'values': [{'userEnteredValue': '=D2="realizado"'}]
                                    },
                                    'format': {
                                        'backgroundColor': {'red': 0.81, 'green': 0.89, 'blue': 0.95}
                                    }
                                }
                            },
                            'index': 2
                        }
                    },
                    # Vermelho para "cancelado"
                    {
                        'addConditionalFormatRule': {
                            'rule': {
                                'ranges': [{'sheetId': 0, 'startRowIndex': 1, 'endRowIndex': 1000}],
                                'booleanRule': {
                                    'condition': {
                                        'type': 'TEXT_EQ',
                                        'values': [{'userEnteredValue': '=D2="cancelado"'}]
                                    },
                                    'format': {
                                        'backgroundColor': {'red': 0.96, 'green': 0.8, 'blue': 0.8}
                                    }
                                }
                            },
                            'index': 3
                        }
                    }
                ]
            }
        ).execute()

        print("✅ Formatação condicional adicionada")

        # 7. TORNAR PÚBLICA
        print("\n7️⃣ Tornando planilha pública...")

        permission = {
            'type': 'anyone',
            'role': 'writer'  # Editor (pode editar)
        }

        self.drive_service.permissions().create(
            fileId=sheet_id,
            body=permission
        ).execute()

        print("✅ Planilha pública (qualquer pessoa com link pode editar)")

        # 8. GERAR URLs
        url_view = f"https://docs.google.com/spreadsheets/d/{sheet_id}/view"
        url_edit = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

        # Resultado
        print("\n" + "=" * 60)
        print("✅ PLANILHA CRIADA COM SUCESSO!")
        print("=" * 60)
        print(f"\n📊 ID: {sheet_id}")
        print(f"🔗 Link: {url_edit}")
        print(f"\n💾 Salvar ID no config:")
        print(f'   "google_sheet_id": "{sheet_id}"')
        print()

        return {
            'id': sheet_id,
            'url': url_view,
            'url_edit': url_edit
        }

    def _gerar_dados_agenda(
        self,
        dias_frente: int,
        vendedores: List[str],
        horarios: List[str]
    ) -> List[List[str]]:
        """Gera dados da agenda (horários disponíveis)"""

        hoje = datetime.now()
        dados = []

        for dia_offset in range(1, dias_frente + 1):
            data = hoje + timedelta(days=dia_offset)

            # Pular finais de semana (opcional)
            # if data.weekday() >= 5:  # 5=Sábado, 6=Domingo
            #     continue

            for hora in horarios:
                for vendedor in vendedores:
                    dados.append([
                        data.strftime('%d/%m/%Y'),
                        hora,
                        vendedor,
                        'disponível',
                        '',  # Cliente vazio
                        ''   # Veículo vazio
                    ])

        return dados


def main():
    parser = argparse.ArgumentParser(
        description='Cria planilha de agenda Google Sheets pública'
    )

    parser.add_argument(
        '--nome',
        type=str,
        default='Agenda Automaia',
        help='Nome da planilha (padrão: "Agenda Automaia")'
    )

    parser.add_argument(
        '--dias',
        type=int,
        default=7,
        help='Quantos dias de horários adicionar (padrão: 7)'
    )

    parser.add_argument(
        '--vendedores',
        type=str,
        default='Bruno,Fernanda',
        help='Vendedores separados por vírgula (padrão: "Bruno,Fernanda")'
    )

    parser.add_argument(
        '--horarios',
        type=str,
        default='10:00,14:00,15:00,16:00',
        help='Horários separados por vírgula (padrão: "10:00,14:00,15:00,16:00")'
    )

    args = parser.parse_args()

    if not GOOGLE_API_DISPONIVEL:
        print("❌ Google API não disponível")
        print("Instale: pip install google-api-python-client google-auth")
        return

    try:
        criador = CriadorAgendaPublica()

        vendedores = args.vendedores.split(',')
        horarios = args.horarios.split(',')

        resultado = criador.criar_planilha(
            nome=args.nome,
            dias_frente=args.dias,
            vendedores=vendedores,
            horarios=horarios
        )

        # Salvar ID no arquivo de config (opcional)
        print("🔧 Quer configurar automaticamente no bot? (s/n): ", end='')
        resposta = input().strip().lower()

        if resposta == 's':
            import json
            config_path = os.path.join(
                os.path.dirname(__file__),
                '../../chatwoot_config_automaia.json'
            )

            with open(config_path, 'r') as f:
                config = json.load(f)

            config['google_sheet_id'] = resultado['id']

            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"\n✅ ID salvo em: {config_path}")
            print("🔄 Reinicie o bot para aplicar")

    except FileNotFoundError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
