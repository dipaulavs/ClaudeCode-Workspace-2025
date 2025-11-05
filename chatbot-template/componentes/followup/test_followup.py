"""
Testes do Sistema de Follow-up

Valida agendamento, processamento e cancelamento.
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from componentes.followup import SistemaFollowUp, DetectorAbandono, IntegradorFollowUp


# Cliente de teste
CLIENTE_TESTE = "5531999999999"


def limpar_testes():
    """
    Remove dados de testes anteriores.
    """
    sistema = SistemaFollowUp()

    # Cancelar follow-ups do cliente teste
    sistema.cancelar_todos(CLIENTE_TESTE)

    # Limpar histórico
    sistema.redis_client.delete(f"followup_history:{CLIENTE_TESTE}")

    # Limpar contadores
    for tipo in ["inatividade", "pos_interacao", "lembrete"]:
        sistema.redis_client.delete(f"followup_count:{CLIENTE_TESTE}:{tipo}")

    print("🧹 Dados de teste limpos\n")


def teste_agendamento():
    """
    Testa agendamento de follow-up.
    """
    print("📝 TESTE 1: Agendamento")
    print("-" * 60)

    sistema = SistemaFollowUp()

    # Agendar follow-up
    followup_id = sistema.agendar(CLIENTE_TESTE, "inatividade_2h")

    assert followup_id is not None, "❌ Follow-up não foi agendado"

    # Verificar que está na fila
    followups = sistema.redis_client.zrange("followups", 0, -1)
    encontrado = False

    for followup_json in followups:
        followup = json.loads(followup_json)
        if followup["id"] == followup_id:
            encontrado = True
            assert followup["cliente"] == CLIENTE_TESTE
            assert followup["trigger"] == "inatividade_2h"
            break

    assert encontrado, "❌ Follow-up não encontrado na fila"

    print("✅ Follow-up agendado com sucesso\n")


def teste_agendamento_com_contexto():
    """
    Testa agendamento com dados de contexto.
    """
    print("📝 TESTE 2: Agendamento com Contexto")
    print("-" * 60)

    sistema = SistemaFollowUp()

    # Agendar follow-up com região
    followup_id = sistema.agendar(
        CLIENTE_TESTE,
        "inatividade_48h",
        dados_contexto={"regiao": "Savassi"}
    )

    assert followup_id is not None, "❌ Follow-up não foi agendado"

    # Verificar mensagem personalizada
    followups = sistema.redis_client.zrange("followups", 0, -1)

    for followup_json in followups:
        followup = json.loads(followup_json)
        if followup["id"] == followup_id:
            assert "Savassi" in followup["mensagem"]
            break

    print("✅ Follow-up com contexto agendado\n")


def teste_cancelamento():
    """
    Testa cancelamento de follow-up.
    """
    print("📝 TESTE 3: Cancelamento")
    print("-" * 60)

    sistema = SistemaFollowUp()

    # Agendar 3 follow-ups
    id1 = sistema.agendar(CLIENTE_TESTE, "inatividade_2h")
    id2 = sistema.agendar(CLIENTE_TESTE, "inatividade_24h")
    id3 = sistema.agendar(CLIENTE_TESTE, "pos_fotos")

    # Cancelar todos
    cancelados = sistema.cancelar_todos(CLIENTE_TESTE)

    assert cancelados == 3, f"❌ Esperava 3 cancelamentos, obteve {cancelados}"

    # Verificar que foram removidos
    followups = sistema.redis_client.zrange("followups", 0, -1)
    for followup_json in followups:
        followup = json.loads(followup_json)
        assert followup["cliente"] != CLIENTE_TESTE, "❌ Follow-up não foi cancelado"

    print("✅ Follow-ups cancelados com sucesso\n")


def teste_processamento():
    """
    Testa processamento de follow-ups vencidos.
    """
    print("📝 TESTE 4: Processamento")
    print("-" * 60)

    sistema = SistemaFollowUp()

    # Agendar follow-up no passado (simular vencido)
    followup_data = {
        "id": f"fu_teste_{int(time.time())}",
        "cliente": CLIENTE_TESTE,
        "trigger": "inatividade_2h",
        "tipo": "inatividade",
        "mensagem": "Teste de processamento",
        "tentativa": 1,
        "criado_em": time.time()
    }

    # Adicionar com timestamp no passado
    sistema.redis_client.zadd(
        "followups",
        {json.dumps(followup_data): time.time() - 10}  # 10 segundos atrás
    )

    print("⚠️  Nota: Teste de envio será simulado (pode falhar se Evolution API não estiver acessível)")

    # Processar
    try:
        enviados = sistema.processar_pendentes()
        print(f"✓ {enviados} follow-up(s) processado(s)")
    except Exception as e:
        print(f"⚠️  Erro ao enviar (esperado em ambiente de teste): {e}")

    # Verificar que foi removido da fila
    followups = sistema.redis_client.zrange("followups", 0, -1)
    for followup_json in followups:
        followup = json.loads(followup_json)
        assert followup["id"] != followup_data["id"], "❌ Follow-up não foi removido"

    print("✅ Follow-up processado\n")


def teste_max_tentativas():
    """
    Testa limite de tentativas.
    """
    print("📝 TESTE 5: Limite de Tentativas")
    print("-" * 60)

    sistema = SistemaFollowUp()

    # Simular 3 tentativas
    for i in range(3):
        sistema.registrar_envio(CLIENTE_TESTE, "inatividade_2h", "inatividade")

    # Tentar agendar quarta tentativa (deve falhar)
    followup_id = sistema.agendar(CLIENTE_TESTE, "inatividade_2h")

    assert followup_id is None, "❌ Deveria ter bloqueado quarta tentativa"

    print("✅ Limite de tentativas respeitado\n")


def teste_detector_abandono():
    """
    Testa detecção de tipos de abandono.
    """
    print("📝 TESTE 6: Detector de Abandono")
    print("-" * 60)

    detector = DetectorAbandono()

    # Testar diferentes mensagens
    casos = [
        ("só to olhando", "curioso"),
        ("depois eu vejo isso", "preguicoso"),
        ("não sei se gosto", "indeciso"),
        ("gostei bastante", "interessado"),
        ("muito caro esse", "negociador"),
        (None, "sumiu")
    ]

    for mensagem, tipo_esperado in casos:
        tipo = detector.detectar_tipo(mensagem)
        assert tipo == tipo_esperado, f"❌ Esperava '{tipo_esperado}', obteve '{tipo}'"
        print(f"  ✓ '{mensagem}' → {tipo}")

    print("\n✅ Detector funcionando corretamente\n")


def teste_integrador():
    """
    Testa integrador com chatbot.
    """
    print("📝 TESTE 7: Integrador")
    print("-" * 60)

    integrador = IntegradorFollowUp()

    # Simular bot enviando mensagem
    integrador.on_mensagem_bot_enviada(CLIENTE_TESTE, "Oi! Como posso ajudar?")

    # Verificar que follow-up foi agendado
    followups = integrador.sistema.redis_client.zrange("followups", 0, -1)
    agendado = False

    for followup_json in followups:
        followup = json.loads(followup_json)
        if followup["cliente"] == CLIENTE_TESTE:
            agendado = True
            break

    assert agendado, "❌ Follow-up não foi agendado"

    # Simular cliente respondendo
    integrador.on_mensagem_cliente_recebida(CLIENTE_TESTE, "Oi! Tô procurando apartamento")

    # Verificar que follow-ups foram cancelados
    followups = integrador.sistema.redis_client.zrange("followups", 0, -1)
    for followup_json in followups:
        followup = json.loads(followup_json)
        assert followup["cliente"] != CLIENTE_TESTE, "❌ Follow-up não foi cancelado"

    print("✅ Integrador funcionando\n")


def teste_lembrete_visita():
    """
    Testa agendamento de lembretes de visita.
    """
    print("📝 TESTE 8: Lembretes de Visita")
    print("-" * 60)

    integrador = IntegradorFollowUp()

    # Agendar visita para 25 horas no futuro (para testar lembrete 24h)
    data_visita = datetime.now() + timedelta(hours=25)

    integrador.on_visita_agendada(
        CLIENTE_TESTE,
        data_visita,
        "imovel_123"
    )

    # Verificar que lembretes foram agendados
    followups = integrador.sistema.redis_client.zrange("followups", 0, -1)
    lembretes = []

    for followup_json in followups:
        followup = json.loads(followup_json)
        if followup["cliente"] == CLIENTE_TESTE and "lembrete" in followup["trigger"]:
            lembretes.append(followup["trigger"])

    assert "lembrete_visita_24h" in lembretes, "❌ Lembrete 24h não agendado"
    assert "lembrete_visita_2h" in lembretes, "❌ Lembrete 2h não agendado"

    print("✅ Lembretes de visita agendados\n")


def executar_todos_testes():
    """
    Executa suite completa de testes.
    """
    print("\n" + "="*60)
    print("🧪 SUITE DE TESTES - SISTEMA DE FOLLOW-UP")
    print("="*60 + "\n")

    # Limpar antes de começar
    limpar_testes()

    # Executar testes
    testes = [
        teste_agendamento,
        teste_agendamento_com_contexto,
        teste_cancelamento,
        teste_processamento,
        teste_max_tentativas,
        teste_detector_abandono,
        teste_integrador,
        teste_lembrete_visita
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

        # Limpar entre testes
        limpar_testes()

    # Resumo
    print("="*60)
    print("📊 RESUMO")
    print("="*60)
    print(f"✅ Passou: {passou}")
    print(f"❌ Falhou: {falhou}")
    print(f"📈 Taxa de sucesso: {passou/(passou+falhou)*100:.1f}%")
    print("="*60 + "\n")

    return falhou == 0


if __name__ == "__main__":
    sucesso = executar_todos_testes()
    sys.exit(0 if sucesso else 1)
