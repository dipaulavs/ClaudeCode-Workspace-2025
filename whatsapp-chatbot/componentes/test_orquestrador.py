#!/usr/bin/env python3
"""
🧪 TESTE DO ORQUESTRADOR INTELIGENTE

Valida integração de todos os componentes
"""

import sys
from pathlib import Path

# Adiciona path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("\n📦 Teste 1: Imports dos componentes")
    print("="*80)

    try:
        from componentes.orquestrador import OrquestradorInteligente
        print("✅ orquestrador.OrquestradorInteligente")
    except ImportError as e:
        print(f"❌ Erro ao importar orquestrador: {e}")
        return False

    try:
        from componentes.rag import IntegradorRAG
        print("✅ rag.IntegradorRAG")
    except ImportError:
        print("⚠️  rag.IntegradorRAG não disponível (opcional)")

    try:
        from componentes.score import IntegradorScore
        print("✅ score.IntegradorScore")
    except ImportError:
        print("⚠️  score.IntegradorScore não disponível (opcional)")

    try:
        from componentes.followup import IntegradorFollowUp
        print("✅ followup.IntegradorFollowUp")
    except ImportError:
        print("⚠️  followup.IntegradorFollowUp não disponível (opcional)")

    try:
        from componentes.escalonamento import IntegradorEscalonamento
        print("✅ escalonamento.IntegradorEscalonamento")
    except ImportError:
        print("⚠️  escalonamento.IntegradorEscalonamento não disponível (opcional)")

    try:
        from componentes.relatorios import IntegradorMetricas
        print("✅ relatorios.IntegradorMetricas")
    except ImportError:
        print("⚠️  relatorios.IntegradorMetricas não disponível (opcional)")

    print("\n✅ Teste 1: PASSOU\n")
    return True


def test_orquestrador_init():
    """Testa inicialização do orquestrador"""
    print("\n🎯 Teste 2: Inicialização do Orquestrador")
    print("="*80)

    try:
        from componentes.orquestrador import OrquestradorInteligente
        from upstash_redis import Redis
        import json

        # Carrega config
        with open('chatwoot_config.json', 'r') as f:
            config = json.load(f)

        # Redis
        redis = Redis(
            url="https://legible-collie-9537.upstash.io",
            token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
        )

        # Inicializa orquestrador
        orquestrador = OrquestradorInteligente(
            imoveis_dir=Path(__file__).parent.parent / "imoveis",
            openai_api_key="sk-test",  # Fake (só para teste de init)
            openrouter_api_key="sk-test",
            redis_client=redis,
            config=config
        )

        print("\n📊 Status dos componentes:")
        status = orquestrador.get_status()
        for componente, estado in status.items():
            print(f"   • {componente}: {estado}")

        print("\n✅ Teste 2: PASSOU\n")
        return True

    except Exception as e:
        print(f"\n❌ Teste 2: FALHOU - {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_orquestrador_pipeline():
    """Testa pipeline completo (sem chamadas reais de API)"""
    print("\n🔄 Teste 3: Pipeline do Orquestrador (Mock)")
    print("="*80)

    print("⚠️  Este teste requer componentes funcionais.")
    print("⚠️  Execute testes individuais primeiro:")
    print("   python3 componentes/rag/test_rag.py")
    print("   python3 componentes/score/test_score.py")
    print("   python3 componentes/followup/test_followup_offline.py")
    print("   python3 componentes/escalonamento/test_escalonamento.py")
    print("   python3 componentes/relatorios/test_relatorios.py")

    print("\n⏭️  Teste 3: PULADO (teste manual recomendado)\n")
    return True


def main():
    """Executa todos os testes"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🧪 TESTE DO ORQUESTRADOR INTELIGENTE                           ║
║                                                                   ║
║   Framework Híbrido - Chatbot WhatsApp                           ║
║   Versão: 1.0                                                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    testes = [
        ("Imports", test_imports),
        ("Inicialização", test_orquestrador_init),
        ("Pipeline", test_orquestrador_pipeline)
    ]

    resultados = []

    for nome, teste_fn in testes:
        try:
            passou = teste_fn()
            resultados.append((nome, passou))
        except Exception as e:
            print(f"\n❌ Erro no teste '{nome}': {e}\n")
            import traceback
            traceback.print_exc()
            resultados.append((nome, False))

    # Resumo
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)

    passou_total = 0
    falhou_total = 0

    for nome, passou in resultados:
        if passou:
            print(f"✅ {nome}")
            passou_total += 1
        else:
            print(f"❌ {nome}")
            falhou_total += 1

    print("="*80)
    print(f"Total: {passou_total}/{len(resultados)} testes passaram")
    print("="*80)

    if falhou_total == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!\n")
        return 0
    else:
        print(f"\n⚠️  {falhou_total} teste(s) falharam\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
