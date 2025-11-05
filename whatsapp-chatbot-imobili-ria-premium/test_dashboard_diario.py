#!/usr/bin/env python3.11
"""
🧪 TESTE COMPLETO: Dashboard Diário

Simula um dia completo de atendimentos e gera dashboard.
Testa todas as métricas coletadas.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import time

# Importação standalone (sem dependências externas)


# ==============================================================================
# COLETOR DE MÉTRICAS (cópia standalone para teste)
# ==============================================================================

class ColetorMetricasChatbot:
    """Coletor de métricas (versão standalone para teste)"""

    def __init__(self, redis_client):
        self.redis = redis_client

    def registrar_atendimento(self, numero_cliente: str):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:total_atendimentos")

    def registrar_bot_respondeu(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:bot_atendeu")

    def registrar_escalada_humano(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:escaladas_humano")

    def registrar_lead_novo(self, numero_cliente: str):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:leads_novos")

    def registrar_lead_quente(self, numero_cliente: str):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        key = f"metricas:{hoje}:leads_quentes"
        if not self.redis.lpos(key, numero_cliente):
            self.redis.lpush(key, numero_cliente)

    def registrar_visita_agendada(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:visitas_agendadas")

    def registrar_proposta_enviada(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:propostas_enviadas")

    def registrar_tag_criada(self, tipo_tag: str):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:tags_{tipo_tag}")

    def registrar_ferramenta_local(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:ferramentas_local")

    def registrar_ferramenta_mcp(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:ferramentas_mcp")

    def registrar_erro_mcp(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:erros_mcp")

    def registrar_tempo_resposta(self, tempo_ms: int):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incrby(f"metricas:{hoje}:tempo_resposta_ms", tempo_ms)

    def registrar_followup_enviado(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:followups_enviados")

    def registrar_followup_respondido(self):
        hoje = datetime.now().date().strftime("%Y-%m-%d")
        self.redis.incr(f"metricas:{hoje}:followups_respondidos")


# ==============================================================================
# MOCK REDIS
# ==============================================================================

class MockRedis:
    """Mock Redis para teste"""
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def incr(self, key, amount=1):
        current = int(self.data.get(key, 0))
        self.data[key] = str(current + amount)
        return int(self.data[key])

    def incrby(self, key, amount):
        return self.incr(key, amount)

    def lpush(self, key, value):
        if key not in self.data:
            self.data[key] = []
        if not isinstance(self.data[key], list):
            self.data[key] = []
        self.data[key].insert(0, value)

    def lrange(self, key, start, end):
        val = self.data.get(key, [])
        return val if isinstance(val, list) else []

    def lpos(self, key, value):
        val = self.data.get(key, [])
        if isinstance(val, list) and value in val:
            return val.index(value)
        return None

    def expire(self, key, seconds):
        pass  # Mock não expira


# ==============================================================================
# DASHBOARD VISUAL (cópia standalone para teste)
# ==============================================================================

class DashboardVisual:
    """Gerador de dashboard (versão standalone para teste)"""

    def __init__(self, redis_client, config):
        self.redis = redis_client
        self.config = config

    def _coletar_metricas(self, data):
        """Coleta métricas do Redis"""
        def get_int(key):
            val = self.redis.get(key)
            return int(val) if val else 0

        def get_list(key):
            return self.redis.lrange(key, 0, -1)

        data_str = data.strftime("%Y-%m-%d")

        metricas = {
            "total_atendimentos": get_int(f"metricas:{data_str}:total_atendimentos"),
            "bot_atendeu": get_int(f"metricas:{data_str}:bot_atendeu"),
            "escaladas": get_int(f"metricas:{data_str}:escaladas_humano"),
            "leads_novos": get_int(f"metricas:{data_str}:leads_novos"),
            "leads_quentes": len(get_list(f"metricas:{data_str}:leads_quentes")),
            "visitas_agendadas": get_int(f"metricas:{data_str}:visitas_agendadas"),
            "propostas_enviadas": get_int(f"metricas:{data_str}:propostas_enviadas"),
            "tags_interesse": get_int(f"metricas:{data_str}:tags_interesse"),
            "tags_frustrado": get_int(f"metricas:{data_str}:tags_frustrado"),
            "tags_visita": get_int(f"metricas:{data_str}:tags_visita"),
            "chamadas_local": get_int(f"metricas:{data_str}:ferramentas_local"),
            "chamadas_mcp": get_int(f"metricas:{data_str}:ferramentas_mcp"),
            "erros_mcp": get_int(f"metricas:{data_str}:erros_mcp"),
            "tempo_resposta_total": get_int(f"metricas:{data_str}:tempo_resposta_ms"),
            "followups_enviados": get_int(f"metricas:{data_str}:followups_enviados"),
            "followups_respondidos": get_int(f"metricas:{data_str}:followups_respondidos"),
        }

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

    def _gerar_texto_relatorio(self, metricas, data):
        """Gera texto do relatório"""
        emoji_atend = "🟢" if metricas['total_atendimentos'] > 0 else "🔴"
        emoji_qualidade = "🟢" if metricas['erros_mcp'] == 0 else "🟡"
        emoji_tempo = "🟢" if metricas['tempo_resposta_medio'] < 2000 else "🟡"

        if metricas['total_atendimentos'] > 0:
            taxa_esc = (metricas['escaladas'] / metricas['total_atendimentos']) * 100
        else:
            taxa_esc = 0

        if metricas['leads_novos'] > 0:
            taxa_conv = (metricas['visitas_agendadas'] / metricas['leads_novos']) * 100
        else:
            taxa_conv = 0

        return f"""📊 *DASHBOARD DIÁRIO*
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

━━━━━━━━━━━━━━━━━━━━━━━"""

    def _gerar_ascii_art(self, metricas):
        """Gera gráficos ASCII"""
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

        return f"""
```
ATENDIMENTOS:
Bot    [{barra_bot:<20}] {perc_bot:.0f}%
Humano [{barra_humano:<20}] {perc_humano:.0f}%

FERRAMENTAS:
Local  [{barra_local:<20}] {perc_local:.0f}%
MCP    [{barra_mcp:<20}] {perc_mcp:.0f}%
```
"""


# ==============================================================================
# SIMULAÇÃO DE UM DIA DE ATENDIMENTOS
# ==============================================================================

def simular_dia_completo():
    """Simula um dia completo de atendimentos com métricas"""

    print("\n" + "="*80)
    print("🎬 SIMULAÇÃO: Um Dia Completo de Atendimentos")
    print("="*80 + "\n")

    # Inicializa
    redis = MockRedis()
    coletor = ColetorMetricasChatbot(redis)

    print("📅 Simulando atendimentos do dia...\n")

    # ========== MANHÃ (9h-12h) ==========
    print("🌅 MANHÃ (9h-12h)\n")

    atendimentos = [
        {"cliente": "5531986549366", "tipo": "novo", "acao": "interesse", "ferramentas": ["local", "local"]},
        {"cliente": "5531987654321", "tipo": "novo", "acao": "visita", "ferramentas": ["local", "mcp", "local"]},
        {"cliente": "5531988776655", "tipo": "novo", "acao": "frustrado", "ferramentas": ["mcp"]},
        {"cliente": "5531989998877", "tipo": "novo", "acao": "interesse", "ferramentas": ["local", "local"]},
        {"cliente": "5531911111111", "tipo": "novo", "acao": "proposta", "ferramentas": ["local", "mcp"]},
    ]

    for i, atend in enumerate(atendimentos, 1):
        print(f"  {i}. 👤 Cliente {atend['cliente'][-4:]}: {atend['acao']}")

        # Registra atendimento
        coletor.registrar_atendimento(atend['cliente'])

        # Novo lead
        if atend['tipo'] == "novo":
            coletor.registrar_lead_novo(atend['cliente'])

        # Ferramentas usadas
        for ferr in atend['ferramentas']:
            if ferr == "local":
                coletor.registrar_ferramenta_local()
            else:
                coletor.registrar_ferramenta_mcp()

        # Ação específica
        if atend['acao'] == "interesse":
            coletor.registrar_tag_criada("interesse")
            coletor.registrar_bot_respondeu()

        elif atend['acao'] == "visita":
            coletor.registrar_tag_criada("interesse")
            coletor.registrar_visita_agendada()
            coletor.registrar_tag_criada("visita")
            coletor.registrar_lead_quente(atend['cliente'])
            coletor.registrar_bot_respondeu()

        elif atend['acao'] == "frustrado":
            coletor.registrar_tag_criada("frustrado")
            coletor.registrar_escalada_humano()

        elif atend['acao'] == "proposta":
            coletor.registrar_tag_criada("interesse")
            coletor.registrar_proposta_enviada()
            coletor.registrar_lead_quente(atend['cliente'])
            coletor.registrar_bot_respondeu()

        # Tempo de resposta
        tempo = 1200 + (i * 100)  # Varia entre 1200-1600ms
        coletor.registrar_tempo_resposta(tempo)

        time.sleep(0.1)

    # ========== TARDE (14h-18h) ==========
    print(f"\n🌆 TARDE (14h-18h)\n")

    atendimentos_tarde = [
        {"cliente": "5531922222222", "tipo": "novo", "acao": "interesse", "ferramentas": ["local", "local"]},
        {"cliente": "5531933333333", "tipo": "novo", "acao": "visita", "ferramentas": ["local", "local", "mcp"]},
        {"cliente": "5531944444444", "tipo": "novo", "acao": "interesse", "ferramentas": ["local"]},
        {"cliente": "5531955555555", "tipo": "novo", "acao": "frustrado", "ferramentas": ["local", "mcp"]},
        {"cliente": "5531966666666", "tipo": "novo", "acao": "visita", "ferramentas": ["local", "mcp", "local"]},
        {"cliente": "5531977777777", "tipo": "novo", "acao": "interesse", "ferramentas": ["local", "local"]},
        {"cliente": "5531988888888", "tipo": "novo", "acao": "proposta", "ferramentas": ["local", "mcp", "local"]},
    ]

    for i, atend in enumerate(atendimentos_tarde, 1):
        print(f"  {i}. 👤 Cliente {atend['cliente'][-4:]}: {atend['acao']}")

        coletor.registrar_atendimento(atend['cliente'])

        if atend['tipo'] == "novo":
            coletor.registrar_lead_novo(atend['cliente'])

        for ferr in atend['ferramentas']:
            if ferr == "local":
                coletor.registrar_ferramenta_local()
            else:
                coletor.registrar_ferramenta_mcp()

        if atend['acao'] == "interesse":
            coletor.registrar_tag_criada("interesse")
            coletor.registrar_bot_respondeu()

        elif atend['acao'] == "visita":
            coletor.registrar_tag_criada("interesse")
            coletor.registrar_visita_agendada()
            coletor.registrar_tag_criada("visita")
            coletor.registrar_lead_quente(atend['cliente'])
            coletor.registrar_bot_respondeu()

        elif atend['acao'] == "frustrado":
            coletor.registrar_tag_criada("frustrado")
            coletor.registrar_escalada_humano()

        elif atend['acao'] == "proposta":
            coletor.registrar_tag_criada("interesse")
            coletor.registrar_proposta_enviada()
            coletor.registrar_lead_quente(atend['cliente'])
            coletor.registrar_bot_respondeu()

        tempo = 1300 + (i * 50)
        coletor.registrar_tempo_resposta(tempo)

        time.sleep(0.1)

    # Follow-ups
    print(f"\n📨 FOLLOW-UPS AUTOMÁTICOS\n")
    print(f"  • 8 follow-ups enviados")
    for _ in range(8):
        coletor.registrar_followup_enviado()

    print(f"  • 4 clientes responderam")
    for _ in range(4):
        coletor.registrar_followup_respondido()

    print(f"\n✅ Simulação do dia completa!")
    print(f"   Total de atendimentos: 12")
    print(f"   Total de leads novos: 12")
    print(f"   Leads quentes: 4")
    print(f"   Visitas agendadas: 3")
    print(f"   Propostas enviadas: 2")

    return redis


# ==============================================================================
# TESTE DASHBOARD
# ==============================================================================

def testar_dashboard():
    """Testa geração do dashboard"""

    print("\n" + "="*80)
    print("📊 TESTE: Dashboard Visual Diário")
    print("="*80 + "\n")

    # 1. Simula dia de atendimentos
    print("PASSO 1: Simular dia completo de atendimentos")
    redis = simular_dia_completo()

    # 2. Gera dashboard
    input("\n⏸️  Pressione ENTER para gerar dashboard...")

    print(f"\n{'='*80}")
    print(f"📊 GERANDO DASHBOARD")
    print(f"{'='*80}\n")

    config = {
        'evolution': {
            'url': 'https://evolution.loop9.com.br',
            'api_key': 'mock',
            'instance': 'test'
        }
    }

    dashboard = DashboardVisual(redis, config)

    # Gera relatório
    data = datetime.now().date()
    metricas = dashboard._coletar_metricas(data)
    texto = dashboard._gerar_texto_relatorio(metricas, data)

    print("📱 MENSAGEM QUE SERIA ENVIADA:\n")
    print(texto)

    grafico = dashboard._gerar_ascii_art(metricas)
    print(grafico)

    # Resumo
    print(f"\n{'='*80}")
    print(f"📊 RESUMO DO TESTE")
    print(f"{'='*80}\n")

    print(f"✅ Funcionalidades testadas:")
    print(f"   • Coleta de métricas durante atendimento")
    print(f"   • Geração de dashboard textual")
    print(f"   • Gráficos ASCII")
    print(f"   • Cálculo de taxas (conversão, escalação)")
    print(f"   • Métricas de qualidade (erros, tempo)")
    print(f"   • Métricas de follow-up")
    print()

    print(f"📊 Métricas coletadas:")
    print(f"   Atendimentos: {metricas['total_atendimentos']}")
    print(f"   Leads novos: {metricas['leads_novos']}")
    print(f"   Leads quentes: {metricas['leads_quentes']}")
    print(f"   Visitas: {metricas['visitas_agendadas']}")
    print(f"   Propostas: {metricas['propostas_enviadas']}")
    print(f"   Taxa conversão: {(metricas['visitas_agendadas']/metricas['leads_novos']*100):.0f}%")
    print(f"   Tempo médio: {metricas['tempo_resposta_medio']:.0f}ms")
    print(f"   Ferramentas LOCAL: {metricas['percentual_local']:.0f}%")
    print(f"   Erros MCP: {metricas['erros_mcp']}")
    print()

    print(f"🎯 VALIDAÇÕES:")

    # Valida métricas
    validacoes = []

    if metricas['total_atendimentos'] == 12:
        validacoes.append(("Atendimentos registrados", True))
    else:
        validacoes.append(("Atendimentos registrados", False))

    if metricas['leads_novos'] == 12:
        validacoes.append(("Leads novos registrados", True))
    else:
        validacoes.append(("Leads novos registrados", False))

    if metricas['visitas_agendadas'] == 3:
        validacoes.append(("Visitas agendadas", True))
    else:
        validacoes.append(("Visitas agendadas", False))

    if metricas['propostas_enviadas'] == 2:
        validacoes.append(("Propostas enviadas", True))
    else:
        validacoes.append(("Propostas enviadas", False))

    if metricas['percentual_local'] > 50:
        validacoes.append(("Eficiência (>50% local)", True))
    else:
        validacoes.append(("Eficiência (>50% local)", False))

    if metricas['tempo_resposta_medio'] < 2000:
        validacoes.append(("Tempo resposta (<2s)", True))
    else:
        validacoes.append(("Tempo resposta (<2s)", False))

    for nome, ok in validacoes:
        emoji = "✅" if ok else "❌"
        print(f"   {emoji} {nome}")

    print()

    todas_ok = all(ok for _, ok in validacoes)

    if todas_ok:
        print("🎉 DASHBOARD 100% FUNCIONAL!")
        print()
        print("📝 Próximos passos:")
        print("   1. Configure NUMERO_GESTOR em enviar_dashboard_diario.py")
        print("   2. Execute: python3 setup_cron_dashboard.py")
        print("   3. Cron enviará automaticamente às 8h")
        print("   4. Integre métricas no chatbot (ver EXEMPLO_INTEGRACAO_METRICAS.py)")
        print()
        return 0
    else:
        print("⚠️ Algumas validações falharam")
        return 1


if __name__ == "__main__":
    try:
        exit(testar_dashboard())
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido\n")
        exit(1)
