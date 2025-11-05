#!/usr/bin/env python3
"""
Script de teste para o MCP Nextcloud Upload
Testa cada tool individualmente
"""

import sys
import os

# Adiciona path do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path

# Importa funções do server
import asyncio
from mcp_nextcloud_upload.server import (
    upload_single_image,
    upload_batch_images,
    scan_upload_folder,
    UPLOAD_FOLDER
)


async def test_scan():
    """Teste 1: Escanear pasta"""
    print("📂 Teste 1: Escaneando pasta de upload...")
    files = await scan_upload_folder()

    if files:
        print(f"✅ Encontrados {len(files)} arquivo(s):")
        for f in files:
            print(f"   - {f['filename']} ({f['size_mb']} MB)")
    else:
        print(f"⚠️  Nenhum arquivo em {UPLOAD_FOLDER}")

    return files


async def test_single_upload():
    """Teste 2: Upload único (sem deletar)"""
    print("\n📤 Teste 2: Upload de 1 arquivo...")

    # Busca primeiro arquivo da pasta
    files = await scan_upload_folder()
    if not files:
        print("⚠️  Nenhum arquivo para testar")
        return None

    test_file = files[0]['path']
    print(f"Arquivo de teste: {Path(test_file).name}")

    result = await upload_single_image(test_file, auto_delete=False)

    if result['success']:
        print(f"✅ Upload bem-sucedido!")
        print(f"   URL: {result['url']}")
    else:
        print(f"❌ Erro: {result['error']}")

    return result


async def test_batch_upload():
    """Teste 3: Upload batch (sem deletar)"""
    print("\n📤 Teste 3: Upload batch (até 3 arquivos)...")

    # Busca até 3 arquivos
    files = await scan_upload_folder()
    if not files:
        print("⚠️  Nenhum arquivo para testar")
        return None

    test_files = [f['path'] for f in files[:3]]
    print(f"Testando {len(test_files)} arquivo(s)...")

    results = await upload_batch_images(test_files, auto_delete=False)

    success_count = sum(1 for r in results if r['success'])
    print(f"\n✅ Resultado: {success_count}/{len(results)} sucesso")

    for r in results:
        if r['success']:
            print(f"   ✓ {r['filename']}: {r['url']}")
        else:
            print(f"   ✗ {r['filename']}: {r['error']}")

    return results


async def main():
    """Executa todos os testes"""
    print("🧪 Testando MCP Nextcloud Upload")
    print("="*60)

    try:
        # Teste 1: Scan
        files = await test_scan()

        if not files:
            print("\n⚠️  Adicione arquivos em ~/Pictures/upload/ para testar uploads")
            return

        # Teste 2: Upload único
        await test_single_upload()

        # Teste 3: Batch
        if len(files) > 1:
            await test_batch_upload()

        print("\n" + "="*60)
        print("✅ Testes concluídos!")
        print("\n💡 Todos os uploads usaram auto_delete=False")
        print("   (arquivos locais foram mantidos para testes)")

    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
