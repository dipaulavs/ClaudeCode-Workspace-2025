#!/usr/bin/env python3
"""
Template: Obter Métricas Meta Ads

Uso:
    python3 scripts/meta-ads/get_insights.py --id 123456789 --level campaign
    python3 scripts/meta-ads/get_insights.py -i 123 -l adset -p last_30d -e relatorio.json
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.meta_ads_insights import MetaAdsInsights

def get_insights(object_id: str, level: str, period: str = "last_7d",
                breakdown: str = None, export_file: str = None):
    """
    Obtém métricas Meta Ads

    Args:
        object_id: ID da campanha/adset/ad
        level: Nível de detalhe (campaign, adset, ad)
        period: Período dos dados
        breakdown: Dimensão para quebra (opcional)
        export_file: Nome do arquivo para exportar (opcional)

    Returns:
        Lista de dicionários com métricas
    """
    mgr = MetaAdsInsights()

    # Busca insights
    data = mgr.get_insights(
        object_id=object_id,
        level=level,
        date_preset=period,
        breakdowns=breakdown
    )

    # Exporta se solicitado
    if export_file:
        mgr.export_insights(
            object_id=object_id,
            filename=export_file,
            level=level,
            date_preset=period
        )

    return data

def main():
    parser = argparse.ArgumentParser(description='Obter métricas Meta Ads')

    parser.add_argument('--id', '-i', required=True,
                       help='ID da campanha/adset/ad')
    parser.add_argument('--level', '-l', required=True,
                       choices=['campaign', 'adset', 'ad'],
                       help='Nível: campaign, adset ou ad')
    parser.add_argument('--period', '-p', default='last_7d',
                       choices=['today', 'yesterday', 'last_7d', 'last_30d', 'lifetime'],
                       help='Período (padrão: last_7d)')
    parser.add_argument('--breakdown', '-b',
                       choices=['age', 'gender', 'country', 'region', 'placement'],
                       help='Dimensão para quebra (opcional)')
    parser.add_argument('--export', '-e',
                       help='Nome do arquivo para exportar (.json)')

    args = parser.parse_args()

    # Mensagem de início
    breakdown_text = f" por {args.breakdown}" if args.breakdown else ""
    export_text = f" e exportando para {args.export}" if args.export else ""
    print(f"📊 Buscando métricas{breakdown_text}...")
    print(f"   ID: {args.id}")
    print(f"   Nível: {args.level}")
    print(f"   Período: {args.period}")

    try:
        data = get_insights(
            args.id,
            args.level,
            args.period,
            args.breakdown,
            args.export
        )

        if not data:
            print(f"\n⚠️  Nenhum dado encontrado para o período selecionado")
            return

        print(f"\n✅ Métricas obtidas com sucesso!")
        print(f"   Total de registros: {len(data)}")

        # Exibe métricas principais
        for idx, record in enumerate(data, 1):
            if idx > 3:  # Limita a 3 registros
                print(f"   ... e mais {len(data) - 3} registro(s)")
                break

            print(f"\n   📈 Registro {idx}:")
            print(f"      Impressões: {record.get('impressions', 'N/A')}")
            print(f"      Cliques: {record.get('clicks', 'N/A')}")
            print(f"      Alcance: {record.get('reach', 'N/A')}")
            print(f"      Gasto: ${record.get('spend', 'N/A')}")
            print(f"      CPC: ${record.get('cpc', 'N/A')}")
            print(f"      CTR: {record.get('ctr', 'N/A')}%")

        if args.export:
            print(f"\n💾 Dados exportados para: {args.export}")

        return data
    except Exception as e:
        print(f"❌ Erro ao obter métricas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
