#!/usr/bin/env python3
"""
Configuração do Nextcloud para upload de arquivos.
"""

import os

# Configurações do Nextcloud
NEXTCLOUD_URL = os.getenv("NEXTCLOUD_URL", "https://media.loop9.com.br")
NEXTCLOUD_USER = os.getenv("NEXTCLOUD_USER", "dipaula")
NEXTCLOUD_PASSWORD = os.getenv("NEXTCLOUD_PASSWORD", "Felipe33876865@")
NEXTCLOUD_FOLDER = os.getenv("NEXTCLOUD_FOLDER", "claude-code")

# Configurações de expiração padrão
DEFAULT_EXPIRE_DAYS = 1  # Links expiram em 24h por padrão
