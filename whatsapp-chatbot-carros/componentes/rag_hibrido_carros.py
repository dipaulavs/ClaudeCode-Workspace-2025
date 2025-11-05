#!/usr/bin/env python3
"""
🎯 RAG HÍBRIDO - Function Calling + MCP

Combina ferramentas locais (rápidas) com ferramentas MCP (pesadas).

FERRAMENTAS LOCAIS (Function Calling):
- lista_carros: Lista carros disponíveis
- consulta_faq: Consulta FAQ do carro ativo
- taguear_cliente: Marca interesse em carro
- agendar_visita: Agenda visita (2 etapas)

FERRAMENTAS MCP (remotas):
- analisar_sentimento: Análise emocional da conversa
- gerar_proposta_comercial: Gera proposta estruturada
- buscar_carros_similares: Busca semântica
- calcular_financiamento: Simulação financeira
- consultar_fipe: Preço FIPE
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

# Adiciona paths
sys.path.append(str(Path(__file__).parent.parent / "ferramentas"))
sys.path.append(str(Path(__file__).parent))

from lista_carros import listar_carros_disponiveis, formatar_lista_para_mensagem
from consulta_faq import consultar_faq_carro
from tagueamento import obter_carro_ativo, taguear_cliente
from cliente_mcp import ClienteMCP


class RAGHibridoCarros:
    """
    RAG híbrido: Function Calling (local) + MCP (remoto)
    """

    def __init__(self, carros_dir, openai_api_key, openrouter_api_key, redis_client, mcp_server_path: Optional[str] = None):
        self.carros_dir = carros_dir
        self.openai_key = openai_api_key
        self.openrouter_key = openrouter_api_key
        self.redis = redis_client
        self.mcp_server_path = mcp_server_path

        # Cliente MCP (iniciado on-demand)
        self.mcp_cliente = None

        # Carrega personalidade
        personalidade_file = Path(__file__).parent.parent / "personalidade.txt"
        with open(personalidade_file, 'r', encoding='utf-8') as f:
            self.personalidade = f.read().strip()

        print("✅ RAGHibridoCarros inicializado", flush=True)
        if mcp_server_path:
            print(f"   📡 MCP: {mcp_server_path}", flush=True)

    async def _garantir_mcp(self):
        """Inicia cliente MCP se necessário"""
        if self.mcp_server_path and not self.mcp_cliente:
            self.mcp_cliente = ClienteMCP(self.mcp_server_path)
            await self.mcp_cliente.conectar()
            print("✅ Cliente MCP conectado", flush=True)

    def processar_mensagem(self, numero_cliente: str, mensagem: str, contexto: list) -> str:
        """
        Processa mensagem usando ferramentas híbridas

        Interface síncrona para compatibilidade com chatbot atual
        """
        # Cria event loop se necessário
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Executa processamento assíncrono
        return loop.run_until_complete(
            self._processar_mensagem_async(numero_cliente, mensagem, contexto)
        )

    async def _processar_mensagem_async(self, numero_cliente: str, mensagem: str, contexto: list) -> str:
        """Processamento assíncrono"""
        import requests
        import json

        # Garante MCP conectado
        await self._garantir_mcp()

        # Verifica carro ativo
        carro_ativo = obter_carro_ativo(numero_cliente, self.redis)

        # Monta prompt com personalidade + ferramentas
        system_prompt = f"""{self.personalidade}

🔧 FERRAMENTAS DISPONÍVEIS:

Você tem 9 ferramentas. Use a ferramenta correta para cada situação!

📋 FERRAMENTAS LOCAIS (rápidas - use sempre que possível):

1. **lista_carros** - Lista carros disponíveis
2. **consulta_faq** - Consulta FAQ do carro ativo
3. **taguear_cliente** - Marca cliente interessado em carro
4. **agendar_visita** - Agenda visita (2 etapas: sugerir → confirmar)

💡 FERRAMENTAS MCP (pesadas - use quando necessário):

5. **analisar_sentimento** - Analisa emoção/tom da conversa
6. **gerar_proposta_comercial** - Gera proposta formal
7. **buscar_carros_similares** - Busca por características
8. **calcular_financiamento** - Simulação de financiamento
9. **consultar_fipe** - Preço FIPE do veículo

{"🚗 CARRO ATIVO: " + carro_ativo if carro_ativo else "❌ SEM CARRO ATIVO"}

⚠️ QUANDO USAR CADA FERRAMENTA:

📋 **lista_carros**: Cliente pergunta "quais carros", "o que tem", "me mostra"
❓ **consulta_faq**: Cliente pergunta sobre carro específico (preço, garantia, motor)
🏷️ **taguear_cliente**: Cliente demonstra interesse em carro específico
🗓️ **agendar_visita**: Cliente quer agendar (2 etapas obrigatórias)

😊 **analisar_sentimento**: Cliente frustrado, ansioso ou indeciso
📄 **gerar_proposta_comercial**: Cliente pede proposta formal/por escrito
🔍 **buscar_carros_similares**: Cliente não encontrou o que quer ("tem algo parecido?")
💰 **calcular_financiamento**: Cliente pergunta sobre financiamento/parcelas
💵 **consultar_fipe**: Cliente pergunta "quanto vale na FIPE?"

🚨 REGRAS:
- Prefira ferramentas locais (mais rápidas)
- Use MCP apenas quando necessário
- NUNCA invente informações
"""

        # Monta mensagens
        mensagens = [{"role": "system", "content": system_prompt}]

        # Adiciona contexto (últimas 6 msgs)
        for msg in contexto[-6:]:
            mensagens.append(msg)

        # Adiciona mensagem atual
        mensagens.append({"role": "user", "content": mensagem})

        # Define TODAS as ferramentas (locais + MCP)
        tools = self._definir_ferramentas()

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

                # Executa ferramenta (local ou MCP)
                resultado_ferramenta = await self._executar_ferramenta(
                    function_name,
                    function_args,
                    numero_cliente
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
            print(f"❌ Erro no RAG Híbrido: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return "Desculpa, tive um problema. Pode repetir? 😊"

    def _definir_ferramentas(self) -> List[Dict]:
        """Define todas as ferramentas (locais + MCP)"""

        # FERRAMENTAS LOCAIS
        ferramentas_locais = [
            {
                "type": "function",
                "function": {
                    "name": "lista_carros",
                    "description": "Lista todos os carros disponíveis com marca, modelo, ano e preço",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "consulta_faq",
                    "description": "Consulta FAQ do carro ativo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pergunta": {"type": "string", "description": "Pergunta do cliente"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "taguear_cliente",
                    "description": "Marca cliente como interessado em carro",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "carro_id": {"type": "string", "description": "ID do carro"}
                        },
                        "required": ["carro_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "agendar_visita",
                    "description": "Agenda visita: sugerir horários ou confirmar escolha",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "acao": {
                                "type": "string",
                                "enum": ["sugerir", "confirmar"]
                            },
                            "escolha": {"type": "string"}
                        },
                        "required": ["acao"]
                    }
                }
            }
        ]

        # FERRAMENTAS MCP
        ferramentas_mcp = [
            {
                "type": "function",
                "function": {
                    "name": "analisar_sentimento",
                    "description": "Analisa sentimento da conversa (use quando cliente frustrado/indeciso)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "mensagens": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Últimas mensagens do cliente"
                            }
                        },
                        "required": ["mensagens"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "gerar_proposta_comercial",
                    "description": "Gera proposta formal (use quando cliente pede proposta por escrito)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "carro_id": {"type": "string"},
                            "cliente_nome": {"type": "string"},
                            "desconto_percentual": {"type": "number"}
                        },
                        "required": ["carro_id", "cliente_nome"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "buscar_carros_similares",
                    "description": "Busca carros similares (use quando cliente não encontrou o que quer)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caracteristicas": {"type": "string"},
                            "limite": {"type": "number"}
                        },
                        "required": ["caracteristicas"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calcular_financiamento",
                    "description": "Calcula financiamento em múltiplos cenários",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "valor_veiculo": {"type": "number"},
                            "valor_entrada": {"type": "number"},
                            "taxa_juros_mensal": {"type": "number"}
                        },
                        "required": ["valor_veiculo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "consultar_fipe",
                    "description": "Consulta preço FIPE do veículo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "marca": {"type": "string"},
                            "modelo": {"type": "string"},
                            "ano": {"type": "string"}
                        },
                        "required": ["marca", "modelo", "ano"]
                    }
                }
            }
        ]

        # Retorna todas (se MCP disponível)
        if self.mcp_server_path:
            return ferramentas_locais + ferramentas_mcp
        else:
            return ferramentas_locais

    async def _executar_ferramenta(self, nome: str, args: Dict, numero_cliente: str) -> str:
        """Executa ferramenta (local ou MCP)"""
        import json

        # FERRAMENTAS LOCAIS
        if nome == "lista_carros":
            carros = listar_carros_disponiveis(self.carros_dir)
            return formatar_lista_para_mensagem(carros)

        elif nome == "consulta_faq":
            carro_ativo = obter_carro_ativo(numero_cliente, self.redis)
            if not carro_ativo:
                return "ERRO: Cliente não tem carro ativo."

            pergunta = args.get('pergunta', '')
            resultado_faq = consultar_faq_carro(carro_ativo, pergunta, self.carros_dir)
            if resultado_faq['sucesso']:
                return f"{resultado_faq['base']}\n\n{resultado_faq['faq']}"
            else:
                return resultado_faq['erro']

        elif nome == "taguear_cliente":
            carro_id = args['carro_id']
            config_path = Path(__file__).parent.parent / "chatwoot_config_automaia.json"
            with open(config_path, 'r') as f:
                config = json.load(f)

            resultado_tag = taguear_cliente(numero_cliente, carro_id, self.redis, config['chatwoot'])
            if resultado_tag['sucesso']:
                return f"✅ Cliente marcado como interessado em {carro_id}"
            else:
                return f"⚠️ Erro: {resultado_tag['erro']}"

        elif nome == "agendar_visita":
            from ferramentas.agendar_visita import agendar_visita_vendedor

            config_path = Path(__file__).parent.parent / "chatwoot_config_automaia.json"
            with open(config_path, 'r') as f:
                config = json.load(f)

            acao = args['acao']
            escolha = args.get('escolha', None)

            return agendar_visita_vendedor(
                acao=acao,
                cliente_numero=numero_cliente,
                redis_client=self.redis,
                config=config,
                escolha=escolha
            )

        # FERRAMENTAS MCP
        elif nome in ["analisar_sentimento", "gerar_proposta_comercial", "buscar_carros_similares",
                      "calcular_financiamento", "consultar_fipe"]:

            if not self.mcp_cliente:
                return "⚠️ MCP não disponível"

            try:
                resultado = await self.mcp_cliente.chamar_ferramenta(nome, args)
                return json.dumps(resultado, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"❌ Erro MCP: {e}"

        else:
            return f"❌ Ferramenta desconhecida: {nome}"

    async def __aenter__(self):
        """Context manager enter"""
        await self._garantir_mcp()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.mcp_cliente:
            await self.mcp_cliente.desconectar()


# ==============================================================================
# TESTE
# ==============================================================================

if __name__ == "__main__":
    print("🧪 RAG Híbrido - Teste\n")
    print("Este módulo deve ser importado pelo chatbot_automaia_v4.py")
