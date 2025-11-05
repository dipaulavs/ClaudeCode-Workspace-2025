"""
Testes Offline do Sistema de Follow-up

Valida lógica sem depender de Redis/Evolution API.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from componentes.followup.tipos_abandono import DetectorAbandono, TIPOS_ABANDONO
from componentes.followup.sistema_followup import TRIGGERS


def teste_triggers_configurados():
    """
    Valida que todos os triggers estão configurados corretamente.
    """
    print("📝 TESTE 1: Configuração de Triggers")
    print("-" * 60)

    triggers_obrigatorios = [
        "inatividade_2h",
        "inatividade_24h",
        "inatividade_48h",
        "pos_fotos",
        "pos_visita",
        "lembrete_visita_24h",
        "lembrete_visita_2h"
    ]

    for trigger in triggers_obrigatorios:
        assert trigger in TRIGGERS, f"❌ Trigger '{trigger}' não encontrado"
        config = TRIGGERS[trigger]

        # Validar estrutura
        assert "delay" in config, f"❌ '{trigger}' sem delay"
        assert "mensagem" in config, f"❌ '{trigger}' sem mensagem"
        assert "tipo" in config, f"❌ '{trigger}' sem tipo"

        print(f"  ✓ {trigger}: {config['mensagem'][:40]}...")

    print("\n✅ Todos os triggers configurados\n")


def teste_detector_abandono():
    """
    Testa detecção de tipos de abandono.
    """
    print("📝 TESTE 2: Detector de Abandono")
    print("-" * 60)

    detector = DetectorAbandono()

    # Casos de teste
    casos = [
        ("só to olhando", "curioso"),
        ("to dando uma olhada", "curioso"),
        ("vendo opções", "curioso"),

        ("depois eu vejo", "preguicoso"),
        ("vou pensar", "preguicoso"),
        ("deixa eu ver", "preguicoso"),

        ("não sei", "indeciso"),
        ("talvez", "indeciso"),
        ("to em dúvida", "indeciso"),

        ("gostei bastante", "interessado"),
        ("interessante", "interessado"),
        ("parece bom", "interessado"),

        ("muito caro", "negociador"),
        ("desconto", "negociador"),
        ("tem como baixar", "negociador"),

        (None, "sumiu"),
        ("", "sumiu"),
        ("mensagem aleatória xyz", "sumiu")
    ]

    for mensagem, tipo_esperado in casos:
        tipo = detector.detectar_tipo(mensagem)
        assert tipo == tipo_esperado, f"❌ '{mensagem}' → Esperava '{tipo_esperado}', obteve '{tipo}'"
        msg_display = f"'{mensagem}'" if mensagem else "(sem mensagem)"
        print(f"  ✓ {msg_display} → {tipo}")

    print("\n✅ Detector funcionando corretamente\n")


def teste_escolha_followup():
    """
    Testa escolha de follow-up por tipo.
    """
    print("📝 TESTE 3: Escolha de Follow-up")
    print("-" * 60)

    detector = DetectorAbandono()

    tipos = ["curioso", "preguicoso", "indeciso", "interessado", "negociador", "sumiu"]

    for tipo in tipos:
        escolha = detector.escolher_followup(tipo)

        assert "trigger" in escolha, f"❌ '{tipo}' sem trigger"
        assert "mensagem" in escolha, f"❌ '{tipo}' sem mensagem"

        print(f"  ✓ {tipo} → {escolha['trigger']}")

    print("\n✅ Escolha de follow-up funcionando\n")


def teste_tipos_abandono_completos():
    """
    Valida estrutura de tipos de abandono.
    """
    print("📝 TESTE 4: Estrutura de Tipos de Abandono")
    print("-" * 60)

    for tipo, config in TIPOS_ABANDONO.imóvels():
        assert "sinais" in config, f"❌ '{tipo}' sem sinais"
        assert "followup" in config, f"❌ '{tipo}' sem followup"
        assert "mensagem_personalizada" in config, f"❌ '{tipo}' sem mensagem"

        # Validar que followup existe em TRIGGERS
        assert config["followup"] in TRIGGERS, f"❌ '{tipo}' usa trigger inexistente: {config['followup']}"

        print(f"  ✓ {tipo}: {len(config['sinais'])} sinais → {config['followup']}")

    print("\n✅ Estrutura validada\n")


def teste_delays_consistentes():
    """
    Valida que delays estão em ordem lógica.
    """
    print("📝 TESTE 5: Delays Consistentes")
    print("-" * 60)

    # Validar ordem de inatividade
    delay_2h = TRIGGERS["inatividade_2h"]["delay"]
    delay_24h = TRIGGERS["inatividade_24h"]["delay"]
    delay_48h = TRIGGERS["inatividade_48h"]["delay"]

    assert delay_2h < delay_24h < delay_48h, "❌ Delays de inatividade fora de ordem"
    print(f"  ✓ inatividade_2h: {delay_2h/3600}h")
    print(f"  ✓ inatividade_24h: {delay_24h/3600}h")
    print(f"  ✓ inatividade_48h: {delay_48h/3600}h")

    # Validar lembretes negativos
    lembrete_24h = TRIGGERS["lembrete_visita_24h"]["delay"]
    lembrete_2h = TRIGGERS["lembrete_visita_2h"]["delay"]

    assert lembrete_24h < 0, "❌ Lembrete 24h deveria ser negativo"
    assert lembrete_2h < 0, "❌ Lembrete 2h deveria ser negativo"
    assert lembrete_24h < lembrete_2h < 0, "❌ Lembretes fora de ordem"

    print(f"  ✓ lembrete_visita_24h: {lembrete_24h/3600}h (antes)")
    print(f"  ✓ lembrete_visita_2h: {lembrete_2h/3600}h (antes)")

    print("\n✅ Delays consistentes\n")


def teste_mensagens_validas():
    """
    Valida que mensagens têm conteúdo adequado.
    """
    print("📝 TESTE 6: Mensagens Válidas")
    print("-" * 60)

    for trigger, config in TRIGGERS.imóvels():
        mensagem = config["mensagem"]

        # Validar comprimento
        assert len(mensagem) > 10, f"❌ '{trigger}' com mensagem muito curta"
        assert len(mensagem) < 200, f"❌ '{trigger}' com mensagem muito longa"

        # Validar que não tem placeholders sem contexto
        if "{" in mensagem and not config.get("precisa_contexto"):
            raise AssertionError(f"❌ '{trigger}' tem placeholder mas não marca precisa_contexto")

        emoji_count = sum(1 for c in mensagem if ord(c) > 0x1F300)
        print(f"  ✓ {trigger}: {len(mensagem)} chars, {emoji_count} emoji(s)")

    print("\n✅ Mensagens válidas\n")


def teste_tipos_consistentes():
    """
    Valida que tipos de trigger estão corretos.
    """
    print("📝 TESTE 7: Tipos de Trigger")
    print("-" * 60)

    tipos_validos = ["inatividade", "pos_interacao", "lembrete"]

    for trigger, config in TRIGGERS.imóvels():
        tipo = config["tipo"]
        assert tipo in tipos_validos, f"❌ '{trigger}' com tipo inválido: {tipo}"
        print(f"  ✓ {trigger} → {tipo}")

    print("\n✅ Tipos consistentes\n")


def executar_todos_testes():
    """
    Executa suite completa de testes offline.
    """
    print("\n" + "="*60)
    print("🧪 SUITE DE TESTES OFFLINE - SISTEMA DE FOLLOW-UP")
    print("="*60 + "\n")

    testes = [
        teste_triggers_configurados,
        teste_detector_abandono,
        teste_escolha_followup,
        teste_tipos_abandono_completos,
        teste_delays_consistentes,
        teste_mensagens_validas,
        teste_tipos_consistentes
    ]

    passou = 0
    falhou = 0

    for teste in testes:
        try:
            teste()
            passou += 1
        except AssertionError as e:
            print(f"❌ FALHOU: {e}\n")
            falhou += 1
        except Exception as e:
            print(f"❌ ERRO: {e}\n")
            import traceback
            traceback.print_exc()
            falhou += 1

    # Resumo
    print("="*60)
    print("📊 RESUMO")
    print("="*60)
    print(f"✅ Passou: {passou}")
    print(f"❌ Falhou: {falhou}")
    print(f"📈 Taxa de sucesso: {passou/(passou+falhou)*100:.1f}%")
    print("="*60 + "\n")

    if falhou == 0:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n⚠️  NOTA: Testes offline validam apenas a lógica.")
        print("Para testar Redis e Evolution API, execute o chatbot em produção.")

    return falhou == 0


if __name__ == "__main__":
    sucesso = executar_todos_testes()
    sys.exit(0 if sucesso else 1)
