#!/usr/bin/env python3
"""
🎯 RAG SIMPLES - Adapter para usar com Orquestrador

Converte nossas 3 ferramentas (lista_carros, consulta_faq, tagueamento)
em interface compatível com Orquestrador Híbrido.
"""

import sys
from pathlib import Path

# Adiciona path das ferramentas
sys.path.append(str(Path(__file__).parent.parent / "ferramentas"))

from lista_carros import listar_carros_disponiveis, formatar_lista_para_mensagem
from consulta_faq import consultar_faq_carro
from tagueamento import obter_carro_ativo, taguear_cliente


class RAGSimplesCarros:
    """
    Adapter que converte ferramentas em interface RAG para Orquestrador
    """

    def __init__(self, carros_dir, openai_api_key, openrouter_api_key, redis_client):
        self.carros_dir = carros_dir
        self.openai_key = openai_api_key
        self.openrouter_key = openrouter_api_key
        self.redis = redis_client

        # Carrega personalidade
        personalidade_file = Path(__file__).parent.parent / "personalidade.txt"
        with open(personalidade_file, 'r', encoding='utf-8') as f:
            self.personalidade = f.read().strip()

        print("✅ RAGSimplesCarros inicializado", flush=True)

    def processar_mensagem(self, numero_cliente: str, mensagem: str, contexto: list) -> str:
        """
        Processa mensagem usando ferramentas

        Interface compatível com Orquestrador
        """
        import requests
        import json

        # Verifica carro ativo
        carro_ativo = obter_carro_ativo(numero_cliente, self.redis)

        # Monta prompt com personalidade + ferramentas
        system_prompt = f"""{self.personalidade}

🔧 FERRAMENTAS OBRIGATÓRIAS:

Você tem 4 ferramentas. SEMPRE use a ferramenta correta - NUNCA invente informações!

1. **lista_carros** - Lista carros disponíveis
2. **consulta_faq** - Consulta FAQ do carro ativo
3. **taguear_cliente** - Marca cliente interessado em carro
4. **agendar_visita** - Agenda visita com vendedor (sugerir horários ou confirmar)

{"🚗 CARRO ATIVO: " + carro_ativo if carro_ativo else "❌ SEM CARRO ATIVO"}

⚠️ REGRAS OBRIGATÓRIAS (NUNCA QUEBRE):

📋 LISTA DE CARROS:
Cliente pergunta: "quais carros tem?", "me mostra", "o que tem?", "tenho X reais"
→ SEMPRE use lista_carros
→ NUNCA responda sem usar a ferramenta
→ NUNCA invente carros que não existem

❓ PERGUNTAS SOBRE CARRO:
Cliente pergunta: "preço", "garantia", "aceita troca", "qual motor"
→ SE tem carro ativo: SEMPRE use consulta_faq
→ SE NÃO tem carro ativo: Pergunte qual carro interessa PRIMEIRO

🏷️ ESCOLHA DE CARRO:
Cliente diz: "quero o Gol", "me fala do HB20", "interessado no Civic"
→ SEMPRE use taguear_cliente PRIMEIRO
→ Depois pode usar consulta_faq para responder

🗓️ AGENDAMENTO DE VISITA:
Cliente quer agendar: "quero agendar", "marcar visita", "quando posso ver"
→ PASSO 1: Use agendar_visita com acao="sugerir" (mostra opções)
→ PASSO 2: Cliente escolhe (1, 2 ou 3)
→ PASSO 3: Use agendar_visita com acao="confirmar" + escolha do cliente

Exemplo prático:
Cliente: "quero agendar uma visita"
→ Você: agendar_visita(acao="sugerir")
Bot mostra: "1️⃣ Amanhã 10h 2️⃣ Quarta 14h 3️⃣ Sexta 16h"
Cliente: "a 2"
→ Você: agendar_visita(acao="confirmar", escolha="2")

🚨 NUNCA FAÇA ISSO:
❌ Responder sobre carros sem usar lista_carros
❌ Responder detalhes sem usar consulta_faq
❌ Esquecer de taguear quando cliente escolhe carro
❌ Inventar horários disponíveis (sempre use a ferramenta!)
❌ Confirmar agendamento sem ter sugerido antes

✅ SEMPRE FAÇA ISSO:
✓ Use ferramenta ANTES de responder
✓ Adapte resposta da ferramenta ao seu tom
✓ Seja natural e amigável na resposta final
✓ Agendamento = 2 etapas (sugerir → confirmar)
"""

        # Monta mensagens para Claude
        mensagens = [{"role": "system", "content": system_prompt}]

        # Adiciona contexto (últimas 6 msgs)
        for msg in contexto[-6:]:
            mensagens.append(msg)

        # Adiciona mensagem atual
        mensagens.append({"role": "user", "content": mensagem})

        # Define ferramentas
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "lista_carros",
                    "description": "Lista todos os carros disponíveis na loja com marca, modelo, ano e preço",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "consulta_faq",
                    "description": "Consulta FAQ do carro ativo para responder perguntas específicas",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pergunta": {"type": "string", "description": "Pergunta do cliente (opcional)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "taguear_cliente",
                    "description": "Marca cliente como interessado em um carro específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "carro_id": {"type": "string", "description": "ID do carro (formato: marca-modelo-ano-001)"}
                        },
                        "required": ["carro_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "agendar_visita",
                    "description": "Agenda visita com vendedor. Primeiro sugere horários (acao='sugerir'), depois confirma escolha do cliente (acao='confirmar')",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "acao": {
                                "type": "string",
                                "description": "Ação: 'sugerir' (mostrar opções) ou 'confirmar' (após cliente escolher)",
                                "enum": ["sugerir", "confirmar"]
                            },
                            "escolha": {
                                "type": "string",
                                "description": "Escolha do cliente: '1', '2' ou '3' (apenas para acao='confirmar')"
                            }
                        },
                        "required": ["acao"]
                    }
                }
            }
        ]

        # Chama Claude
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "anthropic/claude-haiku-4.5",
                "messages": mensagens,
                "tools": tools,
                "temperature": 0.9,
                "max_tokens": 500
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            resultado = response.json()
            message = resultado['choices'][0]['message']

            # Verifica se chamou ferramenta
            if message.get('tool_calls'):
                tool_call = message['tool_calls'][0]
                function_name = tool_call['function']['name']
                function_args = json.loads(tool_call['function']['arguments'])

                print(f"   🔧 Ferramenta: {function_name}", flush=True)

                # Executa ferramenta
                if function_name == "lista_carros":
                    carros = listar_carros_disponiveis(self.carros_dir)
                    resultado_ferramenta = formatar_lista_para_mensagem(carros)

                elif function_name == "consulta_faq":
                    if not carro_ativo:
                        resultado_ferramenta = "ERRO: Cliente não tem carro ativo."
                    else:
                        pergunta = function_args.get('pergunta', '')
                        resultado_faq = consultar_faq_carro(carro_ativo, pergunta, self.carros_dir)
                        if resultado_faq['sucesso']:
                            resultado_ferramenta = f"{resultado_faq['base']}\n\n{resultado_faq['faq']}"
                        else:
                            resultado_ferramenta = resultado_faq['erro']

                elif function_name == "taguear_cliente":
                    carro_id = function_args['carro_id']
                    # Carrega config para tagueamento
                    config_path = Path(__file__).parent.parent / "chatwoot_config_automaia.json"
                    with open(config_path, 'r') as f:
                        config = json.load(f)

                    resultado_tag = taguear_cliente(numero_cliente, carro_id, self.redis, config['chatwoot'])
                    if resultado_tag['sucesso']:
                        resultado_ferramenta = f"✅ Cliente marcado como interessado em {carro_id}"
                    else:
                        resultado_ferramenta = f"⚠️ Erro: {resultado_tag['erro']}"

                elif function_name == "agendar_visita":
                    from ferramentas.agendar_visita import agendar_visita_vendedor

                    # Carrega config completo
                    config_path = Path(__file__).parent.parent / "chatwoot_config_automaia.json"
                    with open(config_path, 'r') as f:
                        config = json.load(f)

                    acao = function_args['acao']
                    escolha = function_args.get('escolha', None)

                    resultado_ferramenta = agendar_visita_vendedor(
                        acao=acao,
                        cliente_numero=numero_cliente,
                        redis_client=self.redis,
                        config=config,
                        escolha=escolha
                    )

                # Adiciona resultado ao contexto
                mensagens.append(message)
                mensagens.append({
                    "role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": resultado_ferramenta
                })

                # Claude gera resposta final
                payload['messages'] = mensagens
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                resultado = response.json()

            # Resposta final
            resposta = resultado['choices'][0]['message']['content'].strip()
            return resposta

        except Exception as e:
            print(f"❌ Erro no RAG: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return "Desculpa, tive um problema. Pode repetir? 😊"


if __name__ == "__main__":
    print("🧪 RAGSimplesCarros - Adapter para Orquestrador")
    print("Este módulo deve ser importado pelo chatbot_automaia_v4.py")
