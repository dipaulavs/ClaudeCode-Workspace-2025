#!/usr/bin/env python3
"""
📊 EXEMPLO: Como Integrar Métricas no Chatbot

Copie este código para seu chatbot_*.py principal
"""

from componentes.relatorios.dashboard_visual import ColetorMetricasChatbot
import time


# ==============================================================================
# NO INÍCIO DO SEU CHATBOT
# ==============================================================================

def inicializar_chatbot():
    """Exemplo de inicialização"""

    # ... suas configurações existentes ...
    redis = None  # seu cliente Redis

    # ✅ ADICIONAR: Inicializar coletor de métricas
    coletor_metricas = ColetorMetricasChatbot(redis)

    return coletor_metricas


# ==============================================================================
# DURANTE O ATENDIMENTO
# ==============================================================================

def processar_mensagem(numero_cliente, mensagem, coletor_metricas):
    """Exemplo de processamento com métricas"""

    # ✅ ADICIONAR: Registrar atendimento
    inicio = time.time()
    coletor_metricas.registrar_atendimento(numero_cliente)

    # ... seu código existente ...

    # Se é novo cliente
    # ✅ ADICIONAR:
    # coletor_metricas.registrar_lead_novo(numero_cliente)

    # ... processamento da mensagem ...

    # Se chamou ferramenta LOCAL
    # ✅ ADICIONAR:
    # coletor_metricas.registrar_ferramenta_local()

    # Se chamou ferramenta MCP
    # ✅ ADICIONAR:
    # coletor_metricas.registrar_ferramenta_mcp()

    # Se MCP deu erro
    # ✅ ADICIONAR:
    # coletor_metricas.registrar_erro_mcp()

    # Se bot respondeu (sem escalação)
    # ✅ ADICIONAR:
    # coletor_metricas.registrar_bot_respondeu()

    # Se escalou para humano
    # ✅ ADICIONAR:
    # coletor_metricas.registrar_escalada_humano()

    # ... resto do código ...

    # ✅ ADICIONAR: Registrar tempo de resposta
    fim = time.time()
    tempo_ms = int((fim - inicio) * 1000)
    coletor_metricas.registrar_tempo_resposta(tempo_ms)


# ==============================================================================
# QUANDO CRIA TAGS
# ==============================================================================

def criar_tag_interesse(numero_cliente, item_id, coletor_metricas):
    """Exemplo ao criar tag de interesse"""

    # ... seu código de tagueamento existente ...

    # ✅ ADICIONAR:
    coletor_metricas.registrar_tag_criada("interesse")


def escalonar_para_humano(numero_cliente, coletor_metricas):
    """Exemplo ao escalonar"""

    # ... seu código de escalonamento ...

    # ✅ ADICIONAR:
    coletor_metricas.registrar_tag_criada("frustrado")
    coletor_metricas.registrar_escalada_humano()


def agendar_visita(numero_cliente, coletor_metricas):
    """Exemplo ao agendar visita"""

    # ... seu código de agendamento ...

    # ✅ ADICIONAR:
    coletor_metricas.registrar_visita_agendada()
    coletor_metricas.registrar_tag_criada("visita")


def enviar_proposta(numero_cliente, coletor_metricas):
    """Exemplo ao enviar proposta"""

    # ... seu código de proposta ...

    # ✅ ADICIONAR:
    coletor_metricas.registrar_proposta_enviada()


# ==============================================================================
# MONITORAMENTO DE SCORE
# ==============================================================================

def atualizar_score(numero_cliente, score, redis, coletor_metricas):
    """Exemplo ao atualizar score"""

    # ... seu código de score ...

    # ✅ ADICIONAR: Se virou lead quente
    if score >= 70:
        coletor_metricas.registrar_lead_quente(numero_cliente)


# ==============================================================================
# EXEMPLO COMPLETO INTEGRADO
# ==============================================================================

def exemplo_chatbot_completo():
    """Exemplo de chatbot COM métricas integradas"""

    # Inicialização
    redis = None  # seu Redis
    coletor = ColetorMetricasChatbot(redis)

    # Simulação de atendimento
    numero = "5531999999999"

    # 1. Cliente envia mensagem
    inicio = time.time()
    coletor.registrar_atendimento(numero)

    # 2. Verifica se é novo lead
    # if novo_cliente:
    coletor.registrar_lead_novo(numero)

    # 3. Bot processa
    # ... lógica do bot ...

    # 4. Usa ferramenta LOCAL
    coletor.registrar_ferramenta_local()

    # 5. Cliente demonstra interesse
    coletor.registrar_tag_criada("interesse")

    # 6. Cliente agenda visita
    coletor.registrar_visita_agendada()
    coletor.registrar_tag_criada("visita")

    # 7. Bot respondeu sem escalação
    coletor.registrar_bot_respondeu()

    # 8. Registra tempo
    fim = time.time()
    coletor.registrar_tempo_resposta(int((fim - inicio) * 1000))

    # 9. Score virou 80 (quente)
    # coletor.registrar_lead_quente(numero)

    print("✅ Métricas registradas!")


if __name__ == "__main__":
    print("📊 Exemplo de Integração de Métricas\n")
    print("Este arquivo é apenas referência.")
    print("Copie o código para seu chatbot_*.py principal.\n")
    print("Veja os comentários '✅ ADICIONAR' em cada função.\n")
