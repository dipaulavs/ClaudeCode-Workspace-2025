#!/usr/bin/env python3
"""
Script para renomear campanhas Meta Ads com padrão customizado
Campanha: Imovel X | engajamento - Wpp | dia/mes
AdSet: Localização | Interesses | qtd criativo
Criativo: ID | Formato (reels/carrossel/unico) | CPC
"""

import requests
from datetime import datetime
from typing import Dict, List

# Credenciais
ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def api_get(url: str, params: dict) -> dict:
    """Faz requisição GET na API"""
    params['access_token'] = ACCESS_TOKEN
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def api_post(url: str, data: dict) -> dict:
    """Faz requisição POST na API"""
    data['access_token'] = ACCESS_TOKEN
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def get_campaigns() -> List[Dict]:
    """Lista campanhas ativas com métricas"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"

    params = {
        'fields': 'id,name,status,objective,created_time,insights{cpc,cpm,ctr,spend,impressions,clicks}',
        'effective_status': '["ACTIVE"]'
    }

    data = api_get(url, params)
    return data.get('data', [])


def get_adsets(campaign_id: str) -> List[Dict]:
    """Lista adsets com segmentação e métricas"""
    url = f"{BASE_URL}/{campaign_id}/adsets"

    params = {
        'fields': 'id,name,status,targeting,insights{cpc,spend,clicks}'
    }

    data = api_get(url, params)
    return data.get('data', [])


def get_ads(adset_id: str) -> List[Dict]:
    """Lista ads com criativo e métricas"""
    url = f"{BASE_URL}/{adset_id}/ads"

    params = {
        'fields': 'id,name,status,creative{id,name,title,body,object_story_spec,image_url,video_id,thumbnail_url},insights{cpc,spend,clicks}'
    }

    data = api_get(url, params)
    return data.get('data', [])


def extract_location(targeting: dict) -> str:
    """Extrai localização principal da segmentação"""
    geo = targeting.get('geo_locations', {})

    if 'cities' in geo and geo['cities']:
        return geo['cities'][0].get('name', 'BR')
    elif 'regions' in geo and geo['regions']:
        return geo['regions'][0].get('name', 'BR')
    elif 'countries' in geo and geo['countries']:
        return geo['countries'][0]

    return 'BR'


def extract_interests(targeting: dict) -> str:
    """Extrai interesses principais"""
    interests = []

    # Flexible spec
    if 'flexible_spec' in targeting:
        for spec in targeting['flexible_spec']:
            if 'interests' in spec:
                for interest in spec['interests'][:2]:  # Pega até 2 interesses
                    name = interest.get('name', '')
                    if name:
                        # Abrevia nome do interesse
                        interests.append(name[:15])

    # Narrow targeting
    if 'narrow_targeting' in targeting:
        for spec in targeting['narrow_targeting']:
            if 'interests' in spec:
                for interest in spec['interests'][:1]:
                    name = interest.get('name', '')
                    if name:
                        interests.append(name[:15])

    if interests:
        return ' + '.join(interests[:2])

    return 'Broad'


def extract_age_range(targeting: dict) -> str:
    """Extrai faixa etária"""
    age_min = targeting.get('age_min', 18)
    age_max = targeting.get('age_max', 65)
    return f"{age_min}-{age_max}"


def detect_creative_format(creative: dict) -> str:
    """Detecta formato do criativo"""

    # Verifica object_story_spec para carrossel
    obj_story = creative.get('object_story_spec', {})

    if 'link_data' in obj_story:
        link_data = obj_story['link_data']

        # Carrossel
        if 'child_attachments' in link_data:
            child_count = len(link_data['child_attachments'])
            return f"Carrossel ({child_count})"

        # Video/Reels
        if 'video_id' in link_data or creative.get('video_id'):
            return "Reels"

    # Video direto
    if creative.get('video_id') or creative.get('thumbnail_url'):
        return "Reels"

    # Imagem única
    if creative.get('image_url'):
        return "Único"

    return "Único"


def format_cpc(insights: dict) -> str:
    """Formata CPC em reais"""
    if not insights:
        return "Sem dados"

    cpc = insights.get('cpc')
    if cpc:
        return f"R$ {float(cpc):.2f}"

    # Calcula CPC se tiver spend e clicks
    spend = insights.get('spend')
    clicks = insights.get('clicks')

    if spend and clicks and int(clicks) > 0:
        cpc_calculated = float(spend) / int(clicks)
        return f"R$ {cpc_calculated:.2f}"

    return "Sem cliques"


def generate_campaign_name(campaign: dict) -> str:
    """
    Gera nome: Imovel X | engajamento - Wpp | dia/mes
    """
    # Data de criação
    created = campaign.get('created_time', '')
    if created:
        date_obj = datetime.strptime(created[:10], '%Y-%m-%d')
        date_str = date_obj.strftime('%d/%m')
    else:
        date_str = datetime.now().strftime('%d/%m')

    # Tipo de engajamento baseado no objetivo
    objective = campaign.get('objective', '')
    engagement_map = {
        'OUTCOME_LEADS': 'Leads - Wpp',
        'OUTCOME_TRAFFIC': 'Tráfego - Wpp',
        'OUTCOME_ENGAGEMENT': 'Engajamento - Wpp',
        'OUTCOME_AWARENESS': 'Alcance - Wpp',
        'OUTCOME_SALES': 'Vendas - Wpp'
    }
    engagement = engagement_map.get(objective, 'Engajamento - Wpp')

    # Nome do imóvel (pega do nome atual ou usa genérico)
    old_name = campaign.get('name', '')
    if 'imovel' in old_name.lower() or 'casa' in old_name.lower() or 'apto' in old_name.lower():
        imovel = old_name.split()[0]
    else:
        imovel = 'Imóvel Premium'

    return f"{imovel} │ {engagement} │ {date_str}"


def generate_adset_name(adset: dict, ad_count: int) -> str:
    """
    Gera nome: Localização | Interesses | qtd criativo
    """
    targeting = adset.get('targeting', {})

    location = extract_location(targeting)
    interests = extract_interests(targeting)
    age = extract_age_range(targeting)

    # Simplifica localização
    if ',' in location:
        location = location.split(',')[0]

    return f"{location} ({age}) │ {interests} │ {ad_count} criativos"


def generate_ad_name(ad: dict, creative_idx: int) -> str:
    """
    Gera nome: ID | Formato | CPC
    """
    creative = ad.get('creative', {})
    creative_id = creative.get('id', f'C{creative_idx:02d}')

    # Formato
    formato = detect_creative_format(creative)

    # CPC
    insights_data = ad.get('insights', {}).get('data', [])
    insights = insights_data[0] if insights_data else {}
    cpc = format_cpc(insights)

    return f"ID{creative_id[-6:]} │ {formato} │ {cpc}"


def update_name(object_id: str, new_name: str) -> bool:
    """Atualiza nome de qualquer objeto (campaign/adset/ad)"""
    url = f"{BASE_URL}/{object_id}"
    data = {'name': new_name}

    result = api_post(url, data)
    return result.get('success', False)


def main():
    print("🔍 Buscando campanhas ativas...\n")

    campaigns = get_campaigns()

    if not campaigns:
        print("❌ Nenhuma campanha ativa encontrada")
        return

    print(f"✅ {len(campaigns)} campanha(s) encontrada(s)\n")

    for campaign in campaigns:
        print("=" * 100)
        print(f"\n📊 CAMPANHA ATUAL: {campaign['name']}")
        print(f"   ID: {campaign['id']}\n")

        # Buscar adsets
        adsets = get_adsets(campaign['id'])

        # Buscar todos os ads
        all_ads_by_adset = {}
        total_ads = 0

        for adset in adsets:
            ads = get_ads(adset['id'])
            all_ads_by_adset[adset['id']] = ads
            total_ads += len(ads)

        print(f"   📁 {len(adsets)} AdSet(s)")
        print(f"   🎨 {total_ads} Criativo(s) total\n")

        # Gerar novos nomes
        new_campaign_name = generate_campaign_name(campaign)

        print("🎯 NOVOS NOMES:\n")
        print(f"📊 Campanha:")
        print(f"   ❌ Antes: {campaign['name']}")
        print(f"   ✅ Depois: {new_campaign_name}\n")

        adset_renames = {}
        ad_renames = {}

        for adset in adsets:
            ads = all_ads_by_adset.get(adset['id'], [])
            new_adset_name = generate_adset_name(adset, len(ads))
            adset_renames[adset['id']] = new_adset_name

            print(f"📁 AdSet:")
            print(f"   ❌ Antes: {adset['name']}")
            print(f"   ✅ Depois: {new_adset_name}\n")

            for idx, ad in enumerate(ads, 1):
                new_ad_name = generate_ad_name(ad, idx)
                ad_renames[ad['id']] = new_ad_name

                print(f"   🎨 Criativo {idx}:")
                print(f"      ❌ Antes: {ad['name']}")
                print(f"      ✅ Depois: {new_ad_name}")

            print()

        # Aplicar alterações
        print("=" * 100)
        print("\n🚀 Aplicando alterações...\n")

        try:
            # Campanha
            if update_name(campaign['id'], new_campaign_name):
                print(f"✅ Campanha renomeada")

            # Adsets
            for adset_id, new_name in adset_renames.items():
                if update_name(adset_id, new_name):
                    print(f"✅ AdSet renomeado")

            # Ads
            for ad_id, new_name in ad_renames.items():
                if update_name(ad_id, new_name):
                    print(f"✅ Criativo renomeado")

            print(f"\n🎉 Concluído! {1 + len(adset_renames) + len(ad_renames)} itens atualizados\n")

        except Exception as e:
            print(f"\n❌ Erro ao aplicar alterações: {e}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
