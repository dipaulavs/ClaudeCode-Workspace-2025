#!/usr/bin/env python3
"""
Configurações para o Apify (Web Scraper, Twitter Scraper e Google Maps Scraper)
"""

import os

# API Token do Apify
APIFY_API_TOKEN = "apify_api_HCIqvg41GN153X9F7dAW0pgI9zBnAI4yPBre"
APIFY_API_KEY = APIFY_API_TOKEN  # Alias para compatibilidade

# Actor ID do Website Content Crawler
APIFY_ACTOR_ID = "aYG0l9s7dbB7j3gbS"

# Actor ID do Twitter Scraper
APIFY_TWITTER_ACTOR_ID = "61RPP7dywgiy0JPD0"

# Actor ID do Google Maps Scraper
GOOGLE_MAPS_SCRAPER_ACTOR_ID = "compass/crawler-google-places"

# Actor ID do Instagram Scraper
INSTAGRAM_SCRAPER_ACTOR_ID = "apify/instagram-scraper"

# Google Maps Scraper - Default Settings
GOOGLE_MAPS_DEFAULTS = {
    "language": "pt",
    "maxCrawledPlaces": 20,
    "maxCrawledPlacesPerSearch": 20,
    "maxReviews": 0,  # 0 = sem reviews (mais rápido)
    "maxImages": 1,
    "includeWebResults": False,
    "includeHistogram": False,
    "includeOpeningHours": True,
    "includePeopleAlsoSearch": False,
    "maxQuestions": 0,
    "exportPlaceUrls": False,
    "scrapeDirectories": False,
    "scrapeReviewerName": False,
    "scrapeReviewerId": False,
    "scrapeReviewerUrl": False,
    "scrapeReviewId": False,
    "scrapeReviewUrl": False,
    "scrapeResponseFromOwnerText": False,
}

# Export Settings
DEFAULT_EXPORT_FORMAT = "json"  # json, csv, xlsx
EXPORT_DIR = os.path.expanduser("~/Downloads")

# Timeout Settings
DEFAULT_TIMEOUT = 300  # 5 minutos

# Configurações padrão do crawler
DEFAULT_CRAWLER_CONFIG = {
    # Tipo de crawler
    "crawlerType": "playwright:adaptive",

    # Controle de páginas
    "maxCrawlPages": 9999999,  # Ilimitado
    "maxCrawlDepth": 20,
    "initialConcurrency": 0,
    "maxConcurrency": 200,

    # Sitemaps e URLs
    "useSitemaps": True,
    "includeUrlGlobs": [],
    "excludeUrlGlobs": [],
    "keepUrlFragments": False,
    "ignoreCanonicalUrl": False,

    # Cookies e sessões
    "initialCookies": [],
    "removeCookieWarnings": True,

    # Proxy
    "proxyConfiguration": {
        "useApifyProxy": True
    },

    # Requisições
    "maxSessionRotations": 10,
    "maxRequestRetries": 3,
    "requestTimeoutSecs": 60,
    "minFileDownloadSpeedKBps": 128,
    "ignoreHttpsErrors": False,

    # Processamento de página
    "dynamicContentWaitSecs": 10,
    "maxScrollHeightPixels": 5000,
    "waitForSelector": "",
    "softWaitForSelector": "",

    # Elementos para remover (limpeza)
    "removeElementsCssSelector": """nav, footer, script, style, noscript, svg, img[src^='data:'],
        [role="alert"],
        [role="banner"],
        [role="dialog"],
        [role="alertdialog"],
        [role="region"][aria-label*="skip" i],
        [aria-modal="true"]""",

    # Elementos para manter
    "keepElementsCssSelector": "",

    # Elementos para clicar (expandir menus colapsados)
    "clickElementsCssSelector": "[aria-expanded=\"false\"]",

    # Iframes
    "expandIframes": True,

    # Mídia
    "blockMedia": True,

    # Transformação HTML
    "htmlTransformer": "readableText",
    "readableTextCharThreshold": 100,
    "aggressivePrune": False,

    # Outputs
    "saveHtml": False,
    "saveHtmlAsFile": False,
    "saveMarkdown": True,
    "saveFiles": False,
    "saveScreenshots": False,
    "maxResults": 9999999,

    # Detecção de renderização
    "clientSideMinChangePercentage": 15,
    "renderingTypeDetectionPercentage": 10,

    # Debug
    "debugMode": False,
    "debugLog": False,

    # Robots.txt
    "respectRobotsTxtFile": False
}

# Limite razoável para preview (evitar scraping excessivo sem confirmação)
PREVIEW_MAX_PAGES = 500  # Mostra aviso se ultrapassar

# Instagram Scraper - Default Settings
INSTAGRAM_DEFAULTS = {
    "resultsLimit": 50,  # Máximo de posts/comentários por execução
    "searchLimit": 10,   # Máximo de resultados de busca
    "addParentData": False,
    "enhanceUserSearchWithFacebookPage": False,
    "isUserTaggedFeedURL": False,
    "onlyPostsNewerThan": "",  # Data ISO 8601 (ex: "2024-01-01")
    "onlyPostsOlderThan": "",  # Data ISO 8601
}

# Instagram Scraper - Search Types
INSTAGRAM_SEARCH_TYPES = {
    "user": "user",        # Buscar por username
    "hashtag": "hashtag",  # Buscar por hashtag
    "place": "place",      # Buscar por localização
}

# Instagram Scraper - Results Types
INSTAGRAM_RESULTS_TYPES = {
    "posts": "posts",      # Retornar posts
    "comments": "comments", # Retornar comentários
    "details": "details",  # Retornar detalhes (perfil/hashtag/place)
}

# Instagram Scraper - Post Types
INSTAGRAM_POST_TYPES = {
    "Image": "Image",
    "Video": "Video",
    "Sidecar": "Sidecar",  # Carrossel (múltiplas imagens)
}
