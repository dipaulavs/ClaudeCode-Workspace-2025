#!/usr/bin/env python3
"""
Teste: 2 imagens em batch paralelo
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("🧪 Teste: Criar 2 imagens GPT-4o em paralelo")
    print("=" * 60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ MCP Server inicializado\n")

            print("📸 Gerando 2 imagens em paralelo...")
            print("-" * 60)

            result = await session.call_tool(
                "generate_image",
                arguments={
                    "prompts": [
                        "A professional modern workspace",
                        "A beautiful mountain landscape"
                    ],
                    "size": "1:1",
                    "nVariants": 1,
                    "auto_download": True,
                    "wait_for_completion": True
                }
            )

            print(f"\n📦 Resposta recebida:")
            print(f"   Text length: {len(result.content[0].text)}")
            print(f"   Text preview: {result.content[0].text[:200]}...")

            try:
                response = json.loads(result.content[0].text)

                print(f"\n✅ Resultado parseado:")
                print(f"   Modo: {response.get('mode', 'N/A')}")
                print(f"   Total: {response.get('total', 0)}")
                print(f"   Sucesso: {response.get('successful', 0)}")
                print(f"   Falhas: {response.get('failed', 0)}")
                print(f"   Tempo: {response.get('total_time', 0)}s")
                print()

                for i, res in enumerate(response.get('results', []), 1):
                    print(f"Imagem {i}:")
                    print(f"  Status: {res.get('status')}")
                    if res.get('status') == 'success':
                        print(f"  URLs: {len(res.get('image_urls', []))}")
                        for url in res.get('image_urls', []):
                            print(f"    {url}")
                        if 'downloads' in res:
                            print(f"  📥 {res['downloads'][0]['filename']}")
                    print()

                print("=" * 60)
                print(f"✅ Teste concluído! {response.get('successful', 0)}/2 sucesso")

            except json.JSONDecodeError as e:
                print(f"\n❌ Erro ao parsear JSON: {e}")
                print(f"   Texto: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
