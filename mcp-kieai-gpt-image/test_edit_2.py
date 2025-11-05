#!/usr/bin/env python3
"""
Teste: Editar 2 imagens em batch paralelo
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("🧪 Teste: Editar 2 imagens GPT-4o em paralelo")
    print("=" * 60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ MCP Server inicializado\n")

            # Primeiro cria 2 imagens base
            print("📸 Criando 2 imagens base...")
            print("-" * 60)

            base_images = []

            for i, prompt in enumerate(["A simple red car", "A simple blue house"], 1):
                print(f"\n{i}. Criando: {prompt}")
                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": prompt,
                        "size": "1:1",
                        "nVariants": 1,
                        "wait_for_completion": True
                    }
                )

                response = json.loads(result.content[0].text)
                if response.get("status") == "success" and response.get("image_urls"):
                    url = response["image_urls"][0]
                    print(f"   ✅ {url}")
                    base_images.append(url)
                else:
                    print(f"   ❌ Falhou")

            if len(base_images) < 2:
                print(f"\n❌ Não foi possível criar as 2 imagens base. Criadas: {len(base_images)}")
                return

            print(f"\n\n✏️ Editando as 2 imagens em paralelo...")
            print("=" * 60)

            result = await session.call_tool(
                "generate_image",
                arguments={
                    "prompts": [
                        "Make it yellow",
                        "Make it green"
                    ],
                    "files_url": base_images,
                    "size": "1:1",
                    "nVariants": 1,
                    "auto_download": True,
                    "wait_for_completion": True
                }
            )

            response = json.loads(result.content[0].text)

            print(f"\n✅ Resultado da edição:")
            print(f"   Modo: {response.get('mode', 'N/A')}")
            print(f"   Total: {response.get('total', 0)}")
            print(f"   Sucesso: {response.get('successful', 0)}")
            print(f"   Falhas: {response.get('failed', 0)}")
            print()

            for i, res in enumerate(response.get('results', []), 1):
                print(f"Imagem {i}:")
                if res.get('status') == 'success':
                    print(f"  ✅ Sucesso!")
                    for url in res.get('image_urls', []):
                        print(f"     {url}")
                    if 'downloads' in res:
                        print(f"  📥 {res['downloads'][0]['filename']}")
                else:
                    print(f"  ❌ Falhou")
                print()

            print("=" * 60)
            print(f"🎉 Teste concluído! {response.get('successful', 0)}/2 editadas")


if __name__ == "__main__":
    asyncio.run(main())
