#!/usr/bin/env python3
"""
Template: Criar Campanha Meta Ads

Uso:
    python3 scripts/meta-ads/create_campaign.py --name "Minha Campanha" --objective OUTCOME_TRAFFIC
    python3 scripts/meta-ads/create_campaign.py -n "Venda Casa" -o OUTCOME_LEADS -d 20.0 -s ACTIVE -c HOUSING
"""

import sys
import argparse
from pathlib import Path

# Adiciona path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.meta_ads_campaigns import MetaAdsCampaigns

def create_campaign(name: str, objective: str, daily_budget: float = 10.0,
                   status: str = "PAUSED", special_category: str = "NONE"):
    """
    Cria campanha Meta Ads

    Args:
        name: Nome da campanha
        objective: Objetivo da campanha
        daily_budget: Orçamento diário em USD
        status: Status inicial (ACTIVE ou PAUSED)
        special_category: Categoria especial (HOUSING, CREDIT, EMPLOYMENT ou NONE)

    Returns:
        Campaign ID
    """
    # Inicializa API
    mgr = MetaAdsCampaigns()

    # Define special_ad_categories
    special_ads = [] if special_category == "NONE" else [special_category]

    # Cria campanha
    campaign_id = mgr.create_campaign(
        name=name,
        objective=objective,
        daily_budget=daily_budget,
        status=status,
        special_ad_categories=special_ads
    )

    return campaign_id

def main():
    parser = argparse.ArgumentParser(description='Criar campanha Meta Ads')

    parser.add_argument('--name', '-n', required=True,
                       help='Nome da campanha')
    parser.add_argument('--objective', '-o', required=True,
                       choices=['OUTCOME_TRAFFIC', 'OUTCOME_LEADS', 'OUTCOME_SALES',
                               'OUTCOME_AWARENESS', 'OUTCOME_ENGAGEMENT'],
                       help='Objetivo da campanha')
    parser.add_argument('--daily-budget', '-d', type=float, default=10.0,
                       help='Orçamento diário em USD (padrão: 10.0)')
    parser.add_argument('--status', '-s', default='PAUSED',
                       choices=['ACTIVE', 'PAUSED'],
                       help='Status inicial (padrão: PAUSED)')
    parser.add_argument('--special-category', '-c', default='NONE',
                       choices=['HOUSING', 'CREDIT', 'EMPLOYMENT', 'NONE'],
                       help='Categoria especial (padrão: NONE)')

    args = parser.parse_args()

    # Mensagem de início
    category_text = f" [{args.special_category}]" if args.special_category != "NONE" else ""
    print(f"📢 Criando campanha '{args.name}'{category_text}...")
    print(f"   Objetivo: {args.objective}")
    print(f"   Orçamento: ${args.daily_budget}/dia")
    print(f"   Status: {args.status}")

    try:
        campaign_id = create_campaign(
            args.name,
            args.objective,
            args.daily_budget,
            args.status,
            args.special_category
        )

        print(f"\n✅ Campanha criada com sucesso!")
        print(f"   Campaign ID: {campaign_id}")
        print(f"   Nome: {args.name}")
        print(f"   Status: {args.status}")

        if args.status == "PAUSED":
            print(f"\n💡 Para ativar: python3 tools/meta_ads_campaigns.py update {campaign_id} --status ACTIVE")

        return campaign_id
    except Exception as e:
        print(f"❌ Erro ao criar campanha: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
