#!/usr/bin/env python3.11
"""
Script para listar designs do Canva via MCP
Conecta ao MCP server do Canva e lista designs disponíveis
"""

import asyncio
import json
import sys
from pathlib import Path

try:
    import httpx
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("❌ Erro: Bibliotecas MCP não instaladas")
    print("Execute: python3.11 -m pip install mcp httpx")
    sys.exit(1)


class CanvaMCPClient:
    """Cliente para interagir com Canva MCP Server"""

    def __init__(self, mcp_url: str = "https://mcp.canva.com/mcp"):
        self.mcp_url = mcp_url
        self.session = None

    async def connect(self):
        """Conecta ao servidor MCP do Canva"""
        print(f"🔌 Conectando ao Canva MCP: {self.mcp_url}")

        # Para MCP HTTP, precisamos usar httpx diretamente
        self.client = httpx.AsyncClient(timeout=30.0)

        # Verificar se servidor está acessível
        try:
            response = await self.client.get(self.mcp_url)
            print(f"✅ Servidor respondeu: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False

    async def list_tools(self):
        """Lista ferramentas disponíveis no MCP"""
        print("\n🔧 Listando ferramentas disponíveis...")

        try:
            # Endpoint padrão MCP para listar tools
            response = await self.client.post(
                self.mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                },
                headers={
                    "Content-Type": "application/json"
                }
            )

            if response.status_code == 200:
                data = response.json()
                if "result" in data and "tools" in data["result"]:
                    tools = data["result"]["tools"]
                    print(f"\n✅ {len(tools)} ferramentas disponíveis:")
                    for tool in tools:
                        print(f"  • {tool.get('name')}: {tool.get('description', 'Sem descrição')}")
                    return tools
                else:
                    print(f"⚠️ Resposta inesperada: {data}")
            else:
                print(f"❌ Erro HTTP {response.status_code}")
                print(f"Resposta: {response.text}")

                # Se receber 401, significa que precisa autenticar
                if response.status_code == 401:
                    print("\n⚠️ AUTENTICAÇÃO NECESSÁRIA")
                    print("O MCP do Canva requer OAuth para acessar suas ferramentas.")
                    print("\nPara autenticar:")
                    print("1. Use Claude.ai web (já autenticado)")
                    print("2. Ou configure OAuth manualmente (requer token)")

        except Exception as e:
            print(f"❌ Erro ao listar ferramentas: {e}")

        return None

    async def call_tool(self, tool_name: str, arguments: dict = None):
        """Chama uma ferramenta específica do MCP"""
        print(f"\n🚀 Chamando ferramenta: {tool_name}")

        try:
            response = await self.client.post(
                self.mcp_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments or {}
                    }
                },
                headers={
                    "Content-Type": "application/json"
                }
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Resposta recebida:")
                print(json.dumps(data, indent=2))
                return data
            else:
                print(f"❌ Erro HTTP {response.status_code}")
                print(f"Resposta: {response.text}")

        except Exception as e:
            print(f"❌ Erro ao chamar ferramenta: {e}")

        return None

    async def list_designs(self):
        """Lista designs do Canva do usuário"""
        print("\n📋 Listando designs do Canva...")

        # Primeiro, vamos descobrir qual ferramenta usar
        tools = await self.list_tools()

        if not tools:
            return None

        # Procurar ferramenta relacionada a designs
        design_tools = [t for t in tools if 'design' in t.get('name', '').lower() or 'list' in t.get('name', '').lower()]

        if design_tools:
            print(f"\n🔍 Encontradas {len(design_tools)} ferramentas de design:")
            for tool in design_tools:
                print(f"  • {tool['name']}")

            # Tentar usar a primeira
            result = await self.call_tool(design_tools[0]['name'])
            return result
        else:
            print("⚠️ Nenhuma ferramenta de listagem de designs encontrada")
            return None

    async def close(self):
        """Fecha conexão"""
        if self.client:
            await self.client.aclose()


async def main():
    """Função principal"""
    print("=" * 60)
    print("🎨 CANVA MCP CLIENT - Listagem de Designs")
    print("=" * 60)

    # Criar cliente
    client = CanvaMCPClient()

    try:
        # Conectar
        connected = await client.connect()

        if not connected:
            print("\n❌ Falha ao conectar ao servidor MCP")
            return

        # Listar designs
        await client.list_designs()

    except KeyboardInterrupt:
        print("\n\n⚠️ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Fechar conexão
        await client.close()
        print("\n" + "=" * 60)
        print("✅ Conexão encerrada")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
