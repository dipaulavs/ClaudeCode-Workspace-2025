#!/usr/bin/env python3
"""
Setup: Upload das 4 Fotos Base para Nextcloud

Faz upload das suas 4 fotos para Nextcloud UMA VEZ e salva as URLs
permanentes em photos_urls.json para reutilização.

Uso:
    python3 scripts/thumbnail-creation/setup_photos.py
"""

import sys
import json
from pathlib import Path

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from upload_to_nextcloud import upload_to_nextcloud


def setup_photos():
    """Faz upload das 4 fotos e salva URLs permanentes"""

    print("📸 Setup de Fotos Base para Thumbnails")
    print("=" * 60)

    script_dir = Path(__file__).resolve().parent
    photos_dir = script_dir / "templates" / "fotos"
    config_file = script_dir / "photos_urls.json"

    # Verifica se já existe config
    if config_file.exists():
        print("⚠️  Arquivo photos_urls.json já existe!")
        response = input("Deseja refazer o upload? (s/N): ").strip().lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("✅ Mantendo URLs existentes")
            return 0

    # Busca as 4 fotos
    photos = []
    for i in range(1, 5):
        for ext in ['jpg', 'jpeg', 'png']:
            photo_path = photos_dir / f"foto{i}.{ext}"
            if photo_path.exists():
                photos.append((i, photo_path))
                break

    if len(photos) < 4:
        print(f"\n❌ Erro: Apenas {len(photos)} foto(s) encontrada(s)")
        print("\n📸 Adicione 4 fotos em:")
        print(f"   {photos_dir}/")
        print("\nNomes esperados:")
        print("   - foto1.jpg (ou .png)")
        print("   - foto2.jpg (ou .png)")
        print("   - foto3.jpg (ou .png)")
        print("   - foto4.jpg (ou .png)")
        return 1

    print(f"\n✅ {len(photos)} fotos encontradas:")
    for num, path in photos:
        print(f"   {num}. {path.name}")

    # Upload de cada foto (PERMANENTE - 365 dias)
    print(f"\n📤 Fazendo upload para Nextcloud (URLs permanentes)...")
    urls = {}

    for num, photo_path in photos:
        print(f"\n   Foto {num}/{len(photos)}: {photo_path.name}")

        try:
            # Upload permanente (1 ano = 365 dias)
            url = upload_to_nextcloud(str(photo_path), expire_days=365)
            urls[f"foto{num}"] = {
                "filename": photo_path.name,
                "url": url,
                "uploaded_at": None  # Poderia adicionar timestamp
            }
            print(f"   ✅ URL salva")

        except Exception as e:
            print(f"   ❌ Erro ao fazer upload: {e}")
            return 1

    # Salva URLs em JSON
    print(f"\n💾 Salvando URLs em {config_file.name}...")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(urls, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("✅ Setup Concluído!")
    print("=" * 60)
    print(f"\n📊 {len(urls)} URLs salvas em: {config_file}")
    print("\n💡 Agora você pode criar thumbnails sem re-upload:")
    print('   python3 scripts/thumbnail-creation/create_thumbnails.py "Sua Headline"')

    return 0


if __name__ == "__main__":
    sys.exit(setup_photos())
