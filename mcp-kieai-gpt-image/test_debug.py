#!/usr/bin/env python3
"""
Debug do MCP Server
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("🔍 Debug do MCP Server GPT-4o")
    print("=" * 60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Server inicializado\n")

            # Lista tools
            tools = await session.list_tools()
            print(f"📋 Tools disponíveis: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"   - {tool.name}")
            print()

            # Testa com 1 imagem simples
            print("🧪 Teste simples (1 imagem)...")
            try:
                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A cute cat",
                        "size": "1:1",
                        "nVariants": 1,
                        "wait_for_completion": True
                    }
                )

                print(f"✅ Resultado recebido:")
                print(f"   Tipo: {type(result)}")
                print(f"   Content: {result.content}")
                print(f"   Content[0]: {result.content[0]}")
                print(f"   Text: {result.content[0].text}")

            except Exception as e:
                print(f"❌ Erro: {e}")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
