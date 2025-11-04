"""
Integrador de Follow-up com Chatbot V4

Conecta sistema de follow-up com callbacks do chatbot.
"""

from datetime import datetime
from typing import Optional, Dict
from .sistema_followup import SistemaFollowUp
from .tipos_abandono import DetectorAbandono


class IntegradorFollowUp:
    """
    Integra sistema de follow-up com chatbot V4.
    """

    def __init__(self):
        self.sistema = SistemaFollowUp()
        self.detector = DetectorAbandono()

    def on_mensagem_bot_enviada(self, cliente_numero: str, mensagem: str):
        """
        Callback: Bot acabou de enviar mensagem.
        Agenda follow-up de inatividade.

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem enviada pelo bot
        """
        # Cancela follow-ups anteriores (cliente estava ativo)
        self.sistema.cancelar_todos(cliente_numero)

        # Agenda novo follow-up de 2h
        self.sistema.agendar(cliente_numero, "inatividade_2h")

        print(f"🔔 Follow-up inatividade_2h agendado para {cliente_numero}")

    def on_mensagem_cliente_recebida(
        self,
        cliente_numero: str,
        mensagem: str
    ):
        """
        Callback: Cliente respondeu.
        Cancela follow-ups de inatividade e registra resposta.

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem recebida do cliente
        """
        # Cliente respondeu → cancela follow-ups
        cancelados = self.sistema.cancelar_todos(cliente_numero)

        if cancelados > 0:
            # Registrar que cliente respondeu
            self.sistema.registrar_resposta(cliente_numero)
            print(f"✅ {cliente_numero} respondeu → {cancelados} follow-ups cancelados")

        # Detectar tipo de abandono para próximos follow-ups
        tipo = self.detector.detectar_tipo(mensagem)
        print(f"🔍 Tipo detectado: {tipo}")

    def on_fotos_enviadas(
        self,
        cliente_numero: str,
        imovel_id: str,
        quantidade: int = 1
    ):
        """
        Callback: Bot enviou fotos.
        Agenda follow-up pós-fotos.

        Args:
            cliente_numero: Número do cliente
            imovel_id: ID do imóvel
            quantidade: Quantidade de fotos enviadas
        """
        # Cancela follow-ups de inatividade anteriores
        self.sistema.cancelar_todos(cliente_numero)

        # Agenda follow-up de 1h
        self.sistema.agendar(cliente_numero, "pos_fotos")

        print(f"📸 Follow-up pós-fotos agendado para {cliente_numero} (imóvel: {imovel_id})")

    def on_visita_agendada(
        self,
        cliente_numero: str,
        data_hora_visita: datetime,
        imovel_id: str
    ):
        """
        Callback: Visita foi agendada.
        Agenda lembretes de visita.

        Args:
            cliente_numero: Número do cliente
            data_hora_visita: Data/hora da visita
            imovel_id: ID do imóvel
        """
        # Cancela follow-ups de inatividade anteriores
        self.sistema.cancelar_todos(cliente_numero)

        # Lembrete 24h antes
        self.sistema.agendar(
            cliente_numero,
            "lembrete_visita_24h",
            dados_contexto={
                "hora": data_hora_visita.strftime("%H:%M"),
                "data_visita": data_hora_visita
            }
        )

        # Lembrete 2h antes
        self.sistema.agendar(
            cliente_numero,
            "lembrete_visita_2h",
            dados_contexto={"data_visita": data_hora_visita}
        )

        print(f"📅 Lembretes de visita agendados para {cliente_numero} ({data_hora_visita.strftime('%d/%m/%Y %H:%M')})")

    def on_visita_realizada(
        self,
        cliente_numero: str,
        data_hora_visita: datetime,
        imovel_id: str
    ):
        """
        Callback: Visita foi realizada.
        Agenda follow-up pós-visita.

        Args:
            cliente_numero: Número do cliente
            data_hora_visita: Data/hora da visita realizada
            imovel_id: ID do imóvel
        """
        # Follow-up pós-visita (4h depois da visita)
        # Calcula timestamp 4h após a visita
        timestamp_visita = data_hora_visita.timestamp()

        self.sistema.agendar(
            cliente_numero,
            "pos_visita"
        )

        print(f"🏠 Follow-up pós-visita agendado para {cliente_numero} (imóvel: {imovel_id})")

    def on_abandono_detectado(
        self,
        cliente_numero: str,
        ultima_mensagem: Optional[str] = None,
        contexto: Optional[Dict] = None
    ):
        """
        Callback: Abandono detectado (cliente sumiu).
        Agenda follow-up personalizado baseado no tipo de abandono.

        Args:
            cliente_numero: Número do cliente
            ultima_mensagem: Última mensagem do cliente
            contexto: Dados adicionais (ex: região preferida)
        """
        # Detectar tipo de abandono
        tipo = self.detector.detectar_tipo(ultima_mensagem)

        # Escolher follow-up adequado
        escolha = self.detector.escolher_followup(tipo)

        # Agendar follow-up
        self.sistema.agendar(
            cliente_numero,
            escolha["trigger"],
            dados_contexto=contexto
        )

        print(f"⚠️ Abandono detectado: {cliente_numero} (tipo: {tipo}) → {escolha['trigger']}")

    def resetar_tentativas(self, cliente_numero: str):
        """
        Reseta contador de tentativas de follow-up.
        Útil quando cliente retoma contato ativamente.

        Args:
            cliente_numero: Número do cliente
        """
        tipos = ["inatividade", "pos_interacao", "lembrete"]

        for tipo in tipos:
            key = f"followup_count:{cliente_numero}:{tipo}"
            self.sistema.redis_client.delete(key)

        print(f"🔄 Tentativas resetadas para {cliente_numero}")

    def obter_historico(self, cliente_numero: str, limite: int = 10) -> list:
        """
        Obtém histórico de follow-ups do cliente.

        Args:
            cliente_numero: Número do cliente
            limite: Quantidade máxima de registros

        Returns:
            Lista de follow-ups históricos
        """
        import json

        historico_key = f"followup_history:{cliente_numero}"
        historico_json = self.sistema.redis_client.lrange(historico_key, 0, limite - 1)

        historico = []
        for item_json in historico_json:
            item = json.loads(item_json)
            item["timestamp_formatado"] = datetime.fromtimestamp(
                item["timestamp"]
            ).strftime("%d/%m/%Y %H:%M")
            historico.append(item)

        return historico
