"""
Gerador de relatórios diários e semanais
"""

import sys
import os
from datetime import datetime, date
from typing import Optional

# Adiciona diretório raiz ao path
sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')

from componentes.relatorios.metricas import ColetorMetricas


class GeradorRelatorio:
    """
    Gera relatórios consolidados de performance do chatbot
    """

    def __init__(self):
        """Inicializa gerador"""
        self.coletor = ColetorMetricas()

    def gerar_relatorio_diario(self, data: Optional[date] = None) -> str:
        """
        Gera relatório consolidado do dia

        Args:
            data: Data do relatório (padrão: hoje)

        Returns:
            Relatório formatado em texto
        """
        if data is None:
            data = datetime.now().date()

        # 1. Buscar métricas
        leads_total = self.coletor.buscar("leads_total", data)
        leads_novos = self.coletor.buscar("leads_novos_hoje", data)
        leads_quentes_raw = self.coletor.buscar("leads_quentes", data)

        bot_atendeu = self.coletor.buscar("bot_atendeu", data)
        escaladas = self.coletor.buscar("escaladas", data)

        visitas = self.coletor.buscar("visitas_agendadas", data)
        propostas = self.coletor.buscar("propostas_enviadas", data)

        followups_env = self.coletor.buscar("followups_enviados", data)
        followups_resp = self.coletor.buscar("followups_respondidos", data)

        # 2. Processar leads quentes
        leads_quentes = []
        if leads_quentes_raw:
            for numero in leads_quentes_raw:
                numero_str = numero.decode() if isinstance(numero, bytes) else numero
                leads_quentes.append(numero_str)

        # 3. Calcular taxas
        taxa_bot = self._calcular_taxa(bot_atendeu, bot_atendeu + escaladas)
        taxa_escalada = 100 - taxa_bot
        taxa_lead_visita = self._calcular_taxa(visitas, leads_novos)
        taxa_visita_proposta = self._calcular_taxa(propostas, visitas)
        taxa_followup = self._calcular_taxa(followups_resp, followups_env)

        # 4. Formatar relatório
        relatorio = f"""📊 RELATÓRIO DIÁRIO - {data.strftime('%d/%m/%Y')}

👥 LEADS:
   • Total: {leads_total}
   • Novos hoje: {leads_novos}
   • Quentes: {len(leads_quentes)} 🔥

🤖 BOT:
   • Conversas atendidas: {bot_atendeu} ({taxa_bot:.0f}%)
   • Escaladas para humano: {escaladas} ({taxa_escalada:.0f}%)

🏠 INTERESSE:
   • Visitas agendadas: {visitas}
   • Propostas enviadas: {propostas}

💰 CONVERSÃO:
   • Lead → Visita: {taxa_lead_visita:.0f}%
   • Visita → Proposta: {taxa_visita_proposta:.0f}%

📨 FOLLOW-UPS:
   • Enviados: {followups_env}
   • Respondidos: {followups_resp} ({taxa_followup:.0f}%)"""

        # 5. Adicionar leads quentes (top 5)
        if leads_quentes:
            relatorio += "\n\n🔥 LEADS QUENTES HOJE:"

            # Buscar scores
            leads_com_score = []

            try:
                sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')
                from componentes.score import SistemaScore

                score_system = SistemaScore()

                for numero in leads_quentes[:10]:  # Max 10
                    score = score_system.get_score(numero)
                    if score >= 70:  # Confirma que é quente
                        leads_com_score.append((numero, score))

                # Ordenar por score
                leads_com_score.sort(key=lambda x: x[1], reverse=True)

                for i, (numero, score) in enumerate(leads_com_score[:5], 1):
                    relatorio += f"\n   {i}. {numero} (Score {score})"

            except Exception as e:
                # Fallback sem scores
                for i, numero in enumerate(leads_quentes[:5], 1):
                    relatorio += f"\n   {i}. {numero}"

        # 6. Adicionar imóveis mais procurados
        imoveis_top_raw = self.coletor.buscar("imoveis_mais_procurados", data)

        if imoveis_top_raw:
            relatorio += "\n\n🏘️ IMÓVEIS MAIS PROCURADOS:"

            for imovel_id, views in imoveis_top_raw[:3]:
                imovel_str = imovel_id.decode() if isinstance(imovel_id, bytes) else imovel_id
                relatorio += f"\n   • {imovel_str}: {int(views)} visualizações"

        return relatorio

    def enviar_relatorio(self, relatorio: str, numero_gestor: str) -> bool:
        """
        Envia relatório via WhatsApp

        Args:
            relatorio: Texto do relatório
            numero_gestor: Número do WhatsApp do gestor

        Returns:
            True se enviou com sucesso
        """
        try:
            sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace')
            from scripts.whatsapp.send_message import main as enviar_mensagem

            # Simula argumentos do script
            import argparse

            # Cria namespace com argumentos
            args = argparse.Namespace(
                phone=numero_gestor,
                message=relatorio
            )

            # Envia (script usa sys.argv, então simulamos)
            import subprocess

            script_path = '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/scripts/whatsapp/send_message.py'

            resultado = subprocess.run(
                ['python3', script_path, '--phone', numero_gestor, '--message', relatorio],
                capture_output=True,
                text=True
            )

            if resultado.returncode == 0:
                print(f"✅ Relatório enviado para {numero_gestor}")
                return True
            else:
                print(f"❌ Erro ao enviar relatório: {resultado.stderr}")
                return False

        except Exception as e:
            print(f"❌ Erro ao enviar relatório: {str(e)}")
            return False

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
