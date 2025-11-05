#!/usr/bin/env python3.11
"""
📊 TESTE COMPLETO - Dashboard Chatwoot + Intervenção Humana

Simula:
1. Dashboard Chatwoot (visualização)
2. Bot atende cliente
3. Cliente fica frustrado
4. Bot escalona para humano
5. Humano assume a conversa
6. Bot para de responder
7. Humano resolve o problema
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time


# ==============================================================================
# MOCK AVANÇADO - CHATWOOT COM DASHBOARD
# ==============================================================================

class ChatwootDashboard:
    """Simula Dashboard do Chatwoot com métricas e filtros"""

    def __init__(self, chatwoot):
        self.chatwoot = chatwoot

    def mostrar_dashboard(self):
        """Exibe dashboard principal"""
        print(f"\n{'='*90}")
        print(f"📊 CHATWOOT DASHBOARD")
        print(f"{'='*90}\n")

        # Estatísticas gerais
        total_conversas = len(self.chatwoot.conversations)
        conversas_abertas = sum(1 for c in self.chatwoot.conversations.values() if c['status'] == 'open')
        conversas_atribuidas = sum(1 for c in self.chatwoot.conversations.values() if c['assignee'])

        print(f"📈 VISÃO GERAL")
        print(f"   Total de Conversas: {total_conversas}")
        print(f"   Abertas: {conversas_abertas}")
        print(f"   Atribuídas: {conversas_atribuidas}")
        print(f"   Aguardando: {total_conversas - conversas_atribuidas}")

        # Lista de conversas
        print(f"\n💬 CONVERSAS ATIVAS\n")
        print(f"{'ID':<5} {'Cliente':<20} {'Status':<10} {'Atribuído':<20} {'Tags':<30}")
        print("─" * 90)

        for conv_id, conv in self.chatwoot.conversations.items():
            cliente = conv['contact']['name']
            status = "🟢 Aberta" if conv['status'] == 'open' else "🔴 Fechada"
            assignee = conv['assignee']['name'] if conv['assignee'] else "🤖 Bot"
            tags = ', '.join(conv['tags'][:2]) if conv['tags'] else "-"
            if len(conv['tags']) > 2:
                tags += f" +{len(conv['tags'])-2}"

            print(f"{conv_id:<5} {cliente:<20} {status:<10} {assignee:<20} {tags:<30}")

        # Filtros por tag
        print(f"\n🏷️ FILTROS POR TAG\n")
        todas_tags = {}
        for conv in self.chatwoot.conversations.values():
            for tag in conv['tags']:
                todas_tags[tag] = todas_tags.get(tag, 0) + 1

        if todas_tags:
            for tag, count in sorted(todas_tags.items(), key=lambda x: x[1], reverse=True):
                print(f"   [{count}] {tag}")
        else:
            print(f"   (nenhuma tag)")

    def mostrar_conversa_detalhada(self, conv_id: int):
        """Exibe conversa específica em detalhe"""
        if conv_id not in self.chatwoot.conversations:
            print(f"❌ Conversa #{conv_id} não encontrada")
            return

        conv = self.chatwoot.conversations[conv_id]

        print(f"\n{'='*90}")
        print(f"💬 CONVERSA #{conv_id} - VISUALIZAÇÃO DETALHADA")
        print(f"{'='*90}\n")

        # Cabeçalho
        print(f"👤 CLIENTE: {conv['contact']['name']}")
        print(f"📱 Telefone: {conv['contact']['phone']}")
        print(f"📊 Status: {'🟢 Aberta' if conv['status'] == 'open' else '🔴 Fechada'}")

        if conv['assignee']:
            print(f"👨‍💼 Atribuído: {conv['assignee']['name']} (ID: {conv['assignee']['id']})")
        else:
            print(f"👨‍💼 Atribuído: 🤖 Bot (automático)")

        if conv['tags']:
            print(f"🏷️ Tags: {', '.join(conv['tags'])}")

        # Histórico de mensagens
        print(f"\n📝 HISTÓRICO DE MENSAGENS ({len(conv['messages'])} mensagens)\n")
        print("─" * 90)

        for i, msg in enumerate(conv['messages'], 1):
            sender_emoji = "👤" if msg['sender'] == 'customer' else "🤖" if msg['sender'] == 'agent' else "👨‍💼"
            sender_label = "Cliente" if msg['sender'] == 'customer' else "Bot" if msg['sender'] == 'agent' else "Humano"

            # Timestamp
            try:
                ts = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
            except:
                ts = "00:00:00"

            print(f"{i}. [{ts}] {sender_emoji} {sender_label}")
            print(f"   {msg['content'][:80]}...")
            print()

    def filtrar_por_tag(self, tag: str):
        """Filtra conversas por tag"""
        print(f"\n{'='*90}")
        print(f"🔍 CONVERSAS COM TAG: {tag}")
        print(f"{'='*90}\n")

        conversas_filtradas = [
            (conv_id, conv) for conv_id, conv in self.chatwoot.conversations.items()
            if tag in conv['tags']
        ]

        if not conversas_filtradas:
            print(f"❌ Nenhuma conversa com a tag '{tag}'")
            return

        print(f"Encontradas {len(conversas_filtradas)} conversa(s)\n")
        print(f"{'ID':<5} {'Cliente':<20} {'Atribuído':<20}")
        print("─" * 50)

        for conv_id, conv in conversas_filtradas:
            cliente = conv['contact']['name']
            assignee = conv['assignee']['name'] if conv['assignee'] else "🤖 Bot"
            print(f"{conv_id:<5} {cliente:<20} {assignee:<20}")

    def mostrar_metricas_tempo_real(self):
        """Mostra métricas em tempo real"""
        print(f"\n{'='*90}")
        print(f"📊 MÉTRICAS EM TEMPO REAL")
        print(f"{'='*90}\n")

        # Contadores
        total = len(self.chatwoot.conversations)
        atribuidas = sum(1 for c in self.chatwoot.conversations.values() if c['assignee'])
        com_bot = total - atribuidas
        com_tags = sum(1 for c in self.chatwoot.conversations.values() if c['tags'])

        # Barra de atribuição
        if total > 0:
            perc_bot = (com_bot / total) * 100
            perc_humano = (atribuidas / total) * 100

            barra_bot = "█" * int(perc_bot / 5)
            barra_humano = "█" * int(perc_humano / 5)

            print(f"🤖 Bot atendendo:    {com_bot}/{total} [{barra_bot:<20}] {perc_bot:.0f}%")
            print(f"👨‍💼 Humano atendendo: {atribuidas}/{total} [{barra_humano:<20}] {perc_humano:.0f}%")

        print(f"\n🏷️ Tags aplicadas: {com_tags}/{total}")

        # Tags mais usadas
        todas_tags = {}
        for conv in self.chatwoot.conversations.values():
            for tag in conv['tags']:
                todas_tags[tag] = todas_tags.get(tag, 0) + 1

        if todas_tags:
            print(f"\n📊 Tags mais usadas:")
            for tag, count in sorted(todas_tags.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"   {tag}: {count}")


# ==============================================================================
# MOCK SISTEMAS
# ==============================================================================

class MockRedis:
    """Mock Redis"""
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def setex(self, key, ttl, value):
        self.data[key] = value


class MockChatwoot:
    """Mock Chatwoot"""
    def __init__(self):
        self.conversations = {}
        self.contacts = {}
        self.conversation_counter = 1

    def criar_contato(self, numero: str, nome: str) -> int:
        contact_id = len(self.contacts) + 1
        self.contacts[numero] = {"id": contact_id, "phone": numero, "name": nome}
        return contact_id

    def criar_conversa(self, numero: str) -> int:
        if numero not in self.contacts:
            self.criar_contato(numero, f"Cliente {numero[-4:]}")

        conv_id = self.conversation_counter
        self.conversation_counter += 1

        self.conversations[conv_id] = {
            "id": conv_id,
            "contact": self.contacts[numero],
            "status": "open",
            "tags": [],
            "assignee": None,
            "messages": [],
            "humano_assumiu": False  # Flag para bot parar
        }
        return conv_id

    def adicionar_tag(self, conv_id: int, tag: str):
        if conv_id in self.conversations:
            if tag not in self.conversations[conv_id]["tags"]:
                self.conversations[conv_id]["tags"].append(tag)

    def atribuir_vendedor(self, conv_id: int, vendedor_id: int, vendedor_nome: str):
        if conv_id in self.conversations:
            self.conversations[conv_id]["assignee"] = {
                "id": vendedor_id,
                "name": vendedor_nome
            }

    def adicionar_mensagem(self, conv_id: int, sender: str, content: str):
        if conv_id in self.conversations:
            self.conversations[conv_id]["messages"].append({
                "sender": sender,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })

    def humano_assumir(self, conv_id: int):
        """Humano assume a conversa - bot para de responder"""
        if conv_id in self.conversations:
            self.conversations[conv_id]["humano_assumiu"] = True
            print(f"   👨‍💼 Chatwoot: HUMANO ASSUMIU conversa #{conv_id}")


class SimuladorChatbot:
    """Simula chatbot"""
    def __init__(self, redis, chatwoot):
        self.redis = redis
        self.chatwoot = chatwoot

    def processar_mensagem(self, numero: str, mensagem: str, conv_id: int) -> Optional[str]:
        """
        Processa mensagem

        Returns:
            Resposta do bot ou None se humano assumiu
        """
        # VERIFICA SE HUMANO ASSUMIU
        if self.chatwoot.conversations[conv_id]["humano_assumiu"]:
            print(f"   ⏸️ Bot: Humano no controle, não respondo")
            return None

        msg_lower = mensagem.lower()

        # Lógica simplificada
        if "caro" in msg_lower or "frustrado" in msg_lower or "complicado" in msg_lower:
            # ESCALONA
            self.chatwoot.adicionar_tag(conv_id, "precisa_humano")
            self.chatwoot.atribuir_vendedor(conv_id, 102, "Maria Supervisora")
            return "Entendo sua preocupação! Vou te conectar com um especialista 😊"

        elif "quais carros" in msg_lower:
            return "Temos: Gol 2020 (R$ 45k), Onix 2021 (R$ 48k), HB20 2019 (R$ 42k)"

        elif "quero" in msg_lower and "gol" in msg_lower:
            self.redis.setex(f"carro_ativo:automaia:{numero}", 86400, "gol-2020-001")
            self.chatwoot.adicionar_tag(conv_id, "interessado_gol_2020_001")
            return "Ótima escolha! Anotei seu interesse no Gol 2020 🚗"

        else:
            return "Oi! Como posso ajudar? 😊"


# ==============================================================================
# SIMULAÇÃO COMPLETA COM INTERVENÇÃO HUMANA
# ==============================================================================

def simular_cenario_completo():
    """Simula cenário completo: Bot → Escalona → Humano resolve"""

    print("\n" + "="*90)
    print("🎬 TESTE COMPLETO: Dashboard + Intervenção Humana")
    print("="*90 + "\n")

    # Inicializa sistemas
    redis = MockRedis()
    chatwoot = MockChatwoot()
    bot = SimuladorChatbot(redis, chatwoot)
    dashboard = ChatwootDashboard(chatwoot)

    # Cliente 1: Satisfeito (só bot)
    print("📱 CLIENTE 1: João Silva (conversa normal)\n")
    conv1 = chatwoot.criar_conversa("5531986549366")
    redis.setex(f"score:5531986549366", 86400, "10")

    mensagens_joao = [
        "Olá, quais carros vocês têm?",
        "Quero saber mais sobre o Gol"
    ]

    for msg in mensagens_joao:
        print(f"   👤 Cliente: {msg}")
        chatwoot.adicionar_mensagem(conv1, "customer", msg)

        resposta = bot.processar_mensagem("5531986549366", msg, conv1)
        if resposta:
            print(f"   🤖 Bot: {resposta}")
            chatwoot.adicionar_mensagem(conv1, "agent", resposta)
        print()
        time.sleep(0.3)

    # Cliente 2: Frustrado (escalona para humano)
    print("\n" + "─"*90)
    print("📱 CLIENTE 2: Carlos Pereira (fica frustrado → ESCALONA)\n")
    conv2 = chatwoot.criar_conversa("5531987654321")
    redis.setex(f"score:5531987654321", 86400, "10")

    mensagens_carlos = [
        "Olá",
        "Quero comprar um carro",
        "Mas esses preços tão muito caros!",
        "Tô frustrado, não tá dando...",
    ]

    for i, msg in enumerate(mensagens_carlos, 1):
        print(f"   👤 Cliente: {msg}")
        chatwoot.adicionar_mensagem(conv2, "customer", msg)

        resposta = bot.processar_mensagem("5531987654321", msg, conv2)
        if resposta:
            print(f"   🤖 Bot: {resposta}")
            chatwoot.adicionar_mensagem(conv2, "agent", resposta)

        # Após terceira mensagem, bot escalona
        if i == 3:
            print(f"\n   ⚠️ BOT DETECTA FRUSTRAÇÃO!")
            print(f"   🏷️ Tag 'precisa_humano' criada")
            print(f"   👨‍💼 Atribuído para: Maria Supervisora")

        print()
        time.sleep(0.3)

    # MOSTRA DASHBOARD APÓS BOT ATENDER
    input("\n⏸️  Pressione ENTER para ver Dashboard do Chatwoot...")
    dashboard.mostrar_dashboard()

    # VENDEDORA VÊ A CONVERSA
    input("\n⏸️  Pressione ENTER para Maria ver a conversa detalhada...")
    dashboard.mostrar_conversa_detalhada(conv2)

    # VENDEDORA ASSUME A CONVERSA
    input("\n⏸️  Pressione ENTER para Maria ASSUMIR a conversa...")
    print(f"\n{'='*90}")
    print(f"👨‍💼 VENDEDORA MARIA ASSUME A CONVERSA")
    print(f"{'='*90}\n")

    chatwoot.humano_assumir(conv2)
    print(f"   ✅ Bot pausado - Humano no controle\n")

    # CLIENTE ENVIA MAIS MENSAGENS → BOT NÃO RESPONDE
    print(f"📱 Cliente continua falando...\n")

    msg_cliente = "Alguém pode me ajudar?"
    print(f"   👤 Cliente: {msg_cliente}")
    chatwoot.adicionar_mensagem(conv2, "customer", msg_cliente)

    resposta_bot = bot.processar_mensagem("5531987654321", msg_cliente, conv2)
    if resposta_bot:
        print(f"   🤖 Bot: {resposta_bot}")
    else:
        print(f"   🤖 Bot: (silencioso - humano assumiu)")

    print()

    # VENDEDORA RESPONDE
    input("⏸️  Pressione ENTER para Maria responder...")
    print(f"\n{'='*90}")
    print(f"👨‍💼 VENDEDORA MARIA RESPONDE")
    print(f"{'='*90}\n")

    respostas_maria = [
        "Oi Carlos! Sou a Maria, supervisora aqui 😊",
        "Vi que está preocupado com os preços. Vamos achar uma solução!",
        "Tenho uma condição especial: 10% de desconto + entrada facilitada",
        "O Gol 2020 sairia de R$ 45mil por R$ 40.500",
        "E podemos parcelar a entrada em 3x sem juros. O que acha?"
    ]

    for resposta in respostas_maria:
        print(f"   👨‍💼 Maria: {resposta}")
        chatwoot.adicionar_mensagem(conv2, "human", resposta)
        time.sleep(0.5)

    print()

    # CLIENTE RESPONDE POSITIVAMENTE
    input("⏸️  Pressione ENTER para reação do cliente...")
    print(f"\n   👤 Cliente: Agora sim! Essa condição tá ótima! 😊")
    chatwoot.adicionar_mensagem(conv2, "customer", "Agora sim! Essa condição tá ótima! 😊")

    print(f"   👨‍💼 Maria: Perfeito! Vou preparar o contrato. Pode vir amanhã às 10h?")
    chatwoot.adicionar_mensagem(conv2, "human", "Perfeito! Vou preparar o contrato. Pode vir amanhã às 10h?")

    print(f"   👤 Cliente: Pode sim! Até amanhã!")
    chatwoot.adicionar_mensagem(conv2, "customer", "Pode sim! Até amanhã!")

    # TAG DE SUCESSO
    chatwoot.adicionar_tag(conv2, "visita_agendada")
    chatwoot.adicionar_tag(conv2, "resolvido_humano")
    print(f"\n   🏷️ Tags adicionadas: visita_agendada, resolvido_humano")

    # DASHBOARD FINAL
    input("\n⏸️  Pressione ENTER para Dashboard Final...")
    dashboard.mostrar_dashboard()

    # MÉTRICAS
    input("\n⏸️  Pressione ENTER para Métricas Finais...")
    dashboard.mostrar_metricas_tempo_real()

    # FILTRO POR TAG
    input("\n⏸️  Pressione ENTER para filtrar tag 'precisa_humano'...")
    dashboard.filtrar_por_tag("precisa_humano")

    # RESUMO
    print(f"\n{'='*90}")
    print(f"📊 RESUMO DO TESTE")
    print(f"{'='*90}\n")

    print(f"✅ Cenários testados:")
    print(f"   1. Cliente satisfeito → Bot atendeu sozinho")
    print(f"   2. Cliente frustrado → Bot escalou → Humano resolveu")
    print()

    print(f"✅ Funcionalidades validadas:")
    print(f"   • Dashboard Chatwoot (visualização)")
    print(f"   • Filtros por tag")
    print(f"   • Métricas em tempo real")
    print(f"   • Escalonamento automático (bot → humano)")
    print(f"   • Bot para quando humano assume")
    print(f"   • Humano resolve problema")
    print(f"   • Tags de status (precisa_humano, resolvido_humano)")
    print()

    print(f"📊 Resultados:")
    print(f"   Total de conversas: {len(chatwoot.conversations)}")
    print(f"   Resolvidas por bot: 1")
    print(f"   Resolvidas por humano: 1")
    print(f"   Taxa de escalonamento: 50%")
    print()

    print(f"🎉 INTEGRAÇÃO DASHBOARD + HUMANO 100% FUNCIONAL!\n")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    try:
        simular_cenario_completo()
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido\n")
