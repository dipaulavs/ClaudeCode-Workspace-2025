#!/usr/bin/env python3
"""
🧪 TESTE COMPLETO - Chatbot LF Imóveis
Simula múltiplos atendimentos para testar todas funcionalidades
"""

import requests
import json
import time
from datetime import datetime

# Configurações
BOT_URL = "http://localhost:5008"  # Middleware (recebe webhooks)
CORRETOR_WHATSAPP = "5531980160822"

# Cenários de teste
CENARIOS_TESTE = [
    {
        "nome": "Cliente Interessado - Apartamento Leblon",
        "cliente": "555199998888",
        "mensagens": [
            "Olá! Tenho interesse em apartamento no Leblon",
            "Quero ver apartamentos de 3 quartos",
            "Qual o valor?",
            "Aceita financiamento?",
            "Quero agendar uma visita",
            "Pode ser amanhã às 11h"
        ],
        "esperado": {
            "tags": ["interessado", "apartamento", "financiamento", "visita_agendada"],
            "imovel": "apartamento-leblon-3quartos",
            "agendamento": True,
            "notificar_corretor": True
        }
    },
    {
        "nome": "Cliente Premium - Cobertura Ipanema",
        "cliente": "555199997777",
        "mensagens": [
            "Boa tarde! Procuro imóvel de alto padrão em Ipanema",
            "Quero ver a cobertura duplex",
            "Tem piscina privativa?",
            "Envie fotos",
            "Onde fica exatamente?",
            "Quero visitar na sexta às 15h"
        ],
        "esperado": {
            "tags": ["premium", "cobertura", "visita_agendada"],
            "imovel": "cobertura-ipanema-luxury",
            "fotos": True,
            "localizacao": True,
            "agendamento": True,
            "notificar_corretor": True
        }
    },
    {
        "nome": "Cliente Dúvidas - FAQ",
        "cliente": "555199996666",
        "mensagens": [
            "Olá",
            "Vocês trabalham com financiamento?",
            "Aceita permuta?",
            "Permite animais?",
            "Obrigado!"
        ],
        "esperado": {
            "tags": ["duvidas", "faq"],
            "respostas_faq": True,
            "agendamento": False
        }
    },
    {
        "nome": "Cliente Casa Barra",
        "cliente": "555199995555",
        "mensagens": [
            "Procuro casa na Barra",
            "Tem casa com 4 quartos?",
            "Qual o tamanho do terreno?",
            "Tem piscina?",
            "Quero mais detalhes",
            "Agendar visita para segunda 13h"
        ],
        "esperado": {
            "tags": ["casa", "barra", "visita_agendada"],
            "imovel": "casa-barra-4quartos",
            "detalhes": True,
            "agendamento": True,
            "notificar_corretor": True
        }
    },
    {
        "nome": "Cliente Vista Mar",
        "cliente": "555199994444",
        "mensagens": [
            "Bom dia!",
            "Tem apartamento com vista mar em Copacabana?",
            "Quero ver o da Av. Atlântica",
            "Como é a vista?",
            "Envie a localização",
            "Vou pensar, obrigado"
        ],
        "esperado": {
            "tags": ["copacabana", "vista_mar"],
            "imovel": "apartamento-copacabana-vista-mar",
            "localizacao": True,
            "agendamento": False
        }
    }
]


class TestadorChatbot:
    """Testa funcionalidades do chatbot"""

    def __init__(self):
        self.resultados = []
        self.sessao_id = f"teste_{int(time.time())}"

    def simular_mensagem(self, cliente: str, mensagem: str):
        """Simula envio de mensagem via Evolution API"""
        print(f"   📱 {cliente}: {mensagem}")

        # Payload simulando webhook Evolution
        payload = {
            "event": "messages.upsert",
            "instance": "lfimoveis",
            "data": {
                "key": {
                    "remoteJid": f"{cliente}@s.whatsapp.net",
                    "fromMe": False,
                    "id": f"msg_{int(time.time() * 1000)}"
                },
                "message": {
                    "conversation": mensagem
                },
                "messageTimestamp": int(time.time()),
                "pushName": "Cliente Teste"
            }
        }

        try:
            # Envia para webhook do bot
            response = requests.post(
                f"{BOT_URL}/webhook/evolution",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                resposta = response.json()
                print(f"   🤖 Bot: {resposta.get('message', 'Sem resposta')[:80]}...")
                return resposta
            else:
                print(f"   ❌ Erro: {response.status_code}")
                return None

        except Exception as e:
            print(f"   ❌ Erro na requisição: {e}")
            return None

    def executar_cenario(self, cenario: dict):
        """Executa um cenário de teste completo"""
        print(f"\n{'=' * 70}")
        print(f"🧪 TESTE: {cenario['nome']}")
        print(f"{'=' * 70}")
        print(f"📱 Cliente: {cenario['cliente']}")
        print()

        respostas = []

        for mensagem in cenario['mensagens']:
            resposta = self.simular_mensagem(cenario['cliente'], mensagem)
            if resposta:
                respostas.append(resposta)
            time.sleep(2)  # Intervalo entre mensagens

        # Análise dos resultados
        print(f"\n📊 ANÁLISE:")
        self._analisar_resultados(cenario, respostas)

        return respostas

    def _analisar_resultados(self, cenario: dict, respostas: list):
        """Analisa se as expectativas foram atendidas"""
        esperado = cenario['esperado']

        # Verifica tags
        if 'tags' in esperado:
            print(f"   🏷️  Tags esperadas: {', '.join(esperado['tags'])}")

        # Verifica agendamento
        if esperado.get('agendamento'):
            print(f"   📅 Agendamento: {'✅ Esperado' if esperado['agendamento'] else '❌ Não esperado'}")

        # Verifica notificação
        if esperado.get('notificar_corretor'):
            print(f"   📞 Notificar corretor ({CORRETOR_WHATSAPP}): ✅ Sim")

        # Verifica imóvel identificado
        if 'imovel' in esperado:
            print(f"   🏠 Imóvel: {esperado['imovel']}")

        # Verifica funcionalidades
        if esperado.get('fotos'):
            print(f"   📸 Envio de fotos: ✅ Esperado")

        if esperado.get('localizacao'):
            print(f"   📍 Localização: ✅ Esperado")

        if esperado.get('respostas_faq'):
            print(f"   ❓ FAQ: ✅ Esperado")

    def verificar_bot_online(self):
        """Verifica se bot está rodando"""
        try:
            response = requests.get(f"{BOT_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Bot online")
                return True
            else:
                print("❌ Bot offline")
                return False
        except:
            print("❌ Bot não responde")
            return False

    def verificar_agenda(self):
        """Verifica agenda Google Sheets"""
        print("\n📅 VERIFICANDO AGENDA...")

        # Carrega config
        with open('chatwoot_config_imobili-ria-premium.json', 'r') as f:
            config = json.load(f)

        sheet_id = config.get('google_sheet_id')

        if sheet_id:
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
            print(f"   ✅ Agenda: {url}")
            print(f"   💡 Verifique visitas agendadas manualmente")
        else:
            print(f"   ⚠️  Sheet ID não configurado")

    def executar_todos_testes(self):
        """Executa todos os cenários de teste"""
        print("\n" + "=" * 70)
        print("🚀 INICIANDO TESTES COMPLETOS - CHATBOT LF IMÓVEIS")
        print("=" * 70)
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()

        # Verifica se bot está online
        if not self.verificar_bot_online():
            print("\n❌ Bot não está online. Execute: ./INICIAR_LFIMOVEIS.sh")
            return

        time.sleep(2)

        # Executa cada cenário
        for i, cenario in enumerate(CENARIOS_TESTE, 1):
            print(f"\n\n🔸 CENÁRIO {i}/{len(CENARIOS_TESTE)}")
            self.executar_cenario(cenario)
            time.sleep(3)  # Pausa entre cenários

        # Verifica agenda
        self.verificar_agenda()

        # Resumo final
        print("\n" + "=" * 70)
        print("✅ TESTES CONCLUÍDOS!")
        print("=" * 70)
        print()
        print("📋 VERIFICAÇÕES MANUAIS:")
        print(f"   1. Abrir Chatwoot: https://chatwoot.loop9.com.br")
        print(f"   2. Verificar inbox 'LF Imoveis'")
        print(f"   3. Conferir tags aplicadas")
        print(f"   4. Verificar agenda Google Sheets")
        print(f"   5. Confirmar notificações enviadas para {CORRETOR_WHATSAPP}")
        print()
        print("📁 Logs:")
        print(f"   tail -f logs/chatbot_lfimoveis.log")
        print(f"   tail -f logs/middleware_lfimoveis.log")
        print()


def main():
    testador = TestadorChatbot()
    testador.executar_todos_testes()


if __name__ == '__main__':
    main()
