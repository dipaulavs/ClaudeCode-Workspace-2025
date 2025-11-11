"""
Integrador Score - Pipeline completo
Executa score + tags + origem em cada mensagem
Com análise IA opcional (fallback para palavras-chave)

v2.0 - Sistema de tags migrado para Redis puro (Upstash)
"""
import json
from typing import Dict, Any, Optional
from .sistema_score import SistemaScore
from .redis_tags import RedisTagsSimples  # NOVO: Redis puro
from .deteccao_origem import DeteccaoOrigem
from .analisador_ia import AnalisadorLeadIA


class IntegradorScore:
    """
    Pipeline completo de score + tags + origem

    Executa em CADA mensagem:
    1. Detectar origem (se primeira mensagem)
    2. Calcular delta de score
    3. Detectar tags da mensagem
    4. Aplicar tags no Chatwoot
    5. Atualizar custom attributes
    """

    def __init__(self, redis_client, chatwoot_config: Dict[str, Any], usar_ia: bool = True):
        """
        Inicializa integrador

        Args:
            redis_client: Cliente Redis configurado (upstash_redis.Redis)
            chatwoot_config: Config do Chatwoot
            usar_ia: True para usar Claude IA, False para keywords apenas
        """
        self.redis = redis_client
        self.chatwoot_config = chatwoot_config
        self.usar_ia = usar_ia

        # Inicializar componentes
        self.score = SistemaScore(redis_client)
        self.tags = RedisTagsSimples(redis_client)  # NOVO: Redis puro
        self.origem = DeteccaoOrigem(redis_client, None)  # Origem não precisa de tags

        # Inicializar IA (com fallback se não disponível)
        try:
            self.analisador_ia = AnalisadorLeadIA()
            print("✅ AnalisadorLeadIA inicializado")
        except Exception as e:
            print(f"⚠️ Não foi possível inicializar IA: {e}")
            self.analisador_ia = None

    def processar_mensagem(
        self,
        cliente_numero: str,
        mensagem: str,
        eh_primeira_msg: bool = False,
        link_params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executa pipeline completo para uma mensagem

        Args:
            cliente_numero: Número do cliente (ex: 5531980160822)
            mensagem: Texto da mensagem
            eh_primeira_msg: True se primeira mensagem do cliente
            link_params: Parâmetros UTM (se houver)

        Returns:
            Dict com resultado: {
                "score": 75,
                "classificacao": "QUENTE",
                "tags_aplicadas": ["interessado", "visual"],
                "delta": 10,
                "origem": "facebook",
                "analise_ia": { ... }  # Incluído se usar_ia=True
            }
        """
        resultado = {
            "score": 0,
            "classificacao": "FRIO",
            "tags_aplicadas": [],
            "delta": 0,
            "origem": None,
            "analise_ia": None
        }

        try:
            # 1. Se primeira mensagem, detectar origem
            if eh_primeira_msg:
                origem_data = self.origem.extrair_origem_inicial(mensagem, link_params)
                if origem_data:
                    self.origem.salvar_origem(cliente_numero, origem_data)
                    self.origem.aplicar_tags_origem(cliente_numero)
                    resultado["origem"] = origem_data.get("utm_source")

            # 2. Buscar estado do cliente
            estado = self._get_estado_cliente(cliente_numero)

            # 3. Analisar com IA (se habilitado)
            analise_ia = None
            if self.usar_ia and self.analisador_ia:
                analise_ia = self._analisar_com_ia(cliente_numero, mensagem, estado)
                resultado["analise_ia"] = analise_ia

            # 4. Calcular delta de score (IA + keywords ou apenas keywords)
            if analise_ia and analise_ia.get("ia_usado"):
                # Usar score da IA como principal
                delta = analise_ia.get("score", 0) - self.score.get_score(cliente_numero)
                delta = max(0, delta)  # Apenas aumentar ou manter
            else:
                # Fallback para keywords
                delta = self.score.calcular_delta(mensagem, estado)

            resultado["delta"] = delta

            # 5. Atualizar score
            if delta > 0:
                novo_score = self.score.atualizar_score(cliente_numero, delta)
                self._salvar_estado_cliente(cliente_numero, estado)
            else:
                novo_score = self.score.get_score(cliente_numero)

            resultado["score"] = novo_score
            resultado["classificacao"] = self.score.classificar_lead(novo_score)

            # 6. Atualizar tags automaticamente (Redis)
            tags_resultado = self.tags.atualizar_tags_automaticas(
                cliente_numero,
                mensagem,
                novo_score
            )

            resultado["tags_aplicadas"] = tags_resultado["tags_adicionadas"]
            resultado["tags_removidas"] = tags_resultado.get("tags_removidas", [])

            # 8. Log de tags aplicadas
            tags_atuais = self.tags.obter_tags(cliente_numero)
            print(f"   Tags: {tags_atuais}", flush=True)

            modo_ia = " (IA)" if analise_ia and analise_ia.get("ia_usado") else ""
            print(f"✅ Pipeline executado para {cliente_numero}: Score {novo_score} ({resultado['classificacao']}){modo_ia}")

            return resultado

        except Exception as e:
            print(f"❌ Erro no pipeline de score: {e}")
            return resultado

    def _get_estado_cliente(self, cliente_numero: str) -> Dict[str, Any]:
        """
        Busca estado do cliente no Redis

        Args:
            cliente_numero: Número do cliente

        Returns:
            Dict com estado
        """
        estado_key = f"estado:{cliente_numero}"
        estado_raw = self.redis.get(estado_key)

        if estado_raw:
            return json.loads(estado_raw)

        # Estado inicial
        return {
            "tem_tipo_definido": False,
            "tem_regiao_definida": False,
            "tem_orcamento_definido": False,
            "pediu_fotos": False,
            "fez_perguntas": False,
            "mencionou_prazo": False,
            "respondeu_rapido": False,
            "tem_urgencia": None,
            "ultima_mensagem_timestamp": None
        }

    def _salvar_estado_cliente(self, cliente_numero: str, estado: Dict[str, Any]):
        """
        Salva estado do cliente no Redis

        Args:
            cliente_numero: Número do cliente
            estado: Dict com estado
        """
        estado_key = f"estado:{cliente_numero}"
        self.redis.set(estado_key, json.dumps(estado))


    def _analisar_com_ia(self, cliente_numero: str, mensagem: str, estado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa mensagem com Claude IA

        Args:
            cliente_numero: Número do cliente
            mensagem: Texto da mensagem
            estado: Estado atual do cliente

        Returns:
            Dict com análise IA ou fallback
        """
        if not self.analisador_ia:
            return None

        # Preparar contexto do cliente
        score_atual = self.score.get_score(cliente_numero)
        contexto = {
            "score_atual": score_atual,
            "tem_interesse": estado.get("fez_perguntas", False),
            "pediu_fotos": estado.get("pediu_fotos", False),
            "mencionou_prazo": estado.get("mencionou_prazo", False)
        }

        # Analisar
        analise = self.analisador_ia.analisar(mensagem, contexto)

        # Salvar análise no Redis para auditoria
        try:
            analise_key = f"analise_ia:{cliente_numero}"
            self.redis.lpush(analise_key, json.dumps(analise))
            self.redis.ltrim(analise_key, 0, 19)  # Manter últimas 20
        except Exception as e:
            print(f"⚠️ Erro ao salvar análise IA no Redis: {e}")

        return analise

    def get_resumo_cliente(self, cliente_numero: str) -> Dict[str, Any]:
        """
        Retorna resumo completo do cliente

        Args:
            cliente_numero: Número do cliente

        Returns:
            Dict com resumo completo
        """
        try:
            # Score
            score = self.score.get_score(cliente_numero)
            classificacao = self.score.classificar_lead(score)
            historico_score = self.score.get_historico(cliente_numero, limit=5)

            # Origem
            origem = self.origem.get_origem(cliente_numero)

            # Tags (Redis)
            tags = list(self.tags.obter_tags(cliente_numero))

            # Estado
            estado = self._get_estado_cliente(cliente_numero)

            return {
                "score": score,
                "classificacao": classificacao,
                "historico_score": historico_score,
                "origem": origem,
                "tags": tags,
                "estado": estado
            }

        except Exception as e:
            print(f"❌ Erro ao buscar resumo do cliente: {e}")
            return {}

    def reset_cliente(self, cliente_numero: str):
        """
        Reseta dados do cliente (usar com cuidado)

        Args:
            cliente_numero: Número do cliente
        """
        # Reset score
        self.score.reset_score(cliente_numero)

        # Reset estado
        estado_key = f"estado:{cliente_numero}"
        self.redis.delete(estado_key)

        # Reset origem
        origem_key = f"origem:{cliente_numero}"
        self.redis.delete(origem_key)

        # Reset tags Redis
        self.tags.limpar_tags(cliente_numero)

        print(f"✅ Cliente {cliente_numero} resetado")

    def get_estatisticas(self) -> Dict[str, Any]:
        """
        Retorna estatísticas gerais

        Returns:
            Dict com estatísticas
        """
        try:
            stats = {
                "total_leads": 0,
                "leads_quentes": 0,
                "leads_mornos": 0,
                "leads_frios": 0,
                "score_medio": 0,
                "origens": {},
                "imoveis_mais_procurados": []
            }

            # Scan de scores
            scores = []
            for key in self.redis.scan_iter(match="score:*"):
                score = int(self.redis.get(key) or 0)
                scores.append(score)

                # Classificar
                if score >= 70:
                    stats["leads_quentes"] += 1
                elif score >= 40:
                    stats["leads_mornos"] += 1
                else:
                    stats["leads_frios"] += 1

            stats["total_leads"] = len(scores)
            if scores:
                stats["score_medio"] = sum(scores) / len(scores)

            # Origens
            for key in self.redis.scan_iter(match="origem:*"):
                origem_raw = self.redis.get(key)
                if origem_raw:
                    origem_data = json.loads(origem_raw)
                    utm_source = origem_data.get("utm_source", "direto")
                    stats["origens"][utm_source] = stats["origens"].get(utm_source, 0) + 1

            # Imóveis mais procurados
            stats["imoveis_mais_procurados"] = self.origem.get_imoveis_mais_procurados(limit=5)

            return stats

        except Exception as e:
            print(f"❌ Erro ao buscar estatísticas: {e}")
            return {}
