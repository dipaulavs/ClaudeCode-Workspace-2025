"""
Integrador de Escalonamento
Orquestra todo o processo de transferência para humano + agendamento
"""

import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

from componentes.escalonamento.triggers import DetectorEscalonamento
from componentes.escalonamento.consulta_agenda import ConsultaAgenda
from componentes.escalonamento.chatwoot_integration import ChatwootEscalonamento
from componentes.escalonamento.notificacao import NotificadorCorretor


class IntegradorEscalonamento:
    """Pipeline completo de escalonamento + agendamento"""

    def __init__(self, redis_client=None, config=None):
        """
        Args:
            redis_client: Cliente Redis
            config: Config completo (com chatwoot, evolution, etc)
        """
        self.detector = DetectorEscalonamento()

        # Agenda: MOCK por padrão, mas pode configurar Google Sheets
        # Para usar Google Sheets: passe sheet_id no config
        sheet_id = config.get('google_sheet_id') if config else None
        if sheet_id:
            print(f"📊 Usando Google Sheets: {sheet_id[:15]}...")
            self.agenda = ConsultaAgenda(use_mock=False, sheet_id=sheet_id)
        else:
            print("📊 Usando agenda MOCK (horários fictícios)")
            self.agenda = ConsultaAgenda(use_mock=True)

        # Passa config de chatwoot para integração
        chatwoot_config = config.get('chatwoot') if config else None
        self.chatwoot = ChatwootEscalonamento(chatwoot_config)

        # Passa config completo para notificador
        self.notificador = NotificadorCorretor(config)

        self.redis_client = redis_client
        self.config = config

    def processar_mensagem(
        self,
        cliente_numero: str,
        mensagem: str,
        score: int
    ) -> Optional[str]:
        """
        Verifica se deve escalonar e retorna resposta

        Args:
            cliente_numero: Número do cliente
            mensagem: Mensagem recebida
            score: Score atual do lead

        Returns:
            Mensagem de resposta ou None (se não escalonar)
        """
        # Verifica se bot está em standby
        if self.redis_client.get(f"bot_standby:{cliente_numero}") == "true":
            return None  # Bot não responde, aguarda corretor

        # Detecta trigger
        trigger = self.detector.detectar_trigger(mensagem, score)

        if not trigger:
            return None  # Não escalonar

        # ESCALONAR
        return self.escalonar(cliente_numero, trigger, score)

    def escalonar(
        self,
        cliente_numero: str,
        trigger: str,
        score: int
    ) -> str:
        """
        Executa escalonamento completo

        Args:
            cliente_numero: Número do cliente
            trigger: Trigger detectado
            score: Score do lead

        Returns:
            Mensagem de resposta para cliente
        """
        print(f"\n🔔 INICIANDO ESCALONAMENTO")
        print(f"Cliente: {cliente_numero}")
        print(f"Trigger: {trigger}")
        print(f"Score: {score}")

        # 1. Busca conversa no Chatwoot
        conv_id = self.chatwoot.buscar_conversa_id(cliente_numero)

        if not conv_id:
            print("⚠️ Conversa não encontrada no Chatwoot")
            # Escalonamento sem Chatwoot (só notifica)
            return self._escalonar_sem_chatwoot(cliente_numero, trigger, score)

        # 2. Aplica tag
        self.chatwoot.aplicar_tag_escalonamento(conv_id, trigger)

        # 3. Adiciona nota privada
        self.chatwoot.criar_nota_escalonamento(conv_id, trigger, score, cliente_numero)

        # 4. Busca corretor disponível
        corretor = self.notificador.buscar_corretor_disponivel()

        # 5. Atribui no Chatwoot
        self.chatwoot.atribuir_corretor(conv_id, corretor["chatwoot_id"])

        # 6. Gera link da conversa
        link_conversa = self.chatwoot.get_link_conversa(conv_id)

        # 7. Notifica corretor via WhatsApp
        self.notificador.notificar_whatsapp(
            corretor=corretor,
            cliente_numero=cliente_numero,
            trigger=trigger,
            score=score,
            conv_id=conv_id,
            link_conversa=link_conversa
        )

        # 8. Registra atribuição
        self.notificador.registrar_atribuicao(corretor, cliente_numero, trigger)

        # 9. Bot em standby (24h)
        self.redis_client.setex(f"bot_standby:{cliente_numero}", 86400, "true")

        # 10. Mensagem ao cliente
        mensagem = self.detector.get_mensagem_escalonamento(trigger)

        print(f"✅ Escalonamento concluído para {corretor['nome']}\n")

        return mensagem

    def _escalonar_sem_chatwoot(
        self,
        cliente_numero: str,
        trigger: str,
        score: int
    ) -> str:
        """Escalonamento simplificado (sem Chatwoot)"""

        # Busca corretor
        corretor = self.notificador.buscar_corretor_disponivel()

        # Notifica (sem link Chatwoot)
        mensagem_corretor = f"""
🔔 *NOVO ATENDIMENTO*

*Cliente:* {cliente_numero}
*Trigger:* {trigger}
*Score:* {score}

⚠️ Conversa não encontrada no Chatwoot
        """.strip()

        # Envia via Evolution API
        try:
            from tools.send_message_evolution import enviar_mensagem
            enviar_mensagem(corretor["whatsapp"], mensagem_corretor)
        except Exception as e:
            print(f"❌ Erro ao notificar: {e}")

        # Bot em standby
        self.redis_client.setex(f"bot_standby:{cliente_numero}", 86400, "true")

        return self.detector.get_mensagem_escalonamento(trigger)

    def sugerir_horarios(
        self,
        cliente_numero: str,
        imovel_id: Optional[str] = None
    ) -> str:
        """
        Sugere horários disponíveis para visita

        Args:
            cliente_numero: Número do cliente
            imovel_id: ID do imóvel (opcional)

        Returns:
            Mensagem com horários ou mensagem de erro
        """
        horarios = self.agenda.buscar_horarios_disponiveis(dias_frente=3, limite=3)

        if not horarios:
            return "No momento não temos horários disponíveis. Vou chamar um corretor pra você! 👍"

        # Formata mensagem
        opcoes = []
        for i, h in enumerate(horarios, 1):
            opcoes.append(f"{i}️⃣ {h['data_formatada']} às {h['hora']}")

        mensagem = "*Posso agendar pra:*\n\n" + "\n".join(opcoes) + "\n\n_Qual prefere?_"

        # Salva opções no Redis (pra processar resposta)
        self.redis_client.setex(
            f"opcoes_horario:{cliente_numero}",
            3600,  # 1 hora
            json.dumps(horarios, default=str)
        )

        return mensagem

    def confirmar_agendamento(
        self,
        cliente_numero: str,
        escolha: str,
        imovel_id: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Confirma agendamento escolhido pelo cliente

        Args:
            cliente_numero: Número do cliente
            escolha: Resposta do cliente (ex: "1", "amanhã 10h")
            imovel_id: ID do imóvel

        Returns:
            (sucesso, mensagem)
        """
        # Recupera opções salvas
        opcoes_json = self.redis_client.get(f"opcoes_horario:{cliente_numero}")

        if not opcoes_json:
            return False, "Ops! As opções expiraram. Me fala de novo quando você quer visitar? 📅"

        horarios = json.loads(opcoes_json)

        # Extrai número da escolha (1, 2, 3)
        escolha_numero = self._extrair_numero(escolha)

        if not escolha_numero or escolha_numero > len(horarios):
            return False, "Não entendi... Pode escolher um dos números? (1, 2 ou 3)"

        # Horário escolhido (índice 0)
        escolha_index = escolha_numero - 1
        horario = horarios[escolha_index]

        # Converte de volta para datetime
        if isinstance(horario['data'], str):
            horario['data'] = datetime.strptime(horario['data'], '%Y-%m-%d').date()

        # Agenda na planilha
        sucesso = self.agenda.agendar_visita(cliente_numero, imovel_id or "N/A", horario)

        if not sucesso:
            return False, "Ops! Erro ao agendar. Vou chamar um corretor pra você! 👍"

        # Agenda follow-ups (lembretes)
        self._agendar_followups(cliente_numero, horario, imovel_id)

        # Limpa opções do Redis
        self.redis_client.delete(f"opcoes_horario:{cliente_numero}")

        # Mensagem confirmação
        mensagem = f"""
✅ *Agendado!*

📅 {horario['data_formatada']} às {horario['hora']}

Te mando lembretes antes! 🔔

_Endereço: [inserir endereço do imóvel]_
        """.strip()

        return True, mensagem

    def _agendar_followups(
        self,
        cliente_numero: str,
        horario: Dict,
        imovel_id: Optional[str]
    ):
        """Agenda follow-ups automáticos (lembretes)"""

        try:
            # Importa sistema de follow-up (se existir)
            from componentes.followup import SistemaFollowUp

            followup = SistemaFollowUp()

            # Data/hora da visita
            data_visita = horario['data']
            hora_visita = horario['hora']
            data_hora_visita = datetime.combine(
                data_visita,
                datetime.strptime(hora_visita, '%H:%M').time()
            )

            # 1. Lembrete 24h antes
            followup.agendar(
                cliente_numero=cliente_numero,
                tipo="lembrete_visita_24h",
                contexto={
                    "data_visita": data_hora_visita.strftime('%d/%m/%Y'),
                    "hora": hora_visita,
                    "imovel_id": imovel_id
                }
            )

            # 2. Lembrete 2h antes
            followup.agendar(
                cliente_numero=cliente_numero,
                tipo="lembrete_visita_2h",
                contexto={
                    "data_visita": data_hora_visita.strftime('%d/%m/%Y'),
                    "hora": hora_visita,
                    "imovel_id": imovel_id
                }
            )

            # 3. Pós-visita (4h depois)
            followup.agendar(
                cliente_numero=cliente_numero,
                tipo="pos_visita",
                contexto={
                    "data_visita": data_hora_visita.strftime('%d/%m/%Y'),
                    "imovel_id": imovel_id
                }
            )

            print(f"✅ Follow-ups agendados para {cliente_numero}")

        except Exception as e:
            print(f"⚠️ Erro ao agendar follow-ups: {e}")

    def _extrair_numero(self, texto: str) -> Optional[int]:
        """Extrai número da resposta do cliente"""
        import re

        # Busca primeiro número
        match = re.search(r'\d+', texto)

        if match:
            return int(match.group())

        return None
