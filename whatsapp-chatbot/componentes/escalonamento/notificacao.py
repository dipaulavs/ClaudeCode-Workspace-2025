"""
Notificação de Corretores
Alertas via WhatsApp quando há escalonamento
"""

import requests
from upstash_redis import Redis
from typing import Dict, Optional
from config.config import REDIS_URL, REDIS_TOKEN


class NotificadorCorretor:
    """Notifica corretores sobre novos atendimentos"""

    # Corretores disponíveis (em produção, vir de banco de dados)
    CORRETORES = [
        {
            "id": 1,
            "nome": "Bruno",
            "whatsapp": "5531999999999",  # Substituir por número real
            "chatwoot_id": 1
        },
        {
            "id": 2,
            "nome": "Fernanda",
            "whatsapp": "5531888888888",  # Substituir por número real
            "chatwoot_id": 2
        }
    ]

    def __init__(self):
        self.redis_client = Redis(
            url=REDIS_URL,
            token=REDIS_TOKEN
        )

    def buscar_corretor_disponivel(self) -> Dict:
        """
        Busca próximo corretor disponível (round-robin)

        Returns:
            Dict com dados do corretor
        """
        try:
            # Round-robin simples
            ultimo_atribuido = self.redis_client.get("ultimo_corretor_atribuido")

            if ultimo_atribuido is None:
                proximo = 0
            else:
                proximo = (int(ultimo_atribuido) + 1) % len(self.CORRETORES)

            # Atualiza Redis
            self.redis_client.set("ultimo_corretor_atribuido", proximo)

            corretor = self.CORRETORES[proximo]
            print(f"✅ Corretor selecionado: {corretor['nome']}")

            return corretor

        except Exception as e:
            print(f"⚠️ Erro ao buscar corretor, usando padrão: {e}")
            # Fallback: primeiro corretor
            return self.CORRETORES[0]

    def notificar_whatsapp(
        self,
        corretor: Dict,
        cliente_numero: str,
        trigger: str,
        score: int,
        conv_id: int,
        link_conversa: str
    ) -> bool:
        """
        Envia notificação via WhatsApp para corretor

        Args:
            corretor: Dict com dados do corretor
            cliente_numero: Número do cliente
            trigger: Trigger que causou escalonamento
            score: Score do lead
            conv_id: ID da conversa no Chatwoot
            link_conversa: Link direto pra conversa

        Returns:
            True se enviado
        """
        # Emoji baseado no score
        emoji_score = "🔥" if score >= 70 else "🌡️" if score >= 40 else "❄️"

        # Tradução dos triggers
        trigger_msgs = {
            "cliente_pede_humano": "Cliente pediu atendimento humano",
            "frustrado": "Cliente frustrado com bot",
            "quer_visitar": "Cliente quer agendar visita",
            "quer_proposta": "Cliente quer proposta/fechar",
            "lead_quente": "Lead quente (score alto)"
        }

        trigger_msg = trigger_msgs.get(trigger, trigger)

        mensagem = f"""
🔔 *NOVO ATENDIMENTO*

*Cliente:* {cliente_numero}
*Motivo:* {trigger_msg}
*Score:* {score} {emoji_score}
*Conversa:* #{conv_id}

{link_conversa}
        """.strip()

        # Envia via Evolution API (usando script existente)
        try:
            from tools.send_message_evolution import enviar_mensagem

            resultado = enviar_mensagem(
                numero_destino=corretor["whatsapp"],
                mensagem=mensagem
            )

            if resultado:
                print(f"✅ Notificação enviada para {corretor['nome']}")
                return True
            else:
                print(f"⚠️ Falha ao enviar notificação para {corretor['nome']}")
                return False

        except Exception as e:
            print(f"❌ Erro ao enviar notificação: {e}")
            return False

    def registrar_atribuicao(
        self,
        corretor: Dict,
        cliente_numero: str,
        trigger: str
    ):
        """
        Registra atribuição no Redis (para estatísticas)

        Args:
            corretor: Dict do corretor
            cliente_numero: Número do cliente
            trigger: Trigger
        """
        try:
            key = f"atribuicao:{cliente_numero}"

            dados = {
                "corretor_id": corretor["id"],
                "corretor_nome": corretor["nome"],
                "trigger": trigger,
                "timestamp": self._get_timestamp()
            }

            self.redis_client.setex(
                key,
                86400 * 7,  # 7 dias
                str(dados)
            )

        except Exception as e:
            print(f"⚠️ Erro ao registrar atribuição: {e}")

    def _get_timestamp(self) -> str:
        """Retorna timestamp formatado"""
        from datetime import datetime
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
