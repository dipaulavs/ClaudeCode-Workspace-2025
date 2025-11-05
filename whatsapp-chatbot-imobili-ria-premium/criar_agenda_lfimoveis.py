#!/usr/bin/env python3
"""
🏠 CRIAR AGENDA LF IMÓVEIS - Intervalo 2h entre visitas
Cria planilha Google Sheets com horários espaçados
"""

import sys
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import json

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    GOOGLE_API_DISPONIVEL = True
except ImportError:
    print("❌ Google API não instalada")
    print("Instale: pip install google-api-python-client google-auth-httplib2")
    sys.exit(1)


class CriadorAgendaLFImoveis:
    """Cria agenda para LF Imóveis com intervalo de 2h"""

    # Horários com intervalo de 2h
    HORARIOS_PADRAO = [
        "09:00",
        "11:00",
        "13:00",
        "15:00",
        "17:00"
    ]

    CORRETORES_PADRAO = ["Lucas", "Fernanda", "Roberto"]

    def __init__(self):
        """Inicializa com credenciais OAuth"""
        self._carregar_credenciais()

    def _carregar_credenciais(self):
        """Carrega credenciais OAuth salvas"""
        token_file = Path(__file__).parent / 'config/google_token.pickle'

        if not token_file.exists():
            print("❌ Credenciais OAuth não encontradas!")
            print("\nExecute primeiro:")
            print("  python3 componentes/escalonamento/autenticar_google.py")
            sys.exit(1)

        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

        # Inicializa serviços
        self.sheets_service = build('sheets', 'v4', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)

    def _gerar_dados_agenda(
        self,
        dias_frente: int,
        corretores: List[str],
        horarios: List[str]
    ) -> List[List[str]]:
        """Gera linhas da agenda com intervalo de 2h"""
        dados = []
        hoje = datetime.now()

        for dia_offset in range(dias_frente):
            data = hoje + timedelta(days=dia_offset)

            # Pula finais de semana
            if data.weekday() >= 5:  # 5=sábado, 6=domingo
                continue

            data_str = data.strftime('%d/%m/%Y')

            for horario in horarios:
                for corretor in corretores:
                    dados.append([
                        data_str,
                        horario,
                        corretor,
                        'disponível',
                        '',  # Cliente
                        ''   # Imóvel
                    ])

        return dados

    def criar_planilha(
        self,
        nome: str = "Agenda LF Imóveis",
        dias_frente: int = 14,
        corretores: List[str] = None,
        horarios: List[str] = None
    ) -> Dict[str, str]:
        """Cria planilha completa de agenda"""

        if corretores is None:
            corretores = self.CORRETORES_PADRAO

        if horarios is None:
            horarios = self.HORARIOS_PADRAO

        print("\n" + "=" * 60)
        print("🏠 CRIANDO AGENDA LF IMÓVEIS")
        print("=" * 60)
        print(f"📝 Nome: {nome}")
        print(f"📅 Dias: {dias_frente}")
        print(f"👥 Corretores: {', '.join(corretores)}")
        print(f"⏰ Horários (intervalo 2h): {', '.join(horarios)}")
        print()

        # 1. CRIAR PLANILHA
        print("1️⃣  Criando planilha...")

        spreadsheet_body = {
            'properties': {
                'title': nome
            },
            'sheets': [{
                'properties': {
                    'title': 'Agenda',
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                }
            }]
        }

        spreadsheet = self.sheets_service.spreadsheets().create(
            body=spreadsheet_body
        ).execute()

        sheet_id = spreadsheet['spreadsheetId']
        grid_id = spreadsheet['sheets'][0]['properties']['sheetId']
        print(f"   ✅ Planilha criada: {sheet_id}")

        # 2. ADICIONAR HEADER
        print("\n2️⃣  Adicionando header...")

        header = [['Data', 'Hora', 'Corretor', 'Status', 'Cliente', 'Imóvel']]

        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Agenda!A1:F1',
            valueInputOption='USER_ENTERED',
            body={'values': header}
        ).execute()

        # Formatar header
        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [{
                    'repeatCell': {
                        'range': {
                            'sheetId': grid_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'textFormat': {'bold': True, 'fontSize': 11},
                                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.7},
                                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                            }
                        },
                        'fields': 'userEnteredFormat(textFormat,backgroundColor)'
                    }
                }]
            }
        ).execute()

        print("   ✅ Header adicionado")

        # 3. ADICIONAR DADOS
        print("\n3️⃣  Adicionando horários...")

        dados = self._gerar_dados_agenda(dias_frente, corretores, horarios)

        self.sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Agenda!A2',
            valueInputOption='USER_ENTERED',
            body={'values': dados}
        ).execute()

        print(f"   ✅ {len(dados)} horários adicionados")

        # 4. AJUSTAR COLUNAS
        print("\n4️⃣  Formatando colunas...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 110}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5}, 'properties': {'pixelSize': 200}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6}, 'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}}
                ]
            }
        ).execute()

        print("   ✅ Colunas formatadas")

        # 5. VALIDAÇÃO STATUS
        print("\n5️⃣  Adicionando validação...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [{
                    'setDataValidation': {
                        'range': {'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000, 'startColumnIndex': 3, 'endColumnIndex': 4},
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

        print("   ✅ Validação adicionada")

        # 6. CORES POR STATUS
        print("\n6️⃣  Adicionando cores...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [
                    # Verde claro: disponível
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="disponível"'}]}, 'format': {'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}}}}, 'index': 0}},
                    # Amarelo: agendado
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="agendado"'}]}, 'format': {'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.8}}}}, 'index': 1}},
                    # Azul: realizado
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="realizado"'}]}, 'format': {'backgroundColor': {'red': 0.81, 'green': 0.89, 'blue': 0.95}}}}, 'index': 2}},
                    # Vermelho: cancelado
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="cancelado"'}]}, 'format': {'backgroundColor': {'red': 0.96, 'green': 0.8, 'blue': 0.8}}}}, 'index': 3}}
                ]
            }
        ).execute()

        print("   ✅ Cores adicionadas")

        # 7. TORNAR PÚBLICA
        print("\n7️⃣  Tornando pública...")

        permission = {'type': 'anyone', 'role': 'writer'}

        self.drive_service.permissions().create(
            fileId=sheet_id,
            body=permission
        ).execute()

        print("   ✅ Planilha pública!")

        # URLs
        url_edit = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

        print("\n" + "=" * 60)
        print("✅ AGENDA CRIADA COM SUCESSO!")
        print("=" * 60)
        print(f"\n📊 ID: {sheet_id}")
        print(f"🔗 Link: {url_edit}")
        print(f"\n⏰ Intervalo entre visitas: 2 horas")
        print(f"📅 Total de horários: {len(dados)}")

        # 8. ATUALIZAR CONFIG
        print("\n8️⃣  Atualizando configuração...")
        config_file = Path(__file__).parent / 'chatwoot_config_imobili-ria-premium.json'

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            config['google_sheet_id'] = sheet_id

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"   ✅ Config atualizado: {config_file.name}")
        except Exception as e:
            print(f"   ⚠️  Erro ao atualizar config: {e}")
            print(f"   💡 Adicione manualmente o sheet_id ao config")

        print("\n" + "=" * 60)
        print("🎉 TUDO PRONTO!")
        print("=" * 60)
        print("\n📋 Próximos passos:")
        print("   1. Abra o link acima e teste a agenda")
        print("   2. Inicie o bot: ./INICIAR_COM_NGROK.sh")
        print("   3. Teste agendamento via WhatsApp")
        print()

        return {
            'spreadsheet_id': sheet_id,
            'url': url_edit
        }


def main():
    print("\n🏠 CRIADOR DE AGENDA - LF IMÓVEIS")
    print("Intervalo de 2h entre visitas\n")

    try:
        criador = CriadorAgendaLFImoveis()

        # Criar agenda
        resultado = criador.criar_planilha(
            nome="Agenda LF Imóveis - 2025",
            dias_frente=21,  # 3 semanas
            corretores=["Lucas", "Fernanda", "Roberto"],
            horarios=["09:00", "11:00", "13:00", "15:00", "17:00"]
        )

        print(f"\n💾 Sheet ID salvo: {resultado['spreadsheet_id']}")

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao criar agenda: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
