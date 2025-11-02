#!/usr/bin/env python3
"""
Configurações para a Instagram Graph API
"""

# Credenciais da Instagram API
INSTAGRAM_USER_ID = "17841477883364829"
INSTAGRAM_USERNAME = "lfimoveismg"
INSTAGRAM_ACCESS_TOKEN = "EAAPXQG5u0qkBP6fd6DYO72LHj3fqfCVPetj6Mb4sEyOzZCX38HPphrWSsUrUmNop3fcLJHfjofEjI6HGTjycZBZBGOUb53HzZBZC1i4ZCODHl7Ed6ZBuxKv1njq9LkrsRSYFsTGwghPuZCZBZCy5jnWsGlPkH4ENxZCeVKtCsLCTzSHSwRgtgyyvggwi5ZCPBySr"

# URLs da API
INSTAGRAM_API_VERSION = "v24.0"
INSTAGRAM_BASE_URL = f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}"

# Endpoints principais
ENDPOINTS = {
    "create_media": f"{INSTAGRAM_BASE_URL}/{INSTAGRAM_USER_ID}/media",
    "publish_media": f"{INSTAGRAM_BASE_URL}/{INSTAGRAM_USER_ID}/media_publish",
    "get_media": f"{INSTAGRAM_BASE_URL}",  # + media_id
    "rate_limit": f"{INSTAGRAM_BASE_URL}/{INSTAGRAM_USER_ID}/content_publishing_limit",
}

# Configurações de rate limit
RATE_LIMITS = {
    "posts_per_day": 100,  # Máximo de posts por 24 horas
    "check_before_post": True,  # Verificar rate limit antes de postar
}

# Configurações de mídia
MEDIA_CONFIG = {
    "allowed_image_formats": [".jpg", ".jpeg"],  # Instagram API aceita APENAS JPEG
    "max_caption_length": 2200,  # Máximo de caracteres na legenda
    "max_hashtags": 30,  # Máximo de hashtags por post
    "max_mentions": 20,  # Máximo de menções por post
}

# Configurações de upload
UPLOAD_CONFIG = {
    "auto_upload_to_nextcloud": True,  # Upload automático se arquivo for local (usa Catbox.moe)
    "convert_png_to_jpeg": True,  # Converter PNG para JPEG automaticamente
    "jpeg_quality": 95,  # Qualidade JPEG (0-100)
}

# Configurações de validação
VALIDATION_CONFIG = {
    "check_container_status": True,  # Verificar status do container antes de publicar
    "max_retries": 3,  # Tentativas de verificação de status
    "retry_delay": 5,  # Segundos entre tentativas
    "timeout": 120,  # Timeout máximo para operações (segundos)
}

# Mensagens de resposta
MESSAGES = {
    "success_container": "✅ Container criado com sucesso!",
    "success_publish": "🎉 Post publicado no Instagram com sucesso!",
    "error_rate_limit": "⚠️ Você atingiu o limite de publicações (100 posts/24h)",
    "error_invalid_image": "❌ Formato de imagem inválido. Use apenas JPEG (.jpg, .jpeg)",
    "error_caption_too_long": "❌ Legenda muito longa. Máximo de 2200 caracteres",
    "error_container_failed": "❌ Falha ao criar container. Verifique a URL da imagem",
    "error_publish_failed": "❌ Falha ao publicar post",
    "warning_converting_png": "🔄 Convertendo PNG para JPEG...",
    "info_uploading": "📤 Fazendo upload da imagem para Catbox.moe...",
    "info_checking_rate_limit": "🔍 Verificando rate limit...",
}
