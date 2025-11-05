"""
Sistema de Score para qualificação de leads
Pontua clientes de 0-100 baseado em informações, comportamento e urgência
"""
import json
import time
import redis
from typing import Dict, Any, Optional
import re

class SistemaScore:
    """
    Sistema de pontuação de leads (0-100)

    Categorias:
    - Informações fornecidas (max 40): tipo, região, orçamento
    - Comportamento (max 40): rapidez, fotos, perguntas, prazo
    - Urgência (max 20): urgente, esta semana, este mês
    """

    # Pesos de pontuação
    PESOS = {
        # Informações fornecidas (max 40)
        "tipo_definido": 10,          # "apartamento" ou "casa"
        "regiao_definida": 10,         # "savassi", "lourdes"
        "orcamento_definido": 20,      # "até 2000"

        # Comportamento (max 40)
        "resposta_rapida": 10,         # < 2min entre mensagens
        "pediu_fotos": 10,             # "foto", "imagem"
        "fez_perguntas": 10,           # mensagens com "?"
        "mencionou_prazo": 10,         # "quando", "prazo"

        # Urgência (max 20)
        "urgente": 20,                 # "urgente", "hoje"
        "esta_semana": 15,             # "essa semana", "amanhã"
        "este_mes": 10,                # "esse mês"
        "proximo_mes": 5               # "mês que vem"
    }

    # Palavras-chave para detecção
    KEYWORDS = {
        "tipo": ["apartamento", "apto", "ap", "casa", "kitnet", "studio", "flat"],
        "regiao": ["savassi", "lourdes", "funcionarios", "funcionários", "santa tereza",
                   "centro", "cruzeiro", "serra", "mangabeiras"],
        "orcamento": [r"r\$\s*\d+", r"\d+\s*reais", "até", "no máximo", "orçamento"],
        "fotos": ["foto", "imagem", "imagens", "fotos", "ver", "mostrar"],
        "pergunta": [r"\?"],
        "prazo": ["quando", "prazo", "disponível", "disponivel"],
        "urgente": ["urgente", "hoje", "agora", "rápido", "rapido", "imediato"],
        "esta_semana": ["essa semana", "esta semana", "amanhã", "amanha", "semana"],
        "este_mes": ["esse mês", "esse mes", "este mês", "este mes", "mês", "mes"],
        "proximo_mes": ["mês que vem", "mes que vem", "próximo mês", "proximo mes"]
    }

    def __init__(self, redis_client: redis.Redis):
        """
        Inicializa sistema de score

        Args:
            redis_client: Cliente Redis configurado
        """
        self.redis = redis_client

    def calcular_delta(self, mensagem: str, estado_cliente: Dict[str, Any]) -> int:
        """
        Calcula pontos a adicionar baseado na mensagem

        Args:
            mensagem: Mensagem do cliente (normalizada lowercase)
            estado_cliente: Estado atual do cliente (últimas ações)

        Returns:
            Pontos a adicionar (0-100)
        """
        mensagem_lower = mensagem.lower()
        delta = 0

        # Informações fornecidas
        if self._detectar_palavras(mensagem_lower, self.KEYWORDS["tipo"]):
            if not estado_cliente.get("tem_tipo_definido"):
                delta += self.PESOS["tipo_definido"]
                estado_cliente["tem_tipo_definido"] = True

        if self._detectar_palavras(mensagem_lower, self.KEYWORDS["regiao"]):
            if not estado_cliente.get("tem_regiao_definida"):
                delta += self.PESOS["regiao_definida"]
                estado_cliente["tem_regiao_definida"] = True

        if self._detectar_palavras(mensagem_lower, self.KEYWORDS["orcamento"]):
            if not estado_cliente.get("tem_orcamento_definido"):
                delta += self.PESOS["orcamento_definido"]
                estado_cliente["tem_orcamento_definido"] = True

        # Comportamento
        if self._detectar_palavras(mensagem_lower, self.KEYWORDS["fotos"]):
            if not estado_cliente.get("pediu_fotos"):
                delta += self.PESOS["pediu_fotos"]
                estado_cliente["pediu_fotos"] = True

        if self._detectar_palavras(mensagem_lower, self.KEYWORDS["pergunta"]):
            if not estado_cliente.get("fez_perguntas"):
                delta += self.PESOS["fez_perguntas"]
                estado_cliente["fez_perguntas"] = True

        if self._detectar_palavras(mensagem_lower, self.KEYWORDS["prazo"]):
            if not estado_cliente.get("mencionou_prazo"):
                delta += self.PESOS["mencionou_prazo"]
                estado_cliente["mencionou_prazo"] = True

        # Resposta rápida (< 2min)
        ultima_mensagem_ts = estado_cliente.get("ultima_mensagem_timestamp")
        if ultima_mensagem_ts:
            tempo_decorrido = time.time() - ultima_mensagem_ts
            if tempo_decorrido < 120:  # 2 minutos
                if not estado_cliente.get("respondeu_rapido"):
                    delta += self.PESOS["resposta_rapida"]
                    estado_cliente["respondeu_rapido"] = True

        # Urgência (mutuamente exclusivo - só o maior vale)
        if not estado_cliente.get("tem_urgencia"):
            if self._detectar_palavras(mensagem_lower, self.KEYWORDS["urgente"]):
                delta += self.PESOS["urgente"]
                estado_cliente["tem_urgencia"] = "urgente"
            elif self._detectar_palavras(mensagem_lower, self.KEYWORDS["esta_semana"]):
                delta += self.PESOS["esta_semana"]
                estado_cliente["tem_urgencia"] = "esta_semana"
            elif self._detectar_palavras(mensagem_lower, self.KEYWORDS["este_mes"]):
                delta += self.PESOS["este_mes"]
                estado_cliente["tem_urgencia"] = "este_mes"
            elif self._detectar_palavras(mensagem_lower, self.KEYWORDS["proximo_mes"]):
                delta += self.PESOS["proximo_mes"]
                estado_cliente["tem_urgencia"] = "proximo_mes"

        # Atualizar timestamp
        estado_cliente["ultima_mensagem_timestamp"] = time.time()

        return delta

    def _detectar_palavras(self, texto: str, keywords: list) -> bool:
        """
        Detecta se alguma palavra-chave está no texto

        Args:
            texto: Texto a verificar (lowercase)
            keywords: Lista de palavras/regex

        Returns:
            True se encontrou alguma palavra-chave
        """
        for keyword in keywords:
            if keyword.startswith(r"\\"):  # É regex
                if re.search(keyword, texto):
                    return True
            else:
                if keyword in texto:
                    return True
        return False

    def atualizar_score(self, cliente_numero: str, delta: int) -> int:
        """
        Atualiza score do cliente

        Args:
            cliente_numero: Número do cliente (ex: 5531980160822)
            delta: Pontos a adicionar

        Returns:
            Novo score total (0-100)
        """
        score_key = f"score:{cliente_numero}"
        history_key = f"score_history:{cliente_numero}"

        # Buscar score atual
        score_atual = int(self.redis.get(score_key) or 0)

        # Calcular novo score (max 100)
        novo_score = min(score_atual + delta, 100)

        # Salvar novo score
        self.redis.set(score_key, novo_score)

        # Salvar no histórico
        self.redis.lpush(history_key, json.dumps({
            "timestamp": time.time(),
            "delta": delta,
            "score_total": novo_score
        }))

        # Limitar histórico a 100 entradas
        self.redis.ltrim(history_key, 0, 99)

        return novo_score

    def get_score(self, cliente_numero: str) -> int:
        """
        Retorna score atual do cliente

        Args:
            cliente_numero: Número do cliente

        Returns:
            Score atual (0-100)
        """
        score_key = f"score:{cliente_numero}"
        return int(self.redis.get(score_key) or 0)

    def get_historico(self, cliente_numero: str, limit: int = 10) -> list:
        """
        Retorna histórico de pontuações

        Args:
            cliente_numero: Número do cliente
            limit: Número de entradas a retornar

        Returns:
            Lista de dicts com histórico
        """
        history_key = f"score_history:{cliente_numero}"
        historico_raw = self.redis.lrange(history_key, 0, limit - 1)

        return [json.loads(h) for h in historico_raw]

    def classificar_lead(self, score: int) -> str:
        """
        Classifica lead baseado no score

        Args:
            score: Score do cliente (0-100)

        Returns:
            "QUENTE", "MORNO" ou "FRIO"
        """
        if score >= 70:
            return "QUENTE"
        elif score >= 40:
            return "MORNO"
        else:
            return "FRIO"

    def reset_score(self, cliente_numero: str):
        """
        Reseta score do cliente (usar com cuidado)

        Args:
            cliente_numero: Número do cliente
        """
        score_key = f"score:{cliente_numero}"
        self.redis.delete(score_key)
