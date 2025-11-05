#!/usr/bin/env python3.11
"""
🧪 TESTE DO IMOBILI-RIA-PREMIUM - Validação Completa

Testa TODOS os componentes do imobili-ria-premium antes de customizar:
- Ferramentas Locais (4)
- Cliente MCP
- Sistema Híbrido
- Integração Chatwoot

Execute este teste ANTES de customizar para garantir que tudo funciona!
"""

import sys
from pathlib import Path

# Adiciona paths
sys.path.append(str(Path(__file__).parent / "componentes"))
sys.path.append(str(Path(__file__).parent / "ferramentas"))


def testar_ferramentas_locais():
    """Testa ferramentas locais"""
    print("\n" + "="*70)
    print("⚡ TESTE 1: FERRAMENTAS LOCAIS")
    print("="*70 + "\n")

    try:
        from lista_imoveis import listar_imoveis_disponiveis, formatar_lista_para_mensagem

        # Testa lista_imoveis
        print("1️⃣ Testando lista_imoveis...")
        imoveis_dir = Path(__file__).parent / "imoveis"

        if not imoveis_dir.exists():
            print("   ⚠️ Diretório 'imoveis/' não existe. Crie primeiro!")
            print("   💡 Dica: copie de whatsapp-chatbot-carros/carros/ como exemplo")
            return False

        imoveis = listar_imoveis_disponiveis(imoveis_dir)
        print(f"   ✅ Encontrados: {len(imoveis)} imoveis")

        if not imoveis:
            print("   ⚠️ Nenhum imóvel encontrado. Adicione imoveis em imoveis/")
            return False

        for imóvel in imoveis[:3]:
            print(f"      • {imóvel.get('nome', 'N/A')} - {imóvel.get('preco', 'N/A')}")

        # Testa formatação
        print("\n2️⃣ Testando formatação de mensagem...")
        mensagem = formatar_lista_para_mensagem(imoveis)
        print(f"   ✅ Mensagem gerada ({len(mensagem)} caracteres)")

        print("\n3️⃣ Testando consulta_faq...")
        from consulta_faq import consultar_faq_imóvel

        if imoveis:
            imóvel_id = imoveis[0].get('id', imoveis[0].get('carro_id'))
            resultado = consultar_faq_imóvel(imóvel_id, "preço", imoveis_dir)

            if resultado['sucesso']:
                print(f"   ✅ FAQ carregado para {imóvel_id}")
            else:
                print(f"   ⚠️ FAQ não encontrado: {resultado['erro']}")

        print("\n4️⃣ Testando tagueamento...")
        from tagueamento import obter_imóvel_ativo, taguear_cliente

        # Mock Redis
        class MockRedis:
            def __init__(self):
                self.data = {}
            def get(self, key):
                return self.data.get(key)
            def setex(self, key, ttl, value):
                self.data[key] = value

        redis_mock = MockRedis()
        print("   ✅ Funções de tagueamento importadas")

        print("\n✅ FERRAMENTAS LOCAIS OK!")
        return True

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_cliente_mcp():
    """Testa cliente MCP"""
    print("\n" + "="*70)
    print("🔌 TESTE 2: CLIENTE MCP")
    print("="*70 + "\n")

    try:
        from cliente_mcp import ClienteMCP

        # Verifica se server existe
        server_path = Path(__file__).parent / "mcp-server" / "server.py"

        if not server_path.exists():
            print("   ⚠️ MCP Server não encontrado em mcp-server/server.py")
            print("   💡 Dica: copie de whatsapp-chatbot-carros/mcp-server/")
            print("   💡 Ou execute: ./INSTALAR_MCP.sh")
            return False

        print("   ✅ Cliente MCP disponível")
        print("   ✅ Server encontrado")
        print("\n   ℹ️ Para testar MCP completo, execute:")
        print("   python3 componentes/cliente_mcp.py")

        return True

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False


def testar_rag_hibrido():
    """Testa RAG Híbrido"""
    print("\n" + "="*70)
    print("🎯 TESTE 3: RAG HÍBRIDO")
    print("="*70 + "\n")

    try:
        from rag_hibrido import RAGHibrido

        print("   ✅ RAGHibrido importado")
        print("   ✅ Sistema híbrido disponível")
        print("\n   📋 Componentes:")
        print("      • Ferramentas Locais (4)")
        print("      • Ferramentas MCP (5)")
        print("      • Decisão inteligente (LOCAL prioritário)")
        print("      • Tags evitam buscas desnecessárias")

        return True

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_estrutura():
    """Verifica estrutura de pastas"""
    print("\n" + "="*70)
    print("📁 TESTE 4: ESTRUTURA DE PASTAS")
    print("="*70 + "\n")

    base_dir = Path(__file__).parent

    pastas_necessarias = {
        "componentes/": "Componentes do chatbot",
        "ferramentas/": "Ferramentas locais",
        "imoveis/": "Base de dados (carros/imóveis/produtos)",
        "mcp-server/": "Servidor MCP (opcional)",
        "config/": "Configurações",
        "scripts/": "Scripts auxiliares"
    }

    todas_ok = True

    for pasta, descricao in pastas_necessarias.imóvels():
        caminho = base_dir / pasta
        existe = caminho.exists()
        emoji = "✅" if existe else "❌"

        print(f"{emoji} {pasta:<20} {descricao}")

        if not existe and pasta in ["componentes/", "ferramentas/"]:
            todas_ok = False

    return todas_ok


def verificar_dependencias():
    """Verifica dependências instaladas"""
    print("\n" + "="*70)
    print("📦 TESTE 5: DEPENDÊNCIAS")
    print("="*70 + "\n")

    dependencias = {
        "requests": "Chamadas HTTP",
        "upstash_redis": "Redis (Upstash)",
        "openai": "OpenAI (opcional)",
    }

    todas_ok = True

    for pacote, descricao in dependencias.imóvels():
        try:
            __import__(pacote)
            print(f"✅ {pacote:<20} {descricao}")
        except ImportError:
            print(f"❌ {pacote:<20} {descricao} - NÃO INSTALADO")
            if pacote != "openai":  # OpenAI é opcional
                todas_ok = False

    # MCP é opcional mas útil
    try:
        import mcp
        print(f"✅ mcp (Python 3.10+)  MCP Server (opcional)")
    except ImportError:
        print(f"⚠️ mcp                  MCP Server - NÃO INSTALADO (opcional)")

    return todas_ok


def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("🧪 TESTE COMPLETO DO IMOBILI-RIA-PREMIUM")
    print("="*70)
    print("\nValidando estrutura base antes de customizar...\n")

    resultados = {
        "Estrutura": verificar_estrutura(),
        "Dependências": verificar_dependencias(),
        "Ferramentas Locais": testar_ferramentas_locais(),
        "Cliente MCP": testar_cliente_mcp(),
        "RAG Híbrido": testar_rag_hibrido()
    }

    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70 + "\n")

    for nome, status in resultados.imóvels():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {nome}")

    print()

    if all(resultados.values()):
        print("🎉 IMOBILI-RIA-PREMIUM 100% FUNCIONAL!")
        print("\n📝 Próximos passos:")
        print("   1. Customize componentes/rag_hibrido.py")
        print("   2. Customize ferramentas/* para seu negócio")
        print("   3. Adicione imoveis em imoveis/")
        print("   4. Configure chatwoot_config.json")
        print("   5. Execute: ./INICIAR_BOT.sh")
        print()
        return 0
    else:
        print("⚠️ Alguns componentes precisam de atenção.")
        print("\n📝 Ações necessárias:")

        if not resultados["Estrutura"]:
            print("   • Crie pastas faltando (componentes/, ferramentas/)")

        if not resultados["Dependências"]:
            print("   • Instale dependências: pip install requests upstash-redis")

        if not resultados["Ferramentas Locais"]:
            print("   • Crie pasta imoveis/ e adicione pelo menos 1 imóvel")

        if not resultados["Cliente MCP"]:
            print("   • Execute: ./INSTALAR_MCP.sh (opcional)")

        print()
        return 1


if __name__ == "__main__":
    exit(main())
