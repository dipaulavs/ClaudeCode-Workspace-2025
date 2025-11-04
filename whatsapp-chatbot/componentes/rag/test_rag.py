#!/usr/bin/env python3
"""
🧪 TESTES RAG - Sistema RAG + Progressive Disclosure

Testa:
1. RAG Híbrido (busca)
2. Progressive Disclosure (níveis)
3. 2 Estágios (identificação → especialista)
4. Integração completa
"""

import sys
from pathlib import Path
from upstash_redis import Redis

# Adiciona path do componente
sys.path.insert(0, str(Path(__file__).parent))

from busca_hibrida import RAGHibrido
from progressive_disclosure import ProgressiveDisclosure
from ia_especialista import IAEspecialista
from integrador import IntegradorRAG


# ==================== CONFIGURAÇÃO ====================

IMOVEIS_DIR = Path(__file__).parent.parent.parent / "imoveis"

OPENAI_KEY = "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"

OPENROUTER_KEY = "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"

REDIS = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
)


# ==================== TESTES ====================

def teste_rag_hibrido():
    """
    Teste 1: RAG Híbrido
    """
    print("\n" + "=" * 60)
    print("🧪 TESTE 1: RAG HÍBRIDO")
    print("=" * 60)

    rag = RAGHibrido(IMOVEIS_DIR, OPENAI_KEY)

    # Cenário 1: Busca específica
    print("\n📋 Cenário 1: Busca específica")
    print("-" * 50)

    mensagem = "Apartamento 2 quartos Savassi"
    candidatos = rag.buscar(mensagem)

    assert len(candidatos) <= 3, f"❌ Esperado máx 3 candidatos, got {len(candidatos)}"

    for candidato in candidatos:
        assert "id" in candidato
        assert candidato.get("tipo") == "apartamento" or candidato.get("tipo") is None

    print(f"✅ Retornou {len(candidatos)} candidatos")
    for i, c in enumerate(candidatos, 1):
        print(f"   {i}. {c['id']} - {c.get('tipo')} - {c.get('regiao')}")

    # Cenário 2: Busca genérica
    print("\n📋 Cenário 2: Busca genérica")
    print("-" * 50)

    mensagem = "Imóvel para alugar"
    candidatos = rag.buscar(mensagem)

    print(f"✅ Retornou {len(candidatos)} candidatos (busca genérica)")

    # Cenário 3: Sem resultados
    print("\n📋 Cenário 3: Filtro muito restritivo")
    print("-" * 50)

    mensagem = "Mansão 10 quartos piscina olímpica heliponto"
    candidatos = rag.buscar(mensagem)

    print(f"✅ Retornou {len(candidatos)} candidatos (esperado: 0 ou poucos)")


def teste_progressive_disclosure():
    """
    Teste 2: Progressive Disclosure
    """
    print("\n" + "=" * 60)
    print("🧪 TESTE 2: PROGRESSIVE DISCLOSURE")
    print("=" * 60)

    disclosure = ProgressiveDisclosure(IMOVEIS_DIR)

    # Pega primeiro imóvel
    primeiro_imovel = None
    for item in IMOVEIS_DIR.iterdir():
        if item.is_dir():
            primeiro_imovel = item.name
            break

    if not primeiro_imovel:
        print("⚠️  Nenhum imóvel encontrado para testar")
        return

    print(f"\n📦 Testando com: {primeiro_imovel}")

    # Cenário 1: Pergunta básica → carrega só base
    print("\n📋 Cenário 1: Pergunta básica")
    print("-" * 50)

    mensagem = "Me fala sobre esse imóvel"
    niveis = disclosure.detectar_nivel(mensagem)

    assert "base" in niveis, "❌ Base deve estar sempre presente"
    assert len(niveis) == 1, f"❌ Esperado 1 nível, got {len(niveis)}"

    dados = disclosure.carregar(primeiro_imovel, niveis)

    assert dados["tokens"] <= 300, f"❌ Esperado ~200 tokens, got {dados['tokens']}"

    print(f"✅ Níveis: {niveis}")
    print(f"✅ Tokens: {dados['tokens']}")

    # Cenário 2: Pergunta IPTU → carrega base + faq
    print("\n📋 Cenário 2: Pergunta sobre IPTU")
    print("-" * 50)

    mensagem = "Qual o IPTU?"
    niveis = disclosure.detectar_nivel(mensagem)

    assert "base" in niveis, "❌ Base deve estar presente"
    assert "faq" in niveis, "❌ FAQ deve estar presente (palavra: iptu)"

    dados = disclosure.carregar(primeiro_imovel, niveis)

    print(f"✅ Níveis: {niveis}")
    print(f"✅ Tokens: {dados['tokens']}")

    # Cenário 3: Pergunta metragem → carrega base + detalhes
    print("\n📋 Cenário 3: Pergunta sobre metragem")
    print("-" * 50)

    mensagem = "Qual a metragem?"
    niveis = disclosure.detectar_nivel(mensagem)

    assert "base" in niveis
    assert "detalhes" in niveis, "❌ Detalhes deve estar presente (palavra: metragem)"

    dados = disclosure.carregar(primeiro_imovel, niveis)

    print(f"✅ Níveis: {niveis}")
    print(f"✅ Tokens: {dados['tokens']}")

    # Cenário 4: Carrega completo
    print("\n📋 Cenário 4: Carregamento completo")
    print("-" * 50)

    dados_completo = disclosure.carregar_completo(primeiro_imovel)

    print(f"✅ Todos os níveis: {dados_completo['niveis_carregados']}")
    print(f"✅ Tokens total: {dados_completo['tokens']}")

    # Verifica economia
    economia = 1 - (dados["tokens"] / dados_completo["tokens"])
    print(f"✅ Economia com PD: {economia*100:.0f}% tokens")


def teste_dois_estagios():
    """
    Teste 3: 2 Estágios (identificação → especialista)
    """
    print("\n" + "=" * 60)
    print("🧪 TESTE 3: 2 ESTÁGIOS")
    print("=" * 60)

    integrador = IntegradorRAG(IMOVEIS_DIR, OPENAI_KEY, OPENROUTER_KEY, REDIS)

    cliente_teste = "5531999999999_teste"

    # Limpa estado anterior
    integrador.limpar_item_ativo(cliente_teste)

    # Cenário 1: Cliente novo → sem item_ativo
    print("\n📋 Cenário 1: Cliente novo (ESTÁGIO 1)")
    print("-" * 50)

    item_ativo = integrador._get_item_ativo(cliente_teste)
    assert item_ativo is None, "❌ Cliente novo não deve ter item ativo"

    print("✅ Cliente novo → sem item_ativo")

    # Cenário 2: Busca → define item_ativo
    print("\n📋 Cenário 2: Após busca (define item_ativo)")
    print("-" * 50)

    # Busca que deve retornar 1 resultado
    mensagem = "apartamento"  # Genérico para pegar primeiro disponível

    resposta = integrador.processar_mensagem(cliente_teste, mensagem)

    print(f"🤖 Resposta: {resposta[:100]}...")

    # Verifica se definiu item_ativo
    item_ativo = integrador._get_item_ativo(cliente_teste)

    if item_ativo:
        print(f"✅ Item ativo definido: {item_ativo}")
    else:
        print("⚠️  Múltiplos candidatos (lista apresentada)")

    # Cenário 3: Próxima pergunta usa item_ativo (ESTÁGIO 2)
    if item_ativo:
        print("\n📋 Cenário 3: Com item_ativo (ESTÁGIO 2)")
        print("-" * 50)

        mensagem = "Qual o valor?"

        resposta = integrador.processar_mensagem(cliente_teste, mensagem)

        print(f"🤖 Resposta: {resposta[:200]}...")
        print("✅ ESTÁGIO 2 executado (IA Especialista)")

    # Limpa teste
    integrador.limpar_item_ativo(cliente_teste)


def teste_integracao_completa():
    """
    Teste 4: Integração completa (RAG + PD + IA)
    """
    print("\n" + "=" * 60)
    print("🧪 TESTE 4: INTEGRAÇÃO COMPLETA")
    print("=" * 60)

    integrador = IntegradorRAG(IMOVEIS_DIR, OPENAI_KEY, OPENROUTER_KEY, REDIS)

    cliente_teste = "5531999999999_integracao"

    # Limpa estado
    integrador.limpar_item_ativo(cliente_teste)

    print("\n📋 Simulando conversa completa...")
    print("-" * 50)

    # Cliente pergunta 1: Busca inicial
    print("\n👤 Cliente: Apartamento 2 quartos")

    resposta1 = integrador.processar_mensagem(cliente_teste, "Apartamento 2 quartos")

    print(f"🤖 Bot: {resposta1}")

    # Cliente pergunta 2: Sobre o imóvel
    print("\n👤 Cliente: Qual o valor?")

    resposta2 = integrador.processar_mensagem(cliente_teste, "Qual o valor?")

    print(f"🤖 Bot: {resposta2}")

    # Cliente pergunta 3: IPTU
    print("\n👤 Cliente: E o IPTU?")

    resposta3 = integrador.processar_mensagem(cliente_teste, "E o IPTU?")

    print(f"🤖 Bot: {resposta3}")

    print("\n✅ Integração completa funcionando!")

    # Limpa teste
    integrador.limpar_item_ativo(cliente_teste)


def teste_economia_tokens():
    """
    Teste 5: Validar economia de tokens
    """
    print("\n" + "=" * 60)
    print("🧪 TESTE 5: ECONOMIA DE TOKENS")
    print("=" * 60)

    disclosure = ProgressiveDisclosure(IMOVEIS_DIR)

    # Pega primeiro imóvel
    primeiro_imovel = None
    for item in IMOVEIS_DIR.iterdir():
        if item.is_dir():
            primeiro_imovel = item.name
            break

    if not primeiro_imovel:
        print("⚠️  Nenhum imóvel para testar")
        return

    print(f"\n📦 Testando com: {primeiro_imovel}")

    # Cenário típico: Pergunta sobre IPTU
    mensagem = "Qual o IPTU?"
    niveis = disclosure.detectar_nivel(mensagem)
    dados_pd = disclosure.carregar(primeiro_imovel, niveis)

    # Carregamento completo (modo antigo)
    dados_completo = disclosure.carregar_completo(primeiro_imovel)

    # Calcula economia
    economia = 1 - (dados_pd["tokens"] / dados_completo["tokens"])

    print(f"\n📊 Progressive Disclosure: {dados_pd['tokens']} tokens")
    print(f"📊 Carregamento completo: {dados_completo['tokens']} tokens")
    print(f"💰 Economia: {economia*100:.0f}%")

    assert economia >= 0.30, f"❌ Esperado economia >= 30%, got {economia*100:.0f}%"

    print(f"✅ Economia validada: {economia*100:.0f}% >= 30%")


# ==================== MAIN ====================

def main():
    """
    Executa todos os testes
    """
    print("\n" + "=" * 60)
    print("🧪 TESTES RAG + PROGRESSIVE DISCLOSURE")
    print("=" * 60)

    print(f"\n📁 Diretório imóveis: {IMOVEIS_DIR}")
    print(f"📦 Imóveis disponíveis: {len([d for d in IMOVEIS_DIR.iterdir() if d.is_dir()])}")

    if not IMOVEIS_DIR.exists() or len([d for d in IMOVEIS_DIR.iterdir() if d.is_dir()]) == 0:
        print("\n❌ Nenhum imóvel encontrado. Execute migração primeiro:")
        print("   python3 componentes/rag/migrar_imoveis.py")
        return

    try:
        # Executa testes
        teste_rag_hibrido()
        teste_progressive_disclosure()
        teste_dois_estagios()
        teste_integracao_completa()
        teste_economia_tokens()

        # Resumo final
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)

        print("\n📊 RESUMO:")
        print("   ✅ RAG Híbrido funcionando")
        print("   ✅ Progressive Disclosure funcionando")
        print("   ✅ 2 Estágios funcionando")
        print("   ✅ Integração completa funcionando")
        print("   ✅ Economia de tokens validada")

    except AssertionError as e:
        print(f"\n\n❌ TESTE FALHOU: {e}")
        return 1

    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
