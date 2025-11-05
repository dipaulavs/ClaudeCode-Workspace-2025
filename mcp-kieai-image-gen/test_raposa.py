#!/usr/bin/env python3
"""
Teste: Raposa em cima de uma mesa
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🦊 GERANDO: Raposa em cima de uma mesa")
    print("="*60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("\n✅ Servidor inicializado!")

                print("\n🎨 Gerando imagem...")
                print("📝 Prompt: A cute fox sitting on top of a wooden table")
                print("⚙️  Configuração:")
                print("   • Formato: PNG")
                print("   • Proporção: 16:9 (paisagem)")
                print("   • Download automático: SIM")

                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A cute fox sitting on top of a wooden table, photorealistic, natural lighting",
                        "output_format": "png",
                        "image_size": "16:9",
                        "wait_for_completion": True,
                        "auto_download": True
                    }
                )

                print("\n" + "="*60)
                print("📥 RESULTADO")
                print("="*60)

                for content in result.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)

                        if data.get("status") == "success":
                            print(f"\n✅ SUCESSO!")
                            print(f"\n⏱️  Tempo de geração: {data.get('cost_time')}s")

                            print(f"\n🔗 URL da imagem:")
                            for url in data.get("image_urls", []):
                                print(f"   {url}")

                            if "downloads" in data:
                                print(f"\n📂 Imagem salva em:")
                                print(f"   {data['downloads_path']}")
                                print(f"\n📄 Arquivo:")
                                for dl in data["downloads"]:
                                    print(f"   • {dl['filename']}")
                                    print(f"     {dl['path']}")

                            print("\n" + "="*60)
                            print("🎉 Imagem gerada e salva com sucesso!")
                            print("="*60)
                        else:
                            print(f"\n❌ Erro:")
                            print(json.dumps(data, indent=2))

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
