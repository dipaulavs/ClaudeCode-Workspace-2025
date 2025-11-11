"""
Detector de Triggers de Escalonamento
Identifica quando transferir atendimento para humano
"""

import re
from typing import Optional, Dict, Tuple


class DetectorEscalonamento:
    """Detecta gatilhos para escalonar conversa para corretor humano"""

    TRIGGERS = {
        # Explícito - Cliente pede humano
        "cliente_pede_humano": {
            "keywords": [
                "falar com humano", "quero falar", "atendente", "corretor",
                "pessoa de verdade", "alguém real", "falar com alguém",
                "atendimento humano", "preciso falar"
            ],
            "prioridade": "alta",
            "score_minimo": 0,  # Sempre escala
            "mensagem": "Vou chamar um corretor agora mesmo! 👍"
        },

        # Frustração - Cliente insatisfeito com bot
        "frustrado": {
            "keywords": [
                "não entendi", "não respondeu", "não está funcionando",
                "ruim", "péssimo", "horrível", "que merda", "não ajudou",
                "não resolve", "burro", "idiota", "inútil"
            ],
            "prioridade": "alta",
            "score_minimo": 0,  # Sempre escala
            "mensagem": "Desculpa! Vou chamar um corretor pra te ajudar melhor 🙏"
        },

        # Interesse alto - Quer visitar
        "quer_visitar": {
            "keywords": [
                "visitar", "conhecer", "ver pessoalmente", "ir ver",
                "agendar visita", "marcar visita", "quero ver",
                "posso visitar", "visita agendada", "quando posso ir"
            ],
            "prioridade": "alta",
            "score_minimo": 40,  # Só escala se minimamente qualificado
            "mensagem": "Opa! Vou chamar o Bruno pra agendar sua visita! 📅"
        },

        # Interesse alto - Quer proposta/fechar
        "quer_proposta": {
            "keywords": [
                "proposta", "contrato", "fechar", "documentação",
                "documentos", "assinar", "quero alugar", "quero comprar",
                "como faço para", "próximos passos", "processo"
            ],
            "prioridade": "alta",
            "score_minimo": 60,
            "mensagem": "Ótimo! Vou chamar o Bruno pra fazer sua proposta! 📝"
        },

        # Score alto - Lead quente automático
        "lead_quente": {
            "keywords": [],  # Sem keywords, só score
            "prioridade": "media",
            "score_minimo": 80,  # Score ≥80 → escala automaticamente
            "auto": True,
            "mensagem": "Vejo que você está bem interessado! Vou chamar o Bruno pra conversar com você 🔥"
        }
    }

    def detectar_trigger(self, mensagem: str, score: int) -> Optional[str]:
        """
        Detecta se mensagem contém trigger de escalonamento

        Args:
            mensagem: Mensagem do cliente
            score: Score de qualificação atual

        Returns:
            Nome do trigger ou None
        """
        mensagem_lower = mensagem.lower()

        # Verifica triggers por ordem de prioridade
        for trigger_nome, config in self.TRIGGERS.items():
            # Trigger automático por score
            if config.get("auto", False):
                if score >= config["score_minimo"]:
                    return trigger_nome
                continue

            # Trigger por keywords
            if config["keywords"]:
                for keyword in config["keywords"]:
                    if keyword in mensagem_lower:
                        # Verifica score mínimo
                        if score >= config["score_minimo"]:
                            return trigger_nome
                        # Se score muito baixo, não escala (exceto alta prioridade)
                        elif config["prioridade"] == "alta":
                            return trigger_nome

        return None

    def deve_escalonar(self, mensagem: str, score: int) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Verifica se deve escalonar e retorna motivo

        Args:
            mensagem: Mensagem do cliente
            score: Score atual

        Returns:
            (deve_escalonar, trigger, motivo)
        """
        trigger = self.detectar_trigger(mensagem, score)

        if not trigger:
            return False, None, None

        config = self.TRIGGERS[trigger]

        motivo = f"Trigger: {trigger} | Score: {score} | Prioridade: {config['prioridade']}"

        return True, trigger, motivo

    def get_mensagem_escalonamento(self, trigger: str) -> str:
        """Retorna mensagem apropriada para o trigger"""
        return self.TRIGGERS.get(trigger, {}).get("mensagem", "Vou chamar um corretor pra você! 👍")

    def get_prioridade(self, trigger: str) -> str:
        """Retorna prioridade do trigger"""
        return self.TRIGGERS.get(trigger, {}).get("prioridade", "media")
