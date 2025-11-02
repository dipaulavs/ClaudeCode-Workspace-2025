"""
Configuração da TikTok API23 (RapidAPI)
"""

# RapidAPI Credentials
RAPIDAPI_KEY = "82a6c38fa1msh40088bb99ac4883p1bd271jsn604d036bd581"
RAPIDAPI_HOST = "tiktok-api23.p.rapidapi.com"

# Base URL
BASE_URL = f"https://{RAPIDAPI_HOST}"

# Headers padrão
HEADERS = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST
}

# Limites padrão
DEFAULT_COUNT = 30
DEFAULT_CURSOR = 0
MAX_RETRIES = 3
TIMEOUT = 30  # segundos
