#!/usr/bin/env python3
"""
Meta Ads - Gerenciar Campanhas
Criar, listar, atualizar, deletar campanhas
"""
import requests, sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import meta_ads_config as config

class MetaAdsCampaigns:
    def __init__(self):
        if not config.validate_config():
            sys.exit(1)
        self.access_token = config.ACCESS_TOKEN
        self.endpoints = config.ENDPOINTS

    def list_campaigns(self, status_filter=None, limit=25):
        """Lista campanhas"""
        print(f"📋 LISTANDO CAMPANHAS")
        print("=" * 60)
        params = {
            "fields": "id,name,objective,status,daily_budget,lifetime_budget,budget_remaining,start_time,stop_time,created_time,updated_time",
            "limit": limit,
            "access_token": self.access_token
        }
        if status_filter:
            params["filtering"] = json.dumps([{"field": "effective_status", "operator": "IN", "value": status_filter}])

        try:
            resp = requests.get(config.ENDPOINTS["campaigns"], params=params)
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:
                print("📭 Nenhuma campanha encontrada")
                return []

            print(f"✅ {len(data)} campanhas:\n")
            for i, c in enumerate(data, 1):
                budget = f"${int(c.get('daily_budget', 0))/100:.2f}/dia" if c.get('daily_budget') else f"${int(c.get('lifetime_budget', 0))/100:.2f} total"
                print(f"[{i}] {c['name']}")
                print(f"    🆔 {c['id']}")
                print(f"    🎯 {c.get('objective', 'N/A')}")
                print(f"    📊 {c['status']}")
                print(f"    💰 {budget}\n")
            return data
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def create_campaign(self, name, objective, status="PAUSED", daily_budget=None, lifetime_budget=None, bid_strategy="LOWEST_COST_WITHOUT_CAP", special_ad_categories=None):
        """Cria campanha"""
        print(f"🚀 CRIANDO CAMPANHA: {name}")
        print("=" * 60)

        # special_ad_categories é obrigatório (NONE, CREDIT, EMPLOYMENT, HOUSING)
        if special_ad_categories is None:
            special_ad_categories = []

        params = {
            "name": name,
            "objective": objective,
            "status": status,
            "bid_strategy": bid_strategy,
            "special_ad_categories": json.dumps(special_ad_categories),
            "access_token": self.access_token
        }

        if daily_budget:
            params["daily_budget"] = int(daily_budget * 100)  # Converte para centavos
        if lifetime_budget:
            params["lifetime_budget"] = int(lifetime_budget * 100)

        try:
            resp = requests.post(config.ENDPOINTS["campaigns"], params=params)
            resp.raise_for_status()
            campaign_id = resp.json().get("id")
            print(f"✅ Campanha criada!")
            print(f"🆔 ID: {campaign_id}")
            return campaign_id
        except Exception as e:
            print(f"❌ Erro: {e}")
            if hasattr(e, 'response'):
                print(f"Detalhes: {e.response.text}")
            return None

    def update_campaign(self, campaign_id, **kwargs):
        """Atualiza campanha"""
        print(f"🔄 ATUALIZANDO CAMPANHA: {campaign_id}")
        params = {"access_token": self.access_token}
        params.update(kwargs)

        try:
            resp = requests.post(f"{config.ENDPOINTS['campaign']}/{campaign_id}", params=params)
            resp.raise_for_status()
            print("✅ Atualizado!")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def delete_campaign(self, campaign_id):
        """Deleta campanha"""
        print(f"🗑️  DELETANDO: {campaign_id}")
        try:
            resp = requests.delete(f"{config.ENDPOINTS['campaign']}/{campaign_id}", params={"access_token": self.access_token})
            resp.raise_for_status()
            print("✅ Deletado!")
            return True
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Meta Ads - Gerenciar Campanhas")
    subparsers = parser.add_subparsers(dest="command")

    # List
    p_list = subparsers.add_parser("list", help="Listar campanhas")
    p_list.add_argument("--status", nargs="+", help="Filtrar por status")
    p_list.add_argument("--limit", type=int, default=25)

    # Create
    p_create = subparsers.add_parser("create", help="Criar campanha")
    p_create.add_argument("name", help="Nome da campanha")
    p_create.add_argument("objective", help="Objetivo (ex: OUTCOME_TRAFFIC)")
    p_create.add_argument("--daily-budget", type=float, help="Orçamento diário em USD")
    p_create.add_argument("--lifetime-budget", type=float, help="Orçamento total em USD")
    p_create.add_argument("--status", default="PAUSED", choices=["ACTIVE", "PAUSED"])

    # Update
    p_update = subparsers.add_parser("update", help="Atualizar campanha")
    p_update.add_argument("campaign_id", help="ID da campanha")
    p_update.add_argument("--name", help="Novo nome")
    p_update.add_argument("--status", help="Novo status")
    p_update.add_argument("--daily-budget", type=float, help="Novo orçamento diário")

    # Delete
    p_delete = subparsers.add_parser("delete", help="Deletar campanha")
    p_delete.add_argument("campaign_id", help="ID da campanha")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MetaAdsCampaigns()

    if args.command == "list":
        manager.list_campaigns(args.status, args.limit)
    elif args.command == "create":
        manager.create_campaign(args.name, args.objective, args.status, args.daily_budget, args.lifetime_budget)
    elif args.command == "update":
        kwargs = {k: v for k, v in vars(args).items() if v and k not in ['command', 'campaign_id']}
        if 'daily_budget' in kwargs:
            kwargs['daily_budget'] = int(kwargs['daily_budget'] * 100)
        manager.update_campaign(args.campaign_id, **kwargs)
    elif args.command == "delete":
        manager.delete_campaign(args.campaign_id)

if __name__ == "__main__":
    main()
