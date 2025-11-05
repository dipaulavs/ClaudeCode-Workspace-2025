#!/opt/homebrew/bin/python3.10
"""Teste local das funções do MCP"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import server functions
from server import (
    scan_upload_folder,
    upload_single_image,
    upload_batch_images,
    UPLOAD_FOLDER
)


async def test_scan():
    """Teste 1: Escanear pasta"""
    print("=" * 60)
    print("📂 TESTE 1: Scan Folder")
    print("=" * 60)

    files = await scan_upload_folder()

    print(f"\n📁 Pasta: {UPLOAD_FOLDER}")
    print(f"📸 Arquivos encontrados: {len(files)}\n")

    for f in files:
        print(f"  • {f['filename']}")
        print(f"    Tamanho: {f['size_mb']} MB")
        print(f"    Path: {f['path']}\n")

    return files


async def test_single_upload(files):
    """Teste 2: Upload único (mantém arquivo)"""
    if not files:
        print("\n⚠️  Nenhum arquivo para testar upload único")
        return None

    print("=" * 60)
    print("📤 TESTE 2: Upload Único (auto_delete=False)")
    print("=" * 60)

    test_file = files[0]['path']
    print(f"\n📸 Arquivo: {files[0]['filename']}")
    print("⏳ Fazendo upload...\n")

    result = await upload_single_image(test_file, auto_delete=False)

    if result['success']:
        print("✅ Upload bem-sucedido!\n")
        print(f"📁 Arquivo: {result['filename']}")
        print(f"🔗 URL: {result['url']}")
        print(f"🗑️  Deletado: {result['deleted']}")
    else:
        print(f"❌ Erro: {result['error']}")

    return result


async def test_batch_upload(files):
    """Teste 3: Upload batch (mantém arquivos)"""
    if len(files) < 2:
        print("\n⚠️  Precisa de pelo menos 2 arquivos para testar batch")
        return None

    print("\n" + "=" * 60)
    print("📤 TESTE 3: Upload Batch Paralelo (auto_delete=False)")
    print("=" * 60)

    test_files = [f['path'] for f in files]
    print(f"\n📸 Arquivos: {len(test_files)}")
    for f in files:
        print(f"  • {f['filename']}")

    print("\n⏳ Fazendo upload paralelo...\n")

    results = await upload_batch_images(test_files, auto_delete=False)

    success_count = sum(1 for r in results if r['success'])

    print(f"✅ Resultado: {success_count}/{len(results)} sucesso\n")

    for r in results:
        if r['success']:
            print(f"✓ {r['filename']}")
            print(f"  {r['url']}\n")
        else:
            print(f"✗ {r['filename']}: {r['error']}\n")

    return results


async def main():
    """Executa todos os testes"""
    print("\n🧪 TESTANDO MCP NEXTCLOUD UPLOAD")
    print("Versão: Python Local (não MCP server)\n")

    try:
        # Teste 1: Scan
        files = await test_scan()

        if not files:
            print("\n⚠️  Adicione arquivos em ~/Pictures/upload/ para testar")
            return

        # Teste 2: Upload único
        await test_single_upload(files)

        # Teste 3: Batch (se tiver múltiplos arquivos)
        if len(files) >= 2:
            await test_batch_upload(files)

        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("=" * 60)
        print("\n💡 Nota: Todos os uploads usaram auto_delete=False")
        print("   (arquivos foram mantidos para testes)\n")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
