#!/usr/bin/env python3
"""
🔐 AUTENTICAÇÃO GOOGLE - OAuth Simples
Login direto no navegador, clica "Autorizar" e pronto!

USO:
    python3 autenticar_google.py
"""

import os
import sys
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    GOOGLE_AUTH_DISPONIVEL = True
except ImportError:
    print("❌ Google Auth não instalada")
    print("Instale: pip install google-auth-oauthlib google-auth-httplib2")
    GOOGLE_AUTH_DISPONIVEL = False


# Escopos necessários
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]


def autenticar_oauth():
    """
    Autentica via OAuth (login Google no navegador)

    Fluxo:
    1. Abre navegador
    2. Login com sua conta Google
    3. Clica "Autorizar"
    4. Salva credenciais
    """

    print("\n" + "=" * 60)
    print("🔐 AUTENTICAÇÃO GOOGLE - OAuth")
    print("=" * 60)
    print()

    creds = None
    token_file = Path(__file__).parent / '../../config/google_token.pickle'
    credentials_file = Path(__file__).parent / '../../config/google_credentials.json'

    # Criar pasta config se não existir
    token_file.parent.mkdir(exist_ok=True, parents=True)

    # Verifica se já tem token salvo
    if token_file.exists():
        print("📝 Token existente encontrado...")
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # Se não tem credenciais válidas, autentica
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token expirado...")
            try:
                creds.refresh(Request())
                print("✅ Token renovado!")
            except Exception as e:
                print(f"⚠️ Erro ao renovar: {e}")
                creds = None

        # Precisa fazer login
        if not creds:
            # Verifica se tem arquivo de credenciais OAuth
            if not credentials_file.exists():
                print("\n❌ Arquivo de credenciais não encontrado!")
                print(f"   Esperado: {credentials_file}")
                print()
                print("🎯 COMO OBTER (2 minutos):")
                print()
                print("1. Acesse: https://console.cloud.google.com")
                print("2. Criar projeto (ex: 'automaia-bot')")
                print("3. Habilitar APIs:")
                print("   - Google Sheets API")
                print("   - Google Drive API")
                print("4. Criar credenciais:")
                print("   - APIs e Serviços → Credenciais")
                print("   - + CRIAR CREDENCIAIS → ID do cliente OAuth")
                print("   - Tipo: Aplicativo para computador")
                print("   - Nome: 'Automaia Desktop'")
                print("   - CRIAR")
                print("5. Baixar JSON:")
                print("   - Clicar no ícone de download (⬇️)")
                print("   - Salvar como: config/google_credentials.json")
                print()
                print("6. Rodar este script novamente")
                print()
                return False

            print("🌐 Autenticando via OAuth...")
            print()

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file),
                    SCOPES
                )

                print("👉 Abrindo navegador automaticamente...")
                print("   Se não abrir, copie a URL que aparecer abaixo")
                print()

                creds = flow.run_local_server(port=0, open_browser=True)

                print("\n✅ Autenticação concluída!")

            except Exception as e:
                print(f"\n❌ Erro ao autenticar: {e}")
                return False

        # Salva token para próxima vez
        print("💾 Salvando credenciais...")
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

        print(f"✅ Token salvo: {token_file}")

    else:
        print("✅ Credenciais válidas encontradas!")

    print()
    print("=" * 60)
    print("🎉 AUTENTICAÇÃO COMPLETA!")
    print("=" * 60)
    print()
    print("Agora você pode usar:")
    print("  python3 componentes/escalonamento/criar_agenda_publica_oauth.py")
    print()

    return True


def main():
    if not GOOGLE_AUTH_DISPONIVEL:
        print("\n❌ Dependências faltando")
        print("Instale:")
        print("  pip install google-auth-oauthlib google-auth-httplib2")
        return

    sucesso = autenticar_oauth()

    if not sucesso:
        print("⚠️ Autenticação não concluída")
        print("Siga as instruções acima e tente novamente")
        sys.exit(1)


if __name__ == '__main__':
    main()
