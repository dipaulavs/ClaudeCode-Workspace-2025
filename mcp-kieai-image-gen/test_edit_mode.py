#!/usr/bin/env python3
"""
Teste: Modo EDIÇÃO de imagens
Primeiro cria uma imagem, depois edita
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("✏️  TESTE: Modo EDIÇÃO")
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

                # PASSO 1: Cria uma imagem base
                print("\n" + "="*60)
                print("🎨 PASSO 1: Criar imagem base")
                print("="*60)
                print("📝 Prompt: A person wearing a blue shirt")

                result1 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A person wearing a blue shirt",
                        "image_size": "1:1"
                        # Sem auto_download, só queremos a URL
                    }
                )

                image_url = None
                for content in result1.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("status") == "success":
                            image_url = data.get("image_urls", [])[0]
                            print(f"\n✅ Imagem criada!")
                            print(f"🔗 URL: {image_url}")

                if not image_url:
                    print("❌ Falha ao criar imagem base")
                    return

                # PASSO 2: Edita a imagem (muda cor da camisa)
                print("\n" + "="*60)
                print("✏️  PASSO 2: EDITAR imagem (mudar cor)")
                print("="*60)
                print("📝 Edição: Change the shirt color to red")
                print(f"🖼️  Imagem base: {image_url[:60]}...")

                result2 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "Change the shirt color to red",
                        "image_url": image_url,  # 🔥 MODO EDIÇÃO
                        "auto_download": True
                    }
                )

                for content in result2.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("status") == "success":
                            print(f"\n✅ Imagem editada com sucesso!")
                            print(f"⏱️  Tempo: {data.get('cost_time')}s")

                            if "downloads" in data:
                                print(f"\n📂 Arquivo salvo:")
                                for dl in data["downloads"]:
                                    print(f"   • {dl['filename']}")
                                    print(f"     {dl['path']}")

                            print(f"\n🔗 URLs:")
                            print(f"   ANTES: {image_url}")
                            print(f"   DEPOIS: {data.get('image_urls', [])[0]}")

                            print("\n" + "="*60)
                            print("🎉 EDIÇÃO CONCLUÍDA!")
                            print("="*60)
                            print("\n✨ O que foi feito:")
                            print("   1. Criou imagem com camisa azul")
                            print("   2. Editou para camisa vermelha")
                            print("   3. Salvou em ~/Downloads")
                            print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
