#!/usr/bin/env python3
"""
PROVA que está gerando em PARALELO (não em fila)
Compara tempo de 3 imagens juntas vs separadas
"""
import asyncio
import json
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_sequential():
    """Testa geração SEQUENCIAL (1 por vez)"""
    print("\n" + "="*60)
    print("📊 TESTE 1: Modo SEQUENCIAL (1 por vez)")
    print("="*60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    prompts = [
        "A cute fox",
        "A sleeping cat",
        "A happy dog"
    ]

    start_time = time.time()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for i, prompt in enumerate(prompts, 1):
                print(f"\n⏳ Gerando imagem {i}/3: {prompt}")
                result = await session.call_tool(
                    "generate_image",
                    arguments={"prompt": prompt}
                )

    elapsed = time.time() - start_time
    print(f"\n⏱️  TEMPO SEQUENCIAL: {elapsed:.1f}s")
    return elapsed


async def test_parallel():
    """Testa geração PARALELA (todas juntas)"""
    print("\n" + "="*60)
    print("⚡ TESTE 2: Modo PARALELO (todas juntas)")
    print("="*60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    prompts = [
        "A cute fox",
        "A sleeping cat",
        "A happy dog"
    ]

    start_time = time.time()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print(f"\n🚀 Gerando 3 imagens AO MESMO TEMPO...")
            result = await session.call_tool(
                "generate_image",
                arguments={"prompts": prompts}  # BATCH MODE
            )

            for content in result.content:
                if hasattr(content, 'text'):
                    data = json.loads(content.text)
                    print(f"✅ Sucesso: {data.get('successful')}/3")

    elapsed = time.time() - start_time
    print(f"\n⏱️  TEMPO PARALELO: {elapsed:.1f}s")
    return elapsed


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🧪 PROVA: Paralelo vs Sequencial")
    print("="*60)

    # Teste sequencial
    seq_time = await test_sequential()

    await asyncio.sleep(2)

    # Teste paralelo
    par_time = await test_parallel()

    # Comparação
    print("\n" + "="*60)
    print("📊 COMPARAÇÃO FINAL")
    print("="*60)
    print(f"\n⏱️  Sequencial (1 por vez): {seq_time:.1f}s")
    print(f"⚡ Paralelo (todas juntas): {par_time:.1f}s")

    if par_time < seq_time:
        speedup = seq_time / par_time
        saved = seq_time - par_time
        print(f"\n🎉 PARALELO É MAIS RÁPIDO!")
        print(f"   • Economia: {saved:.1f}s ({(saved/seq_time*100):.0f}%)")
        print(f"   • Aceleração: {speedup:.1f}x")
    else:
        print(f"\n⚠️  Tempos similares (overhead de rede)")

    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(main())
