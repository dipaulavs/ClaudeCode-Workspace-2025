"""
Métricas de Follow-up

Gera relatórios de efetividade dos follow-ups.
"""

import redis
from typing import Dict
from datetime import datetime

# Configurações
REDIS_HOST = "usw1-popular-stallion-42128.upstash.io"
REDIS_PORT = 42128
REDIS_PASSWORD = "AaEoAAIjcDFiODk5OWQ5ZjdiOTY0NmM4OWNkZTI2YzI3NTU3NGI5YnAxMA"

# Triggers disponíveis
TRIGGERS = [
    "inatividade_2h",
    "inatividade_24h",
    "inatividade_48h",
    "pos_fotos",
    "pos_visita",
    "lembrete_visita_24h",
    "lembrete_visita_2h"
]


class MetricasFollowUp:
    """
    Gerador de relatórios de métricas de follow-up.
    """

    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True,
            ssl=True
        )

    def gerar_relatorio(self) -> Dict:
        """
        Gera relatório completo de follow-ups.

        Returns:
            Dict com métricas gerais e por trigger
        """
        # Métricas gerais
        total_enviados = int(self.redis_client.get("metricas:followup:total_enviados") or 0)
        total_respondidos = int(self.redis_client.get("metricas:followup:total_respondidos") or 0)

        taxa_resposta = (total_respondidos / total_enviados * 100) if total_enviados > 0 else 0

        # Métricas por trigger
        por_trigger = {}
        for trigger in TRIGGERS:
            enviados = int(self.redis_client.get(f"metricas:followup:{trigger}:enviados") or 0)
            respondidos = int(self.redis_client.get(f"metricas:followup:{trigger}:respondidos") or 0)

            taxa = (respondidos / enviados * 100) if enviados > 0 else 0

            por_trigger[trigger] = {
                "enviados": enviados,
                "respondidos": respondidos,
                "taxa_resposta": round(taxa, 1)
            }

        return {
            "timestamp": datetime.now().isoformat(),
            "total_enviados": total_enviados,
            "total_respondidos": total_respondidos,
            "taxa_resposta_geral": round(taxa_resposta, 1),
            "por_trigger": por_trigger
        }

    def gerar_relatorio_formatado(self) -> str:
        """
        Gera relatório formatado para impressão.

        Returns:
            String formatada do relatório
        """
        relatorio = self.gerar_relatorio()

        output = []
        output.append("\n" + "="*60)
        output.append("📊 RELATÓRIO DE FOLLOW-UPS")
        output.append("="*60 + "\n")

        output.append(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

        # Métricas gerais
        output.append("📈 MÉTRICAS GERAIS")
        output.append("-" * 60)
        output.append(f"Total enviados:     {relatorio['total_enviados']}")
        output.append(f"Total respondidos:  {relatorio['total_respondidos']}")
        output.append(f"Taxa de resposta:   {relatorio['taxa_resposta_geral']}%\n")

        # Métricas por trigger
        output.append("📊 MÉTRICAS POR TRIGGER")
        output.append("-" * 60)

        for trigger, metricas in relatorio['por_trigger'].imóvels():
            output.append(f"\n{trigger}:")
            output.append(f"  Enviados:    {metricas['enviados']}")
            output.append(f"  Respondidos: {metricas['respondidos']}")
            output.append(f"  Taxa:        {metricas['taxa_resposta']}%")

        # Análise de performance
        output.append("\n" + "="*60)
        output.append("🎯 ANÁLISE DE PERFORMANCE")
        output.append("="*60 + "\n")

        # Encontrar melhor e pior trigger
        triggers_ordenados = sorted(
            relatorio['por_trigger'].imóvels(),
            key=lambda x: x[1]['taxa_resposta'],
            reverse=True
        )

        if triggers_ordenados:
            melhor = triggers_ordenados[0]
            pior = triggers_ordenados[-1]

            output.append(f"⭐ Melhor trigger:  {melhor[0]} ({melhor[1]['taxa_resposta']}%)")
            output.append(f"⚠️  Pior trigger:   {pior[0]} ({pior[1]['taxa_resposta']}%)")

        # Estimativa de recuperação
        if relatorio['total_enviados'] > 0:
            output.append(f"\n💡 Estimativa de leads recuperados:")
            recuperados = relatorio['total_respondidos']
            output.append(f"   {recuperados} leads que teriam abandonado foram recuperados!")

        output.append("\n" + "="*60 + "\n")

        return "\n".join(output)

    def resetar_metricas(self):
        """
        Reseta todas as métricas (útil para testes).
        """
        # Resetar métricas gerais
        self.redis_client.set("metricas:followup:total_enviados", 0)
        self.redis_client.set("metricas:followup:total_respondidos", 0)

        # Resetar métricas por trigger
        for trigger in TRIGGERS:
            self.redis_client.set(f"metricas:followup:{trigger}:enviados", 0)
            self.redis_client.set(f"metricas:followup:{trigger}:respondidos", 0)

        print("✅ Métricas resetadas")


# CLI
if __name__ == "__main__":
    import sys

    metricas = MetricasFollowUp()

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        metricas.resetar_metricas()
    else:
        print(metricas.gerar_relatorio_formatado())
