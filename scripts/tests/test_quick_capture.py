#!/usr/bin/env python3
"""
Script temporário para encontrar e processar nota solta
"""

import sys
from datetime import datetime
from scripts.obsidian.obsidian_client import ObsidianClient

client = ObsidianClient()

print("🔍 Conectando ao Obsidian...")

# 1. Listar todos os arquivos
try:
    files = client.list_files()
    print(f"✅ Conectado! Total de arquivos: {len(files.get('files', []))}")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    sys.exit(1)

# 2. Filtrar notas em INBOX ou raiz (recentes)
print("\n📥 Buscando notas recentes no Inbox...\n")

inbox_files = [f for f in files.get('files', []) if '00 - Inbox' in f or f.endswith('.md')]

# Mostrar 10 mais recentes
recent = sorted(inbox_files, reverse=True)[:10]

print("🗒️  Notas recentes encontradas:\n")
for i, file in enumerate(recent, 1):
    print(f"{i}. {file}")

print("\n" + "="*60)
print("Digite o número da nota para processar (ou 0 para cancelar):")
