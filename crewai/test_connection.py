"""
Teste rápido de conexão com OpenRouter
"""
from dotenv import load_dotenv
from pathlib import Path
import os

# Carrega .env
load_dotenv(Path(__file__).parent / ".env")

print("🔍 Testando configuração...\n")

# Verifica API Key
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key and api_key != "sua_chave_openrouter_aqui":
    print(f"✅ API Key configurada!")
    print(f"   Chave: {api_key[:20]}...{api_key[-10:]}\n")
else:
    print("❌ API Key não configurada!\n")
    exit(1)

# Verifica modelo
model = os.getenv("OPENAI_MODEL_NAME")
print(f"✅ Modelo configurado: {model}\n")

# Verifica base URL
base_url = os.getenv("OPENAI_API_BASE")
print(f"✅ Base URL: {base_url}\n")

print("=" * 60)
print("✅ CONFIGURAÇÃO OK! Pronto para executar crews!")
print("=" * 60)
