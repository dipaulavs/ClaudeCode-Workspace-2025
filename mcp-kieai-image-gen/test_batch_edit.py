#!/usr/bin/env python3
"""
Teste ÉPICO: Edição em lote paralela
Cria 3 imagens e edita as 3 AO MESMO TEMPO
"""
import asyncio
import json
import time
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Função principal"""
    print("\n" + "="*60)
    print("✏️  TESTE ÉPICO: Edição em Lote Paralela")
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

                # PASSO 1: Cria 3 imagens base em paralelo
                print("\n" + "="*60)
                print("🎨 PASSO 1: Criar 3 imagens base (PARALELO)")
                print("="*60)

                base_prompts = [
                    "A person wearing a blue shirt",
                    "A car painted in green",
                    "A house with yellow walls"
                ]

                for i, p in enumerate(base_prompts, 1):
                    print(f"   {i}. {p}")

                result1 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompts": base_prompts,
                        "image_size": "1:1"
                    }
                )

                image_urls = []
                for content in result1.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        if data.get("mode") == "batch_parallel":
                            print(f"\n✅ {data.get('successful')}/3 imagens criadas!")

                            for r in data.get('results', []):
                                if r.get('status') == 'success':
                                    url = r.get('image_urls', [])[0]
                                    image_urls.append(url)
                                    print(f"   • {url[:60]}...")

                if len(image_urls) != 3:
                    print("❌ Erro ao criar imagens base")
                    return

                # PASSO 2: Edita as 3 imagens em paralelo
                print("\n" + "="*60)
                print("✏️  PASSO 2: EDITAR 3 imagens (PARALELO)")
                print("="*60)

                edit_prompts = [
                    "Change the shirt color to red",
                    "Paint the car in blue",
                    "Change the house walls to pink"
                ]

                for i, (edit_p, img_url) in enumerate(zip(edit_prompts, image_urls), 1):
                    print(f"   {i}. {edit_p}")
                    print(f"      Imagem: ...{img_url[-30:]}")

                print("\n⏱️  Iniciando edição em PARALELO...")
                start_time = time.time()

                result2 = await session.call_tool(
                    "generate_image",
                    arguments={
                        "prompts": edit_prompts,
                        "image_urls": image_urls,  # 🔥 BATCH EDIT MODE
                        "auto_download": True
                    }
                )

                elapsed = time.time() - start_time

                print("\n" + "="*60)
                print("📊 RESULTADO")
                print("="*60)

                for content in result2.content:
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)

                        if data.get("mode") == "batch_parallel":
                            print(f"\n✅ Modo: Batch Paralelo (EDIÇÃO)")
                            print(f"📊 Total: {data.get('total')}")
                            print(f"✅ Editadas: {data.get('successful')}")
                            print(f"❌ Falhas: {data.get('failed')}")
                            print(f"⏱️  Tempo de edição: {elapsed:.1f}s")

                            print(f"\n📸 Imagens editadas:")
                            for i, r in enumerate(data.get('results', []), 1):
                                if r.get('status') == 'success':
                                    print(f"\n   {i}. ✅ {r.get('prompt', '')}")
                                    print(f"      Tempo: {r.get('cost_time')}s")
                                    print(f"      Mode: {r.get('mode', 'N/A')}")

                                    if 'downloads' in r:
                                        for dl in r['downloads']:
                                            print(f"      Arquivo: {dl['filename']}")

                            print("\n" + "="*60)
                            print("🎉 TESTE CONCLUÍDO!")
                            print("="*60)
                            print("\n✨ Resumo:")
                            print(f"   • 3 imagens criadas em paralelo")
                            print(f"   • 3 imagens editadas em paralelo")
                            print(f"   • Tempo de edição: {elapsed:.0f}s")
                            print(f"   • Arquivos salvos em ~/Downloads")
                            print("\n💡 O servidor detectou automaticamente:")
                            print("   • PASSO 1: modo CRIAR (sem image_urls)")
                            print("   • PASSO 2: modo EDITAR (com image_urls)")
                            print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
