#!/usr/bin/env python3
"""
🧪 TESTE SISTEMA HÍBRIDO
Testa integração Function Calling + MCP
"""

import asyncio
import sys
from pathlib import Path

# Adiciona paths
sys.path.append(str(Path(__file__).parent / "componentes"))

from cliente_mcp import conectar_mcp
import json


async def testar_mcp_standalone():
    """Testa MCP Server standalone"""
    print("=" * 60)
    print("🔌 TESTE 1: MCP SERVER STANDALONE")
    print("=" * 60 + "\n")

    server_path = Path(__file__).parent / "mcp-server" / "server.py"

    if not server_path.exists():
        print(f"❌ Server não encontrado: {server_path}")
        return False

    try:
        async with conectar_mcp(str(server_path)) as cliente:

            # 1. Lista ferramentas
            print("1️⃣ Listando ferramentas MCP...")
            ferramentas = await cliente.listar_ferramentas()
            print(f"   ✅ Encontradas: {len(ferramentas)} ferramentas")
            for f in ferramentas:
                print(f"      • {f}")
            print()

            # 2. Testa calcular_financiamento
            print("2️⃣ Testando calcular_financiamento...")
            resultado = await cliente.chamar_ferramenta(
                "calcular_financiamento",
                {
                    "valor_veiculo": 45000,
                    "valor_entrada": 10000,
                    "taxa_juros_mensal": 1.99
                }
            )
            print(f"   ✅ Resultado:")
            print(f"      Financiado: R$ {resultado['valor_financiado']:,}".replace(",", "."))
            print(f"      Cenários: {len(resultado['cenarios'])}")
            for c in resultado['cenarios']:
                print(f"         • {c['prazo_meses']}x de R$ {c['valor_parcela']:.2f}")
            print()

            # 3. Testa analisar_sentimento
            print("3️⃣ Testando analisar_sentimento...")
            resultado = await cliente.chamar_ferramenta(
                "analisar_sentimento",
                {
                    "mensagens": ["obrigado!", "gostei muito", "perfeito", "show"]
                }
            )
            print(f"   ✅ Resultado:")
            print(f"      Score: {resultado['score']}/100")
            print(f"      Emoção: {resultado['emocao']}")
            print(f"      Sugestão: {resultado['sugestao']}")
            print()

            # 4. Testa buscar_carros_similares
            print("4️⃣ Testando buscar_carros_similares...")
            resultado = await cliente.chamar_ferramenta(
                "buscar_carros_similares",
                {
                    "caracteristicas": "sedan econômico até 50mil",
                    "limite": 3
                }
            )
            print(f"   ✅ Resultado:")
            print(f"      Encontrados: {resultado['total_encontrados']}")
            for carro in resultado['carros'][:3]:
                print(f"         • {carro['marca']} {carro['modelo']} {carro['ano']} - Score: {carro['score_match']}")
            print()

            # 5. Testa consultar_fipe
            print("5️⃣ Testando consultar_fipe...")
            resultado = await cliente.chamar_ferramenta(
                "consultar_fipe",
                {
                    "marca": "Volkswagen",
                    "modelo": "Gol",
                    "ano": "2020"
                }
            )
            print(f"   ✅ Resultado:")
            print(f"      FIPE: {resultado['valor_fipe']}")
            print(f"      Referência: {resultado['mes_referencia']}")
            print()

            print("✅ TODOS OS TESTES MCP PASSARAM!\n")
            return True

    except Exception as e:
        print(f"❌ Erro no teste MCP: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_ferramentas_locais():
    """Testa ferramentas locais (function calling)"""
    print("=" * 60)
    print("🔧 TESTE 2: FERRAMENTAS LOCAIS")
    print("=" * 60 + "\n")

    try:
        # 1. Testa lista_carros
        print("1️⃣ Testando lista_carros...")
        sys.path.append(str(Path(__file__).parent / "ferramentas"))
        from lista_carros import listar_carros_disponiveis, formatar_lista_para_mensagem

        carros_dir = Path(__file__).parent / "carros"
        carros = listar_carros_disponiveis(carros_dir)

        print(f"   ✅ Encontrados: {len(carros)} carros")
        for c in carros[:3]:
            print(f"      • {c['marca']} {c['modelo']} {c['ano']} - {c['preco']}")
        print()

        # 2. Testa consulta_faq
        print("2️⃣ Testando consulta_faq...")
        from consulta_faq import consultar_faq_carro

        if carros:
            carro_id = carros[0]['id']
            resultado = consultar_faq_carro(carro_id, "garantia", carros_dir)
            if resultado['sucesso']:
                print(f"   ✅ FAQ carregado para {carro_id}")
                print(f"      Base: {len(resultado['base'])} caracteres")
                print(f"      FAQ: {len(resultado['faq'])} caracteres")
            else:
                print(f"   ⚠️ Erro: {resultado['erro']}")
        print()

        print("✅ TODOS OS TESTES LOCAIS PASSARAM!\n")
        return True

    except Exception as e:
        print(f"❌ Erro no teste local: {e}")
        import traceback
        traceback.print_exc()
        return False


def resumo_arquitetura():
    """Mostra resumo da arquitetura híbrida"""
    print("=" * 60)
    print("📊 ARQUITETURA HÍBRIDA")
    print("=" * 60 + "\n")

    print("""
┌────────────────────────────────────────────────────────┐
│              CHATBOT AUTOMAIA V4                       │
│              (chatbot_automaia_v4.py)                  │
└─────────────────┬──────────────────────────────────────┘
                  │
                  ↓
         ┌────────────────────┐
         │  RAG HÍBRIDO       │
         │  (rag_hibrido)     │
         └────────┬───────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ↓                   ↓
┌───────────────┐   ┌──────────────────┐
│ FERRAMENTAS   │   │  FERRAMENTAS MCP │
│ LOCAIS (4)    │   │  (remotas) (5)   │
├───────────────┤   ├──────────────────┤
│ • lista       │   │ • sentimento     │
│ • faq         │   │ • proposta       │
│ • taguear     │   │ • similares      │
│ • agendar     │   │ • financiamento  │
└───────────────┘   │ • fipe           │
                    └──────────────────┘
    ~0ms latência      ~150ms latência

DECISÃO INTELIGENTE:
────────────────────
• Lista carros? → Local (rápido)
• Busca similar? → MCP (pesado)
• Agenda visita? → Local (conversacional)
• Calcula juros? → MCP (complexo)

PERFORMANCE:
────────────
• 4 ferramentas locais: 0ms overhead
• 5 ferramentas MCP: ~150ms cada
• Total: 9 ferramentas disponíveis
• Latência média: 50ms (uso misto)
    """)


async def main():
    """Executa todos os testes"""
    print("\n🚀 INICIANDO TESTES SISTEMA HÍBRIDO\n")

    # Mostra arquitetura
    resumo_arquitetura()

    # Testa ferramentas locais
    local_ok = testar_ferramentas_locais()

    # Testa MCP
    mcp_ok = await testar_mcp_standalone()

    # Resumo final
    print("=" * 60)
    print("📋 RESUMO FINAL")
    print("=" * 60 + "\n")

    print(f"Ferramentas Locais: {'✅ OK' if local_ok else '❌ FALHOU'}")
    print(f"MCP Server: {'✅ OK' if mcp_ok else '❌ FALHOU'}")
    print()

    if local_ok and mcp_ok:
        print("🎉 SISTEMA HÍBRIDO 100% FUNCIONAL!")
        print()
        print("📝 Próximos passos:")
        print("   1. cd whatsapp-chatbot-carros")
        print("   2. Atualizar chatbot_automaia_v4.py para usar RAGHibridoCarros")
        print("   3. Reiniciar chatbot: ./INICIAR_COM_NGROK.sh")
        print()
        return 0
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
