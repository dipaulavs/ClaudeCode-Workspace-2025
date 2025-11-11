#!/usr/bin/env python3
"""
Renomeia campanhas Meta Ads com MÉTRICAS REAIS
Busca dados reais antes de renomear:
- CPC real do criativo
- Formato real (reels/carrossel/único)
- Localização e interesses reais
- Quantidade real de criativos
"""

import requests
from datetime import datetime
from typing import Dict, List, Optional

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def api_get(url: str, params: dict) -> dict:
    """Requisição GET com tratamento de erro"""
    params['access_token'] = ACCESS_TOKEN
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def api_post(url: str, data: dict) -> dict:
    """Requisição POST com tratamento de erro"""
    data['access_token'] = ACCESS_TOKEN
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def get_campaigns() -> List[Dict]:
    """Lista todas as campanhas com insights"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"

    params = {
        'fields': 'id,name,status,effective_status,objective,created_time',
        'limit': 100
    }

    data = api_get(url, params)
    return data.get('data', [])


def get_adsets_with_metrics(campaign_id: str) -> List[Dict]:
    """Busca adsets com targeting E métricas reais"""
    url = f"{BASE_URL}/{campaign_id}/adsets"

    params = {
        'fields': 'id,name,targeting,insights.date_preset(maximum){cpc,cpm,spend,clicks,impressions}'
    }

    data = api_get(url, params)
    return data.get('data', [])


def get_ads_with_metrics(adset_id: str) -> List[Dict]:
    """Busca ads com creative E métricas reais"""
    url = f"{BASE_URL}/{adset_id}/ads"

    params = {
        'fields': 'id,name,creative{id,name,title,body,object_story_spec,image_url,video_id,thumbnail_url},insights.date_preset(maximum){cpc,cpm,spend,clicks,impressions,reach}'
    }

    data = api_get(url, params)
    return data.get('data', [])


def get_creative_details(creative_id: str) -> Optional[Dict]:
    """Busca detalhes completos do criativo"""
    url = f"{BASE_URL}/{creative_id}"

    params = {
        'fields': 'id,name,title,body,object_story_spec,image_url,video_id,thumbnail_url,effective_object_story_id'
    }

    try:
        return api_get(url, params)
    except:
        return None


def extract_location(targeting: dict) -> str:
    """Extrai localização principal"""
    geo = targeting.get('geo_locations', {})

    # Cidades
    if 'cities' in geo and geo['cities']:
        city = geo['cities'][0].get('name', '')
        # Remove estado se tiver vírgula
        if ',' in city:
            city = city.split(',')[0].strip()
        return city

    # Regiões
    if 'regions' in geo and geo['regions']:
        region = geo['regions'][0].get('name', '')
        if ',' in region:
            region = region.split(',')[0].strip()
        return region

    # País
    if 'countries' in geo and geo['countries']:
        return geo['countries'][0]

    return 'BR'


def extract_interests(targeting: dict) -> str:
    """Extrai interesses principais"""
    interests = []

    # Flexible spec (interesses principais)
    if 'flexible_spec' in targeting:
        for spec in targeting['flexible_spec']:
            if 'interests' in spec:
                for interest in spec['interests']:
                    name = interest.get('name', '')
                    if name:
                        # Abrevia interesses longos
                        short_name = name[:12] if len(name) > 12 else name
                        interests.append(short_name)
                        if len(interests) >= 2:
                            break
            if len(interests) >= 2:
                break

    # Narrow targeting (interesses mais específicos)
    if not interests and 'narrow_targeting' in targeting:
        for spec in targeting['narrow_targeting']:
            if 'interests' in spec:
                for interest in spec['interests'][:1]:
                    name = interest.get('name', '')
                    if name:
                        interests.append(name[:12])

    if interests:
        return ' + '.join(interests)

    return 'Broad'


def detect_creative_format(creative: dict) -> str:
    """Detecta formato do criativo analisando object_story_spec"""

    obj_story = creative.get('object_story_spec', {})

    # Link data (formato mais comum)
    if 'link_data' in obj_story:
        link_data = obj_story['link_data']

        # Carrossel (tem child_attachments)
        if 'child_attachments' in link_data and link_data['child_attachments']:
            count = len(link_data['child_attachments'])
            return f"Carrossel ({count})"

        # Vídeo/Reels
        if 'video_id' in link_data or link_data.get('call_to_action', {}).get('type') == 'WATCH_VIDEO':
            return "Reels"

    # Video data direto
    if 'video_data' in obj_story:
        return "Reels"

    # Tem video_id ou thumbnail
    if creative.get('video_id') or creative.get('thumbnail_url'):
        return "Reels"

    # Imagem única
    return "Único"


def calculate_real_cpc(insights_data: list) -> str:
    """Calcula CPC real dos insights"""
    if not insights_data:
        return "Sem dados"

    # Pega os insights mais recentes
    insights = insights_data[0] if isinstance(insights_data, list) else insights_data

    # CPC direto
    if 'cpc' in insights and insights['cpc']:
        cpc = float(insights['cpc'])
        return f"R$ {cpc:.2f}"

    # Calcula manualmente: spend / clicks
    spend = insights.get('spend')
    clicks = insights.get('clicks')

    if spend and clicks:
        try:
            cpc = float(spend) / int(clicks)
            return f"R$ {cpc:.2f}"
        except (ValueError, ZeroDivisionError):
            pass

    # Se tem spend mas sem clicks
    if spend and float(spend) > 0:
        return "Sem cliques"

    return "Sem dados"


def generate_campaign_name(campaign: dict) -> str:
    """
    Gera: Imovel X │ engajamento - Wpp │ dia/mes
    """
    # Data
    created = campaign.get('created_time', '')
    if created:
        date_obj = datetime.strptime(created[:10], '%Y-%m-%d')
        date_str = date_obj.strftime('%d/%m')
    else:
        date_str = datetime.now().strftime('%d/%m')

    # Tipo de engajamento
    objective = campaign.get('objective', '')
    engagement_map = {
        'OUTCOME_LEADS': 'Leads - Wpp',
        'OUTCOME_TRAFFIC': 'Tráfego - Wpp',
        'OUTCOME_ENGAGEMENT': 'Engajamento - Wpp',
        'OUTCOME_AWARENESS': 'Alcance - Wpp',
        'OUTCOME_SALES': 'Vendas - Wpp'
    }
    engagement = engagement_map.get(objective, 'Engajamento - Wpp')

    # Nome do imóvel (extrai do nome atual)
    old_name = campaign.get('name', '')

    # Procura palavras-chave
    keywords = ['apartamento', 'casa', 'imovel', 'cobertura', 'lote', 'terreno', 'sala', 'galpão']
    imovel = 'Imóvel Premium'

    for word in old_name.split():
        if word.lower() in keywords:
            imovel = word.capitalize()
            break

    return f"{imovel} │ {engagement} │ {date_str}"


def generate_adset_name(adset: dict, ad_count: int) -> str:
    """
    Gera: Localização │ Interesses │ qtd criativo
    """
    targeting = adset.get('targeting', {})

    location = extract_location(targeting)
    interests = extract_interests(targeting)

    age_min = targeting.get('age_min', 18)
    age_max = targeting.get('age_max', 65)

    return f"{location} ({age_min}-{age_max}) │ {interests} │ {ad_count} criativos"


def generate_ad_name(ad: dict, creative_idx: int) -> str:
    """
    Gera: ID │ Formato │ CPC
    """
    creative = ad.get('creative', {})
    creative_id = creative.get('id', f'C{creative_idx:03d}')

    # Formato
    formato = detect_creative_format(creative)

    # CPC real
    insights_data = ad.get('insights', {}).get('data', [])
    cpc = calculate_real_cpc(insights_data)

    # Usa últimos 6 dígitos do ID
    short_id = creative_id[-6:] if len(creative_id) > 6 else creative_id

    return f"ID{short_id} │ {formato} │ {cpc}"


def update_name(object_id: str, new_name: str) -> bool:
    """Atualiza nome via API"""
    url = f"{BASE_URL}/{object_id}"
    data = {'name': new_name}

    result = api_post(url, data)
    return result.get('success', False)


def main():
    print("\n🔍 Buscando campanhas e MÉTRICAS REAIS...\n")

    campaigns = get_campaigns()

    if not campaigns:
        print("❌ Nenhuma campanha encontrada\n")
        return

    # Filtra campanhas que ainda não foram renomeadas
    to_rename = [c for c in campaigns if '│' not in c['name']]

    if not to_rename:
        print("✅ Todas as campanhas já estão com o padrão correto!\n")

        # Mostra as campanhas atuais
        print("📊 CAMPANHAS ATUAIS:\n")
        for c in campaigns:
            status = "🟢" if c.get('effective_status') == 'ACTIVE' else "⏸️"
            print(f"{status} {c['name']}")
        print()
        return

    print(f"📊 {len(to_rename)} campanha(s) para renomear:\n")

    for campaign in to_rename:
        print("=" * 100)
        print(f"\n📌 {campaign['name']}")
        print(f"   ID: {campaign['id']}")
        print(f"   Status: {campaign.get('effective_status', 'UNKNOWN')}\n")

        # Busca adsets com métricas
        print("   🔎 Buscando adsets e métricas...")
        adsets = get_adsets_with_metrics(campaign['id'])

        # Busca ads de cada adset
        all_ads_by_adset = {}
        total_ads = 0

        for adset in adsets:
            ads = get_ads_with_metrics(adset['id'])
            all_ads_by_adset[adset['id']] = ads
            total_ads += len(ads)

        print(f"   ✅ {len(adsets)} AdSet(s) | {total_ads} Criativo(s)\n")

        # Gera novos nomes
        new_campaign_name = generate_campaign_name(campaign)

        print("🎯 NOVOS NOMES (com métricas reais):\n")
        print(f"📊 Campanha:")
        print(f"   ❌ Antes: {campaign['name']}")
        print(f"   ✅ Depois: {new_campaign_name}\n")

        adset_updates = {}
        ad_updates = {}

        for adset in adsets:
            ads = all_ads_by_adset.get(adset['id'], [])
            new_adset_name = generate_adset_name(adset, len(ads))
            adset_updates[adset['id']] = new_adset_name

            print(f"📁 AdSet:")
            print(f"   ❌ Antes: {adset['name']}")
            print(f"   ✅ Depois: {new_adset_name}\n")

            for idx, ad in enumerate(ads, 1):
                new_ad_name = generate_ad_name(ad, idx)
                ad_updates[ad['id']] = new_ad_name

                print(f"   🎨 Criativo {idx}:")
                print(f"      ❌ Antes: {ad['name']}")
                print(f"      ✅ Depois: {new_ad_name}")

            print()

        # Aplica alterações
        print("=" * 100)
        print("\n🚀 Aplicando alterações...\n")

        try:
            # Campanha
            if update_name(campaign['id'], new_campaign_name):
                print(f"✅ Campanha renomeada")

            # Adsets
            for adset_id, new_name in adset_updates.items():
                if update_name(adset_id, new_name):
                    print(f"✅ AdSet renomeado")

            # Ads
            for ad_id, new_name in ad_updates.items():
                if update_name(ad_id, new_name):
                    print(f"✅ Criativo renomeado")

            total_updated = 1 + len(adset_updates) + len(ad_updates)
            print(f"\n🎉 {total_updated} itens atualizados!\n")

        except Exception as e:
            print(f"\n❌ Erro ao aplicar: {e}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
