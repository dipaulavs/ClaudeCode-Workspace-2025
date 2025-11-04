"""
Sistema de Detecção de Origem (UTM tracking)
Rastreia de onde o lead veio (Facebook, Instagram, etc)
"""
import json
import time
import redis
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs


class DeteccaoOrigem:
    """
    Sistema de detecção de origem via UTM tracking

    Como funciona:
    1. Link do anúncio: https://wa.me/5531980160822?text=oi&utm_source=facebook&imovel=apto-001
    2. Cliente clica → WhatsApp abre com mensagem "oi" + dados UTM
    3. Bot detecta e salva origem: facebook, imóvel: apto-001
    4. Aplica tags no Chatwoot: origem_facebook, imovel_apto-001
    """

    # Mapeamento de origens conhecidas
    ORIGENS = {
        "facebook": "origem_facebook",
        "instagram": "origem_instagram",
        "google": "origem_google",
        "whatsapp": "origem_whatsapp",
        "indicacao": "origem_indicacao",
        "site": "origem_site",
        "olx": "origem_olx",
        "imovelweb": "origem_imovelweb"
    }

    def __init__(self, redis_client: redis.Redis, sistema_tags):
        """
        Inicializa sistema de detecção de origem

        Args:
            redis_client: Cliente Redis configurado
            sistema_tags: Instância do SistemaTags para aplicar tags
        """
        self.redis = redis_client
        self.sistema_tags = sistema_tags

    def extrair_origem_inicial(self, mensagem_inicial: str, link_params: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """
        Extrai origem da mensagem inicial

        Args:
            mensagem_inicial: Primeira mensagem do cliente
            link_params: Parâmetros do link (utm_source, imovel, etc)
                        Em produção, virá do webhook da Evolution API

        Returns:
            Dict com dados de origem ou None
        """
        if not link_params:
            # Sem UTM = origem direta
            return {
                "utm_source": "direto",
                "imovel_id": None,
                "timestamp": time.time()
            }

        # Extrair dados do link
        origem_data = {
            "utm_source": link_params.get("utm_source", "direto"),
            "utm_medium": link_params.get("utm_medium"),
            "utm_campaign": link_params.get("utm_campaign"),
            "imovel_id": link_params.get("imovel"),
            "timestamp": time.time()
        }

        return origem_data

    def extrair_origem_de_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrai origem de uma URL completa

        Args:
            url: URL completa (ex: https://wa.me/...?utm_source=facebook&imovel=apto-001)

        Returns:
            Dict com dados de origem
        """
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)

            # Extrair parâmetros (parse_qs retorna listas)
            link_params = {}
            for key, value in params.items():
                link_params[key] = value[0] if value else None

            return self.extrair_origem_inicial(None, link_params)

        except Exception as e:
            print(f"❌ Erro ao extrair origem de URL: {e}")
            return None

    def salvar_origem(self, cliente_numero: str, origem_data: Dict[str, Any]) -> bool:
        """
        Salva origem no Redis

        Args:
            cliente_numero: Número do cliente
            origem_data: Dados de origem extraídos

        Returns:
            True se sucesso
        """
        try:
            origem_key = f"origem:{cliente_numero}"

            # Salvar dados completos
            self.redis.set(origem_key, json.dumps(origem_data))

            print(f"✅ Origem salva para {cliente_numero}: {origem_data['utm_source']}")
            return True

        except Exception as e:
            print(f"❌ Erro ao salvar origem: {e}")
            return False

    def get_origem(self, cliente_numero: str) -> Optional[Dict[str, Any]]:
        """
        Retorna origem do cliente

        Args:
            cliente_numero: Número do cliente

        Returns:
            Dict com dados de origem ou None
        """
        origem_key = f"origem:{cliente_numero}"
        origem_raw = self.redis.get(origem_key)

        if origem_raw:
            return json.loads(origem_raw)

        return None

    def aplicar_tags_origem(self, cliente_numero: str) -> bool:
        """
        Aplica tags de origem no Chatwoot

        Args:
            cliente_numero: Número do cliente

        Returns:
            True se sucesso
        """
        try:
            # Buscar origem
            origem_data = self.get_origem(cliente_numero)
            if not origem_data:
                print(f"⚠️ Sem dados de origem para {cliente_numero}")
                return False

            tags_aplicar = []

            # Tag de origem
            utm_source = origem_data.get("utm_source", "direto").lower()
            if utm_source in self.ORIGENS:
                tags_aplicar.append(self.ORIGENS[utm_source])
            else:
                tags_aplicar.append(f"origem_{utm_source}")

            # Tag de imóvel (se houver)
            imovel_id = origem_data.get("imovel_id")
            if imovel_id:
                tags_aplicar.append(f"imovel_{imovel_id}")

            # Tag de campanha (se houver)
            utm_campaign = origem_data.get("utm_campaign")
            if utm_campaign:
                tags_aplicar.append(f"campanha_{utm_campaign}")

            # Aplicar tags via SistemaTags
            self.sistema_tags.aplicar_chatwoot(cliente_numero, tags_aplicar)

            # Aplicar custom attributes
            custom_attrs = {
                "origem": origem_data.get("utm_source"),
                "imovel_interesse": imovel_id or "nao_especificado"
            }

            if utm_campaign:
                custom_attrs["campanha"] = utm_campaign

            self.sistema_tags.atualizar_custom_attributes(cliente_numero, custom_attrs)

            print(f"✅ Tags de origem aplicadas para {cliente_numero}: {tags_aplicar}")
            return True

        except Exception as e:
            print(f"❌ Erro ao aplicar tags de origem: {e}")
            return False

    def registrar_conversao(self, cliente_numero: str, tipo_conversao: str = "visita_agendada") -> bool:
        """
        Registra conversão do lead

        Args:
            cliente_numero: Número do cliente
            tipo_conversao: Tipo (visita_agendada, contrato_assinado, etc)

        Returns:
            True se sucesso
        """
        try:
            # Buscar origem
            origem_data = self.get_origem(cliente_numero)
            if not origem_data:
                return False

            # Salvar conversão
            conversao_key = f"conversao:{cliente_numero}"
            conversao_data = {
                "tipo": tipo_conversao,
                "timestamp": time.time(),
                "origem": origem_data
            }

            self.redis.set(conversao_key, json.dumps(conversao_data))

            # Aplicar tag de conversão
            self.sistema_tags.aplicar_chatwoot(cliente_numero, [f"converteu_{tipo_conversao}"])

            print(f"✅ Conversão registrada: {cliente_numero} → {tipo_conversao}")
            return True

        except Exception as e:
            print(f"❌ Erro ao registrar conversão: {e}")
            return False

    def get_conversoes(self, origem: str, periodo_dias: int = 30) -> int:
        """
        Retorna número de conversões por origem

        Args:
            origem: Origem a verificar (ex: "facebook")
            periodo_dias: Período em dias

        Returns:
            Número de conversões
        """
        try:
            # Buscar todas as conversões
            conversoes = 0
            timestamp_limite = time.time() - (periodo_dias * 86400)

            # Scan de chaves de conversão
            for key in self.redis.scan_iter(match="conversao:*"):
                conversao_raw = self.redis.get(key)
                if conversao_raw:
                    conversao_data = json.loads(conversao_raw)

                    # Verificar origem e período
                    if conversao_data.get("origem", {}).get("utm_source") == origem:
                        if conversao_data.get("timestamp", 0) >= timestamp_limite:
                            conversoes += 1

            return conversoes

        except Exception as e:
            print(f"❌ Erro ao contar conversões: {e}")
            return 0

    def get_imoveis_mais_procurados(self, limit: int = 10) -> list:
        """
        Retorna imóveis mais procurados

        Args:
            limit: Número de resultados

        Returns:
            Lista de dicts com imovel_id e contagem
        """
        try:
            imoveis_count = {}

            # Scan de origens
            for key in self.redis.scan_iter(match="origem:*"):
                origem_raw = self.redis.get(key)
                if origem_raw:
                    origem_data = json.loads(origem_raw)
                    imovel_id = origem_data.get("imovel_id")

                    if imovel_id:
                        imoveis_count[imovel_id] = imoveis_count.get(imovel_id, 0) + 1

            # Ordenar por contagem
            ranking = [
                {"imovel_id": imovel, "leads": count}
                for imovel, count in sorted(imoveis_count.items(), key=lambda x: x[1], reverse=True)
            ]

            return ranking[:limit]

        except Exception as e:
            print(f"❌ Erro ao buscar imóveis mais procurados: {e}")
            return []
