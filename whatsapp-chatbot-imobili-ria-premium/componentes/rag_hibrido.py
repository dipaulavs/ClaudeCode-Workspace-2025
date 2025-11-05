#!/usr/bin/env python3
"""
🎯 RAG HÍBRIDO - Function Calling + MCP (IMOBILI-RIA-PREMIUM GENÉRICO)

⚠️ CUSTOMIZAÇÃO OBRIGATÓRIA:
1. Ajuste ferramentas locais conforme seu negócio
2. Ajuste ferramentas MCP conforme necessário
3. Renomeie referências genéricas (imoveis → carros/imoveis/produtos)
4. Ajuste prompts do system_prompt

ESTRUTURA:
- Ferramentas LOCAIS: Rápidas, críticas para conversação (0ms overhead)
- Ferramentas MCP: Pesadas, reutilizáveis (~150ms cada)

A IA decide automaticamente qual usar baseado no contexto.
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

# Adiciona paths
sys.path.append(str(Path(__file__).parent.parent / "ferramentas"))
sys.path.append(str(Path(__file__).parent))

# ⚠️ CUSTOMIZAR: Importar suas ferramentas locais
# Use lista_imoveis (genérico) OU lista_carros/lista_imoveis (específico)
try:
    from lista_imoveis import listar_imoveis_disponiveis, formatar_lista_para_mensagem
except ImportError:
    from lista_carros import listar_carros_disponiveis as listar_imoveis_disponiveis
    from lista_carros import formatar_lista_para_mensagem

from consulta_faq import consultar_faq_carro as consultar_faq_imóvel
from tagueamento import obter_carro_ativo as obter_imóvel_ativo, taguear_cliente
from cliente_mcp import ClienteMCP


class RAGHibrido:
    """
    RAG híbrido: Function Calling (local) + MCP (remoto)

    ⚠️ CUSTOMIZAR para seu negócio
    """

    def __init__(self, imoveis_dir, openai_api_key, openrouter_api_key, redis_client, mcp_server_path: Optional[str] = None):
        self.imoveis_dir = imoveis_dir
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

        print("✅ RAG Híbrido inicializado", flush=True)
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

        # Verifica imóvel ativo
        imóvel_ativo = obter_imóvel_ativo(numero_cliente, self.redis)

        # ⚠️ CUSTOMIZAR: Ajuste prompt conforme seu negócio
        system_prompt = f"""{self.personalidade}

🔧 FERRAMENTAS DISPONÍVEIS:

Você tem 9 ferramentas. Use a ferramenta correta para cada situação!

📋 FERRAMENTAS LOCAIS (rápidas - use sempre que possível):

1. **lista_imoveis** - Lista imoveis disponíveis
2. **consulta_faq** - Consulta FAQ do imóvel ativo
3. **taguear_cliente** - Marca cliente interessado em imóvel
4. **agendar_visita** - Agenda visita/atendimento (2 etapas: sugerir → confirmar)

💡 FERRAMENTAS MCP (pesadas - use quando necessário):

5. **analisar_sentimento** - Analisa emoção/tom da conversa
6. **gerar_proposta_comercial** - Gera proposta formal
7. **buscar_imoveis_similares** - Busca por características
8. **calcular_financiamento** - Simulação de financiamento
9. **consultar_tabela_preco** - Preço de mercado/tabela

{"🎯 ITEM ATIVO: " + imóvel_ativo if imóvel_ativo else "❌ SEM ITEM ATIVO"}

⚠️ QUANDO USAR CADA FERRAMENTA:

📋 **lista_imoveis**: Cliente pergunta "o que tem", "me mostra", "quais opções"
❓ **consulta_faq**: Cliente pergunta sobre imóvel específico (preço, detalhes)
🏷️ **taguear_cliente**: Cliente demonstra interesse em imóvel específico
🗓️ **agendar_visita**: Cliente quer agendar (2 etapas obrigatórias)

😊 **analisar_sentimento**: Cliente frustrado, ansioso ou indeciso
📄 **gerar_proposta_comercial**: Cliente pede proposta formal/por escrito
🔍 **buscar_imoveis_similares**: Cliente não encontrou o que quer ("tem algo parecido?")
💰 **calcular_financiamento**: Cliente pergunta sobre financiamento/parcelas
💵 **consultar_tabela_preco**: Cliente pergunta "quanto vale?" ou preço de mercado

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
        """
        Define todas as ferramentas (locais + MCP)

        ⚠️ CUSTOMIZAR: Ajuste descrições conforme seu negócio
        """

        # FERRAMENTAS LOCAIS
        ferramentas_locais = [
            {
                "type": "function",
                "function": {
                    "name": "lista_imoveis",
                    "description": "Lista todos os imoveis disponíveis",  # ⚠️ CUSTOMIZAR
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "consulta_faq",
                    "description": "Consulta FAQ do imóvel ativo",
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
                    "description": "Marca cliente como interessado em imóvel",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "imóvel_id": {"type": "string", "description": "ID do imóvel"}
                        },
                        "required": ["imóvel_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "agendar_visita",
                    "description": "Agenda visita/atendimento: sugerir horários ou confirmar escolha",
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
                                "imóvels": {"type": "string"},
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
                            "imóvel_id": {"type": "string"},
                            "cliente_nome": {"type": "string"},
                            "desconto_percentual": {"type": "number"}
                        },
                        "required": ["imóvel_id", "cliente_nome"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "buscar_imoveis_similares",
                    "description": "Busca imoveis similares (use quando cliente não encontrou o que quer)",
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
                            "valor_total": {"type": "number"},
                            "valor_entrada": {"type": "number"},
                            "taxa_juros_mensal": {"type": "number"}
                        },
                        "required": ["valor_total"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "consultar_tabela_preco",
                    "description": "Consulta preço de mercado/tabela",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tipo": {"type": "string"},
                            "modelo": {"type": "string"},
                            "ano": {"type": "string"}
                        },
                        "required": ["tipo", "modelo"]
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
        """
        Executa ferramenta (local ou MCP)

        ⚠️ CUSTOMIZAR: Ajuste execução conforme suas ferramentas
        """
        import json

        # FERRAMENTAS LOCAIS
        if nome == "lista_imoveis":
            imoveis = listar_imoveis_disponiveis(self.imoveis_dir)
            return formatar_lista_para_mensagem(imoveis)

        elif nome == "consulta_faq":
            imóvel_ativo = obter_imóvel_ativo(numero_cliente, self.redis)
            if not imóvel_ativo:
                return "ERRO: Cliente não tem imóvel ativo."

            pergunta = args.get('pergunta', '')
            resultado_faq = consultar_faq_imóvel(imóvel_ativo, pergunta, self.imoveis_dir)
            if resultado_faq['sucesso']:
                return f"{resultado_faq['base']}\n\n{resultado_faq['faq']}"
            else:
                return resultado_faq['erro']

        elif nome == "taguear_cliente":
            imóvel_id = args['imóvel_id']
            config_path = Path(__file__).parent.parent / "chatwoot_config.json"
            with open(config_path, 'r') as f:
                config = json.load(f)

            resultado_tag = taguear_cliente(numero_cliente, imóvel_id, self.redis, config['chatwoot'])
            if resultado_tag['sucesso']:
                return f"✅ Cliente marcado como interessado em {imóvel_id}"
            else:
                return f"⚠️ Erro: {resultado_tag['erro']}"

        elif nome == "agendar_visita":
            from ferramentas.agendar_visita import agendar_visita_vendedor

            config_path = Path(__file__).parent.parent / "chatwoot_config.json"
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
        elif nome in ["analisar_sentimento", "gerar_proposta_comercial", "buscar_imoveis_similares",
                      "calcular_financiamento", "consultar_tabela_preco"]:

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
    print("🧪 RAG Híbrido - Imobiliária Premium Genérico\n")
    print("⚠️ CUSTOMIZAR: Ajuste para seu negócio antes de usar")
    print("Este módulo deve ser importado pelo chatbot principal")
