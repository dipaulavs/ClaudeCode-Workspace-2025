#!/usr/bin/env python3
"""
Mostra detalhes completos de uma campanha específica
"""

import requests
import json

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# ID da campanha ativa
CAMPAIGN_ID = "120239403628280242"

print(f"\n🔍 Buscando detalhes da campanha {CAMPAIGN_ID}...\n")
print("=" * 100)

# Campanha
url = f"{BASE_URL}/{CAMPAIGN_ID}"
params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'id,name,objective,status,effective_status,created_time,updated_time'
}
campaign = requests.get(url, params=params).json()

print("\n📊 CAMPANHA:")
print(f"   Nome: {campaign.get('name')}")
print(f"   Objetivo: {campaign.get('objective')}")
print(f"   Status: {campaign.get('effective_status')}")
print(f"   Criada: {campaign.get('created_time', '')[:10]}")

# AdSets
url = f"{BASE_URL}/{CAMPAIGN_ID}/adsets"
params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'id,name,targeting,insights.date_preset(lifetime){cpc,spend,clicks,impressions}'
}
adsets = requests.get(url, params=params).json().get('data', [])

print(f"\n📁 ADSETS ({len(adsets)}):\n")

for idx, adset in enumerate(adsets, 1):
    print(f"{idx}. {adset['name']}")
    print(f"   ID: {adset['id']}")

    # Targeting
    targeting = adset.get('targeting', {})
    print(f"\n   🎯 SEGMENTAÇÃO:")

    # Localização
    geo = targeting.get('geo_locations', {})
    if 'cities' in geo:
        print(f"      Cidades: {[c.get('name') for c in geo['cities']]}")
    if 'regions' in geo:
        print(f"      Regiões: {[r.get('name') for r in geo['regions']]}")

    # Idade
    print(f"      Idade: {targeting.get('age_min', 18)}-{targeting.get('age_max', 65)}")

    # Gênero
    if 'genders' in targeting:
        genders = {1: 'Masculino', 2: 'Feminino'}
        print(f"      Gênero: {[genders.get(g, 'Todos') for g in targeting['genders']]}")

    # Interesses
    if 'flexible_spec' in targeting:
        for spec in targeting['flexible_spec']:
            if 'interests' in spec:
                interests = [i.get('name') for i in spec['interests']]
                print(f"      Interesses: {interests}")

    # Métricas
    insights = adset.get('insights', {}).get('data', [])
    if insights:
        insight = insights[0]
        print(f"\n   📈 MÉTRICAS:")
        print(f"      CPC: R$ {insight.get('cpc', 'N/A')}")
        print(f"      Gasto: R$ {insight.get('spend', 'N/A')}")
        print(f"      Cliques: {insight.get('clicks', 'N/A')}")
        print(f"      Impressões: {insight.get('impressions', 'N/A')}")

    # Anúncios
    url_ads = f"{BASE_URL}/{adset['id']}/ads"
    params_ads = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,creative{id,title,body,object_story_spec},insights.date_preset(lifetime){cpc,spend,clicks,impressions,reach}'
    }
    ads = requests.get(url_ads, params=params_ads).json().get('data', [])

    print(f"\n   🎨 CRIATIVOS ({len(ads)}):\n")

    for ad_idx, ad in enumerate(ads, 1):
        print(f"   {ad_idx}. {ad['name']}")
        print(f"      ID: {ad['id']}")

        creative = ad.get('creative', {})
        print(f"      Creative ID: {creative.get('id')}")
        print(f"      Título: {creative.get('title', 'N/A')}")

        # Detecta formato
        obj_story = creative.get('object_story_spec', {})
        formato = "Único"

        if 'link_data' in obj_story:
            link_data = obj_story['link_data']
            if 'child_attachments' in link_data:
                formato = f"Carrossel ({len(link_data['child_attachments'])})"
            elif 'video_id' in link_data:
                formato = "Reels"

        print(f"      Formato: {formato}")

        # Métricas do anúncio
        ad_insights = ad.get('insights', {}).get('data', [])
        if ad_insights:
            ad_insight = ad_insights[0]
            print(f"\n      📈 MÉTRICAS DO CRIATIVO:")
            print(f"         CPC: R$ {ad_insight.get('cpc', 'N/A')}")
            print(f"         Gasto: R$ {ad_insight.get('spend', 'N/A')}")
            print(f"         Cliques: {ad_insight.get('clicks', 'N/A')}")
            print(f"         Impressões: {ad_insight.get('impressions', 'N/A')}")
            print(f"         Alcance: {ad_insight.get('reach', 'N/A')}")

        print()

print("=" * 100 + "\n")
