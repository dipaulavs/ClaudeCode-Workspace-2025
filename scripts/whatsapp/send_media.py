#!/usr/bin/env python3
"""
Template: Enviar mídia WhatsApp via Evolution API

🚨 REGRA CRÍTICA - Evolution API aceita APENAS URLs públicas:

✅ SEMPRE use:
   - URLs PÚBLICAS e diretas (http:// ou https://)
   - URLs retornadas pelas APIs de geração:
     • Nano Banana: https://tempfile.aiquickdraw.com/...
     • GPT-4o: URL na resposta da OpenAI
     • Sora/Vídeos: URL na resposta da Kie.ai

❌ NÃO funciona (opção --file foi REMOVIDA):
   - Arquivos locais do sistema
   - Base64 encoded
   - Paths relativos ou absolutos

Uso:
    python3 scripts/whatsapp/send_media.py \\
        --phone 5531980160822 \\
        --url "https://tempfile.aiquickdraw.com/workers/nano/image_1762111620183_63um11_2x3_683x1024.png" \\
        --type image \\
        --caption "Veja isso!"
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def infer_media_type(url: str) -> str:
    """
    Infere automaticamente o tipo de mídia pela extensão da URL
    Retorna: 'image', 'video', 'audio', ou 'document'
    """
    url_lower = url.lower()

    # Imagens
    if any(ext in url_lower for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']):
        return 'image'

    # Vídeos
    if any(ext in url_lower for ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']):
        return 'video'

    # Áudio
    if any(ext in url_lower for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac']):
        return 'audio'

    # Documento (padrão se não for detectado)
    if any(ext in url_lower for ext in ['.pdf', '.doc', '.docx', '.txt', '.zip']):
        return 'document'

    # Se não detectar, retorna None para forçar usuário especificar
    return None


def validate_url(url: str):
    """
    Valida regra crítica: APENAS URLs públicas
    Lê a docstring do arquivo pra confirmar
    """
    if not url:
        raise ValueError("URL não pode estar vazia")

    # ✅ URLs públicas válidas
    if url.startswith(('http://', 'https://')):
        return True

    # ❌ Rejeita base64
    if url.startswith('data:'):
        raise ValueError(
            "❌ Base64 não funciona na Evolution API!\n"
            "A regra diz: APENAS URLs públicas (http:// ou https://)"
        )

    # ❌ Rejeita paths locais
    if url.startswith(('/','~', '.')):
        raise ValueError(
            "❌ Caminho local não funciona na Evolution API!\n"
            "A regra diz: APENAS URLs públicas (http:// ou https://)"
        )

    raise ValueError(
        f"❌ URL inválida: {url}\n"
        "A regra diz: APENAS URLs públicas (http:// ou https://)\n"
        "Exemplos:\n"
        "  - https://tempfile.aiquickdraw.com/..."
        "  - https://example.com/imagem.png"
    )


def send_media(phone: str, media_source: str, media_type: str, caption: str = "", filename: str = None):
    """Envia mídia via WhatsApp"""

    # Valida a URL ANTES de tentar enviar
    try:
        validate_url(media_source)
    except ValueError as e:
        print(e)
        sys.exit(1)

    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    response = api.send_media(
        number=phone,
        media_url=media_source,
        caption=caption,
        media_type=media_type,
        filename=filename
    )

    return response


def main():
    parser = argparse.ArgumentParser(
        description='Enviar mídia WhatsApp - APENAS URLs públicas (Evolution API não aceita arquivos locais)',
        epilog='💡 Use URLs retornadas pelas APIs: Nano Banana, GPT-4o, Sora, etc.'
    )
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI')
    parser.add_argument('--url', '-u', required=True,
                       help='URL PÚBLICA da mídia (http:// ou https://)')
    parser.add_argument('--type', '-t', required=False,
                       choices=['image', 'video', 'document', 'audio'],
                       help='Tipo de mídia (opcional - detectado automaticamente pela extensão)')
    parser.add_argument('--caption', '-c', default='', help='Legenda da mídia')
    parser.add_argument('--filename', '-f', help='Nome do arquivo (para documentos)')

    args = parser.parse_args()

    media_source = args.url

    # Inferir tipo automaticamente se não foi especificado
    if args.type:
        media_type = args.type
    else:
        media_type = infer_media_type(media_source)
        if not media_type:
            print("❌ Não foi possível detectar o tipo de mídia pela URL.")
            print("   Use --type para especificar: image, video, audio ou document")
            sys.exit(1)
        print(f"🔍 Tipo detectado automaticamente: {media_type}")

    print(f"📤 Enviando {media_type} para {args.phone}...")

    try:
        response = send_media(args.phone, media_source, media_type, args.caption, args.filename)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Mídia enviada com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar mídia: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
