"""
Configuração para integração com Obsidian via Local REST API

Documentação: https://github.com/coddingtonbear/obsidian-local-rest-api
"""

import os
from pathlib import Path

# Carregar .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    # Se python-dotenv não estiver instalado, tentar carregar manualmente
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# ============================================
# CONFIGURAÇÃO DO OBSIDIAN LOCAL REST API
# ============================================

# URL da API (padrão quando Obsidian está aberto)
OBSIDIAN_API_URL = os.getenv("OBSIDIAN_API_URL", "https://127.0.0.1:27124")

# API Key (será configurada após instalação do plugin)
# Obtenha em: Obsidian → Settings → Local REST API
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY", "")

# Caminho do vault
OBSIDIAN_VAULT_PATH = "/Users/felipemdepaula/Library/Mobile Documents/com~apple~CloudDocs/Obsidian [meu cerebro]/dipaula/claude-code"

# ============================================
# ESTRUTURA DE PASTAS
# ============================================

FOLDERS = {
    "inbox": "00 - Inbox",
    "projects": "01 - Projetos",
    "ideas": "02 - Ideias",
    "knowledge": "03 - Conhecimento",
    "automations": "04 - Automações",
    "templates": "05 - Templates",
    "daily": "06 - Daily Notes",
    "resources": "07 - Recursos"
}

# ============================================
# CONFIGURAÇÕES DE TEMPLATES
# ============================================

# Ativar uso de templates
USE_TEMPLATES = True

# Pasta de templates
TEMPLATES_FOLDER = FOLDERS["templates"]

# ============================================
# CONFIGURAÇÕES DE DAILY NOTES
# ============================================

# Formato de data para daily notes
DAILY_NOTE_FORMAT = "%Y-%m-%d"  # Ex: 2025-11-02

# Criar daily note automaticamente
AUTO_CREATE_DAILY = True

# ============================================
# CONFIGURAÇÕES DE AUTOMAÇÃO
# ============================================

# Registrar automações em daily note
LOG_TO_DAILY = True

# Adicionar timestamp automático
AUTO_TIMESTAMP = True

# ============================================
# INTEGRAÇÕES
# ============================================

# Salvar outputs de ferramentas do workspace
SAVE_TOOL_OUTPUTS = True

# Documentar automações automaticamente
AUTO_DOC_AUTOMATIONS = True

# ============================================
# SEGURANÇA
# ============================================

# Verificar certificado SSL (False para desenvolvimento local)
VERIFY_SSL = False

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def get_headers():
    """Retorna headers para requisições à API"""
    return {
        "Authorization": f"Bearer {OBSIDIAN_API_KEY}",
        "Content-Type": "application/json"
    }

def get_folder_path(folder_key):
    """Retorna caminho completo de uma pasta"""
    return f"{OBSIDIAN_VAULT_PATH}/{FOLDERS.get(folder_key, '')}"

def validate_config():
    """Valida se configuração está completa"""
    if not OBSIDIAN_API_KEY:
        raise ValueError(
            "OBSIDIAN_API_KEY não configurada!\n"
            "Configure em: Obsidian → Settings → Local REST API\n"
            "Depois adicione em .env: OBSIDIAN_API_KEY=sua_key_aqui"
        )
    return True
