#!/usr/bin/env python3
"""Meta Ads - Gerenciar Ads"""
import requests, sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import meta_ads_config as config

class MetaAdsAds:
    def __init__(self):
        if not config.validate_config():
            sys.exit(1)
        self.access_token = config.ACCESS_TOKEN

    def list_ads(self, adset_id=None, limit=25):
        print("📢 LISTANDO ADS")
        print("=" * 60)
        endpoint = f"{config.ENDPOINTS['adset']}/{adset_id}/ads" if adset_id else config.ENDPOINTS["ads"]
        params = {"fields": "id,name,adset_id,creative,status", "limit": limit, "access_token": self.access_token}

        try:
            resp = requests.get(endpoint, params=params)
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:
                print("📭 Nenhum ad encontrado")
                return []

            print(f"✅ {len(data)} ads:\n")
            for i, a in enumerate(data, 1):
                print(f"[{i}] {a['name']}")
                print(f"    🆔 {a['id']}")
                print(f"    📊 {a['status']}\n")
            return data
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def create_ad(self, adset_id, name, creative_id, status="PAUSED"):
        print(f"🚀 CRIANDO AD: {name}")
        params = {
            "adset_id": adset_id,
            "name": name,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": status,
            "access_token": self.access_token
        }

        try:
            resp = requests.post(config.ENDPOINTS["ads"], params=params)
            resp.raise_for_status()
            ad_id = resp.json().get("id")
            print(f"✅ Ad criado! ID: {ad_id}")
            return ad_id
        except Exception as e:
            print(f"❌ Erro: {e}")
            if hasattr(e, 'response'):
                print(e.response.text)
            return None

    def update_ad(self, ad_id, **kwargs):
        print(f"🔄 ATUALIZANDO AD: {ad_id}")
        params = {"access_token": self.access_token}
        params.update(kwargs)
        try:
            resp = requests.post(f"{config.ENDPOINTS['ad']}/{ad_id}", params=params)
            resp.raise_for_status()
            print("✅ Atualizado!")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    p_list = subparsers.add_parser("list")
    p_list.add_argument("--adset-id")
    p_list.add_argument("--limit", type=int, default=25)

    p_create = subparsers.add_parser("create")
    p_create.add_argument("adset_id")
    p_create.add_argument("name")
    p_create.add_argument("creative_id")
    p_create.add_argument("--status", default="PAUSED")

    p_update = subparsers.add_parser("update")
    p_update.add_argument("ad_id")
    p_update.add_argument("--status")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MetaAdsAds()

    if args.command == "list":
        manager.list_ads(args.adset_id, args.limit)
    elif args.command == "create":
        manager.create_ad(args.adset_id, args.name, args.creative_id, args.status)
    elif args.command == "update":
        manager.update_ad(args.ad_id, status=args.status)

if __name__ == "__main__":
    main()
