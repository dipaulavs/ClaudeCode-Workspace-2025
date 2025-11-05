#!/usr/bin/env python3
"""
Teste: Nomes de arquivos em português
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🇧🇷 TESTE: Nomes em Português")
    print("="*60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    tests = [
        {
            "prompt": "A fox sitting on top of a wooden table",
            "esperado": "raposa (fox traduzido)"
        },
        {
            "prompt": "A cat sleeping on a pillow",
            "esperado": "gato (cat traduzido)"
        },
        {
            "prompt": "A beautiful sunset over the ocean",
            "esperado": "por_do_sol_oceano"
        }
    ]

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("\n✅ Servidor inicializado!")

                for i, test in enumerate(tests, 1):
                    print("\n" + "="*60)
                    print(f"🎨 Teste {i}/{len(tests)}")
                    print("="*60)
                    print(f"📝 Prompt: {test['prompt']}")
                    print(f"🎯 Esperado: {test['esperado']}")

                    result = await session.call_tool(
                        "generate_image",
                        arguments={
                            "prompt": test["prompt"],
                            "auto_download": True
                        }
                    )

                    for content in result.content:
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            if data.get("status") == "success":
                                print(f"\n⏱️  Tempo: {data.get('cost_time')}s")

                                if "downloads" in data:
                                    filename = data["downloads"][0]["filename"]
                                    print(f"\n📄 Nome gerado:")
                                    print(f"   {filename}")

                                    # Verifica se está em português
                                    if any(palavra in filename for palavra in ['raposa', 'gato', 'por_do_sol', 'oceano', 'mesa', 'dormindo']):
                                        print("   ✅ Em português!")
                                    else:
                                        print(f"   ⚠️  Pode não estar em português")

                print("\n" + "="*60)
                print("📊 RESUMO")
                print("="*60)
                print("\n✅ Todos os testes concluídos!")
                print("🔍 Verifique os nomes dos arquivos em ~/Downloads/")
                print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
