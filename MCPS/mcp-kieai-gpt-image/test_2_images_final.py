#!/usr/bin/env python3
"""
Teste final: Criar 2 imagens em paralelo com MCP corrigido
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("🧪 Teste: Criar 2 imagens GPT-4o em paralelo via MCP")
    print("=" * 60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ MCP Server inicializado\n")

            # Teste: Criar 2 imagens
            print("📸 Gerando 2 imagens em paralelo...")
            print("-" * 60)

            result = await session.call_tool(
                "generate_image",
                arguments={
                    "prompts": [
                        "A professional photo of a modern workspace with laptop",
                        "A serene mountain landscape at golden hour"
                    ],
                    "size": "1:1",
                    "nVariants": 1,
                    "auto_download": True,
                    "wait_for_completion": True
                }
            )

            response = json.loads(result.content[0].text)

            print(f"\n✅ Resultado:")
            print(f"   Total: {response['total']} imagens")
            print(f"   Sucesso: {response['successful']}")
            print(f"   Falhas: {response['failed']}")
            print(f"   Tempo total: {response['total_time']}s")
            print()

            for i, res in enumerate(response['results'], 1):
                print(f"{i}. Status: {res['status']}")
                if res['status'] == 'success':
                    print(f"   Tempo: {res['cost_time']}s")
                    print(f"   Imagens: {len(res['image_urls'])}")
                    for img_url in res['image_urls']:
                        print(f"      {img_url}")
                    if 'downloads' in res:
                        print(f"   📥 Download: {res['downloads'][0]['filename']}")
                else:
                    print(f"   ❌ Erro: {res.get('error', 'Unknown')}")
                print()

            print("=" * 60)
            print("✅ Teste concluído!")


if __name__ == "__main__":
    asyncio.run(main())
