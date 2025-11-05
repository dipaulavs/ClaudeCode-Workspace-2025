#!/usr/bin/env python3
"""
Teste de geração em lote - 3 imagens
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROMPTS = [
    {
        "prompt": "A cute robot playing with colorful blocks, digital art, vibrant colors",
        "image_size": "1:1",
        "name": "Robô Fofo"
    },
    {
        "prompt": "A beautiful sunset over the ocean with palm trees, photorealistic",
        "image_size": "16:9",
        "name": "Pôr do Sol"
    },
    {
        "prompt": "A futuristic city with flying cars, neon lights, cyberpunk style",
        "image_size": "16:9",
        "name": "Cidade Futurista"
    }
]


async def generate_single_image(session, prompt_data, index):
    """Gera uma única imagem"""
    print(f"\n{'='*60}")
    print(f"🎨 Imagem {index+1}/3: {prompt_data['name']}")
    print(f"📝 Prompt: {prompt_data['prompt']}")
    print(f"{'='*60}")

    result = await session.call_tool(
        "generate_image",
        arguments={
            "prompt": prompt_data["prompt"],
            "output_format": "png",
            "image_size": prompt_data["image_size"],
            "wait_for_completion": True
        }
    )

    for content in result.content:
        if hasattr(content, 'text'):
            data = json.loads(content.text)

            if data.get("status") == "success":
                print(f"\n✅ SUCESSO!")
                print(f"   📎 URL: {data.get('image_urls', [])[0]}")
                print(f"   ⏱️  Tempo: {data.get('cost_time')}s")
                print(f"   💰 Créditos: {data.get('consume_credits')}")
                return {
                    "success": True,
                    "name": prompt_data['name'],
                    "url": data.get('image_urls', [])[0] if data.get('image_urls') else None,
                    "cost_time": data.get('cost_time')
                }
            else:
                print(f"\n❌ ERRO!")
                print(f"   {json.dumps(data, indent=2)}")
                return {
                    "success": False,
                    "name": prompt_data['name'],
                    "error": data
                }


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🧪 TESTE EM LOTE - GERANDO 3 IMAGENS")
    print("="*60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializa
                await session.initialize()
                print("\n✅ Servidor inicializado!")

                # Gera as 3 imagens sequencialmente
                results = []
                for i, prompt_data in enumerate(PROMPTS):
                    result = await generate_single_image(session, prompt_data, i)
                    results.append(result)

                # Resumo final
                print("\n" + "="*60)
                print("📊 RESUMO FINAL")
                print("="*60)

                successful = [r for r in results if r.get('success')]
                failed = [r for r in results if not r.get('success')]

                print(f"\n✅ Sucesso: {len(successful)}/3")
                print(f"❌ Falhas: {len(failed)}/3")

                if successful:
                    print("\n📸 Imagens geradas:")
                    for r in successful:
                        print(f"   • {r['name']}: {r['url']}")

                total_time = sum(r.get('cost_time', 0) for r in successful)
                print(f"\n⏱️  Tempo total: {total_time}s")

                print("\n" + "="*60)
                print("✅ TESTE CONCLUÍDO!")
                print("="*60)

    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
