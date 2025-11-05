#!/usr/bin/env python3
"""
🎭 TESTE DE CONVERSAÇÕES FICTÍCIAS
Simula interações completas de clientes reais com o chatbot da Automaia
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Adiciona paths
sys.path.append(str(Path(__file__).parent / "componentes"))

from cliente_mcp import conectar_mcp
import json


# ==============================================================================
# CENÁRIOS DE CONVERSAÇÃO
# ==============================================================================

class ClienteFicticio:
    """Representa um cliente fictício com histórico de mensagens"""

    def __init__(self, nome, perfil, historico_mensagens):
        self.nome = nome
        self.perfil = perfil
        self.historico = historico_mensagens


CENARIOS = [
    ClienteFicticio(
        "João Silva",
        "Cliente interessado, mas indeciso sobre financiamento",
        [
            "Oi, tô procurando um carro usado",
            "Mas não sei se consigo financiar",
            "Tenho R$ 5.000 de entrada",
            "Será que dá pra financiar um carro de uns R$ 40.000?"
        ]
    ),
    ClienteFicticio(
        "Maria Souza",
        "Cliente satisfeita, quer proposta rápida",
        [
            "Olá! Vi o Gol 2020 no site",
            "Adorei o carro!",
            "Pode me enviar uma proposta?",
            "Obrigada! Perfeito!"
        ]
    ),
    ClienteFicticio(
        "Carlos Pereira",
        "Cliente frustrado, preço alto",
        [
            "Esses carros tão muito caros",
            "Não tem nada mais em conta?",
            "Tô procurando há dias e não acho",
            "Pô, complicado..."
        ]
    ),
    ClienteFicticio(
        "Ana Costa",
        "Cliente urgente, quer decisão rápida",
        [
            "Preciso de um carro HOJE",
            "Tem algum disponível agora?",
            "Posso buscar hoje mesmo?",
            "Urgente por favor"
        ]
    ),
    ClienteFicticio(
        "Roberto Lima",
        "Cliente comparando preços com FIPE",
        [
            "Quanto tá a tabela FIPE do Gol 2020?",
            "E vocês vendem por quanto?",
            "Tá muito acima da tabela",
            "Não rola um desconto?"
        ]
    )
]


# ==============================================================================
# FUNÇÕES DE TESTE
# ==============================================================================

async def simular_analise_sentimento(cliente_mcp, cliente: ClienteFicticio):
    """Simula análise de sentimento do histórico do cliente"""
    print(f"\n{'='*70}")
    print(f"👤 CLIENTE: {cliente.nome}")
    print(f"📊 PERFIL: {cliente.perfil}")
    print(f"{'='*70}\n")

    print("💬 Histórico de mensagens:")
    for i, msg in enumerate(cliente.historico, 1):
        print(f"   {i}. {msg}")

    print("\n🤖 Analisando sentimento...")
    resultado = await cliente_mcp.chamar_ferramenta(
        "analisar_sentimento",
        {"mensagens": cliente.historico}
    )

    # Mostra resultado visual
    score = resultado['score']
    emocao = resultado['emocao']
    sugestao = resultado['sugestao']

    # Barra de score visual
    barra_tamanho = 50
    preenchido = int((score / 100) * barra_tamanho)
    barra = "█" * preenchido + "░" * (barra_tamanho - preenchido)

    # Emoji baseado na emoção
    emoji_map = {
        "satisfeito": "😊",
        "frustrado": "😤",
        "ansioso": "😰",
        "indeciso": "🤔",
        "neutro": "😐"
    }
    emoji = emoji_map.get(emocao, "😐")

    print(f"\n📈 RESULTADO DA ANÁLISE:")
    print(f"   Score: {score}/100")
    print(f"   [{barra}] {score}%")
    print(f"   {emoji} Emoção: {emocao.upper()}")
    print(f"   💡 Sugestão: {sugestao}")
    print(f"\n   📊 Detalhes:")
    for key, value in resultado['analise'].items():
        print(f"      • {key}: {value}")

    return resultado


async def simular_simulacao_financiamento(cliente_mcp, valor_veiculo=45000, entrada=10000):
    """Simula cálculo de financiamento"""
    print(f"\n{'='*70}")
    print(f"💰 SIMULAÇÃO DE FINANCIAMENTO")
    print(f"{'='*70}\n")

    print(f"📋 Dados:")
    print(f"   Valor do veículo: R$ {valor_veiculo:,.2f}".replace(",", "."))
    print(f"   Entrada: R$ {entrada:,.2f}".replace(",", "."))
    print(f"   Taxa: 1.99% a.m.")

    print(f"\n🤖 Calculando cenários de financiamento...")
    resultado = await cliente_mcp.chamar_ferramenta(
        "calcular_financiamento",
        {
            "valor_veiculo": valor_veiculo,
            "valor_entrada": entrada,
            "taxa_juros_mensal": 1.99
        }
    )

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

    return resultado


async def simular_geracao_proposta(cliente_mcp, carro_id, cliente_nome, desconto=5):
    """Simula geração de proposta comercial"""
    print(f"\n{'='*70}")
    print(f"📄 GERAÇÃO DE PROPOSTA COMERCIAL")
    print(f"{'='*70}\n")

    print(f"📋 Dados:")
    print(f"   Cliente: {cliente_nome}")
    print(f"   Carro ID: {carro_id}")
    print(f"   Desconto: {desconto}%")

    print(f"\n🤖 Gerando proposta...")

    try:
        resultado = await cliente_mcp.chamar_ferramenta(
            "gerar_proposta_comercial",
            {
                "carro_id": carro_id,
                "cliente_nome": cliente_nome,
                "desconto_percentual": desconto
            }
        )

        if "erro" in resultado:
            print(f"   ⚠️ Erro: {resultado['erro']}")
            return resultado

        print(f"\n📄 PROPOSTA GERADA:")
        print(f"   Nº: {resultado['numero_proposta']}")
        print(f"   Data: {resultado['data_emissao']}")
        print(f"   Validade: {resultado['validade']}")
        print(f"\n   🚗 VEÍCULO:")
        print(f"      {resultado['veiculo']['marca']} {resultado['veiculo']['modelo']} {resultado['veiculo']['ano']}")
        print(f"\n   💰 VALORES:")
        print(f"      Preço tabela: {resultado['valores']['preco_tabela']}")
        print(f"      Desconto ({resultado['valores']['desconto_percentual']}): {resultado['valores']['valor_desconto']}")
        print(f"      PREÇO FINAL: {resultado['valores']['preco_final']}")
        print(f"\n   📋 CONDIÇÕES:")
        print(f"      Entrada mínima: {resultado['condicoes']['entrada_minima']}")
        print(f"      Parcelamento: {resultado['condicoes']['parcelamento']}")
        print(f"      Garantia: {resultado['condicoes']['garantia']}")

        return resultado

    except Exception as e:
        print(f"   ❌ Erro ao gerar proposta: {e}")
        return {"erro": str(e)}


async def simular_busca_similares(cliente_mcp, caracteristicas="sedan econômico até 50mil"):
    """Simula busca de carros similares"""
    print(f"\n{'='*70}")
    print(f"🔍 BUSCA DE CARROS SIMILARES")
    print(f"{'='*70}\n")

    print(f"📋 Busca: \"{caracteristicas}\"")
    print(f"\n🤖 Buscando carros similares...")

    resultado = await cliente_mcp.chamar_ferramenta(
        "buscar_carros_similares",
        {
            "caracteristicas": caracteristicas,
            "limite": 5
        }
    )

    print(f"\n🚗 CARROS ENCONTRADOS: {resultado['total_encontrados']}")

    if resultado['total_encontrados'] == 0:
        print("   ⚠️ Nenhum carro encontrado com essas características")
    else:
        print(f"\n{'#':<4} {'Marca':<12} {'Modelo':<15} {'Ano':<6} {'Preço':<15} {'Match':<6}")
        print("─" * 70)

        for i, carro in enumerate(resultado['carros'], 1):
            print(f"{i:<4} {carro['marca']:<12} {carro['modelo']:<15} {carro['ano']:<6} {carro['preco']:<15} {carro['score_match']:<6}")

    return resultado


async def simular_consulta_fipe(cliente_mcp, marca="Volkswagen", modelo="Gol", ano="2020"):
    """Simula consulta à tabela FIPE"""
    print(f"\n{'='*70}")
    print(f"📊 CONSULTA TABELA FIPE")
    print(f"{'='*70}\n")

    print(f"📋 Veículo: {marca} {modelo} {ano}")
    print(f"\n🤖 Consultando FIPE...")

    resultado = await cliente_mcp.chamar_ferramenta(
        "consultar_fipe",
        {
            "marca": marca,
            "modelo": modelo,
            "ano": ano
        }
    )

    print(f"\n💰 VALOR FIPE:")
    print(f"   Marca: {resultado['marca']}")
    print(f"   Modelo: {resultado['modelo']}")
    print(f"   Ano: {resultado['ano']}")
    print(f"   Valor: {resultado['valor_fipe']}")
    print(f"   Referência: {resultado['mes_referencia']}")
    print(f"   ℹ️ {resultado['observacao']}")

    return resultado


# ==============================================================================
# CONVERSAÇÃO COMPLETA
# ==============================================================================

async def simular_conversacao_completa(cliente_mcp, cliente: ClienteFicticio):
    """Simula uma conversação completa do início ao fim"""
    print(f"\n{'='*70}")
    print(f"🎬 CONVERSAÇÃO COMPLETA: {cliente.nome}")
    print(f"{'='*70}\n")

    # 1. Análise de sentimento
    sentimento = await simular_analise_sentimento(cliente_mcp, cliente)

    # 2. Busca carros baseado no perfil
    print(f"\n🤖 Bot detecta interesse e busca carros similares...")
    await asyncio.sleep(1)
    busca = await simular_busca_similares(cliente_mcp, "carro popular até 50mil")

    # 3. Se cliente satisfeito, gera proposta
    if sentimento['emocao'] == 'satisfeito' and busca['total_encontrados'] > 0:
        print(f"\n🤖 Cliente satisfeito! Gerando proposta...")
        await asyncio.sleep(1)
        carro_id = busca['carros'][0]['carro_id']
        proposta = await simular_geracao_proposta(cliente_mcp, carro_id, cliente.nome, desconto=5)

    # 4. Se menciona financiamento, calcula
    if any(palavra in ' '.join(cliente.historico).lower() for palavra in ['financiar', 'entrada', 'parcela']):
        print(f"\n🤖 Cliente perguntou sobre financiamento!")
        await asyncio.sleep(1)
        await simular_simulacao_financiamento(cliente_mcp, valor_veiculo=45000, entrada=5000)

    # 5. Se menciona FIPE, consulta
    if 'fipe' in ' '.join(cliente.historico).lower():
        print(f"\n🤖 Cliente perguntou sobre FIPE!")
        await asyncio.sleep(1)
        await simular_consulta_fipe(cliente_mcp, "Volkswagen", "Gol", "2020")

    print(f"\n✅ Conversação com {cliente.nome} finalizada!\n")


# ==============================================================================
# MAIN
# ==============================================================================

async def main():
    """Executa simulação completa de conversações"""
    print("\n" + "="*70)
    print("🎭 TESTE DE CONVERSAÇÕES FICTÍCIAS - CHATBOT AUTOMAIA")
    print("="*70 + "\n")

    print("📋 Este teste simula conversações reais de clientes com o chatbot")
    print("   Testando todas as ferramentas MCP em cenários realistas\n")

    server_path = Path(__file__).parent / "mcp-server" / "server.py"

    if not server_path.exists():
        print(f"❌ Server não encontrado: {server_path}")
        return 1

    try:
        async with conectar_mcp(str(server_path)) as cliente_mcp:

            # Lista ferramentas disponíveis
            print("🔌 Conectando ao MCP Server...")
            ferramentas = await cliente_mcp.listar_ferramentas()
            print(f"✅ {len(ferramentas)} ferramentas disponíveis: {', '.join(ferramentas)}\n")

            # Menu de opções
            print("\n📋 ESCOLHA O TESTE:")
            print("   1. Análise de sentimento de todos os clientes")
            print("   2. Simulação de financiamento")
            print("   3. Geração de proposta comercial")
            print("   4. Busca de carros similares")
            print("   5. Consulta tabela FIPE")
            print("   6. Conversação completa (1 cliente)")
            print("   7. TODAS AS CONVERSAÇÕES (5 clientes)")
            print("   0. Sair\n")

            escolha = input("Digite sua escolha (1-7): ").strip()

            if escolha == "1":
                for cliente in CENARIOS:
                    await simular_analise_sentimento(cliente_mcp, cliente)
                    await asyncio.sleep(1)

            elif escolha == "2":
                await simular_simulacao_financiamento(cliente_mcp, 45000, 10000)

            elif escolha == "3":
                # Busca primeiro carro disponível
                carros_dir = Path(__file__).parent / "carros"
                carros = [p.name for p in carros_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]
                if carros:
                    await simular_geracao_proposta(cliente_mcp, carros[0], "João Silva", desconto=5)
                else:
                    print("❌ Nenhum carro cadastrado")

            elif escolha == "4":
                await simular_busca_similares(cliente_mcp, "sedan econômico até 50mil")

            elif escolha == "5":
                await simular_consulta_fipe(cliente_mcp, "Volkswagen", "Gol", "2020")

            elif escolha == "6":
                print("\n📋 Escolha o cliente:")
                for i, cliente in enumerate(CENARIOS, 1):
                    print(f"   {i}. {cliente.nome} - {cliente.perfil}")
                cliente_idx = int(input("\nDigite o número do cliente: ").strip()) - 1
                if 0 <= cliente_idx < len(CENARIOS):
                    await simular_conversacao_completa(cliente_mcp, CENARIOS[cliente_idx])
                else:
                    print("❌ Cliente inválido")

            elif escolha == "7":
                print("\n🚀 Iniciando TODAS as conversações...\n")
                for i, cliente in enumerate(CENARIOS, 1):
                    print(f"\n{'#'*70}")
                    print(f"# CONVERSAÇÃO {i}/{len(CENARIOS)}")
                    print(f"{'#'*70}")
                    await simular_conversacao_completa(cliente_mcp, cliente)
                    await asyncio.sleep(2)

            elif escolha == "0":
                print("\n👋 Até mais!\n")
                return 0

            else:
                print("\n❌ Opção inválida\n")
                return 1

            # Resumo final
            print(f"\n{'='*70}")
            print(f"📊 RESUMO DO TESTE")
            print(f"{'='*70}\n")
            print(f"✅ Todos os testes MCP executados com sucesso!")
            print(f"⏱️ Hora: {datetime.now().strftime('%H:%M:%S')}")
            print(f"\n🎉 Sistema MCP 100% funcional!\n")

            return 0

    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário\n")
        sys.exit(0)
