"""
Notificação de Corretores
Alertas via WhatsApp quando há escalonamento
"""

import requests
from upstash_redis import Redis
from typing import Dict, Optional


class NotificadorCorretor:
    """Notifica corretores sobre novos atendimentos"""

    # Corretor LF Imóveis
    CORRETORES = [
        {
            "id": 1,
            "nome": "Luciano",
            "whatsapp": "5531980160822",
            "chatwoot_id": 1
        }
    ]

    def __init__(self, config: Optional[Dict] = None):
        """
        Args:
            config: Config completo (opcional, para redis se necessário)
        """
        # Redis pode ser injetado posteriormente
        self.redis_client = None
        self.config = config

    def buscar_corretor_disponivel(self) -> Dict:
        """
        Busca próximo corretor disponível (round-robin)

        Returns:
            Dict com dados do corretor
        """
        try:
            # Se redis não disponível, retorna primeiro corretor
            if not self.redis_client:
                print(f"⚠️ Redis não disponível, usando primeiro corretor")
                return self.CORRETORES[0]

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

        # Envia via Evolution API
        try:
            # Importa configuração do Evolution API
            import json
            import os

            config_path = os.path.join(
                os.path.dirname(__file__),
                "../../chatwoot_config_lfimoveis.json"
            )

            with open(config_path, 'r') as f:
                config = json.load(f)

            evolution_url = config['evolution']['url']
            evolution_instance = config['evolution']['instance']
            evolution_api_key = config['evolution']['api_key']

            # Monta payload para Evolution API
            payload = {
                "number": corretor["whatsapp"],
                "text": mensagem
            }

            headers = {
                "apikey": evolution_api_key,
                "Content-Type": "application/json"
            }

            url = f"{evolution_url}/message/sendText/{evolution_instance}"

            resultado = requests.post(url, headers=headers, json=payload, timeout=10)

            if resultado.status_code in [200, 201]:
                print(f"✅ Notificação enviada para {corretor['nome']}")
                return True
            else:
                print(f"⚠️ Falha ao enviar notificação: {resultado.status_code}")
                return False

        except FileNotFoundError:
            print(f"❌ Arquivo de config não encontrado")
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
            if not self.redis_client:
                print(f"⚠️ Redis não disponível, atribuição não registrada")
                return

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
