#!/usr/bin/env python3
"""
Configurações para a Meta Ads (Marketing API)
"""

# ===================================================================
# CREDENCIAIS - PREENCHA COM SEUS DADOS
# ===================================================================

# Ad Account ID (formato: act_XXXXXXXXX)
# Encontre em: https://business.facebook.com/settings/ad-accounts
AD_ACCOUNT_ID = "act_1050347575979650"  # CA - 01 DIP (Conta Ativa)

# Access Token com permissões:
# - ads_management
# - ads_read
# - business_management
# Gere em: https://developers.facebook.com/tools/explorer
ACCESS_TOKEN = "EAAPXQG5u0qkBPwoIHPkCZB0dzPtR0rVjLZAxwmWzLS3SdfiSwwnzeQVv91d4Ts93pwhFJyF2WxFNwXEukLEjjY1DAZBJ4uCCfb9QOOBqw4Y3uOOFdwR7LcLozgOv4Gfwp9xHgaUcm5vF5KMNQhg9cu17dt50yz5cwSMuspOXT5AXk22PrZAm18kTH0Bm"

# Page ID (opcional, para criativos que usam página)
PAGE_ID = "859614930562831"  # LF Imóveis

# Instagram Account ID (opcional, para criativos no Instagram)
INSTAGRAM_ACTOR_ID = ""  # ID da conta Instagram Business

# ===================================================================
# CONFIGURAÇÕES DA API
# ===================================================================

# Versão da API
API_VERSION = "v24.0"

# URL Base da API
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Endpoints principais
ENDPOINTS = {
    # Campanhas
    "campaigns": f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns",
    "campaign": f"{BASE_URL}",  # + campaign_id

    # Ad Sets
    "adsets": f"{BASE_URL}/{AD_ACCOUNT_ID}/adsets",
    "adset": f"{BASE_URL}",  # + adset_id

    # Ads
    "ads": f"{BASE_URL}/{AD_ACCOUNT_ID}/ads",
    "ad": f"{BASE_URL}",  # + ad_id

    # Criativos
    "adcreatives": f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives",
    "adcreative": f"{BASE_URL}",  # + creative_id

    # Insights
    "insights": f"{BASE_URL}",  # + object_id + /insights

    # Ad Account
    "ad_account": f"{BASE_URL}/{AD_ACCOUNT_ID}",
}

# ===================================================================
# OBJETIVOS DE CAMPANHA
# ===================================================================

CAMPAIGN_OBJECTIVES = {
    "OUTCOME_AWARENESS": "Reconhecimento",
    "OUTCOME_ENGAGEMENT": "Engajamento",
    "OUTCOME_LEADS": "Geração de Leads",
    "OUTCOME_SALES": "Vendas",
    "OUTCOME_TRAFFIC": "Tráfego",
    "OUTCOME_APP_PROMOTION": "Promoção de App",
}

# ===================================================================
# BID STRATEGIES (Estratégias de Lance)
# ===================================================================

BID_STRATEGIES = {
    "LOWEST_COST_WITHOUT_CAP": "Custo mais baixo (sem limite)",
    "LOWEST_COST_WITH_BID_CAP": "Custo mais baixo (com limite de lance)",
    "COST_CAP": "Limite de custo",
    "LOWEST_COST_WITH_MIN_ROAS": "Custo mais baixo (com ROAS mínimo)",
}

# ===================================================================
# OPTIMIZATION GOALS (Metas de Otimização)
# ===================================================================

OPTIMIZATION_GOALS = {
    "LINK_CLICKS": "Cliques no link",
    "IMPRESSIONS": "Impressões",
    "REACH": "Alcance",
    "LANDING_PAGE_VIEWS": "Visualizações da página de destino",
    "POST_ENGAGEMENT": "Engajamento com a publicação",
    "CONVERSATIONS": "Conversas",
    "LEAD_GENERATION": "Geração de leads",
    "OFFSITE_CONVERSIONS": "Conversões fora do site",
    "APP_INSTALLS": "Instalações do app",
    "VALUE": "Valor",
    "QUALITY_LEAD": "Lead de qualidade",
}

# ===================================================================
# BILLING EVENTS (Eventos de Cobrança)
# ===================================================================

BILLING_EVENTS = {
    "IMPRESSIONS": "Impressões",
    "LINK_CLICKS": "Cliques no link",
    "POST_ENGAGEMENT": "Engajamento",
    "THRUPLAY": "ThruPlay (vídeo)",
}

# ===================================================================
# STATUS
# ===================================================================

STATUS_OPTIONS = {
    "ACTIVE": "Ativo",
    "PAUSED": "Pausado",
    "DELETED": "Deletado",
    "ARCHIVED": "Arquivado",
}

# ===================================================================
# CALL TO ACTION (CTAs)
# ===================================================================

CALL_TO_ACTIONS = [
    "SHOP_NOW",
    "LEARN_MORE",
    "SIGN_UP",
    "DOWNLOAD",
    "GET_QUOTE",
    "CONTACT_US",
    "APPLY_NOW",
    "BOOK_TRAVEL",
    "CALL_NOW",
    "GET_DIRECTIONS",
    "MESSAGE_PAGE",
    "SEND_MESSAGE",
    "SUBSCRIBE",
    "WATCH_MORE",
    "PLAY_GAME",
    "LISTEN_NOW",
    "ORDER_NOW",
    "REQUEST_TIME",
    "SEE_MENU",
    "VISIT_PAGES_FEED",
    "WHATSAPP_MESSAGE",
]

# ===================================================================
# MÉTRICAS DISPONÍVEIS
# ===================================================================

AVAILABLE_METRICS = [
    # Básicas
    "impressions",
    "clicks",
    "reach",
    "frequency",
    "spend",

    # Custos
    "cpc",  # Custo por clique
    "cpm",  # Custo por mil impressões
    "cpp",  # Custo por mil alcance
    "ctr",  # Taxa de cliques

    # Conversões
    "conversions",
    "conversion_values",
    "cost_per_conversion",
    "conversion_rate_ranking",

    # Vídeo
    "video_play_actions",
    "video_avg_time_watched_actions",
    "video_p25_watched_actions",
    "video_p50_watched_actions",
    "video_p75_watched_actions",
    "video_p100_watched_actions",

    # Engajamento
    "post_engagement",
    "post_reactions",
    "page_likes",
    "link_clicks",
    "landing_page_views",

    # ROI
    "purchase_roas",
    "website_purchase_roas",
]

# ===================================================================
# BREAKDOWNS (Dimensões para Análise)
# ===================================================================

AVAILABLE_BREAKDOWNS = [
    "age",
    "gender",
    "country",
    "region",
    "dma",
    "impression_device",
    "platform_position",
    "publisher_platform",
    "device_platform",
    "product_id",
    "hourly_stats_aggregated_by_advertiser_time_zone",
    "hourly_stats_aggregated_by_audience_time_zone",
]

# ===================================================================
# CONFIGURAÇÕES DE LIMITE
# ===================================================================

LIMITS = {
    "default_page_size": 25,
    "max_page_size": 500,
    "max_batch_size": 50,
}

# ===================================================================
# MENSAGENS
# ===================================================================

MESSAGES = {
    "success_create": "✅ Criado com sucesso!",
    "success_update": "✅ Atualizado com sucesso!",
    "success_delete": "✅ Deletado com sucesso!",
    "error_create": "❌ Erro ao criar",
    "error_update": "❌ Erro ao atualizar",
    "error_delete": "❌ Erro ao deletar",
    "error_fetch": "❌ Erro ao buscar dados",
    "error_no_token": "❌ Access Token não configurado",
    "error_no_account": "❌ Ad Account ID não configurado",
    "warning_config": "⚠️  Configure suas credenciais em config/meta_ads_config.py",
}

# ===================================================================
# VALIDAÇÕES
# ===================================================================

def validate_config():
    """Valida se as configurações estão preenchidas"""
    if ACCESS_TOKEN == "SEU_ACCESS_TOKEN_AQUI":
        print(MESSAGES["error_no_token"])
        print(MESSAGES["warning_config"])
        return False

    if AD_ACCOUNT_ID == "act_XXXXXXXXX":
        print(MESSAGES["error_no_account"])
        print(MESSAGES["warning_config"])
        return False

    return True
