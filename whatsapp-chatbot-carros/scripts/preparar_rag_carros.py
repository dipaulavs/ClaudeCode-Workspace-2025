#!/usr/bin/env python3
"""
🚀 Prepara Carros para RAG Semântico

Consolida arquivos .txt de cada carro em documento único
para processamento com rag-novo
"""

from pathlib import Path
import sys

def consolidar_carro(carro_dir: Path) -> str:
    """
    Consolida todos os .txt de um carro em documento único

    Args:
        carro_dir: Diretório do carro

    Returns:
        Texto consolidado
    """
    carro_id = carro_dir.name

    # Ordem lógica dos arquivos
    arquivos = [
        ("base.txt", "INFORMAÇÕES BÁSICAS"),
        ("detalhes.txt", "DETALHES TÉCNICOS"),
        ("faq.txt", "PERGUNTAS FREQUENTES"),
        ("historico.txt", "HISTÓRICO DO VEÍCULO"),
        ("financiamento.txt", "FINANCIAMENTO")
    ]

    documento = f"# {carro_id}\n\n"
    documento += "Documento consolidado para análise semântica\n\n"
    documento += "=" * 70 + "\n\n"

    for arquivo, secao in arquivos:
        arquivo_path = carro_dir / arquivo

        if not arquivo_path.exists():
            continue

        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()

            if conteudo:
                documento += f"\n## {secao}\n\n"
                documento += conteudo + "\n\n"
                documento += "-" * 70 + "\n"

        except Exception as e:
            print(f"⚠️  Erro ao ler {arquivo}: {e}")

    return documento

def main():
    # Diretório de carros
    carros_dir = Path(__file__).parent.parent / "carros"

    if not carros_dir.exists():
        print("❌ Diretório de carros não encontrado")
        sys.exit(1)

    print("🚗 Preparando carros para RAG semântico...\n")

    carros_processados = 0

    for carro_dir in carros_dir.iterdir():
        if not carro_dir.is_dir():
            continue

        carro_id = carro_dir.name

        print(f"📝 Processando {carro_id}...")

        # Consolida documento
        documento = consolidar_carro(carro_dir)

        # Salva documento consolidado
        output_file = carro_dir / "documento_completo.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(documento)

        print(f"   ✅ Documento consolidado: {len(documento)} caracteres")
        print(f"   📄 Salvo em: {output_file}\n")

        carros_processados += 1

    print(f"✅ {carros_processados} carro(s) preparado(s)!")
    print("\n📋 Próximo passo:")
    print("   Aplicar rag-novo para quebrar semanticamente")

if __name__ == "__main__":
    main()
