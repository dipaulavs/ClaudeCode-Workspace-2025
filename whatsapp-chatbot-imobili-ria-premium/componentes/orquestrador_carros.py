#!/usr/bin/env python3
"""
🎯 ORQUESTRADOR CARROS - Framework Híbrido Completo

Combina TODOS os componentes:
- RAG Simples (3 ferramentas)
- Score + Tags + Origem
- Follow-ups Anti-Abandono
- Escalonamento Inteligente
- Métricas e Relatórios
"""

import json
from datetime import datetime
from typing import Dict, List
from pathlib import Path

# RAG Simples
try:
    from componentes.rag_simples_carros import RAGSimplesCarros
    RAG_DISPONIVEL = True
except ImportError:
    print("⚠️  RAG Simples não disponível")
    RAG_DISPONIVEL = False

# Score
try:
    from componentes.score import IntegradorScore
    SCORE_DISPONIVEL = True
except ImportError:
    print("⚠️  Score não disponível")
    SCORE_DISPONIVEL = False

# Follow-up
try:
    from componentes.followup import IntegradorFollowUp
    FOLLOWUP_DISPONIVEL = True
except ImportError:
    print("⚠️  Follow-up não disponível")
    FOLLOWUP_DISPONIVEL = False

# Escalonamento
try:
    from componentes.escalonamento import IntegradorEscalonamento
    ESCALONAMENTO_DISPONIVEL = True
except ImportError:
    print("⚠️  Escalonamento não disponível")
    ESCALONAMENTO_DISPONIVEL = False

# Métricas
try:
    from componentes.relatorios import IntegradorMetricas
    METRICAS_DISPONIVEL = True
except ImportError:
    print("⚠️  Métricas não disponível")
    METRICAS_DISPONIVEL = False


class OrquestradorCarros:
    """
    Orquestrador adaptado para carros
    """

    def __init__(self, carros_dir, openai_api_key, openrouter_api_key, redis_client, config):
        self.redis = redis_client
        self.config = config

        print("\n🎯 Inicializando Orquestrador Carros...", flush=True)

        # RAG Simples
        if RAG_DISPONIVEL:
            try:
                self.rag = RAGSimplesCarros(
                    carros_dir,
                    openai_api_key,
                    openrouter_api_key,
                    redis_client
                )
                print("✅ RAG Simples inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro RAG: {e}", flush=True)
                self.rag = None
        else:
            self.rag = None

        # Score
        if SCORE_DISPONIVEL:
            try:
                # Score espera chatwoot_config (não config completo)
                self.score = IntegradorScore(redis_client, config.get('chatwoot', config))
                print("✅ Score inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro Score: {e}", flush=True)
                import traceback
                traceback.print_exc()
                self.score = None
        else:
            self.score = None

        # Follow-up
        if FOLLOWUP_DISPONIVEL:
            try:
                # Follow-up espera config completo
                self.followup = IntegradorFollowUp(redis_client, config)
                print("✅ Follow-up inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro Follow-up: {e}", flush=True)
                import traceback
                traceback.print_exc()
                self.followup = None
        else:
            self.followup = None

        # Escalonamento
        if ESCALONAMENTO_DISPONIVEL:
            try:
                # Escalonamento espera config completo
                self.escalonamento = IntegradorEscalonamento(redis_client, config)
                print("✅ Escalonamento inicializado", flush=True)
            except Exception as e:
                print(f"⚠️  Erro Escalonamento: {e}", flush=True)
                import traceback
                traceback.print_exc()
                self.escalonamento = None
        else:
            self.escalonamento = None

        # Métricas
        if METRICAS_DISPONIVEL:
            try:
                self.metricas = IntegradorMetricas(redis_client)
                print("✅ Métricas inicializadas", flush=True)
            except Exception as e:
                print(f"⚠️  Erro Métricas: {e}", flush=True)
                self.metricas = None
        else:
            self.metricas = None

        print("🎉 Orquestrador Carros pronto!\n", flush=True)

    def processar_mensagem(
        self,
        numero_cliente: str,
        mensagem: str,
        contexto: List[Dict],
        eh_primeira_msg: bool = False
    ) -> Dict:
        """
        Pipeline completo de processamento
        """
        print(f"\n{'='*80}", flush=True)
        print(f"🎯 ORQUESTRADOR CARROS - {datetime.now().strftime('%H:%M:%S')}", flush=True)
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

        # 1. MÉTRICAS: Nova conversa
        if eh_primeira_msg and self.metricas:
            try:
                self.metricas.on_nova_conversa(numero_cliente)
                print("📊 Nova conversa registrada", flush=True)
            except Exception as e:
                print(f"⚠️  Erro métricas: {e}", flush=True)

        # 2. SCORE: Processar mensagem
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

                # Lead quente
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
                    resultado["deve_escalonar"] = True
                    resultado["resposta"] = resposta_escalonamento

                    print(f"🔺 ESCALONAMENTO ATIVADO!", flush=True)

                    if self.metricas:
                        self.metricas.on_escalamento(numero_cliente)

                    if self.followup:
                        self.followup.on_mensagem_cliente_recebida(numero_cliente, mensagem)

                    return resultado
            except Exception as e:
                print(f"⚠️  Erro escalonamento: {e}", flush=True)

        # 4. RAG: Processar com IA
        if self.rag:
            try:
                resposta_rag = self.rag.processar_mensagem(
                    numero_cliente,
                    mensagem,
                    contexto
                )
                resultado["resposta"] = resposta_rag

                print(f"🤖 RAG respondeu ({len(resposta_rag)} chars)", flush=True)

                # Detecta se enviou fotos
                if "[ENVIAR_FOTOS:" in resposta_rag:
                    import re
                    match = re.search(r'\[ENVIAR_FOTOS:([^\]]+)\]', resposta_rag)
                    if match:
                        carro_id = match.group(1)
                        resultado["resposta"] = resposta_rag.replace(f"[ENVIAR_FOTOS:{carro_id}]", "").strip()

                        # Busca fotos do carro
                        from ferramentas.tagueamento import obter_carro_ativo
                        carro_path = Path(__file__).parent.parent / "carros" / carro_id
                        links_file = carro_path / "links.json"

                        if links_file.exists():
                            import json
                            with open(links_file, 'r') as f:
                                links_data = json.load(f)
                                fotos = links_data.get("fotos", [])
                                resultado["fotos"] = [f["link"] for f in fotos[:5]]
                                print(f"📸 {len(resultado['fotos'])} fotos serão enviadas", flush=True)

                                if self.metricas:
                                    self.metricas.on_imovel_visualizado(numero_cliente, carro_id)
            except Exception as e:
                print(f"⚠️  Erro RAG: {e}", flush=True)
                resultado["resposta"] = "Desculpa, tive um problema. Pode repetir? 😊"
        else:
            resultado["resposta"] = "Olá! Como posso ajudar? 😊"

        # 5. FOLLOW-UP: Cancelar anteriores (cliente ativo)
        if self.followup:
            try:
                self.followup.on_mensagem_cliente_recebida(numero_cliente, mensagem)
                print(f"✅ Follow-ups cancelados", flush=True)
            except Exception as e:
                print(f"⚠️  Erro follow-up: {e}", flush=True)

        # 6. MÉTRICAS: Bot respondeu
        if self.metricas:
            try:
                self.metricas.on_bot_respondeu(numero_cliente)
            except Exception as e:
                print(f"⚠️  Erro métricas: {e}", flush=True)

        print(f"\n{'='*80}", flush=True)
        print(f"✅ ORQUESTRADOR CONCLUÍDO", flush=True)
        print(f"{'='*80}\n", flush=True)

        return resultado

    def on_bot_enviou_mensagem(self, numero_cliente: str, mensagem: str):
        """Callback: Bot enviou mensagem"""
        if self.followup:
            try:
                self.followup.on_mensagem_bot_enviada(numero_cliente)
                print(f"📅 Follow-up agendado (2h)", flush=True)
            except Exception as e:
                print(f"⚠️  Erro follow-up: {e}", flush=True)

    def on_fotos_enviadas(self, numero_cliente: str, carro_id: str, quantidade: int):
        """Callback: Fotos enviadas"""
        if self.followup:
            try:
                self.followup.on_fotos_enviadas(numero_cliente, carro_id, quantidade)
                print(f"📅 Follow-up pós-fotos agendado (1h)", flush=True)
            except Exception as e:
                print(f"⚠️  Erro follow-up: {e}", flush=True)

    def get_status(self) -> Dict:
        """Status de todos componentes"""
        return {
            "rag": "✅" if self.rag else "❌",
            "score": "✅" if self.score else "❌",
            "followup": "✅" if self.followup else "❌",
            "escalonamento": "✅" if self.escalonamento else "❌",
            "metricas": "✅" if self.metricas else "❌"
        }
