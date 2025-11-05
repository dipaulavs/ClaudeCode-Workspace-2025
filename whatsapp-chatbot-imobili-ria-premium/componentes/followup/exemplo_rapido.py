#!/usr/bin/env python3
"""
Exemplo Rápido - Sistema de Follow-up

Demonstra uso básico do sistema de follow-ups.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from componentes.followup import SistemaFollowUp, DetectorAbandono, IntegradorFollowUp


def exemplo_1_agendamento_basico():
    """
    Exemplo 1: Agendar follow-up básico
    """
    print("\n" + "="*60)
    print("EXEMPLO 1: Agendamento Básico")
    print("="*60 + "\n")

    sistema = SistemaFollowUp()

    # Agendar follow-up de inatividade (2h)
    followup_id = sistema.agendar("5531999999999", "inatividade_2h")

    print(f"✅ Follow-up agendado: {followup_id}")
    print("   Será enviado em 2 horas")


def exemplo_2_com_contexto():
    """
    Exemplo 2: Follow-up com dados de contexto
    """
    print("\n" + "="*60)
    print("EXEMPLO 2: Follow-up com Contexto")
    print("="*60 + "\n")

    sistema = SistemaFollowUp()

    # Agendar follow-up com região
    followup_id = sistema.agendar(
        "5531999999999",
        "inatividade_48h",
        dados_contexto={"regiao": "Savassi"}
    )

    print(f"✅ Follow-up personalizado agendado: {followup_id}")
    print("   Mensagem: 'Oi! Achei mais opções na Savassi. Quer ver?'")


def exemplo_3_detector_abandono():
    """
    Exemplo 3: Detectar tipo de abandono
    """
    print("\n" + "="*60)
    print("EXEMPLO 3: Detector de Abandono")
    print("="*60 + "\n")

    detector = DetectorAbandono()

    mensagens = [
        "só to olhando",
        "depois eu vejo isso",
        "não sei se gosto",
        "muito caro",
        None
    ]

    for mensagem in mensagens:
        tipo = detector.detectar_tipo(mensagem)
        escolha = detector.escolher_followup(tipo)

        msg_display = f'"{mensagem}"' if mensagem else "(sem mensagem)"
        print(f"{msg_display}")
        print(f"  → Tipo: {tipo}")
        print(f"  → Trigger: {escolha['trigger']}")
        print(f"  → Mensagem: {escolha['mensagem'][:50]}...\n")


def exemplo_4_integrador():
    """
    Exemplo 4: Usar integrador (callbacks)
    """
    print("\n" + "="*60)
    print("EXEMPLO 4: Integrador com Chatbot")
    print("="*60 + "\n")

    integrador = IntegradorFollowUp()
    numero = "5531999999999"

    print("1. Bot envia mensagem")
    integrador.on_mensagem_bot_enviada(numero, "Oi! Posso te ajudar?")
    print("   → Follow-up de inatividade agendado (2h)\n")

    print("2. Cliente responde")
    integrador.on_mensagem_cliente_recebida(numero, "Oi! Quero apartamento")
    print("   → Follow-ups cancelados (cliente ativo)\n")

    print("3. Bot envia fotos")
    integrador.on_fotos_enviadas(numero, "imovel_123", quantidade=5)
    print("   → Follow-up pós-fotos agendado (1h)\n")

    print("4. Visita agendada")
    data_visita = datetime.now() + timedelta(days=1, hours=15)
    integrador.on_visita_agendada(numero, data_visita, "imovel_123")
    print("   → Lembretes agendados (24h e 2h antes)\n")


def exemplo_5_cancelamento():
    """
    Exemplo 5: Cancelar follow-ups
    """
    print("\n" + "="*60)
    print("EXEMPLO 5: Cancelamento")
    print("="*60 + "\n")

    sistema = SistemaFollowUp()
    numero = "5531999999999"

    # Agendar 3 follow-ups
    sistema.agendar(numero, "inatividade_2h")
    sistema.agendar(numero, "inatividade_24h")
    sistema.agendar(numero, "pos_fotos")

    print("3 follow-ups agendados\n")

    # Cancelar todos
    cancelados = sistema.cancelar_todos(numero)

    print(f"✅ {cancelados} follow-ups cancelados")


def exemplo_6_historico():
    """
    Exemplo 6: Ver histórico de follow-ups
    """
    print("\n" + "="*60)
    print("EXEMPLO 6: Histórico de Follow-ups")
    print("="*60 + "\n")

    integrador = IntegradorFollowUp()
    numero = "5531999999999"

    # Buscar histórico
    historico = integrador.obter_historico(numero, limite=5)

    if historico:
        print(f"Últimos {len(historico)} follow-ups:\n")
        for imóvel in historico:
            print(f"  • {imóvel['timestamp_formatado']}")
            print(f"    Trigger: {imóvel['trigger']}")
            print(f"    Enviado: {'Sim' if imóvel['enviado'] else 'Não'}")
            print(f"    Respondeu: {'Sim' if imóvel['respondeu'] else 'Não'}\n")
    else:
        print("Nenhum follow-up no histórico")


def menu_interativo():
    """
    Menu interativo para testar exemplos
    """
    print("\n" + "="*60)
    print("🔔 SISTEMA DE FOLLOW-UPS - EXEMPLOS RÁPIDOS")
    print("="*60)

    exemplos = [
        ("Agendamento Básico", exemplo_1_agendamento_basico),
        ("Follow-up com Contexto", exemplo_2_com_contexto),
        ("Detector de Abandono", exemplo_3_detector_abandono),
        ("Integrador (Callbacks)", exemplo_4_integrador),
        ("Cancelamento", exemplo_5_cancelamento),
        ("Histórico", exemplo_6_historico)
    ]

    while True:
        print("\nEscolha um exemplo:")
        for i, (nome, _) in enumerate(exemplos, 1):
            print(f"  {i}. {nome}")
        print("  0. Sair")

        try:
            escolha = int(input("\nOpção: "))

            if escolha == 0:
                print("\n👋 Até logo!")
                break
            elif 1 <= escolha <= len(exemplos):
                _, funcao = exemplos[escolha - 1]
                funcao()
            else:
                print("❌ Opção inválida")

        except ValueError:
            print("❌ Digite um número")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Executar exemplo específico
        numero = sys.argv[1]
        funcoes = {
            "1": exemplo_1_agendamento_basico,
            "2": exemplo_2_com_contexto,
            "3": exemplo_3_detector_abandono,
            "4": exemplo_4_integrador,
            "5": exemplo_5_cancelamento,
            "6": exemplo_6_historico
        }

        if numero in funcoes:
            funcoes[numero]()
        else:
            print("❌ Exemplo inválido")
            print("Uso: python3 exemplo_rapido.py [1-6]")
    else:
        # Menu interativo
        menu_interativo()
