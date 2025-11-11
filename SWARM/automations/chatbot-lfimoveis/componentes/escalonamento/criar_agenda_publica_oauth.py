#!/usr/bin/env python3
"""
🚀 CRIAR AGENDA PÚBLICA - OAuth (Login Google Simples)
Versão simplificada usando OAuth (login no navegador)

USO:
    # 1. Autenticar primeiro (só 1 vez):
    python3 autenticar_google.py

    # 2. Criar planilha:
    python3 criar_agenda_publica_oauth.py
    python3 criar_agenda_publica_oauth.py --nome "Agenda 2025" --dias 14
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict
import pickle
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    GOOGLE_API_DISPONIVEL = True
except ImportError:
    print("❌ Google API não instalada")
    print("Instale: pip install google-api-python-client google-auth-httplib2")
    GOOGLE_API_DISPONIVEL = False


class CriadorAgendaPublicaOAuth:
    """Cria planilha de agenda usando OAuth"""

    HORARIOS_PADRAO = ["10:00", "14:00", "15:00", "16:00"]
    VENDEDORES_PADRAO = ["Bruno", "Fernanda"]

    def __init__(self):
        """Inicializa com credenciais OAuth"""
        if not GOOGLE_API_DISPONIVEL:
            raise RuntimeError("Google API não disponível")

        self._carregar_credenciais()

    def _carregar_credenciais(self):
        """Carrega credenciais OAuth salvas"""
        token_file = Path(__file__).parent / '../../config/google_token.pickle'

        if not token_file.exists():
            raise FileNotFoundError(
                "❌ Credenciais OAuth não encontradas!\n\n"
                "Execute primeiro:\n"
                "  python3 componentes/escalonamento/autenticar_google.py\n"
            )

        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

        # Inicializa serviços
        self.sheets_service = build('sheets', 'v4', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)

    def criar_planilha(
        self,
        nome: str = "Agenda Automaia",
        dias_frente: int = 7,
        vendedores: List[str] = None,
        horarios: List[str] = None
    ) -> Dict[str, str]:
        """
        Cria planilha completa (igual à versão Service Account)
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
                        'frozenRowCount': 1
                    }
                }
            }]
        }

        spreadsheet = self.sheets_service.spreadsheets().create(
            body=spreadsheet_body
        ).execute()

        sheet_id = spreadsheet['spreadsheetId']
        grid_id = spreadsheet['sheets'][0]['properties']['sheetId']  # ID da aba
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
        print("\n3️⃣ Adicionando horários...")

        dados = self._gerar_dados_agenda(dias_frente, vendedores, horarios)

        self.sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Agenda!A2',
            valueInputOption='USER_ENTERED',
            body={'values': dados}
        ).execute()

        print(f"✅ {len(dados)} horários adicionados")

        # 4. AJUSTAR COLUNAS
        print("\n4️⃣ Formatando colunas...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 100}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5}, 'properties': {'pixelSize': 150}, 'fields': 'pixelSize'}},
                    {'updateDimensionProperties': {'range': {'sheetId': grid_id, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}}
                ]
            }
        ).execute()

        print("✅ Colunas formatadas")

        # 5. VALIDAÇÃO STATUS
        print("\n5️⃣ Adicionando validação...")

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

        print("✅ Validação adicionada")

        # 6. CORES POR STATUS
        print("\n6️⃣ Adicionando cores...")

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="disponível"'}]}, 'format': {'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 0.83}}}}, 'index': 0}},
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="agendado"'}]}, 'format': {'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.8}}}}, 'index': 1}},
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="realizado"'}]}, 'format': {'backgroundColor': {'red': 0.81, 'green': 0.89, 'blue': 0.95}}}}, 'index': 2}},
                    {'addConditionalFormatRule': {'rule': {'ranges': [{'sheetId': grid_id, 'startRowIndex': 1, 'endRowIndex': 1000}], 'booleanRule': {'condition': {'type': 'TEXT_EQ', 'values': [{'userEnteredValue': '=D2="cancelado"'}]}, 'format': {'backgroundColor': {'red': 0.96, 'green': 0.8, 'blue': 0.8}}}}, 'index': 3}}
                ]
            }
        ).execute()

        print("✅ Cores adicionadas")

        # 7. TORNAR PÚBLICA
        print("\n7️⃣ Tornando pública...")

        permission = {'type': 'anyone', 'role': 'writer'}

        self.drive_service.permissions().create(
            fileId=sheet_id,
            body=permission
        ).execute()

        print("✅ Planilha pública!")

        # URLs
        url_edit = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

        print("\n" + "=" * 60)
        print("✅ PLANILHA CRIADA COM SUCESSO!")
        print("=" * 60)
        print(f"\n📊 ID: {sheet_id}")
        print(f"🔗 Link: {url_edit}")
        print(f"\n💾 Salvar no config:")
        print(f'   "google_sheet_id": "{sheet_id}"')
        print()

        return {
            'id': sheet_id,
            'url_edit': url_edit
        }

    def _gerar_dados_agenda(self, dias_frente, vendedores, horarios):
        """Gera dados da agenda"""
        hoje = datetime.now()
        dados = []

        for dia_offset in range(1, dias_frente + 1):
            data = hoje + timedelta(days=dia_offset)

            for hora in horarios:
                for vendedor in vendedores:
                    dados.append([
                        data.strftime('%d/%m/%Y'),
                        hora,
                        vendedor,
                        'disponível',
                        '',
                        ''
                    ])

        return dados


def main():
    parser = argparse.ArgumentParser(description='Cria planilha OAuth')

    parser.add_argument('--nome', type=str, default='Agenda Automaia')
    parser.add_argument('--dias', type=int, default=7)
    parser.add_argument('--vendedores', type=str, default='Bruno,Fernanda')
    parser.add_argument('--horarios', type=str, default='10:00,14:00,15:00,16:00')

    args = parser.parse_args()

    if not GOOGLE_API_DISPONIVEL:
        print("❌ Google API não disponível")
        print("Instale: pip install google-api-python-client google-auth-httplib2")
        return

    try:
        criador = CriadorAgendaPublicaOAuth()

        vendedores = args.vendedores.split(',')
        horarios = args.horarios.split(',')

        resultado = criador.criar_planilha(
            nome=args.nome,
            dias_frente=args.dias,
            vendedores=vendedores,
            horarios=horarios
        )

        # Configurar automaticamente
        print("🔧 Quer configurar no bot? (s/n): ", end='')
        resposta = input().strip().lower()

        if resposta == 's':
            import json
            config_path = Path(__file__).parent / '../../chatwoot_config_automaia.json'

            with open(config_path, 'r') as f:
                config = json.load(f)

            config['google_sheet_id'] = resultado['id']

            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"\n✅ ID salvo em: {config_path}")
            print("🔄 Reinicie o bot")

    except FileNotFoundError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
