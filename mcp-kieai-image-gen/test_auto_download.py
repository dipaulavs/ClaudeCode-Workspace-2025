#!/usr/bin/env python3
"""
Teste de geração com download automático
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🧪 TESTE COM DOWNLOAD AUTOMÁTICO")
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

                # Gera imagem com download automático
                print("\n" + "="*60)
                print("🎨 Gerando imagem com download automático")
                print("📝 Prompt: A cute robot with big eyes")
                print("="*60)

                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A cute robot with big eyes, digital art",
                        "output_format": "png",
                        "image_size": "1:1",
                        "wait_for_completion": True,
                        "auto_download": True  # 🔥 DOWNLOAD AUTOMÁTICO
                    }
                )

                print("\n📥 Resultado:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        print(json.dumps(data, indent=2))

                        if data.get("status") == "success":
                            print(f"\n✅ SUCESSO!")

                            if "downloads" in data:
                                print(f"\n📂 Imagens baixadas em: {data['downloads_path']}")
                                for dl in data["downloads"]:
                                    print(f"   • {dl['filename']}")
                                    print(f"     {dl['path']}")
                            else:
                                print("\n⚠️ Download automático não foi executado")

                print("\n" + "="*60)
                print("✅ TESTE CONCLUÍDO!")
                print("="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
