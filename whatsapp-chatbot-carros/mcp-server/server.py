#!/usr/bin/env python3
"""
🔌 MCP SERVER - AUTOMAIA CHATBOT
Ferramentas pesadas/reutilizáveis para múltiplos chatbots

Ferramentas disponíveis:
1. analisar_sentimento - Análise de tom/emoção da conversa
2. gerar_proposta_comercial - Gera PDF de proposta
3. buscar_carros_similares - Busca semântica por características
4. calcular_financiamento - Simulação completa de financiamento
5. consultar_fipe - Busca preço FIPE do veículo
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

app = Server("automaia-tools")


# ==============================================================================
# FERRAMENTA 1: ANALISAR SENTIMENTO
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
            description="Gera proposta comercial em PDF com dados do veículo, preços, condições de pagamento e informações da loja.",
            inputSchema={
                "type": "object",
                "properties": {
                    "carro_id": {
                        "type": "string",
                        "description": "ID do carro (ex: gol-2020-001)"
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
                "required": ["carro_id", "cliente_nome"]
            }
        ),
        Tool(
            name="buscar_carros_similares",
            description="Busca carros similares baseado em características (busca semântica). Útil quando cliente não encontra exatamente o que quer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "caracteristicas": {
                        "type": "string",
                        "description": "Descrição das características desejadas (ex: 'sedan econômico 2020-2023 até 60mil')"
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
                    "valor_veiculo": {
                        "type": "number",
                        "description": "Valor do veículo em reais"
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
                "required": ["valor_veiculo"]
            }
        ),
        Tool(
            name="consultar_fipe",
            description="Consulta tabela FIPE para verificar preço médio de mercado do veículo. Útil para validar preço de venda.",
            inputSchema={
                "type": "object",
                "properties": {
                    "marca": {
                        "type": "string",
                        "description": "Marca do veículo (ex: Volkswagen)"
                    },
                    "modelo": {
                        "type": "string",
                        "description": "Modelo do veículo (ex: Gol)"
                    },
                    "ano": {
                        "type": "string",
                        "description": "Ano do veículo (ex: 2020)"
                    }
                },
                "required": ["marca", "modelo", "ano"]
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
            arguments["carro_id"],
            arguments["cliente_nome"],
            arguments.get("desconto_percentual", 0)
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "buscar_carros_similares":
        resultado = await buscar_carros_similares(
            arguments["caracteristicas"],
            arguments.get("limite", 3)
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "calcular_financiamento":
        resultado = await calcular_financiamento(
            arguments["valor_veiculo"],
            arguments.get("valor_entrada", 0),
            arguments.get("taxa_juros_mensal", 1.99)
        )
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

    elif name == "consultar_fipe":
        resultado = await consultar_fipe(
            arguments["marca"],
            arguments["modelo"],
            arguments["ano"]
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

    Em produção, usar API de NLP (OpenAI, Anthropic, etc)
    Esta é versão simplificada baseada em keywords
    """

    # Concatena mensagens
    texto_completo = " ".join(mensagens).lower()

    # Análise por keywords
    palavras_positivas = ["obrigado", "ótimo", "perfeito", "legal", "gostei", "maravilha", "show"]
    palavras_negativas = ["ruim", "péssimo", "horrível", "não gostei", "problema", "erro"]
    palavras_neutras = ["ok", "certo", "entendi", "sim", "não"]
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
    score = max(0, min(100, score))  # limita 0-100

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


async def gerar_proposta_comercial(carro_id: str, cliente_nome: str, desconto: float) -> Dict:
    """
    Gera proposta comercial

    Em produção: gerar PDF real com reportlab/weasyprint
    Esta versão retorna estrutura JSON
    """

    # Busca dados do carro
    carros_dir = Path(__file__).parent.parent / "carros"
    carro_dir = carros_dir / carro_id

    if not carro_dir.exists():
        return {"erro": f"Carro {carro_id} não encontrado"}

    # Lê base.txt
    base_file = carro_dir / "base.txt"
    with open(base_file, 'r', encoding='utf-8') as f:
        base_txt = f.read()

    # Extrai informações
    import re
    marca = re.search(r'Marca:\s*(.+)', base_txt).group(1) if re.search(r'Marca:\s*(.+)', base_txt) else ""
    modelo = re.search(r'Modelo:\s*(.+)', base_txt).group(1) if re.search(r'Modelo:\s*(.+)', base_txt) else ""
    ano = re.search(r'Ano:\s*(.+)', base_txt).group(1) if re.search(r'Ano:\s*(.+)', base_txt) else ""
    preco_match = re.search(r'À vista:\s*R\$\s*([\d.,]+)', base_txt)
    preco_str = preco_match.group(1).replace(".", "").replace(",", "") if preco_match else "0"
    preco = int(preco_str)

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
        "veiculo": {
            "marca": marca,
            "modelo": modelo,
            "ano": ano,
            "id": carro_id
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
            "garantia": "3 meses de garantia mecânica",
            "documentacao": "Incluída no valor"
        },
        "observacoes": "Proposta sujeita a análise de crédito. Veículo sujeito a venda prévia.",
        "pdf_gerado": False,  # Em produção: True após gerar PDF
        "pdf_url": None  # Em produção: URL do PDF gerado
    }

    return proposta


async def buscar_carros_similares(caracteristicas: str, limite: int) -> Dict:
    """
    Busca carros similares por características

    Em produção: usar embeddings + busca vetorial (Pinecone, Weaviate, etc)
    Esta versão usa busca por keywords simples
    """

    carros_dir = Path(__file__).parent.parent / "carros"

    if not carros_dir.exists():
        return {"erro": "Diretório de carros não encontrado"}

    # Extrai keywords
    caracteristicas_lower = caracteristicas.lower()

    # Score de match para cada carro
    matches = []

    for pasta in carros_dir.iterdir():
        if not pasta.is_dir() or pasta.name.startswith('.'):
            continue

        base_file = pasta / "base.txt"
        detalhes_file = pasta / "detalhes.txt"

        if not base_file.exists():
            continue

        # Lê arquivos
        with open(base_file, 'r', encoding='utf-8') as f:
            base_txt = f.read().lower()

        detalhes_txt = ""
        if detalhes_file.exists():
            with open(detalhes_file, 'r', encoding='utf-8') as f:
                detalhes_txt = f.read().lower()

        conteudo_completo = base_txt + " " + detalhes_txt

        # Calcula score de match
        score = 0
        palavras_busca = caracteristicas_lower.split()

        for palavra in palavras_busca:
            if len(palavra) < 3:  # ignora palavras muito curtas
                continue
            if palavra in conteudo_completo:
                score += 1

        if score > 0:
            # Extrai info básica
            import re
            marca = re.search(r'marca:\s*(.+)', base_txt)
            modelo = re.search(r'modelo:\s*(.+)', base_txt)
            ano = re.search(r'ano:\s*(.+)', base_txt)
            preco = re.search(r'à vista:\s*r\$\s*([\d.,]+)', base_txt)

            matches.append({
                "carro_id": pasta.name,
                "marca": marca.group(1).strip() if marca else "",
                "modelo": modelo.group(1).strip() if modelo else "",
                "ano": ano.group(1).strip() if ano else "",
                "preco": preco.group(1).strip() if preco else "",
                "score_match": score
            })

    # Ordena por score e limita
    matches.sort(key=lambda x: x["score_match"], reverse=True)
    matches = matches[:limite]

    return {
        "total_encontrados": len(matches),
        "carros": matches,
        "busca": caracteristicas
    }


async def calcular_financiamento(valor_veiculo: float, entrada: float, taxa_mensal: float) -> Dict:
    """
    Calcula financiamento em múltiplos cenários

    Usa tabela Price (parcela fixa)
    """

    # Valor financiado
    valor_financiado = valor_veiculo - entrada

    if valor_financiado <= 0:
        return {"erro": "Valor de entrada maior ou igual ao valor do veículo"}

    # Taxa mensal em decimal
    taxa = taxa_mensal / 100

    # Calcula para diferentes prazos
    cenarios = []

    for meses in [24, 36, 48, 60]:
        # Fórmula Price: P = [V * i * (1+i)^n] / [(1+i)^n - 1]
        fator = (1 + taxa) ** meses
        parcela = (valor_financiado * taxa * fator) / (fator - 1)

        total_pago = parcela * meses
        juros_total = total_pago - valor_financiado

        # CET simplificado (aproximação)
        cet_anual = ((total_pago / valor_financiado) ** (12 / meses) - 1) * 100

        cenarios.append({
            "prazo_meses": meses,
            "valor_parcela": round(parcela, 2),
            "total_pago": round(total_pago, 2),
            "juros_total": round(juros_total, 2),
            "cet_anual": round(cet_anual, 2)
        })

    return {
        "valor_veiculo": valor_veiculo,
        "valor_entrada": entrada,
        "valor_financiado": valor_financiado,
        "taxa_juros_mensal": taxa_mensal,
        "cenarios": cenarios
    }


async def consultar_fipe(marca: str, modelo: str, ano: str) -> Dict:
    """
    Consulta tabela FIPE

    Em produção: usar API FIPE real (https://deividfortuna.github.io/fipe/)
    Esta versão retorna MOCK
    """

    # MOCK: em produção, fazer request real
    # import requests
    # url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas"

    # Simula resposta
    import random

    # Gera valor aleatório baseado em ano (carros mais novos = mais caros)
    try:
        ano_int = int(ano)
        valor_base = (ano_int - 2000) * 2000
        variacao = random.randint(-5000, 5000)
        valor_fipe = max(20000, valor_base + variacao)
    except:
        valor_fipe = 45000

    return {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "valor_fipe": f"R$ {valor_fipe:,}".replace(",", "."),
        "mes_referencia": "novembro/2025",
        "fonte": "FIPE",
        "observacao": "VALOR MOCK - Em produção, usar API FIPE real"
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
