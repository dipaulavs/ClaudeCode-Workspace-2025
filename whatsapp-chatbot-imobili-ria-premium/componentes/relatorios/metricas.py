"""
Sistema de coleta de métricas para chatbot
Armazena counters no Redis para gerar relatórios
"""

import redis
from datetime import datetime, date
from typing import Optional, Union, List, Tuple


class ColetorMetricas:
    """
    Coleta e armazena métricas do chatbot no Redis

    Métricas disponíveis:
    - leads_total: Total acumulado de leads
    - leads_novos_hoje: Leads novos do dia (resetado diariamente)
    - leads_quentes: Lista de números com score >= 70
    - bot_atendeu: Conversas respondidas pelo bot
    - escaladas: Conversas transferidas para humano
    - visitas_agendadas: Visitas confirmadas
    - propostas_enviadas: Propostas geradas
    - followups_enviados: Follow-ups automáticos enviados
    - followups_respondidos: Follow-ups que obtiveram resposta
    - imoveis_mais_procurados: Sorted set {imovel_id: views}
    """

    def __init__(self):
        """Inicializa conexão com Redis"""
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=False  # Mantem bytes para controle
        )

    def incrementar(self, metrica: str, valor: int = 1, data: Optional[date] = None) -> None:
        """
        Incrementa contador de métrica

        Args:
            metrica: Nome da métrica (ex: "leads_novos_hoje")
            valor: Valor a incrementar (padrão: 1)
            data: Data da métrica (padrão: hoje)
        """
        if data is None:
            data = datetime.now().date()

        chave = self._gerar_chave(metrica, data)
        self.redis.incr(chave, valor)

        # Define expiração de 90 dias
        self.redis.expire(chave, 90 * 24 * 60 * 60)

    def adicionar_lista(self, metrica: str, imóvel: str, data: Optional[date] = None) -> None:
        """
        Adiciona imóvel em lista de métrica

        Args:
            metrica: Nome da métrica (ex: "leads_quentes")
            imóvel: Imóvel a adicionar (ex: número de telefone)
            data: Data da métrica (padrão: hoje)
        """
        if data is None:
            data = datetime.now().date()

        chave = self._gerar_chave(metrica, data)

        # Evita duplicatas
        if not self.redis.lpos(chave, imóvel):
            self.redis.lpush(chave, imóvel)

        # Define expiração de 90 dias
        self.redis.expire(chave, 90 * 24 * 60 * 60)

    def incrementar_sorted_set(self, metrica: str, imóvel: str, score: int = 1, data: Optional[date] = None) -> None:
        """
        Incrementa score em sorted set

        Args:
            metrica: Nome da métrica (ex: "imoveis_mais_procurados")
            imóvel: Imóvel a incrementar (ex: imovel_id)
            score: Score a incrementar (padrão: 1)
            data: Data da métrica (padrão: hoje)
        """
        if data is None:
            data = datetime.now().date()

        chave = self._gerar_chave(metrica, data)
        self.redis.zincrby(chave, score, imóvel)

        # Define expiração de 90 dias
        self.redis.expire(chave, 90 * 24 * 60 * 60)

    def buscar(self, metrica: str, data: Optional[date] = None) -> Union[int, List[bytes], List[Tuple[bytes, float]], None]:
        """
        Busca valor de métrica

        Args:
            metrica: Nome da métrica
            data: Data da métrica (padrão: hoje)

        Returns:
            - int: Para counters
            - List[bytes]: Para listas
            - List[Tuple[bytes, float]]: Para sorted sets
            - None: Se não existir
        """
        if data is None:
            data = datetime.now().date()

        chave = self._gerar_chave(metrica, data)

        # Verifica se chave existe
        if not self.redis.exists(chave):
            # Retorna valor padrão baseado no tipo de métrica
            if metrica in ['leads_quentes']:
                return []
            elif metrica in ['imoveis_mais_procurados']:
                return []
            else:
                return 0

        # Detecta tipo
        tipo = self.redis.type(chave).decode()

        if tipo == 'string':
            valor = self.redis.get(chave)
            return int(valor) if valor else 0

        elif tipo == 'list':
            return self.redis.lrange(chave, 0, -1)

        elif tipo == 'zset':
            return self.redis.zrevrange(chave, 0, -1, withscores=True)

        return None

    def resetar(self, metrica: str, data: Optional[date] = None) -> None:
        """
        Reseta métrica para zero

        Args:
            metrica: Nome da métrica
            data: Data da métrica (padrão: hoje)
        """
        if data is None:
            data = datetime.now().date()

        chave = self._gerar_chave(metrica, data)
        self.redis.delete(chave)

    def _gerar_chave(self, metrica: str, data: date) -> str:
        """
        Gera chave Redis para métrica

        Args:
            metrica: Nome da métrica
            data: Data da métrica

        Returns:
            Chave formatada (ex: "metricas:2025-11-04:leads_novos_hoje")
        """
        data_str = data.strftime('%Y-%m-%d')
        return f"metricas:{data_str}:{metrica}"

    def buscar_periodo(self, metrica: str, data_inicio: date, data_fim: date) -> int:
        """
        Busca soma de métrica em período

        Args:
            metrica: Nome da métrica (deve ser counter)
            data_inicio: Data inicial
            data_fim: Data final

        Returns:
            Soma dos valores no período
        """
        from datetime import timedelta

        total = 0
        data_atual = data_inicio

        while data_atual <= data_fim:
            valor = self.buscar(metrica, data_atual)
            if isinstance(valor, int):
                total += valor

            data_atual += timedelta(days=1)

        return total
