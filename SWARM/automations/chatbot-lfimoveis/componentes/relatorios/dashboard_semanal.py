"""
Gerador de dashboard semanal
Enviado toda segunda-feira com resumo da semana
"""

import sys
from datetime import datetime, timedelta, date
from typing import Optional

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')

from componentes.relatorios.metricas import ColetorMetricas


class DashboardSemanal:
    """
    Gera relatório semanal consolidado (segunda a domingo)
    """

    def __init__(self):
        """Inicializa dashboard"""
        self.coletor = ColetorMetricas()

    def gerar_relatorio_semanal(self, data_fim: Optional[date] = None) -> str:
        """
        Gera relatório da semana (seg-dom)

        Args:
            data_fim: Último dia da semana (padrão: domingo anterior)

        Returns:
            Relatório formatado em texto
        """
        if data_fim is None:
            hoje = datetime.now().date()
            # Último domingo
            dias_desde_domingo = (hoje.weekday() + 1) % 7
            data_fim = hoje - timedelta(days=dias_desde_domingo)

        # Calcula início da semana (segunda-feira)
        inicio_semana = data_fim - timedelta(days=6)

        # Acumular métricas da semana
        total = {
            "leads": 0,
            "leads_novos": 0,
            "bot_atendeu": 0,
            "escaladas": 0,
            "visitas": 0,
            "propostas": 0,
            "followups": 0,
            "followups_resp": 0,
            "leads_quentes_count": 0
        }

        # Somar métricas dia a dia
        for dia in range(7):
            data = inicio_semana + timedelta(days=dia)

            total["leads"] += self.coletor.buscar("leads_total", data)
            total["leads_novos"] += self.coletor.buscar("leads_novos_hoje", data)
            total["bot_atendeu"] += self.coletor.buscar("bot_atendeu", data)
            total["escaladas"] += self.coletor.buscar("escaladas", data)
            total["visitas"] += self.coletor.buscar("visitas_agendadas", data)
            total["propostas"] += self.coletor.buscar("propostas_enviadas", data)
            total["followups"] += self.coletor.buscar("followups_enviados", data)
            total["followups_resp"] += self.coletor.buscar("followups_respondidos", data)

            # Contar leads quentes
            leads_quentes = self.coletor.buscar("leads_quentes", data)
            total["leads_quentes_count"] += len(leads_quentes) if leads_quentes else 0

        # Calcular taxas
        taxa_bot = self._calcular_taxa(
            total["bot_atendeu"],
            total["bot_atendeu"] + total["escaladas"]
        )

        taxa_lead_visita = self._calcular_taxa(
            total["visitas"],
            total["leads_novos"]
        )

        taxa_visita_proposta = self._calcular_taxa(
            total["propostas"],
            total["visitas"]
        )

        taxa_followup = self._calcular_taxa(
            total["followups_resp"],
            total["followups"]
        )

        taxa_conversao_final = self._calcular_taxa(
            total["propostas"],
            total["leads_novos"]
        )

        # Formatar relatório
        relatorio = f"""📊 RELATÓRIO SEMANAL
{inicio_semana.strftime('%d/%m')} - {data_fim.strftime('%d/%m/%Y')}

📈 RESUMO DA SEMANA:
   • Leads novos: {total["leads_novos"]}
   • Leads quentes: {total["leads_quentes_count"]} 🔥
   • Visitas agendadas: {total["visitas"]}
   • Propostas enviadas: {total["propostas"]}
   • Taxa conversão final: {taxa_conversao_final:.0f}% (lead → proposta)

🤖 PERFORMANCE BOT:
   • Conversas atendidas: {total["bot_atendeu"]} ({taxa_bot:.0f}%)
   • Escaladas: {total["escaladas"]} ({100-taxa_bot:.0f}%)

💰 FUNIL DE CONVERSÃO:
   • Lead → Visita: {taxa_lead_visita:.0f}%
   • Visita → Proposta: {taxa_visita_proposta:.0f}%
   • Lead → Proposta: {taxa_conversao_final:.0f}%

📨 FOLLOW-UPS:
   • Enviados: {total["followups"]}
   • Respondidos: {total["followups_resp"]}
   • Taxa resposta: {taxa_followup:.0f}%"""

        # Adicionar imóveis mais procurados da semana
        imoveis_semana = {}

        for dia in range(7):
            data = inicio_semana + timedelta(days=dia)
            imoveis_dia = self.coletor.buscar("imoveis_mais_procurados", data)

            if imoveis_dia:
                for imovel_id, views in imoveis_dia:
                    imovel_str = imovel_id.decode() if isinstance(imovel_id, bytes) else imovel_id
                    imoveis_semana[imovel_str] = imoveis_semana.get(imovel_str, 0) + int(views)

        if imoveis_semana:
            # Ordenar por views
            imoveis_top = sorted(imoveis_semana.items(), key=lambda x: x[1], reverse=True)

            relatorio += "\n\n🏘️ IMÓVEIS MAIS PROCURADOS DA SEMANA:"

            for i, (imovel_id, views) in enumerate(imoveis_top[:5], 1):
                relatorio += f"\n   {i}. {imovel_id}: {views} visualizações"

        # Adicionar insights
        relatorio += self._gerar_insights(total, taxa_bot, taxa_conversao_final)

        return relatorio

    def _gerar_insights(self, total: dict, taxa_bot: float, taxa_conversao: float) -> str:
        """
        Gera insights baseados nos números

        Args:
            total: Métricas totais
            taxa_bot: Taxa de atendimento do bot
            taxa_conversao: Taxa de conversão final

        Returns:
            Seção de insights
        """
        insights = "\n\n💡 INSIGHTS:"

        # Insight 1: Performance do bot
        if taxa_bot >= 80:
            insights += "\n   ✅ Bot está atendendo maioria das conversas (>80%)"
        elif taxa_bot >= 60:
            insights += "\n   ⚠️ Bot pode ser otimizado (60-80% atendimento)"
        else:
            insights += "\n   ❌ Bot precisa melhorias urgentes (<60% atendimento)"

        # Insight 2: Taxa de conversão
        if taxa_conversao >= 10:
            insights += "\n   ✅ Excelente taxa de conversão (>10%)"
        elif taxa_conversao >= 5:
            insights += "\n   ⚠️ Taxa de conversão aceitável (5-10%)"
        else:
            insights += "\n   ❌ Taxa de conversão baixa (<5%). Revisar abordagem."

        # Insight 3: Follow-ups
        if total["followups"] > 0:
            taxa_followup = (total["followups_resp"] / total["followups"]) * 100
            if taxa_followup >= 30:
                insights += "\n   ✅ Follow-ups efetivos (>30% resposta)"
            else:
                insights += "\n   ⚠️ Follow-ups podem ser otimizados (<30% resposta)"

        return insights

    def _calcular_taxa(self, parte: int, total: int) -> float:
        """
        Calcula percentual

        Args:
            parte: Valor parcial
            total: Valor total

        Returns:
            Percentual (0-100)
        """
        if total == 0:
            return 0.0
        return (parte / total) * 100
