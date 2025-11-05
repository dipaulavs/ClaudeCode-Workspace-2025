#!/usr/bin/env python3
"""
🎯 ORQUESTRADOR INTELIGENTE - Framework Híbrido

Combina TODOS os componentes em um pipeline único:
- RAG + Progressive Disclosure
- Score + Tags + Origem
- Follow-ups Anti-Abandono
- Escalonamento Inteligente
- Métricas e Relatórios

Autor: Claude Code
Data: 04/11/2025
Versão: 1.0
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Imports dos componentes
try:
    from componentes.rag import IntegradorRAG
    RAG_DISPONIVEL = True
except ImportError:
    print("⚠️  RAG não disponível")
    RAG_DISPONIVEL = False

try:
    from componentes.score import IntegradorScore
    SCORE_DISPONIVEL = True
except ImportError:
    print("⚠️  Score não disponível")
    SCORE_DISPONIVEL = False

try:
    from componentes.followup import IntegradorFollowUp
    FOLLOWUP_DISPONIVEL = True
except ImportError:
    print("⚠️  Follow-up não disponível")
    FOLLOWUP_DISPONIVEL = False

try:
    from componentes.escalonamento import IntegradorEscalonamento
    ESCALONAMENTO_DISPONIVEL = True
except ImportError:
    print("⚠️  Escalonamento não disponível")
    ESCALONAMENTO_DISPONIVEL = False

try:
    from componentes.relatorios import IntegradorMetricas
    METRICAS_DISPONIVEL = True
except ImportError:
    print("⚠️  Métricas não disponível")
    METRICAS_DISPONIVEL = False


class OrquestradorInteligente:
    """
    Orquestrador que decide qual componente usar em cada momento
    """

    def __init__(self, imoveis_dir, openai_api_key, openrouter_api_key, redis_client, config):
        """
        Inicializa orquestrador com todos os componentes

        Args:
            imoveis_dir: Path para diretório de imóveis
            openai_api_key: Chave API OpenAI
            openrouter_api_key: Chave API OpenRouter
            redis_client: Cliente Redis configurado
            config: Dict com configurações do Chatwoot/Evolution
        """
        self.redis = redis_client
        self.config = config

        print("\n🎯 Inicializando Orquestrador Inteligente...", flush=True)

        # Inicializa RAG
        if RAG_DISPONIVEL:
            try:
                self.rag = IntegradorRAG(
                    imoveis_dir,
                    openai_api_key,
                    openrouter_api_key,
                    redis_client
                )
                print("✅ RAG inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar RAG: {e}", flush=True)
                self.rag = None
        else:
            self.rag = None

        # Inicializa Score
        if SCORE_DISPONIVEL:
            try:
                self.score = IntegradorScore(redis_client, config)
                print("✅ Score inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar Score: {e}", flush=True)
                self.score = None
        else:
            self.score = None

        # Inicializa Follow-up
        if FOLLOWUP_DISPONIVEL:
            try:
                self.followup = IntegradorFollowUp(redis_client, config)
                print("✅ Follow-up inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar Follow-up: {e}", flush=True)
                self.followup = None
        else:
            self.followup = None

        # Inicializa Escalonamento
        if ESCALONAMENTO_DISPONIVEL:
            try:
                self.escalonamento = IntegradorEscalonamento(redis_client, config)
                print("✅ Escalonamento inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar Escalonamento: {e}", flush=True)
                self.escalonamento = None
        else:
            self.escalonamento = None

        # Inicializa Métricas
        if METRICAS_DISPONIVEL:
            try:
                self.metricas = IntegradorMetricas(redis_client)
                print("✅ Métricas inicializadas", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar Métricas: {e}", flush=True)
                self.metricas = None
        else:
            self.metricas = None

        print("🎉 Orquestrador pronto!\n", flush=True)

    def processar_mensagem(
        self,
        numero_cliente: str,
        mensagem: str,
        contexto: List[Dict],
        eh_primeira_msg: bool = False
    ) -> Dict:
        """
        Pipeline completo de processamento

        Args:
            numero_cliente: Número do cliente (formato: 5531980160822)
            mensagem: Mensagem do cliente
            contexto: Lista de mensagens anteriores
            eh_primeira_msg: Se é a primeira mensagem da conversa

        Returns:
            Dict com:
                - resposta: Texto da resposta para o cliente
                - fotos: Lista de URLs de fotos (se houver)
                - deve_escalonar: Bool indicando se deve escalonar
                - score: Score atual do cliente
                - tags: Tags aplicadas
        """
        print(f"\n{'='*80}", flush=True)
        print(f"🎯 ORQUESTRADOR - {datetime.now().strftime('%H:%M:%S')}", flush=True)
        print(f"{'='*80}", flush=True)
        print(f"📱 Cliente: {numero_cliente}", flush=True)
        print(f"💬 Mensagem: {mensagem[:100]}...", flush=True)
        print(f"🆕 Primeira msg: {eh_primeira_msg}", flush=True)

        resultado = {
            "resposta": "",
            "fotos": [],
            "deve_escalonar": False,
            "score": 0,
            "tags": [],
            "classificacao": "FRIO"
        }

        # 1. MÉTRICAS: Registrar nova conversa
        if eh_primeira_msg and self.metricas:
            try:
                self.metricas.on_nova_conversa(numero_cliente)
                print("📊 Métrica: Nova conversa registrada", flush=True)
            except Exception as e:
                print(f"⚠️  Erro métricas (nova conversa): {e}", flush=True)

        # 2. SCORE: Processar mensagem (primeira msg = origem)
        if self.score:
            try:
                score_result = self.score.processar_mensagem(
                    numero_cliente,
                    mensagem,
                    eh_primeira_msg
                )
                resultado["score"] = score_result.get("score", 0)
                resultado["tags"] = score_result.get("tags_aplicadas", [])
                resultado["classificacao"] = score_result.get("classificacao", "FRIO")

                print(f"📊 Score: {resultado['score']} ({resultado['classificacao']})", flush=True)
                print(f"🏷️  Tags: {resultado['tags']}", flush=True)

                # Métricas: Lead quente
                if self.metricas and resultado["score"] >= 70:
                    self.metricas.on_lead_quente(numero_cliente, resultado["score"])
            except Exception as e:
                print(f"⚠️  Erro score: {e}", flush=True)

        # 3. ESCALONAMENTO: Verificar se deve escalonar
        if self.escalonamento:
            try:
                resposta_escalonamento = self.escalonamento.processar_mensagem(
                    numero_cliente,
                    mensagem,
                    resultado["score"]
                )

                if resposta_escalonamento:
                    # Deve escalonar!
                    resultado["deve_escalonar"] = True
                    resultado["resposta"] = resposta_escalonamento

                    print(f"🔺 ESCALONAMENTO ATIVADO!", flush=True)

                    # Métricas: Escalamento
                    if self.metricas:
                        self.metricas.on_escalamento(numero_cliente)

                    # Cancela follow-ups (corretor assume)
                    if self.followup:
                        self.followup.on_mensagem_cliente_recebida(numero_cliente, mensagem)

                    return resultado
            except Exception as e:
                print(f"⚠️  Erro escalonamento: {e}", flush=True)

        # 4. RAG: Processar mensagem com IA
        if self.rag:
            try:
                resposta_rag = self.rag.processar_mensagem(
                    numero_cliente,
                    mensagem,
                    contexto
                )
                resultado["resposta"] = resposta_rag

                print(f"🤖 RAG respondeu ({len(resposta_rag)} chars)", flush=True)

                # Detecta se enviou fotos (comando [ENVIAR_FOTOS:id])
                if "[ENVIAR_FOTOS:" in resposta_rag:
                    import re
                    match = re.search(r'\[ENVIAR_FOTOS:([^\]]+)\]', resposta_rag)
                    if match:
                        imovel_id = match.group(1)
                        # Remove comando da resposta
                        resultado["resposta"] = resposta_rag.replace(f"[ENVIAR_FOTOS:{imovel_id}]", "").strip()

                        # Busca fotos do imóvel
                        imovel = self.rag.busca.imoveis_database.get(imovel_id)
                        if imovel and imovel.get("fotos"):
                            resultado["fotos"] = [f["link"] for f in imovel["fotos"][:5]]
                            print(f"📸 {len(resultado['fotos'])} fotos serão enviadas", flush=True)

                            # Métricas: Fotos enviadas
                            if self.metricas:
                                self.metricas.on_imovel_visualizado(numero_cliente, imovel_id)
            except Exception as e:
                print(f"⚠️  Erro RAG: {e}", flush=True)
                # Fallback: resposta genérica
                resultado["resposta"] = "Desculpe, tive um problema ao processar sua mensagem. Pode repetir?"
        else:
            # Sem RAG: resposta genérica
            resultado["resposta"] = "Olá! Como posso ajudar você hoje? 😊"

        # 5. FOLLOW-UP: Agendar follow-up de inatividade
        if self.followup:
            try:
                # Cancela follow-ups anteriores (cliente está ativo)
                self.followup.on_mensagem_cliente_recebida(numero_cliente, mensagem)

                print(f"✅ Follow-ups anteriores cancelados", flush=True)
            except Exception as e:
                print(f"⚠️  Erro follow-up: {e}", flush=True)

        # 6. MÉTRICAS: Bot respondeu
        if self.metricas:
            try:
                self.metricas.on_bot_respondeu(numero_cliente)
            except Exception as e:
                print(f"⚠️  Erro métricas (bot respondeu): {e}", flush=True)

        print(f"\n{'='*80}", flush=True)
        print(f"✅ ORQUESTRADOR CONCLUÍDO", flush=True)
        print(f"{'='*80}\n", flush=True)

        return resultado

    def on_bot_enviou_mensagem(self, numero_cliente: str, mensagem: str):
        """
        Callback: Bot acabou de enviar mensagem
        Agenda follow-up de inatividade
        """
        if self.followup:
            try:
                self.followup.on_mensagem_bot_enviada(numero_cliente)
                print(f"📅 Follow-up de inatividade agendado (2h)", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao agendar follow-up: {e}", flush=True)

    def on_fotos_enviadas(self, numero_cliente: str, imovel_id: str, quantidade: int):
        """
        Callback: Bot enviou fotos
        Agenda follow-up pós-fotos
        """
        if self.followup:
            try:
                self.followup.on_fotos_enviadas(numero_cliente, imovel_id, quantidade)
                print(f"📅 Follow-up pós-fotos agendado (1h)", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao agendar follow-up pós-fotos: {e}", flush=True)

    def on_visita_agendada(self, numero_cliente: str, data_hora_visita, imovel_id: str):
        """
        Callback: Visita foi agendada
        """
        # Follow-ups: Lembretes de visita
        if self.followup:
            try:
                self.followup.on_visita_agendada(numero_cliente, data_hora_visita, imovel_id)
                print(f"📅 Follow-ups de visita agendados (24h e 2h antes)", flush=True)
            except Exception as e:
                print(f"⚠️  Erro ao agendar follow-ups de visita: {e}", flush=True)

        # Métricas: Visita agendada
        if self.metricas:
            try:
                self.metricas.on_visita_agendada(numero_cliente, imovel_id)
            except Exception as e:
                print(f"⚠️  Erro métricas (visita agendada): {e}", flush=True)

    def get_status(self) -> Dict:
        """
        Retorna status de todos os componentes
        """
        return {
            "rag": "✅" if self.rag else "❌",
            "score": "✅" if self.score else "❌",
            "followup": "✅" if self.followup else "❌",
            "escalonamento": "✅" if self.escalonamento else "❌",
            "metricas": "✅" if self.metricas else "❌"
        }


if __name__ == "__main__":
    print("""
🎯 ORQUESTRADOR INTELIGENTE - Framework Híbrido

Este módulo deve ser importado pelo chatbot_corretor_v4.py

Uso:
    from componentes.orquestrador import OrquestradorInteligente

    orquestrador = OrquestradorInteligente(
        imoveis_dir,
        openai_api_key,
        openrouter_api_key,
        redis,
        config
    )

    resultado = orquestrador.processar_mensagem(
        numero_cliente="5531980160822",
        mensagem="Quero alugar apartamento 2 quartos",
        contexto=[],
        eh_primeira_msg=True
    )
    """)
