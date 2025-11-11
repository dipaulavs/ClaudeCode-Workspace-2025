#!/usr/bin/env python3
"""
Cliente de teste para o MCP Server KIE.AI
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_generate_image():
    """Testa a geração de imagem"""
    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializa a sessão
            await session.initialize()

            # Lista as ferramentas disponíveis
            tools_result = await session.list_tools()
            tools = tools_result.tools
            print("\n=== Ferramentas Disponíveis ===")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")

            # Testa geração de imagem
            print("\n=== Testando Geração de Imagem ===")
            print("Prompt: 'A beautiful sunset over the ocean with palm trees'")

            result = await session.call_tool(
                "generate_image",
                arguments={
                    "prompt": "A beautiful sunset over the ocean with palm trees",
                    "output_format": "png",
                    "image_size": "16:9",
                    "wait_for_completion": True
                }
            )

            print("\n=== Resultado ===")
            for content in result.content:
                if hasattr(content, 'text'):
                    data = json.loads(content.text)
                    print(json.dumps(data, indent=2))

                    if data.get("status") == "success":
                        print(f"\n✅ Imagem gerada com sucesso!")
                        print(f"URLs: {data.get('image_urls')}")
                    else:
                        print(f"\n❌ Erro na geração")


async def test_check_status():
    """Testa a verificação de status (exemplo)"""
    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Primeiro cria uma task sem aguardar
            print("\n=== Criando Task sem Aguardar ===")
            result = await session.call_tool(
                "generate_image",
                arguments={
                    "prompt": "A cute cat playing with a ball of yarn",
                    "wait_for_completion": False
                }
            )

            task_id = None
            for content in result.content:
                if hasattr(content, 'text'):
                    data = json.loads(content.text)
                    print(json.dumps(data, indent=2))
                    task_id = data.get("task_id")

            if task_id:
                # Aguarda um pouco
                await asyncio.sleep(10)

                # Verifica o status
                print(f"\n=== Verificando Status da Task {task_id} ===")
                status_result = await session.call_tool(
                    "check_task_status",
                    arguments={"task_id": task_id}
                )

                for content in status_result.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        print(json.dumps(data, indent=2))


async def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DO MCP SERVER KIE.AI - GERAÇÃO DE IMAGENS")
    print("=" * 60)

    try:
        # Teste 1: Geração completa
        await test_generate_image()

        # Teste 2: Verificação de status (opcional)
        # await test_check_status()

        print("\n" + "=" * 60)
        print("✅ Todos os testes concluídos!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
