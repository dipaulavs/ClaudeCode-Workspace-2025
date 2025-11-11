#!/usr/bin/env python3
"""
Busca todas as campanhas com métricas históricas
"""

import requests
import json

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

print("\n🔍 Buscando TODAS as campanhas com métricas...\n")
print("=" * 100)

# Buscar todas as campanhas
url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'id,name,objective,status,effective_status',
    'limit': 100
}
campaigns = requests.get(url, params=params).json().get('data', [])

print(f"\n✅ {len(campaigns)} campanhas encontradas\n")

for idx, campaign in enumerate(campaigns, 1):
    status_icon = "🟢" if campaign.get('effective_status') == 'ACTIVE' else "⏸️"
    print(f"\n{status_icon} CAMPANHA {idx}: {campaign['name']}")
    print(f"   ID: {campaign['id']}")

    # Buscar adsets
    url_adsets = f"{BASE_URL}/{campaign['id']}/adsets"
    params_adsets = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,targeting,insights.date_preset(lifetime){cpc,cpm,spend,clicks,impressions,reach}'
    }

    try:
        adsets = requests.get(url_adsets, params=params_adsets).json().get('data', [])

        if not adsets:
            print(f"   ⚠️ Sem adsets")
            continue

        print(f"\n   📁 {len(adsets)} ADSET(S):")

        for adset_idx, adset in enumerate(adsets, 1):
            print(f"\n   {adset_idx}. {adset['name']}")

            # Targeting
            targeting = adset.get('targeting', {})

            # Localização
            geo = targeting.get('geo_locations', {})
            if 'cities' in geo and geo['cities']:
                cities = [c.get('name', '') for c in geo['cities'][:2]]
                print(f"      📍 Cidades: {', '.join(cities)}")
            elif 'regions' in geo and geo['regions']:
                regions = [r.get('name', '') for r in geo['regions'][:2]]
                print(f"      📍 Regiões: {', '.join(regions)}")

            # Idade
            age_min = targeting.get('age_min', 18)
            age_max = targeting.get('age_max', 65)
            print(f"      👥 Idade: {age_min}-{age_max}")

            # Interesses
            if 'flexible_spec' in targeting:
                for spec in targeting['flexible_spec']:
                    if 'interests' in spec:
                        interests = [i.get('name', '') for i in spec['interests'][:3]]
                        if interests:
                            print(f"      🎯 Interesses: {', '.join(interests)}")

            # Métricas do adset
            insights_data = adset.get('insights', {}).get('data', [])
            if insights_data:
                insights = insights_data[0]
                print(f"\n      📊 MÉTRICAS ADSET:")
                print(f"         💰 Gasto: R$ {insights.get('spend', '0')}")
                print(f"         👆 Cliques: {insights.get('clicks', '0')}")
                print(f"         👁️ Impressões: {insights.get('impressions', '0')}")
                print(f"         📈 Alcance: {insights.get('reach', '0')}")

                if insights.get('cpc'):
                    print(f"         💵 CPC: R$ {insights['cpc']}")
                elif insights.get('spend') and insights.get('clicks'):
                    try:
                        cpc = float(insights['spend']) / int(insights['clicks'])
                        print(f"         💵 CPC calculado: R$ {cpc:.2f}")
                    except:
                        pass

            # Buscar anúncios
            url_ads = f"{BASE_URL}/{adset['id']}/ads"
            params_ads = {
                'access_token': ACCESS_TOKEN,
                'fields': 'id,name,creative{id,title,body,object_story_spec,video_id},insights.date_preset(lifetime){cpc,spend,clicks,impressions,reach}'
            }

            try:
                ads = requests.get(url_ads, params=params_ads).json().get('data', [])

                if ads:
                    print(f"\n      🎨 {len(ads)} CRIATIVO(S):")

                    for ad_idx, ad in enumerate(ads, 1):
                        print(f"\n      {ad_idx}. {ad['name']}")

                        creative = ad.get('creative', {})
                        creative_id = creative.get('id', 'N/A')
                        print(f"         🆔 Creative ID: {creative_id}")

                        # Detectar formato
                        obj_story = creative.get('object_story_spec', {})
                        formato = "Único"

                        if 'link_data' in obj_story:
                            link_data = obj_story['link_data']
                            if 'child_attachments' in link_data:
                                count = len(link_data['child_attachments'])
                                formato = f"Carrossel ({count})"
                            elif 'video_id' in link_data or creative.get('video_id'):
                                formato = "Reels"

                        print(f"         🎬 Formato: {formato}")

                        # Métricas do criativo
                        ad_insights = ad.get('insights', {}).get('data', [])
                        if ad_insights:
                            ad_insight = ad_insights[0]
                            print(f"\n         📊 MÉTRICAS CRIATIVO:")
                            print(f"            💰 Gasto: R$ {ad_insight.get('spend', '0')}")
                            print(f"            👆 Cliques: {ad_insight.get('clicks', '0')}")
                            print(f"            👁️ Impressões: {ad_insight.get('impressions', '0')}")
                            print(f"            📈 Alcance: {ad_insight.get('reach', '0')}")

                            if ad_insight.get('cpc'):
                                print(f"            💵 CPC: R$ {ad_insight['cpc']}")
                            elif ad_insight.get('spend') and ad_insight.get('clicks'):
                                try:
                                    cpc = float(ad_insight['spend']) / int(ad_insight['clicks'])
                                    print(f"            💵 CPC calculado: R$ {cpc:.2f}")
                                except:
                                    pass
            except Exception as e:
                print(f"      ⚠️ Erro ao buscar anúncios: {e}")

    except Exception as e:
        print(f"   ⚠️ Erro ao buscar adsets: {e}")

    print("\n" + "-" * 100)

print("\n" + "=" * 100 + "\n")
