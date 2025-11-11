#!/usr/bin/env python3
"""
Gera dashboard HTML com métricas Meta Ads usando dados do fetch_meta_ads.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Template base do dashboard (MotherDuck style)
DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{campaign_name} - Dashboard Meta Ads</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --beige: rgb(244, 239, 234);
            --yellow: rgb(255, 222, 0);
            --dark-gray: rgb(56, 56, 56);
            --black: rgb(0, 0, 0);
            --white: rgb(255, 255, 255);
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --border-width: 2px;
            --border-radius: 0px;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--beige);
            color: var(--black);
            line-height: 1.6;
            font-size: 16px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
        }}

        header h1 {{
            font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
            font-size: 3rem;
            margin-bottom: 0.5rem;
            color: var(--dark-gray);
            font-weight: 800;
            letter-spacing: -0.02em;
        }}

        .subtitle {{
            color: var(--dark-gray);
            font-size: 1.1rem;
            opacity: 0.7;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}

        .stat-card {{
            background: var(--white);
            padding: 1.5rem;
            border: var(--border-width) solid var(--dark-gray);
            border-radius: var(--border-radius);
            display: flex;
            flex-direction: column;
            transition: all 0.2s;
        }}

        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 8px 8px 0px var(--dark-gray);
        }}

        .stat-label {{
            color: var(--dark-gray);
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
            font-family: 'SF Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--dark-gray);
            font-family: 'SF Mono', monospace;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .metric-card {{
            background: var(--white);
            padding: 1.5rem;
            border: var(--border-width) solid var(--dark-gray);
            border-radius: var(--border-radius);
            transition: all 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 8px 8px 0px var(--dark-gray);
        }}

        .metric-card.winner {{
            border-color: var(--success);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, var(--white) 100%);
        }}

        .metric-card.warning {{
            border-color: var(--warning);
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, var(--white) 100%);
        }}

        .metric-card.danger {{
            border-color: var(--danger);
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, var(--white) 100%);
        }}

        .metric-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .metric-icon {{
            font-size: 1.5rem;
        }}

        .metric-status {{
            font-family: 'SF Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.75rem;
            border: var(--border-width) solid var(--dark-gray);
            border-radius: var(--border-radius);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .metric-card.winner .metric-status {{
            background: var(--success);
            color: var(--white);
        }}

        .metric-card.warning .metric-status {{
            background: var(--warning);
            color: var(--dark-gray);
        }}

        .metric-card.danger .metric-status {{
            background: var(--danger);
            color: var(--white);
        }}

        .metric-label {{
            font-size: 0.875rem;
            color: var(--dark-gray);
            opacity: 0.8;
            margin-bottom: 0.5rem;
            font-family: 'SF Mono', monospace;
            text-transform: uppercase;
        }}

        .metric-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--dark-gray);
            font-family: 'SF Mono', monospace;
            margin-bottom: 0.5rem;
        }}

        .metric-detail {{
            font-size: 0.875rem;
            color: var(--dark-gray);
            opacity: 0.6;
        }}

        .section-title {{
            font-family: 'SF Mono', monospace;
            font-size: 2rem;
            color: var(--dark-gray);
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .alert {{
            padding: 1.5rem;
            border: var(--border-width) solid var(--dark-gray);
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
        }}

        .alert-success {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, var(--white) 100%);
            border-color: var(--success);
        }}

        .alert-warning {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, var(--white) 100%);
            border-color: var(--warning);
        }}

        .alert-danger {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, var(--white) 100%);
            border-color: var(--danger);
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            header h1 {{
                font-size: 2rem;
            }}

            .section-title {{
                font-size: 1.5rem;
            }}

            .metric-grid {{
                grid-template-columns: 1fr;
            }}

            .metric-value,
            .stat-value {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>📊 {campaign_name}</h1>
                <p class="subtitle">Dashboard Métricas Meta Ads · {date_br}</p>
            </div>
        </header>

        <!-- RESUMO GERAL -->
        <div class="stats">
            <div class="stat-card">
                <span class="stat-label">💰 Investido (30d)</span>
                <span class="stat-value">R$ {spend:.2f}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">💬 Conversões</span>
                <span class="stat-value">{total_conversoes}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">💵 Custo/Conversão</span>
                <span class="stat-value">R$ {custo_conversao:.2f}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">📊 CTR</span>
                <span class="stat-value">{ctr:.2f}%</span>
            </div>
        </div>

        <!-- STATUS GERAL -->
        {status_alert}

        <!-- MÉTRICAS PRIMÁRIAS -->
        <h2 class="section-title">Métricas de Performance</h2>
        <div class="metric-grid">
            {ctr_card}
            {custo_card}
            {conversoes_card}
            {frequencia_card}
        </div>

        <!-- MÉTRICAS SECUNDÁRIAS -->
        <div class="stats">
            <div class="stat-card">
                <span class="stat-label">👁️ Impressões</span>
                <span class="stat-value">{impressions:,}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">📈 Alcance</span>
                <span class="stat-value">{reach:,}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">💸 CPM</span>
                <span class="stat-value">R$ {cpm:.2f}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">👆 Cliques</span>
                <span class="stat-value">{clicks:,}</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

def generate_status_alert(metrics):
    """Gera o alerta de status geral da campanha."""
    ctr = metrics['ctr']
    custo = metrics['custo_conversao']
    conversoes = metrics['total_conversoes']
    frequencia = metrics['frequency']

    # Determinar status geral
    if ctr >= 3 and conversoes >= 10 and custo <= 10 and frequencia < 3.5:
        alert_class = "alert-success"
        title = "✅ CAMPANHA PERFORMANDO MUITO BEM!"
        message = f"Seu anúncio está validado como WINNER. CTR {ctr:.2f}%, {conversoes} conversões a R$ {custo:.2f} cada. Continue assim!"
    elif ctr >= 1.5 and conversoes >= 5:
        alert_class = "alert-warning"
        title = "⚠️ CAMPANHA COM POTENCIAL"
        message = f"Métricas promissoras mas ainda não validadas. Aguarde mais dados ou otimize criativos."
    else:
        alert_class = "alert-danger"
        title = "❌ CAMPANHA PRECISA DE ATENÇÃO"
        message = "Métricas abaixo do esperado. Revise criativos, targeting ou pausar e testar novo ângulo."

    return f'<div class="alert {alert_class}"><strong>{title}</strong><p>{message}</p></div>'

def generate_metric_card(label, value, detail, status, icon):
    """Gera um card de métrica com status."""
    status_classes = {
        'winner': 'winner',
        'warning': 'warning',
        'danger': 'danger'
    }

    status_labels = {
        'winner': '✅ EXCELENTE',
        'warning': '⚠️ ATENÇÃO',
        'danger': '❌ CRÍTICO'
    }

    card_class = status_classes.get(status, '')
    status_label = status_labels.get(status, '')

    return f"""
    <div class="metric-card {card_class}">
        <div class="metric-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-status">{status_label}</span>
        </div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-detail">{detail}</div>
    </div>
    """

def generate_dashboard(metrics_data):
    """
    Gera dashboard HTML a partir dos dados de métricas.

    Args:
        metrics_data (dict): Dados com 'metrics' e 'raw_data'

    Returns:
        str: HTML do dashboard
    """
    metrics = metrics_data['metrics']

    # Determinar status de cada métrica
    ctr = metrics['ctr']
    ctr_status = 'winner' if ctr >= 5 else ('winner' if ctr >= 3 else ('warning' if ctr >= 1.5 else 'danger'))
    ctr_card = generate_metric_card(
        "CTR (Click-Through Rate)",
        f"{ctr:.2f}%",
        f"Meta: 3%+ | {'Acima da média' if ctr >= 3 else 'Abaixo da média'}",
        ctr_status,
        "🔥" if ctr >= 5 else "📊"
    )

    custo = metrics['custo_conversao']
    custo_status = 'winner' if custo <= 5 else ('winner' if custo <= 10 else ('warning' if custo <= 20 else 'danger'))
    custo_card = generate_metric_card(
        "Custo por Conversão (CPA)",
        f"R$ {custo:.2f}",
        f"{metrics['total_conversoes']} conversões totais",
        custo_status,
        "💎" if custo <= 5 else "💵"
    )

    conversoes = metrics['total_conversoes']
    conversoes_status = 'winner' if conversoes >= 10 else ('warning' if conversoes >= 5 else 'danger')
    conversoes_card = generate_metric_card(
        "Volume de Conversões",
        str(conversoes),
        "Meta: 10+ para validar" if conversoes < 10 else "Volume validado ✅",
        conversoes_status,
        "🎯"
    )

    freq = metrics['frequency']
    freq_status = 'winner' if freq < 2 else ('winner' if freq < 3.5 else ('warning' if freq < 5 else 'danger'))
    frequencia_card = generate_metric_card(
        "Frequência",
        f"{freq:.2f}",
        "Meta: < 3.5 | " + ("Audiência fresca" if freq < 3.5 else "Audiência saturando"),
        freq_status,
        "📱"
    )

    # Preencher template
    html = DASHBOARD_TEMPLATE.format(
        campaign_name=metrics['campaign_name'],
        date_br=datetime.now().strftime("%d/%m/%Y"),
        spend=metrics['spend'],
        total_conversoes=metrics['total_conversoes'],
        custo_conversao=metrics['custo_conversao'],
        ctr=metrics['ctr'],
        status_alert=generate_status_alert(metrics),
        ctr_card=ctr_card,
        custo_card=custo_card,
        conversoes_card=conversoes_card,
        frequencia_card=frequencia_card,
        impressions=metrics['impressions'],
        reach=metrics['reach'],
        cpm=metrics['cpm'],
        clicks=metrics['clicks']
    )

    return html

if __name__ == "__main__":
    # Ler dados do JSON gerado por fetch_meta_ads.py
    json_path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/meta_ads_data.json'

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Gerar HTML
    html = generate_dashboard(data)

    # Salvar em Downloads com nome do produto + data
    campaign_name = data['metrics']['campaign_name'].split('│')[0].strip().replace(' ', '-').lower()
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{campaign_name}_{date_str}.html"

    downloads_path = Path.home() / "Downloads" / filename

    with open(downloads_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Dashboard salvo em: {downloads_path}")
