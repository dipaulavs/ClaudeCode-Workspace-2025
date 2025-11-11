#!/usr/bin/env python3
"""
Script para listar e editar campanhas Meta Ads
"""

import requests
import json
from typing import Dict, List

# Credenciais
ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def list_campaigns() -> List[Dict]:
    """Lista todas as campanhas ativas"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,objective,created_time,updated_time',
        'effective_status': '["ACTIVE"]'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data.get('data', [])


def list_adsets(campaign_id: str) -> List[Dict]:
    """Lista todos os adsets de uma campanha"""
    url = f"{BASE_URL}/{campaign_id}/adsets"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,targeting,optimization_goal,billing_event,bid_amount,daily_budget',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data.get('data', [])


def list_ads(adset_id: str) -> List[Dict]:
    """Lista todos os anúncios de um adset"""
    url = f"{BASE_URL}/{adset_id}/ads"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,creative',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return data.get('data', [])


def get_creative(creative_id: str) -> Dict:
    """Busca detalhes de um criativo"""
    url = f"{BASE_URL}/{creative_id}"

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,title,body,image_url,object_story_spec',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def update_campaign_name(campaign_id: str, new_name: str) -> bool:
    """Atualiza nome da campanha"""
    url = f"{BASE_URL}/{campaign_id}"

    data = {
        'access_token': ACCESS_TOKEN,
        'name': new_name
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.json().get('success', False)


def update_adset_name(adset_id: str, new_name: str) -> bool:
    """Atualiza nome do adset"""
    url = f"{BASE_URL}/{adset_id}"

    data = {
        'access_token': ACCESS_TOKEN,
        'name': new_name
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.json().get('success', False)


def update_ad_name(ad_id: str, new_name: str) -> bool:
    """Atualiza nome do anúncio"""
    url = f"{BASE_URL}/{ad_id}"

    data = {
        'access_token': ACCESS_TOKEN,
        'name': new_name
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.json().get('success', False)


def extract_targeting_info(adset: Dict) -> str:
    """Extrai informações de segmentação do adset"""
    targeting = adset.get('targeting', {})

    info_parts = []

    # Localização
    if 'geo_locations' in targeting:
        geo = targeting['geo_locations']
        if 'cities' in geo:
            cities = [c.get('name', '') for c in geo['cities']]
            info_parts.append(f"Cities:{','.join(cities[:2])}")
        elif 'regions' in geo:
            regions = [r.get('name', '') for r in geo['regions']]
            info_parts.append(f"Regions:{','.join(regions[:2])}")
        elif 'countries' in geo:
            info_parts.append(f"Country:{','.join(geo['countries'][:2])}")

    # Idade
    if 'age_min' in targeting and 'age_max' in targeting:
        info_parts.append(f"Age:{targeting['age_min']}-{targeting['age_max']}")

    # Gênero
    if 'genders' in targeting:
        gender_map = {1: 'M', 2: 'F'}
        genders = [gender_map.get(g, 'All') for g in targeting['genders']]
        if genders and genders != ['All']:
            info_parts.append(f"Gender:{''.join(genders)}")

    # Interesses
    if 'flexible_spec' in targeting:
        interests = []
        for spec in targeting['flexible_spec']:
            if 'interests' in spec:
                interests.extend([i.get('name', '') for i in spec['interests'][:2]])
        if interests:
            info_parts.append(f"Int:{','.join(interests[:2])}")

    return '_'.join(info_parts) if info_parts else 'Broad'


def generate_smart_names(campaign: Dict, adsets: List[Dict], ads: List[Dict]) -> Dict:
    """Gera nomes inteligentes baseados nas informações extraídas"""

    names = {
        'campaign': {},
        'adsets': {},
        'ads': {}
    }

    # Nome da campanha baseado no objetivo
    objective = campaign.get('objective', 'UNKNOWN')
    objective_map = {
        'OUTCOME_LEADS': 'LeadGen',
        'OUTCOME_TRAFFIC': 'Traffic',
        'OUTCOME_ENGAGEMENT': 'Engagement',
        'OUTCOME_AWARENESS': 'Awareness',
        'OUTCOME_SALES': 'Sales'
    }
    objective_short = objective_map.get(objective, objective[:8])

    campaign_date = campaign.get('created_time', '')[:10].replace('-', '')
    new_campaign_name = f"CA-01_DIP_{objective_short}_{campaign_date}"

    names['campaign'] = {
        'id': campaign['id'],
        'old_name': campaign['name'],
        'new_name': new_campaign_name
    }

    # Nomes dos adsets baseados na segmentação
    for idx, adset in enumerate(adsets, 1):
        targeting_info = extract_targeting_info(adset)
        optimization = adset.get('optimization_goal', 'UNKNOWN')[:8]

        new_adset_name = f"AS{idx:02d}_{targeting_info}_{optimization}"

        names['adsets'][adset['id']] = {
            'id': adset['id'],
            'old_name': adset['name'],
            'new_name': new_adset_name
        }

    # Nomes dos anúncios baseados no criativo
    for idx, ad in enumerate(ads, 1):
        creative_id = ad.get('creative', {}).get('id', '')

        try:
            creative = get_creative(creative_id)
            creative_title = creative.get('title', creative.get('name', ''))[:20]
            creative_title = creative_title.replace(' ', '_')
        except:
            creative_title = 'Creative'

        new_ad_name = f"AD{idx:02d}_{creative_title}"

        names['ads'][ad['id']] = {
            'id': ad['id'],
            'old_name': ad['name'],
            'new_name': new_ad_name,
            'creative_id': creative_id
        }

    return names


def main():
    print("🔍 Buscando campanhas ativas...\n")

    campaigns = list_campaigns()

    if not campaigns:
        print("❌ Nenhuma campanha ativa encontrada")
        return

    print(f"✅ {len(campaigns)} campanha(s) ativa(s) encontrada(s)\n")

    for campaign in campaigns:
        print("=" * 80)
        print(f"📊 CAMPANHA: {campaign['name']}")
        print(f"   ID: {campaign['id']}")
        print(f"   Objetivo: {campaign.get('objective', 'N/A')}")
        print(f"   Status: {campaign.get('status', 'N/A')}")
        print()

        # Buscar adsets
        adsets = list_adsets(campaign['id'])
        print(f"   📁 {len(adsets)} AdSet(s) encontrado(s)")

        for adset in adsets:
            print(f"      → {adset['name']} (ID: {adset['id']})")

        # Buscar ads de cada adset
        all_ads = []
        for adset in adsets:
            ads = list_ads(adset['id'])
            all_ads.extend(ads)
            print(f"   🎨 {len(ads)} Anúncio(s) no AdSet {adset['name']}")
            for ad in ads:
                print(f"      → {ad['name']} (ID: {ad['id']})")

        print()

        # Gerar nomes inteligentes
        print("🤖 GERANDO NOMES INTELIGENTES...\n")
        smart_names = generate_smart_names(campaign, adsets, all_ads)

        # Mostrar sugestões
        print("📝 SUGESTÕES DE NOMES:\n")

        print("Campanha:")
        print(f"   Atual: {smart_names['campaign']['old_name']}")
        print(f"   Novo:  {smart_names['campaign']['new_name']}")
        print()

        print("AdSets:")
        for adset_id, info in smart_names['adsets'].items():
            print(f"   Atual: {info['old_name']}")
            print(f"   Novo:  {info['new_name']}")
            print()

        print("Anúncios:")
        for ad_id, info in smart_names['ads'].items():
            print(f"   Atual: {info['old_name']}")
            print(f"   Novo:  {info['new_name']}")
            print()

        # Confirmar alterações
        print("=" * 80)
        confirm = input("\n✅ Aplicar essas alterações? (s/n): ").lower()

        if confirm == 's':
            print("\n🚀 Aplicando alterações...\n")

            # Atualizar campanha
            if update_campaign_name(campaign['id'], smart_names['campaign']['new_name']):
                print(f"✅ Campanha atualizada: {smart_names['campaign']['new_name']}")

            # Atualizar adsets
            for adset_id, info in smart_names['adsets'].items():
                if update_adset_name(adset_id, info['new_name']):
                    print(f"✅ AdSet atualizado: {info['new_name']}")

            # Atualizar ads
            for ad_id, info in smart_names['ads'].items():
                if update_ad_name(ad_id, info['new_name']):
                    print(f"✅ Anúncio atualizado: {info['new_name']}")

            print("\n🎉 Todas as alterações foram aplicadas com sucesso!")
        else:
            print("\n❌ Operação cancelada")

        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
