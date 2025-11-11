#!/usr/bin/env python3
"""
Busca métricas detalhadas de campanhas Meta Ads e retorna dados estruturados.
"""

import requests
import json
import sys
from datetime import datetime

ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"
AD_ACCOUNT_ID = "act_1050347575979650"
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def fetch_campaign_metrics(campaign_id=None):
    """
    Busca métricas completas de uma campanha específica ou todas as ativas.

    Args:
        campaign_id (str, optional): ID da campanha. Se None, busca todas as ativas.

    Returns:
        dict: Dados estruturados com campanha, adsets e anúncios
    """

    if campaign_id:
        # Buscar campanha específica
        url = f"{BASE_URL}/{campaign_id}"
        params = {
            'access_token': ACCESS_TOKEN,
            'fields': 'id,name,objective,status,effective_status,insights.date_preset(last_30d){spend,impressions,reach,clicks,cpc,cpm,ctr,frequency,actions,cost_per_action_type}'
        }
        campaign = requests.get(url, params=params).json()
        campaigns = [campaign]
    else:
        # Buscar todas as campanhas ativas
        url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
        params = {
            'access_token': ACCESS_TOKEN,
            'fields': 'id,name,objective,status,effective_status,insights.date_preset(last_30d){spend,impressions,reach,clicks,cpc,cpm,ctr,frequency,actions,cost_per_action_type}',
            'filtering': '[{"field":"effective_status","operator":"IN","value":["ACTIVE"]}]',
            'limit': 100
        }
        campaigns = requests.get(url, params=params).json().get('data', [])

    if not campaigns:
        return {"error": "Nenhuma campanha encontrada"}

    # Processar cada campanha
    result = []

    for campaign in campaigns:
        campaign_data = {
            'campaign': campaign,
            'adsets': [],
            'ads': []
        }

        # Buscar adsets
        url_adsets = f"{BASE_URL}/{campaign['id']}/adsets"
        params_adsets = {
            'access_token': ACCESS_TOKEN,
            'fields': 'id,name,targeting,insights.date_preset(last_30d){spend,impressions,reach,clicks,cpc,ctr,frequency,actions,cost_per_action_type}'
        }
        adsets = requests.get(url_adsets, params=params_adsets).json().get('data', [])
        campaign_data['adsets'] = adsets

        # Buscar anúncios de cada adset
        for adset in adsets:
            url_ads = f"{BASE_URL}/{adset['id']}/ads"
            params_ads = {
                'access_token': ACCESS_TOKEN,
                'fields': 'id,name,creative{title,body,image_url,video_id},insights.date_preset(last_30d){spend,impressions,clicks,cpc,ctr,actions,cost_per_action_type}'
            }
            ads = requests.get(url_ads, params=ads).json().get('data', [])
            campaign_data['ads'].extend(ads)

        result.append(campaign_data)

    return result

def extract_key_metrics(campaign_data):
    """
    Extrai métricas-chave de uma campanha.

    Args:
        campaign_data (dict): Dados da campanha

    Returns:
        dict: Métricas-chave formatadas
    """
    campaign = campaign_data['campaign']
    insights = campaign.get('insights', {}).get('data', [])

    if not insights:
        return None

    data = insights[0]

    # Extrair conversas/leads
    actions = data.get('actions', [])
    conversas = 0
    leads = 0

    for action in actions:
        if 'messaging_conversation_started' in action.get('action_type', ''):
            conversas = int(action.get('value', 0))
        elif 'lead' in action.get('action_type', ''):
            leads += int(action.get('value', 0))

    # Calcular custo por conversão
    cost_per_actions = data.get('cost_per_action_type', [])
    cpl = 0
    for cpa in cost_per_actions:
        if 'messaging_conversation_started' in cpa.get('action_type', '') or 'lead' in cpa.get('action_type', ''):
            cpl = float(cpa.get('value', 0))
            break

    # Se não encontrou CPA, calcular manualmente
    total_conversoes = conversas or leads
    if not cpl and total_conversoes > 0:
        cpl = float(data.get('spend', 0)) / total_conversoes

    return {
        'campaign_name': campaign.get('name'),
        'campaign_id': campaign.get('id'),
        'objective': campaign.get('objective'),
        'spend': float(data.get('spend', 0)),
        'impressions': int(data.get('impressions', 0)),
        'reach': int(data.get('reach', 0)),
        'clicks': int(data.get('clicks', 0)),
        'cpc': float(data.get('cpc', 0)),
        'cpm': float(data.get('cpm', 0)),
        'ctr': float(data.get('ctr', 0)),
        'frequency': float(data.get('frequency', 0)),
        'conversas': conversas,
        'leads': leads,
        'total_conversoes': total_conversoes,
        'custo_conversao': round(cpl, 2),
        'adsets_count': len(campaign_data['adsets']),
        'ads_count': len(campaign_data['ads'])
    }

def format_text_summary(metrics):
    """
    Formata um resumo em texto das métricas.

    Args:
        metrics (dict): Métricas-chave

    Returns:
        str: Resumo formatado
    """
    summary = f"""
📊 RESUMO DA CAMPANHA: {metrics['campaign_name']}
{'=' * 80}

💰 INVESTIMENTO E RESULTADOS:
   Gasto Total (30d): R$ {metrics['spend']:.2f}
   Conversas WhatsApp: {metrics['conversas']}
   Leads Gerados: {metrics['leads']}
   Total de Conversões: {metrics['total_conversoes']}
   Custo por Conversão: R$ {metrics['custo_conversao']:.2f}

📈 PERFORMANCE:
   Impressões: {metrics['impressions']:,}
   Alcance: {metrics['reach']:,}
   Cliques: {metrics['clicks']:,}
   CPC (Custo por Clique): R$ {metrics['cpc']:.2f}
   CTR (Click-Through Rate): {metrics['ctr']:.2f}%
   CPM (Custo por Mil): R$ {metrics['cpm']:.2f}
   Frequência: {metrics['frequency']:.2f}

🎯 ESTRUTURA:
   Conjuntos de Anúncios: {metrics['adsets_count']}
   Anúncios Ativos: {metrics['ads_count']}

📊 ANÁLISE HORMOZI:
"""

    # Análise CTR
    if metrics['ctr'] >= 5:
        summary += "   ✅ CTR EXCELENTE (5%+) - Hook e copy funcionam muito bem\n"
    elif metrics['ctr'] >= 3:
        summary += "   ✅ CTR BOM (3-5%) - Hook funciona, pode melhorar\n"
    elif metrics['ctr'] >= 1.5:
        summary += "   ⚠️ CTR MÉDIO (1.5-3%) - Hook precisa de ajustes\n"
    else:
        summary += "   ❌ CTR BAIXO (<1.5%) - Hook não funciona, refazer criativo\n"

    # Análise Custo/Conversão
    if metrics['custo_conversao'] > 0:
        if metrics['custo_conversao'] <= 5:
            summary += f"   ✅ CUSTO/CONVERSÃO ÓTIMO (R$ {metrics['custo_conversao']:.2f}) - Muito competitivo\n"
        elif metrics['custo_conversao'] <= 10:
            summary += f"   ✅ CUSTO/CONVERSÃO BOM (R$ {metrics['custo_conversao']:.2f}) - Aceitável\n"
        elif metrics['custo_conversao'] <= 20:
            summary += f"   ⚠️ CUSTO/CONVERSÃO ALTO (R$ {metrics['custo_conversao']:.2f}) - Pode melhorar\n"
        else:
            summary += f"   ❌ CUSTO/CONVERSÃO CRÍTICO (R$ {metrics['custo_conversao']:.2f}) - Revisar estratégia\n"

    # Análise Frequência
    if metrics['frequency'] < 2:
        summary += f"   ✅ FREQUÊNCIA SAUDÁVEL ({metrics['frequency']:.2f}) - Audiência fresca\n"
    elif metrics['frequency'] < 3.5:
        summary += f"   ✅ FREQUÊNCIA BOA ({metrics['frequency']:.2f}) - Audiência ainda boa\n"
    elif metrics['frequency'] < 5:
        summary += f"   ⚠️ FREQUÊNCIA ALTA ({metrics['frequency']:.2f}) - Monitorar saturação\n"
    else:
        summary += f"   ❌ FREQUÊNCIA CRÍTICA ({metrics['frequency']:.2f}) - Audiência saturada\n"

    # Análise Volume
    if metrics['total_conversoes'] >= 10:
        summary += f"   ✅ VOLUME VALIDADO ({metrics['total_conversoes']} conversões) - Pode escalar\n"
    elif metrics['total_conversoes'] >= 5:
        summary += f"   ⚠️ VOLUME BAIXO ({metrics['total_conversoes']} conversões) - Aguardar validação\n"
    else:
        summary += f"   ❌ VOLUME INSUFICIENTE ({metrics['total_conversoes']} conversões) - Não validado\n"

    summary += "\n" + "=" * 80 + "\n"

    return summary

if __name__ == "__main__":
    # Aceita campaign_id como argumento opcional
    campaign_id = sys.argv[1] if len(sys.argv) > 1 else None

    # Buscar dados
    data = fetch_campaign_metrics(campaign_id)

    if isinstance(data, dict) and 'error' in data:
        print(json.dumps(data))
        sys.exit(1)

    # Processar primeira campanha
    campaign_data = data[0] if isinstance(data, list) else data
    metrics = extract_key_metrics(campaign_data)

    # Imprimir resumo em texto
    print(format_text_summary(metrics))

    # Salvar JSON completo para uso posterior
    output = {
        'metrics': metrics,
        'raw_data': campaign_data
    }

    print("\n📁 JSON completo salvo em /tmp/meta_ads_data.json")
    with open('/tmp/meta_ads_data.json', 'w') as f:
        json.dumps(output, f, indent=2, ensure_ascii=False)
