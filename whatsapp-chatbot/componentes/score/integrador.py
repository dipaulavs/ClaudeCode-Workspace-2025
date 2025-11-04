"""
Integrador Score - Pipeline completo
Executa score + tags + origem em cada mensagem
"""
import json
import redis
from typing import Dict, Any, Optional
from .sistema_score import SistemaScore
from .sistema_tags import SistemaTags
from .deteccao_origem import DeteccaoOrigem


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

    def __init__(self, redis_client: redis.Redis, chatwoot_config: Dict[str, Any]):
        """
        Inicializa integrador

        Args:
            redis_client: Cliente Redis configurado
            chatwoot_config: Config do Chatwoot
        """
        self.redis = redis_client
        self.chatwoot_config = chatwoot_config

        # Inicializar componentes
        self.score = SistemaScore(redis_client)
        self.tags = SistemaTags(redis_client, chatwoot_config)
        self.origem = DeteccaoOrigem(redis_client, self.tags)

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
                "origem": "facebook"
            }
        """
        resultado = {
            "score": 0,
            "classificacao": "FRIO",
            "tags_aplicadas": [],
            "delta": 0,
            "origem": None
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

            # 3. Calcular delta de score
            delta = self.score.calcular_delta(mensagem, estado)
            resultado["delta"] = delta

            # 4. Atualizar score
            if delta > 0:
                novo_score = self.score.atualizar_score(cliente_numero, delta)
                # Salvar estado atualizado
                self._salvar_estado_cliente(cliente_numero, estado)
            else:
                novo_score = self.score.get_score(cliente_numero)

            resultado["score"] = novo_score
            resultado["classificacao"] = self.score.classificar_lead(novo_score)

            # 5. Detectar tags da mensagem
            tags = self.tags.detectar_tags(mensagem, novo_score)
            resultado["tags_aplicadas"] = tags

            # 6. Aplicar tags no Chatwoot
            if tags:
                self.tags.aplicar_chatwoot(cliente_numero, tags)

            # 7. Atualizar custom attributes no Chatwoot
            self._atualizar_custom_attributes_chatwoot(cliente_numero, resultado)

            # 8. Remover tags obsoletas (ex: morno → quente)
            self._atualizar_tags_score(cliente_numero, resultado["classificacao"])

            print(f"✅ Pipeline executado para {cliente_numero}: Score {novo_score} ({resultado['classificacao']})")

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

    def _atualizar_custom_attributes_chatwoot(self, cliente_numero: str, resultado: Dict[str, Any]):
        """
        Atualiza custom attributes no Chatwoot

        Args:
            cliente_numero: Número do cliente
            resultado: Resultado do pipeline
        """
        custom_attrs = {
            "score": resultado["score"],
            "classificacao": resultado["classificacao"]
        }

        # Adicionar origem (se houver)
        origem_data = self.origem.get_origem(cliente_numero)
        if origem_data:
            custom_attrs["origem"] = origem_data.get("utm_source")
            if origem_data.get("imovel_id"):
                custom_attrs["imovel_interesse"] = origem_data.get("imovel_id")

        self.tags.atualizar_custom_attributes(cliente_numero, custom_attrs)

    def _atualizar_tags_score(self, cliente_numero: str, classificacao: str):
        """
        Atualiza tags de score (remove obsoletas)

        Args:
            cliente_numero: Número do cliente
            classificacao: QUENTE, MORNO ou FRIO
        """
        # Remover tags antigas
        if classificacao == "QUENTE":
            self.tags.remover_tag(cliente_numero, "lead_morno")
            self.tags.remover_tag(cliente_numero, "lead_frio")
        elif classificacao == "MORNO":
            self.tags.remover_tag(cliente_numero, "lead_frio")
            self.tags.remover_tag(cliente_numero, "lead_quente")
        else:  # FRIO
            self.tags.remover_tag(cliente_numero, "lead_quente")
            self.tags.remover_tag(cliente_numero, "lead_morno")

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

            # Tags
            tags = self.tags.get_tags_aplicadas(cliente_numero)

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

        # Reset tags cache
        tags_key = f"tags_aplicadas:{cliente_numero}"
        self.redis.delete(tags_key)

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
