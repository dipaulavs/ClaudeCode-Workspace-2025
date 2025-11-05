#!/usr/bin/env python3
"""
Teste: Geração em lote PARALELA (2-3 imagens simultâneas)
"""
import asyncio
import json
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("⚡ TESTE: Geração em Lote PARALELA")
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

                # Teste: 3 imagens em paralelo
                prompts = [
                    "A cute fox sitting on a table",
                    "A cat sleeping on a pillow",
                    "A dog playing in a garden"
                ]

                print("\n" + "="*60)
                print("🚀 Gerando 3 imagens EM PARALELO")
                print("="*60)
                for i, p in enumerate(prompts, 1):
                    print(f"   {i}. {p}")

                print("\n⏱️  Cronômetro iniciado...")
                start_time = time.time()

                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompts": prompts,  # 🔥 BATCH MODE
                        "auto_download": True
                    }
                )

                elapsed_time = time.time() - start_time

                print("\n" + "="*60)
                print("📊 RESULTADO")
                print("="*60)

                for content in result.content:
                    if hasattr(content, 'text'):
                        print(f"\n🔍 Debug - Conteúdo bruto:")
                        print(f"   Tipo: {type(content.text)}")
                        print(f"   Tamanho: {len(content.text)}")
                        print(f"   Primeiros 200 chars: {content.text[:200]}")
                        print()

                        if not content.text:
                            print("❌ Resposta vazia!")
                            continue

                        data = json.loads(content.text)

                        if data.get("mode") == "batch_parallel":
                            print(f"\n✅ Modo: Batch Paralelo")
                            print(f"📊 Total: {data.get('total')}")
                            print(f"✅ Sucesso: {data.get('successful')}")
                            print(f"❌ Falhas: {data.get('failed')}")
                            print(f"⏱️  Tempo de geração (API): {data.get('total_time')}s")
                            print(f"⏱️  Tempo total (incluindo rede): {elapsed_time:.1f}s")

                            # Comparação com geração sequencial
                            avg_time = data.get('total_time', 0) / data.get('successful', 1)
                            sequential_time = avg_time * data.get('total', 1)
                            speedup = sequential_time / elapsed_time if elapsed_time > 0 else 0

                            print(f"\n💡 Análise:")
                            print(f"   • Tempo médio por imagem: {avg_time:.1f}s")
                            print(f"   • Estimativa sequencial: {sequential_time:.1f}s")
                            print(f"   • Aceleração: {speedup:.1f}x mais rápido")

                            # Detalhes de cada imagem
                            print(f"\n📸 Imagens geradas:")
                            for i, r in enumerate(data.get('results', []), 1):
                                if r.get('status') == 'success':
                                    print(f"\n   {i}. ✅ {r.get('prompt', '')[:40]}...")
                                    print(f"      • Tempo: {r.get('cost_time')}s")

                                    if 'downloads' in r:
                                        for dl in r['downloads']:
                                            print(f"      • Arquivo: {dl['filename']}")
                                else:
                                    print(f"\n   {i}. ❌ {r.get('prompt', '')[:40]}...")
                                    print(f"      • Erro")

                            print("\n" + "="*60)
                            print("🎉 TESTE CONCLUÍDO!")
                            print("="*60)
                            print(f"\n✨ Comparação:")
                            print(f"   Sequencial (1 por vez): ~{sequential_time:.0f}s")
                            print(f"   Paralelo (todas juntas): {elapsed_time:.0f}s")
                            print(f"   Ganho: {speedup:.1f}x mais rápido! ⚡")
                            print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
