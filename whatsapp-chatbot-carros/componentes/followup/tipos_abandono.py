"""
Detector de Tipos de Abandono

Detecta o tipo de abandono para personalizar o follow-up adequado.
"""

from typing import Optional, Dict


TIPOS_ABANDONO = {
    "curioso": {
        "sinais": [
            "só olhando", "so olhando", "to olhando", "vendo opções", "pesquisando",
            "to dando uma olhada", "vou dar uma olhada",
            "quero ver", "deixa eu ver opções"
        ],
        "followup": "inatividade_24h",
        "mensagem_personalizada": "Oi! Encontrei mais opções que podem te interessar. Quer dar uma olhada? 😊"
    },

    "preguicoso": {
        "sinais": [
            "depois eu vejo", "vou pensar", "deixa eu ver",
            "mais tarde", "amanhã eu vejo", "vou analisar",
            "preciso pensar", "vou considerar"
        ],
        "followup": "inatividade_2h",
        "mensagem_personalizada": "Ei! Lembrou de dar uma olhada? 😊"
    },

    "indeciso": {
        "sinais": [
            "não sei", "talvez", "vou pensar",
            "tenho dúvidas", "to em dúvida", "não tenho certeza",
            "preciso decidir", "difícil escolher"
        ],
        "followup": "pos_fotos",
        "mensagem_personalizada": "Olha, mandei umas fotos extras que podem te ajudar a decidir! 📸"
    },

    "interessado": {
        "sinais": [
            "interessante", "gostei", "parece bom",
            "pode ser", "vou conferir", "quero saber mais",
            "me manda", "tem mais"
        ],
        "followup": "inatividade_2h",
        "mensagem_personalizada": "E aí, quer mais detalhes? 😊"
    },

    "negociador": {
        "sinais": [
            "desconto", "negociar", "muito caro",
            "preço alto", "valor salgado", "tem como baixar",
            "posso pagar menos", "aceita oferta"
        ],
        "followup": "inatividade_2h",
        "mensagem_personalizada": "Oi! Vamos conversar sobre aquele imóvel? Posso te ajudar 😊"
    },

    "sumiu": {
        "sinais": [],  # Sem mensagem, só parou de responder
        "followup": "inatividade_2h",
        "mensagem_personalizada": "E aí, ficou alguma dúvida? 😊"
    }
}


class DetectorAbandono:
    """
    Detecta tipo de abandono para personalizar follow-up.
    """

    def detectar_tipo(self, ultima_mensagem_cliente: Optional[str] = None) -> str:
        """
        Detecta tipo de abandono baseado na última mensagem do cliente.

        Args:
            ultima_mensagem_cliente: Última mensagem enviada pelo cliente

        Returns:
            Tipo de abandono (ex: "curioso", "preguicoso", "sumiu")
        """
        if not ultima_mensagem_cliente:
            return "sumiu"

        mensagem_lower = ultima_mensagem_cliente.lower()

        # Verificar cada tipo
        for tipo, config in TIPOS_ABANDONO.items():
            if tipo == "sumiu":  # Pular tipo padrão
                continue

            for sinal in config["sinais"]:
                if sinal in mensagem_lower:
                    return tipo

        # Padrão se não encontrou nenhum sinal
        return "sumiu"

    def escolher_followup(self, tipo: str) -> Dict[str, str]:
        """
        Escolhe trigger e mensagem adequados para o tipo de abandono.

        Args:
            tipo: Tipo de abandono

        Returns:
            Dict com "trigger" e "mensagem"
        """
        if tipo not in TIPOS_ABANDONO:
            tipo = "sumiu"

        config = TIPOS_ABANDONO[tipo]

        return {
            "trigger": config["followup"],
            "mensagem": config["mensagem_personalizada"]
        }

    def listar_tipos(self) -> Dict[str, Dict]:
        """
        Lista todos os tipos de abandono disponíveis.

        Returns:
            Dict com configuração de cada tipo
        """
        return TIPOS_ABANDONO
