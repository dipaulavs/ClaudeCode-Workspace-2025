from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'config/google_service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

print("🔑 Carregando credenciais...")
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

print("📋 Criando serviço Google Sheets...")
service = build('sheets', 'v4', credentials=credentials)

print("✅ Conexão estabelecida!")
print(f"📧 Service Account: {credentials.service_account_email}")

# Testar criando planilha simples
print("\n🧪 Testando criação de planilha...")
spreadsheet = {
    'properties': {'title': 'Teste Conexão API'},
    'sheets': [{'properties': {'title': 'Teste'}}]
}

result = service.spreadsheets().create(body=spreadsheet).execute()
print(f"✅ Planilha teste criada: {result['spreadsheetId']}")
print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{result['spreadsheetId']}")

# Deletar planilha teste
print("\n🗑️ Limpando teste...")
drive_service = build('drive', 'v3', credentials=credentials)
drive_service.files().delete(fileId=result['spreadsheetId']).execute()
print("✅ Teste completo!")
