#!/usr/bin/env python3
"""
📚 EXEMPLOS PRÁTICOS - Como usar o teste de agendamento

Mostra diferentes cenários:
1. Cliente normal (fluxo happy path)
2. Cliente com escolha inválida
3. Cliente com opções expiradas
4. Teste com múltiplos clientes
"""

from datetime import datetime
import sys

# Importar o teste
from testar_agendamento_visita import (
    MockRedis,
    MockIntegradorEscalonamento,
    _notificar_corretor_agendamento,
)


def exemplo_1_fluxo_normal():
    """Exemplo 1: Cliente normal - escolhe horário válido"""
    print("\n" + "="*80)
    print("📌 EXEMPLO 1: Cliente Maria Silva - Fluxo Normal")
    print("="*80)

    redis = MockRedis()
    integrador = MockIntegradorEscalonamento(redis, {})

    # Cliente
    cliente = {
        "numero": "5531987654321",
        "nome": "Maria Silva",
        "imovel": "itatiaiucu-001"
    }

    print(f"\n👤 Cliente: {cliente['nome']} ({cliente['numero']})")

    # Fase 1: Sugerir
    print(f"\n1️⃣ Cliente: 'Quero agendar uma visita'")
    resposta1 = integrador.sugerir_horarios(cliente["numero"], cliente["imovel"])
    print(f"\n🤖 Bot:\n{resposta1}")

    # Fase 2: Escolher
    print(f"\n2️⃣ Cliente: 'Quero a opção 2'")
    sucesso, resposta2 = integrador.confirmar_agendamento(
        cliente["numero"],
        "2",
        cliente["imovel"]
    )

    if sucesso:
        print(f"\n🤖 Bot:\n{resposta2}")
        print(f"\n✅ Agendamento CONFIRMADO")
    else:
        print(f"\n❌ Erro: {resposta2}")

    return sucesso


def exemplo_2_escolha_invalida():
    """Exemplo 2: Cliente tenta escolher opção inválida"""
    print("\n" + "="*80)
    print("📌 EXEMPLO 2: Cliente João - Escolha Inválida")
    print("="*80)

    redis = MockRedis()
    integrador = MockIntegradorEscalonamento(redis, {})

    cliente = {
        "numero": "5531988888888",
        "nome": "João Pedro",
        "imovel": "itatiaiucu-001"
    }

    print(f"\n👤 Cliente: {cliente['nome']} ({cliente['numero']})")

    # Fase 1: Sugerir
    print(f"\n1️⃣ Cliente: 'Quero agendar'")
    resposta1 = integrador.sugerir_horarios(cliente["numero"], cliente["imovel"])
    print(f"\n🤖 Bot:\n{resposta1}")

    # Fase 2: Escolher INVÁLIDO
    print(f"\n2️⃣ Cliente: 'Quero a opção 5' (inválida)")
    sucesso, resposta2 = integrador.confirmar_agendamento(
        cliente["numero"],
        "5",
        cliente["imovel"]
    )

    if sucesso:
        print(f"\n🤖 Bot:\n{resposta2}")
    else:
        print(f"\n⚠️ Bot corrigiu:")
        print(f"{resposta2}")

    # Tenta novamente com escolha válida
    print(f"\n3️⃣ Cliente: 'Desculpa, quero a opção 1'")
    sucesso, resposta3 = integrador.confirmar_agendamento(
        cliente["numero"],
        "1",
        cliente["imovel"]
    )

    if sucesso:
        print(f"\n🤖 Bot:\n{resposta3}")
        print(f"\n✅ Agendamento CONFIRMADO (segunda tentativa)")
    else:
        print(f"\n❌ Erro: {resposta3}")

    return sucesso


def exemplo_3_opcoes_expiradas():
    """Exemplo 3: Cliente demora > 1 hora para responder (opções expiram)"""
    print("\n" + "="*80)
    print("📌 EXEMPLO 3: Cliente Ana - Opções Expiradas")
    print("="*80)

    redis = MockRedis()
    integrador = MockIntegradorEscalonamento(redis, {})

    cliente = {
        "numero": "5531989999999",
        "nome": "Ana Costa",
        "imovel": "itatiaiucu-001"
    }

    print(f"\n👤 Cliente: {cliente['nome']} ({cliente['numero']})")

    # Fase 1: Sugerir
    print(f"\n1️⃣ Cliente: 'Quero agendar'")
    resposta1 = integrador.sugerir_horarios(cliente["numero"], cliente["imovel"])
    print(f"\n🤖 Bot:\n{resposta1}")

    # Simula expiração: deleta do Redis
    print(f"\n⏳ [SIMULAÇÃO] Cliente demora 2 horas para responder...")
    redis.delete(f"opcoes_horario:{cliente['numero']}")

    # Fase 2: Tenta escolher depois da expiração
    print(f"\n2️⃣ Cliente: 'Agora quero a opção 3'")
    sucesso, resposta2 = integrador.confirmar_agendamento(
        cliente["numero"],
        "3",
        cliente["imovel"]
    )

    if sucesso:
        print(f"\n🤖 Bot:\n{resposta2}")
    else:
        print(f"\n⚠️ Bot avisa sobre expiração:")
        print(f"{resposta2}")
        print(f"\n💡 Solução: Bot ofereceu agendar novamente")

    # Cliente pede para agendar de novo
    print(f"\n3️⃣ Cliente: 'Tá bom, me mostra os horários de novo'")
    resposta3 = integrador.sugerir_horarios(cliente["numero"], cliente["imovel"])
    print(f"\n🤖 Bot:\n{resposta3}")

    return True  # Teste de fluxo (não falha)


def exemplo_4_multiplos_clientes():
    """Exemplo 4: Múltiplos clientes agendando simultaneamente"""
    print("\n" + "="*80)
    print("📌 EXEMPLO 4: Múltiplos Clientes Simultâneos")
    print("="*80)

    redis = MockRedis()
    integrador = MockIntegradorEscalonamento(redis, {})

    clientes = [
        {"numero": "5531981111111", "nome": "Carlos Silva", "escolha": "1"},
        {"numero": "5531982222222", "nome": "Fernanda Costa", "escolha": "2"},
        {"numero": "5531983333333", "nome": "Roberto Lima", "escolha": "3"},
    ]

    print(f"\n📊 Agendando {len(clientes)} clientes...")

    # Fase 1: Todos pedem para agendar
    for cliente in clientes:
        print(f"\n👤 {cliente['nome']} ({cliente['numero']})")
        resposta = integrador.sugerir_horarios(cliente["numero"])
        print(f"   → Horários sugeridos ✓")

    # Verificar Redis
    print(f"\n📊 Estado do Redis:")
    print(f"   → {len(redis.data)} opções armazenadas")
    for key in redis.data.keys():
        print(f"     • {key}")

    # Fase 2: Todos escolhem
    print(f"\n📋 Confirmar agendamentos:")
    sucesso_count = 0

    for cliente in clientes:
        sucesso, _ = integrador.confirmar_agendamento(
            cliente["numero"],
            cliente["escolha"],
            "itatiaiucu-001"
        )
        status = "✅" if sucesso else "❌"
        print(f"   {status} {cliente['nome']}: opção {cliente['escolha']}")
        if sucesso:
            sucesso_count += 1

    print(f"\n📊 Resultado: {sucesso_count}/{len(clientes)} agendamentos confirmados")
    return sucesso_count == len(clientes)


def exemplo_5_notificacao_completa():
    """Exemplo 5: Mostra a notificação completa formatada"""
    print("\n" + "="*80)
    print("📌 EXEMPLO 5: Notificação Completa para Corretor")
    print("="*80)

    redis = MockRedis()
    config = {
        'google_sheet_id': 'abc123',
        'evolution': {'url': 'mock', 'api_key': 'mock', 'instance': 'mock'}
    }

    cliente = {
        "numero": "5531987654321",
        "nome": "Maria Silva",
        "imovel": "itatiaiucu-001"
    }

    print(f"\n👤 Cliente: {cliente['nome']}")
    print(f"📱 Número: {cliente['numero']}")
    print(f"🏠 Imóvel: Chácara em Itatiaiuçu")

    # Gera notificação
    mensagem = _notificar_corretor_agendamento(
        cliente_numero=cliente["numero"],
        nome_cliente=cliente["nome"],
        imovel_id=cliente["imovel"],
        horario_confirmado="14:30",
        data_formatada="Quarta",
        redis_client=redis,
        config=config
    )

    print(f"\n📱 MENSAGEM PARA CORRETOR (5531980160822):")
    print(f"{'='*80}")
    print(mensagem)
    print(f"{'='*80}")

    return True


def main():
    """Executa todos os exemplos"""
    print("\n" + "🔷"*40)
    print("📚 EXEMPLOS PRÁTICOS - AGENDAMENTO DE VISITA")
    print("🔷"*40)

    exemplos = [
        ("Fluxo Normal", exemplo_1_fluxo_normal),
        ("Escolha Inválida", exemplo_2_escolha_invalida),
        ("Opções Expiradas", exemplo_3_opcoes_expiradas),
        ("Múltiplos Clientes", exemplo_4_multiplos_clientes),
        ("Notificação Completa", exemplo_5_notificacao_completa),
    ]

    resultados = []

    for nome, func in exemplos:
        try:
            resultado = func()
            resultados.append((nome, True))
            print(f"\n✅ {nome}: OK")
        except Exception as e:
            resultados.append((nome, False))
            print(f"\n❌ {nome}: ERRO - {e}")
            import traceback
            traceback.print_exc()

    # Resumo
    print("\n" + "="*80)
    print("📊 RESUMO FINAL")
    print("="*80)

    for nome, ok in resultados:
        status = "✅" if ok else "❌"
        print(f"{status} {nome}")

    total_ok = sum(1 for _, ok in resultados if ok)
    print(f"\n{total_ok}/{len(exemplos)} exemplos executados com sucesso")

    return total_ok == len(exemplos)


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
