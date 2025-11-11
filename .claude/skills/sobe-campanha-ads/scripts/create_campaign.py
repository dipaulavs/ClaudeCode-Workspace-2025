#!/usr/bin/env python3
"""
Create Meta Ads campaigns with standardized naming convention.

Usage:
    python3 create_campaign.py \
        --product-type "lote" \
        --strategy "engajamento para WhatsApp" \
        --copy "copy_file.txt" \
        --creatives "url1,url2,url3" \
        --location "SP Capital" \
        --interests "imóveis,investimento" \
        --date "15/01"
"""

import argparse
import os
import sys
from datetime import datetime

try:
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad
    from facebook_business.adobjects.adcreative import AdCreative
    from facebook_business.api import FacebookAdsApi
except ImportError:
    print("Error: facebook_business library not installed")
    print("Install with: pip install facebook-business")
    sys.exit(1)


def load_credentials():
    """Load Meta Ads API credentials from environment or Cofre de APIs."""
    access_token = os.getenv("META_ADS_ACCESS_TOKEN")
    account_id = os.getenv("META_ADS_ACCOUNT_ID")

    if not access_token or not account_id:
        print("Error: Meta Ads credentials not found")
        print("Set environment variables:")
        print("  export META_ADS_ACCESS_TOKEN='your_token'")
        print("  export META_ADS_ACCOUNT_ID='act_your_account_id'")
        sys.exit(1)

    return access_token, account_id


def format_campaign_name(product, objective, conversion, date):
    """Format campaign name: {Produto} │ {Objetivo} - {Conversão} │ {Dia/Mês}"""
    return f"{product} │ {objective} - {conversion} │ {date}"


def format_adset_name(location, interests, creative_count):
    """Format adset name: {Localização} │ {Interesses} │ {Qtd criativos}"""
    return f"{location} │ {interests} │ {creative_count} criativos"


def format_creative_name(creative_id, format_type, cpc="R$-"):
    """Format creative name: {ID} │ {Formato} │ {CPC}"""
    return f"{creative_id:03d} │ {format_type} │ {cpc}"


def detect_creative_format(creative_url):
    """Detect creative format from URL."""
    url_lower = creative_url.lower()
    if "reel" in url_lower or "reels" in url_lower:
        return "reels"
    elif "carousel" in url_lower or "carrossel" in url_lower:
        return "carrossel"
    elif "stories" in url_lower or "story" in url_lower:
        return "stories"
    else:
        return "único"


def create_campaign_structure(
    product_type,
    strategy,
    copy_file,
    creative_urls,
    location,
    interests,
    launch_date
):
    """Create complete Meta Ads campaign structure."""

    # Load credentials
    access_token, account_id = load_credentials()

    # Initialize API
    FacebookAdsApi.init(access_token=access_token)
    account = AdAccount(account_id)

    # Parse strategy to extract objective and conversion
    # Example: "engajamento para WhatsApp" -> objective="engajamento", conversion="Wpp"
    strategy_lower = strategy.lower()
    if "engajamento" in strategy_lower:
        objective = "engajamento"
    elif "conversão" in strategy_lower or "conversao" in strategy_lower:
        objective = "conversão"
    elif "tráfego" in strategy_lower or "trafego" in strategy_lower:
        objective = "tráfego"
    else:
        objective = "engajamento"  # default

    if "whatsapp" in strategy_lower or "wpp" in strategy_lower:
        conversion = "Wpp"
    elif "lead" in strategy_lower:
        conversion = "Lead"
    elif "dm" in strategy_lower:
        conversion = "DM"
    elif "site" in strategy_lower:
        conversion = "Site"
    else:
        conversion = "Wpp"  # default

    # Format campaign name
    campaign_name = format_campaign_name(
        product=product_type,
        objective=objective,
        conversion=conversion,
        date=launch_date
    )

    print(f"Creating campaign: {campaign_name}")

    # Create campaign
    campaign = account.create_campaign(params={
        'name': campaign_name,
        'objective': 'OUTCOME_ENGAGEMENT',  # adjust based on objective
        'status': 'PAUSED',  # start paused for review
        'special_ad_categories': []
    })

    campaign_id = campaign['id']
    print(f"✅ Campaign created: {campaign_id}")

    # Load ad copy
    with open(copy_file, 'r', encoding='utf-8') as f:
        ad_copy = f.read().strip()

    # Parse creative URLs
    creative_url_list = [url.strip() for url in creative_urls.split(',')]
    creative_count = len(creative_url_list)

    # Format adset name
    adset_name = format_adset_name(
        location=location,
        interests=interests,
        creative_count=creative_count
    )

    print(f"Creating adset: {adset_name}")

    # Create adset
    adset = account.create_ad_set(params={
        'name': adset_name,
        'campaign_id': campaign_id,
        'optimization_goal': 'REACH',  # adjust based on strategy
        'billing_event': 'IMPRESSIONS',
        'bid_amount': 100,  # adjust based on budget
        'daily_budget': 5000,  # R$50 in cents, adjust as needed
        'targeting': {
            'geo_locations': {'countries': ['BR']},  # adjust based on location
            'interests': [{'name': interest.strip()} for interest in interests.split('+')]
        },
        'status': 'PAUSED'
    })

    adset_id = adset['id']
    print(f"✅ Adset created: {adset_id}")

    # Create ads for each creative
    ads_created = []
    for idx, creative_url in enumerate(creative_url_list, start=1):
        creative_format = detect_creative_format(creative_url)
        creative_name = format_creative_name(
            creative_id=idx,
            format_type=creative_format,
            cpc="R$-"  # will be updated after campaign runs
        )

        print(f"Creating ad: {creative_name}")

        # Create ad creative
        creative = account.create_ad_creative(params={
            'name': creative_name,
            'object_story_spec': {
                'page_id': os.getenv('META_PAGE_ID', ''),  # get from env
                'link_data': {
                    'image_url': creative_url,
                    'message': ad_copy,
                    'link': os.getenv('META_ADS_LINK_URL', 'https://example.com')
                }
            }
        })

        # Create ad
        ad = account.create_ad(params={
            'name': creative_name,
            'adset_id': adset_id,
            'creative': {'creative_id': creative['id']},
            'status': 'PAUSED'
        })

        ads_created.append({
            'id': ad['id'],
            'name': creative_name
        })

        print(f"✅ Ad created: {creative_name} ({ad['id']})")

    # Summary
    print("\n" + "="*60)
    print("CAMPAIGN CREATED SUCCESSFULLY")
    print("="*60)
    print(f"Campaign: {campaign_name}")
    print(f"Campaign ID: {campaign_id}")
    print(f"Adset: {adset_name}")
    print(f"Ads created: {len(ads_created)}")
    for ad in ads_created:
        print(f"  - {ad['name']}")
    print("="*60)
    print(f"View in Ads Manager: https://business.facebook.com/adsmanager/manage/campaigns?act={account_id.replace('act_', '')}")
    print("\nNote: Campaign is PAUSED. Review and activate when ready.")

    return {
        'campaign_id': campaign_id,
        'campaign_name': campaign_name,
        'adset_id': adset_id,
        'adset_name': adset_name,
        'ads': ads_created
    }


def main():
    parser = argparse.ArgumentParser(
        description='Create Meta Ads campaign with standardized naming'
    )
    parser.add_argument('--product-type', required=True, help='Product type (lote, chácara, etc.)')
    parser.add_argument('--strategy', required=True, help='Campaign strategy')
    parser.add_argument('--copy', required=True, help='Path to ad copy text file')
    parser.add_argument('--creatives', required=True, help='Comma-separated creative URLs')
    parser.add_argument('--location', required=True, help='Geographic location')
    parser.add_argument('--interests', required=True, help='Plus-separated interests')
    parser.add_argument('--date', required=True, help='Launch date (DD/MM format)')

    args = parser.parse_args()

    # Validate copy file exists
    if not os.path.exists(args.copy):
        print(f"Error: Copy file not found: {args.copy}")
        sys.exit(1)

    # Create campaign
    result = create_campaign_structure(
        product_type=args.product_type,
        strategy=args.strategy,
        copy_file=args.copy,
        creative_urls=args.creatives,
        location=args.location,
        interests=args.interests,
        launch_date=args.date
    )

    return result


if __name__ == '__main__':
    main()
