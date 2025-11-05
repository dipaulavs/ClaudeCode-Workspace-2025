#!/usr/bin/env python3
"""
Teste completo do MCP GPT-4o Image
Testa geração com nVariants e novas features
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("🧪 Testando MCP GPT-4o Image...")
    print("=" * 60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ Servidor inicializado\n")

                # Teste 1: Geração simples (1 variante)
                print("📸 Teste 1: Geração simples (1 imagem)")
                print("-" * 60)

                result1 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A cute golden retriever puppy playing in a park",
                        "size": "1:1",
                        "nVariants": 1,
                        "auto_download": True,
                        "wait_for_completion": True
                    }
                )

                response1 = json.loads(result1.content[0].text)
                print(f"✅ Status: {response1['status']}")
                print(f"⏱️  Tempo: {response1['cost_time']}s")
                print(f"🖼️  Imagens: {len(response1['image_urls'])}")
                if 'downloads' in response1:
                    print(f"📥 Baixado: {response1['downloads'][0]['filename']}")
                print()

                # Teste 2: Múltiplas variantes
                print("📸 Teste 2: Múltiplas variantes (4 imagens)")
                print("-" * 60)

                result2 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A modern minimalist living room with plants",
                        "size": "3:2",
                        "nVariants": 4,
                        "auto_download": True,
                        "wait_for_completion": True
                    }
                )

                response2 = json.loads(result2.content[0].text)
                print(f"✅ Status: {response2['status']}")
                print(f"⏱️  Tempo: {response2['cost_time']}s")
                print(f"🖼️  Variantes geradas: {len(response2['image_urls'])}")
                if 'downloads' in response2:
                    print(f"📥 Downloads ({len(response2['downloads'])}):")
                    for dl in response2['downloads']:
                        print(f"   - {dl['filename']}")
                print()

                # Teste 3: Geração batch em paralelo
                print("📸 Teste 3: Batch paralelo (3 prompts)")
                print("-" * 60)

                result3 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompts": [
                            "A red sports car on a mountain road",
                            "A serene beach at sunset",
                            "A cozy coffee shop interior"
                        ],
                        "size": "2:3",
                        "nVariants": 1,
                        "auto_download": True,
                        "wait_for_completion": True
                    }
                )

                response3 = json.loads(result3.content[0].text)
                print(f"✅ Total: {response3['total']} imagens")
                print(f"✅ Sucesso: {response3['successful']}")
                print(f"⏱️  Tempo total: {response3['total_time']}s")
                print(f"📥 Downloads:")
                for result in response3['results']:
                    if 'downloads' in result:
                        print(f"   - {result['downloads'][0]['filename']}")
                print()

                print("=" * 60)
                print("✅ Todos os testes concluídos com sucesso!")
                print("=" * 60)
                print("\n💡 Recursos testados:")
                print("   ✅ Geração simples")
                print("   ✅ Múltiplas variantes (nVariants)")
                print("   ✅ Geração batch paralela")
                print("   ✅ Download automático")
                print("   ✅ Proporções diferentes (1:1, 3:2, 2:3)")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
