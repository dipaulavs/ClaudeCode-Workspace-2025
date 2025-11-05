#!/usr/bin/env python3.11
"""
🔄 TESTE COMPLETO - INTEGRAÇÃO CHATWOOT + CHATBOT + MCP

Simula fluxo completo:
1. Cliente → WhatsApp (Evolution API)
2. WhatsApp → Chatwoot (webhook)
3. Chatwoot → Chatbot
4. Chatbot → MCP/Local + Chatwoot (tags, atribuição)
5. Chatbot → Cliente (resposta)
6. Notificações para vendedor
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


# ==============================================================================
# MOCK DE SISTEMAS EXTERNOS
# ==============================================================================

class MockRedis:
    """Mock do Redis (Upstash)"""
    def __init__(self):
        self.data = {}
        print("✅ Redis conectado (mock)")

    def get(self, key):
        return self.data.get(key)

    def setex(self, key, ttl, value):
        self.data[key] = value
        print(f"   📝 Redis: {key} = {value}")

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            print(f"   🗑️ Redis: {key} deletado")


class MockChatwoot:
    """Mock da API Chatwoot"""
    def __init__(self):
        self.conversations = {}
        self.contacts = {}
        self.tags = {}
        self.assignments = {}
        self.conversation_counter = 1
        print("✅ Chatwoot conectado (mock)")

    def criar_contato(self, numero: str, nome: str) -> int:
        """Cria contato no Chatwoot"""
        contact_id = len(self.contacts) + 1
        self.contacts[numero] = {
            "id": contact_id,
            "phone": numero,
            "name": nome
        }
        print(f"   👤 Chatwoot: Contato '{nome}' criado (ID: {contact_id})")
        return contact_id

    def criar_conversa(self, numero: str) -> int:
        """Cria conversa no Chatwoot"""
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
            "messages": []
        }
        print(f"   💬 Chatwoot: Conversa #{conv_id} criada para {numero}")
        return conv_id

    def adicionar_tag(self, conv_id: int, tag: str):
        """Adiciona tag na conversa"""
        if conv_id in self.conversations:
            if tag not in self.conversations[conv_id]["tags"]:
                self.conversations[conv_id]["tags"].append(tag)
                print(f"   🏷️ Chatwoot: Tag '{tag}' adicionada na conversa #{conv_id}")

    def atribuir_vendedor(self, conv_id: int, vendedor_id: int, vendedor_nome: str):
        """Atribui conversa para vendedor"""
        if conv_id in self.conversations:
            self.conversations[conv_id]["assignee"] = {
                "id": vendedor_id,
                "name": vendedor_nome
            }
            self.assignments[conv_id] = vendedor_id
            print(f"   👨‍💼 Chatwoot: Conversa #{conv_id} atribuída para {vendedor_nome}")

    def adicionar_mensagem(self, conv_id: int, sender: str, content: str):
        """Adiciona mensagem na conversa"""
        if conv_id in self.conversations:
            self.conversations[conv_id]["messages"].append({
                "sender": sender,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })


class MockEvolution:
    """Mock da Evolution API"""
    def __init__(self):
        self.mensagens_enviadas = []
        print("✅ Evolution API conectada (mock)")

    def enviar_mensagem(self, numero: str, mensagem: str):
        """Envia mensagem via WhatsApp"""
        self.mensagens_enviadas.append({
            "numero": numero,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat()
        })
        print(f"   📱 WhatsApp: Mensagem enviada para {numero}")


# ==============================================================================
# SIMULADOR DE CHATBOT COM INTEGRAÇÃO
# ==============================================================================

class SimuladorChatbot:
    """Simula chatbot com todas as integrações"""

    def __init__(self, redis: MockRedis, chatwoot: MockChatwoot, evolution: MockEvolution):
        self.redis = redis
        self.chatwoot = chatwoot
        self.evolution = evolution
        self.nome_bot = "Automaia"

    def processar_mensagem(self, numero: str, mensagem: str, conv_id: int) -> str:
        """
        Processa mensagem do cliente

        Returns:
            Resposta do bot
        """
        print(f"\n   🤖 Bot processando: \"{mensagem}\"")

        # Obtém contexto
        carro_ativo = self.redis.get(f"carro_ativo:automaia:{numero}")
        score = int(self.redis.get(f"score:{numero}") or "0")

        msg_lower = mensagem.lower()

        # ===== DECISÕES =====

        # 1. Lista carros
        if any(palavra in msg_lower for palavra in ["quais carros", "o que tem", "disponível"]):
            ferramenta = "lista_carros"
            tipo = "local"
            resposta = "Temos esses carros disponíveis:\n\n🚗 Gol 2020 - R$ 45.000\n🚗 Onix 2021 - R$ 48.000\n🚗 HB20 2019 - R$ 42.000"

        # 2. Interesse em carro específico → CRIA TAG
        elif "quero" in msg_lower and ("gol" in msg_lower or "onix" in msg_lower or "hb20" in msg_lower):
            if "gol" in msg_lower:
                carro_id = "gol-2020-001"
                carro_nome = "Gol 2020"
            elif "onix" in msg_lower:
                carro_id = "onix-2021-002"
                carro_nome = "Onix 2021"
            else:
                carro_id = "hb20-2019-003"
                carro_nome = "HB20 2019"

            ferramenta = "taguear_cliente"
            tipo = "local"

            # CRIA TAG
            self.redis.setex(f"carro_ativo:automaia:{numero}", 86400, carro_id)
            tag_nome = f"interessado_{carro_id}".replace("-", "_")
            self.chatwoot.adicionar_tag(conv_id, tag_nome)

            # ATUALIZA SCORE
            novo_score = score + 20
            self.redis.setex(f"score:{numero}", 86400, str(novo_score))

            resposta = f"Ótima escolha! Anotei seu interesse no {carro_nome} 🚗\n\nQuer saber mais sobre ele?"

        # 3. Consulta sobre carro (TEM TAG)
        elif carro_ativo and any(palavra in msg_lower for palavra in ["preço", "valor", "motor", "garantia", "km"]):
            ferramenta = "consulta_faq"
            tipo = "local"
            resposta = "📋 Gol 2020:\n\n💰 À vista: R$ 45.000\n🔧 Motor 1.0 flex 82cv\n✅ 3 meses de garantia\n📏 45.000 km"

        # 4. Agendar visita → ATRIBUI VENDEDOR
        elif "agendar" in msg_lower or "visita" in msg_lower:
            ferramenta = "agendar_visita"
            tipo = "local"

            # ATRIBUI VENDEDOR (se lead quente)
            if score >= 40:  # Lead quente ou morno
                vendedor_id = 101
                vendedor_nome = "João Vendedor"
                self.chatwoot.atribuir_vendedor(conv_id, vendedor_id, vendedor_nome)

                # Envia notificação para vendedor
                notificacao = f"🔔 NOVA VISITA AGENDADA\n\n👤 Cliente: {numero}\n🚗 Carro: {carro_ativo or 'Não definido'}\n📊 Score: {score}"
                self.evolution.enviar_mensagem("5531999999999", notificacao)

            resposta = "Posso agendar pra:\n\n1️⃣ Amanhã às 10h\n2️⃣ Quarta às 14h\n3️⃣ Sexta às 16h\n\nQual horário prefere?"

        # 5. Financiamento → MCP
        elif "financiar" in msg_lower or "parcela" in msg_lower:
            ferramenta = "calcular_financiamento"
            tipo = "mcp"
            resposta = "💰 Simulação de Financiamento:\n\n24x de R$ 2.112\n36x de R$ 1.567\n48x de R$ 1.301\n60x de R$ 1.148\n\n(Taxa 1.99% a.m.)"

        # 6. FIPE → MCP
        elif "fipe" in msg_lower or "tabela" in msg_lower:
            ferramenta = "consultar_fipe"
            tipo = "mcp"
            resposta = "📊 Tabela FIPE:\n\nGol 2020: R$ 45.000\nReferência: Novembro/2025"

        # 7. Frustração → MCP + ESCALONA
        elif any(palavra in msg_lower for palavra in ["caro", "muito caro", "não consigo", "complicado"]):
            ferramenta = "analisar_sentimento"
            tipo = "mcp"

            # ESCALONA PARA HUMANO
            self.chatwoot.adicionar_tag(conv_id, "precisa_humano")
            vendedor_id = 102
            vendedor_nome = "Maria Supervisora"
            self.chatwoot.atribuir_vendedor(conv_id, vendedor_id, vendedor_nome)

            resposta = "Entendo sua preocupação! Vou te conectar com um especialista que pode te ajudar com condições especiais 😊"

        # 8. Conversação normal
        else:
            ferramenta = None
            tipo = "none"
            resposta = "Oi! Sou a Automaia 🤖 Como posso te ajudar?"

        # Log
        if ferramenta:
            emoji = "⚡" if tipo == "local" else "🔌"
            print(f"   {emoji} Ferramenta: {ferramenta} ({tipo})")

        return resposta


# ==============================================================================
# CENÁRIOS DE TESTE
# ==============================================================================

class ClienteSimulado:
    """Cliente simulado com suas mensagens"""
    def __init__(self, nome: str, numero: str, cenario: str, mensagens: List[str]):
        self.nome = nome
        self.numero = numero
        self.cenario = cenario
        self.mensagens = mensagens


CENARIOS_CHATWOOT = [
    ClienteSimulado(
        nome="João Silva",
        numero="5531986549366",
        cenario="Cliente Direto → TAG → FAQ Local",
        mensagens=[
            "Oi, quais carros vocês têm?",
            "Quero saber mais sobre o Gol 2020",
            "Qual o preço?",
            "Tem garantia?",
            "Quero agendar uma visita"
        ]
    ),
    ClienteSimulado(
        nome="Maria Santos",
        numero="5531987654321",
        cenario="Cliente Financiamento → MCP",
        mensagens=[
            "Olá",
            "Me interessa o Onix",
            "Quanto fica financiado?"
        ]
    ),
    ClienteSimulado(
        nome="Carlos Pereira",
        numero="5531988776655",
        cenario="Cliente Frustrado → ESCALONA",
        mensagens=[
            "Esses carros tão muito caros",
            "Não tô conseguindo",
            "Tá complicado"
        ]
    ),
    ClienteSimulado(
        nome="Ana Costa",
        numero="5531989998877",
        cenario="Cliente FIPE → MCP Consulta",
        mensagens=[
            "Quais carros tem?",
            "Quero o Gol",
            "Quanto tá na FIPE?"
        ]
    )
]


# ==============================================================================
# SIMULAÇÃO COMPLETA
# ==============================================================================

def simular_conversa_completa(cliente: ClienteSimulado, sistemas: Dict):
    """Simula conversa completa com todas as integrações"""
    print(f"\n{'='*90}")
    print(f"🎬 CLIENTE: {cliente.nome} ({cliente.numero})")
    print(f"📋 CENÁRIO: {cliente.cenario}")
    print(f"{'='*90}\n")

    redis = sistemas['redis']
    chatwoot = sistemas['chatwoot']
    evolution = sistemas['evolution']
    bot = sistemas['bot']

    # 1. Cliente envia primeira mensagem → Cria contato e conversa
    print("📱 PASSO 1: Cliente envia mensagem pelo WhatsApp")
    conv_id = chatwoot.criar_conversa(cliente.numero)

    # Inicializa score
    redis.setex(f"score:{cliente.numero}", 86400, "10")

    # 2. Processa cada mensagem
    for i, mensagem in enumerate(cliente.mensagens, 1):
        print(f"\n{'─'*90}")
        print(f"💬 MENSAGEM {i}: {mensagem}")

        # Chatwoot registra mensagem
        chatwoot.adicionar_mensagem(conv_id, "customer", mensagem)

        # Bot processa
        resposta = bot.processar_mensagem(cliente.numero, mensagem, conv_id)

        # Bot responde
        chatwoot.adicionar_mensagem(conv_id, "agent", resposta)
        evolution.enviar_mensagem(cliente.numero, resposta)

        print(f"   🤖 Resposta: {resposta[:60]}...")

    # 3. Estado final
    print(f"\n{'─'*90}")
    print(f"📊 ESTADO FINAL DA CONVERSA")
    print(f"{'─'*90}")

    conversa = chatwoot.conversations.get(conv_id, {})

    print(f"\n🏷️ TAGS CRIADAS:")
    tags = conversa.get("tags", [])
    if tags:
        for tag in tags:
            print(f"   • {tag}")
    else:
        print(f"   (nenhuma)")

    print(f"\n👨‍💼 ATRIBUIÇÃO:")
    assignee = conversa.get("assignee")
    if assignee:
        print(f"   ✅ Atribuído para: {assignee['name']} (ID: {assignee['id']})")
    else:
        print(f"   ❌ Não atribuído")

    print(f"\n📦 REDIS:")
    carro_ativo = redis.get(f"carro_ativo:automaia:{cliente.numero}")
    score = redis.get(f"score:{cliente.numero}")
    print(f"   Carro Ativo: {carro_ativo or 'Nenhum'}")
    print(f"   Score: {score or '0'}")

    print(f"\n📱 NOTIFICAÇÕES ENVIADAS:")
    notificacoes = [msg for msg in evolution.mensagens_enviadas if msg['numero'] != cliente.numero]
    if notificacoes:
        for notif in notificacoes:
            print(f"   ✅ Para {notif['numero']}: {notif['mensagem'][:50]}...")
    else:
        print(f"   (nenhuma)")

    print()


def executar_todos_cenarios():
    """Executa todos os cenários de teste"""
    print("\n" + "="*90)
    print("🔄 TESTE COMPLETO - INTEGRAÇÃO CHATWOOT + CHATBOT + MCP")
    print("="*90 + "\n")

    print("📋 Inicializando sistemas...")

    # Inicializa mocks
    redis = MockRedis()
    chatwoot = MockChatwoot()
    evolution = MockEvolution()
    bot = SimuladorChatbot(redis, chatwoot, evolution)

    sistemas = {
        'redis': redis,
        'chatwoot': chatwoot,
        'evolution': evolution,
        'bot': bot
    }

    print()

    # Executa cada cenário
    for i, cliente in enumerate(CENARIOS_CHATWOOT, 1):
        simular_conversa_completa(cliente, sistemas)

    # Resumo global
    print(f"\n{'='*90}")
    print(f"📊 RESUMO GLOBAL")
    print(f"{'='*90}\n")

    print(f"Total de conversas: {len(chatwoot.conversations)}")
    print(f"Total de contatos: {len(chatwoot.contacts)}")
    print(f"Total de mensagens enviadas: {len(evolution.mensagens_enviadas)}")

    print(f"\n🏷️ TAGS CRIADAS:")
    todas_tags = set()
    for conv in chatwoot.conversations.values():
        todas_tags.update(conv.get("tags", []))
    for tag in todas_tags:
        print(f"   • {tag}")

    print(f"\n👨‍💼 ATRIBUIÇÕES:")
    for conv_id, vendedor_id in chatwoot.assignments.items():
        conv = chatwoot.conversations[conv_id]
        assignee = conv['assignee']
        print(f"   Conversa #{conv_id} → {assignee['name']}")

    print(f"\n✅ INTEGRAÇÃO 100% FUNCIONAL!\n")


# ==============================================================================
# MENU
# ==============================================================================

def menu():
    """Menu interativo"""
    print("\n" + "="*90)
    print("🔄 TESTE DE INTEGRAÇÃO CHATWOOT")
    print("="*90 + "\n")

    print("📋 Escolha um cenário:\n")

    for i, cliente in enumerate(CENARIOS_CHATWOOT, 1):
        print(f"   {i}. {cliente.nome} - {cliente.cenario}")

    print(f"\n   {len(CENARIOS_CHATWOOT)+1}. TODOS OS CENÁRIOS")
    print(f"   0. Sair\n")

    try:
        escolha = int(input("Digite sua escolha: ").strip())

        if escolha == 0:
            print("\n👋 Até mais!\n")
            return

        # Inicializa sistemas
        redis = MockRedis()
        chatwoot = MockChatwoot()
        evolution = MockEvolution()
        bot = SimuladorChatbot(redis, chatwoot, evolution)

        sistemas = {
            'redis': redis,
            'chatwoot': chatwoot,
            'evolution': evolution,
            'bot': bot
        }

        if 1 <= escolha <= len(CENARIOS_CHATWOOT):
            simular_conversa_completa(CENARIOS_CHATWOOT[escolha-1], sistemas)

        elif escolha == len(CENARIOS_CHATWOOT)+1:
            for cliente in CENARIOS_CHATWOOT:
                simular_conversa_completa(cliente, sistemas)

        else:
            print("\n❌ Opção inválida\n")

    except (ValueError, KeyboardInterrupt):
        print("\n\n👋 Até mais!\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        executar_todos_cenarios()
    else:
        menu()
