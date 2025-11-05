#!/usr/bin/env python3
"""
🔧 FERRAMENTA: Lista Carros Disponíveis

Retorna lista simples dos carros cadastrados na loja.
Lê a pasta carros/ e extrai informações básicas.
"""

import json
from pathlib import Path
from typing import List, Dict


def listar_carros_disponiveis(carros_dir: Path = None) -> List[Dict]:
    """
    Lista todos os carros disponíveis na loja

    Args:
        carros_dir: Diretório dos carros (padrão: ../carros)

    Returns:
        Lista de dicts com: id, marca, modelo, ano, preco
    """
    if carros_dir is None:
        carros_dir = Path(__file__).parent.parent / "carros"

    carros = []

    # Itera por todas as pastas em carros/
    for pasta in sorted(carros_dir.iterdir()):
        if not pasta.is_dir():
            continue

        # Ignora pastas ocultas
        if pasta.name.startswith('.'):
            continue

        carro_id = pasta.name
        base_file = pasta / "base.txt"

        if not base_file.exists():
            continue

        # Lê base.txt para extrair informações
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # Extrai informações básicas
            info = {
                "id": carro_id,
                "marca": _extrair_campo(conteudo, "Marca"),
                "modelo": _extrair_campo(conteudo, "Modelo"),
                "ano": _extrair_campo(conteudo, "Ano"),
                "preco": _extrair_preco(conteudo),
                "cor": _extrair_campo(conteudo, "Cor"),
                "km": _extrair_campo(conteudo, "Kilometragem")
            }

            carros.append(info)

        except Exception as e:
            print(f"⚠️ Erro ao ler {carro_id}: {e}")
            continue

    return carros


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

    # Padrão: • À vista: R$ 45.000
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


def formatar_lista_para_mensagem(carros: List[Dict]) -> str:
    """
    Formata lista de carros para mensagem amigável

    Args:
        carros: Lista retornada por listar_carros_disponiveis()

    Returns:
        String formatada para WhatsApp
    """
    if not carros:
        return "No momento não temos carros disponíveis."

    msg = f"📋 Temos {len(carros)} carros disponíveis:\n\n"

    for i, carro in enumerate(carros, 1):
        marca = carro.get("marca", "")
        modelo = carro.get("modelo", "")
        ano = carro.get("ano", "")
        preco = carro.get("preco", "")

        linha = f"{i}. "

        if marca and modelo:
            linha += f"{marca} {modelo}"
        elif marca:
            linha += marca
        elif modelo:
            linha += modelo
        else:
            linha += carro["id"]

        if ano:
            linha += f" {ano}"

        if preco:
            linha += f" - {preco}"

        msg += linha + "\n"

    return msg.strip()


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando lista_carros.py...\n")

    carros = listar_carros_disponiveis()

    print(f"✅ {len(carros)} carros encontrados:\n")

    for carro in carros:
        print(f"  • {carro['marca']} {carro['modelo']} {carro['ano']} - {carro['preco']}")

    print("\n📱 Mensagem formatada:\n")
    print(formatar_lista_para_mensagem(carros))
