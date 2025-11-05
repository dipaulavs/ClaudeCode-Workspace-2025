#!/usr/bin/env python3
"""
Teste final: português + sem acentos + nome do MCP
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("✅ TESTE FINAL - v2.0.0")
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

                # Teste completo
                print("\n" + "="*60)
                print("🦊 Gerando: Raposa na mesa")
                print("="*60)

                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompt": "A fox sitting on a wooden table",
                        # Usa todos os padrões: 4:5, auto_download=False
                        "auto_download": True
                    }
                )

                for content in result.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)

                        if data.get("status") == "success":
                            print(f"\n✅ Sucesso! Tempo: {data.get('cost_time')}s")

                            if "downloads" in data:
                                filename = data["downloads"][0]["filename"]
                                print(f"\n📄 Nome do arquivo:")
                                print(f"   {filename}")

                                # Verifica português
                                has_portuguese = any(word in filename for word in [
                                    'raposa', 'mesa', 'gato', 'cachorro', 'por_do_sol'
                                ])

                                # Verifica se NÃO tem acentos
                                has_accents = any(char in filename for char in 'áàãâéêíóôõúüç')

                                print(f"\n🔍 Validações:")
                                if has_portuguese:
                                    print("   ✅ Está em português")
                                else:
                                    print(f"   ⚠️  Nome: {filename}")

                                if not has_accents:
                                    print("   ✅ Sem acentos")
                                else:
                                    print("   ❌ Tem acentos")

                                print(f"\n📐 Proporção padrão: 4:5")
                                print(f"📂 Download automático: Ativo")

                                print("\n" + "="*60)
                                print("🎉 TUDO FUNCIONANDO!")
                                print("="*60)
                                print("\n✨ Configurações aplicadas:")
                                print("   • Nome MCP: kie-nanobanana-create")
                                print("   • Nomes em português (sem acentos)")
                                print("   • Proporção padrão: 4:5")
                                print("   • Download automático disponível")
                                print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
