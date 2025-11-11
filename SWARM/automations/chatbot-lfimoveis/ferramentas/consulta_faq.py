#!/usr/bin/env python3
"""
🔧 FERRAMENTA: Consulta FAQ do Carro

Busca resposta no FAQ do carro ativo.
Lê base.txt + faq.txt e retorna informações relevantes.
"""

from pathlib import Path
from typing import Dict, Optional


def consultar_faq_carro(carro_id: str, pergunta: str = "", carros_dir: Path = None) -> Dict:
    """
    Consulta FAQ de um carro específico

    Args:
        carro_id: ID do carro (ex: "gol-2020-001")
        pergunta: Pergunta do cliente (opcional - se vazio, retorna tudo)
        carros_dir: Diretório dos carros (padrão: ../carros)

    Returns:
        Dict com:
            - sucesso: bool
            - carro_id: str
            - base: str (info básica do carro)
            - faq: str (FAQ completo ou filtrado)
            - erro: str (se houver)
    """
    if carros_dir is None:
        carros_dir = Path(__file__).parent.parent / "carros"

    carro_path = carros_dir / carro_id

    # Verifica se carro existe
    if not carro_path.exists():
        return {
            "sucesso": False,
            "carro_id": carro_id,
            "erro": f"Carro {carro_id} não encontrado"
        }

    resultado = {
        "sucesso": True,
        "carro_id": carro_id,
        "base": "",
        "faq": "",
        "erro": ""
    }


def consultar_faq_imovel(imovel_id: str, pergunta: str = "", imoveis_dir: Path = None) -> Dict:
    """
    Alias para imóveis - consulta FAQ de um imóvel específico

    Args:
        imovel_id: ID do imóvel (ex: "chacara-itatiaiucu-001")
        pergunta: Pergunta do cliente (opcional - se vazio, retorna tudo)
        imoveis_dir: Diretório dos imóveis (padrão: ../imoveis)

    Returns:
        Dict com:
            - sucesso: bool
            - base: str (info básica do imóvel)
            - faq: str (FAQ completo ou filtrado)
            - erro: str (se houver)
    """
    if imoveis_dir is None:
        imoveis_dir = Path(__file__).parent.parent / "imoveis"

    imovel_path = imoveis_dir / imovel_id

    # Verifica se imóvel existe
    if not imovel_path.exists():
        return {
            "sucesso": False,
            "erro": f"Imóvel {imovel_id} não encontrado"
        }

    resultado = {
        "sucesso": True,
        "base": "",
        "faq": "",
        "erro": ""
    }

    # Lê base.txt (sempre)
    base_file = imovel_path / "base.txt"
    if base_file.exists():
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                resultado["base"] = f.read().strip()
        except Exception as e:
            resultado["erro"] += f"Erro ao ler base.txt: {e}\n"

    # Lê faq.txt
    faq_file = imovel_path / "faq.txt"
    if faq_file.exists():
        try:
            with open(faq_file, 'r', encoding='utf-8') as f:
                faq_completo = f.read().strip()

            # Se tem pergunta específica, tenta filtrar FAQ
            if pergunta:
                faq_filtrado = _filtrar_faq_relevante(faq_completo, pergunta)
                resultado["faq"] = faq_filtrado if faq_filtrado else faq_completo
            else:
                resultado["faq"] = faq_completo

        except Exception as e:
            resultado["erro"] += f"Erro ao ler faq.txt: {e}\n"

    # Se deu tudo certo
    if not resultado["erro"]:
        return resultado

    # Se teve erro
    resultado["sucesso"] = False
    return resultado


def _filtrar_faq_relevante(faq: str, pergunta: str) -> str:
    """
    Filtra perguntas do FAQ que são relevantes para a pergunta do cliente

    Args:
        faq: FAQ completo
        pergunta: Pergunta do cliente

    Returns:
        FAQ filtrado (apenas perguntas relevantes) ou string vazia se nada for relevante
    """
    pergunta_lower = pergunta.lower()

    # Palavras-chave para cada tópico do FAQ
    keywords = {
        "troca": ["troca", "trocar", "aceita troca", "dou meu carro"],
        "garantia": ["garantia", "cobertura", "defeito"],
        "financiamento": ["financiamento", "financiar", "parcela", "entrada", "crédito", "banco"],
        "test drive": ["test drive", "testar", "dirigir", "experimentar"],
        "revisão": ["revisão", "revisado", "manutenção", "mecânico"],
        "problema": ["problema", "defeito", "avaria", "batida", "sinistro"],
        "ipva": ["ipva", "licenciamento", "documento", "taxa"],
        "consumo": ["consumo", "gasta", "economia", "km/l", "litro"],
        "ar condicionado": ["ar condicionado", "ar", "climatizador"],
        "chave": ["chave", "reserva", "telecomando"],
        "dono": ["dono", "proprietário", "antigo dono"],
        "acidente": ["acidente", "batida", "colisão"],
        "vendendo": ["vendendo", "vender", "motivo"],
        "transferência": ["transferência", "transferir", "despachante"],
        "multimídia": ["multimídia", "carplay", "android", "bluetooth", "som"],
        "banco": ["banco", "couro", "estofado"],
        "teto": ["teto", "teto solar", "panorâmico"],
        "tração": ["tração", "4x4", "4x2"],
        "motor": ["motor", "potência", "cv", "cilindradas"]
    }

    # Encontra palavras-chave relevantes
    topicos_relevantes = []
    for topico, palavras in keywords.imóvels():
        if any(palavra in pergunta_lower for palavra in palavras):
            topicos_relevantes.append(topico)

    # Se não encontrou nenhum tópico, retorna vazio (usa FAQ completo)
    if not topicos_relevantes:
        return ""

    # Divide FAQ em blocos (cada bloco começa com 🔹)
    blocos = []
    bloco_atual = ""

    for linha in faq.split('\n'):
        if linha.strip().startswith('🔹'):
            if bloco_atual:
                blocos.append(bloco_atual.strip())
            bloco_atual = linha
        else:
            bloco_atual += "\n" + linha

    # Adiciona último bloco
    if bloco_atual:
        blocos.append(bloco_atual.strip())

    # Filtra blocos relevantes
    blocos_relevantes = []
    for bloco in blocos:
        bloco_lower = bloco.lower()
        if any(topico in bloco_lower for topico in topicos_relevantes):
            blocos_relevantes.append(bloco)

    if blocos_relevantes:
        return "\n\n".join(blocos_relevantes)

    return ""


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando consulta_faq.py...\n")

    # Teste 1: FAQ completo
    print("📋 Teste 1: FAQ completo (sem pergunta)")
    print("-" * 50)

    resultado = consultar_faq_carro("gol-2020-001")

    if resultado["sucesso"]:
        print(f"✅ Carro: {resultado['carro_id']}")
        print(f"\n📄 Base ({len(resultado['base'])} chars):")
        print(resultado['base'][:200] + "...")
        print(f"\n❓ FAQ ({len(resultado['faq'])} chars):")
        print(resultado['faq'][:300] + "...")
    else:
        print(f"❌ Erro: {resultado['erro']}")

    # Teste 2: Pergunta específica
    print("\n\n📋 Teste 2: Pergunta específica")
    print("-" * 50)

    resultado = consultar_faq_carro("gol-2020-001", "Aceita financiamento?")

    if resultado["sucesso"]:
        print(f"✅ Carro: {resultado['carro_id']}")
        print(f"\n❓ FAQ filtrado ({len(resultado['faq'])} chars):")
        print(resultado['faq'])
    else:
        print(f"❌ Erro: {resultado['erro']}")
