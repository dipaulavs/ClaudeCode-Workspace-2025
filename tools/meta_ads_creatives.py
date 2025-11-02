#!/usr/bin/env python3
"""Meta Ads - Gerenciar Criativos"""
import requests, sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import meta_ads_config as config

class MetaAdsCreatives:
    def __init__(self):
        if not config.validate_config():
            sys.exit(1)
        self.access_token = config.ACCESS_TOKEN

    def list_creatives(self, limit=25):
        print("🎨 LISTANDO CRIATIVOS")
        print("=" * 60)
        params = {"fields": "id,name,object_story_spec,image_url,thumbnail_url,title,body,link_url", "limit": limit, "access_token": self.access_token}

        try:
            resp = requests.get(config.ENDPOINTS["adcreatives"], params=params)
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:
                print("📭 Nenhum criativo encontrado")
                return []

            print(f"✅ {len(data)} criativos:\n")
            for i, c in enumerate(data, 1):
                print(f"[{i}] {c.get('name', 'Sem nome')}")
                print(f"    🆔 {c['id']}\n")
            return data
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def create_creative(self, name, page_id, message, link, image_hash=None, call_to_action="LEARN_MORE"):
        print(f"🚀 CRIANDO CRIATIVO: {name}")

        object_story_spec = {
            "page_id": page_id,
            "link_data": {
                "message": message,
                "link": link,
                "call_to_action": {"type": call_to_action}
            }
        }

        if image_hash:
            object_story_spec["link_data"]["image_hash"] = image_hash

        params = {
            "name": name,
            "object_story_spec": json.dumps(object_story_spec),
            "access_token": self.access_token
        }

        try:
            resp = requests.post(config.ENDPOINTS["adcreatives"], params=params)
            resp.raise_for_status()
            creative_id = resp.json().get("id")
            print(f"✅ Criativo criado! ID: {creative_id}")
            return creative_id
        except Exception as e:
            print(f"❌ Erro: {e}")
            if hasattr(e, 'response'):
                print(e.response.text)
            return None

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    p_list = subparsers.add_parser("list")
    p_list.add_argument("--limit", type=int, default=25)

    p_create = subparsers.add_parser("create")
    p_create.add_argument("name")
    p_create.add_argument("page_id")
    p_create.add_argument("message")
    p_create.add_argument("link")
    p_create.add_argument("--image-hash")
    p_create.add_argument("--cta", default="LEARN_MORE")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MetaAdsCreatives()

    if args.command == "list":
        manager.list_creatives(args.limit)
    elif args.command == "create":
        manager.create_creative(args.name, args.page_id, args.message, args.link, args.image_hash, args.cta)

if __name__ == "__main__":
    main()
