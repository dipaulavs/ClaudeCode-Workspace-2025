#!/usr/bin/env python3
"""
Configure Meta Ads API credentials.

Usage:
    python3 configure_meta_ads.py
"""

import os
import sys


def configure_credentials():
    """Interactive script to configure Meta Ads credentials."""

    print("="*60)
    print("META ADS API CONFIGURATION")
    print("="*60)

    print("\nTo use the Meta Marketing API, you need:")
    print("1. Access Token - from Meta for Developers")
    print("2. Ad Account ID - your Meta Ads account (format: act_XXXXXXXXXX)")
    print("3. Page ID - your Facebook Page ID (optional)")
    print("4. Link URL - default link for ads (optional)")

    print("\n" + "-"*60)
    print("GETTING YOUR CREDENTIALS")
    print("-"*60)

    print("\n1. Access Token:")
    print("   - Go to: https://developers.facebook.com/tools/explorer/")
    print("   - Select your app")
    print("   - Generate token with these permissions:")
    print("     - ads_management")
    print("     - ads_read")
    print("     - business_management")

    print("\n2. Ad Account ID:")
    print("   - Go to: https://business.facebook.com/adsmanager/")
    print("   - Find your account ID in the URL or settings")
    print("   - Format: act_XXXXXXXXXX")

    print("\n3. Page ID:")
    print("   - Go to your Facebook Page")
    print("   - Settings → Page Info → Page ID")

    print("\n" + "-"*60)

    # Collect credentials
    access_token = input("\nEnter your Access Token: ").strip()
    account_id = input("Enter your Ad Account ID (act_XXXXXXXXXX): ").strip()
    page_id = input("Enter your Page ID (optional, press Enter to skip): ").strip()
    link_url = input("Enter default link URL (optional, press Enter to skip): ").strip()

    # Validate
    if not access_token:
        print("Error: Access Token is required")
        sys.exit(1)

    if not account_id:
        print("Error: Ad Account ID is required")
        sys.exit(1)

    if not account_id.startswith('act_'):
        print("Warning: Ad Account ID should start with 'act_'")
        print(f"Formatting as: act_{account_id}")
        account_id = f"act_{account_id}"

    # Save to environment (shell profile)
    shell_profile = os.path.expanduser("~/.zshrc")  # or ~/.bashrc

    print("\n" + "-"*60)
    print("SAVING CREDENTIALS")
    print("-"*60)

    env_lines = [
        f'\nexport META_ADS_ACCESS_TOKEN="{access_token}"',
        f'export META_ADS_ACCOUNT_ID="{account_id}"'
    ]

    if page_id:
        env_lines.append(f'export META_PAGE_ID="{page_id}"')

    if link_url:
        env_lines.append(f'export META_ADS_LINK_URL="{link_url}"')

    print(f"\nAdding credentials to {shell_profile}:")
    for line in env_lines:
        print(f"  {line.strip()}")

    # Append to shell profile
    with open(shell_profile, 'a') as f:
        f.write('\n# Meta Ads API credentials\n')
        for line in env_lines:
            f.write(line + '\n')

    print("\n✅ Credentials saved!")
    print("\nTo use them now, run:")
    print(f"  source {shell_profile}")

    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)

    print("\n1. Reload your shell:")
    print(f"   source {shell_profile}")

    print("\n2. Test your credentials:")
    print("   python3 scripts/create_campaign.py --help")

    print("\n3. Create your first campaign:")
    print("   python3 scripts/create_campaign.py \\")
    print("       --product-type \"lote\" \\")
    print("       --strategy \"engajamento para WhatsApp\" \\")
    print("       --copy \"copy.txt\" \\")
    print("       --creatives \"url1,url2,url3\" \\")
    print("       --location \"SP Capital\" \\")
    print("       --interests \"imóveis+investimento\" \\")
    print("       --date \"15/01\"")

    print("\n" + "="*60)


if __name__ == '__main__':
    configure_credentials()
