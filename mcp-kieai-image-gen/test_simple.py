#!/usr/bin/env python3
"""
Teste simples do servidor MCP - apenas lista as ferramentas
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("🧪 Testando MCP Server KIE.AI...")

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializa a sessão
                await session.initialize()
                print("✅ Servidor inicializado com sucesso!")

                # Lista as ferramentas disponíveis
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"\n📋 Ferramentas disponíveis ({len(tools)}):\n")

                for tool in tools:
                    print(f"  🔧 {tool.name}")
                    print(f"     {tool.description}\n")

                print("=" * 60)
                print("✅ Teste concluído! Servidor está funcionando.")
                print("=" * 60)

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
