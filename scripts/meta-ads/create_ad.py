#!/usr/bin/env python3
"""
Template: Criar Anúncio Meta Ads (Criativo + Ad)

Uso:
    python3 scripts/meta-ads/create_ad.py --adset-id 123 --name "Anúncio Casa" --message "Casa linda!" --link "https://site.com" --image "foto.jpg"
    python3 scripts/meta-ads/create_ad.py -a 123 -n "Ad Casa" -m "Conheça!" -l "https://site.com" -i "img.jpg" -c SHOP_NOW
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.meta_ads_creatives import MetaAdsCreatives
from tools.meta_ads_ads import MetaAdsAds
from tools.meta_ads_upload_image import MetaAdsImageUploader
from config import meta_ads_config as config

def create_ad(adset_id: str, name: str, message: str, link: str,
             image_path: str, cta: str = "LEARN_MORE", status: str = "PAUSED"):
    """
    Cria anúncio completo (upload imagem + criativo + ad)

    Args:
        adset_id: ID do ad set pai
        name: Nome do anúncio
        message: Texto do anúncio
        link: URL de destino
        image_path: Caminho da imagem
        cta: Call to action
        status: Status inicial

    Returns:
        Dict com ad_id, creative_id, image_hash
    """
    # 1. Upload da imagem
    print("   📤 Fazendo upload da imagem...")
    uploader = MetaAdsImageUploader()
    image_hash = uploader.upload_image(image_path)

    if not image_hash:
        raise Exception("Falha no upload da imagem")

    # 2. Criar criativo
    print("   🎨 Criando criativo...")
    creatives_mgr = MetaAdsCreatives()
    creative_id = creatives_mgr.create_creative(
        name=f"{name} - Creative",
        page_id=config.PAGE_ID,
        message=message,
        link=link,
        image_hash=image_hash,
        call_to_action=cta
    )

    if not creative_id:
        raise Exception("Falha ao criar criativo")

    # 3. Criar anúncio
    print("   📢 Criando anúncio...")
    ads_mgr = MetaAdsAds()
    ad_id = ads_mgr.create_ad(
        adset_id=adset_id,
        name=name,
        creative_id=creative_id,
        status=status
    )

    if not ad_id:
        raise Exception("Falha ao criar anúncio")

    return {
        "ad_id": ad_id,
        "creative_id": creative_id,
        "image_hash": image_hash
    }

def main():
    parser = argparse.ArgumentParser(description='Criar anúncio Meta Ads completo')

    parser.add_argument('--adset-id', '-a', required=True,
                       help='ID do ad set pai')
    parser.add_argument('--name', '-n', required=True,
                       help='Nome do anúncio')
    parser.add_argument('--message', '-m', required=True,
                       help='Texto do anúncio')
    parser.add_argument('--link', '-l', required=True,
                       help='URL de destino')
    parser.add_argument('--image', '-i', required=True,
                       help='Caminho da imagem')
    parser.add_argument('--cta', '-c', default='LEARN_MORE',
                       choices=['LEARN_MORE', 'SHOP_NOW', 'SIGN_UP', 'DOWNLOAD',
                               'GET_QUOTE', 'CONTACT_US', 'APPLY_NOW'],
                       help='Call to action (padrão: LEARN_MORE)')
    parser.add_argument('--status', '-s', default='PAUSED',
                       choices=['ACTIVE', 'PAUSED'],
                       help='Status inicial (padrão: PAUSED)')

    args = parser.parse_args()

    # Validar arquivo de imagem
    image_file = Path(args.image)
    if not image_file.exists():
        print(f"❌ Erro: Arquivo de imagem não encontrado: {args.image}")
        sys.exit(1)

    # Mensagem de início
    print(f"📢 Criando anúncio '{args.name}'...")
    print(f"   Ad Set ID: {args.adset_id}")
    print(f"   Mensagem: {args.message[:50]}{'...' if len(args.message) > 50 else ''}")
    print(f"   Link: {args.link}")
    print(f"   Imagem: {args.image}")
    print(f"   CTA: {args.cta}")

    try:
        result = create_ad(
            args.adset_id,
            args.name,
            args.message,
            args.link,
            args.image,
            args.cta,
            args.status
        )

        print(f"\n✅ Anúncio criado com sucesso!")
        print(f"   Ad ID: {result['ad_id']}")
        print(f"   Creative ID: {result['creative_id']}")
        print(f"   Image Hash: {result['image_hash']}")
        print(f"   Status: {args.status}")

        if args.status == "PAUSED":
            print(f"\n💡 Para ativar: python3 tools/meta_ads_ads.py update {result['ad_id']} --status ACTIVE")

        return result
    except Exception as e:
        print(f"❌ Erro ao criar anúncio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
