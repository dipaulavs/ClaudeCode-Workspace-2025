#!/usr/bin/env python3
"""Teste: Criar campanha COM targeting por raio (sem HOUSING)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from meta_ads_campaigns import MetaAdsCampaigns
from meta_ads_adsets import MetaAdsAdSets
from meta_ads_creatives import MetaAdsCreatives
from meta_ads_ads import MetaAdsAds
from meta_ads_upload_image import MetaAdsImageUploader
from config import meta_ads_config as config

def test_radius_targeting():
    """Testa targeting por raio SEM categoria HOUSING"""

    print("🧪 TESTE: Targeting por Raio (SEM HOUSING)")
    print("=" * 60)

    image_path = "/Users/felipemdepaula/Downloads/luxuoso_apartamento_minimalista_em_belo_horizonte_c1e8.png"

    campaigns_mgr = MetaAdsCampaigns()
    adsets_mgr = MetaAdsAdSets()
    creatives_mgr = MetaAdsCreatives()
    ads_mgr = MetaAdsAds()
    uploader = MetaAdsImageUploader()

    # PASSO 1: Upload imagem
    print("\n1️⃣  Upload da imagem...")
    image_hash = uploader.upload_image(image_path)
    if not image_hash:
        return False

    # PASSO 2: Campanha SEM special_ad_categories
    print("\n2️⃣  Criar campanha (SEM HOUSING)...")
    campaign_id = campaigns_mgr.create_campaign(
        name="[TESTE RAIO] Apartamento BH - 20km",
        objective="OUTCOME_TRAFFIC",
        status="PAUSED",
        daily_budget=15.0,
        special_ad_categories=[]  # SEM categoria especial!
    )
    if not campaign_id:
        return False

    # PASSO 3: Ad set com custom_locations + radius
    print("\n3️⃣  Criar ad set com radius...")

    # Formato correto para custom_locations
    targeting = {
        "geo_locations": {
            "custom_locations": [
                {
                    "latitude": -19.9167,
                    "longitude": -43.9345,
                    "radius": 20,
                    "distance_unit": "kilometer"
                }
            ]
        },
        "age_min": 30,
        "age_max": 60,
        "targeting_automation": {
            "advantage_audience": 0  # 0=desabilitado, 1=habilitado (recomendado pelo Meta)
        }
    }

    print(f"📍 Targeting: BH com raio de 20km")

    adset_id = adsets_mgr.create_adset(
        campaign_id=campaign_id,
        name="[TESTE] BH - Raio 20km",
        daily_budget=None,
        optimization_goal="LINK_CLICKS",
        billing_event="IMPRESSIONS",
        targeting=targeting,
        status="PAUSED"
    )
    if not adset_id:
        print("\n❌ Falhou! Vou tentar formato alternativo...")
        # Tenta formato com location_types
        targeting_alt = {
            "geo_locations": {
                "location_types": ["home", "recent"],
                "custom_locations": [
                    {
                        "latitude": -19.9167,
                        "longitude": -43.9345,
                        "radius": 20,
                        "distance_unit": "kilometer",
                        "name": "Belo Horizonte, MG"
                    }
                ]
            },
            "age_min": 30,
            "age_max": 60,
            "targeting_automation": {
                "advantage_audience": 0
            }
        }

        adset_id = adsets_mgr.create_adset(
            campaign_id=campaign_id,
            name="[TESTE] BH - Raio 20km v2",
            daily_budget=None,
            optimization_goal="LINK_CLICKS",
            billing_event="IMPRESSIONS",
            targeting=targeting_alt,
            status="PAUSED"
        )

        if not adset_id:
            return False

    # PASSO 4: Criativo
    print("\n4️⃣  Criar criativo...")
    creative_id = creatives_mgr.create_creative(
        name="[TESTE] Criativo BH",
        page_id=config.PAGE_ID,
        message="🏢 Apartamento de luxo em Belo Horizonte! Design minimalista. 🔑",
        link="https://lfimoveis.com.br",
        image_hash=image_hash,
        call_to_action="LEARN_MORE"
    )
    if not creative_id:
        return False

    # PASSO 5: Anúncio
    print("\n5️⃣  Criar anúncio...")
    ad_id = ads_mgr.create_ad(
        adset_id=adset_id,
        name="[TESTE] Anúncio BH Raio",
        creative_id=creative_id,
        status="PAUSED"
    )
    if not ad_id:
        return False

    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)
    print(f"Campaign ID: {campaign_id}")
    print(f"Ad Set ID: {adset_id}")
    print(f"Creative ID: {creative_id}")
    print(f"Ad ID: {ad_id}")
    print("=" * 60)

    return True

if __name__ == "__main__":
    success = test_radius_targeting()
    sys.exit(0 if success else 1)
