#!/usr/bin/env python3
"""
🤖 AGENTE PRINCIPAL SIMPLES

Responsabilidade ÚNICA:
- Conversa com cliente usando personalidade
- Decide quando chamar sub-agente FAQ
- NÃO busca informações diretamente

Prompt CURTO (max 50 linhas)
"""

import requests
import json
from pathlib import Path


class AgentePrincipalSimples:
    """
    Agente conversacional que delega buscas ao SubAgenteFAQ
    """

    def __init__(self, personalidade: str, redis_client, config: dict):
        self.personalidade = personalidade
        self.redis = redis_client
        self.config = config

    def processar(self, mensagem: str, contexto: list, numero_cliente: str, imovel_ativo: str = None) -> str:
        """
        Processa mensagem do cliente

        Args:
            mensagem: Mensagem do cliente
            contexto: Histórico de conversas
            numero_cliente: Número do WhatsApp
            imovel_ativo: ID do imóvel ativo (se houver)

        Returns:
            Resposta do agente
        """

        # ═══════════════════════════════════════════
        # PROMPT CURTO - SÓ PERSONALIDADE + 1 FERRAMENTA
        # ═══════════════════════════════════════════
        system_prompt = f"""{self.personalidade}

{"🏠 IMÓVEL ATIVO: " + imovel_ativo if imovel_ativo else "❌ SEM IMÓVEL ATIVO"}

🔧 FERRAMENTA DISPONÍVEL:

**buscar_faq** - Busca informações do imóvel ativo
- Use quando cliente perguntar sobre: preço, características, localização, documentação
- Se NÃO tem imóvel ativo: pergunte qual imóvel interessa primeiro

REGRAS:
✅ Use buscar_faq quando precisar de dados específicos
❌ NUNCA invente informações sobre imóveis
✅ Seja natural e consultivo na resposta final
"""

        # Monta mensagens
        mensagens = [{"role": "system", "content": system_prompt}]

        # Adiciona contexto (últimas 6)
        for msg in contexto[-6:]:
            mensagens.append(msg)

        # Mensagem atual
        mensagens.append({"role": "user", "content": mensagem})

        # Define ferramenta
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "buscar_faq",
                    "description": "Busca informações do imóvel ativo (base.txt + faq.txt)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pergunta": {
                                "type": "string",
                                "description": "Pergunta do cliente (opcional)"
                            }
                        }
                    }
                }
            }
        ]

        # Chama Claude via OpenRouter
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.config['openrouter_api_key']}",
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

                print(f"   🔧 Agente chamou: {function_name}", flush=True)

                if function_name == "buscar_faq":
                    # Delega para sub-agente (será implementado no rag_simples_imoveis.py)
                    return {
                        "tipo": "chamar_subagente",
                        "subagente": "faq",
                        "args": {
                            "imovel_id": imovel_ativo,
                            "pergunta": function_args.get('pergunta', '')
                        },
                        "mensagens": mensagens,
                        "message": message,
                        "tool_call": tool_call
                    }

            # Resposta direta (sem ferramenta)
            resposta = message['content'].strip()
            return {
                "tipo": "resposta_direta",
                "texto": resposta
            }

        except Exception as e:
            print(f"❌ Erro no Agente Principal: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return {
                "tipo": "erro",
                "texto": "Desculpa, tive um problema. Pode repetir? 😊"
            }


if __name__ == "__main__":
    print("🤖 AgentePrincipalSimples")
    print("Este módulo deve ser importado pelo rag_simples_imoveis.py")
