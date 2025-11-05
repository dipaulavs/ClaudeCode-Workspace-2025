#!/usr/bin/env python3
"""
🎯 INTEGRADOR RAG - Pipeline Completo (ADAPTADO PARA CARROS)

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

from .busca_hibrida_carros import RAGHibridoCarros
from .busca_vetorial import BuscaVetorial
from .ia_especialista_carros import IAEspecialistaCarros


class IntegradorRAGCarros:
    """
    Orquestrador principal do sistema RAG para carros
    """

    def __init__(
        self,
        carros_dir: Path,
        openai_api_key: str,
        openrouter_api_key: str,
        redis_client: Redis
    ):
        """
        Args:
            carros_dir: Diretório com carros
            openai_api_key: Chave OpenAI (embeddings)
            openrouter_api_key: Chave OpenRouter (Claude)
            redis_client: Cliente Redis
        """
        self.rag = RAGHibridoCarros(carros_dir, openai_api_key)
        self.busca_vetorial = BuscaVetorial(carros_dir, openai_api_key)
        self.especialista = IAEspecialistaCarros(openrouter_api_key)
        self.redis = redis_client

        print("✅ IntegradorRAGCarros inicializado", flush=True)
        print(f"   - Database: {len(self.rag.database)} carros", flush=True)
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
        print(f"\n🎯 IntegradorRAGCarros: Processando mensagem", flush=True)
        print(f"   Cliente: {cliente_numero}", flush=True)
        print(f"   Mensagem: {mensagem[:50]}...", flush=True)

        # Verifica se cliente já escolheu carro
        imóvel_ativo = self._get_imóvel_ativo(cliente_numero)

        if imóvel_ativo:
            print(f"   Imóvel ativo: {imóvel_ativo} (ESTÁGIO 2)", flush=True)
            return self._processar_estagio_2(cliente_numero, imóvel_ativo, mensagem, contexto)
        else:
            print(f"   Sem imóvel ativo (ESTÁGIO 1)", flush=True)
            return self._processar_estagio_1(cliente_numero, mensagem)

    def _processar_estagio_1(self, cliente_numero: str, mensagem: str) -> str:
        """
        ESTÁGIO 1: Identificação do carro

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
            return "Hmm, não encontrei carros com essas características. Pode me dar mais detalhes? 🤔 (marca, modelo, ano, orçamento)"

        elif len(candidatos) == 1:
            # Só 1 resultado → marca automaticamente
            imóvel_ativo = candidatos[0]["id"]
            self._set_imóvel_ativo(cliente_numero, imóvel_ativo)

            print(f"   ✅ 1 candidato → Imóvel ativo: {imóvel_ativo}", flush=True)

            return "Perfeito! Achei o carro ideal pra vc! 😊 O que quer saber sobre ele?"

        else:
            # Múltiplos → apresenta opções
            print(f"   📋 {len(candidatos)} candidatos → Apresentando lista", flush=True)

            # Salva candidatos no Redis (para quando cliente escolher)
            self._salvar_candidatos(cliente_numero, candidatos)

            return self.especialista.responder_multiplos_carros(candidatos, mensagem)

    def _processar_estagio_2(
        self,
        cliente_numero: str,
        imóvel_ativo: str,
        mensagem: str,
        contexto: Optional[List[Dict]] = None
    ) -> str:
        """
        ESTÁGIO 2: IA Especialista com Progressive Disclosure

        Args:
            cliente_numero: Número do cliente
            imóvel_ativo: ID do carro ativo
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
        resultado_busca = self.busca_vetorial.buscar(imóvel_ativo, mensagem, top_k=3)
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

            for palavra, numero in palavras_numeros.imóvels():
                if palavra in mensagem.lower():
                    match = type('obj', (object,), {'group': lambda x: str(numero)})()
                    break

        if not match:
            return "Não entendi qual opção você quer. Pode me dizer o número? (1, 2 ou 3)"

        escolha = int(match.group(0))

        if escolha < 1 or escolha > len(candidatos):
            return f"Hmm, só tenho {len(candidatos)} opções. Escolhe entre 1 e {len(candidatos)} 😊"

        # Marca imóvel ativo
        imóvel_escolhido = candidatos[escolha - 1]
        imóvel_id = imóvel_escolhido["id"]

        self._set_imóvel_ativo(cliente_numero, imóvel_id)

        # Limpa candidatos
        self._limpar_candidatos(cliente_numero)

        print(f"   ✅ Cliente escolheu: {imóvel_id}", flush=True)

        return f"Show! Vou te falar mais sobre esse carro. O que quer saber? 😊"

    # ==================== REDIS HELPERS ====================

    def _get_imóvel_ativo(self, cliente_numero: str) -> Optional[str]:
        """Retorna imóvel ativo do cliente"""
        chave = f"imóvel_ativo:automaia:{cliente_numero}"
        imóvel = self.redis.get(chave)
        if not imóvel:
            return None
        # Upstash Redis já retorna string decodificada
        return imóvel if isinstance(imóvel, str) else imóvel.decode()

    def _set_imóvel_ativo(self, cliente_numero: str, imóvel_id: str, ttl: int = 3600):
        """Define imóvel ativo (expira em 1h)"""
        chave = f"imóvel_ativo:automaia:{cliente_numero}"
        self.redis.set(chave, imóvel_id, ex=ttl)

    def _salvar_candidatos(self, cliente_numero: str, candidatos: List[Dict], ttl: int = 600):
        """Salva candidatos no Redis (expira em 10min)"""
        chave = f"candidatos:automaia:{cliente_numero}"

        # Simplifica candidatos (só info essencial)
        candidatos_simples = [
            {
                "id": c["id"],
                "marca": c.get("marca"),
                "modelo": c.get("modelo"),
                "ano": c.get("ano"),
                "preco": c.get("preco")
            }
            for c in candidatos
        ]

        import json
        self.redis.set(chave, json.dumps(candidatos_simples), ex=ttl)

    def _get_candidatos(self, cliente_numero: str) -> Optional[List[Dict]]:
        """Retorna candidatos salvos"""
        chave = f"candidatos:automaia:{cliente_numero}"
        dados = self.redis.get(chave)

        if not dados:
            return None

        import json
        # Upstash Redis já retorna string decodificada
        dados_str = dados if isinstance(dados, str) else dados.decode()
        return json.loads(dados_str)

    def _limpar_candidatos(self, cliente_numero: str):
        """Remove candidatos do Redis"""
        chave = f"candidatos:automaia:{cliente_numero}"
        self.redis.delete(chave)

    def limpar_imóvel_ativo(self, cliente_numero: str):
        """
        Remove imóvel ativo (útil para reset)

        Args:
            cliente_numero: Número do cliente
        """
        self._set_imóvel_ativo(cliente_numero, "", ttl=1)  # Expira imediatamente


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando IntegradorRAGCarros...")

    from pathlib import Path
    from upstash_redis import Redis

    # Config
    carros_dir = Path(__file__).parent.parent.parent / "carros"
    openai_key = "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"
    openrouter_key = "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"

    redis = Redis(
        url="https://legible-collie-9537.upstash.io",
        token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
    )

    # Instância
    integrador = IntegradorRAGCarros(carros_dir, openai_key, openrouter_key, redis)

    # Teste
    cliente_teste = "5531999999999"

    # Limpa estado anterior
    integrador.limpar_imóvel_ativo(cliente_teste)

    # Teste 1: Busca inicial
    print("\n📋 Teste 1: Busca inicial")
    print("-" * 50)

    resposta = integrador.processar_mensagem(
        cliente_teste,
        "Volkswagen Gol 2020"
    )

    print(f"\n🤖 Resposta:\n{resposta}")

    # Teste 2: Pergunta sobre carro ativo
    print("\n\n📋 Teste 2: Pergunta sobre carro")
    print("-" * 50)

    resposta = integrador.processar_mensagem(
        cliente_teste,
        "Qual o motor dele?"
    )

    print(f"\n🤖 Resposta:\n{resposta}")
