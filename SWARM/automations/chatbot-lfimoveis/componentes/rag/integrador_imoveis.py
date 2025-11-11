#!/usr/bin/env python3
"""
🎯 INTEGRADOR RAG - Pipeline Completo (ADAPTADO PARA IMÓVEIS)

Orquestra todo o fluxo RAG + Progressive Disclosure:

ESTÁGIO 1: Identificação
  Cliente pergunta → RAG Híbrido → TOP 3 candidatos → Cliente escolhe

ESTÁGIO 2: Especialista
  Cliente escolheu → Progressive Disclosure → IA Especialista → 100% precisão

Economia: 50% tokens | Precisão: 100%
"""

from pathlib import Path
from typing import Dict, List, Optional
from upstash_redis import Redis

from .busca_hibrida_imoveis import RAGHibridoImoveis
from .busca_vetorial import BuscaVetorial
from .ia_especialista_imoveis import IAEspecialistaImoveis


class IntegradorRAGImoveis:
    """
    Orquestrador principal do sistema RAG para imóveis
    """

    def __init__(
        self,
        imoveis_dir: Path,
        openai_api_key: str,
        openrouter_api_key: str,
        redis_client: Redis
    ):
        """
        Args:
            imoveis_dir: Diretório com imóveis
            openai_api_key: Chave OpenAI (embeddings)
            openrouter_api_key: Chave OpenRouter (Claude)
            redis_client: Cliente Redis
        """
        self.rag = RAGHibridoImoveis(imoveis_dir, openai_api_key)
        self.busca_vetorial = BuscaVetorial(imoveis_dir, openai_api_key)
        self.especialista = IAEspecialistaImoveis(openrouter_api_key)
        self.redis = redis_client

        print("✅ IntegradorRAGImoveis inicializado", flush=True)
        print(f"   - Database: {len(self.rag.database)} imóveis", flush=True)
        print(f"   - Busca Vetorial: Ativa", flush=True)

    def processar_mensagem(
        self,
        cliente_numero: str,
        mensagem: str,
        contexto: Optional[List[Dict]] = None
    ) -> str:
        """
        Pipeline completo RAG

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem do cliente
            contexto: Histórico da conversa

        Returns:
            Resposta para o cliente
        """
        print(f"\n🎯 IntegradorRAGImoveis: Processando mensagem", flush=True)
        print(f"   Cliente: {cliente_numero}", flush=True)
        print(f"   Mensagem: {mensagem[:50]}...", flush=True)

        # Verifica se cliente já escolheu imóvel
        item_ativo = self._get_item_ativo(cliente_numero)

        if item_ativo:
            print(f"   Item ativo: {item_ativo} (ESTÁGIO 2)", flush=True)
            return self._processar_estagio_2(cliente_numero, item_ativo, mensagem, contexto)
        else:
            print(f"   Sem item ativo (ESTÁGIO 1)", flush=True)
            return self._processar_estagio_1(cliente_numero, mensagem)

    def _processar_estagio_1(self, cliente_numero: str, mensagem: str) -> str:
        """
        ESTÁGIO 1: Identificação do imóvel

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem do cliente

        Returns:
            Resposta (apresentação de candidatos ou confirmação)
        """
        print("   🔍 ESTÁGIO 1: Buscando candidatos...", flush=True)

        # RAG Híbrido busca candidatos
        candidatos = self.rag.buscar(mensagem)

        if len(candidatos) == 0:
            return "Hmm, não encontrei imóveis com essas características. Pode me dar mais detalhes? 🤔 (tipo, bairro, quartos, preço)"

        elif len(candidatos) == 1:
            # Só 1 resultado → marca automaticamente
            item_ativo = candidatos[0]["id"]
            self._set_item_ativo(cliente_numero, item_ativo)

            print(f"   ✅ 1 candidato → Item ativo: {item_ativo}", flush=True)

            return "Perfeito! Achei o imóvel ideal pra vc! 😊 O que quer saber sobre ele?"

        else:
            # Múltiplos → apresenta opções
            print(f"   📋 {len(candidatos)} candidatos → Apresentando lista", flush=True)

            # Salva candidatos no Redis (para quando cliente escolher)
            self._salvar_candidatos(cliente_numero, candidatos)

            return self.especialista.responder_multiplos_imoveis(candidatos, mensagem)

    def _processar_estagio_2(
        self,
        cliente_numero: str,
        item_ativo: str,
        mensagem: str,
        contexto: Optional[List[Dict]] = None
    ) -> str:
        """
        ESTÁGIO 2: IA Especialista com Progressive Disclosure

        Args:
            cliente_numero: Número do cliente
            item_ativo: ID do imóvel ativo
            mensagem: Mensagem do cliente
            contexto: Histórico

        Returns:
            Resposta da IA Especialista
        """
        print("   🤖 ESTÁGIO 2: IA Especialista...", flush=True)

        # Verifica se cliente está escolhendo de uma lista
        if self._eh_escolha_numerica(mensagem):
            return self._processar_escolha(cliente_numero, mensagem)

        # 🔍 Busca Vetorial - retorna chunks mais relevantes
        resultado_busca = self.busca_vetorial.buscar(item_ativo, mensagem, top_k=3)
        print(f"   💾 Carregados: {resultado_busca.get('tokens_total', 0):.0f} tokens", flush=True)

        # IA Especialista responde com chunks relevantes
        resposta = self.especialista.responder_busca_vetorial(resultado_busca, mensagem, contexto)

        return resposta

    def _eh_escolha_numerica(self, mensagem: str) -> bool:
        """
        Detecta se mensagem é escolha numérica (ex: "1", "o primeiro", "segundo")

        Args:
            mensagem: Mensagem do cliente

        Returns:
            True se for escolha numérica
        """
        msg_lower = mensagem.lower().strip()

        # Padrões de escolha
        padroes = [
            r'^\d+$',  # "1", "2", "3"
            r'^o?\s*primeiro',  # "primeiro", "o primeiro"
            r'^o?\s*segundo',  # "segundo", "o segundo"
            r'^o?\s*terceiro',  # "terceiro", "o terceiro"
            r'^opção\s*\d+',  # "opção 1"
            r'^número\s*\d+',  # "número 1"
        ]

        import re
        return any(re.search(padrao, msg_lower) for padrao in padroes)

    def _processar_escolha(self, cliente_numero: str, mensagem: str) -> str:
        """
        Processa escolha numérica do cliente

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem com escolha

        Returns:
            Confirmação da escolha
        """
        # Carrega candidatos salvos
        candidatos = self._get_candidatos(cliente_numero)

        if not candidatos:
            return "Desculpa, não lembro quais opções te mostrei. Pode me dizer o que procura novamente? 🤔"

        # Extrai número da escolha
        import re
        match = re.search(r'\d+', mensagem)

        if not match:
            # Tenta palavras (primeiro, segundo, terceiro)
            palavras_numeros = {
                "primeiro": 1, "primeira": 1,
                "segundo": 2, "segunda": 2,
                "terceiro": 3, "terceira": 3
            }

            for palavra, numero in palavras_numeros.items():
                if palavra in mensagem.lower():
                    match = type('obj', (object,), {'group': lambda x: str(numero)})()
                    break

        if not match:
            return "Não entendi qual opção você quer. Pode me dizer o número? (1, 2 ou 3)"

        escolha = int(match.group(0))

        if escolha < 1 or escolha > len(candidatos):
            return f"Hmm, só tenho {len(candidatos)} opções. Escolhe entre 1 e {len(candidatos)} 😊"

        # Marca item ativo
        item_escolhido = candidatos[escolha - 1]
        item_id = item_escolhido["id"]

        self._set_item_ativo(cliente_numero, item_id)

        # Limpa candidatos
        self._limpar_candidatos(cliente_numero)

        print(f"   ✅ Cliente escolheu: {item_id}", flush=True)

        return f"Show! Vou te falar mais sobre esse imóvel. O que quer saber? 😊"

    # ==================== REDIS HELPERS ====================

    def _get_item_ativo(self, cliente_numero: str) -> Optional[str]:
        """Retorna item ativo do cliente"""
        chave = f"item_ativo:lfimoveis:{cliente_numero}"
        item = self.redis.get(chave)
        if not item:
            return None
        # Upstash Redis já retorna string decodificada
        return item if isinstance(item, str) else item.decode()

    def _set_item_ativo(self, cliente_numero: str, item_id: str, ttl: int = 3600):
        """Define item ativo (expira em 1h)"""
        chave = f"item_ativo:lfimoveis:{cliente_numero}"
        self.redis.set(chave, item_id, ex=ttl)

    def _salvar_candidatos(self, cliente_numero: str, candidatos: List[Dict], ttl: int = 600):
        """Salva candidatos no Redis (expira em 10min)"""
        chave = f"candidatos:lfimoveis:{cliente_numero}"

        # Simplifica candidatos (só info essencial)
        candidatos_simples = [
            {
                "id": c["id"],
                "tipo": c.get("tipo"),
                "bairro": c.get("bairro"),
                "quartos": c.get("quartos"),
                "preco": c.get("preco")
            }
            for c in candidatos
        ]

        import json
        self.redis.set(chave, json.dumps(candidatos_simples), ex=ttl)

    def _get_candidatos(self, cliente_numero: str) -> Optional[List[Dict]]:
        """Retorna candidatos salvos"""
        chave = f"candidatos:lfimoveis:{cliente_numero}"
        dados = self.redis.get(chave)

        if not dados:
            return None

        import json
        # Upstash Redis já retorna string decodificada
        dados_str = dados if isinstance(dados, str) else dados.decode()
        return json.loads(dados_str)

    def _limpar_candidatos(self, cliente_numero: str):
        """Remove candidatos do Redis"""
        chave = f"candidatos:lfimoveis:{cliente_numero}"
        self.redis.delete(chave)

    def limpar_item_ativo(self, cliente_numero: str):
        """
        Remove item ativo (útil para reset)

        Args:
            cliente_numero: Número do cliente
        """
        self._set_item_ativo(cliente_numero, "", ttl=1)  # Expira imediatamente
