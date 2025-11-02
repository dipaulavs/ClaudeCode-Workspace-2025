#!/usr/bin/env python3
"""Script de teste: Cria campanha completa com imagem"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from meta_ads_campaigns import MetaAdsCampaigns
from meta_ads_adsets import MetaAdsAdSets
from meta_ads_creatives import MetaAdsCreatives
from meta_ads_ads import MetaAdsAds
from meta_ads_upload_image import MetaAdsImageUploader
from config import meta_ads_config as config

def create_test_campaign(image_path):
    """Cria campanha de teste completa"""

    print("🚀 CRIANDO CAMPANHA DE TESTE COMPLETA")
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
        name="[TESTE] Campanha Casa Moderna - LF Imóveis",
        objective="OUTCOME_TRAFFIC",
        status="PAUSED",
        daily_budget=10.0,  # $10/dia
        special_ad_categories=["HOUSING"]  # Categoria: Imóveis
    )
    if not campaign_id:
        print("❌ Falha ao criar campanha")
        return False

    # PASSO 3: Criar ad set (PAUSED)
    print("\n📦 PASSO 3: Criar ad set")
    print("-" * 60)
    targeting = {
        "geo_locations": {"countries": ["BR"]},  # Brasil
        "age_min": 25,
        "age_max": 55,
        "interests": [
            {"id": "6003107902433", "name": "Real estate"}  # Interesse em imóveis
        ]
    }

    adset_id = adsets_mgr.create_adset(
        campaign_id=campaign_id,
        name="[TESTE] Ad Set - Público Imóveis BR",
        daily_budget=None,  # Não definir orçamento aqui (já definido na campanha)
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
        name="[TESTE] Criativo Casa Moderna",
        page_id=config.PAGE_ID,
        message="✨ Conheça sua nova casa! Casa moderna com design minimalista. 🏡 Clique e descubra mais!",
        link="https://lfimoveis.com.br",  # Ajuste o link se necessário
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
        name="[TESTE] Anúncio Casa Moderna",
        creative_id=creative_id,
        status="PAUSED"
    )
    if not ad_id:
        print("❌ Falha ao criar anúncio")
        return False

    # SUCESSO!
    print("\n" + "=" * 60)
    print("✅ CAMPANHA DE TESTE CRIADA COM SUCESSO!")
    print("=" * 60)
    print(f"📋 Campaign ID: {campaign_id}")
    print(f"📦 Ad Set ID: {adset_id}")
    print(f"🎨 Creative ID: {creative_id}")
    print(f"📢 Ad ID: {ad_id}")
    print(f"🔑 Image Hash: {image_hash}")
    print("=" * 60)
    print("⚠️  Status: PAUSED (inativo)")
    print("💡 Para ativar, use:")
    print(f"   python3 tools/meta_ads_campaigns.py update {campaign_id} --status ACTIVE")
    print("=" * 60)

    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Caminho da imagem")
    args = parser.parse_args()

    success = create_test_campaign(args.image_path)
    sys.exit(0 if success else 1)
