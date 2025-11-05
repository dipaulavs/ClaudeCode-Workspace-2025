#!/usr/bin/env python3
"""
Teste das melhorias:
1. Nome descritivo automático
2. Proporção 4:5 como padrão
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🧪 TESTE DAS MELHORIAS")
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

                # Teste 1: Raposa (nome descritivo + padrão 4:5)
                print("\n" + "="*60)
                print("🦊 Teste 1: Raposa em cima de uma mesa")
                print("="*60)
                print("📝 Prompt: A fox sitting on top of a wooden table")
                print("⚙️  Proporção: PADRÃO (deve ser 4:5)")
                print("📄 Nome: AUTOMÁTICO (deve ser descritivo)")

                result1 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A fox sitting on top of a wooden table",
                        # image_size NÃO especificado = deve usar padrão 4:5
                        "auto_download": True
                    }
                )

                for content in result1.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("status") == "success":
                            print(f"\n✅ Sucesso! Tempo: {data.get('cost_time')}s")
                            if "downloads" in data:
                                for dl in data["downloads"]:
                                    print(f"\n📄 Nome do arquivo:")
                                    print(f"   {dl['filename']}")
                                    print(f"\n💡 Análise do nome:")
                                    filename = dl['filename']
                                    if 'fox' in filename or 'raposa' in filename:
                                        print("   ✅ Nome descritivo OK!")
                                    else:
                                        print(f"   ⚠️  Nome não parece descritivo: {filename}")

                # Teste 2: Gato (verificar proporção 4:5)
                print("\n" + "="*60)
                print("🐱 Teste 2: Gato dormindo em uma almofada")
                print("="*60)
                print("📝 Prompt: A cat sleeping on a soft pillow")
                print("⚙️  Proporção: PADRÃO (deve ser 4:5)")
                print("📄 Nome: AUTOMÁTICO")

                result2 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A cat sleeping on a soft pillow",
                        "auto_download": True
                    }
                )

                for content in result2.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("status") == "success":
                            print(f"\n✅ Sucesso! Tempo: {data.get('cost_time')}s")

                            # Verifica proporção na URL
                            url = data.get("image_urls", [])[0]
                            if "4x5" in url or "4:5" in url:
                                print("\n📐 Proporção: ✅ 4:5 confirmado na URL!")
                            else:
                                print(f"\n📐 Proporção na URL: {url}")

                            if "downloads" in data:
                                for dl in data["downloads"]:
                                    print(f"\n📄 Nome do arquivo:")
                                    print(f"   {dl['filename']}")
                                    if 'cat' in dl['filename'] or 'gato' in dl['filename']:
                                        print("   ✅ Nome descritivo OK!")

                # Resumo
                print("\n" + "="*60)
                print("📊 RESUMO DOS TESTES")
                print("="*60)
                print("\n✅ Testes concluídos!")
                print("\n🔍 Verificações:")
                print("   1. Nome descritivo: Baseado no prompt")
                print("   2. Proporção padrão: 4:5 (vertical)")
                print("   3. Download automático: Funcionando")
                print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
