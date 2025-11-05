#!/usr/bin/env python3
"""
Exemplo de Uso: Cliente MCP Image Generation

Demonstra como integrar o cliente MCP em um chatbot ou aplicação.
"""

import asyncio
from pathlib import Path
from test_mcp_client import conectar_mcp


async def exemplo_basico():
    """Exemplo básico de uso do cliente MCP"""
    print("=" * 60)
    print("EXEMPLO 1: Uso Básico do Cliente MCP")
    print("=" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    # Usar context manager para gerenciar conexão automaticamente
    async with conectar_mcp(str(server_path)) as cliente:
        # Listar ferramentas disponíveis
        ferramentas = await cliente.listar_ferramentas()
        print(f"\nFerramentas disponíveis: {ferramentas}\n")

        # Gerar imagem simples
        resultado = await cliente.chamar_ferramenta(
            "generate_image",
            {
                "prompt": "um gato programando em Python",
                "api": "nanobanana",
                "quality": "high"
            }
        )

        print(f"Imagem gerada:")
        print(f"  URL: {resultado.get('image_url')}")
        print(f"  Status: {resultado.get('status')}")
        print(f"  Mensagem: {resultado.get('message')}\n")


async def exemplo_multiplas_geracao():
    """Exemplo de geração em lote"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Geração em Lote")
    print("=" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        prompts = [
            "cachorro jogando frisbee na praia",
            "astronauta em um planeta alienígena",
            "castelo medieval à noite com lua cheia"
        ]

        resultado = await cliente.chamar_ferramenta(
            "batch_generate",
            {
                "prompts": prompts,
                "api": "nanobanana"
            }
        )

        print(f"\nGeradas {resultado.get('prompts_count')} imagens:")
        for i, url in enumerate(resultado.get('generated_urls', []), 1):
            print(f"  {i}. {url}")


async def exemplo_edicao():
    """Exemplo de edição de imagem"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Edição de Imagem")
    print("=" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        resultado = await cliente.chamar_ferramenta(
            "edit_image",
            {
                "image_url": "https://example.com/imagem.jpg",
                "operation": "resize",
                "parameters": {
                    "width": 1024,
                    "height": 768,
                    "maintain_aspect": True
                }
            }
        )

        print(f"\nImagem editada:")
        print(f"  Operação: {resultado.get('operation')}")
        print(f"  Parâmetros: {resultado.get('parameters')}")
        print(f"  URL resultado: {resultado.get('edited_url')}\n")


async def exemplo_tratamento_erro():
    """Exemplo de tratamento de erro"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Tratamento de Erro")
    print("=" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        try:
            # Tentar chamar ferramenta que não existe
            resultado = await cliente.chamar_ferramenta(
                "super_generate_magica",
                {"prompt": "algo"}
            )
        except RuntimeError as e:
            print(f"\nErro capturado (esperado):")
            print(f"  {e}\n")


async def exemplo_multiplas_operacoes():
    """Exemplo com múltiplas operações sequenciais"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Múltiplas Operações Sequenciais")
    print("=" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        # 1. Gerar imagem
        print("\n1. Gerando imagem...")
        gen_resultado = await cliente.chamar_ferramenta(
            "generate_image",
            {
                "prompt": "paisagem montanhosa",
                "api": "gpt4o",
                "quality": "high"
            }
        )
        image_url = gen_resultado.get("image_url")
        print(f"   ✅ Imagem gerada: {image_url}")

        # 2. Editar imagem
        print("\n2. Editando imagem...")
        edit_resultado = await cliente.chamar_ferramenta(
            "edit_image",
            {
                "image_url": image_url,
                "operation": "enhance",
                "parameters": {
                    "contrast": 1.2,
                    "saturation": 1.1
                }
            }
        )
        edited_url = edit_resultado.get("edited_url")
        print(f"   ✅ Imagem editada: {edited_url}")

        # 3. Summarize
        print("\n3. Resumo do fluxo:")
        print(f"   - Original: {image_url}")
        print(f"   - Editada: {edited_url}")
        print(f"   - Status: {edit_resultado.get('status')}\n")


async def main():
    """Executa todos os exemplos"""
    try:
        await exemplo_basico()
        await exemplo_multiplas_geracao()
        await exemplo_edicao()
        await exemplo_tratamento_erro()
        await exemplo_multiplas_operacoes()

        print("\n" + "=" * 60)
        print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
