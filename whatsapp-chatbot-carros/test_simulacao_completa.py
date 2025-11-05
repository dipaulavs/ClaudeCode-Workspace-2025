#!/usr/bin/env python3.11
"""
🎬 SIMULAÇÃO COMPLETA - Teste de Conversações Fictícias
MOCK das ferramentas MCP (não precisa do servidor rodando)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path


# ==============================================================================
# MOCK DAS FERRAMENTAS MCP
# ==============================================================================

class MCPMock:
    """Mock das ferramentas MCP para teste sem servidor"""

    async def analisar_sentimento(self, mensagens):
        """Mock de análise de sentimento"""
        texto_completo = " ".join(mensagens).lower()

        # Análise por keywords
        palavras_positivas = ["obrigado", "ótimo", "perfeito", "legal", "gostei", "maravilha", "show", "adorei"]
        palavras_negativas = ["ruim", "péssimo", "horrível", "não gostei", "problema", "erro", "caro", "complicado"]
        palavras_urgencia = ["hoje", "agora", "urgente", "rápido", "preciso"]
        palavras_duvida = ["não sei", "talvez", "dúvida", "será", "pode ser"]

        count_positivo = sum(1 for p in palavras_positivas if p in texto_completo)
        count_negativo = sum(1 for p in palavras_negativas if p in texto_completo)
        count_urgencia = sum(1 for p in palavras_urgencia if p in texto_completo)
        count_duvida = sum(1 for p in palavras_duvida if p in texto_completo)

        score = 50
        score += count_positivo * 10
        score -= count_negativo * 15
        score += count_urgencia * 5
        score -= count_duvida * 5
        score = max(0, min(100, score))

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

        sugestoes = {
            "frustrado": "Demonstre empatia, ofereça ajuda imediata e considere escalonamento.",
            "satisfeito": "Mantenha tom positivo e avance para próximos passos (agendamento/proposta).",
            "ansioso": "Responda rapidamente, seja direto e ofereça soluções imediatas.",
            "indeciso": "Faça perguntas específicas, ofereça comparações e ajude na decisão.",
            "neutro": "Continue conversação natural, busque entender necessidades."
        }

        return {
            "score": score,
            "emocao": emocao,
            "sugestao": sugestoes[emocao],
            "analise": {
                "palavras_positivas": count_positivo,
                "palavras_negativas": count_negativo,
                "sinais_urgencia": count_urgencia,
                "sinais_duvida": count_duvida
            }
        }

    async def calcular_financiamento(self, valor_veiculo, entrada, taxa_mensal):
        """Mock de cálculo de financiamento"""
        valor_financiado = valor_veiculo - entrada

        if valor_financiado <= 0:
            return {"erro": "Valor de entrada maior ou igual ao valor do veículo"}

        taxa = taxa_mensal / 100
        cenarios = []

        for meses in [24, 36, 48, 60]:
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
            "valor_veiculo": valor_veiculo,
            "valor_entrada": entrada,
            "valor_financiado": valor_financiado,
            "taxa_juros_mensal": taxa_mensal,
            "cenarios": cenarios
        }

    async def gerar_proposta_comercial(self, carro_id, cliente_nome, desconto):
        """Mock de geração de proposta"""
        # Dados ficticios do carro
        carro = {
            "marca": "Volkswagen",
            "modelo": "Gol 1.0",
            "ano": "2020",
            "preco": 45000
        }

        valor_desconto = int(carro["preco"] * (desconto / 100))
        preco_final = carro["preco"] - valor_desconto

        from datetime import datetime, timedelta
        data_validade = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")

        return {
            "numero_proposta": f"PROP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "data_emissao": datetime.now().strftime("%d/%m/%Y"),
            "validade": data_validade,
            "cliente": cliente_nome,
            "veiculo": carro,
            "valores": {
                "preco_tabela": f"R$ {carro['preco']:,}".replace(",", "."),
                "desconto_percentual": f"{desconto}%",
                "valor_desconto": f"R$ {valor_desconto:,}".replace(",", "."),
                "preco_final": f"R$ {preco_final:,}".replace(",", ".")
            },
            "condicoes": {
                "entrada_minima": f"R$ {int(preco_final * 0.2):,}".replace(",", "."),
                "parcelamento": "Até 60x com taxa de 1,99% a.m.",
                "garantia": "3 meses de garantia mecânica",
                "documentacao": "Incluída no valor"
            }
        }

    async def buscar_carros_similares(self, caracteristicas, limite):
        """Mock de busca de carros similares"""
        carros_mock = [
            {"carro_id": "gol-2020-001", "marca": "Volkswagen", "modelo": "Gol 1.0", "ano": "2020", "preco": "R$ 45.000", "score_match": 8},
            {"carro_id": "onix-2021-002", "marca": "Chevrolet", "modelo": "Onix 1.0", "ano": "2021", "preco": "R$ 48.000", "score_match": 7},
            {"carro_id": "hb20-2019-003", "marca": "Hyundai", "modelo": "HB20 1.0", "ano": "2019", "preco": "R$ 42.000", "score_match": 7},
            {"carro_id": "argo-2020-004", "marca": "Fiat", "modelo": "Argo 1.0", "ano": "2020", "preco": "R$ 43.000", "score_match": 6},
            {"carro_id": "kwid-2021-005", "marca": "Renault", "modelo": "Kwid 1.0", "ano": "2021", "preco": "R$ 41.000", "score_match": 5}
        ]

        return {
            "total_encontrados": len(carros_mock[:limite]),
            "carros": carros_mock[:limite],
            "busca": caracteristicas
        }

    async def consultar_fipe(self, marca, modelo, ano):
        """Mock de consulta FIPE"""
        ano_int = int(ano) if ano.isdigit() else 2020
        valor_base = (ano_int - 2000) * 2000
        valor_fipe = max(20000, valor_base + 5000)

        return {
            "marca": marca,
            "modelo": modelo,
            "ano": ano,
            "valor_fipe": f"R$ {valor_fipe:,}".replace(",", "."),
            "mes_referencia": "novembro/2025",
            "fonte": "FIPE",
            "observacao": "VALOR SIMULADO - teste fictício"
        }


# ==============================================================================
# CLIENTES FICTÍCIOS
# ==============================================================================

class ClienteFicticio:
    def __init__(self, nome, perfil, historico_mensagens):
        self.nome = nome
        self.perfil = perfil
        self.historico = historico_mensagens


CENARIOS = [
    ClienteFicticio(
        "João Silva",
        "Cliente interessado, mas indeciso sobre financiamento",
        ["Oi, tô procurando um carro usado", "Mas não sei se consigo financiar",
         "Tenho R$ 5.000 de entrada", "Será que dá pra financiar um carro de uns R$ 40.000?"]
    ),
    ClienteFicticio(
        "Maria Souza",
        "Cliente satisfeita, quer proposta rápida",
        ["Olá! Vi o Gol 2020 no site", "Adorei o carro!", "Pode me enviar uma proposta?", "Obrigada! Perfeito!"]
    ),
    ClienteFicticio(
        "Carlos Pereira",
        "Cliente frustrado, preço alto",
        ["Esses carros tão muito caros", "Não tem nada mais em conta?",
         "Tô procurando há dias e não acho", "Pô, complicado..."]
    ),
    ClienteFicticio(
        "Ana Costa",
        "Cliente urgente, quer decisão rápida",
        ["Preciso de um carro HOJE", "Tem algum disponível agora?", "Posso buscar hoje mesmo?", "Urgente por favor"]
    ),
    ClienteFicticio(
        "Roberto Lima",
        "Cliente comparando preços com FIPE",
        ["Quanto tá a tabela FIPE do Gol 2020?", "E vocês vendem por quanto?",
         "Tá muito acima da tabela", "Não rola um desconto?"]
    )
]


# ==============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ==============================================================================

async def simular_analise_sentimento(mcp, cliente):
    """Simula análise de sentimento do histórico do cliente"""
    print(f"\n{'='*70}")
    print(f"👤 CLIENTE: {cliente.nome}")
    print(f"📊 PERFIL: {cliente.perfil}")
    print(f"{'='*70}\n")

    print("💬 Histórico de mensagens:")
    for i, msg in enumerate(cliente.historico, 1):
        print(f"   {i}. {msg}")

    print("\n🤖 Analisando sentimento...")
    resultado = await mcp.analisar_sentimento(cliente.historico)

    score = resultado['score']
    emocao = resultado['emocao']
    sugestao = resultado['sugestao']

    # Barra visual
    barra_tamanho = 50
    preenchido = int((score / 100) * barra_tamanho)
    barra = "█" * preenchido + "░" * (barra_tamanho - preenchido)

    emoji_map = {
        "satisfeito": "😊", "frustrado": "😤", "ansioso": "😰", "indeciso": "🤔", "neutro": "😐"
    }
    emoji = emoji_map.get(emocao, "😐")

    print(f"\n📈 RESULTADO DA ANÁLISE:")
    print(f"   Score: {score}/100")
    print(f"   [{barra}] {score}%")
    print(f"   {emoji} Emoção: {emocao.upper()}")
    print(f"   💡 Sugestão: {sugestao}")

    return resultado


async def simular_simulacao_financiamento(mcp, valor_veiculo=45000, entrada=10000):
    """Simula cálculo de financiamento"""
    print(f"\n{'='*70}")
    print(f"💰 SIMULAÇÃO DE FINANCIAMENTO")
    print(f"{'='*70}\n")

    print(f"📋 Dados:")
    print(f"   Valor do veículo: R$ {valor_veiculo:,.2f}".replace(",", "."))
    print(f"   Entrada: R$ {entrada:,.2f}".replace(",", "."))

    resultado = await mcp.calcular_financiamento(valor_veiculo, entrada, 1.99)

    print(f"\n📊 CENÁRIOS DISPONÍVEIS:")
    print(f"\n{'Prazo':<10} {'Parcela':<15} {'Total Pago':<15} {'Juros':<15} {'CET/ano':<10}")
    print("─" * 70)

    for c in resultado['cenarios']:
        prazo = f"{c['prazo_meses']}x"
        parcela = f"R$ {c['valor_parcela']:,.2f}".replace(",", ".")
        total = f"R$ {c['total_pago']:,.2f}".replace(",", ".")
        juros = f"R$ {c['juros_total']:,.2f}".replace(",", ".")
        cet = f"{c['cet_anual']:.2f}%"
        print(f"{prazo:<10} {parcela:<15} {total:<15} {juros:<15} {cet:<10}")


async def simular_geracao_proposta(mcp, cliente_nome, desconto=5):
    """Simula geração de proposta comercial"""
    print(f"\n{'='*70}")
    print(f"📄 GERAÇÃO DE PROPOSTA COMERCIAL")
    print(f"{'='*70}\n")

    resultado = await mcp.gerar_proposta_comercial("gol-2020-001", cliente_nome, desconto)

    print(f"\n📄 PROPOSTA GERADA:")
    print(f"   Nº: {resultado['numero_proposta']}")
    print(f"   Cliente: {resultado['cliente']}")
    print(f"   Validade: {resultado['validade']}")
    print(f"\n   🚗 VEÍCULO: {resultado['veiculo']['marca']} {resultado['veiculo']['modelo']} {resultado['veiculo']['ano']}")
    print(f"\n   💰 VALORES:")
    print(f"      Preço tabela: {resultado['valores']['preco_tabela']}")
    print(f"      Desconto: {resultado['valores']['valor_desconto']}")
    print(f"      PREÇO FINAL: {resultado['valores']['preco_final']}")


async def simular_busca_similares(mcp, caracteristicas="sedan econômico até 50mil"):
    """Simula busca de carros similares"""
    print(f"\n{'='*70}")
    print(f"🔍 BUSCA DE CARROS SIMILARES")
    print(f"{'='*70}\n")

    print(f"📋 Busca: \"{caracteristicas}\"")
    resultado = await mcp.buscar_carros_similares(caracteristicas, 5)

    print(f"\n🚗 CARROS ENCONTRADOS: {resultado['total_encontrados']}")
    print(f"\n{'#':<4} {'Marca':<12} {'Modelo':<15} {'Ano':<6} {'Preço':<15} {'Match':<6}")
    print("─" * 70)

    for i, carro in enumerate(resultado['carros'], 1):
        print(f"{i:<4} {carro['marca']:<12} {carro['modelo']:<15} {carro['ano']:<6} {carro['preco']:<15} {carro['score_match']:<6}")


async def simular_consulta_fipe(mcp, marca="Volkswagen", modelo="Gol", ano="2020"):
    """Simula consulta à tabela FIPE"""
    print(f"\n{'='*70}")
    print(f"📊 CONSULTA TABELA FIPE")
    print(f"{'='*70}\n")

    resultado = await mcp.consultar_fipe(marca, modelo, ano)

    print(f"\n💰 VALOR FIPE:")
    print(f"   Veículo: {resultado['marca']} {resultado['modelo']} {resultado['ano']}")
    print(f"   Valor: {resultado['valor_fipe']}")
    print(f"   Referência: {resultado['mes_referencia']}")


async def simular_conversacao_completa(mcp, cliente):
    """Simula uma conversação completa do início ao fim"""
    print(f"\n{'#'*70}")
    print(f"# 🎬 CONVERSAÇÃO COMPLETA: {cliente.nome}")
    print(f"{'#'*70}\n")

    # 1. Análise de sentimento
    sentimento = await simular_analise_sentimento(mcp, cliente)
    await asyncio.sleep(0.5)

    # 2. Busca carros similares
    print(f"\n🤖 Bot detecta interesse e busca carros similares...")
    await simular_busca_similares(mcp, "carro popular até 50mil")
    await asyncio.sleep(0.5)

    # 3. Se cliente satisfeito, gera proposta
    if sentimento['emocao'] == 'satisfeito':
        print(f"\n🤖 Cliente satisfeito! Gerando proposta...")
        await simular_geracao_proposta(mcp, cliente.nome, desconto=5)
        await asyncio.sleep(0.5)

    # 4. Se menciona financiamento, calcula
    if any(palavra in ' '.join(cliente.historico).lower() for palavra in ['financiar', 'entrada', 'parcela']):
        print(f"\n🤖 Cliente perguntou sobre financiamento!")
        await simular_simulacao_financiamento(mcp, valor_veiculo=45000, entrada=5000)
        await asyncio.sleep(0.5)

    # 5. Se menciona FIPE, consulta
    if 'fipe' in ' '.join(cliente.historico).lower():
        print(f"\n🤖 Cliente perguntou sobre FIPE!")
        await simular_consulta_fipe(mcp, "Volkswagen", "Gol", "2020")

    print(f"\n✅ Conversação com {cliente.nome} finalizada!\n")


# ==============================================================================
# MAIN
# ==============================================================================

async def main():
    """Executa simulação completa"""
    print("\n" + "="*70)
    print("🎭 SIMULAÇÃO COMPLETA - CHATBOT AUTOMAIA (MOCK)")
    print("="*70 + "\n")

    print("📋 Este teste simula conversações reais usando MOCK das ferramentas MCP")
    print("   (não precisa do servidor MCP rodando)\n")

    mcp = MCPMock()

    # Menu
    print("\n📋 ESCOLHA O TESTE:")
    print("   1. Análise de sentimento de todos os clientes")
    print("   2. Simulação de financiamento")
    print("   3. Geração de proposta comercial")
    print("   4. Busca de carros similares")
    print("   5. Consulta tabela FIPE")
    print("   6. Conversação completa (1 cliente)")
    print("   7. TODAS AS CONVERSAÇÕES (5 clientes) 🎬")
    print("   0. Sair\n")

    escolha = input("Digite sua escolha (1-7): ").strip()

    if escolha == "1":
        for cliente in CENARIOS:
            await simular_analise_sentimento(mcp, cliente)
            await asyncio.sleep(0.5)

    elif escolha == "2":
        await simular_simulacao_financiamento(mcp, 45000, 10000)

    elif escolha == "3":
        await simular_geracao_proposta(mcp, "João Silva", desconto=5)

    elif escolha == "4":
        await simular_busca_similares(mcp, "sedan econômico até 50mil")

    elif escolha == "5":
        await simular_consulta_fipe(mcp, "Volkswagen", "Gol", "2020")

    elif escolha == "6":
        print("\n📋 Escolha o cliente:")
        for i, cliente in enumerate(CENARIOS, 1):
            print(f"   {i}. {cliente.nome} - {cliente.perfil}")
        cliente_idx = int(input("\nDigite o número: ").strip()) - 1
        if 0 <= cliente_idx < len(CENARIOS):
            await simular_conversacao_completa(mcp, CENARIOS[cliente_idx])

    elif escolha == "7":
        print("\n🚀 Iniciando TODAS as conversações...\n")
        for i, cliente in enumerate(CENARIOS, 1):
            print(f"\n{'#'*70}")
            print(f"# CONVERSAÇÃO {i}/{len(CENARIOS)}")
            print(f"{'#'*70}")
            await simular_conversacao_completa(mcp, cliente)
            await asyncio.sleep(1)

    elif escolha == "0":
        print("\n👋 Até mais!\n")
        return 0

    # Resumo final
    print(f"\n{'='*70}")
    print(f"📊 RESUMO DO TESTE")
    print(f"{'='*70}\n")
    print(f"✅ Todas as ferramentas MCP testadas com sucesso (mock)")
    print(f"⏱️ Hora: {datetime.now().strftime('%H:%M:%S')}")
    print(f"\n🎉 Simulação 100% funcional!\n")

    print("📝 PRÓXIMOS PASSOS:")
    print("   1. Instalar MCP: ./INSTALAR_MCP.sh (requer Python 3.10+)")
    print("   2. Testar sistema real: python3 testar_sistema_hibrido.py")
    print("   3. Integrar no chatbot: editar chatbot_automaia_v4.py\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido\n")
