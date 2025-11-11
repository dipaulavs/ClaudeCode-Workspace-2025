#!/usr/bin/env python3
"""
🎯 RAG SIMPLES - Arquitetura Simplificada

ARQUITETURA:
┌─────────────────┐
│ Agente Principal│ ← Personalidade curta
└────────┬────────┘
         │ precisa info?
         ↓
┌─────────────────┐
│  Sub-agente FAQ │ ← Busca base.txt + faq.txt
└─────────────────┘
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Adiciona path das ferramentas
sys.path.append(str(Path(__file__).parent.parent / "ferramentas"))

from lista_imoveis import listar_imoveis_disponiveis, formatar_lista_para_mensagem
from consulta_faq import consultar_faq_imovel
from tagueamento import obter_imovel_ativo, taguear_cliente

# Importa novos componentes
from componentes.agente_principal_simples import AgentePrincipalSimples
from componentes.subagente_faq import SubAgenteFAQ

# Importa Matcher e Tagger Dinâmico (opcionais)
try:
    from componentes.matcher_imoveis import MatcherImoveis
except ImportError:
    MatcherImoveis = None

try:
    from componentes.tagger_dinamico import TaggerDinamico
except ImportError:
    TaggerDinamico = None


class RAGSimplesImoveis:
    """
    Orquestrador que coordena Agente Principal + Sub-agente FAQ
    """

    def __init__(
        self,
        imoveis_dir,
        openai_api_key,
        openrouter_api_key,
        redis_client,
        chatwoot_config: Optional[Dict] = None,
        enable_auto_matching: bool = True,
        matcher_score_threshold: float = 70.0
    ):
        self.imoveis_dir = imoveis_dir
        self.openai_key = openai_api_key
        self.openrouter_key = openrouter_api_key
        self.redis = redis_client
        self.chatwoot_config = chatwoot_config or {}
        self.enable_auto_matching = enable_auto_matching
        self.matcher_score_threshold = matcher_score_threshold

        # Carrega personalidade
        personalidade_file = Path(__file__).parent.parent / "personalidade.txt"
        with open(personalidade_file, 'r', encoding='utf-8') as f:
            personalidade = f.read().strip()

        # Inicializa agentes
        config = {
            "openrouter_api_key": openrouter_api_key
        }
        self.agente_principal = AgentePrincipalSimples(personalidade, redis_client, config)
        self.subagente_faq = SubAgenteFAQ(imoveis_dir)

        # Inicializa componentes opcionais (Matcher + Tagger)
        self.matcher = None
        self.tagger = None

        if enable_auto_matching and MatcherImoveis is not None:
            try:
                self.matcher = MatcherImoveis(imoveis_dir, redis_client)
                print("✅ Matcher de imóveis inicializado", flush=True)
            except Exception as e:
                print(f"⚠️ Aviso: Matcher não inicializado ({e})", flush=True)

        if enable_auto_matching and TaggerDinamico is not None and chatwoot_config:
            try:
                self.tagger = TaggerDinamico(redis_client, chatwoot_config)
                print("✅ Tagger Dinâmico inicializado", flush=True)
            except Exception as e:
                print(f"⚠️ Aviso: Tagger não inicializado ({e})", flush=True)

        print("✅ RAGSimplesImoveis inicializado (Arquitetura Simplificada + Matcher/Tagger)", flush=True)

    def _tentar_auto_matching(
        self,
        numero_cliente: str,
        mensagem: str,
        contexto: list
    ) -> Optional[str]:
        """
        Tenta encontrar imóvel automaticamente se não houver ativo

        NOVO FLUXO:
        1. Matcher identifica melhor match
        2. Se score >= threshold → Tagger aplica tag
        3. Retorna imovel_id ou None

        Returns:
            imovel_id (str) ou None
        """
        if not self.enable_auto_matching:
            return None

        if self.matcher is None:
            return None

        try:
            print(f"   🔍 Auto-matching: Procurando imóvel match para mensagem...", flush=True)

            # Matcher encontra melhor match
            match = self.matcher.encontrar_melhor_match(
                mensagem=mensagem,
                contexto_cliente=contexto
            )

            if not match:
                print(f"   ⚠️ Nenhum match encontrado", flush=True)
                return None

            match_score = match.get('score_match', 0)

            # Verifica se match é forte o suficiente
            if match_score < self.matcher_score_threshold:
                print(
                    f"   ⚠️ Match score baixo ({match_score:.1f}% < {self.matcher_score_threshold}%)",
                    flush=True
                )
                return None

            imovel_id = match.get('imovel_id')
            print(
                f"   ✅ Match encontrado: {imovel_id} (score: {match_score:.1f}%)",
                flush=True
            )

            # Tagger aplica tag (melhor esforço)
            if self.tagger is not None and self.chatwoot_config:
                try:
                    resultado_tag = self.tagger.aplicar_tag_imovel(
                        numero_cliente=numero_cliente,
                        imovel_id=imovel_id,
                        contexto=match
                    )
                    if resultado_tag.get('sucesso'):
                        print(f"   ✅ Tag aplicada: {resultado_tag.get('tag')}", flush=True)
                    else:
                        print(f"   ⚠️ Falha ao aplicar tag (Redis salvo)", flush=True)
                except Exception as e:
                    print(f"   ⚠️ Erro no Tagger: {e}", flush=True)

            return imovel_id

        except Exception as e:
            print(f"   ❌ Erro no auto-matching: {e}", flush=True)
            return None

    def processar_mensagem(self, numero_cliente: str, mensagem: str, contexto: list) -> str:
        """
        Processa mensagem usando Agente Principal + Sub-agente FAQ

        FLUXO ORIGINAL:
        1. Agente Principal decide se precisa info
        2. Se SIM → chama Sub-agente FAQ
        3. Sub-agente retorna dados
        4. Agente Principal responde cliente

        NOVO (com Matcher + Tagger):
        - Se sem imóvel ativo → tenta auto-matching
        - Se encontrar → aplica tag + continua
        """
        import requests
        import json

        # Verifica imóvel ativo
        imovel_ativo = obter_imovel_ativo(numero_cliente, self.redis)

        # ═══════════════════════════════════════════
        # NOVO: Tenta auto-matching se sem imóvel
        # ═══════════════════════════════════════════
        if not imovel_ativo and self.enable_auto_matching:
            imovel_encontrado = self._tentar_auto_matching(
                numero_cliente,
                mensagem,
                contexto
            )
            if imovel_encontrado:
                imovel_ativo = imovel_encontrado
                # Salva no Redis (redundância)
                try:
                    chave_redis = f"carro_ativo:automaia:{numero_cliente}"
                    self.redis.setex(chave_redis, 86400, imovel_ativo)
                    print(f"   ✅ Imóvel ativo salvo em Redis: {imovel_ativo}", flush=True)
                except Exception as e:
                    print(f"   ⚠️ Erro ao salvar em Redis: {e}", flush=True)

        # ═══════════════════════════════════════════
        # PASSO 1: Agente Principal processa
        # ═══════════════════════════════════════════
        resultado_agente = self.agente_principal.processar(
            mensagem=mensagem,
            contexto=contexto,
            numero_cliente=numero_cliente,
            imovel_ativo=imovel_ativo
        )

        # ═══════════════════════════════════════════
        # PASSO 2: Verifica se precisa sub-agente
        # ═══════════════════════════════════════════
        if isinstance(resultado_agente, dict) and resultado_agente.get('tipo') == 'chamar_subagente':
            print("   🔍 Chamando Sub-agente FAQ...", flush=True)

            # Verifica se tem imóvel ativo
            if not imovel_ativo:
                return "⚠️ Você ainda não escolheu um imóvel. Qual imóvel te interessa?"

            # Sub-agente busca informações
            args = resultado_agente['args']
            resultado_faq = self.subagente_faq.consultar(
                imovel_id=imovel_ativo,  # Usa o imóvel ativo ao invés do args
                pergunta=args.get('pergunta', '')
            )

            if not resultado_faq['sucesso']:
                return f"⚠️ {resultado_faq['erro']}"

            # ═══════════════════════════════════════════
            # PASSO 3: Agente Principal gera resposta final
            # ═══════════════════════════════════════════
            mensagens = resultado_agente['mensagens']
            mensagens.append(resultado_agente['message'])
            mensagens.append({
                "role": "tool",
                "tool_call_id": resultado_agente['tool_call']['id'],
                "content": resultado_faq['dados']
            })

            # Chama Claude novamente com dados do FAQ
            try:
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.openrouter_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "anthropic/claude-haiku-4.5",
                    "messages": mensagens,
                    "temperature": 0.9,
                    "max_tokens": 500
                }

                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()

                resultado = response.json()
                resposta = resultado['choices'][0]['message']['content'].strip()
                return resposta

            except Exception as e:
                print(f"❌ Erro na resposta final: {e}", flush=True)
                return "Desculpa, tive um problema ao processar a informação. 😊"

        # ═══════════════════════════════════════════
        # RESPOSTA DIRETA (sem sub-agente)
        # ═══════════════════════════════════════════
        elif isinstance(resultado_agente, dict) and resultado_agente.get('tipo') == 'resposta_direta':
            return resultado_agente['texto']

        # ═══════════════════════════════════════════
        # ERRO
        # ═══════════════════════════════════════════
        elif isinstance(resultado_agente, dict) and resultado_agente.get('tipo') == 'erro':
            return resultado_agente['texto']

        else:
            return "Desculpa, não entendi. Pode reformular? 😊"

    def configurar_matching(
        self,
        enable: bool = True,
        score_threshold: float = 70.0
    ) -> None:
        """
        Configura comportamento de auto-matching em tempo de execução

        Args:
            enable: Se True, ativa matching automático
            score_threshold: Score mínimo (0-100) para aceitar match
        """
        self.enable_auto_matching = enable
        self.matcher_score_threshold = score_threshold
        status = "ativado" if enable else "desativado"
        print(
            f"⚙️ Auto-matching {status} (threshold: {score_threshold}%)",
            flush=True
        )

    def obter_status_matching(self) -> Dict[str, Any]:
        """
        Retorna status dos componentes Matcher e Tagger

        Returns:
            Dict com:
            - enable_auto_matching: bool
            - matcher_score_threshold: float
            - matcher_disponivel: bool
            - tagger_disponivel: bool
        """
        return {
            "enable_auto_matching": self.enable_auto_matching,
            "matcher_score_threshold": self.matcher_score_threshold,
            "matcher_disponivel": self.matcher is not None,
            "tagger_disponivel": self.tagger is not None
        }


if __name__ == "__main__":
    print("🧪 RAGSimplesImoveis - Adapter para Orquestrador")
    print("Este módulo deve ser importado pelo chatbot_imobili-ria-premium_v4.py")
