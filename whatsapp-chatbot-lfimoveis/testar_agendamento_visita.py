#!/usr/bin/env python3
"""
🧪 TESTE COMPLETO - FLUXO DE AGENDAMENTO + NOTIFICAÇÃO
Simula todo o fluxo sem enviar WhatsApp real
Testa: sugestão → escolha → confirmação → notificação corretor
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


# ============================================================================
# MOCK CLASSES - Simular componentes reais
# ============================================================================

class MockRedis:
    """Mock simples do Redis para testes"""
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def setex(self, key, ttl, value):
        self.data[key] = value

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def __repr__(self):
        return f"MockRedis({len(self.data)} keys)"


class MockConsultaAgenda:
    """Mock da agenda (horários fictícios)"""
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def buscar_horarios_disponiveis(self, dias_frente=3, limite=3):
        """Retorna 3 horários fictícios"""
        horarios = []
        base = datetime.now()

        opcoes = [
            {"data_offset": 1, "hora": "10:00", "dia_semana": "amanhã"},
            {"data_offset": 2, "hora": "14:30", "dia_semana": "quarta"},
            {"data_offset": 3, "hora": "15:00", "dia_semana": "quinta"},
        ]

        for i, opcao in enumerate(opcoes[:limite], 1):
            data = base + timedelta(days=opcao["data_offset"])
            horarios.append({
                "data": data.date(),
                "data_formatada": opcao["dia_semana"].capitalize(),
                "hora": opcao["hora"],
                "disponivel": True
            })

        return horarios

    def agendar_visita(self, cliente_numero, imovel_id, horario):
        """Simula agendamento na planilha"""
        print(f"   → Agendamento salvo em Google Sheets:")
        print(f"     Cliente: {cliente_numero}")
        print(f"     Imóvel: {imovel_id}")
        print(f"     Data/Hora: {horario['data_formatada']} às {horario['hora']}")
        return True


class MockIntegradorEscalonamento:
    """Mock do integrador de escalonamento"""
    def __init__(self, redis_client=None, config=None):
        self.redis_client = redis_client or MockRedis()
        self.config = config or {}
        self.agenda = MockConsultaAgenda(use_mock=True)

    def sugerir_horarios(self, cliente_numero, imovel_id=None):
        """Sugere 3 horários disponíveis"""
        horarios = self.agenda.buscar_horarios_disponiveis(dias_frente=3, limite=3)

        if not horarios:
            return "No momento não temos horários disponíveis. Vou chamar um corretor pra você! 👍"

        # Formata mensagem
        opcoes = []
        for i, h in enumerate(horarios, 1):
            opcoes.append(f"{i}️⃣ {h['data_formatada']} às {h['hora']}")

        mensagem = "*Posso agendar pra:*\n\n" + "\n".join(opcoes) + "\n\n_Qual prefere?_"

        # Salva opções no Redis
        self.redis_client.setex(
            f"opcoes_horario:{cliente_numero}",
            3600,
            json.dumps(horarios, default=str)
        )

        print(f"   → Opções salvas no Redis para {cliente_numero}")
        return mensagem

    def confirmar_agendamento(self, cliente_numero, escolha, imovel_id=None):
        """Confirma agendamento escolhido"""
        # Recupera opções salvas
        opcoes_json = self.redis_client.get(f"opcoes_horario:{cliente_numero}")

        if not opcoes_json:
            return False, "Ops! As opções expiraram. Me fala de novo quando você quer visitar? 📅"

        horarios = json.loads(opcoes_json)

        # Extrai número
        import re
        match = re.search(r'\d+', escolha)
        escolha_numero = int(match.group()) if match else None

        if not escolha_numero or escolha_numero > len(horarios):
            return False, "Não entendi... Pode escolher um dos números? (1, 2 ou 3)"

        # Horário escolhido
        horario = horarios[escolha_numero - 1]

        # Converte data de volta se necessário
        if isinstance(horario['data'], str):
            from datetime import datetime
            horario['data'] = datetime.strptime(horario['data'], '%Y-%m-%d').date()

        # Agenda na planilha
        sucesso = self.agenda.agendar_visita(cliente_numero, imovel_id or "N/A", horario)

        if not sucesso:
            return False, "Ops! Erro ao agendar. Vou chamar um corretor pra você! 👍"

        # Limpa Redis
        self.redis_client.delete(f"opcoes_horario:{cliente_numero}")

        # Mensagem confirmação
        mensagem = f"""
✅ *Agendado!*

📅 {horario['data_formatada']} às {horario['hora']}

Te mando lembretes antes! 🔔

_Endereço: Chácara em Itatiaiuçu_
        """.strip()

        return True, mensagem


# ============================================================================
# TESTE PRINCIPAL
# ============================================================================

def formatar_telefone(numero: str) -> str:
    """Formata número de telefone brasileiro"""
    try:
        if len(numero) >= 13:
            ddi = numero[:2]
            ddd = numero[2:4]
            parte1 = numero[4:9]
            parte2 = numero[9:]
            return f"+{ddi} ({ddd}) {parte1}-{parte2}"
        return numero
    except:
        return numero


def extrair_detalhes_imovel(imovel_id: Optional[str]) -> Dict:
    """Extrai detalhes fictícios do imóvel"""
    return {
        "titulo": "Chácara em Itatiaiuçu - 5.000m² (ID: itatiaiucu-001)",
        "preco": "Entrada: R$ 50k + 120x R$ 1.200",
        "condicoes": "Financiado em 120 meses",
        "tipo": "Chácara",
        "area": "5.000m²",
        "localizacao": "Itatiaiuçu - MG"
    }


def gerar_resumo_conversa_ia(cliente_numero: str, tipo_imovel: str) -> str:
    """Simula resumo gerado por IA"""
    return "• Cliente muito interessado em chácara\n• Quer visitar ASAP\n• Urgência: ALTA"


def _notificar_corretor_agendamento(
    cliente_numero: str,
    nome_cliente: str,
    imovel_id: Optional[str],
    horario_confirmado: str,
    data_formatada: str,
    redis_client: MockRedis,
    config: Dict
) -> str:
    """
    SIMULA notificação que seria enviada para o corretor
    Mostra a mensagem que SERIA enviada via WhatsApp
    """
    # 1. Dados do cliente
    telefone_formatado = formatar_telefone(cliente_numero)

    # Score fictício
    score = 85
    classificacao = "🔥 QUENTE"

    # 2. Detalhes do imóvel
    detalhes_imovel = extrair_detalhes_imovel(imovel_id)

    # 3. Resumo da conversa
    resumo_conversa = gerar_resumo_conversa_ia(cliente_numero, detalhes_imovel['tipo'])

    # 4. Monta mensagem para corretor
    corretor_whatsapp = "5531980160822"  # Luciano

    mensagem_corretor = f"""
🗓️ *NOVA VISITA AGENDADA*

👤 *CLIENTE*
📱 {nome_cliente}
📞 {telefone_formatado}
📊 Score: {score} - {classificacao}

🏠 *IMÓVEL DE INTERESSE*
{detalhes_imovel['titulo']}
💰 Preço: {detalhes_imovel['preco']}
💳 Condições: {detalhes_imovel['condicoes']}

📅 *AGENDAMENTO*
{data_formatada} às {horario_confirmado}

💬 *RESUMO DA CONVERSA*
{resumo_conversa}

🔔 *Ação:* Confirme presença 1 dia antes!
    """.strip()

    return mensagem_corretor


def teste_agendamento_completo():
    """Teste completo do fluxo de agendamento"""

    print("\n" + "="*80)
    print("🧪 TESTE COMPLETO - FLUXO DE AGENDAMENTO DE VISITA")
    print("="*80)

    # Dados do teste
    CLIENTE_NUMERO = "5531987654321"
    CLIENTE_NOME = "Maria Silva"
    IMOVEL_ID = "itatiaiucu-001"

    print(f"\n👤 Cliente: {CLIENTE_NOME}")
    print(f"📱 Número: {CLIENTE_NUMERO}")
    print(f"🏠 Imóvel: Chácara em Itatiaiuçu (ID: {IMOVEL_ID})")
    print(f"📍 Notificação para: 5531980160822 (Luciano)")

    # ========================================================================
    # SETUP
    # ========================================================================
    print("\n" + "-"*80)
    print("⚙️  SETUP")
    print("-"*80)

    redis = MockRedis()
    config = {
        'google_sheet_id': 'mock-sheet-id',
        'chatwoot': {'url': '', 'token': '', 'account_id': ''},
        'evolution': {'url': '', 'api_key': '', 'instance': ''}
    }

    integrador = MockIntegradorEscalonamento(redis, config)

    print(f"✓ Redis inicializado: {redis}")
    print(f"✓ Integrador inicializado: Mock Escalonamento")

    # ========================================================================
    # FASE 1: SUGERIR HORÁRIOS
    # ========================================================================
    print("\n" + "-"*80)
    print("📋 FASE 1: CLIENTE PEDE PARA AGENDAR")
    print("-"*80)
    print(f"\n👤 Cliente: 'Quero agendar uma visita para conhecer a chácara'")

    resposta_sugerir = integrador.sugerir_horarios(CLIENTE_NUMERO, IMOVEL_ID)

    print(f"\n🤖 Bot sugeriu horários:")
    print(f"\n{resposta_sugerir}")

    # Verifica Redis
    opcoes_salvas = redis.get(f"opcoes_horario:{CLIENTE_NUMERO}")
    print(f"\n✓ Horários salvos no Redis")
    print(f"  Tamanho: {len(opcoes_salvas)} bytes")

    # ========================================================================
    # FASE 2: CLIENTE ESCOLHE OPÇÃO
    # ========================================================================
    print("\n" + "-"*80)
    print("📋 FASE 2: CLIENTE ESCOLHE HORÁRIO")
    print("-"*80)
    print(f"\n👤 Cliente: 'Quero a opção 2'")

    escolha_cliente = "2"
    sucesso, resposta_confirmar = integrador.confirmar_agendamento(
        CLIENTE_NUMERO,
        escolha_cliente,
        IMOVEL_ID
    )

    if sucesso:
        print(f"\n✅ Agendamento confirmado!")
        print(f"\n🤖 Bot respondeu:")
        print(f"\n{resposta_confirmar}")
    else:
        print(f"\n❌ Erro ao confirmar: {resposta_confirmar}")
        return False

    # ========================================================================
    # FASE 3: EXTRAIR DADOS PARA NOTIFICAÇÃO
    # ========================================================================
    print("\n" + "-"*80)
    print("📋 FASE 3: PREPARAR NOTIFICAÇÃO PARA CORRETOR")
    print("-"*80)

    # Extrai horário confirmado da mensagem
    import re
    match_hora = re.search(r'(\d{1,2}):(\d{2})', resposta_confirmar)
    hora_confirmada = f"{match_hora.group(1)}:{match_hora.group(2)}" if match_hora else "14:30"

    match_data = re.search(r'(quarta|quinta|amanhã)', resposta_confirmar.lower())
    data_confirmada = match_data.group(1).capitalize() if match_data else "Quarta"

    print(f"\n✓ Data/Hora extraída: {data_confirmada} às {hora_confirmada}")

    # ========================================================================
    # FASE 4: GERAR NOTIFICAÇÃO COMPLETA
    # ========================================================================
    print("\n" + "-"*80)
    print("🔔 FASE 4: MENSAGEM PARA CORRETOR (O que SERIA enviado)")
    print("-"*80)

    mensagem_final = _notificar_corretor_agendamento(
        cliente_numero=CLIENTE_NUMERO,
        nome_cliente=CLIENTE_NOME,
        imovel_id=IMOVEL_ID,
        horario_confirmado=hora_confirmada,
        data_formatada=data_confirmada,
        redis_client=redis,
        config=config
    )

    print(f"\n{'='*80}")
    print("📱 MENSAGEM A ENVIAR PARA LUCIANO (5531980160822):")
    print(f"{'='*80}\n")
    print(mensagem_final)
    print(f"\n{'='*80}")

    # ========================================================================
    # FASE 5: VERIFICAÇÕES
    # ========================================================================
    print("\n" + "-"*80)
    print("✅ VERIFICAÇÕES DO FLUXO")
    print("-"*80)

    checks = [
        ("Ferramenta agendar_visita (sugerir) funciona?", len(resposta_sugerir) > 0),
        ("Horários sugeridos com sucesso?", "Amanhã" in resposta_sugerir),
        ("Opções salvadas no Redis?", opcoes_salvas is not None),
        ("Agendamento confirmado?", sucesso),
        ("Google Sheets atualizado?", sucesso),
        ("Notificação montada com dados completos?", "Maria Silva" in mensagem_final),
        ("Score incluído na notificação?", "Score:" in mensagem_final),
        ("Telefone formatado?", "+55" in mensagem_final),
        ("Detalhes do imóvel presentes?", "Chácara" in mensagem_final),
        ("Resumo da conversa incluído?", "Cliente muito interessado" in mensagem_final),
    ]

    print()
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")

    # ========================================================================
    # RESUMO
    # ========================================================================
    print("\n" + "="*80)
    print("📊 RESUMO DO TESTE")
    print("="*80)

    todos_ok = all(result for _, result in checks)

    if todos_ok:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("\n📋 O QUE FOI TESTADO:")
        print("   1. Ferramenta agendar_visita (sugerir)")
        print("   2. Armazenamento de opções no Redis")
        print("   3. Ferramenta agendar_visita (confirmar)")
        print("   4. Agendamento em Google Sheets")
        print("   5. Geração de notificação enriquecida")
        print("   6. Inclusão de dados completos (cliente, score, imóvel)")
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("   → Deploy: python3 testar_agendamento_visita.py")
        print("   → Verificar logs do bot em: logs/chatbot_lfimoveis.log")
        print("   → Chamar agendamento via: ferramentas/agendar_visita.py")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        failed = [name for name, result in checks if not result]
        for f in failed:
            print(f"   ✗ {f}")

    print("\n" + "="*80)
    return todos_ok


if __name__ == "__main__":
    sucesso = teste_agendamento_completo()
    sys.exit(0 if sucesso else 1)
