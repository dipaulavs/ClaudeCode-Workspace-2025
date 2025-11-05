"""
Sistema de Follow-ups

Gerencia agendamento, processamento e envio de follow-ups automáticos.
"""

import json
import time
import uuid
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import redis

# Configurações
REDIS_HOST = "usw1-popular-stallion-42128.upstash.io"
REDIS_PORT = 42128
REDIS_PASSWORD = "AaEoAAIjcDFiODk5OWQ5ZjdiOTY0NmM4OWNkZTI2YzI3NTU3NGI5YnAxMA"

EVOLUTION_URL = "https://megatalk.com.br"
EVOLUTION_INSTANCE = "lfimoveis"
EVOLUTION_API_KEY = "6C60BE7E-A2D7-4EF3-8BA4-E4C050"

# Configuração de triggers
TRIGGERS = {
    # Inatividade
    "inatividade_2h": {
        "delay": 7200,  # 2h em segundos
        "mensagem": "E aí, ficou alguma dúvida? 😊",
        "max_tentativas": 1,
        "tipo": "inatividade"
    },

    "inatividade_24h": {
        "delay": 86400,  # 24h
        "mensagem": "Oi! Ainda tá procurando imóvel? Posso ajudar!",
        "max_tentativas": 1,
        "tipo": "inatividade"
    },

    "inatividade_48h": {
        "delay": 172800,  # 48h
        "mensagem": "Oi! Achei mais opções na {regiao}. Quer ver?",
        "max_tentativas": 1,
        "tipo": "inatividade",
        "precisa_contexto": True
    },

    # Pós-interação
    "pos_fotos": {
        "delay": 3600,  # 1h
        "mensagem": "Gostou das fotos? Quer agendar visita? 📅",
        "max_tentativas": 1,
        "tipo": "pos_interacao"
    },

    "pos_visita": {
        "delay": 14400,  # 4h
        "mensagem": "E aí, gostou do imóvel? 😊",
        "max_tentativas": 1,
        "tipo": "pos_interacao"
    },

    # Lembretes (tempo NEGATIVO = antes do evento)
    "lembrete_visita_24h": {
        "delay": -86400,  # 24h ANTES
        "mensagem": "Amanhã às {hora} é sua visita! Confirma? 📅",
        "tipo": "lembrete",
        "precisa_contexto": True
    },

    "lembrete_visita_2h": {
        "delay": -7200,  # 2h ANTES
        "mensagem": "Daqui 2h é sua visita! Já estamos a caminho ✅",
        "tipo": "lembrete"
    }
}


class SistemaFollowUp:
    """
    Sistema de agendamento e processamento de follow-ups.
    """

    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True,
            ssl=True
        )

    def agendar(
        self,
        cliente_numero: str,
        trigger: str,
        dados_contexto: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Agenda um follow-up.

        Args:
            cliente_numero: Número do cliente (formato: 5531980160822)
            trigger: Nome do trigger (ex: "inatividade_2h")
            dados_contexto: Dados adicionais (ex: região, hora da visita)

        Returns:
            ID do follow-up ou None se não agendado
        """
        if trigger not in TRIGGERS:
            print(f"❌ Trigger inválido: {trigger}")
            return None

        config = TRIGGERS[trigger]

        # Verificar se já atingiu max tentativas
        tentativas_key = f"followup_count:{cliente_numero}:{config['tipo']}"
        tentativas = int(self.redis_client.get(tentativas_key) or 0)

        max_tentativas = config.get("max_tentativas", 3)
        if tentativas >= max_tentativas:
            print(f"⚠️ Max tentativas atingidas para {cliente_numero} ({trigger})")
            return None

        # Calcular timestamp de execução
        if config["tipo"] == "lembrete" and dados_contexto and "data_visita" in dados_contexto:
            # Para lembretes, usar data da visita como referência
            data_visita = dados_contexto["data_visita"]
            if isinstance(data_visita, str):
                data_visita = datetime.fromisoformat(data_visita)
            timestamp_execucao = data_visita.timestamp() + config["delay"]
        else:
            timestamp_execucao = time.time() + config["delay"]

        # Verificar se já passou (lembretes)
        if timestamp_execucao < time.time():
            print(f"⚠️ Timestamp já passou para {trigger}")
            return None

        # Preparar mensagem
        mensagem = config["mensagem"]
        if config.get("precisa_contexto") and dados_contexto:
            mensagem = mensagem.format(**dados_contexto)

        # Criar follow-up
        followup_id = f"fu_{uuid.uuid4().hex[:8]}"
        followup_data = {
            "id": followup_id,
            "cliente": cliente_numero,
            "trigger": trigger,
            "tipo": config["tipo"],
            "mensagem": mensagem,
            "tentativa": tentativas + 1,
            "criado_em": time.time()
        }

        # Adicionar ao sorted set (score = timestamp de execução)
        self.redis_client.zadd(
            "followups",
            {json.dumps(followup_data): timestamp_execucao}
        )

        print(f"✅ Follow-up agendado: {followup_id} ({trigger}) para {datetime.fromtimestamp(timestamp_execucao).strftime('%d/%m/%Y %H:%M')}")

        return followup_id

    def cancelar(self, followup_id: str) -> bool:
        """
        Cancela um follow-up específico.

        Args:
            followup_id: ID do follow-up

        Returns:
            True se cancelado com sucesso
        """
        # Buscar no sorted set
        followups = self.redis_client.zrange("followups", 0, -1)

        for followup_json in followups:
            followup = json.loads(followup_json)
            if followup["id"] == followup_id:
                self.redis_client.zrem("followups", followup_json)
                print(f"✅ Follow-up cancelado: {followup_id}")
                return True

        return False

    def cancelar_todos(self, cliente_numero: str) -> int:
        """
        Cancela todos os follow-ups de um cliente.

        Args:
            cliente_numero: Número do cliente

        Returns:
            Quantidade de follow-ups cancelados
        """
        followups = self.redis_client.zrange("followups", 0, -1)
        cancelados = 0

        for followup_json in followups:
            followup = json.loads(followup_json)
            if followup["cliente"] == cliente_numero:
                self.redis_client.zrem("followups", followup_json)
                cancelados += 1

        if cancelados > 0:
            print(f"✅ {cancelados} follow-ups cancelados para {cliente_numero}")

        return cancelados

    def processar_pendentes(self) -> int:
        """
        Processa follow-ups pendentes (timestamp <= agora).

        Returns:
            Quantidade de follow-ups enviados
        """
        timestamp_atual = time.time()

        # Buscar follow-ups vencidos
        followups_vencidos = self.redis_client.zrangebyscore(
            "followups",
            "-inf",
            timestamp_atual
        )

        enviados = 0

        for followup_json in followups_vencidos:
            followup = json.loads(followup_json)

            # Enviar mensagem
            sucesso = self._enviar_followup(
                followup["cliente"],
                followup["mensagem"]
            )

            if sucesso:
                # Registrar envio
                self.registrar_envio(
                    followup["cliente"],
                    followup["trigger"],
                    followup["tipo"]
                )

                # Remover da fila
                self.redis_client.zrem("followups", followup_json)

                # Incrementar métricas
                self._incrementar_metricas(followup["trigger"], "enviados")

                enviados += 1
                print(f"✅ Follow-up enviado: {followup['id']} → {followup['cliente']}")
            else:
                print(f"❌ Erro ao enviar follow-up: {followup['id']}")

        return enviados

    def registrar_envio(self, cliente_numero: str, trigger: str, tipo: str):
        """
        Registra envio de follow-up (para controle de tentativas).

        Args:
            cliente_numero: Número do cliente
            trigger: Nome do trigger
            tipo: Tipo do follow-up (inatividade, pos_interacao, lembrete)
        """
        # Incrementar contador de tentativas
        tentativas_key = f"followup_count:{cliente_numero}:{tipo}"
        self.redis_client.incr(tentativas_key)

        # Expirar após 30 dias
        self.redis_client.expire(tentativas_key, 2592000)

        # Adicionar ao histórico
        historico_key = f"followup_history:{cliente_numero}"
        historico_imóvel = {
            "timestamp": time.time(),
            "trigger": trigger,
            "tipo": tipo,
            "enviado": True,
            "respondeu": False  # Será atualizado quando cliente responder
        }

        self.redis_client.lpush(historico_key, json.dumps(historico_imóvel))
        self.redis_client.ltrim(historico_key, 0, 99)  # Manter últimos 100

    def registrar_resposta(self, cliente_numero: str):
        """
        Registra que cliente respondeu após follow-up.

        Args:
            cliente_numero: Número do cliente
        """
        historico_key = f"followup_history:{cliente_numero}"

        # Buscar último follow-up enviado
        historico = self.redis_client.lrange(historico_key, 0, 0)

        if historico:
            ultimo_imóvel = json.loads(historico[0])
            ultimo_imóvel["respondeu"] = True

            # Atualizar
            self.redis_client.lset(historico_key, 0, json.dumps(ultimo_imóvel))

            # Incrementar métricas
            self._incrementar_metricas(ultimo_imóvel["trigger"], "respondidos")

            print(f"✅ Resposta registrada: {cliente_numero} → {ultimo_imóvel['trigger']}")

    def _enviar_followup(self, cliente_numero: str, mensagem: str) -> bool:
        """
        Envia mensagem de follow-up via Evolution API.

        Args:
            cliente_numero: Número do cliente
            mensagem: Texto da mensagem

        Returns:
            True se enviado com sucesso
        """
        url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"

        headers = {
            "apikey": EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "number": cliente_numero,
            "text": mensagem
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            return response.status_code == 201
        except Exception as e:
            print(f"❌ Erro ao enviar follow-up: {e}")
            return False

    def _incrementar_metricas(self, trigger: str, tipo: str):
        """
        Incrementa métricas de follow-up.

        Args:
            trigger: Nome do trigger
            tipo: "enviados" ou "respondidos"
        """
        # Métricas gerais
        self.redis_client.incr(f"metricas:followup:total_{tipo}")

        # Métricas por trigger
        self.redis_client.incr(f"metricas:followup:{trigger}:{tipo}")
