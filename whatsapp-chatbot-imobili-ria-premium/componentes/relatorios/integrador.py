"""
Integrador de métricas no chatbot
Conecta eventos do chatbot com coleta de métricas
"""

import sys

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')

from componentes.relatorios.metricas import ColetorMetricas


class IntegradorMetricas:
    """
    Integra coleta de métricas no chatbot
    Oferece callbacks para eventos do chatbot
    """

    def __init__(self, redis_client=None):
        """
        Inicializa integrador

        Args:
            redis_client: Cliente Redis (compatibilidade)
        """
        self.redis = redis_client
        self.coletor = ColetorMetricas()

    def on_nova_conversa(self, cliente_numero: str) -> None:
        """
        Callback: nova conversa iniciada

        Args:
            cliente_numero: Número do cliente
        """
        self.coletor.incrementar("leads_total")
        self.coletor.incrementar("leads_novos_hoje")

    def on_bot_respondeu(self, cliente_numero: str) -> None:
        """
        Callback: bot respondeu mensagem

        Args:
            cliente_numero: Número do cliente
        """
        self.coletor.incrementar("bot_atendeu")

    def on_escalamento(self, cliente_numero: str) -> None:
        """
        Callback: conversa escalada para humano

        Args:
            cliente_numero: Número do cliente
        """
        self.coletor.incrementar("escaladas")

    def on_lead_quente(self, cliente_numero: str, score: int) -> None:
        """
        Callback: lead ficou quente (score >= 70)

        Args:
            cliente_numero: Número do cliente
            score: Score atual do lead
        """
        if score >= 70:
            self.coletor.adicionar_lista("leads_quentes", cliente_numero)

    def on_visita_agendada(self, cliente_numero: str, imovel_id: str) -> None:
        """
        Callback: visita agendada

        Args:
            cliente_numero: Número do cliente
            imovel_id: ID do imóvel
        """
        self.coletor.incrementar("visitas_agendadas")
        self.coletor.incrementar_sorted_set("imoveis_mais_procurados", imovel_id)

    def on_proposta_enviada(self, cliente_numero: str) -> None:
        """
        Callback: proposta enviada

        Args:
            cliente_numero: Número do cliente
        """
        self.coletor.incrementar("propostas_enviadas")

    def on_followup_enviado(self, cliente_numero: str) -> None:
        """
        Callback: follow-up enviado

        Args:
            cliente_numero: Número do cliente
        """
        self.coletor.incrementar("followups_enviados")

    def on_followup_respondido(self, cliente_numero: str) -> None:
        """
        Callback: cliente respondeu follow-up

        Args:
            cliente_numero: Número do cliente
        """
        self.coletor.incrementar("followups_respondidos")

    def on_imovel_visualizado(self, cliente_numero: str, imovel_id: str) -> None:
        """
        Callback: cliente visualizou imóvel

        Args:
            cliente_numero: Número do cliente
            imovel_id: ID do imóvel
        """
        self.coletor.incrementar_sorted_set("imoveis_mais_procurados", imovel_id)

    def registrar_evento_customizado(self, nome_metrica: str, valor: int = 1) -> None:
        """
        Registra evento customizado

        Args:
            nome_metrica: Nome da métrica customizada
            valor: Valor a incrementar
        """
        self.coletor.incrementar(nome_metrica, valor)
