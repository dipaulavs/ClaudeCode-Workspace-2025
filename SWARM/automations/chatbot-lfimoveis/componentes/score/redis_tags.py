#!/usr/bin/env python3
"""
🏷️ SISTEMA DE TAGS - Redis Puro (Upstash)

Sistema simplificado 100% Redis para tagueamento de leads.
Substitui sistema_tags.py (complexo) por solução Redis-first.

FUNÇÕES:
- adicionar_tag(cliente, tag)
- remover_tag(cliente, tag)
- obter_tags(cliente)
- limpar_tags(cliente)
- tags_por_score(score)
- tags_por_mensagem(mensagem)
"""

import json
import time
from typing import List, Set, Dict, Any
from upstash_redis import Redis


class RedisTagsSimples:
    """
    Sistema de tags 100% Redis (sem Chatwoot)

    Armazena no Redis:
    - tags:{cliente} → Set de tags
    - tag_history:{cliente} → Lista de eventos

    Tags automáticas baseadas em score:
    - lead_quente (score >= 70)
    - lead_morno (score 40-69)
    - lead_frio (score < 40)
    """

    # Tags automáticas por palavras-chave
    TAGS_KEYWORDS = {
        # Estágio
        "primeiro_contato": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"],
        "interessado": ["quero", "procurando", "busco", "preciso", "gostaria", "interesse"],
        "engajado": ["foto", "visitar", "quando posso", "agendar", "ver"],

        # Preferências
        "tem_pet": ["pet", "cachorro", "gato", "animal", "bicho"],
        "quer_mobiliado": ["mobiliado", "mobília", "mobilia", "móveis", "moveis"],
        "vaga_garagem": ["garagem", "vaga", "estacionamento", "carro"],

        # Urgência
        "urgente": ["urgente", "hoje", "rápido", "rapido", "agora", "imediato"],
        "esta_semana": ["essa semana", "esta semana", "amanhã", "amanha"],

        # Comportamento
        "visual": ["foto", "imagem", "vídeo", "video", "imagens", "fotos"],
        "preco_sensivel": ["valor", "preço", "preco", "quanto custa", "quanto é"],
    }

    def __init__(self, redis_client: Redis):
        """
        Inicializa sistema de tags

        Args:
            redis_client: Cliente upstash_redis.Redis
        """
        self.redis = redis_client

    def adicionar_tag(self, cliente_numero: str, tag: str) -> bool:
        """
        Adiciona tag ao cliente (Redis Set)

        Args:
            cliente_numero: Número do cliente
            tag: Tag a adicionar

        Returns:
            True se adicionou (False se já existia)
        """
        try:
            tags_key = f"tags:{cliente_numero}"

            # Adiciona no Set (retorna 1 se novo, 0 se já existia)
            resultado = self.redis.sadd(tags_key, tag)

            # Registra no histórico
            if resultado == 1:
                self._registrar_evento(cliente_numero, "add", tag)
                return True

            return False

        except Exception as e:
            print(f"❌ Erro ao adicionar tag: {e}", flush=True)
            return False

    def remover_tag(self, cliente_numero: str, tag: str) -> bool:
        """
        Remove tag do cliente

        Args:
            cliente_numero: Número do cliente
            tag: Tag a remover

        Returns:
            True se removeu (False se não existia)
        """
        try:
            tags_key = f"tags:{cliente_numero}"

            # Remove do Set (retorna 1 se existia, 0 se não)
            resultado = self.redis.srem(tags_key, tag)

            # Registra no histórico
            if resultado == 1:
                self._registrar_evento(cliente_numero, "remove", tag)
                return True

            return False

        except Exception as e:
            print(f"❌ Erro ao remover tag: {e}", flush=True)
            return False

    def obter_tags(self, cliente_numero: str) -> Set[str]:
        """
        Retorna todas as tags do cliente

        Args:
            cliente_numero: Número do cliente

        Returns:
            Set de tags
        """
        try:
            tags_key = f"tags:{cliente_numero}"
            tags_raw = self.redis.smembers(tags_key)

            # Upstash Redis já retorna strings
            if isinstance(tags_raw, set):
                return tags_raw
            elif isinstance(tags_raw, list):
                return set(tags_raw)
            else:
                return set()

        except Exception as e:
            print(f"❌ Erro ao obter tags: {e}", flush=True)
            return set()

    def limpar_tags(self, cliente_numero: str) -> bool:
        """
        Remove todas as tags do cliente

        Args:
            cliente_numero: Número do cliente

        Returns:
            True se sucesso
        """
        try:
            tags_key = f"tags:{cliente_numero}"
            self.redis.delete(tags_key)

            self._registrar_evento(cliente_numero, "clear", "all")
            return True

        except Exception as e:
            print(f"❌ Erro ao limpar tags: {e}", flush=True)
            return False

    def tags_por_score(self, score: int) -> List[str]:
        """
        Retorna tags automáticas baseadas no score

        Args:
            score: Score do cliente (0-100)

        Returns:
            Lista de tags
        """
        tags = []

        if score >= 70:
            tags.append("lead_quente")
        elif score >= 40:
            tags.append("lead_morno")
        else:
            tags.append("lead_frio")

        return tags

    def tags_por_mensagem(self, mensagem: str) -> List[str]:
        """
        Detecta tags baseadas em palavras-chave na mensagem

        Args:
            mensagem: Mensagem do cliente

        Returns:
            Lista de tags detectadas
        """
        mensagem_lower = mensagem.lower()
        tags = []

        for tag, keywords in self.TAGS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in mensagem_lower:
                    tags.append(tag)
                    break  # Próxima tag

        return tags

    def atualizar_tags_automaticas(
        self,
        cliente_numero: str,
        mensagem: str,
        score: int
    ) -> Dict[str, List[str]]:
        """
        Atualiza tags automaticamente baseado em mensagem e score

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem do cliente
            score: Score atual

        Returns:
            Dict com tags_adicionadas e tags_removidas
        """
        resultado = {
            "tags_adicionadas": [],
            "tags_removidas": []
        }

        # Tags de score (remover antigas primeiro)
        tags_score_antigas = {"lead_quente", "lead_morno", "lead_frio"}
        tags_score_novas = self.tags_por_score(score)

        for tag_antiga in tags_score_antigas:
            if tag_antiga not in tags_score_novas:
                if self.remover_tag(cliente_numero, tag_antiga):
                    resultado["tags_removidas"].append(tag_antiga)

        for tag_nova in tags_score_novas:
            if self.adicionar_tag(cliente_numero, tag_nova):
                resultado["tags_adicionadas"].append(tag_nova)

        # Tags de mensagem
        tags_mensagem = self.tags_por_mensagem(mensagem)
        for tag in tags_mensagem:
            if self.adicionar_tag(cliente_numero, tag):
                resultado["tags_adicionadas"].append(tag)

        return resultado

    def _registrar_evento(self, cliente_numero: str, acao: str, tag: str):
        """
        Registra evento no histórico (últimos 50)

        Args:
            cliente_numero: Número do cliente
            acao: "add", "remove", "clear"
            tag: Tag afetada
        """
        try:
            history_key = f"tag_history:{cliente_numero}"

            evento = json.dumps({
                "timestamp": time.time(),
                "acao": acao,
                "tag": tag
            })

            # Adiciona no início da lista
            self.redis.lpush(history_key, evento)

            # Limita a 50 entradas
            self.redis.ltrim(history_key, 0, 49)

        except Exception as e:
            print(f"⚠️ Erro ao registrar evento: {e}", flush=True)

    def obter_historico(self, cliente_numero: str, limit: int = 10) -> List[Dict]:
        """
        Retorna histórico de tags

        Args:
            cliente_numero: Número do cliente
            limit: Quantidade de eventos

        Returns:
            Lista de eventos
        """
        try:
            history_key = f"tag_history:{cliente_numero}"
            eventos_raw = self.redis.lrange(history_key, 0, limit - 1)

            if not eventos_raw:
                return []

            eventos = []
            for evento_str in eventos_raw:
                try:
                    # Upstash já retorna string
                    if isinstance(evento_str, bytes):
                        evento_str = evento_str.decode()
                    eventos.append(json.loads(evento_str))
                except:
                    continue

            return eventos

        except Exception as e:
            print(f"❌ Erro ao obter histórico: {e}", flush=True)
            return []


# ================== TESTE STANDALONE ==================

if __name__ == "__main__":
    print("🧪 Testando RedisTagsSimples...\n")

    from upstash_redis import Redis

    # Credenciais corretas
    redis = Redis(
        url="https://smashing-gull-23432.upstash.io",
        token="AVuIAAIncDJkMDY5NTA1ZWM5OTg0NmY4YjYwN2U0NmI1YjY2YmJhNXAyMjM0MzI"
    )

    sistema = RedisTagsSimples(redis)

    cliente_teste = "5531999999999"

    print("📋 Teste 1: Adicionar tags")
    print("-" * 50)
    sistema.adicionar_tag(cliente_teste, "interessado")
    sistema.adicionar_tag(cliente_teste, "tem_pet")
    sistema.adicionar_tag(cliente_teste, "urgente")
    print(f"Tags: {sistema.obter_tags(cliente_teste)}\n")

    print("📋 Teste 2: Tags por mensagem")
    print("-" * 50)
    msg = "Quero agendar uma visita, tenho cachorro"
    tags = sistema.tags_por_mensagem(msg)
    print(f"Mensagem: {msg}")
    print(f"Tags detectadas: {tags}\n")

    print("📋 Teste 3: Tags por score")
    print("-" * 50)
    print(f"Score 80: {sistema.tags_por_score(80)}")
    print(f"Score 50: {sistema.tags_por_score(50)}")
    print(f"Score 20: {sistema.tags_por_score(20)}\n")

    print("📋 Teste 4: Atualização automática")
    print("-" * 50)
    resultado = sistema.atualizar_tags_automaticas(
        cliente_teste,
        "Quero ver fotos do apartamento urgente",
        75
    )
    print(f"Adicionadas: {resultado['tags_adicionadas']}")
    print(f"Removidas: {resultado['tags_removidas']}")
    print(f"Tags finais: {sistema.obter_tags(cliente_teste)}\n")

    print("📋 Teste 5: Histórico")
    print("-" * 50)
    historico = sistema.obter_historico(cliente_teste)
    for evento in historico[:3]:
        print(f"  {evento}")

    # Limpa
    print("\n🧹 Limpando teste...")
    sistema.limpar_tags(cliente_teste)
    print(f"Tags após limpar: {sistema.obter_tags(cliente_teste)}")
    print("\n✅ Teste completo!")
