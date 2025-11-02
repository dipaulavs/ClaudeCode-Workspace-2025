#!/usr/bin/env python3
"""
Template: Gerenciar webhooks da instância WhatsApp via Evolution API

⚠️  ATENÇÃO: Use com cuidado! Alterar webhooks pode afetar integrações em produção.
            Sempre use --action get primeiro para ver a configuração atual.

Uso:
    # Ver webhooks atuais
    python3 scripts/whatsapp/manage_webhooks.py --action get

    # Configurar webhook (USE COM CUIDADO!)
    python3 scripts/whatsapp/manage_webhooks.py --action set --url https://seu.webhook.com/events --events MESSAGES_UPSERT,CONNECTION_UPDATE
    python3 scripts/whatsapp/manage_webhooks.py --action set --url https://seu.webhook.com/events --events MESSAGES_UPSERT --by-events --base64

Eventos disponíveis:
    - MESSAGES_UPSERT: Nova mensagem recebida
    - MESSAGES_UPDATE: Mensagem atualizada (lida, deletada, etc)
    - MESSAGES_DELETE: Mensagem deletada
    - SEND_MESSAGE: Mensagem enviada
    - CONNECTION_UPDATE: Mudança no estado da conexão
    - QRCODE_UPDATED: QR code atualizado
    - GROUPS_UPSERT: Novo grupo criado
    - GROUPS_UPDATE: Grupo atualizado
    - GROUP_PARTICIPANTS_UPDATE: Participantes do grupo atualizados
"""

import sys
import argparse
from pathlib import Path
import json

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


# Eventos disponíveis na Evolution API
AVAILABLE_EVENTS = [
    'MESSAGES_UPSERT',
    'MESSAGES_UPDATE',
    'MESSAGES_DELETE',
    'SEND_MESSAGE',
    'CONNECTION_UPDATE',
    'QRCODE_UPDATED',
    'GROUPS_UPSERT',
    'GROUPS_UPDATE',
    'GROUP_PARTICIPANTS_UPDATE'
]


def get_webhooks():
    """Obtém configurações atuais dos webhooks"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Obtém webhooks
    response = api.get_webhook()

    return response


def set_webhooks(url: str, events: list, by_events: bool = False, base64: bool = False):
    """
    Configura webhooks da instância

    Args:
        url: URL do webhook
        events: Lista de eventos a monitorar
        by_events: Se True, cria URL específica por evento
        base64: Se True, envia mídias em base64
    """

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Valida eventos
    invalid_events = [e for e in events if e not in AVAILABLE_EVENTS]
    if invalid_events:
        raise ValueError(f"Eventos inválidos: {', '.join(invalid_events)}")

    # Configura webhook
    response = api.set_webhook(
        webhook_url=url,
        events=events,
        webhook_by_events=by_events,
        webhook_base64=base64
    )

    return response


def main():
    parser = argparse.ArgumentParser(
        description='Gerenciar webhooks da instância WhatsApp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Eventos disponíveis:
  {'  '.join(AVAILABLE_EVENTS)}

Exemplos:
  # Ver configuração atual
  python3 scripts/whatsapp/manage_webhooks.py --action get

  # Configurar webhook (USE COM CUIDADO!)
  python3 scripts/whatsapp/manage_webhooks.py --action set \\
      --url https://seu.webhook.com/events \\
      --events MESSAGES_UPSERT,CONNECTION_UPDATE

  # Webhook com eventos separados e base64
  python3 scripts/whatsapp/manage_webhooks.py --action set \\
      --url https://seu.webhook.com/events \\
      --events MESSAGES_UPSERT,SEND_MESSAGE \\
      --by-events --base64

⚠️  AVISO: Alterar webhooks pode afetar integrações em produção!
        """
    )

    parser.add_argument('--action', '-a', required=True, choices=['get', 'set'],
                       help='Ação: get (ver) ou set (configurar)')
    parser.add_argument('--url', '-u',
                       help='URL do webhook (obrigatório para --action set)')
    parser.add_argument('--events', '-e',
                       help='Eventos separados por vírgula (obrigatório para --action set)')
    parser.add_argument('--by-events', action='store_true',
                       help='Criar webhook específico por evento')
    parser.add_argument('--base64', action='store_true',
                       help='Enviar mídias em base64')

    args = parser.parse_args()

    # Validação de argumentos para action=set
    if args.action == 'set':
        if not args.url:
            parser.error("--url é obrigatório quando --action set")
        if not args.events:
            parser.error("--events é obrigatório quando --action set")

    try:
        if args.action == 'get':
            print(f"🔍 Obtendo webhooks configurados para '{EVOLUTION_INSTANCE_NAME}'...")
            print()

            response = get_webhooks()

            print("✅ Webhooks obtidos com sucesso!")
            print()
            print("=" * 60)
            print(json.dumps(response, indent=2, ensure_ascii=False))
            print("=" * 60)

            # Resumo
            if 'url' in response:
                print()
                print("📊 Resumo da Configuração:")
                print(f"   URL: {response.get('url', 'N/A')}")
                # Tenta ambos os formatos: snake_case e camelCase
                by_events = response.get('webhook_by_events') or response.get('webhookByEvents', False)
                base64_enabled = response.get('webhook_base64') or response.get('webhookBase64', False)
                print(f"   Webhook por eventos: {by_events}")
                print(f"   Base64: {base64_enabled}")
                if 'events' in response:
                    print(f"   Eventos ({len(response['events'])}):")
                    for event in response['events']:
                        print(f"      - {event}")

            return response

        elif args.action == 'set':
            # Confirmação de segurança
            print("⚠️  ATENÇÃO: Você está prestes a MODIFICAR os webhooks da instância!")
            print()
            print(f"Instância: {EVOLUTION_INSTANCE_NAME}")
            print(f"URL: {args.url}")
            print(f"Eventos: {args.events}")
            print(f"Por eventos: {args.by_events}")
            print(f"Base64: {args.base64}")
            print()

            confirm = input("Tem certeza? Digite 'SIM' para confirmar: ")

            if confirm != 'SIM':
                print("❌ Operação cancelada pelo usuário")
                sys.exit(0)

            print()
            print("⚙️  Configurando webhooks...")

            # Parse dos eventos
            events = [e.strip() for e in args.events.split(',')]

            response = set_webhooks(
                url=args.url,
                events=events,
                by_events=args.by_events,
                base64=args.base64
            )

            print()
            print("✅ Webhooks configurados com sucesso!")
            print()
            print("=" * 60)
            print(json.dumps(response, indent=2, ensure_ascii=False))
            print("=" * 60)

            return response

    except Exception as e:
        print(f"❌ Erro ao gerenciar webhooks: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
