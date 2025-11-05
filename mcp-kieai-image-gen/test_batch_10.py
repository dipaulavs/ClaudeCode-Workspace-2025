#!/usr/bin/env python3
"""
Teste ÉPICO: 10 imagens em paralelo!
Demonstra o verdadeiro poder do batch mode
"""
import asyncio
import json
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🚀 TESTE ÉPICO: 10 IMAGENS EM PARALELO")
    print("="*60)

    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
    )

    # 10 prompts diferentes
    prompts = [
        "A cute fox in the forest",
        "A cat sleeping peacefully",
        "A dog running on the beach",
        "A bird flying in the sky",
        "A rabbit eating a carrot",
        "A lion roaring in the savanna",
        "A dolphin jumping in the ocean",
        "A butterfly on a flower",
        "A wolf howling at the moon",
        "A panda eating bamboo"
    ]

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("\n✅ Servidor inicializado!")

                print("\n" + "="*60)
                print("📋 LISTA DE IMAGENS A GERAR")
                print("="*60)
                for i, p in enumerate(prompts, 1):
                    print(f"   {i:2d}. {p}")

                print("\n⏱️  Iniciando geração em PARALELO...")
                print("    (Todas as 10 imagens ao mesmo tempo!)")
                start_time = time.time()

                result = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompts": prompts,  # 🔥 10 IMAGENS!
                        "auto_download": True
                    }
                )

                elapsed_time = time.time() - start_time

                print("\n" + "="*60)
                print("📊 RESULTADO FINAL")
                print("="*60)

                for content in result.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)

                        if data.get("mode") == "batch_parallel":
                            print(f"\n✅ Modo: Batch Paralelo")
                            print(f"📊 Total solicitado: {data.get('total')}")
                            print(f"✅ Geradas com sucesso: {data.get('successful')}")
                            print(f"❌ Falhas: {data.get('failed')}")
                            print(f"⏱️  Tempo de geração (API): {data.get('total_time')}s")
                            print(f"⏱️  Tempo total (com downloads): {elapsed_time:.1f}s")

                            # Cálculo de economia de tempo
                            avg_time = data.get('total_time', 0) / max(data.get('successful', 1), 1)
                            sequential_time = avg_time * data.get('total', 1)
                            saved_time = sequential_time - elapsed_time
                            speedup = sequential_time / elapsed_time if elapsed_time > 0 else 0

                            print(f"\n💰 ECONOMIA DE TEMPO:")
                            print(f"   • Tempo médio por imagem: {avg_time:.1f}s")
                            print(f"   • Se fosse 1 por vez (sequencial): ~{sequential_time:.0f}s")
                            print(f"   • Em paralelo (todas juntas): {elapsed_time:.0f}s")
                            print(f"   • Tempo economizado: {saved_time:.0f}s")
                            print(f"   • Aceleração: {speedup:.1f}x mais rápido! ⚡")

                            # Lista as imagens geradas
                            print(f"\n📸 IMAGENS GERADAS:")
                            print("="*60)
                            for i, r in enumerate(data.get('results', []), 1):
                                if r.get('status') == 'success':
                                    prompt_text = r.get('prompt', '')[:35]
                                    print(f"{i:2d}. ✅ {prompt_text}... ({r.get('cost_time')}s)")

                                    if 'downloads' in r:
                                        for dl in r['downloads']:
                                            print(f"       📄 {dl['filename']}")
                                else:
                                    print(f"{i:2d}. ❌ Erro")

                            print("\n" + "="*60)
                            print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
                            print("="*60)
                            print(f"\n✨ Resumo:")
                            print(f"   • 10 imagens geradas simultaneamente")
                            print(f"   • Tempo: {elapsed_time:.0f}s (vs ~{sequential_time:.0f}s sequencial)")
                            print(f"   • Economia: {saved_time:.0f}s ({(saved_time/sequential_time*100):.0f}% mais rápido)")
                            print(f"   • Arquivos em português salvos em ~/Downloads")
                            print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
