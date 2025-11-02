#!/usr/bin/env python3
"""
Meta Ads - Gerenciar Ad Sets
"""
import requests, sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import meta_ads_config as config

class MetaAdsAdSets:
    def __init__(self):
        if not config.validate_config():
            sys.exit(1)
        self.access_token = config.ACCESS_TOKEN

    def list_adsets(self, campaign_id=None, limit=25):
        """Lista ad sets"""
        print("📦 LISTANDO AD SETS")
        print("=" * 60)
        endpoint = f"{config.ENDPOINTS['campaign']}/{campaign_id}/adsets" if campaign_id else config.ENDPOINTS["adsets"]
        params = {
            "fields": "id,name,campaign_id,status,daily_budget,lifetime_budget,optimization_goal,billing_event,bid_amount,targeting",
            "limit": limit,
            "access_token": self.access_token
        }

        try:
            resp = requests.get(endpoint, params=params)
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:
                print("📭 Nenhum ad set encontrado")
                return []

            print(f"✅ {len(data)} ad sets:\n")
            for i, a in enumerate(data, 1):
                print(f"[{i}] {a['name']}")
                print(f"    🆔 {a['id']}")
                print(f"    📊 {a['status']}")
                print(f"    🎯 {a.get('optimization_goal', 'N/A')}\n")
            return data
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def create_adset(self, campaign_id, name, daily_budget=None, optimization_goal="LINK_CLICKS", billing_event="IMPRESSIONS", bid_amount=None, targeting=None, status="PAUSED"):
        """Cria ad set"""
        print(f"🚀 CRIANDO AD SET: {name}")
        print("=" * 60)

        params = {
            "campaign_id": campaign_id,
            "name": name,
            "optimization_goal": optimization_goal,
            "billing_event": billing_event,
            "status": status,
            "access_token": self.access_token
        }

        # Só adiciona orçamento se fornecido (não usar quando campanha já tem orçamento)
        if daily_budget:
            params["daily_budget"] = int(daily_budget * 100)

        if bid_amount:
            params["bid_amount"] = int(bid_amount * 100)

        if targeting:
            params["targeting"] = json.dumps(targeting)
        else:
            # Targeting mínimo requerido
            params["targeting"] = json.dumps({
                "geo_locations": {"countries": ["US"]},
                "age_min": 18,
                "age_max": 65
            })

        try:
            resp = requests.post(config.ENDPOINTS["adsets"], params=params)
            resp.raise_for_status()
            adset_id = resp.json().get("id")
            print(f"✅ Ad Set criado!")
            print(f"🆔 ID: {adset_id}")
            return adset_id
        except Exception as e:
            print(f"❌ Erro: {e}")
            if hasattr(e, 'response'):
                print(f"Detalhes: {e.response.text}")
            return None

    def update_adset(self, adset_id, **kwargs):
        """Atualiza ad set"""
        print(f"🔄 ATUALIZANDO AD SET: {adset_id}")
        params = {"access_token": self.access_token}
        params.update(kwargs)

        try:
            resp = requests.post(f"{config.ENDPOINTS['adset']}/{adset_id}", params=params)
            resp.raise_for_status()
            print("✅ Atualizado!")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Meta Ads - Gerenciar Ad Sets")
    subparsers = parser.add_subparsers(dest="command")

    p_list = subparsers.add_parser("list")
    p_list.add_argument("--campaign-id", help="Filtrar por campanha")
    p_list.add_argument("--limit", type=int, default=25)

    p_create = subparsers.add_parser("create")
    p_create.add_argument("campaign_id", help="ID da campanha")
    p_create.add_argument("name", help="Nome do ad set")
    p_create.add_argument("daily_budget", type=float, help="Orçamento diário USD")
    p_create.add_argument("--optimization-goal", default="LINK_CLICKS")
    p_create.add_argument("--status", default="PAUSED")

    p_update = subparsers.add_parser("update")
    p_update.add_argument("adset_id")
    p_update.add_argument("--status")
    p_update.add_argument("--daily-budget", type=float)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MetaAdsAdSets()

    if args.command == "list":
        manager.list_adsets(args.campaign_id, args.limit)
    elif args.command == "create":
        manager.create_adset(args.campaign_id, args.name, args.daily_budget, args.optimization_goal, status=args.status)
    elif args.command == "update":
        kwargs = {k: v for k, v in vars(args).items() if v and k not in ['command', 'adset_id']}
        if 'daily_budget' in kwargs:
            kwargs['daily_budget'] = int(kwargs['daily_budget'] * 100)
        manager.update_adset(args.adset_id, **kwargs)

if __name__ == "__main__":
    main()
