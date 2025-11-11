#!/usr/bin/env python3
"""
Teste: 2 imagens criadas individualmente (não batch)
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("🧪 Teste: Criar 2 imagens GPT-4o individualmente")
    print("=" * 60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ MCP Server inicializado\n")

            prompts = [
                "A cute golden retriever puppy",
                "A beautiful red rose flower"
            ]

            for i, prompt in enumerate(prompts, 1):
                print(f"\n{i}. Gerando: {prompt}")
                print("-" * 60)

                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": prompt,
                        "size": "1:1",
                        "nVariants": 1,
                        "auto_download": True,
                        "wait_for_completion": True
                    }
                )

                response = json.loads(result.content[0].text)

                if response.get("status") == "success":
                    print(f"   ✅ Sucesso!")
                    print(f"   URLs: {len(response['image_urls'])}")
                    for url in response['image_urls']:
                        print(f"      {url}")
                    if 'downloads' in response:
                        print(f"   📥 {response['downloads'][0]['filename']}")
                else:
                    print(f"   ❌ Falhou: {response}")

            print("\n" + "=" * 60)
            print("✅ Teste concluído!")


if __name__ == "__main__":
    asyncio.run(main())
