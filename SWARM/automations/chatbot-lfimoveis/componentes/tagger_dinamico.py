#!/usr/bin/env python3
"""
🏷️ TAGGER DINÂMICO - Gerenciamento Inteligente de Tags de Imóveis

RESPONSABILIDADES:
1. Detectar mudança de contexto (cliente quer outro imóvel)
2. Decidir automaticamente: trocar direto ou perguntar
3. Manter histórico completo de imóveis visitados
4. Aplicar tags visuais no Chatwoot
5. Sincronizar estado Redis + Chatwoot

REGRAS DE DECISÃO:
- Score < 40 (FRIO): Troca direto
- Score >= 40 (MORNO/QUENTE): Pergunta confirmação
- Sem imóvel ativo: Aplica direto
- Mesmo imóvel: Mantém sem ação

INTEGRAÇÃO:
- Redis: Estado persistente
- Chatwoot: Tags visuais + custom attributes
- Score: Decisões baseadas em interesse
"""

import json
import time
import redis
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class TaggerDinamico:
    """
    Gerencia tags de imóveis de forma inteligente e dinâmica

    FLUXO:
    1. Cliente menciona imóvel X
    2. Busca imóvel ativo atual (se existe)
    3. Calcula interesse no atual (via score/tempo)
    4. Decide ação: aplicar|trocar|confirmar
    5. Retorna mensagem para bot (se precisa confirmar)
    """

    def __init__(self, redis_client: redis.Redis, chatwoot_config: Dict, prefix: str = "lfimoveis"):
        """
        Inicializa Tagger Dinâmico

        Args:
            redis_client: Cliente Redis configurado
            chatwoot_config: Config do Chatwoot {url, token, account_id, inbox_id}
            prefix: Prefixo para chaves Redis (default: lfimoveis)
        """
        self.redis = redis_client
        self.chatwoot = chatwoot_config
        self.prefix = prefix

        # Thresholds de decisão
        self.SCORE_BAIXO = 40  # Abaixo = troca direto
        self.TEMPO_MAXIMO_MINUTOS = 30  # Se passou 30min = troca direto

        print(f"✅ TaggerDinamico inicializado (prefix={prefix})")

    def aplicar_tag_imovel(
        self,
        numero_cliente: str,
        novo_imovel_id: str,
        score_atual: int = 0,
        forcar_troca: bool = False
    ) -> Dict:
        """
        Aplica tag de imóvel de forma inteligente

        Args:
            numero_cliente: Número WhatsApp (ex: 5531980160822)
            novo_imovel_id: ID do novo imóvel (ex: imovel-001)
            score_atual: Score atual do cliente (0-100)
            forcar_troca: True para forçar troca sem perguntar

        Returns:
            {
                'acao': 'aplicada'|'trocar_confirmar'|'mantida',
                'imovel_anterior': <id> ou None,
                'imovel_novo': <id>,
                'mensagem_bot': 'texto' ou None,
                'precisa_confirmar': bool
            }
        """
        resultado = {
            'acao': None,
            'imovel_anterior': None,
            'imovel_novo': novo_imovel_id,
            'mensagem_bot': None,
            'precisa_confirmar': False
        }

        try:
            # 1. Busca imóvel ativo atual
            imovel_atual = self._obter_imovel_ativo(numero_cliente)
            resultado['imovel_anterior'] = imovel_atual

            # 2. CASO 1: Cliente sem imóvel ativo
            if not imovel_atual:
                self._aplicar_tag_nova(numero_cliente, novo_imovel_id)
                resultado['acao'] = 'aplicada'
                print(f"✅ Tag aplicada (novo): {novo_imovel_id}")
                return resultado

            # 3. CASO 2: Mesmo imóvel (mantém)
            if imovel_atual == novo_imovel_id:
                resultado['acao'] = 'mantida'
                print(f"✅ Tag mantida (mesmo imóvel): {novo_imovel_id}")
                return resultado

            # 4. CASO 3: Cliente quer OUTRO imóvel
            # Calcular nível de interesse no atual
            nivel_interesse = self._calcular_interesse_atual(numero_cliente, score_atual)

            # DECISÃO: Trocar direto ou perguntar?
            if forcar_troca or nivel_interesse < self.SCORE_BAIXO:
                # BAIXO interesse → Troca direto
                self._trocar_tag(numero_cliente, imovel_atual, novo_imovel_id)
                resultado['acao'] = 'trocada'
                print(f"✅ Tag trocada (baixo interesse): {imovel_atual} → {novo_imovel_id}")
            else:
                # ALTO interesse → Pergunta confirmação
                resultado['acao'] = 'trocar_confirmar'
                resultado['precisa_confirmar'] = True
                resultado['mensagem_bot'] = self._gerar_mensagem_confirmacao(
                    imovel_atual,
                    novo_imovel_id
                )
                print(f"❓ Confirmação necessária: {imovel_atual} → {novo_imovel_id}")

            return resultado

        except Exception as e:
            print(f"❌ Erro em aplicar_tag_imovel: {e}")
            resultado['acao'] = 'erro'
            return resultado

    def confirmar_troca(self, numero_cliente: str, novo_imovel_id: str) -> bool:
        """
        Confirma troca de imóvel (após cliente responder "sim")

        Args:
            numero_cliente: Número WhatsApp
            novo_imovel_id: ID do novo imóvel

        Returns:
            bool (sucesso)
        """
        try:
            imovel_anterior = self._obter_imovel_ativo(numero_cliente)
            self._trocar_tag(numero_cliente, imovel_anterior, novo_imovel_id)
            print(f"✅ Troca confirmada: {imovel_anterior} → {novo_imovel_id}")
            return True
        except Exception as e:
            print(f"❌ Erro ao confirmar troca: {e}")
            return False

    def cancelar_troca(self, numero_cliente: str) -> bool:
        """
        Cancela troca (cliente disse "não")
        Mantém imóvel atual

        Args:
            numero_cliente: Número WhatsApp

        Returns:
            bool (sucesso)
        """
        try:
            imovel_atual = self._obter_imovel_ativo(numero_cliente)
            print(f"✅ Troca cancelada. Mantido: {imovel_atual}")
            return True
        except Exception as e:
            print(f"❌ Erro ao cancelar troca: {e}")
            return False

    def registrar_historico(self, numero_cliente: str, imovel_id: str, acao: str = "visualizou"):
        """
        Registra visita no histórico do cliente

        Args:
            numero_cliente: Número WhatsApp
            imovel_id: ID do imóvel
            acao: Tipo de ação (visualizou, pediu_fotos, agendou_visita)
        """
        try:
            # Lista de imóveis visitados (IDs únicos)
            key_historico = f"imoveis_vistos:{self.prefix}:{numero_cliente}"
            historico_raw = self.redis.get(key_historico)
            historico = json.loads(historico_raw) if historico_raw else []

            # Adiciona se não existir
            if imovel_id not in historico:
                historico.append(imovel_id)
                self.redis.setex(
                    key_historico,
                    86400 * 14,  # 14 dias
                    json.dumps(historico)
                )

            # Timeline detalhada (com timestamps)
            key_timeline = f"timeline_imoveis:{self.prefix}:{numero_cliente}"
            evento = {
                "imovel_id": imovel_id,
                "acao": acao,
                "timestamp": int(time.time())
            }

            self.redis.lpush(key_timeline, json.dumps(evento))
            self.redis.ltrim(key_timeline, 0, 99)  # Mantém últimos 100 eventos
            self.redis.expire(key_timeline, 86400 * 14)

            print(f"✅ Histórico registrado: {numero_cliente} {acao} {imovel_id}")

        except Exception as e:
            print(f"⚠️ Erro ao registrar histórico: {e}")

    def obter_historico(self, numero_cliente: str, limit: int = 10) -> List[Dict]:
        """
        Retorna histórico de imóveis visitados

        Args:
            numero_cliente: Número WhatsApp
            limit: Quantidade máxima de eventos

        Returns:
            Lista de eventos [{imovel_id, acao, timestamp}]
        """
        try:
            key_timeline = f"timeline_imoveis:{self.prefix}:{numero_cliente}"
            eventos_raw = self.redis.lrange(key_timeline, 0, limit - 1)

            eventos = []
            for evento_raw in eventos_raw:
                eventos.append(json.loads(evento_raw))

            return eventos

        except Exception as e:
            print(f"⚠️ Erro ao obter histórico: {e}")
            return []

    def obter_imoveis_visitados(self, numero_cliente: str) -> List[str]:
        """
        Retorna lista de IDs de imóveis visitados (sem duplicatas)

        Args:
            numero_cliente: Número WhatsApp

        Returns:
            Lista de IDs únicos
        """
        try:
            key_historico = f"imoveis_vistos:{self.prefix}:{numero_cliente}"
            historico_raw = self.redis.get(key_historico)
            return json.loads(historico_raw) if historico_raw else []

        except Exception as e:
            print(f"⚠️ Erro ao obter imóveis visitados: {e}")
            return []

    def limpar_tag_atual(self, numero_cliente: str) -> bool:
        """
        Remove tag de imóvel ativo (útil para reset)

        Args:
            numero_cliente: Número WhatsApp

        Returns:
            bool (sucesso)
        """
        try:
            imovel_atual = self._obter_imovel_ativo(numero_cliente)

            if imovel_atual:
                # Remove tag do Chatwoot
                self._remover_tag_chatwoot(numero_cliente, imovel_atual)

                # Remove do Redis
                self._limpar_imovel_ativo(numero_cliente)

                print(f"✅ Tag limpa: {imovel_atual}")
                return True

            return False

        except Exception as e:
            print(f"❌ Erro ao limpar tag: {e}")
            return False

    def obter_resumo(self, numero_cliente: str) -> Dict:
        """
        Retorna resumo completo do cliente

        Args:
            numero_cliente: Número WhatsApp

        Returns:
            Dict com resumo {
                imovel_ativo,
                imoveis_visitados,
                total_eventos,
                ultimo_acesso
            }
        """
        try:
            imovel_ativo = self._obter_imovel_ativo(numero_cliente)
            imoveis_visitados = self.obter_imoveis_visitados(numero_cliente)
            timeline = self.obter_historico(numero_cliente, limit=1)

            return {
                "imovel_ativo": imovel_ativo,
                "imoveis_visitados": imoveis_visitados,
                "total_visitados": len(imoveis_visitados),
                "ultimo_acesso": timeline[0] if timeline else None
            }

        except Exception as e:
            print(f"❌ Erro ao obter resumo: {e}")
            return {}

    # ============================================
    # MÉTODOS INTERNOS (Privados)
    # ============================================

    def _obter_imovel_ativo(self, numero_cliente: str) -> Optional[str]:
        """Busca imóvel ativo no Redis"""
        try:
            chave = f"imovel_ativo:{self.prefix}:{numero_cliente}"
            imovel_id = self.redis.get(chave)
            return imovel_id if isinstance(imovel_id, str) else (imovel_id.decode() if imovel_id else None)
        except Exception as e:
            print(f"⚠️ Erro ao obter imóvel ativo: {e}")
            return None

    def _salvar_imovel_ativo(self, numero_cliente: str, imovel_id: str):
        """Salva imóvel ativo no Redis"""
        try:
            chave = f"imovel_ativo:{self.prefix}:{numero_cliente}"
            self.redis.setex(chave, 86400, imovel_id)  # 24h TTL

            # Salva também timestamp da última troca
            chave_timestamp = f"imovel_ativo_timestamp:{self.prefix}:{numero_cliente}"
            self.redis.setex(chave_timestamp, 86400, str(int(time.time())))

        except Exception as e:
            print(f"⚠️ Erro ao salvar imóvel ativo: {e}")

    def _limpar_imovel_ativo(self, numero_cliente: str):
        """Remove imóvel ativo do Redis"""
        try:
            chave = f"imovel_ativo:{self.prefix}:{numero_cliente}"
            chave_timestamp = f"imovel_ativo_timestamp:{self.prefix}:{numero_cliente}"
            self.redis.delete(chave)
            self.redis.delete(chave_timestamp)
        except Exception as e:
            print(f"⚠️ Erro ao limpar imóvel ativo: {e}")

    def _calcular_interesse_atual(self, numero_cliente: str, score_atual: int) -> int:
        """
        Calcula nível de interesse no imóvel atual

        Fatores:
        - Score atual do cliente
        - Tempo desde última troca de imóvel

        Returns:
            int (0-100)
        """
        try:
            # Fator 1: Score (peso 70%)
            interesse_score = score_atual * 0.7

            # Fator 2: Tempo no imóvel atual (peso 30%)
            chave_timestamp = f"imovel_ativo_timestamp:{self.prefix}:{numero_cliente}"
            timestamp_raw = self.redis.get(chave_timestamp)

            interesse_tempo = 0
            if timestamp_raw:
                timestamp = int(timestamp_raw if isinstance(timestamp_raw, str) else timestamp_raw.decode())
                minutos_no_imovel = (int(time.time()) - timestamp) / 60

                # Se passou muito tempo (>30min) = baixo interesse
                if minutos_no_imovel > self.TEMPO_MAXIMO_MINUTOS:
                    interesse_tempo = 0
                else:
                    # Mais tempo = mais interesse (até 30 pontos)
                    interesse_tempo = min(30, minutos_no_imovel)

            interesse_total = int(interesse_score + interesse_tempo)

            print(f"📊 Interesse calculado: {interesse_total} (score={score_atual}, tempo={interesse_tempo})")
            return interesse_total

        except Exception as e:
            print(f"⚠️ Erro ao calcular interesse: {e}")
            return score_atual  # Fallback: usar apenas score

    def _aplicar_tag_nova(self, numero_cliente: str, imovel_id: str):
        """Aplica tag de imóvel (primeira vez)"""
        # Salva no Redis
        self._salvar_imovel_ativo(numero_cliente, imovel_id)

        # Aplica tag no Chatwoot
        self._aplicar_tag_chatwoot(numero_cliente, imovel_id)

        # Registra histórico
        self.registrar_historico(numero_cliente, imovel_id, "interesse_inicial")

        # Atualiza custom attribute
        self._atualizar_custom_attribute(numero_cliente, "imovel_atual", imovel_id)

    def _trocar_tag(self, numero_cliente: str, imovel_anterior: Optional[str], imovel_novo: str):
        """Troca tag de imóvel"""
        # Remove tag anterior do Chatwoot
        if imovel_anterior:
            self._remover_tag_chatwoot(numero_cliente, imovel_anterior)
            self.registrar_historico(numero_cliente, imovel_anterior, "abandonou")

        # Aplica nova tag
        self._aplicar_tag_nova(numero_cliente, imovel_novo)

    def _aplicar_tag_chatwoot(self, numero_cliente: str, imovel_id: str):
        """Aplica tag no Chatwoot (melhor esforço)"""
        try:
            import requests

            # Busca conversation_id
            conversation_id = self._buscar_conversation_id(numero_cliente)
            if not conversation_id:
                print(f"⚠️ Conversa não encontrada no Chatwoot")
                return

            # Formata nome da tag
            tag_nome = f"interessado_{imovel_id}".replace("-", "_")

            # Adiciona tag
            url = f"{self.chatwoot['url']}/api/v1/accounts/{self.chatwoot['account_id']}/conversations/{conversation_id}/labels"
            headers = {
                "api_access_token": self.chatwoot['token'],
                "Content-Type": "application/json"
            }
            payload = {"labels": [tag_nome]}

            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                print(f"✅ Tag Chatwoot aplicada: {tag_nome}")
            else:
                print(f"⚠️ Erro ao aplicar tag Chatwoot: {response.status_code}")

        except Exception as e:
            print(f"⚠️ Erro no Chatwoot (não crítico): {e}")

    def _remover_tag_chatwoot(self, numero_cliente: str, imovel_id: str):
        """Remove tag no Chatwoot (melhor esforço)"""
        try:
            import requests

            # Busca conversation_id
            conversation_id = self._buscar_conversation_id(numero_cliente)
            if not conversation_id:
                return

            # Formata nome da tag
            tag_nome = f"interessado_{imovel_id}".replace("-", "_")

            # Remove tag
            url = f"{self.chatwoot['url']}/api/v1/accounts/{self.chatwoot['account_id']}/conversations/{conversation_id}/labels"
            headers = {
                "api_access_token": self.chatwoot['token'],
                "Content-Type": "application/json"
            }
            payload = {"labels": [tag_nome]}

            response = requests.delete(url, headers=headers, json=payload, timeout=10)

            if response.status_code in [200, 204]:
                print(f"✅ Tag Chatwoot removida: {tag_nome}")

        except Exception as e:
            print(f"⚠️ Erro ao remover tag Chatwoot: {e}")

    def _buscar_conversation_id(self, numero_cliente: str) -> Optional[int]:
        """Busca ID da conversa do cliente no Chatwoot"""
        try:
            import requests

            # Busca contato
            url = f"{self.chatwoot['url']}/api/v1/accounts/{self.chatwoot['account_id']}/contacts/search"
            headers = {"api_access_token": self.chatwoot['token']}
            params = {"q": numero_cliente}

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code != 200:
                return None

            contacts = response.json().get('payload', [])
            if not contacts:
                return None

            contact_id = contacts[0]['id']

            # Busca conversas abertas do contato
            url = f"{self.chatwoot['url']}/api/v1/accounts/{self.chatwoot['account_id']}/conversations"
            params = {"inbox_id": self.chatwoot['inbox_id'], "status": "open"}

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code != 200:
                return None

            conversations = response.json().get('data', {}).get('payload', [])

            for conv in conversations:
                if conv.get('meta', {}).get('sender', {}).get('id') == contact_id:
                    return conv['id']

            return None

        except Exception as e:
            print(f"⚠️ Erro ao buscar conversation_id: {e}")
            return None

    def _atualizar_custom_attribute(self, numero_cliente: str, atributo: str, valor: str):
        """Atualiza custom attribute no Chatwoot"""
        try:
            import requests

            # Busca conversation_id
            conversation_id = self._buscar_conversation_id(numero_cliente)
            if not conversation_id:
                return

            # Atualiza custom attribute
            url = f"{self.chatwoot['url']}/api/v1/accounts/{self.chatwoot['account_id']}/conversations/{conversation_id}/custom_attributes"
            headers = {
                "api_access_token": self.chatwoot['token'],
                "Content-Type": "application/json"
            }
            payload = {
                "custom_attributes": {
                    atributo: valor
                }
            }

            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                print(f"✅ Custom attribute atualizado: {atributo}={valor}")

        except Exception as e:
            print(f"⚠️ Erro ao atualizar custom attribute: {e}")

    def _gerar_mensagem_confirmacao(self, imovel_anterior: str, imovel_novo: str) -> str:
        """Gera mensagem de confirmação para o cliente"""
        return (
            f"Você estava vendo o *{imovel_anterior}*. "
            f"Quer que eu mostre informações do *{imovel_novo}* agora? "
            f"(Responda *sim* ou *não*)"
        )


# ============================================
# EXEMPLO DE USO
# ============================================

if __name__ == "__main__":
    print("🧪 Testando TaggerDinamico...\n")

    from upstash_redis import Redis
    from pathlib import Path

    # Carrega config
    config_path = Path(__file__).parent.parent / "chatwoot_config_lfimoveis.json"

    if not config_path.exists():
        print("❌ Arquivo chatwoot_config_lfimoveis.json não encontrado")
        exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Redis
    redis_client = Redis(
        url=config['redis']['url'],
        token=config['redis']['token']
    )

    # Inicializa tagger
    tagger = TaggerDinamico(
        redis_client,
        config['chatwoot'],
        prefix="lfimoveis"
    )

    # ====================================
    # TESTE 1: Cliente novo (sem imóvel ativo)
    # ====================================
    print("=" * 60)
    print("TESTE 1: Cliente novo vê imovel-001")
    print("=" * 60)

    numero_teste = "5531999999999"

    resultado = tagger.aplicar_tag_imovel(
        numero_teste,
        "imovel-001",
        score_atual=0
    )

    print(f"\n✅ Resultado:")
    print(f"   Ação: {resultado['acao']}")
    print(f"   Imóvel anterior: {resultado['imovel_anterior']}")
    print(f"   Imóvel novo: {resultado['imovel_novo']}")
    print(f"   Precisa confirmar: {resultado['precisa_confirmar']}")

    # ====================================
    # TESTE 2: Cliente quer outro imóvel (BAIXO interesse)
    # ====================================
    print("\n" + "=" * 60)
    print("TESTE 2: Cliente quer imovel-002 (score baixo = 30)")
    print("=" * 60)

    resultado = tagger.aplicar_tag_imovel(
        numero_teste,
        "imovel-002",
        score_atual=30  # BAIXO → Troca direto
    )

    print(f"\n✅ Resultado:")
    print(f"   Ação: {resultado['acao']}")
    print(f"   Imóvel anterior: {resultado['imovel_anterior']}")
    print(f"   Imóvel novo: {resultado['imovel_novo']}")
    print(f"   Precisa confirmar: {resultado['precisa_confirmar']}")

    # ====================================
    # TESTE 3: Cliente quer outro imóvel (ALTO interesse)
    # ====================================
    print("\n" + "=" * 60)
    print("TESTE 3: Cliente quer imovel-003 (score alto = 75)")
    print("=" * 60)

    resultado = tagger.aplicar_tag_imovel(
        numero_teste,
        "imovel-003",
        score_atual=75  # ALTO → Pergunta confirmação
    )

    print(f"\n✅ Resultado:")
    print(f"   Ação: {resultado['acao']}")
    print(f"   Imóvel anterior: {resultado['imovel_anterior']}")
    print(f"   Imóvel novo: {resultado['imovel_novo']}")
    print(f"   Precisa confirmar: {resultado['precisa_confirmar']}")
    if resultado['mensagem_bot']:
        print(f"   Mensagem: {resultado['mensagem_bot']}")

    # ====================================
    # TESTE 4: Histórico
    # ====================================
    print("\n" + "=" * 60)
    print("TESTE 4: Histórico de imóveis visitados")
    print("=" * 60)

    historico = tagger.obter_historico(numero_teste)
    print(f"\n✅ Total de eventos: {len(historico)}")
    for evento in historico:
        print(f"   - {evento['imovel_id']} | {evento['acao']} | {evento['timestamp']}")

    imoveis_visitados = tagger.obter_imoveis_visitados(numero_teste)
    print(f"\n✅ Imóveis únicos visitados: {imoveis_visitados}")

    # ====================================
    # TESTE 5: Resumo completo
    # ====================================
    print("\n" + "=" * 60)
    print("TESTE 5: Resumo completo do cliente")
    print("=" * 60)

    resumo = tagger.obter_resumo(numero_teste)
    print(f"\n✅ Resumo:")
    print(f"   Imóvel ativo: {resumo['imovel_ativo']}")
    print(f"   Total visitados: {resumo['total_visitados']}")
    print(f"   Imóveis visitados: {resumo['imoveis_visitados']}")
    print(f"   Último acesso: {resumo['ultimo_acesso']}")

    # ====================================
    # LIMPEZA
    # ====================================
    print("\n" + "=" * 60)
    print("LIMPEZA: Removendo dados de teste")
    print("=" * 60)

    sucesso = tagger.limpar_tag_atual(numero_teste)
    print(f"✅ Tag limpa: {sucesso}")

    # Limpa histórico também
    redis_client.delete(f"imoveis_vistos:lfimoveis:{numero_teste}")
    redis_client.delete(f"timeline_imoveis:lfimoveis:{numero_teste}")
    print("✅ Histórico limpo")

    print("\n🎉 Testes concluídos!")
