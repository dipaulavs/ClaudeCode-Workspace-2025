#!/usr/bin/env python3
"""
Renomeia campanhas na conta CORRETA: act_990218527765536
"""

import requests
from datetime import datetime

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_990218527765536"  # CONTA CORRETA
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def get_all_campaigns():
    """Busca TODAS as campanhas"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,effective_status,objective,created_time',
        'limit': 100
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('data', [])


def get_adsets(campaign_id):
    """Lista adsets"""
    url = f"{BASE_URL}/{campaign_id}/adsets"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,targeting,insights{cpc}'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except:
        return []


def get_ads(adset_id):
    """Lista ads"""
    url = f"{BASE_URL}/{adset_id}/ads"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,creative{id,object_story_spec,video_id},insights{cpc}'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except:
        return []


def update_name(object_id, new_name):
    """Atualiza nome"""
    url = f"{BASE_URL}/{object_id}"
    data = {
        'access_token': ACCESS_TOKEN,
        'name': new_name
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get('success', False)


def extract_location(targeting):
    """Extrai localização"""
    geo = targeting.get('geo_locations', {})

    if 'cities' in geo and geo['cities']:
        city = geo['cities'][0].get('name', 'BR')
        return city.split(',')[0] if ',' in city else city
    elif 'regions' in geo and geo['regions']:
        region = geo['regions'][0].get('name', 'BR')
        return region.split(',')[0] if ',' in region else region

    return 'BR'


def extract_interests(targeting):
    """Extrai interesses"""
    interests = []

    if 'flexible_spec' in targeting:
        for spec in targeting['flexible_spec']:
            if 'interests' in spec:
                for interest in spec['interests'][:2]:
                    name = interest.get('name', '')
                    if name:
                        interests.append(name[:15])

    return ' + '.join(interests[:2]) if interests else 'Broad'


def detect_format(creative):
    """Detecta formato"""
    obj_story = creative.get('object_story_spec', {})

    if 'link_data' in obj_story:
        link_data = obj_story['link_data']

        if 'child_attachments' in link_data:
            return f"Carrossel ({len(link_data['child_attachments'])})"

        if 'video_id' in link_data or creative.get('video_id'):
            return "Reels"

    if creative.get('video_id'):
        return "Reels"

    return "Único"


def format_cpc(insights):
    """Formata CPC"""
    if not insights:
        return "Sem dados"

    cpc = insights.get('cpc')
    return f"R$ {float(cpc):.2f}" if cpc else "Sem dados"


def generate_names(campaign, adsets, all_ads):
    """Gera nomes com padrão customizado"""

    # CAMPANHA: Imovel X | engajamento - Wpp | dia/mes
    created = campaign.get('created_time', '')
    date_str = datetime.strptime(created[:10], '%Y-%m-%d').strftime('%d/%m') if created else datetime.now().strftime('%d/%m')

    objective = campaign.get('objective', '')
    engagement_map = {
        'OUTCOME_LEADS': 'Leads - Wpp',
        'OUTCOME_TRAFFIC': 'Tráfego - Wpp',
        'OUTCOME_ENGAGEMENT': 'Engajamento - Wpp',
        'OUTCOME_AWARENESS': 'Alcance - Wpp',
        'OUTCOME_SALES': 'Vendas - Wpp'
    }
    engagement = engagement_map.get(objective, 'Engajamento - Wpp')

    old_name = campaign.get('name', '')

    # Extrai nome do imóvel do nome atual
    if any(word in old_name.lower() for word in ['apartamento', 'casa', 'imovel', 'cobertura', 'lote', 'terreno']):
        # Pega primeira palavra que seja relevante
        words = old_name.split()
        for word in words:
            if word.lower() in ['apartamento', 'casa', 'imovel', 'cobertura', 'lote', 'terreno']:
                imovel = word
                break
        else:
            imovel = 'Imóvel Premium'
    else:
        imovel = 'Imóvel Premium'

    campaign_name = f"{imovel} │ {engagement} │ {date_str}"

    # ADSETS
    adset_names = {}
    for adset in adsets:
        targeting = adset.get('targeting', {})
        location = extract_location(targeting)
        interests = extract_interests(targeting)

        age_min = targeting.get('age_min', 18)
        age_max = targeting.get('age_max', 65)

        ad_count = len([a for a in all_ads if a.get('adset_id') == adset['id']])

        adset_names[adset['id']] = f"{location} ({age_min}-{age_max}) │ {interests} │ {ad_count} criativos"

    # ADS
    ad_names = {}
    for idx, ad in enumerate(all_ads, 1):
        creative = ad.get('creative', {})
        creative_id = creative.get('id', f'{idx:02d}')

        formato = detect_format(creative)

        insights_data = ad.get('insights', {}).get('data', [])
        insights = insights_data[0] if insights_data else {}
        cpc = format_cpc(insights)

        ad_names[ad['id']] = f"ID{creative_id[-6:]} │ {formato} │ {cpc}"

    return campaign_name, adset_names, ad_names


def main():
    print(f"\n🔍 Buscando campanhas na conta: {AD_ACCOUNT_ID}\n")

    campaigns = get_all_campaigns()

    if not campaigns:
        print("❌ Nenhuma campanha encontrada")
        return

    print(f"📊 {len(campaigns)} campanha(s) encontrada(s)\n")

    # Mostrar todas primeiro
    print("=" * 100)
    for idx, c in enumerate(campaigns, 1):
        print(f"{idx}. {c['name']}")
        print(f"   ID: {c['id']}")
        print(f"   Status: {c.get('effective_status', 'DRAFT')}")
        print()

    print("=" * 100)

    # Filtrar apenas as que ainda não foram renomeadas
    to_rename = [c for c in campaigns if '│' not in c['name']]

    if not to_rename:
        print("\n✅ Todas as campanhas já estão com o padrão correto!\n")
        return

    print(f"\n🎯 {len(to_rename)} campanha(s) para renomear:\n")

    for campaign in to_rename:
        print("=" * 100)
        print(f"\n📌 CAMPANHA: {campaign['name']}")
        print(f"   ID: {campaign['id']}")
        print(f"   Status: {campaign.get('effective_status', 'DRAFT')}")

        adsets = get_adsets(campaign['id'])

        all_ads = []
        for adset in adsets:
            ads = get_ads(adset['id'])
            for ad in ads:
                ad['adset_id'] = adset['id']
            all_ads.extend(ads)

        print(f"   📁 {len(adsets)} AdSet(s) | 🎨 {len(all_ads)} Criativo(s)\n")

        # Gerar novos nomes
        new_campaign_name, adset_names, ad_names = generate_names(campaign, adsets, all_ads)

        print("🎯 NOVOS NOMES:\n")
        print(f"📊 Campanha: {new_campaign_name}")

        for adset_id, name in adset_names.items():
            print(f"📁 AdSet: {name}")

        for ad_id, name in ad_names.items():
            print(f"🎨 Criativo: {name}")

        print("\n🚀 Aplicando...\n")

        try:
            update_name(campaign['id'], new_campaign_name)
            print(f"✅ Campanha renomeada")

            for adset_id, name in adset_names.items():
                update_name(adset_id, name)
                print(f"✅ AdSet renomeado")

            for ad_id, name in ad_names.items():
                update_name(ad_id, name)
                print(f"✅ Criativo renomeado")

            print(f"\n🎉 {1 + len(adset_names) + len(ad_names)} itens atualizados!\n")

        except Exception as e:
            print(f"❌ Erro: {e}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
