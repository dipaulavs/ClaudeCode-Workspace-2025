#!/usr/bin/env python3
"""
🔧 FERRAMENTA: Lista Imóveis Disponíveis

Retorna lista simples dos imóveis cadastrados na loja.
Lê a pasta imoveis/ e extrai informações básicas.
"""

import json
from pathlib import Path
from typing import List, Dict


def listar_imoveis_disponiveis(imoveis_dir: Path = None) -> List[Dict]:
    """
    Lista todos os imóveis disponíveis na loja

    Args:
        imoveis_dir: Diretório dos imóveis (padrão: ../imoveis)

    Returns:
        Lista de dicts com: id, tipo, bairro, quartos, preço
    """
    if imoveis_dir is None:
        imoveis_dir = Path(__file__).parent.parent / "imoveis"

    imoveis = []

    # Itera por todas as pastas em imoveis/
    for pasta in sorted(imoveis_dir.iterdir()):
        if not pasta.is_dir():
            continue

        # Ignora pastas ocultas
        if pasta.name.startswith('.'):
            continue

        imovel_id = pasta.name
        base_file = pasta / "base.txt"

        if not base_file.exists():
            continue

        # Lê base.txt para extrair informações
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # Extrai informações básicas
            info = {
                "id": imovel_id,
                "tipo": _extrair_campo(conteudo, "Tipo"),
                "bairro": _extrair_campo(conteudo, "Bairro"),
                "quartos": _extrair_campo(conteudo, "Quartos"),
                "preco": _extrair_preco(conteudo),
                "area": _extrair_campo(conteudo, "Área"),
                "endereco": _extrair_campo(conteudo, "Endereço")
            }

            imoveis.append(info)

        except Exception as e:
            print(f"⚠️ Erro ao ler {imovel_id}: {e}")
            continue

    return imoveis


def _extrair_campo(texto: str, campo: str) -> str:
    """Extrai valor de um campo no formato '• Campo: Valor'"""
    import re

    # Padrão: • Campo: Valor
    padrao = rf"•\s*{campo}:\s*(.+?)(?:\n|$)"
    match = re.search(padrao, texto, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def _extrair_preco(texto: str) -> str:
    """Extrai preço à vista"""
    import re

    # Padrão: • À vista: R$ 450.000
    padrao = r"•\s*À vista:\s*R\$\s*([\d.,]+)"
    match = re.search(padrao, texto, re.IGNORECASE)

    if match:
        preco_str = match.group(1).replace(".", "").replace(",", "")
        try:
            preco_int = int(preco_str)
            return f"R$ {preco_int:,}".replace(",", ".")
        except:
            return match.group(1)

    return ""


def formatar_lista_para_mensagem(imoveis: List[Dict]) -> str:
    """
    Formata lista de imóveis para mensagem amigável

    Args:
        imoveis: Lista retornada por listar_imoveis_disponiveis()

    Returns:
        String formatada para WhatsApp
    """
    if not imoveis:
        return "No momento não temos imóveis disponíveis."

    msg = f"🏠 Temos {len(imoveis)} imóveis disponíveis:\n\n"

    for i, imovel in enumerate(imoveis, 1):
        tipo = imovel.get("tipo", "")
        bairro = imovel.get("bairro", "")
        quartos = imovel.get("quartos", "")
        preco = imovel.get("preco", "")

        linha = f"{i}. "

        if tipo:
            linha += f"{tipo}"
        else:
            linha += "Imóvel"

        if bairro:
            linha += f" - {bairro}"

        if quartos:
            linha += f" ({quartos})"

        if preco:
            linha += f" - {preco}"

        msg += linha + "\n"

    return msg.strip()


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando lista_imoveis.py...\n")

    imoveis = listar_imoveis_disponiveis()

    print(f"✅ {len(imoveis)} imóveis encontrados:\n")

    for imovel in imoveis:
        print(f"  • {imovel['tipo']} - {imovel['bairro']} ({imovel['quartos']}) - {imovel['preco']}")

    print("\n📱 Mensagem formatada:\n")
    print(formatar_lista_para_mensagem(imoveis))
