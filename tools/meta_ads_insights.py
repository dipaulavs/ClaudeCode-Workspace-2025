#!/usr/bin/env python3
"""Meta Ads - Obter Insights/Métricas"""
import requests, sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import meta_ads_config as config

class MetaAdsInsights:
    def __init__(self):
        if not config.validate_config():
            sys.exit(1)
        self.access_token = config.ACCESS_TOKEN

    def get_insights(self, object_id, level="campaign", date_preset="last_30d", breakdowns=None):
        print(f"📊 OBTENDO INSIGHTS")
        print("=" * 60)
        print(f"🎯 Nível: {level}")
        print(f"📅 Período: {date_preset}")
        print("=" * 60)

        params = {
            "level": level,
            "date_preset": date_preset,
            "fields": "impressions,clicks,spend,reach,cpc,cpm,ctr,conversions",
            "access_token": self.access_token
        }

        if breakdowns:
            params["breakdowns"] = breakdowns

        try:
            resp = requests.get(f"{config.ENDPOINTS['insights']}/{object_id}/insights", params=params)
            resp.raise_for_status()
            data = resp.json().get("data", [])

            if not data:
                print("📭 Nenhum dado encontrado")
                return []

            print(f"\n✅ {len(data)} resultados:\n")
            for i, d in enumerate(data, 1):
                print(f"[{i}] {d.get('campaign_name', d.get('adset_name', d.get('ad_name', 'N/A')))}")
                print(f"    👁️  Impressões: {int(d.get('impressions', 0)):,}")
                print(f"    🖱️  Cliques: {int(d.get('clicks', 0)):,}")
                print(f"    💰 Gasto: ${float(d.get('spend', 0)):.2f}")
                print(f"    📈 CPC: ${float(d.get('cpc', 0)):.2f}")
                print(f"    📊 CTR: {float(d.get('ctr', 0)):.2f}%\n")

            return data
        except Exception as e:
            print(f"❌ Erro: {e}")
            if hasattr(e, 'response'):
                print(e.response.text)
            return []

    def export_insights(self, object_id, filename, level="campaign", date_preset="last_30d"):
        data = self.get_insights(object_id, level, date_preset)
        if data:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Exportado para: {filename}")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    p_get = subparsers.add_parser("get")
    p_get.add_argument("object_id", help="ID da campanha/adset/ad")
    p_get.add_argument("--level", default="campaign", choices=["campaign", "adset", "ad"])
    p_get.add_argument("--period", default="last_30d", choices=["today", "yesterday", "last_7d", "last_30d", "lifetime"])
    p_get.add_argument("--breakdown", help="age, gender, country, etc")

    p_export = subparsers.add_parser("export")
    p_export.add_argument("object_id")
    p_export.add_argument("filename")
    p_export.add_argument("--level", default="campaign")
    p_export.add_argument("--period", default="last_30d")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MetaAdsInsights()

    if args.command == "get":
        manager.get_insights(args.object_id, args.level, args.period, args.breakdown)
    elif args.command == "export":
        manager.export_insights(args.object_id, args.filename, args.level, args.period)

if __name__ == "__main__":
    main()
