"""
Testes do Sistema de Escalonamento
Validação completa de todos os componentes
"""

import sys
import os
import json

# Adiciona path do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from componentes.escalonamento.triggers import DetectorEscalonamento
from componentes.escalonamento.consulta_agenda import ConsultaAgenda
from componentes.escalonamento.integrador import IntegradorEscalonamento
from upstash_redis import Redis
from config.config import REDIS_URL, REDIS_TOKEN


def teste_detector_triggers():
    """Testa detecção de triggers de escalonamento"""
    print("\n" + "="*60)
    print("🧪 TESTE 1: Detector de Triggers")
    print("="*60)

    detector = DetectorEscalonamento()

    # Caso 1: Cliente pede humano
    mensagem1 = "Quero falar com um atendente humano"
    score1 = 30
    trigger1 = detector.detectar_trigger(mensagem1, score1)
    print(f"\n✓ Mensagem: '{mensagem1}'")
    print(f"  Score: {score1}")
    print(f"  Trigger: {trigger1}")
    assert trigger1 == "cliente_pede_humano", "Deveria detectar 'cliente_pede_humano'"

    # Caso 2: Cliente frustrado
    mensagem2 = "Isso não está funcionando, péssimo"
    score2 = 45
    trigger2 = detector.detectar_trigger(mensagem2, score2)
    print(f"\n✓ Mensagem: '{mensagem2}'")
    print(f"  Score: {score2}")
    print(f"  Trigger: {trigger2}")
    assert trigger2 == "frustrado", "Deveria detectar 'frustrado'"

    # Caso 3: Quer visitar (score OK)
    mensagem3 = "Quero visitar o imóvel"
    score3 = 65
    trigger3 = detector.detectar_trigger(mensagem3, score3)
    print(f"\n✓ Mensagem: '{mensagem3}'")
    print(f"  Score: {score3}")
    print(f"  Trigger: {trigger3}")
    assert trigger3 == "quer_visitar", "Deveria detectar 'quer_visitar'"

    # Caso 4: Quer visitar (score baixo - não escala)
    mensagem4 = "Quero visitar"
    score4 = 20
    trigger4 = detector.detectar_trigger(mensagem4, score4)
    print(f"\n✓ Mensagem: '{mensagem4}'")
    print(f"  Score: {score4}")
    print(f"  Trigger: {trigger4}")
    # Score < 40, mas quer_visitar é alta prioridade
    assert trigger4 == "quer_visitar", "Alta prioridade ignora score baixo"

    # Caso 5: Lead quente automático
    mensagem5 = "Me fala mais sobre o imóvel"
    score5 = 85
    trigger5 = detector.detectar_trigger(mensagem5, score5)
    print(f"\n✓ Mensagem: '{mensagem5}'")
    print(f"  Score: {score5}")
    print(f"  Trigger: {trigger5}")
    assert trigger5 == "lead_quente", "Score ≥80 deveria disparar 'lead_quente'"

    # Caso 6: Mensagem normal (não escala)
    mensagem6 = "Qual o endereço?"
    score6 = 50
    trigger6 = detector.detectar_trigger(mensagem6, score6)
    print(f"\n✓ Mensagem: '{mensagem6}'")
    print(f"  Score: {score6}")
    print(f"  Trigger: {trigger6}")
    assert trigger6 is None, "Não deveria escalonar"

    print("\n✅ TESTE 1 PASSOU\n")


def teste_consulta_agenda():
    """Testa consulta de horários disponíveis (MOCK)"""
    print("\n" + "="*60)
    print("🧪 TESTE 2: Consulta de Agenda (MOCK)")
    print("="*60)

    agenda = ConsultaAgenda(use_mock=True)

    # Busca horários
    horarios = agenda.buscar_horarios_disponiveis(dias_frente=3, limite=3)

    print(f"\n✓ Horários encontrados: {len(horarios)}")
    assert len(horarios) == 3, "Deveria retornar 3 horários"

    for i, h in enumerate(horarios, 1):
        print(f"\n  {i}. {h['data_formatada']} às {h['hora']} ({h['corretor']})")
        assert h['data'], "Data não pode ser vazia"
        assert h['hora'], "Hora não pode ser vazia"
        assert h['corretor'], "Corretor não pode ser vazio"
        assert h['mock'] == True, "Deveria estar em modo MOCK"

    # Testa agendamento
    print("\n✓ Testando agendamento...")
    sucesso = agenda.agendar_visita(
        cliente_numero="5531980160822",
        imovel_id="apto-001",
        horario=horarios[0]
    )
    assert sucesso == True, "Agendamento deveria ter sucesso"

    print("\n✅ TESTE 2 PASSOU\n")


def teste_integrador_escalonamento():
    """Testa pipeline completo de escalonamento"""
    print("\n" + "="*60)
    print("🧪 TESTE 3: Integrador de Escalonamento")
    print("="*60)

    integrador = IntegradorEscalonamento()
    redis_client = Redis(
        url=REDIS_URL,
        token=REDIS_TOKEN
    )

    # Limpa Redis (teste)
    cliente_teste = "5531999999999"
    redis_client.delete(f"bot_standby:{cliente_teste}")
    redis_client.delete(f"opcoes_horario:{cliente_teste}")

    # Caso 1: Mensagem normal (não escala)
    print("\n✓ Caso 1: Mensagem normal")
    mensagem1 = "Qual o endereço?"
    score1 = 50
    resposta1 = integrador.processar_mensagem(cliente_teste, mensagem1, score1)
    print(f"  Mensagem: '{mensagem1}'")
    print(f"  Resposta: {resposta1}")
    assert resposta1 is None, "Não deveria escalonar"

    # Caso 2: Cliente pede humano (escala)
    print("\n✓ Caso 2: Cliente pede humano")
    mensagem2 = "Quero falar com corretor"
    score2 = 40

    # Mock chatwoot (para não fazer chamada real)
    integrador.chatwoot.buscar_conversa_id = lambda n: None  # Simula não encontrado

    resposta2 = integrador.processar_mensagem(cliente_teste, mensagem2, score2)
    print(f"  Mensagem: '{mensagem2}'")
    print(f"  Resposta: '{resposta2}'")
    assert resposta2 is not None, "Deveria retornar mensagem de escalonamento"
    assert "chamar" in resposta2.lower(), "Resposta deveria mencionar 'chamar'"

    # Verifica standby
    standby = redis_client.get(f"bot_standby:{cliente_teste}")
    print(f"  Bot standby: {standby}")
    assert standby == "true", "Bot deveria entrar em standby"

    # Caso 3: Mensagem em standby (não responde)
    print("\n✓ Caso 3: Cliente em standby")
    mensagem3 = "Oi"
    score3 = 50
    resposta3 = integrador.processar_mensagem(cliente_teste, mensagem3, score3)
    print(f"  Mensagem: '{mensagem3}'")
    print(f"  Resposta: {resposta3}")
    assert resposta3 is None, "Bot em standby não deveria responder"

    # Limpa standby
    redis_client.delete(f"bot_standby:{cliente_teste}")

    print("\n✅ TESTE 3 PASSOU\n")


def teste_sugestao_horarios():
    """Testa sugestão de horários"""
    print("\n" + "="*60)
    print("🧪 TESTE 4: Sugestão de Horários")
    print("="*60)

    integrador = IntegradorEscalonamento()
    redis_client = Redis(
        url=REDIS_URL,
        token=REDIS_TOKEN
    )

    cliente_teste = "5531888888888"

    # Limpa Redis
    redis_client.delete(f"opcoes_horario:{cliente_teste}")

    # Sugere horários
    print("\n✓ Sugerindo horários...")
    mensagem = integrador.sugerir_horarios(cliente_teste, "apto-001")
    print(f"\nMensagem:\n{mensagem}")

    assert "1️⃣" in mensagem, "Deveria conter emoji de número"
    assert "às" in mensagem, "Deveria conter horários"

    # Verifica se salvou no Redis
    opcoes_json = redis_client.get(f"opcoes_horario:{cliente_teste}")
    assert opcoes_json is not None, "Opções deveriam estar no Redis"

    opcoes = json.loads(opcoes_json)
    print(f"\n✓ Opções salvas no Redis: {len(opcoes)} horários")

    # Confirma agendamento
    print("\n✓ Confirmando escolha...")
    sucesso, msg_confirmacao = integrador.confirmar_agendamento(
        cliente_numero=cliente_teste,
        escolha="1",
        imovel_id="apto-001"
    )

    print(f"  Sucesso: {sucesso}")
    print(f"  Mensagem: {msg_confirmacao}")

    assert sucesso == True, "Confirmação deveria ter sucesso"
    assert "✅" in msg_confirmacao or "Agendado" in msg_confirmacao, "Mensagem deveria confirmar"

    # Verifica se limpou Redis
    opcoes_apos = redis_client.get(f"opcoes_horario:{cliente_teste}")
    assert opcoes_apos is None, "Opções deveriam ser limpas após confirmação"

    print("\n✅ TESTE 4 PASSOU\n")


def executar_todos_testes():
    """Executa bateria completa de testes"""
    print("\n" + "="*70)
    print("🚀 EXECUTANDO TESTES DO SISTEMA DE ESCALONAMENTO")
    print("="*70)

    try:
        teste_detector_triggers()
        teste_consulta_agenda()
        teste_integrador_escalonamento()
        teste_sugestao_horarios()

        print("\n" + "="*70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*70)
        print("\n📊 Resumo:")
        print("  • Detector de Triggers: ✅")
        print("  • Consulta Agenda (MOCK): ✅")
        print("  • Integrador Completo: ✅")
        print("  • Sugestão de Horários: ✅")
        print("\n🎯 Sistema de Escalonamento funcionando corretamente!\n")

        return True

    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = executar_todos_testes()
    sys.exit(0 if sucesso else 1)
