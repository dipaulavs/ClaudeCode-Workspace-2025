#!/usr/bin/env python3
"""
🔧 FERRAMENTA GENÉRICA: Lista Itens Disponíveis

⚠️ CUSTOMIZAR para seu negócio:
- Renomear: imoveis → carros/imoveis/produtos
- Ajustar campos extraídos conforme sua estrutura
- Customizar formatação da mensagem

ESTRUTURA ESPERADA:
imoveis/
├── imóvel-001/
│   ├── base.txt      (informações principais)
│   ├── faq.txt       (perguntas frequentes)
│   └── links.json    (fotos, vídeos)
"""

import json
from pathlib import Path
from typing import List, Dict


def listar_imoveis_disponiveis(imoveis_dir: Path = None) -> List[Dict]:
    """
    Lista todos os imoveis disponíveis

    Args:
        imoveis_dir: Diretório dos imoveis (padrão: ../imoveis)

    Returns:
        Lista de dicts com informações dos imoveis

    Exemplo de retorno:
        [
            {
                "id": "imóvel-001",
                "nome": "Produto X",
                "preco": "R$ 10.000",
                "categoria": "Categoria A",
                ...campos customizados...
            }
        ]
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

        imóvel_id = pasta.name
        base_file = pasta / "base.txt"

        if not base_file.exists():
            continue

        # Lê base.txt para extrair informações
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # ⚠️ CUSTOMIZAR: Ajuste campos conforme seu negócio
            info = {
                "id": imóvel_id,

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
                "nome": _extrair_nome(conteudo),  # Nome completo do imóvel
            }

            imoveis.append(info)

        except Exception as e:
            print(f"⚠️ Erro ao ler {imóvel_id}: {e}")
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
    Extrai nome completo do imóvel (primeira linha)

    Exemplo: "🚗 Volkswagen Gol 1.0 2020"
    """
    primeira_linha = texto.split('\n')[0].strip()
    # Remove emojis
    import re
    nome_limpo = re.sub(r'[^\w\s.-]', '', primeira_linha).strip()
    return nome_limpo


def formatar_lista_para_mensagem(imoveis: List[Dict], tipo_imóvel: str = "imoveis") -> str:
    """
    Formata lista de imoveis para mensagem amigável

    Args:
        imoveis: Lista retornada por listar_imoveis_disponiveis()
        tipo_imóvel: Tipo de imóvel (ex: "carros", "imóveis", "produtos")

    Returns:
        String formatada para WhatsApp
    """
    if not imoveis:
        return f"No momento não temos {tipo_imóvel} disponíveis."

    msg = f"📋 Temos {len(imoveis)} {tipo_imóvel} disponíveis:\n\n"

    for i, imóvel in enumerate(imoveis, 1):
        # ⚠️ CUSTOMIZAR: Ajuste campos exibidos
        linha = f"{i}. "

        # Exemplo: Carros
        if 'marca' in imóvel and 'modelo' in imóvel:
            linha += f"{imóvel['marca']} {imóvel['modelo']}"
            if imóvel.get('ano'):
                linha += f" {imóvel['ano']}"

        # Exemplo: Imóveis (descomente se usar)
        # elif 'tipo' in imóvel and 'bairro' in imóvel:
        #     linha += f"{imóvel['tipo']} - {imóvel['bairro']}"
        #     if imóvel.get('quartos'):
        #         linha += f" ({imóvel['quartos']} quartos)"

        # Fallback genérico
        elif 'nome' in imóvel:
            linha += imóvel['nome']
        else:
            linha += imóvel["id"]

        # Preço (comum a todos)
        if imóvel.get('preco'):
            linha += f" - {imóvel['preco']}"

        msg += linha + "\n"

    return msg.strip()


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando lista_imoveis.py...\n")

    imoveis = listar_imoveis_disponiveis()

    print(f"✅ {len(imoveis)} imoveis encontrados:\n")

    for imóvel in imoveis:
        print(f"  • {imóvel.get('nome', imóvel['id'])} - {imóvel.get('preco', 'N/A')}")

    print("\n📱 Mensagem formatada:\n")
    print(formatar_lista_para_mensagem(imoveis, "imoveis"))
