#!/usr/bin/env python3
"""
🔧 FERRAMENTA: Enviar Localização do Imóvel

Extrai URL do Google Maps do imóvel e formata uma mensagem amigável
com informações de localização e distâncias para WhatsApp.

Funcionalidades:
- Lê links.json do imóvel
- Extrai URL do Google Maps
- Formata mensagem com distâncias aproximadas
"""

import json
from pathlib import Path
from typing import Dict, Optional


def enviar_localizacao_imovel(
    imovel_id: str,
    imoveis_dir: Path = None
) -> Dict[str, str]:
    """
    Extrai e formata localização do imóvel

    Args:
        imovel_id: ID do imóvel (ex: 'chacara-itatiaiucu-001')
        imoveis_dir: Diretório dos imóveis (padrão: ../imoveis)

    Returns:
        Dict com:
        - 'sucesso': True/False
        - 'mensagem': Mensagem formatada para WhatsApp
        - 'url_maps': URL do Google Maps (se encontrada)
    """
    if imoveis_dir is None:
        imoveis_dir = Path(__file__).parent.parent / "imoveis"

    imovel_path = imoveis_dir / imovel_id
    links_file = imovel_path / "links.json"

    # Valida se diretório existe
    if not imovel_path.exists():
        return {
            "sucesso": False,
            "mensagem": f"❌ Imóvel '{imovel_id}' não encontrado.",
            "url_maps": None
        }

    # Valida se links.json existe
    if not links_file.exists():
        return {
            "sucesso": False,
            "mensagem": f"❌ Arquivo de links não encontrado para '{imovel_id}'.",
            "url_maps": None
        }

    # Lê links.json
    try:
        with open(links_file, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    except json.JSONDecodeError as e:
        return {
            "sucesso": False,
            "mensagem": f"❌ Erro ao ler arquivo de links: {e}",
            "url_maps": None
        }
    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"❌ Erro inesperado: {e}",
            "url_maps": None
        }

    # Extrai URL do Google Maps
    url_maps = links_data.get("localizacao")

    if not url_maps:
        return {
            "sucesso": False,
            "mensagem": f"❌ Localização não configurada para este imóvel.",
            "url_maps": None
        }

    # Extrai nome do imóvel da pasta (transforma ID em nome legível)
    nome_imovel = _formatar_nome_imovel(imovel_id)

    # Obtém distâncias baseado no imóvel
    distancias = _obter_distancias(imovel_id)

    # Formata mensagem
    mensagem = _formatar_mensagem_localizacao(
        nome_imovel,
        url_maps,
        distancias
    )

    return {
        "sucesso": True,
        "mensagem": mensagem,
        "url_maps": url_maps
    }


def _formatar_nome_imovel(imovel_id: str) -> str:
    """
    Transforma ID do imóvel em nome legível

    Ex: 'chacara-itatiaiucu-001' → 'Chácara Itatiaiuçu'
    """
    # Remove número sequencial
    nome = imovel_id.rsplit('-', 1)[0]

    # Substitui hífens por espaços
    nome = nome.replace('-', ' ')

    # Capitaliza primeira letra de cada palavra
    nome = nome.title()

    # Corrige palavras acentuadas
    correcoes = {
        'Itatiaiucu': 'Itatiaiuçu',
        'Chacara': 'Chácara'
    }

    for incorreto, correto in correcoes.items():
        nome = nome.replace(incorreto, correto)

    return nome


def _obter_distancias(imovel_id: str) -> Dict[str, str]:
    """
    Retorna distâncias aproximadas baseado no tipo de imóvel

    Dados de exemplo para a região de Itatiaiuçu
    """
    distancias_por_imovel = {
        "chacara-itatiaiucu-001": {
            "centro": "Centro Itatiaiuçu: 10 min",
            "cidade1": "Betim: 43 min",
            "cidade2": "Belo Horizonte: 60 min",
            "apoio": "Próximo a supermercado e farmácia"
        }
    }

    # Se o imóvel tem distâncias específicas, usa
    if imovel_id in distancias_por_imovel:
        return distancias_por_imovel[imovel_id]

    # Caso contrário, retorna padrão
    return {
        "centro": "Centro: 15 min",
        "cidade1": "Cidade próxima: 30 min",
        "cidade2": "Belo Horizonte: 60 min",
        "apoio": "Boa infraestrutura na região"
    }


def _formatar_mensagem_localizacao(
    nome_imovel: str,
    url_maps: str,
    distancias: Dict[str, str]
) -> str:
    """
    Formata mensagem final para WhatsApp

    Args:
        nome_imovel: Nome do imóvel formatado
        url_maps: URL do Google Maps
        distancias: Dict com informações de distâncias

    Returns:
        Mensagem formatada
    """
    msg = f"📍 LOCALIZAÇÃO DA {nome_imovel.upper()}:\n\n"

    msg += f"🗺️ Ver no mapa:\n{url_maps}\n\n"

    msg += "📏 Distâncias:\n"
    for chave in ["centro", "cidade1", "cidade2", "apoio"]:
        if chave in distancias:
            msg += f"• {distancias[chave]}\n"

    msg += "\n💡 Clique no link acima para visualizar a localização exata no Google Maps."

    return msg.strip()


def formatar_resposta_para_whatsapp(resultado: Dict) -> str:
    """
    Prepara resposta para envio via WhatsApp

    Args:
        resultado: Dict retornado por enviar_localizacao_imovel()

    Returns:
        String pronta para enviar no WhatsApp
    """
    if resultado.get("sucesso"):
        return resultado.get("mensagem", "")
    else:
        return resultado.get("mensagem", "❌ Erro ao obter localização.")


# ============================================================================
# TESTE STANDALONE
# ============================================================================

if __name__ == "__main__":
    print("🧪 Testando enviar_localizacao.py...\n")

    # Teste 1: Imóvel existente
    print("=" * 60)
    print("📝 TESTE 1: Imóvel existente")
    print("=" * 60)

    resultado = enviar_localizacao_imovel("chacara-itatiaiucu-001")

    if resultado["sucesso"]:
        print(f"✅ Sucesso!\n")
        print("📱 Mensagem para WhatsApp:\n")
        print(resultado["mensagem"])
        print(f"\n🔗 URL Maps: {resultado['url_maps']}")
    else:
        print(f"❌ Erro: {resultado['mensagem']}")

    # Teste 2: Imóvel não existente
    print("\n" + "=" * 60)
    print("📝 TESTE 2: Imóvel não existente")
    print("=" * 60)

    resultado = enviar_localizacao_imovel("imovel-fantasma-999")
    print(f"Resultado: {resultado['mensagem']}")

    # Teste 3: Nome formatado
    print("\n" + "=" * 60)
    print("📝 TESTE 3: Formatação de nomes")
    print("=" * 60)

    nomes_teste = [
        "chacara-itatiaiucu-001",
        "casa-centro-002",
        "terreno-betim-001"
    ]

    for nome_id in nomes_teste:
        nome_formatado = _formatar_nome_imovel(nome_id)
        print(f"  {nome_id} → {nome_formatado}")

    print("\n✅ Testes concluídos!")
