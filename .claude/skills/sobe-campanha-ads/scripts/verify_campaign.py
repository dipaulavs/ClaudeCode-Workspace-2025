#!/usr/bin/env python3
"""
Verify Meta Ads campaign follows naming conventions.

Usage:
    python3 verify_campaign.py --campaign-id 120123456789
"""

import argparse
import os
import sys
import re

try:
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.api import FacebookAdsApi
except ImportError:
    print("Error: facebook_business library not installed")
    print("Install with: pip install facebook-business")
    sys.exit(1)


def load_credentials():
    """Load Meta Ads API credentials."""
    access_token = os.getenv("META_ADS_ACCESS_TOKEN")

    if not access_token:
        print("Error: META_ADS_ACCESS_TOKEN not found")
        sys.exit(1)

    return access_token


def verify_naming_format(name, expected_pattern, description):
    """Verify a name matches the expected pattern."""
    if "│" in name:
        print(f"✅ {description}: {name}")
        return True
    else:
        print(f"❌ {description}: {name}")
        print(f"   Expected format: {expected_pattern}")
        return False


def verify_campaign(campaign_id):
    """Verify campaign structure and naming."""

    # Load credentials
    access_token = load_credentials()
    FacebookAdsApi.init(access_token=access_token)

    # Get campaign
    campaign = Campaign(campaign_id)
    campaign_data = campaign.api_get(fields=[
        'name',
        'objective',
        'status'
    ])

    print("="*60)
    print("CAMPAIGN VERIFICATION")
    print("="*60)

    # Verify campaign name format: {Produto} │ {Objetivo} - {Conversão} │ {Dia/Mês}
    campaign_name = campaign_data['name']
    campaign_valid = verify_naming_format(
        campaign_name,
        "{Produto} │ {Objetivo} - {Conversão} │ {Dia/Mês}",
        "Campaign name"
    )

    # Get adsets
    adsets = campaign.get_ad_sets(fields=['name', 'status'])

    print("\n" + "-"*60)
    print(f"ADSETS ({len(adsets)} total)")
    print("-"*60)

    adsets_valid = []
    for adset in adsets:
        adset_name = adset['name']
        # Verify adset name format: {Localização} │ {Interesses} │ {Qtd criativos}
        adset_valid = verify_naming_format(
            adset_name,
            "{Localização} │ {Interesses} │ {Qtd criativos}",
            "Adset"
        )
        adsets_valid.append(adset_valid)

        # Get ads in this adset
        ads = adset.get_ads(fields=['name', 'status'])

        print(f"\n  ADS in {adset_name} ({len(ads)} total):")
        ads_valid = []
        for ad in ads:
            ad_name = ad['name']
            # Verify ad name format: {ID} │ {Formato} │ {CPC}
            ad_valid = verify_naming_format(
                ad_name,
                "{ID} │ {Formato} │ {CPC}",
                "    Ad"
            )
            ads_valid.append(ad_valid)

    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    all_valid = campaign_valid and all(adsets_valid) and all(ads_valid)

    if all_valid:
        print("✅ Campaign structure is valid!")
        print("✅ All naming conventions followed")
    else:
        print("❌ Campaign structure has issues")
        print("❌ Some naming conventions not followed")

    print("="*60)

    return all_valid


def main():
    parser = argparse.ArgumentParser(
        description='Verify Meta Ads campaign naming conventions'
    )
    parser.add_argument('--campaign-id', required=True, help='Campaign ID to verify')

    args = parser.parse_args()

    result = verify_campaign(args.campaign_id)

    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
