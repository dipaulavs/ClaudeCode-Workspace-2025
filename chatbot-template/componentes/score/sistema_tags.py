"""
Sistema de Tags automáticas para Chatwoot
Detecta e aplica tags baseado em mensagens e score
"""
import json
import re
import requests
from typing import List, Dict, Any, Optional
import redis


class SistemaTags:
    """
    Sistema de tags automáticas para organização no Chatwoot

    Categorias:
    - Estágio do funil: primeiro_contato, interessado, engajado
    - Preferências: tem_pet, quer_mobilia, vaga_garagem
    - Urgência: prioridade_alta, prioridade_media
    - Comportamento: visual, preco_sensivel
    - Score: lead_quente, lead_morno, lead_frio
    """

    # Tags automáticas baseadas em palavras-chave
    TAGS_AUTOMATICAS = {
        # Estágio do funil
        "primeiro_contato": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"],
        "interessado": ["quero", "procurando", "busco", "preciso", "gostaria", "interesse"],
        "engajado": ["foto", "visitar", "quando posso", "agendar", "ver"],

        # Preferências
        "tem_pet": ["pet", "cachorro", "gato", "animal", "bicho"],
        "quer_mobilia": ["mobiliado", "mobília", "mobilia", "móveis", "moveis"],
        "vaga_garagem": ["garagem", "vaga", "estacionamento", "carro"],

        # Urgência
        "prioridade_alta": ["urgente", "hoje", "rápido", "rapido", "agora", "imediato"],
        "prioridade_media": ["essa semana", "esta semana", "amanhã", "amanha"],

        # Comportamento
        "visual": ["foto", "imagem", "vídeo", "video", "imagens", "fotos"],
        "preco_sensivel": ["valor", "preço", "preco", "quanto custa", "quanto é", "quanto sai"],
    }

    def __init__(self, redis_client: redis.Redis, chatwoot_config: Dict[str, Any]):
        """
        Inicializa sistema de tags

        Args:
            redis_client: Cliente Redis configurado
            chatwoot_config: Config do Chatwoot (url, token, account_id)
        """
        self.redis = redis_client
        self.chatwoot_url = chatwoot_config["url"]
        self.chatwoot_token = chatwoot_config["token"]
        self.account_id = chatwoot_config["account_id"]
        self.inbox_id = chatwoot_config["inbox_id"]

        self.headers = {
            "api_access_token": self.chatwoot_token,
            "Content-Type": "application/json"
        }

    def detectar_tags(self, mensagem: str, score: int) -> List[str]:
        """
        Detecta tags aplicáveis baseado na mensagem e score

        Args:
            mensagem: Mensagem do cliente (normalizada)
            score: Score atual do cliente

        Returns:
            Lista de tags a aplicar
        """
        mensagem_lower = mensagem.lower()
        tags = []

        # Tags baseadas em palavras-chave
        for tag, keywords in self.TAGS_AUTOMATICAS.items():
            if self._detectar_palavras(mensagem_lower, keywords):
                tags.append(tag)

        # Tags baseadas em score
        if score >= 70:
            tags.append("lead_quente")
        elif score >= 40:
            tags.append("lead_morno")
        else:
            tags.append("lead_frio")

        return tags

    def _detectar_palavras(self, texto: str, keywords: List[str]) -> bool:
        """
        Detecta se alguma palavra-chave está no texto

        Args:
            texto: Texto a verificar (lowercase)
            keywords: Lista de palavras-chave

        Returns:
            True se encontrou alguma palavra-chave
        """
        for keyword in keywords:
            if keyword in texto:
                return True
        return False

    def aplicar_chatwoot(self, cliente_numero: str, tags: List[str]) -> bool:
        """
        Aplica tags no Chatwoot via API

        Args:
            cliente_numero: Número do cliente
            tags: Lista de tags a aplicar

        Returns:
            True se sucesso
        """
        try:
            # 1. Buscar ID da conversa
            conv_id = self._get_conversa_id(cliente_numero)
            if not conv_id:
                print(f"⚠️ Conversa não encontrada para {cliente_numero}")
                return False

            # 2. Para cada tag
            for tag in tags:
                # Verificar se já aplicada
                if self._tag_ja_aplicada(cliente_numero, tag):
                    continue

                # Aplicar tag
                url = f"{self.chatwoot_url}/api/v1/accounts/{self.account_id}/conversations/{conv_id}/labels"
                response = requests.post(
                    url,
                    headers=self.headers,
                    json={"labels": [tag]}
                )

                if response.status_code in [200, 201]:
                    # Salvar no Redis (cache)
                    self._marcar_tag_aplicada(cliente_numero, tag)
                    print(f"✅ Tag '{tag}' aplicada para {cliente_numero}")
                else:
                    print(f"❌ Erro ao aplicar tag '{tag}': {response.text}")

            return True

        except Exception as e:
            print(f"❌ Erro ao aplicar tags no Chatwoot: {e}")
            return False

    def _get_conversa_id(self, cliente_numero: str) -> Optional[int]:
        """
        Busca ID da conversa no Chatwoot baseado no número

        Args:
            cliente_numero: Número do cliente

        Returns:
            ID da conversa ou None
        """
        try:
            # Cache no Redis
            cache_key = f"chatwoot:conv_id:{cliente_numero}"
            cached = self.redis.get(cache_key)
            if cached:
                return int(cached)

            # Buscar via API
            url = f"{self.chatwoot_url}/api/v1/accounts/{self.account_id}/conversations"
            params = {
                "inbox_id": self.inbox_id,
                "status": "all"
            }

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                conversas = response.json().get("data", {}).get("payload", [])

                # Filtrar por número
                for conv in conversas:
                    contact = conv.get("meta", {}).get("sender", {})
                    phone = contact.get("phone_number", "").replace("+", "")

                    if phone == cliente_numero:
                        conv_id = conv["id"]
                        # Cachear por 1 hora
                        self.redis.setex(cache_key, 3600, conv_id)
                        return conv_id

            return None

        except Exception as e:
            print(f"❌ Erro ao buscar conversa: {e}")
            return None

    def _tag_ja_aplicada(self, cliente_numero: str, tag: str) -> bool:
        """
        Verifica se tag já foi aplicada

        Args:
            cliente_numero: Número do cliente
            tag: Tag a verificar

        Returns:
            True se já aplicada
        """
        tags_key = f"tags_aplicadas:{cliente_numero}"
        tags_aplicadas = self.redis.smembers(tags_key)
        return tag.encode() in tags_aplicadas

    def _marcar_tag_aplicada(self, cliente_numero: str, tag: str):
        """
        Marca tag como aplicada no cache

        Args:
            cliente_numero: Número do cliente
            tag: Tag aplicada
        """
        tags_key = f"tags_aplicadas:{cliente_numero}"
        self.redis.sadd(tags_key, tag)

    def remover_tag(self, cliente_numero: str, tag: str) -> bool:
        """
        Remove tag do Chatwoot

        Args:
            cliente_numero: Número do cliente
            tag: Tag a remover

        Returns:
            True se sucesso
        """
        try:
            # Buscar ID da conversa
            conv_id = self._get_conversa_id(cliente_numero)
            if not conv_id:
                return False

            # Remover tag
            url = f"{self.chatwoot_url}/api/v1/accounts/{self.account_id}/conversations/{conv_id}/labels"
            response = requests.delete(
                url,
                headers=self.headers,
                json={"labels": [tag]}
            )

            if response.status_code in [200, 204]:
                # Remover do cache
                tags_key = f"tags_aplicadas:{cliente_numero}"
                self.redis.srem(tags_key, tag)
                print(f"✅ Tag '{tag}' removida para {cliente_numero}")
                return True
            else:
                print(f"❌ Erro ao remover tag: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Erro ao remover tag: {e}")
            return False

    def atualizar_custom_attributes(self, cliente_numero: str, attributes: Dict[str, Any]) -> bool:
        """
        Atualiza custom attributes no Chatwoot

        Args:
            cliente_numero: Número do cliente
            attributes: Dict com atributos (ex: {"score": 75, "classificacao": "QUENTE"})

        Returns:
            True se sucesso
        """
        try:
            # Buscar ID da conversa
            conv_id = self._get_conversa_id(cliente_numero)
            if not conv_id:
                return False

            # Atualizar custom attributes
            url = f"{self.chatwoot_url}/api/v1/accounts/{self.account_id}/conversations/{conv_id}/custom_attributes"
            response = requests.post(
                url,
                headers=self.headers,
                json={"custom_attributes": attributes}
            )

            if response.status_code in [200, 201]:
                print(f"✅ Custom attributes atualizados para {cliente_numero}: {attributes}")
                return True
            else:
                print(f"❌ Erro ao atualizar custom attributes: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Erro ao atualizar custom attributes: {e}")
            return False

    def get_tags_aplicadas(self, cliente_numero: str) -> List[str]:
        """
        Retorna tags aplicadas para o cliente

        Args:
            cliente_numero: Número do cliente

        Returns:
            Lista de tags aplicadas
        """
        tags_key = f"tags_aplicadas:{cliente_numero}"
        tags = self.redis.smembers(tags_key)
        return [tag.decode() for tag in tags]
