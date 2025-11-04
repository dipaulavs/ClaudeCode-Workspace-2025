"""
Configurações compartilhadas do Chatbot WhatsApp V4
Centraliza todas as configurações de APIs e serviços
"""

import json
import os
from pathlib import Path

# 📂 Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent

# Carrega config do Chatwoot/Evolution
config_file = BASE_DIR / "chatwoot_config.json"
if config_file.exists():
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    # Valores padrão (substituir pelos reais)
    config = {
        "chatwoot": {
            "url": "https://chatwoot.loop9.com.br",
            "token": "SEU_TOKEN_CHATWOOT",
            "account_id": 1
        },
        "evolution": {
            "url": "https://evolution.loop9.com.br",
            "api_key": "SEU_API_KEY_EVOLUTION",
            "instance": "lfimoveis"
        }
    }

# ================================
# CHATWOOT
# ================================
CHATWOOT_API_URL = config['chatwoot']['url']
CHATWOOT_API_TOKEN = config['chatwoot']['token']
CHATWOOT_ACCOUNT_ID = config['chatwoot']['account_id']

# ================================
# EVOLUTION API (WhatsApp)
# ================================
EVOLUTION_URL = config['evolution']['url']
EVOLUTION_API_KEY = config['evolution']['api_key']
EVOLUTION_INSTANCE = config['evolution']['instance']

# ================================
# REDIS (Upstash)
# ================================
REDIS_URL = "https://legible-collie-9537.upstash.io"
REDIS_TOKEN = "ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"

# Para upstash_redis
REDIS_HOST = REDIS_URL
REDIS_PORT = 6379
REDIS_DB = 0

# ================================
# OPENROUTER (Claude Haiku 3.5)
# ================================
OPENROUTER_API_KEY = "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"

# ================================
# OPENAI (Whisper)
# ================================
OPENAI_API_KEY = "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"

# ================================
# GOOGLE SHEETS (Opcional)
# ================================
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")  # Configurar depois

# ================================
# IMÓVEIS
# ================================
IMOVEIS_DIR = BASE_DIR / "imoveis"

# ================================
# DEBOUNCE
# ================================
DEBOUNCE_SEGUNDOS = 15  # Aguarda 15s após última mensagem
DEBOUNCE_ESTENDIDO = 50  # Tempo adicional se incompleta
CONTEXTO_TTL = 1209600  # 14 dias
