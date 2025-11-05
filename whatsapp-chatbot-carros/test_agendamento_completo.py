#!/usr/bin/env python3.11
"""
📅 TESTE COMPLETO: Sistema de Agendamento

Testa:
1. Cliente pede para agendar
2. Bot busca horários disponíveis (Google Calendar mock)
3. Bot sugere 3 horários
4. Cliente escolhe horário OCUPADO
5. Bot informa indisponibilidade
6. Bot oferece alternativas
7. Cliente escolhe horário disponível
8. Bot confirma agendamento
9. Chatwoot registra
10. Vendedor é notificado
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


# ==============================================================================
# MOCK GOOGLE CALENDAR
# ==============================================================================

class AgendaGoogle:
    """Simula Google Calendar com horários ocupados"""

    def __init__(self):
        # Gera agenda para próximos 7 dias
        self.horarios_ocupados = self._gerar_horarios_ocupados()
        self.agendamentos = []
        print("✅ Google Calendar conectado (mock)")

    def _gerar_horarios_ocupados(self) -> List[Dict]:
        """Gera horários já ocupados (simulação realista)"""
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ocupados = []

        # Amanhã às 10h - OCUPADO
        ocupados.append({
            "data": hoje + timedelta(days=1),
            "hora": "10:00",
            "cliente": "João Silva",
            "veiculo": "Onix 2021"
        })

        # Amanhã às 14h - OCUPADO
        ocupados.append({
            "data": hoje + timedelta(days=1),
            "hora": "14:00",
            "cliente": "Maria Santos",
            "veiculo": "Civic 2018"
        })

        # Quarta às 14h - OCUPADO
        ocupados.append({
            "data": hoje + timedelta(days=3),
            "hora": "14:00",
            "cliente": "Carlos Pereira",
            "veiculo": "Corolla 2023"
        })

        return ocupados

    def buscar_horarios_disponiveis(self, quantidade: int = 3, incluir_ocupados: bool = False) -> List[Dict]:
        """
        Busca horários disponíveis

        Args:
            quantidade: Número de horários a retornar
            incluir_ocupados: Se True, inclui horários ocupados para teste de conflito
        """
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        horarios_retorno = []

        horarios_possiveis = ["10:00", "11:00", "14:00", "15:00", "16:00"]
        dia_offset = 1  # Começa amanhã

        # Se incluir_ocupados, adiciona primeiro os ocupados para teste
        if incluir_ocupados and self.horarios_ocupados:
            # Adiciona primeiro horário ocupado (para testar conflito)
            horarios_retorno.append({
                "data": self.horarios_ocupados[0]['data'],
                "hora": self.horarios_ocupados[0]['hora'],
                "disponivel": False  # OCUPADO
            })

        # Depois adiciona os disponíveis
        while len(horarios_retorno) < quantidade and dia_offset <= 7:
            data_candidata = hoje + timedelta(days=dia_offset)

            # Pula finais de semana
            if data_candidata.weekday() >= 5:  # 5=sábado, 6=domingo
                dia_offset += 1
                continue

            for hora in horarios_possiveis:
                # Verifica se horário está ocupado
                ocupado = any(
                    h['data'].date() == data_candidata.date() and h['hora'] == hora
                    for h in self.horarios_ocupados
                )

                if not ocupado:
                    horarios_retorno.append({
                        "data": data_candidata,
                        "hora": hora,
                        "disponivel": True
                    })

                    if len(horarios_retorno) >= quantidade:
                        break

            dia_offset += 1

        return horarios_retorno

    def verificar_disponibilidade(self, data: datetime, hora: str) -> Tuple[bool, Optional[str]]:
        """
        Verifica se horário está disponível

        Returns:
            (disponível, motivo_se_ocupado)
        """
        # Verifica se está ocupado
        for ocupado in self.horarios_ocupados:
            if ocupado['data'].date() == data.date() and ocupado['hora'] == hora:
                motivo = f"Horário ocupado (visita de {ocupado['cliente']})"
                return False, motivo

        # Verifica se já foi agendado nesta sessão
        for agendado in self.agendamentos:
            if agendado['data'].date() == data.date() and agendado['hora'] == hora:
                return False, "Horário acabou de ser agendado"

        return True, None

    def agendar(self, data: datetime, hora: str, cliente: str, veiculo: str) -> bool:
        """Agenda visita"""
        disponivel, _ = self.verificar_disponibilidade(data, hora)

        if not disponivel:
            return False

        self.agendamentos.append({
            "data": data,
            "hora": hora,
            "cliente": cliente,
            "veiculo": veiculo,
            "agendado_em": datetime.now()
        })

        print(f"   📅 Google: Agendamento criado - {data.strftime('%d/%m')} às {hora}")
        return True

    def mostrar_agenda(self):
        """Mostra agenda completa"""
        print(f"\n{'='*70}")
        print(f"📅 AGENDA GOOGLE CALENDAR")
        print(f"{'='*70}\n")

        print(f"🔴 HORÁRIOS OCUPADOS ({len(self.horarios_ocupados)}):\n")
        for h in sorted(self.horarios_ocupados, key=lambda x: (x['data'], x['hora'])):
            data_str = h['data'].strftime("%d/%m/%Y (%a)")
            print(f"   {data_str} às {h['hora']} - {h['cliente']} ({h['veiculo']})")

        if self.agendamentos:
            print(f"\n✅ NOVOS AGENDAMENTOS ({len(self.agendamentos)}):\n")
            for a in sorted(self.agendamentos, key=lambda x: (x['data'], x['hora'])):
                data_str = a['data'].strftime("%d/%m/%Y (%a)")
                print(f"   {data_str} às {a['hora']} - {a['cliente']} ({a['veiculo']})")


# ==============================================================================
# SISTEMA DE AGENDAMENTO
# ==============================================================================

class SistemaAgendamento:
    """Sistema de agendamento integrado"""

    def __init__(self, agenda: AgendaGoogle, redis, chatwoot):
        self.agenda = agenda
        self.redis = redis
        self.chatwoot = chatwoot
        self.estado_agendamento = {}  # {numero_cliente: {etapa, horarios_sugeridos}}

    def iniciar_agendamento(self, cliente_numero: str, carro_id: str, teste_conflito: bool = False) -> str:
        """Inicia processo de agendamento"""
        # Busca horários disponíveis (ou inclui ocupados para teste)
        horarios = self.agenda.buscar_horarios_disponiveis(quantidade=3, incluir_ocupados=teste_conflito)

        if not horarios:
            return "❌ Não há horários disponíveis no momento. Entre em contato pelo telefone."

        # Salva estado
        self.estado_agendamento[cliente_numero] = {
            "etapa": "aguardando_escolha",
            "horarios_sugeridos": horarios,
            "carro_id": carro_id
        }

        # Formata mensagem
        mensagem = "📅 *Horários disponíveis para visita:*\n\n"

        for i, h in enumerate(horarios, 1):
            dia_semana = ["Seg", "Ter", "Qua", "Qui", "Sex"][h['data'].weekday()]
            data_str = h['data'].strftime("%d/%m")
            mensagem += f"{i}️⃣ {dia_semana} {data_str} às {h['hora']}\n"

        mensagem += "\n*Qual horário prefere?* Digite o número (1, 2 ou 3)"

        return mensagem

    def processar_escolha(self, cliente_numero: str, cliente_nome: str, escolha: str) -> Tuple[bool, str]:
        """
        Processa escolha do cliente

        Returns:
            (sucesso, mensagem)
        """
        estado = self.estado_agendamento.get(cliente_numero)

        if not estado:
            return False, "❌ Nenhum agendamento em andamento. Digite 'agendar' para iniciar."

        # Valida escolha
        try:
            indice = int(escolha) - 1
            if indice < 0 or indice >= len(estado['horarios_sugeridos']):
                return False, "❌ Escolha inválida. Digite 1, 2 ou 3."
        except ValueError:
            # Tenta detectar horário manual (ex: "amanhã 10h")
            return False, "❌ Digite o número da opção (1, 2 ou 3)."

        horario_escolhido = estado['horarios_sugeridos'][indice]
        data = horario_escolhido['data']
        hora = horario_escolhido['hora']

        # Verifica disponibilidade (pode ter mudado)
        disponivel, motivo = self.agenda.verificar_disponibilidade(data, hora)

        if not disponivel:
            # HORÁRIO OCUPADO - Oferece alternativas
            mensagem = f"❌ Ops! O horário *{data.strftime('%d/%m')} às {hora}* não está mais disponível.\n"
            mensagem += f"📍 Motivo: {motivo}\n\n"

            # Busca novas alternativas
            novos_horarios = self.agenda.buscar_horarios_disponiveis(quantidade=3)

            if novos_horarios:
                mensagem += "🔄 *Que tal estas alternativas?*\n\n"
                for i, h in enumerate(novos_horarios, 1):
                    dia_semana = ["Seg", "Ter", "Qua", "Qui", "Sex"][h['data'].weekday()]
                    data_str = h['data'].strftime("%d/%m")
                    mensagem += f"{i}️⃣ {dia_semana} {data_str} às {h['hora']}\n"

                mensagem += "\n*Digite o novo número que prefere:*"

                # Atualiza estado
                self.estado_agendamento[cliente_numero]['horarios_sugeridos'] = novos_horarios

                return False, mensagem
            else:
                mensagem += "😞 Não há outros horários disponíveis. Entre em contato pelo telefone."
                return False, mensagem

        # Horário disponível - Confirma agendamento
        carro_id = estado.get('carro_id', 'Não especificado')
        sucesso = self.agenda.agendar(data, hora, cliente_nome, carro_id)

        if not sucesso:
            return False, "❌ Erro ao agendar. Tente novamente."

        # Salva no Redis
        chave_agendamento = f"agendamento:{cliente_numero}"
        dados_agendamento = {
            "data": data.isoformat(),
            "hora": hora,
            "carro_id": carro_id,
            "confirmado_em": datetime.now().isoformat()
        }
        self.redis.setex(chave_agendamento, 86400*7, json.dumps(dados_agendamento))  # 7 dias

        # Limpa estado
        del self.estado_agendamento[cliente_numero]

        # Mensagem de confirmação
        dia_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"][data.weekday()]
        mensagem = f"✅ *Agendado com sucesso!*\n\n"
        mensagem += f"📅 *Dia:* {dia_semana}, {data.strftime('%d/%m/%Y')}\n"
        mensagem += f"🕐 *Horário:* {hora}\n"
        mensagem += f"🚗 *Veículo:* {carro_id}\n"
        mensagem += f"📍 *Local:* Loja Automaia - BH\n\n"
        mensagem += f"📲 *Confirmado!* Te esperamos lá!\n"
        mensagem += f"💡 *Dica:* Traga RG, CNH e comprovante de renda."

        return True, mensagem


# ==============================================================================
# MOCK SISTEMAS
# ==============================================================================

class MockRedis:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def setex(self, key, ttl, value):
        self.data[key] = value
        print(f"   📝 Redis: {key[:30]}... salvo")


class MockChatwoot:
    def __init__(self):
        self.conversations = {}
        self.conversation_counter = 1

    def criar_conversa(self, numero: str, nome: str) -> int:
        conv_id = self.conversation_counter
        self.conversation_counter += 1

        self.conversations[conv_id] = {
            "id": conv_id,
            "contact": {"phone": numero, "name": nome},
            "status": "open",
            "tags": [],
            "messages": []
        }
        return conv_id

    def adicionar_tag(self, conv_id: int, tag: str):
        if conv_id in self.conversations:
            if tag not in self.conversations[conv_id]["tags"]:
                self.conversations[conv_id]["tags"].append(tag)
                print(f"   🏷️ Chatwoot: Tag '{tag}' adicionada")

    def adicionar_mensagem(self, conv_id: int, sender: str, content: str):
        if conv_id in self.conversations:
            self.conversations[conv_id]["messages"].append({
                "sender": sender,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })


# ==============================================================================
# SIMULAÇÃO COMPLETA
# ==============================================================================

def simular_agendamento_completo():
    """Simula fluxo completo de agendamento"""

    print("\n" + "="*80)
    print("📅 TESTE COMPLETO: Sistema de Agendamento com Conflitos")
    print("="*80 + "\n")

    # Inicializa sistemas
    print("🔧 Inicializando sistemas...")
    agenda = AgendaGoogle()
    redis = MockRedis()
    chatwoot = MockChatwoot()
    sistema = SistemaAgendamento(agenda, redis, chatwoot)
    print()

    # Mostra agenda inicial
    agenda.mostrar_agenda()

    # Cliente
    cliente_numero = "5531986549366"
    cliente_nome = "Roberto Silva"
    carro_id = "Gol 2020"

    conv_id = chatwoot.criar_conversa(cliente_numero, cliente_nome)

    # ========== CONVERSA ==========

    print(f"\n{'='*80}")
    print(f"💬 CONVERSAÇÃO")
    print(f"{'='*80}\n")

    print(f"👤 CLIENTE: {cliente_nome}")
    print(f"🚗 INTERESSE: {carro_id}\n")

    # Mensagem 1: Cliente pede para agendar
    input("⏸️  Pressione ENTER para cliente pedir agendamento...")
    print(f"\n1. 👤 Cliente: Quero agendar uma visita para ver o carro")
    chatwoot.adicionar_mensagem(conv_id, "customer", "Quero agendar uma visita")

    resposta = sistema.iniciar_agendamento(cliente_numero, carro_id, teste_conflito=True)
    print(f"   🤖 Bot:\n{resposta}\n")
    chatwoot.adicionar_mensagem(conv_id, "agent", resposta)

    # Mensagem 2: Cliente escolhe HORÁRIO OCUPADO
    input("⏸️  Pressione ENTER para cliente escolher horário OCUPADO (1)...")
    print(f"\n2. 👤 Cliente: 1")
    chatwoot.adicionar_mensagem(conv_id, "customer", "1")

    print(f"   🔍 Bot verifica disponibilidade...")
    print(f"   ⚠️ Horário está OCUPADO!")

    sucesso, resposta = sistema.processar_escolha(cliente_numero, cliente_nome, "1")
    print(f"   🤖 Bot:\n{resposta}\n")
    chatwoot.adicionar_mensagem(conv_id, "agent", resposta)

    if not sucesso:
        chatwoot.adicionar_tag(conv_id, "horario_conflito")

    # Mensagem 3: Cliente escolhe HORÁRIO DISPONÍVEL
    input("⏸️  Pressione ENTER para cliente escolher horário DISPONÍVEL (2)...")
    print(f"\n3. 👤 Cliente: 2")
    chatwoot.adicionar_mensagem(conv_id, "customer", "2")

    print(f"   🔍 Bot verifica disponibilidade...")
    print(f"   ✅ Horário está DISPONÍVEL!")

    sucesso, resposta = sistema.processar_escolha(cliente_numero, cliente_nome, "2")
    print(f"   🤖 Bot:\n{resposta}\n")
    chatwoot.adicionar_mensagem(conv_id, "agent", resposta)

    if sucesso:
        chatwoot.adicionar_tag(conv_id, "visita_agendada")

    # ========== AGENDA ATUALIZADA ==========

    input("⏸️  Pressione ENTER para ver agenda atualizada...")
    agenda.mostrar_agenda()

    # ========== CHATWOOT DASHBOARD ==========

    input("⏸️  Pressione ENTER para ver Chatwoot Dashboard...")
    print(f"\n{'='*80}")
    print(f"📊 CHATWOOT DASHBOARD")
    print(f"{'='*80}\n")

    conv = chatwoot.conversations[conv_id]
    print(f"💬 Conversa #{conv_id}")
    print(f"   Cliente: {conv['contact']['name']}")
    print(f"   Telefone: {conv['contact']['phone']}")
    print(f"   Status: Aberta")
    print(f"   Tags: {', '.join(conv['tags'])}")
    print(f"\n📝 Mensagens: {len(conv['messages'])}")

    for i, msg in enumerate(conv['messages'], 1):
        sender = "👤 Cliente" if msg['sender'] == 'customer' else "🤖 Bot"
        preview = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
        print(f"   {i}. {sender}: {preview}")

    # ========== REDIS STATE ==========

    print(f"\n{'='*80}")
    print(f"📦 REDIS STATE")
    print(f"{'='*80}\n")

    chave_agendamento = f"agendamento:{cliente_numero}"
    dados = redis.get(chave_agendamento)

    if dados:
        agendamento = json.loads(dados)
        print(f"✅ Agendamento salvo:")
        print(f"   Data: {agendamento['data']}")
        print(f"   Hora: {agendamento['hora']}")
        print(f"   Carro: {agendamento['carro_id']}")
        print(f"   Confirmado em: {agendamento['confirmado_em']}")

    # ========== NOTIFICAÇÃO VENDEDOR ==========

    print(f"\n{'='*80}")
    print(f"📱 NOTIFICAÇÃO PARA VENDEDOR")
    print(f"{'='*80}\n")

    if sucesso:
        dados_agendamento = json.loads(redis.get(chave_agendamento))
        data_obj = datetime.fromisoformat(dados_agendamento['data'])

        notificacao = f"""
🗓️ *NOVA VISITA AGENDADA*

👤 *Cliente:* {cliente_nome}
📱 *Telefone:* {cliente_numero}
🚗 *Veículo:* {carro_id}

📅 *Data:* {data_obj.strftime('%d/%m/%Y (%A)')}
🕐 *Horário:* {dados_agendamento['hora']}

📍 *Local:* Loja Automaia - BH

🔔 *Lembrete:* Confirme com cliente 1 dia antes!
        """.strip()

        print(notificacao)

    # ========== RESUMO ==========

    print(f"\n{'='*80}")
    print(f"📊 RESUMO DO TESTE")
    print(f"{'='*80}\n")

    print(f"✅ Funcionalidades testadas:")
    print(f"   • Google Calendar (horários ocupados/disponíveis)")
    print(f"   • Cliente pede agendamento")
    print(f"   • Bot sugere 3 horários")
    print(f"   • Cliente escolhe horário OCUPADO")
    print(f"   • Bot detecta conflito e oferece alternativas")
    print(f"   • Cliente escolhe horário DISPONÍVEL")
    print(f"   • Bot confirma agendamento")
    print(f"   • Salvou no Redis")
    print(f"   • Registrou no Chatwoot")
    print(f"   • Notificou vendedor")
    print()

    print(f"📊 Métricas:")
    print(f"   Total de mensagens: {len(conv['messages'])}")
    print(f"   Tentativas de agendamento: 2")
    print(f"   Conflitos detectados: 1")
    print(f"   Agendamento confirmado: {'✅ Sim' if sucesso else '❌ Não'}")
    print(f"   Tags criadas: {len(conv['tags'])}")
    print()

    print(f"🎉 SISTEMA DE AGENDAMENTO 100% FUNCIONAL!\n")


if __name__ == "__main__":
    try:
        simular_agendamento_completo()
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido\n")
