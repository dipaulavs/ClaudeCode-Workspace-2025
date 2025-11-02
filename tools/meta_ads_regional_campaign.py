#!/usr/bin/env python3
"""Script: Cria campanha regional com targeting por raio geográfico"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from meta_ads_campaigns import MetaAdsCampaigns
from meta_ads_adsets import MetaAdsAdSets
from meta_ads_creatives import MetaAdsCreatives
from meta_ads_ads import MetaAdsAds
from meta_ads_upload_image import MetaAdsImageUploader
from config import meta_ads_config as config

def create_regional_campaign(image_path, city_name, latitude, longitude, radius_km, campaign_name, ad_message, link, age_min=25, age_max=55):
    """
    Cria campanha regional com targeting por raio

    Args:
        image_path: Caminho da imagem
        city_name: Nome da cidade (ex: "Belo Horizonte, MG")
        latitude: Latitude da cidade
        longitude: Longitude da cidade
        radius_km: Raio em quilômetros
        campaign_name: Nome da campanha
        ad_message: Mensagem do anúncio
        link: Link de destino
        age_min: Idade mínima (padrão: 25)
        age_max: Idade máxima (padrão: 55)
    """

    print("🎯 CRIANDO CAMPANHA REGIONAL")
    print("=" * 60)
    print(f"📍 Localização: {city_name}")
    print(f"📏 Raio: {radius_km}km")
    print(f"🗺️  Coordenadas: {latitude}, {longitude}")
    print("=" * 60)

    # Instanciar gerenciadores
    campaigns_mgr = MetaAdsCampaigns()
    adsets_mgr = MetaAdsAdSets()
    creatives_mgr = MetaAdsCreatives()
    ads_mgr = MetaAdsAds()
    uploader = MetaAdsImageUploader()

    # PASSO 1: Upload da imagem
    print("\n📤 PASSO 1: Upload da imagem")
    print("-" * 60)
    image_hash = uploader.upload_image(image_path)
    if not image_hash:
        print("❌ Falha no upload da imagem")
        return False

    # PASSO 2: Criar campanha (PAUSED)
    print("\n📋 PASSO 2: Criar campanha")
    print("-" * 60)
    campaign_id = campaigns_mgr.create_campaign(
        name=campaign_name,
        objective="OUTCOME_TRAFFIC",
        status="PAUSED",
        daily_budget=15.0,  # $15/dia
        special_ad_categories=[]  # SEM categoria especial (necessário para targeting por raio)
    )
    if not campaign_id:
        print("❌ Falha ao criar campanha")
        return False

    # PASSO 3: Criar ad set com targeting regional
    print("\n📦 PASSO 3: Criar ad set com targeting regional")
    print("-" * 60)

    # Targeting regional com raio em km
    # IMPORTANTE: Não funciona com special_ad_categories (HOUSING, CREDIT, EMPLOYMENT)
    # Para usar raio, a campanha deve ser criada SEM categoria especial

    targeting = {
        "geo_locations": {
            "custom_locations": [
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius": radius_km,
                    "distance_unit": "kilometer"
                }
            ]
        },
        "age_min": age_min,
        "age_max": age_max,
        "targeting_automation": {
            "advantage_audience": 0  # OBRIGATÓRIO! 0=desabilitado, 1=habilitado
        }
    }

    print(f"📍 Targeting: {city_name}")
    print(f"📏 Raio: {radius_km}km (lat: {latitude}, lon: {longitude})")
    print(f"⚠️  Nota: Certifique-se que a campanha NÃO tem special_ad_categories")

    adset_id = adsets_mgr.create_adset(
        campaign_id=campaign_id,
        name=f"[REGIONAL] {city_name} - {radius_km}km",
        daily_budget=None,  # Orçamento definido na campanha
        optimization_goal="LINK_CLICKS",
        billing_event="IMPRESSIONS",
        targeting=targeting,
        status="PAUSED"
    )
    if not adset_id:
        print("❌ Falha ao criar ad set")
        return False

    # PASSO 4: Criar criativo
    print("\n🎨 PASSO 4: Criar criativo")
    print("-" * 60)
    creative_id = creatives_mgr.create_creative(
        name=f"[REGIONAL] Criativo {city_name}",
        page_id=config.PAGE_ID,
        message=ad_message,
        link=link,
        image_hash=image_hash,
        call_to_action="LEARN_MORE"
    )
    if not creative_id:
        print("❌ Falha ao criar criativo")
        return False

    # PASSO 5: Criar anúncio
    print("\n📢 PASSO 5: Criar anúncio")
    print("-" * 60)
    ad_id = ads_mgr.create_ad(
        adset_id=adset_id,
        name=f"[REGIONAL] Anúncio {city_name}",
        creative_id=creative_id,
        status="PAUSED"
    )
    if not ad_id:
        print("❌ Falha ao criar anúncio")
        return False

    # SUCESSO!
    print("\n" + "=" * 60)
    print("✅ CAMPANHA REGIONAL CRIADA COM SUCESSO!")
    print("=" * 60)
    print(f"📋 Campaign ID: {campaign_id}")
    print(f"📦 Ad Set ID: {adset_id}")
    print(f"🎨 Creative ID: {creative_id}")
    print(f"📢 Ad ID: {ad_id}")
    print(f"🔑 Image Hash: {image_hash}")
    print("=" * 60)
    print(f"📍 Targeting: {city_name}")
    print(f"📏 Raio: {radius_km}km")
    print(f"🗺️  Coordenadas: {latitude}, {longitude}")
    print(f"👥 Idade: {age_min}-{age_max} anos")
    print("=" * 60)
    print("⚠️  Status: PAUSED (inativo)")
    print("💡 Para ativar, use:")
    print(f"   python3 tools/meta_ads_campaigns.py update {campaign_id} --status ACTIVE")
    print("=" * 60)

    return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cria campanha regional Meta Ads")
    parser.add_argument("image_path", help="Caminho da imagem")
    parser.add_argument("city_name", help="Nome da cidade (ex: 'Belo Horizonte, MG')")
    parser.add_argument("latitude", type=float, help="Latitude da cidade")
    parser.add_argument("longitude", type=float, help="Longitude da cidade")
    parser.add_argument("radius_km", type=int, help="Raio em quilômetros")
    parser.add_argument("campaign_name", help="Nome da campanha")
    parser.add_argument("ad_message", help="Mensagem do anúncio")
    parser.add_argument("link", help="Link de destino")
    parser.add_argument("--age-min", type=int, default=25, help="Idade mínima (padrão: 25)")
    parser.add_argument("--age-max", type=int, default=55, help="Idade máxima (padrão: 55)")

    args = parser.parse_args()

    success = create_regional_campaign(
        image_path=args.image_path,
        city_name=args.city_name,
        latitude=args.latitude,
        longitude=args.longitude,
        radius_km=args.radius_km,
        campaign_name=args.campaign_name,
        ad_message=args.ad_message,
        link=args.link,
        age_min=args.age_min,
        age_max=args.age_max
    )

    sys.exit(0 if success else 1)
