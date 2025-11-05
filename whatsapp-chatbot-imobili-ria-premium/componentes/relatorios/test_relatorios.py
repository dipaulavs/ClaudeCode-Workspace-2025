#!/usr/bin/env python3
"""
Testes do sistema de relatórios
"""

import sys
import os
from datetime import datetime, date, timedelta

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')

from componentes.relatorios import ColetorMetricas, GeradorRelatorio, DashboardSemanal, IntegradorMetricas


def test_coletor_metricas():
    """Testa coleta de métricas"""
    print("\n🧪 Testando ColetorMetricas...")

    coletor = ColetorMetricas()
    hoje = datetime.now().date()

    # Limpar dados anteriores
    coletor.resetar("leads_novos_hoje", hoje)
    coletor.resetar("bot_atendeu", hoje)

    # Teste 1: Incrementar
    coletor.incrementar("leads_novos_hoje")
    coletor.incrementar("leads_novos_hoje")

    valor = coletor.buscar("leads_novos_hoje", hoje)
    assert valor == 2, f"Esperado 2, obtido {valor}"
    print("✅ Incremento funciona")

    # Teste 2: Lista
    coletor.resetar("leads_quentes", hoje)
    coletor.adicionar_lista("leads_quentes", "5531980160822")
    coletor.adicionar_lista("leads_quentes", "5531988887777")

    lista = coletor.buscar("leads_quentes", hoje)
    assert len(lista) == 2, f"Esperado 2 imoveis, obtido {len(lista)}"
    print("✅ Lista funciona")

    # Teste 3: Sorted Set
    coletor.resetar("imoveis_mais_procurados", hoje)
    coletor.incrementar_sorted_set("imoveis_mais_procurados", "imovel_001", 5)
    coletor.incrementar_sorted_set("imoveis_mais_procurados", "imovel_002", 3)
    coletor.incrementar_sorted_set("imoveis_mais_procurados", "imovel_001", 2)  # +2 = 7 total

    sorted_set = coletor.buscar("imoveis_mais_procurados", hoje)
    assert len(sorted_set) == 2, f"Esperado 2 imoveis, obtido {len(sorted_set)}"

    # Verifica ordem (maior score primeiro)
    primeiro = sorted_set[0]
    imovel_id = primeiro[0].decode() if isinstance(primeiro[0], bytes) else primeiro[0]
    score = int(primeiro[1])

    assert imovel_id == "imovel_001", f"Esperado imovel_001, obtido {imovel_id}"
    assert score == 7, f"Esperado score 7, obtido {score}"
    print("✅ Sorted Set funciona")

    # Teste 4: Buscar período
    coletor.resetar("leads_novos_hoje", hoje)
    coletor.resetar("leads_novos_hoje", hoje - timedelta(days=1))

    coletor.incrementar("leads_novos_hoje", 10, hoje)
    coletor.incrementar("leads_novos_hoje", 5, hoje - timedelta(days=1))

    total = coletor.buscar_periodo(
        "leads_novos_hoje",
        hoje - timedelta(days=1),
        hoje
    )
    assert total == 15, f"Esperado 15, obtido {total}"
    print("✅ Buscar período funciona")

    print("✅ ColetorMetricas: todos os testes passaram")


def test_gerador_relatorio():
    """Testa geração de relatório"""
    print("\n🧪 Testando GeradorRelatorio...")

    coletor = ColetorMetricas()
    hoje = datetime.now().date()

    # Popular métricas
    coletor.resetar("leads_novos_hoje", hoje)
    coletor.resetar("bot_atendeu", hoje)
    coletor.resetar("escaladas", hoje)
    coletor.resetar("visitas_agendadas", hoje)
    coletor.resetar("propostas_enviadas", hoje)

    coletor.incrementar("leads_novos_hoje", 10, hoje)
    coletor.incrementar("bot_atendeu", 8, hoje)
    coletor.incrementar("escaladas", 2, hoje)
    coletor.incrementar("visitas_agendadas", 3, hoje)
    coletor.incrementar("propostas_enviadas", 1, hoje)

    # Gerar relatório
    gerador = GeradorRelatorio()
    relatorio = gerador.gerar_relatorio_diario(hoje)

    # Validar conteúdo
    assert "RELATÓRIO DIÁRIO" in relatorio, "Título ausente"
    assert "LEADS" in relatorio, "Seção LEADS ausente"
    assert "10" in relatorio, "Leads novos não aparece"
    assert "8" in relatorio, "Bot atendeu não aparece"
    assert "3" in relatorio, "Visitas não aparece"
    assert "BOT" in relatorio, "Seção BOT ausente"
    assert "CONVERSÃO" in relatorio, "Seção CONVERSÃO ausente"

    print("✅ Relatório gerado corretamente")
    print("\n📄 Exemplo de relatório:")
    print(relatorio)

    print("\n✅ GeradorRelatorio: todos os testes passaram")


def test_integrador():
    """Testa integrador de métricas"""
    print("\n🧪 Testando IntegradorMetricas...")

    coletor = ColetorMetricas()
    hoje = datetime.now().date()

    # Limpar
    coletor.resetar("leads_novos_hoje", hoje)
    coletor.resetar("bot_atendeu", hoje)
    coletor.resetar("escaladas", hoje)
    coletor.resetar("leads_quentes", hoje)

    # Usar integrador
    integrador = IntegradorMetricas()

    # Simular eventos
    integrador.on_nova_conversa("5531980160822")
    integrador.on_bot_respondeu("5531980160822")
    integrador.on_lead_quente("5531980160822", 75)

    integrador.on_nova_conversa("5531988887777")
    integrador.on_escalamento("5531988887777")

    # Verificar
    leads_novos = coletor.buscar("leads_novos_hoje", hoje)
    assert leads_novos == 2, f"Esperado 2 leads, obtido {leads_novos}"

    bot_atendeu = coletor.buscar("bot_atendeu", hoje)
    assert bot_atendeu == 1, f"Esperado 1 atendimento, obtido {bot_atendeu}"

    escaladas = coletor.buscar("escaladas", hoje)
    assert escaladas == 1, f"Esperado 1 escalada, obtido {escaladas}"

    leads_quentes = coletor.buscar("leads_quentes", hoje)
    assert len(leads_quentes) == 1, f"Esperado 1 lead quente, obtido {len(leads_quentes)}"

    print("✅ Integrador funciona corretamente")
    print("✅ IntegradorMetricas: todos os testes passaram")


def test_dashboard_semanal():
    """Testa dashboard semanal"""
    print("\n🧪 Testando DashboardSemanal...")

    coletor = ColetorMetricas()
    hoje = datetime.now().date()

    # Popular dados de 7 dias
    for dia in range(7):
        data = hoje - timedelta(days=dia)

        coletor.resetar("leads_novos_hoje", data)
        coletor.resetar("bot_atendeu", data)
        coletor.resetar("visitas_agendadas", data)

        coletor.incrementar("leads_novos_hoje", 5, data)
        coletor.incrementar("bot_atendeu", 4, data)
        coletor.incrementar("visitas_agendadas", 1, data)

    # Gerar dashboard
    dashboard = DashboardSemanal()
    relatorio = dashboard.gerar_relatorio_semanal(hoje)

    # Validar
    assert "RELATÓRIO SEMANAL" in relatorio, "Título ausente"
    assert "RESUMO DA SEMANA" in relatorio, "Seção resumo ausente"
    assert "35" in relatorio, "Total leads novos incorreto (5*7=35)"
    assert "INSIGHTS" in relatorio, "Seção insights ausente"

    print("✅ Dashboard semanal gerado")
    print("\n📄 Exemplo de dashboard:")
    print(relatorio)

    print("\n✅ DashboardSemanal: todos os testes passaram")


def main():
    """Roda todos os testes"""
    print("=" * 60)
    print("🧪 TESTES DO SISTEMA DE RELATÓRIOS")
    print("=" * 60)

    try:
        test_coletor_metricas()
        test_gerador_relatorio()
        test_integrador()
        test_dashboard_semanal()

        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM")
        print("=" * 60)

        return 0

    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {str(e)}")
        return 1

    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
