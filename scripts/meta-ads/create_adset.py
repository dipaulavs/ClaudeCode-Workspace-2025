#!/usr/bin/env python3
"""
Template: Criar Ad Set Meta Ads

Uso:
    python3 scripts/meta-ads/create_adset.py --campaign-id 123456789 --name "Meu Ad Set"
    python3 scripts/meta-ads/create_adset.py -c 123456789 -n "Ad Set Brasil" -co BR -amin 30 -amax 60
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.meta_ads_adsets import MetaAdsAdSets

def create_adset(campaign_id: str, name: str, daily_budget: float = None,
                optimization_goal: str = "LINK_CLICKS", country: str = "BR",
                age_min: int = 25, age_max: int = 55, status: str = "PAUSED"):
    """
    Cria ad set Meta Ads

    Args:
        campaign_id: ID da campanha pai
        name: Nome do ad set
        daily_budget: Orçamento diário em USD (opcional)
        optimization_goal: Meta de otimização
        country: País de targeting (código ISO)
        age_min: Idade mínima
        age_max: Idade máxima
        status: Status inicial

    Returns:
        Ad Set ID
    """
    mgr = MetaAdsAdSets()

    # Define targeting
    targeting = {
        "geo_locations": {"countries": [country]},
        "age_min": age_min,
        "age_max": age_max
    }

    # Cria ad set
    adset_id = mgr.create_adset(
        campaign_id=campaign_id,
        name=name,
        daily_budget=daily_budget,
        optimization_goal=optimization_goal,
        targeting=targeting,
        status=status
    )

    return adset_id

def main():
    parser = argparse.ArgumentParser(description='Criar ad set Meta Ads')

    parser.add_argument('--campaign-id', '-c', required=True,
                       help='ID da campanha pai')
    parser.add_argument('--name', '-n', required=True,
                       help='Nome do ad set')
    parser.add_argument('--daily-budget', '-d', type=float,
                       help='Orçamento diário em USD (se campanha não tiver)')
    parser.add_argument('--optimization-goal', '-g', default='LINK_CLICKS',
                       choices=['LINK_CLICKS', 'IMPRESSIONS', 'REACH', 'LANDING_PAGE_VIEWS'],
                       help='Meta de otimização (padrão: LINK_CLICKS)')
    parser.add_argument('--country', '-co', default='BR',
                       help='País de targeting (padrão: BR)')
    parser.add_argument('--age-min', '-amin', type=int, default=25,
                       help='Idade mínima (padrão: 25)')
    parser.add_argument('--age-max', '-amax', type=int, default=55,
                       help='Idade máxima (padrão: 55)')
    parser.add_argument('--status', '-s', default='PAUSED',
                       choices=['ACTIVE', 'PAUSED'],
                       help='Status inicial (padrão: PAUSED)')

    args = parser.parse_args()

    # Mensagem de início
    budget_text = f"${args.daily_budget}/dia" if args.daily_budget else "Orçamento da campanha"
    print(f"🎯 Criando ad set '{args.name}'...")
    print(f"   Campaign ID: {args.campaign_id}")
    print(f"   Targeting: {args.country}, {args.age_min}-{args.age_max} anos")
    print(f"   Orçamento: {budget_text}")
    print(f"   Status: {args.status}")

    try:
        adset_id = create_adset(
            args.campaign_id,
            args.name,
            args.daily_budget,
            args.optimization_goal,
            args.country,
            args.age_min,
            args.age_max,
            args.status
        )

        print(f"\n✅ Ad set criado com sucesso!")
        print(f"   Ad Set ID: {adset_id}")
        print(f"   Nome: {args.name}")
        print(f"   Status: {args.status}")

        if args.status == "PAUSED":
            print(f"\n💡 Próximo passo: Criar anúncio com python3 scripts/meta-ads/create_ad.py --adset-id {adset_id}")

        return adset_id
    except Exception as e:
        print(f"❌ Erro ao criar ad set: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
