#!/usr/bin/env python3
"""
🔧 FERRAMENTA GENÉRICA: Lista Itens Disponíveis

⚠️ CUSTOMIZAR para seu negócio:
- Renomear: itens → carros/imoveis/produtos
- Ajustar campos extraídos conforme sua estrutura
- Customizar formatação da mensagem

ESTRUTURA ESPERADA:
itens/
├── item-001/
│   ├── base.txt      (informações principais)
│   ├── faq.txt       (perguntas frequentes)
│   └── links.json    (fotos, vídeos)
"""

import json
from pathlib import Path
from typing import List, Dict


def listar_itens_disponiveis(itens_dir: Path = None) -> List[Dict]:
    """
    Lista todos os itens disponíveis

    Args:
        itens_dir: Diretório dos itens (padrão: ../itens)

    Returns:
        Lista de dicts com informações dos itens

    Exemplo de retorno:
        [
            {
                "id": "item-001",
                "nome": "Produto X",
                "preco": "R$ 10.000",
                "categoria": "Categoria A",
                ...campos customizados...
            }
        ]
    """
    if itens_dir is None:
        itens_dir = Path(__file__).parent.parent / "itens"

    itens = []

    # Itera por todas as pastas em itens/
    for pasta in sorted(itens_dir.iterdir()):
        if not pasta.is_dir():
            continue

        # Ignora pastas ocultas
        if pasta.name.startswith('.'):
            continue

        item_id = pasta.name
        base_file = pasta / "base.txt"

        if not base_file.exists():
            continue

        # Lê base.txt para extrair informações
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # ⚠️ CUSTOMIZAR: Ajuste campos conforme seu negócio
            info = {
                "id": item_id,

                # EXEMPLO: Carros
                "marca": _extrair_campo(conteudo, "Marca"),
                "modelo": _extrair_campo(conteudo, "Modelo"),
                "ano": _extrair_campo(conteudo, "Ano"),
                "cor": _extrair_campo(conteudo, "Cor"),
                "km": _extrair_campo(conteudo, "Kilometragem"),

                # EXEMPLO: Imóveis (descomente se usar)
                # "tipo": _extrair_campo(conteudo, "Tipo"),  # Casa, Apto, Lote
                # "quartos": _extrair_campo(conteudo, "Quartos"),
                # "area": _extrair_campo(conteudo, "Área"),
                # "bairro": _extrair_campo(conteudo, "Bairro"),

                # COMUM A TODOS
                "preco": _extrair_preco(conteudo),
                "nome": _extrair_nome(conteudo),  # Nome completo do item
            }

            itens.append(info)

        except Exception as e:
            print(f"⚠️ Erro ao ler {item_id}: {e}")
            continue

    return itens


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


def _extrair_nome(texto: str) -> str:
    """
    Extrai nome completo do item (primeira linha)

    Exemplo: "🚗 Volkswagen Gol 1.0 2020"
    """
    primeira_linha = texto.split('\n')[0].strip()
    # Remove emojis
    import re
    nome_limpo = re.sub(r'[^\w\s.-]', '', primeira_linha).strip()
    return nome_limpo


def formatar_lista_para_mensagem(itens: List[Dict], tipo_item: str = "itens") -> str:
    """
    Formata lista de itens para mensagem amigável

    Args:
        itens: Lista retornada por listar_itens_disponiveis()
        tipo_item: Tipo de item (ex: "carros", "imóveis", "produtos")

    Returns:
        String formatada para WhatsApp
    """
    if not itens:
        return f"No momento não temos {tipo_item} disponíveis."

    msg = f"📋 Temos {len(itens)} {tipo_item} disponíveis:\n\n"

    for i, item in enumerate(itens, 1):
        # ⚠️ CUSTOMIZAR: Ajuste campos exibidos
        linha = f"{i}. "

        # Exemplo: Carros
        if 'marca' in item and 'modelo' in item:
            linha += f"{item['marca']} {item['modelo']}"
            if item.get('ano'):
                linha += f" {item['ano']}"

        # Exemplo: Imóveis (descomente se usar)
        # elif 'tipo' in item and 'bairro' in item:
        #     linha += f"{item['tipo']} - {item['bairro']}"
        #     if item.get('quartos'):
        #         linha += f" ({item['quartos']} quartos)"

        # Fallback genérico
        elif 'nome' in item:
            linha += item['nome']
        else:
            linha += item["id"]

        # Preço (comum a todos)
        if item.get('preco'):
            linha += f" - {item['preco']}"

        msg += linha + "\n"

    return msg.strip()


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando lista_itens.py...\n")

    itens = listar_itens_disponiveis()

    print(f"✅ {len(itens)} itens encontrados:\n")

    for item in itens:
        print(f"  • {item.get('nome', item['id'])} - {item.get('preco', 'N/A')}")

    print("\n📱 Mensagem formatada:\n")
    print(formatar_lista_para_mensagem(itens, "itens"))
