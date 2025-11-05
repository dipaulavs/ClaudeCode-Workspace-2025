#!/usr/bin/env python3.11
"""
🎭 SIMULAÇÃO DE CONVERSAS REAIS - Análise do Sistema Híbrido

Simula conversas COMPLETAS mostrando:
- QUANDO cada ferramenta é ativada
- POR QUÊ foi escolhida (contexto/tag)
- Uso eficiente de MCP vs Local
- Prevenção de alucinações
"""

import json
from datetime import datetime
from typing import List, Dict, Optional


class EstadoConversa:
    """Estado da conversa (simula Redis)"""
    def __init__(self):
        self.carro_ativo: Optional[str] = None
        self.mensagens_cliente: List[str] = []
        self.tags: List[str] = []
        self.etapa_agendamento: Optional[str] = None


class DecisaoIA:
    """Simula decisão da IA sobre qual ferramenta usar"""

    def __init__(self, estado: EstadoConversa):
        self.estado = estado

    def analisar_mensagem(self, mensagem: str) -> Dict:
        """
        Analisa mensagem e decide ferramenta (simula Claude)

        Returns:
            {
                "ferramenta": nome da ferramenta,
                "razao": por que foi escolhida,
                "tipo": "local" ou "mcp",
                "parametros": {...}
            }
        """
        msg_lower = mensagem.lower()

        # Adiciona mensagem ao histórico
        self.estado.mensagens_cliente.append(mensagem)

        # ===== DECISÕES LOCAIS (prioridade) =====

        # 1. Lista carros (cliente não sabe o que tem)
        if any(palavra in msg_lower for palavra in ["quais carros", "o que tem", "me mostra", "tem disponível"]):
            return {
                "ferramenta": "lista_carros",
                "razao": "Cliente perguntou quais carros estão disponíveis (sem contexto ainda)",
                "tipo": "local",
                "parametros": {},
                "latencia": "~0ms"
            }

        # 2. Consulta FAQ (TEM carro ativo)
        if self.estado.carro_ativo:
            if any(palavra in msg_lower for palavra in ["preço", "valor", "quanto custa", "motor", "garantia", "km", "ano", "cor"]):
                return {
                    "ferramenta": "consulta_faq",
                    "razao": f"Cliente perguntou sobre {self.estado.carro_ativo} (CARRO ATIVO no contexto)",
                    "tipo": "local",
                    "parametros": {"carro_id": self.estado.carro_ativo, "pergunta": mensagem},
                    "latencia": "~0ms",
                    "contexto": f"✅ Tem tag: {self.estado.carro_ativo}"
                }

        # 3. Taguear interesse (cliente escolheu carro)
        if any(palavra in msg_lower for palavra in ["quero", "gostei", "me interessa", "quero saber mais"]):
            # Tenta extrair ID do carro da mensagem
            if "gol" in msg_lower:
                carro_id = "gol-2020-001"
            elif "onix" in msg_lower:
                carro_id = "onix-2021-002"
            elif "civic" in msg_lower:
                carro_id = "civic-2019-003"
            else:
                carro_id = None

            if carro_id:
                self.estado.carro_ativo = carro_id
                self.estado.tags.append(carro_id)
                return {
                    "ferramenta": "taguear_cliente",
                    "razao": f"Cliente demonstrou interesse em {carro_id}",
                    "tipo": "local",
                    "parametros": {"carro_id": carro_id},
                    "latencia": "~0ms",
                    "acao": f"🏷️ Criou tag: {carro_id}"
                }

        # 4. Agendar visita (cliente quer agendar)
        if any(palavra in msg_lower for palavra in ["agendar", "visita", "ver o carro", "ir até loja", "horário"]):
            if self.estado.etapa_agendamento == "aguardando_escolha":
                return {
                    "ferramenta": "agendar_visita",
                    "razao": "Confirmar escolha de horário (etapa 2/2)",
                    "tipo": "local",
                    "parametros": {"acao": "confirmar", "escolha": mensagem},
                    "latencia": "~0ms"
                }
            else:
                self.estado.etapa_agendamento = "aguardando_escolha"
                return {
                    "ferramenta": "agendar_visita",
                    "razao": "Sugerir horários de visita (etapa 1/2)",
                    "tipo": "local",
                    "parametros": {"acao": "sugerir"},
                    "latencia": "~0ms"
                }

        # ===== DECISÕES MCP (quando necessário) =====

        # 5. Busca similares (SEM contexto, busca genérica)
        if any(palavra in msg_lower for palavra in ["parecido", "similar", "algo como", "tipo", "econômico", "esportivo"]):
            if not self.estado.carro_ativo:
                return {
                    "ferramenta": "buscar_carros_similares",
                    "razao": "Busca por características (SEM carro ativo, cliente não sabe o que quer)",
                    "tipo": "mcp",
                    "parametros": {"caracteristicas": mensagem, "limite": 5},
                    "latencia": "~150ms",
                    "contexto": "❌ Sem tag - usa busca semântica"
                }
            else:
                # Se JÁ tem carro ativo, não precisa buscar!
                return {
                    "ferramenta": "consulta_faq",
                    "razao": f"Cliente já tem interesse em {self.estado.carro_ativo}, consulta FAQ local",
                    "tipo": "local",
                    "parametros": {"carro_id": self.estado.carro_ativo, "pergunta": mensagem},
                    "latencia": "~0ms",
                    "contexto": f"✅ Tem tag: {self.estado.carro_ativo} - EVITA MCP!"
                }

        # 6. Calcular financiamento
        if any(palavra in msg_lower for palavra in ["financiar", "parcela", "entrada", "juros", "prestação"]):
            # Tenta extrair valores
            valor_veiculo = 45000  # mock
            valor_entrada = 10000 if "entrada" in msg_lower else 0

            return {
                "ferramenta": "calcular_financiamento",
                "razao": "Cliente perguntou sobre financiamento (cálculo complexo)",
                "tipo": "mcp",
                "parametros": {"valor_veiculo": valor_veiculo, "valor_entrada": valor_entrada, "taxa_juros_mensal": 1.99},
                "latencia": "~150ms"
            }

        # 7. Consultar FIPE
        if "fipe" in msg_lower or "tabela" in msg_lower:
            marca = "Volkswagen"
            modelo = "Gol"
            ano = "2020"

            return {
                "ferramenta": "consultar_fipe",
                "razao": "Cliente perguntou sobre valor FIPE (consulta externa)",
                "tipo": "mcp",
                "parametros": {"marca": marca, "modelo": modelo, "ano": ano},
                "latencia": "~150ms"
            }

        # 8. Analisar sentimento (frustração detectada)
        if any(palavra in msg_lower for palavra in ["caro", "não sei", "complicado", "difícil", "frustrado"]):
            return {
                "ferramenta": "analisar_sentimento",
                "razao": "Sinais de frustração/indecisão (análise emocional)",
                "tipo": "mcp",
                "parametros": {"mensagens": self.estado.mensagens_cliente[-5:]},
                "latencia": "~150ms"
            }

        # 9. Gerar proposta (pedido formal)
        if any(palavra in msg_lower for palavra in ["proposta", "por escrito", "enviar", "documento"]):
            if self.estado.carro_ativo:
                return {
                    "ferramenta": "gerar_proposta_comercial",
                    "razao": "Cliente pediu proposta formal (geração de documento)",
                    "tipo": "mcp",
                    "parametros": {"carro_id": self.estado.carro_ativo, "cliente_nome": "Cliente", "desconto_percentual": 5},
                    "latencia": "~150ms"
                }

        # Sem ferramenta (conversação normal)
        return {
            "ferramenta": None,
            "razao": "Conversação normal, sem necessidade de ferramenta",
            "tipo": "none",
            "parametros": {}
        }


# ==============================================================================
# CENÁRIOS DE CONVERSAS REAIS
# ==============================================================================

CONVERSAS = [
    {
        "titulo": "Conversa 1: Cliente Exploratório (USA MCP corretamente)",
        "descricao": "Cliente não sabe o que quer → Busca semântica necessária",
        "mensagens": [
            "Olá, tô procurando um carro",
            "Quero algo econômico e confiável",
            "Tem algum tipo sedan até 50 mil?",
        ]
    },
    {
        "titulo": "Conversa 2: Cliente Direto (USA LOCAL - eficiente)",
        "descricao": "Cliente já sabe o carro → Usa FAQ local, NÃO busca MCP",
        "mensagens": [
            "Quais carros vocês têm?",
            "Quero saber mais sobre o Gol 2020",
            "Qual o preço?",
            "Tem garantia?",
            "Quero agendar uma visita"
        ]
    },
    {
        "titulo": "Conversa 3: Cliente com Tag (EVITA MCP)",
        "descricao": "Cliente já tem interesse marcado → Todas consultas locais",
        "mensagens": [
            "Oi, vi o Gol no site",
            "Me interessa!",  # <- Cria tag
            "Qual o motor?",  # <- USA LOCAL (tem tag)
            "E o consumo?",   # <- USA LOCAL (tem tag)
            "Quanto tá na FIPE?"  # <- Só aqui usa MCP (consulta externa)
        ]
    },
    {
        "titulo": "Conversa 4: Cliente Financiamento (MIX correto)",
        "descricao": "Mix de local + MCP quando apropriado",
        "mensagens": [
            "Quais carros tem?",  # <- LOCAL
            "Gostei do Onix",     # <- LOCAL (tagueamento)
            "Quanto fica financiado em 48x?",  # <- MCP (cálculo complexo)
            "E se der 10 mil de entrada?"      # <- MCP (recalculo)
        ]
    },
    {
        "titulo": "Conversa 5: Cliente Frustrado (MCP emocional)",
        "descricao": "Detecção de frustração → Análise de sentimento",
        "mensagens": [
            "Tô procurando carro há dias",
            "Tudo muito caro",
            "Não tô achando nada que presta",
            "Tá complicado..."
        ]
    }
]


# ==============================================================================
# SIMULADOR
# ==============================================================================

def simular_conversa(conversa: Dict):
    """Simula uma conversa completa"""
    print(f"\n{'='*80}")
    print(f"🎬 {conversa['titulo']}")
    print(f"{'='*80}")
    print(f"📝 {conversa['descricao']}\n")

    estado = EstadoConversa()
    decisao = DecisaoIA(estado)

    ferramentas_usadas = {"local": 0, "mcp": 0, "none": 0}
    latencia_total = 0

    for i, mensagem in enumerate(conversa['mensagens'], 1):
        print(f"\n{'─'*80}")
        print(f"💬 MENSAGEM {i}: {mensagem}")

        # Analisa e decide
        resultado = decisao.analisar_mensagem(mensagem)

        # Mostra decisão
        print(f"\n🤖 DECISÃO DA IA:")
        print(f"   Ferramenta: {resultado['ferramenta'] or 'Nenhuma'}")
        print(f"   Tipo: {resultado['tipo'].upper()}")
        print(f"   Razão: {resultado['razao']}")

        if resultado['tipo'] != 'none':
            print(f"   Latência: {resultado.get('latencia', 'N/A')}")
            ferramentas_usadas[resultado['tipo']] += 1

            if resultado['tipo'] == 'mcp':
                latencia_total += 150

        # Mostra contexto adicional
        if 'contexto' in resultado:
            print(f"\n   ℹ️ {resultado['contexto']}")

        if 'acao' in resultado:
            print(f"\n   ⚡ {resultado['acao']}")

        # Mostra estado atual
        print(f"\n📊 ESTADO:")
        print(f"   Carro Ativo: {estado.carro_ativo or 'Nenhum'}")
        print(f"   Tags: {', '.join(estado.tags) if estado.tags else 'Nenhuma'}")
        print(f"   Mensagens no histórico: {len(estado.mensagens_cliente)}")

    # Resumo da conversa
    print(f"\n{'='*80}")
    print(f"📈 RESUMO DA CONVERSA")
    print(f"{'='*80}")
    print(f"Total de mensagens: {len(conversa['mensagens'])}")
    print(f"Ferramentas Locais: {ferramentas_usadas['local']} (0ms overhead)")
    print(f"Ferramentas MCP: {ferramentas_usadas['mcp']} (~{latencia_total}ms total)")
    print(f"Sem ferramenta: {ferramentas_usadas['none']}")
    print(f"Latência total estimada: ~{latencia_total}ms")

    # Análise de eficiência
    total_ferramentas = ferramentas_usadas['local'] + ferramentas_usadas['mcp']
    if total_ferramentas > 0:
        percentual_local = (ferramentas_usadas['local'] / total_ferramentas) * 100
        print(f"\n✅ Eficiência: {percentual_local:.0f}% das ferramentas foram locais (rápidas)")

    # Validação
    print(f"\n🎯 VALIDAÇÃO:")

    # Verifica se usou MCP desnecessariamente
    if estado.carro_ativo and ferramentas_usadas['mcp'] > 1:
        print(f"   ⚠️ ATENÇÃO: Cliente tinha tag '{estado.carro_ativo}' mas usou {ferramentas_usadas['mcp']} MCPs")
        print(f"      Algumas buscas poderiam ser locais?")
    else:
        print(f"   ✅ Uso eficiente: MCP usado apenas quando necessário")

    print()


def menu():
    """Menu interativo"""
    print("\n" + "="*80)
    print("🎭 SIMULAÇÃO DE CONVERSAS REAIS - SISTEMA HÍBRIDO")
    print("="*80 + "\n")

    print("📋 Escolha uma conversa para simular:\n")

    for i, conversa in enumerate(CONVERSAS, 1):
        print(f"   {i}. {conversa['titulo']}")
        print(f"      {conversa['descricao']}\n")

    print(f"   {len(CONVERSAS)+1}. TODAS AS CONVERSAS")
    print(f"   0. Sair\n")

    try:
        escolha = int(input("Digite sua escolha: ").strip())

        if escolha == 0:
            print("\n👋 Até mais!\n")
            return

        elif 1 <= escolha <= len(CONVERSAS):
            simular_conversa(CONVERSAS[escolha-1])

        elif escolha == len(CONVERSAS)+1:
            for conversa in CONVERSAS:
                simular_conversa(conversa)
                input("\n⏸️  Pressione ENTER para próxima conversa...")

        else:
            print("\n❌ Opção inválida\n")

    except (ValueError, KeyboardInterrupt):
        print("\n\n👋 Até mais!\n")


if __name__ == "__main__":
    menu()
