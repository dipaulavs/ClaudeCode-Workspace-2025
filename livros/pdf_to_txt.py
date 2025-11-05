#!/usr/bin/env python3
"""
Converte PDF para TXT para processamento posterior
"""

import sys
from pathlib import Path
from PyPDF2 import PdfReader

def pdf_to_txt(pdf_path):
    """Extrai texto de PDF e salva como TXT"""
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        return None

    print(f"📄 Lendo PDF: {pdf_path.name}")
    print(f"📦 Tamanho: {pdf_path.stat().st_size / 1024 / 1024:.1f} MB")

    # Ler PDF
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"📖 Total de páginas: {total_pages}")

    # Extrair texto
    print("⏳ Extraindo texto...")
    text = ""
    for i, page in enumerate(reader.pages, 1):
        text += page.extract_text() + "\n\n"
        if i % 10 == 0:
            print(f"   Processando: {i}/{total_pages} páginas...")

    # Salvar TXT
    txt_path = pdf_path.with_suffix('.txt')
    txt_path.write_text(text, encoding='utf-8')

    # Estatísticas
    lines = text.count('\n')
    words = len(text.split())

    print(f"✅ Convertido com sucesso!")
    print(f"📝 Arquivo TXT: {txt_path.name}")
    print(f"📊 Linhas: {lines:,}")
    print(f"📊 Palavras: {words:,}")
    print(f"💾 Tamanho TXT: {txt_path.stat().st_size / 1024:.1f} KB")

    return txt_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 pdf_to_txt.py <arquivo.pdf>")
        sys.exit(1)

    pdf_to_txt(sys.argv[1])
