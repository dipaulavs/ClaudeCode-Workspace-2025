#!/usr/bin/env python3
"""
🔌 MCP SERVER - TEMPLATE CHATBOT
Ferramentas pesadas/reutilizáveis para chatbots

⚠️ CUSTOMIZAÇÃO OBRIGATÓRIA:
1. Renomeie Server("template-tools") para Server("seu-negocio-tools")
2. Ajuste ferramentas conforme seu negócio
3. Adicione/remova ferramentas conforme necessário

Ferramentas padrão incluídas:
1. analisar_sentimento - Análise de tom/emoção da conversa
2. gerar_proposta_comercial - Gera proposta estruturada
3. buscar_itens_similares - Busca semântica por características
4. calcular_financiamento - Simulação completa de financiamento
5. consultar_tabela_preco - Consulta tabela de preços externa
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# ==============================================================================
# SERVIDOR MCP
# ==============================================================================

# ⚠️ CUSTOMIZAR: Renomeie para seu negócio (ex: "imoveis-tools", "produtos-tools")
app = Server("template-tools")


# ==============================================================================
# FERRAMENTAS DISPONÍVEIS
# ==============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas as ferramentas disponíveis"""
    return [
        Tool(
            name="analisar_sentimento",
            description="Analisa o sentimento e tom emocional da conversa do cliente. Retorna score de satisfação (0-100), emoção predominante e sugestões de abordagem.",
            inputSchema={
                "type": "object",
                "properties": {
                    "mensagens": {
                        "type": "array",
                        "description": "Lista de mensagens do cliente (últimas 5-10)",
                        "items": {"type": "string"}
                    }
                },
                "required": ["mensagens"]
            }
        ),
        Tool(
            name="gerar_proposta_comercial",
            description="Gera proposta comercial estruturada com dados do item, preços e condições.",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "ID do item/produto/imóvel"
                    },
                    "cliente_nome": {
                        "type": "string",
                        "description": "Nome do cliente"
                    },
                    "desconto_percentual": {
                        "type": "number",
                        "description": "Desconto em % (opcional)",
                        "default": 0
                    }
                },
                "required": ["item_id", "cliente_nome"]
            }
        ),
        Tool(
            name="buscar_itens_similares",
            description="Busca itens similares baseado em características (busca semântica). Útil quando cliente não encontra exatamente o que quer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "caracteristicas": {
                        "type": "string",
                        "description": "Descrição das características desejadas"
                    },
                    "limite": {
                        "type": "number",
                        "description": "Número máximo de resultados",
                        "default": 3
                    }
                },
                "required": ["caracteristicas"]
            }
        ),
        Tool(
            name="calcular_financiamento",
            description="Calcula simulação completa de financiamento com diferentes cenários (24x, 36x, 48x, 60x). Retorna valor parcela, juros totais e CET.",
            inputSchema={
                "type": "object",
                "properties": {
                    "valor_total": {
                        "type": "number",
                        "description": "Valor total a financiar em reais"
                    },
                    "valor_entrada": {
                        "type": "number",
                        "description": "Valor de entrada em reais",
                        "default": 0
                    },
                    "taxa_juros_mensal": {
                        "type": "number",
                        "description": "Taxa de juros mensal em % (padrão: 1.99%)",
                        "default": 1.99
                    }
                },
                "required": ["valor_total"]
            }
        ),
        Tool(
            name="consultar_tabela_preco",
            description="Consulta tabela de preços externa para validar valor de mercado.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tipo": {
                        "type": "string",
                        "description": "Tipo do item (ex: marca, categoria)"
                    },
                    "modelo": {
                        "type": "string",
                        "description": "Modelo/nome do item"
                    },
                    "ano": {
                        "type": "string",
                        "description": "Ano (se aplicável)"
                    }
                },
                "required": ["tipo", "modelo"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Executa ferramenta solicitada"""

    if name == "analisar_sentimento":
        resultado = await analisar_sentimento(arguments["mensagens"])
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "gerar_proposta_comercial":
        resultado = await gerar_proposta_comercial(
            arguments["item_id"],
            arguments["cliente_nome"],
            arguments.get("desconto_percentual", 0)
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "buscar_itens_similares":
        resultado = await buscar_itens_similares(
            arguments["caracteristicas"],
            arguments.get("limite", 3)
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "calcular_financiamento":
        resultado = await calcular_financiamento(
            arguments["valor_total"],
            arguments.get("valor_entrada", 0),
            arguments.get("taxa_juros_mensal", 1.99)
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "consultar_tabela_preco":
        resultado = await consultar_tabela_preco(
            arguments["tipo"],
            arguments["modelo"],
            arguments.get("ano", "")
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    else:
        raise ValueError(f"Ferramenta desconhecida: {name}")


# ==============================================================================
# IMPLEMENTAÇÃO DAS FERRAMENTAS
# ==============================================================================

async def analisar_sentimento(mensagens: List[str]) -> Dict:
    """
    Analisa sentimento usando modelo de IA

    ⚠️ CUSTOMIZAR: Em produção, integrar API de NLP real
    Esta é versão simplificada baseada em keywords
    """

    # Concatena mensagens
    texto_completo = " ".join(mensagens).lower()

    # Análise por keywords (CUSTOMIZAR para seu negócio)
    palavras_positivas = ["obrigado", "ótimo", "perfeito", "legal", "gostei", "maravilha", "show"]
    palavras_negativas = ["ruim", "péssimo", "horrível", "não gostei", "problema", "erro"]
    palavras_urgencia = ["hoje", "agora", "urgente", "rápido", "preciso"]
    palavras_duvida = ["não sei", "talvez", "dúvida", "será", "pode ser"]

    # Contagens
    count_positivo = sum(1 for p in palavras_positivas if p in texto_completo)
    count_negativo = sum(1 for p in palavras_negativas if p in texto_completo)
    count_urgencia = sum(1 for p in palavras_urgencia if p in texto_completo)
    count_duvida = sum(1 for p in palavras_duvida if p in texto_completo)

    # Score (0-100)
    score = 50  # neutro
    score += count_positivo * 10
    score -= count_negativo * 15
    score += count_urgencia * 5
    score -= count_duvida * 5
    score = max(0, min(100, score))

    # Emoção predominante
    if count_negativo > count_positivo:
        emocao = "frustrado"
    elif count_positivo > count_negativo:
        emocao = "satisfeito"
    elif count_urgencia > 2:
        emocao = "ansioso"
    elif count_duvida > 2:
        emocao = "indeciso"
    else:
        emocao = "neutro"

    # Sugestões de abordagem
    if emocao == "frustrado":
        sugestao = "Demonstre empatia, ofereça ajuda imediata e considere escalonamento."
    elif emocao == "satisfeito":
        sugestao = "Mantenha tom positivo e avance para próximos passos (agendamento/proposta)."
    elif emocao == "ansioso":
        sugestao = "Responda rapidamente, seja direto e ofereça soluções imediatas."
    elif emocao == "indeciso":
        sugestao = "Faça perguntas específicas, ofereça comparações e ajude na decisão."
    else:
        sugestao = "Continue conversação natural, busque entender necessidades."

    return {
        "score": score,
        "emocao": emocao,
        "sugestao": sugestao,
        "analise": {
            "palavras_positivas": count_positivo,
            "palavras_negativas": count_negativo,
            "sinais_urgencia": count_urgencia,
            "sinais_duvida": count_duvida
        }
    }


async def gerar_proposta_comercial(item_id: str, cliente_nome: str, desconto: float) -> Dict:
    """
    Gera proposta comercial

    ⚠️ CUSTOMIZAR: Ajuste para seu negócio e integre geração de PDF real
    """

    # ⚠️ CUSTOMIZAR: Buscar dados do item do seu banco/diretório
    # Exemplo: carros/, imoveis/, produtos/
    itens_dir = Path(__file__).parent.parent / "itens"  # ALTERAR nome da pasta
    item_dir = itens_dir / item_id

    if not item_dir.exists():
        return {"erro": f"Item {item_id} não encontrado"}

    # Lê base.txt (⚠️ CUSTOMIZAR estrutura conforme seu banco)
    base_file = item_dir / "base.txt"
    if not base_file.exists():
        return {"erro": f"Arquivo base.txt não encontrado para {item_id}"}

    with open(base_file, 'r', encoding='utf-8') as f:
        base_txt = f.read()

    # Extrai preço (⚠️ CUSTOMIZAR regex conforme seu formato)
    import re
    preco_match = re.search(r'[Pp]reço|[Vv]alor:\s*R\$\s*([\d.,]+)', base_txt)
    if preco_match:
        preco_str = preco_match.group(1).replace(".", "").replace(",", "")
        preco = int(preco_str)
    else:
        preco = 0

    # Calcula desconto
    valor_desconto = int(preco * (desconto / 100))
    preco_final = preco - valor_desconto

    # Monta proposta
    from datetime import datetime, timedelta
    data_validade = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")

    proposta = {
        "numero_proposta": f"PROP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "data_emissao": datetime.now().strftime("%d/%m/%Y"),
        "validade": data_validade,
        "cliente": cliente_nome,
        "item": {
            "id": item_id,
            "descricao": base_txt[:200]  # Primeiras linhas
        },
        "valores": {
            "preco_tabela": f"R$ {preco:,}".replace(",", "."),
            "desconto_percentual": f"{desconto}%",
            "valor_desconto": f"R$ {valor_desconto:,}".replace(",", "."),
            "preco_final": f"R$ {preco_final:,}".replace(",", ".")
        },
        "condicoes": {
            "entrada_minima": f"R$ {int(preco_final * 0.2):,}".replace(",", "."),
            "parcelamento": "Até 60x com taxa de 1,99% a.m.",
            "garantia": "Conforme contrato",  # ⚠️ CUSTOMIZAR
            "observacoes": "Proposta sujeita a aprovação."  # ⚠️ CUSTOMIZAR
        },
        "pdf_gerado": False,  # ⚠️ Em produção: True após gerar PDF
        "pdf_url": None  # ⚠️ Em produção: URL do PDF gerado
    }

    return proposta


async def buscar_itens_similares(caracteristicas: str, limite: int) -> Dict:
    """
    Busca itens similares por características

    ⚠️ CUSTOMIZAR: Em produção, usar embeddings + busca vetorial
    Esta versão usa busca por keywords simples
    """

    # ⚠️ CUSTOMIZAR: Alterar nome da pasta conforme seu negócio
    itens_dir = Path(__file__).parent.parent / "itens"  # carros/, imoveis/, produtos/

    if not itens_dir.exists():
        return {"erro": "Diretório de itens não encontrado"}

    caracteristicas_lower = caracteristicas.lower()
    matches = []

    for pasta in itens_dir.iterdir():
        if not pasta.is_dir() or pasta.name.startswith('.'):
            continue

        base_file = pasta / "base.txt"
        if not base_file.exists():
            continue

        # Lê arquivo
        with open(base_file, 'r', encoding='utf-8') as f:
            conteudo = f.read().lower()

        # Calcula score de match
        score = 0
        palavras_busca = caracteristicas_lower.split()

        for palavra in palavras_busca:
            if len(palavra) < 3:
                continue
            if palavra in conteudo:
                score += 1

        if score > 0:
            matches.append({
                "item_id": pasta.name,
                "score_match": score,
                "preview": conteudo[:150]  # Primeiras linhas
            })

    # Ordena por score e limita
    matches.sort(key=lambda x: x["score_match"], reverse=True)
    matches = matches[:limite]

    return {
        "total_encontrados": len(matches),
        "itens": matches,
        "busca": caracteristicas
    }


async def calcular_financiamento(valor_total: float, entrada: float, taxa_mensal: float) -> Dict:
    """
    Calcula financiamento em múltiplos cenários

    Usa tabela Price (parcela fixa)
    """

    valor_financiado = valor_total - entrada

    if valor_financiado <= 0:
        return {"erro": "Valor de entrada maior ou igual ao valor total"}

    taxa = taxa_mensal / 100
    cenarios = []

    # ⚠️ CUSTOMIZAR: Ajuste prazos conforme seu negócio
    for meses in [24, 36, 48, 60]:
        # Fórmula Price
        fator = (1 + taxa) ** meses
        parcela = (valor_financiado * taxa * fator) / (fator - 1)

        total_pago = parcela * meses
        juros_total = total_pago - valor_financiado
        cet_anual = ((total_pago / valor_financiado) ** (12 / meses) - 1) * 100

        cenarios.append({
            "prazo_meses": meses,
            "valor_parcela": round(parcela, 2),
            "total_pago": round(total_pago, 2),
            "juros_total": round(juros_total, 2),
            "cet_anual": round(cet_anual, 2)
        })

    return {
        "valor_total": valor_total,
        "valor_entrada": entrada,
        "valor_financiado": valor_financiado,
        "taxa_juros_mensal": taxa_mensal,
        "cenarios": cenarios
    }


async def consultar_tabela_preco(tipo: str, modelo: str, ano: str) -> Dict:
    """
    Consulta tabela de preços externa

    ⚠️ CUSTOMIZAR: Integrar API real do seu segmento
    Exemplos: FIPE (carros), Zap/Viva Real (imóveis), B2W (produtos)
    """

    # MOCK: em produção, fazer request real
    import random

    # Simula resposta
    try:
        ano_int = int(ano) if ano else 2020
        valor_base = (ano_int - 2000) * 2000
        variacao = random.randint(-5000, 5000)
        valor_tabela = max(20000, valor_base + variacao)
    except:
        valor_tabela = 45000

    return {
        "tipo": tipo,
        "modelo": modelo,
        "ano": ano,
        "valor_tabela": f"R$ {valor_tabela:,}".replace(",", "."),
        "mes_referencia": "novembro/2025",
        "fonte": "Tabela de Referência",  # ⚠️ CUSTOMIZAR
        "observacao": "⚠️ VALOR MOCK - Em produção, integrar API real"
    }


# ==============================================================================
# MAIN
# ==============================================================================

async def main():
    """Inicia servidor MCP"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
