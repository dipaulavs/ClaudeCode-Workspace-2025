#!/usr/bin/env python3
"""
📊 DASHBOARD VISUAL DIÁRIO - Gráficos + WhatsApp

Gera dashboard completo com:
- Gráficos visuais (barras, pizza, linha)
- Métricas consolidadas
- Análise de qualidade
- Envia por WhatsApp às 8h (cron)

DEPENDÊNCIAS:
- Orshot API (geração de imagens) OU
- Matplotlib (fallback local)
"""

import sys
import json
import requests
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Adiciona path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class DashboardVisual:
    """Gera dashboard visual com gráficos"""

    def __init__(self, redis_client, config: Dict):
        """
        Args:
            redis_client: Cliente Redis (Upstash)
            config: Config com Evolution API
        """
        self.redis = redis_client
        self.config = config

    def gerar_e_enviar(self, numero_destino: str, data: Optional[date] = None):
        """
        Gera dashboard e envia por WhatsApp

        Args:
            numero_destino: Número WhatsApp do gestor
            data: Data do relatório (padrão: ontem)
        """
        if data is None:
            # Por padrão, relatório de ontem (executado às 8h de hoje)
            data = (datetime.now() - timedelta(days=1)).date()

        print(f"\n📊 Gerando dashboard para {data.strftime('%d/%m/%Y')}...")

        # 1. Coletar métricas
        metricas = self._coletar_metricas(data)

        # 2. Gerar texto do relatório
        texto_relatorio = self._gerar_texto_relatorio(metricas, data)

        # 3. Gerar imagem com gráficos
        url_imagem = self._gerar_grafico_visual(metricas, data)

        # 4. Enviar por WhatsApp
        self._enviar_whatsapp(numero_destino, texto_relatorio, url_imagem)

        print(f"✅ Dashboard enviado para {numero_destino}")

    def _coletar_metricas(self, data: date) -> Dict:
        """Coleta todas as métricas do dia"""

        def get_int(key):
            val = self.redis.get(key)
            if val is None:
                return 0
            return int(val) if isinstance(val, (int, str)) else int(val.decode())

        def get_list(key):
            val = self.redis.lrange(key, 0, -1)
            return [v.decode() if isinstance(v, bytes) else v for v in val] if val else []

        data_str = data.strftime("%Y-%m-%d")

        metricas = {
            # Atendimentos
            "total_atendimentos": get_int(f"metricas:{data_str}:total_atendimentos"),
            "bot_atendeu": get_int(f"metricas:{data_str}:bot_atendeu"),
            "escaladas": get_int(f"metricas:{data_str}:escaladas_humano"),

            # Leads
            "leads_novos": get_int(f"metricas:{data_str}:leads_novos"),
            "leads_quentes": len(get_list(f"metricas:{data_str}:leads_quentes")),

            # Conversão
            "visitas_agendadas": get_int(f"metricas:{data_str}:visitas_agendadas"),
            "propostas_enviadas": get_int(f"metricas:{data_str}:propostas_enviadas"),

            # Tags criadas
            "tags_interesse": get_int(f"metricas:{data_str}:tags_interesse"),
            "tags_frustrado": get_int(f"metricas:{data_str}:tags_frustrado"),
            "tags_visita": get_int(f"metricas:{data_str}:tags_visita"),

            # Ferramentas
            "chamadas_local": get_int(f"metricas:{data_str}:ferramentas_local"),
            "chamadas_mcp": get_int(f"metricas:{data_str}:ferramentas_mcp"),

            # Qualidade
            "erros_mcp": get_int(f"metricas:{data_str}:erros_mcp"),
            "tempo_resposta_total": get_int(f"metricas:{data_str}:tempo_resposta_ms"),

            # Follow-ups
            "followups_enviados": get_int(f"metricas:{data_str}:followups_enviados"),
            "followups_respondidos": get_int(f"metricas:{data_str}:followups_respondidos"),
        }

        # Cálculos derivados
        if metricas['total_atendimentos'] > 0:
            metricas['tempo_resposta_medio'] = metricas['tempo_resposta_total'] / metricas['total_atendimentos']
        else:
            metricas['tempo_resposta_medio'] = 0

        total_ferramentas = metricas['chamadas_local'] + metricas['chamadas_mcp']
        if total_ferramentas > 0:
            metricas['percentual_local'] = (metricas['chamadas_local'] / total_ferramentas) * 100
        else:
            metricas['percentual_local'] = 0

        return metricas

    def _gerar_texto_relatorio(self, metricas: Dict, data: date) -> str:
        """Gera texto do relatório"""

        # Emojis de status
        emoji_atend = "🟢" if metricas['total_atendimentos'] > 0 else "🔴"
        emoji_qualidade = "🟢" if metricas['erros_mcp'] == 0 else "🟡" if metricas['erros_mcp'] < 3 else "🔴"
        emoji_tempo = "🟢" if metricas['tempo_resposta_medio'] < 2000 else "🟡" if metricas['tempo_resposta_medio'] < 5000 else "🔴"

        # Taxa de escalonamento
        if metricas['total_atendimentos'] > 0:
            taxa_esc = (metricas['escaladas'] / metricas['total_atendimentos']) * 100
        else:
            taxa_esc = 0

        # Taxa de conversão
        if metricas['leads_novos'] > 0:
            taxa_conv = (metricas['visitas_agendadas'] / metricas['leads_novos']) * 100
        else:
            taxa_conv = 0

        relatorio = f"""📊 *DASHBOARD DIÁRIO*
📅 {data.strftime('%d/%m/%Y (%A)')}

━━━━━━━━━━━━━━━━━━━━━━━

{emoji_atend} *ATENDIMENTOS*
   Total: {metricas['total_atendimentos']}
   🤖 Bot: {metricas['bot_atendeu']} ({100-taxa_esc:.0f}%)
   👨‍💼 Humano: {metricas['escaladas']} ({taxa_esc:.0f}%)

👥 *LEADS*
   Novos: {metricas['leads_novos']}
   🔥 Quentes: {metricas['leads_quentes']}

📅 *CONVERSÃO*
   Visitas: {metricas['visitas_agendadas']} ({taxa_conv:.0f}%)
   Propostas: {metricas['propostas_enviadas']}

🏷️ *TAGS CRIADAS*
   Interesse: {metricas['tags_interesse']}
   Visita: {metricas['tags_visita']}
   Frustrado: {metricas['tags_frustrado']}

━━━━━━━━━━━━━━━━━━━━━━━

{emoji_qualidade} *QUALIDADE*
   Erros MCP: {metricas['erros_mcp']}
   Ferramentas Local: {metricas['chamadas_local']} ({metricas['percentual_local']:.0f}%)
   Ferramentas MCP: {metricas['chamadas_mcp']}

{emoji_tempo} *PERFORMANCE*
   Tempo médio: {metricas['tempo_resposta_medio']:.0f}ms

📨 *FOLLOW-UPS*
   Enviados: {metricas['followups_enviados']}
   Respondidos: {metricas['followups_respondidos']}

━━━━━━━━━━━━━━━━━━━━━━━

📸 *Gráficos detalhados abaixo* ↓
"""

        return relatorio

    def _gerar_grafico_visual(self, metricas: Dict, data: date) -> Optional[str]:
        """
        Gera imagem com gráficos usando Orshot

        Returns:
            URL da imagem gerada ou None
        """
        try:
            # Dados para os gráficos
            dados_graficos = {
                # Gráfico 1: Atendimentos (Pizza)
                "atendimentos": {
                    "Bot": metricas['bot_atendeu'],
                    "Humano": metricas['escaladas']
                },

                # Gráfico 2: Conversão (Funil)
                "conversao": {
                    "Leads": metricas['leads_novos'],
                    "Visitas": metricas['visitas_agendadas'],
                    "Propostas": metricas['propostas_enviadas']
                },

                # Gráfico 3: Ferramentas (Barra)
                "ferramentas": {
                    "Local": metricas['chamadas_local'],
                    "MCP": metricas['chamadas_mcp']
                },

                # Gráfico 4: Tags (Barra horizontal)
                "tags": {
                    "Interesse": metricas['tags_interesse'],
                    "Visita": metricas['tags_visita'],
                    "Frustrado": metricas['tags_frustrado']
                }
            }

            # Tenta gerar com Orshot
            url_imagem = self._gerar_com_orshot(dados_graficos, data)

            if url_imagem:
                return url_imagem

            # Fallback: ASCII art
            return self._gerar_ascii_art(metricas)

        except Exception as e:
            print(f"⚠️ Erro ao gerar gráfico: {e}")
            return None

    def _gerar_com_orshot(self, dados: Dict, data: date) -> Optional[str]:
        """Gera imagem usando Orshot API"""
        # TODO: Integrar Orshot quando disponível
        # Por enquanto retorna None (usa ASCII art)
        return None

    def _gerar_ascii_art(self, metricas: Dict) -> str:
        """
        Gera gráficos ASCII (fallback)

        Returns:
            String com gráficos ASCII
        """
        # Gráfico de barras: Atendimentos
        total = metricas['bot_atendeu'] + metricas['escaladas']
        if total > 0:
            perc_bot = (metricas['bot_atendeu'] / total) * 100
            perc_humano = (metricas['escaladas'] / total) * 100

            barra_bot = "█" * int(perc_bot / 5)
            barra_humano = "█" * int(perc_humano / 5)
        else:
            barra_bot = ""
            barra_humano = ""
            perc_bot = 0
            perc_humano = 0

        # Gráfico de barras: Ferramentas
        total_ferr = metricas['chamadas_local'] + metricas['chamadas_mcp']
        if total_ferr > 0:
            perc_local = (metricas['chamadas_local'] / total_ferr) * 100
            perc_mcp = (metricas['chamadas_mcp'] / total_ferr) * 100

            barra_local = "█" * int(perc_local / 5)
            barra_mcp = "█" * int(perc_mcp / 5)
        else:
            barra_local = ""
            barra_mcp = ""
            perc_local = 0
            perc_mcp = 0

        grafico = f"""
```
ATENDIMENTOS:
Bot    [{barra_bot:<20}] {perc_bot:.0f}%
Humano [{barra_humano:<20}] {perc_humano:.0f}%

FERRAMENTAS:
Local  [{barra_local:<20}] {perc_local:.0f}%
MCP    [{barra_mcp:<20}] {perc_mcp:.0f}%
```
"""
        return grafico

    def _enviar_whatsapp(self, numero: str, mensagem: str, url_imagem: Optional[str]):
        """Envia dashboard por WhatsApp via Evolution API"""

        evolution_config = self.config.get('evolution', {})
        api_url = evolution_config.get('url', '').rstrip('/')
        api_key = evolution_config.get('api_key', '')
        instance = evolution_config.get('instance', '')

        if not all([api_url, api_key, instance]):
            print("⚠️ Evolution API não configurada")
            return False

        try:
            # Envia texto
            url = f"{api_url}/message/sendText/{instance}"
            headers = {"apikey": api_key, "Content-Type": "application/json"}

            payload = {
                "number": numero,
                "text": mensagem
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 201:
                print(f"   ✅ Mensagem enviada")
            else:
                print(f"   ⚠️ Erro ao enviar mensagem: {response.status_code}")

            # Envia imagem (se houver)
            if url_imagem and not url_imagem.startswith("```"):
                url = f"{api_url}/message/sendMedia/{instance}"

                payload = {
                    "number": numero,
                    "mediatype": "image",
                    "media": url_imagem,
                    "caption": f"Dashboard {data.strftime('%d/%m/%Y')}"
                }

                response = requests.post(url, headers=headers, json=payload, timeout=30)

                if response.status_code == 201:
                    print(f"   ✅ Imagem enviada")

            return True

        except Exception as e:
            print(f"❌ Erro ao enviar WhatsApp: {e}")
            return False


# ==============================================================================
# COLETOR DE MÉTRICAS (durante atendimento)
# ==============================================================================

class ColetorMetricasChatbot:
    """
    Coleta métricas durante atendimento do chatbot

    USO:
    - Importar no chatbot principal
    - Registrar cada evento
    """

    def __init__(self, redis_client):
        self.redis = redis_client

    def registrar_atendimento(self, numero_cliente: str):
        """Registra novo atendimento"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:total_atendimentos")
        print(f"   📊 Métrica: total_atendimentos++")

    def registrar_bot_respondeu(self):
        """Registra que bot respondeu"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:bot_atendeu")

    def registrar_escalada_humano(self):
        """Registra escalada para humano"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:escaladas_humano")

    def registrar_lead_novo(self, numero_cliente: str):
        """Registra novo lead"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:leads_novos")

    def registrar_lead_quente(self, numero_cliente: str):
        """Registra lead quente (score >= 70)"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        key = f"metricas:{hoje}:leads_quentes"
        # Adiciona à lista se não existir
        if not self.redis.lpos(key, numero_cliente):
            self.redis.lpush(key, numero_cliente)
            self.redis.expire(key, 7*24*60*60)  # 7 dias

    def registrar_visita_agendada(self):
        """Registra visita agendada"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:visitas_agendadas")

    def registrar_proposta_enviada(self):
        """Registra proposta enviada"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:propostas_enviadas")

    def registrar_tag_criada(self, tipo_tag: str):
        """
        Registra tag criada

        Args:
            tipo_tag: "interesse", "frustrado", "visita", etc
        """
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:tags_{tipo_tag}")

    def registrar_ferramenta_local(self):
        """Registra uso de ferramenta local"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:ferramentas_local")

    def registrar_ferramenta_mcp(self):
        """Registra uso de ferramenta MCP"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:ferramentas_mcp")

    def registrar_erro_mcp(self):
        """Registra erro em ferramenta MCP"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:erros_mcp")

    def registrar_tempo_resposta(self, tempo_ms: int):
        """Registra tempo de resposta em ms"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incrby(f"metricas:{hoje}:tempo_resposta_ms", tempo_ms)

    def registrar_followup_enviado(self):
        """Registra follow-up enviado"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:followups_enviados")

    def registrar_followup_respondido(self):
        """Registra follow-up respondido"""
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:followups_respondidos")


# ==============================================================================
# TESTE
# ==============================================================================

if __name__ == "__main__":
    print("📊 Dashboard Visual - Teste\n")

    # Mock Redis
    class MockRedis:
        def __init__(self):
            self.data = {}
            # Popula com dados fictícios
            hoje = datetime.now().date().strftime("%Y-%m-%d")
            self.data = {
                f"metricas:{hoje}:total_atendimentos": "45",
                f"metricas:{hoje}:bot_atendeu": "32",
                f"metricas:{hoje}:escaladas_humano": "13",
                f"metricas:{hoje}:leads_novos": "28",
                f"metricas:{hoje}:leads_quentes": ["5531999999999", "5531888888888"],
                f"metricas:{hoje}:visitas_agendadas": "12",
                f"metricas:{hoje}:propostas_enviadas": "8",
                f"metricas:{hoje}:tags_interesse": "25",
                f"metricas:{hoje}:tags_frustrado": "5",
                f"metricas:{hoje}:tags_visita": "12",
                f"metricas:{hoje}:ferramentas_local": "89",
                f"metricas:{hoje}:ferramentas_mcp": "34",
                f"metricas:{hoje}:erros_mcp": "1",
                f"metricas:{hoje}:tempo_resposta_ms": "67500",  # 45 atendimentos * 1500ms
                f"metricas:{hoje}:followups_enviados": "15",
                f"metricas:{hoje}:followups_respondidos": "7",
            }

        def get(self, key):
            return self.data.get(key)

        def lrange(self, key, start, end):
            val = self.data.get(key, [])
            return val if isinstance(val, list) else []

    # Mock config
    config = {
        'evolution': {
            'url': 'https://evolution.loop9.com.br',
            'api_key': 'mock_key',
            'instance': 'test'
        }
    }

    # Teste
    redis_mock = MockRedis()
    dashboard = DashboardVisual(redis_mock, config)

    # Gera relatório
    metricas = dashboard._coletar_metricas(datetime.now().date())
    texto = dashboard._gerar_texto_relatorio(metricas, datetime.now().date())

    print(texto)
    print()

    grafico = dashboard._gerar_ascii_art(metricas)
    print(grafico)

    print("\n✅ Dashboard gerado com sucesso!")
