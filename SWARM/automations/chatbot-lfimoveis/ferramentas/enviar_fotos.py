#!/usr/bin/env python3
"""
🔧 FERRAMENTA: Enviar Fotos do Imóvel

Busca todas as fotos, vídeo tour e localização de um imóvel.
Formata URLs em mensagem bonita para WhatsApp.
"""

import json
from pathlib import Path
from typing import Dict, Optional


def enviar_fotos_imovel(imovel_id: str, imoveis_dir: Path = None) -> Dict:
    """
    Busca fotos do imóvel e retorna URLs formatadas

    Args:
        imovel_id: ID do imóvel (ex: 'chacara-itatiaiucu-001')
        imoveis_dir: Diretório dos imóveis (padrão: ../imoveis)

    Returns:
        Dict com:
        - sucesso: bool
        - mensagem: str (pronta para WhatsApp)
        - fotos: list de URLs
        - video_tour: str (URL) ou None
        - localizacao: str (URL) ou None
        - documentos: list de URLs
    """
    if imoveis_dir is None:
        imoveis_dir = Path(__file__).parent.parent / "imoveis"

    imovel_path = imoveis_dir / imovel_id
    links_file = imovel_path / "links.json"

    # Validar se imóvel existe
    if not imovel_path.exists():
        return {
            "sucesso": False,
            "mensagem": f"❌ Imóvel '{imovel_id}' não encontrado.",
            "fotos": [],
            "video_tour": None,
            "localizacao": None,
            "documentos": []
        }

    # Validar se links.json existe
    if not links_file.exists():
        return {
            "sucesso": False,
            "mensagem": f"⚠️ Nenhuma foto disponível para '{imovel_id}' ainda.",
            "fotos": [],
            "video_tour": None,
            "localizacao": None,
            "documentos": []
        }

    try:
        with open(links_file, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    except json.JSONDecodeError:
        return {
            "sucesso": False,
            "mensagem": f"❌ Erro ao ler fotos do imóvel '{imovel_id}'.",
            "fotos": [],
            "video_tour": None,
            "localizacao": None,
            "documentos": []
        }

    # Extrair dados
    fotos = links_data.get("fotos", [])
    video_tour = links_data.get("video_tour", None)
    localizacao = links_data.get("localizacao", None)
    documentos = links_data.get("documentos", [])

    # Formatar mensagem
    mensagem = _formatar_mensagem_fotos(
        imovel_id=imovel_id,
        fotos=fotos,
        video_tour=video_tour,
        localizacao=localizacao,
        documentos=documentos
    )

    return {
        "sucesso": True,
        "mensagem": mensagem,
        "fotos": fotos,
        "video_tour": video_tour,
        "localizacao": localizacao,
        "documentos": documentos
    }


def _formatar_mensagem_fotos(
    imovel_id: str,
    fotos: list,
    video_tour: Optional[str],
    localizacao: Optional[str],
    documentos: list
) -> str:
    """
    Formata mensagem bonita com as fotos e URLs

    Args:
        imovel_id: ID do imóvel (usado no título)
        fotos: Lista de URLs das fotos
        video_tour: URL do vídeo tour ou None
        localizacao: URL do Google Maps ou None
        documentos: Lista de URLs dos documentos

    Returns:
        String formatada para WhatsApp
    """
    # Título com emoji apropriado
    titulo = _extrair_titulo_imovel(imovel_id)
    msg = f"📸 FOTOS - {titulo}\n\n"

    # Fotos
    if fotos:
        for i, foto_url in enumerate(fotos, 1):
            descricao = _descrever_foto(i, len(fotos))
            msg += f"{i}️⃣ {descricao}\n{foto_url}\n\n"
    else:
        msg += "Nenhuma foto disponível.\n\n"

    # Vídeo tour
    if video_tour:
        msg += f"🎥 Vídeo tour\n{video_tour}\n\n"

    # Localização
    if localizacao:
        msg += f"📍 Localização no mapa\n{localizacao}\n\n"

    # Documentos
    if documentos:
        msg += "📄 Documentos:\n"
        for i, doc_url in enumerate(documentos, 1):
            msg += f"  • Documento {i}: {doc_url}\n"
        msg += "\n"

    # Rodapé
    msg += "Clique nos links acima para ver fotos em alta resolução!"

    return msg.strip()


def _extrair_titulo_imovel(imovel_id: str) -> str:
    """
    Converte ID do imóvel em título legível

    Exemplos:
    - chacara-itatiaiucu-001 → Chácara Itatiaiucu
    - casa-moderna-bh-001 → Casa Moderna BH
    """
    # Remove número do final (ex: -001)
    partes = imovel_id.rsplit("-", 1)[0].split("-")

    # Capitaliza cada parte
    titulo = " ".join(p.capitalize() for p in partes)

    # Correções específicas para acentos/abreviações
    titulo = titulo.replace("itatiaiucu", "Itatiaiucu")
    titulo = titulo.replace("bh", "BH")
    titulo = titulo.replace("sp", "SP")
    titulo = titulo.replace("mg", "MG")

    return titulo


def _descrever_foto(numero: int, total: int) -> str:
    """
    Gera descrição genérica para foto baseada em posição

    Args:
        numero: Posição da foto (1-indexed)
        total: Total de fotos

    Returns:
        String descritiva (ex: "Fachada", "Interior", "Piscina")
    """
    descricoes = {
        1: "Fachada/Vista frontal",
        2: "Terreno/Área externa",
        3: "Vista panorâmica",
        4: "Interior",
        5: "Cômodo principal",
        6: "Detalhes da propriedade"
    }

    if numero <= total:
        return descricoes.get(numero, f"Foto {numero}")

    return f"Foto {numero}"


def formatar_resposta_fotos_para_whatsapp(resultado: Dict) -> str:
    """
    Wrapper para retornar apenas a mensagem formatada

    Args:
        resultado: Dict retornado por enviar_fotos_imovel()

    Returns:
        String pronta para enviar no WhatsApp
    """
    if not resultado["sucesso"]:
        return resultado["mensagem"]

    return resultado["mensagem"]


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando enviar_fotos.py...\n")

    # Teste 1: Imóvel existente
    print("=" * 60)
    print("TESTE 1: Imóvel com fotos (chacara-itatiaiucu-001)")
    print("=" * 60)
    resultado = enviar_fotos_imovel("chacara-itatiaiucu-001")

    if resultado["sucesso"]:
        print("✅ Sucesso!\n")
        print(resultado["mensagem"])
        print("\n")
        print(f"📊 Dados estruturados:")
        print(f"  • Fotos: {len(resultado['fotos'])}")
        print(f"  • Vídeo tour: {'✅ Sim' if resultado['video_tour'] else '❌ Não'}")
        print(f"  • Localização: {'✅ Sim' if resultado['localizacao'] else '❌ Não'}")
        print(f"  • Documentos: {len(resultado['documentos'])}")
    else:
        print(f"❌ Erro: {resultado['mensagem']}")

    # Teste 2: Imóvel inexistente
    print("\n" + "=" * 60)
    print("TESTE 2: Imóvel inexistente (casa-fake-001)")
    print("=" * 60)
    resultado = enviar_fotos_imovel("casa-fake-001")

    if resultado["sucesso"]:
        print(resultado["mensagem"])
    else:
        print(f"✅ Erro esperado: {resultado['mensagem']}")

    # Teste 3: Verificar se consegue listar outros imóveis
    print("\n" + "=" * 60)
    print("TESTE 3: Listando imóveis disponíveis")
    print("=" * 60)

    imoveis_dir = Path(__file__).parent.parent / "imoveis"
    if imoveis_dir.exists():
        imoveis = [p.name for p in imoveis_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]
        print(f"✅ Imóveis encontrados: {len(imoveis)}")
        for imovel_id in imoveis[:5]:  # Mostra primeiros 5
            print(f"  • {imovel_id}")
            # Tenta enviar fotos de cada um
            resultado = enviar_fotos_imovel(imovel_id)
            status = "✅ Com fotos" if resultado["sucesso"] else "⚠️ Sem fotos"
            print(f"    {status}")
    else:
        print("❌ Diretório de imóveis não encontrado")
