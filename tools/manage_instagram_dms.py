#!/usr/bin/env python3
"""
Script para gerenciar Direct Messages (DMs) no Instagram via Instagram Graph API

Funcionalidades:
- ✅ Listar conversas (DMs)
- ✅ Ler mensagens de uma conversa
- ✅ Responder mensagens
- ✅ Marcar mensagens como lidas
- ⚠️  Nota: Só pode responder mensagens iniciadas pelo usuário (limitação da API)

Uso:
    # Listar conversas
    python3 manage_instagram_dms.py list

    # Ver mensagens de uma conversa
    python3 manage_instagram_dms.py read CONVERSATION_ID

    # Responder uma mensagem
    python3 manage_instagram_dms.py reply CONVERSATION_ID "Sua resposta"

    # Marcar conversa como lida
    python3 manage_instagram_dms.py mark-read CONVERSATION_ID
"""

import requests
import sys
import os
import argparse
import json
from datetime import datetime

# Importar configurações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import instagram_config as config


class InstagramDMManager:
    """Classe para gerenciar Direct Messages no Instagram"""

    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.endpoints = config.ENDPOINTS

    def list_conversations(self, limit=25):
        """Lista conversas (DMs)"""
        print("💬 CONVERSAS (DMs)")
        print("=" * 60)
        print(f"📱 Conta: @{config.INSTAGRAM_USERNAME}")
        print(f"📋 Últimas {limit} conversas")
        print("=" * 60)

        try:
            response = requests.get(
                f"{self.endpoints['get_media']}/{self.user_id}/conversations",
                params={
                    "fields": "id,participants,updated_time,message_count,unread_count,messages{message,from,created_time}",
                    "limit": limit,
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            conversations = data.get("data", [])

            if not conversations:
                print("\n📭 Nenhuma conversa encontrada")
                return []

            print(f"\n✅ Encontradas {len(conversations)} conversas:\n")

            for i, conv in enumerate(conversations, 1):
                conv_id = conv.get("id")
                participants = conv.get("participants", {}).get("data", [])
                updated_time = conv.get("updated_time", "")
                message_count = conv.get("message_count", 0)
                unread_count = conv.get("unread_count", 0)
                messages = conv.get("messages", {}).get("data", [])

                # Formatar timestamp
                if updated_time:
                    try:
                        dt = datetime.fromisoformat(updated_time.replace('Z', '+00:00'))
                        time_str = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        from datetime import datetime as dt_module
                        dt = dt_module.strptime(updated_time, "%Y-%m-%dT%H:%M:%S%z")
                        time_str = dt.strftime("%d/%m/%Y %H:%M")
                else:
                    time_str = "N/A"

                # Obter nome dos participantes
                participant_names = []
                for p in participants:
                    username = p.get("username", "Unknown")
                    participant_names.append(f"@{username}")

                # Última mensagem
                last_message = messages[0].get("message", "...") if messages else "Sem mensagens"
                last_message_preview = last_message[:50] + "..." if len(last_message) > 50 else last_message

                # Status de não lidas
                status = f"🔴 {unread_count} não lida(s)" if unread_count > 0 else "✅ Lida"

                print(f"[{i}] {status}")
                print(f"    🆔 ID: {conv_id}")
                print(f"    👥 Com: {', '.join(participant_names)}")
                print(f"    💬 Mensagens: {message_count}")
                print(f"    📅 Atualizada: {time_str}")
                print(f"    📝 Última: {last_message_preview}")
                print()

            return conversations

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao listar conversas: {e}")
            if hasattr(e.response, 'text'):
                error_data = e.response.json()
                print(f"Detalhes: {error_data}")

                # Verificar se é problema de permissões/capacidade
                error_str = str(error_data).lower()
                if "capability" in error_str or "permissions" in error_str or "oauth" in error_str:
                    print("\n" + "=" * 60)
                    print("⚠️  PERMISSÕES NECESSÁRIAS NÃO CONFIGURADAS")
                    print("=" * 60)
                    print("\nEsta funcionalidade requer:")
                    print("  ✓ Permissão: instagram_manage_messages")
                    print("  ✓ Permissão: pages_manage_metadata")
                    print("  ✓ Conta Instagram Business/Creator")
                    print("  ✓ Conectada a uma Página do Facebook")
                    print("\nComo configurar:")
                    print("  1. Acesse: developers.facebook.com/apps")
                    print("  2. Selecione seu App")
                    print("  3. Vá em: Permissões e Recursos")
                    print("  4. Solicite as permissões acima")
                    print("  5. Conecte sua conta Instagram a uma Página do Facebook")
                    print("  6. Gere novo Access Token com as permissões")
                    print("=" * 60)
            return []
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def read_messages(self, conversation_id, limit=25):
        """Lê mensagens de uma conversa"""
        print(f"💬 MENSAGENS DA CONVERSA")
        print("=" * 60)
        print(f"🆔 Conversa ID: {conversation_id}")
        print("=" * 60)

        try:
            response = requests.get(
                f"{self.endpoints['get_media']}/{conversation_id}",
                params={
                    "fields": "participants,messages{message,from,created_time,id}",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            participants = data.get("participants", {}).get("data", [])
            messages_data = data.get("messages", {}).get("data", [])

            # Informações dos participantes
            print("\n👥 PARTICIPANTES:")
            for p in participants:
                username = p.get("username", "Unknown")
                user_id = p.get("id", "N/A")
                print(f"   @{username} (ID: {user_id})")

            if not messages_data:
                print("\n📭 Nenhuma mensagem encontrada")
                return []

            print(f"\n✅ Mensagens ({len(messages_data)}):\n")

            # Ordenar mensagens por data (mais antigas primeiro)
            messages_data.reverse()

            for i, msg in enumerate(messages_data, 1):
                message_id = msg.get("id")
                message_text = msg.get("message", "[Sem texto]")
                created_time = msg.get("created_time", "")
                from_data = msg.get("from", {})
                from_username = from_data.get("username", "Unknown")
                from_id = from_data.get("id", "")

                # Formatar timestamp
                if created_time:
                    try:
                        dt = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                        time_str = dt.strftime("%d/%m %H:%M")
                    except:
                        from datetime import datetime as dt_module
                        dt = dt_module.strptime(created_time, "%Y-%m-%dT%H:%M:%S%z")
                        time_str = dt.strftime("%d/%m %H:%M")
                else:
                    time_str = "N/A"

                # Identificar se é sua mensagem ou do outro
                is_you = from_id == self.user_id
                sender = "Você" if is_you else f"@{from_username}"
                arrow = "→" if is_you else "←"

                print(f"[{i}] {arrow} {sender} ({time_str})")
                print(f"    {message_text}")
                print()

            return messages_data

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao ler mensagens: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return []
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def send_message(self, conversation_id, message):
        """Envia uma mensagem em uma conversa"""
        print(f"📤 ENVIANDO MENSAGEM")
        print("=" * 60)

        if len(message) > 1000:
            print("❌ Mensagem muito longa. Máximo: 1000 caracteres")
            return False

        try:
            # Endpoint para enviar mensagens
            response = requests.post(
                f"{self.endpoints['get_media']}/{conversation_id}/messages",
                params={
                    "message": message,
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            message_id = data.get("id")

            if not message_id:
                print("❌ Falha ao enviar mensagem")
                print(f"Resposta da API: {data}")
                return False

            print("✅ Mensagem enviada com sucesso!")
            print(f"🆔 Message ID: {message_id}")
            print(f"💬 Mensagem: {message}")

            return True

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            if hasattr(e.response, 'text'):
                error_data = e.response.json()
                print(f"Detalhes: {error_data}")

                # Mensagens de erro comuns
                error_message = str(error_data)
                if "24-hour window" in error_message or "outside the 24" in error_message:
                    print("\n⚠️  LIMITAÇÃO DA API:")
                    print("   Você só pode responder dentro de 24 horas após a última mensagem do usuário.")
                    print("   Depois disso, apenas respostas de template são permitidas.")
                elif "permission" in error_message.lower():
                    print("\n⚠️  Permissões insuficientes. Verifique:")
                    print("   - instagram_manage_messages")
                    print("   - pages_manage_metadata")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def mark_as_read(self, conversation_id):
        """Marca uma conversa como lida"""
        print(f"✅ MARCANDO COMO LIDA")
        print("=" * 60)

        try:
            response = requests.post(
                f"{self.endpoints['get_media']}/{conversation_id}",
                params={
                    "is_read": "true",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            success = data.get("success", False)

            if success:
                print("✅ Conversa marcada como lida!")
                return True
            else:
                print("❌ Falha ao marcar como lida")
                print(f"Resposta da API: {data}")
                return False

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao marcar como lida: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Gerenciar Direct Messages (DMs) no Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Listar conversas
  python3 manage_instagram_dms.py list

  # Listar mais conversas (até 100)
  python3 manage_instagram_dms.py list --limit 50

  # Ler mensagens de uma conversa
  python3 manage_instagram_dms.py read CONVERSATION_ID

  # Responder uma mensagem
  python3 manage_instagram_dms.py reply CONVERSATION_ID "Obrigado pela mensagem!"

  # Marcar conversa como lida
  python3 manage_instagram_dms.py mark-read CONVERSATION_ID

⚠️  LIMITAÇÕES IMPORTANTES DA API:
  - Requer permissões: instagram_manage_messages, pages_manage_metadata
  - Conta Business/Creator conectada a uma Página do Facebook
  - Só pode responder mensagens iniciadas pelo usuário
  - Janela de resposta: 24 horas (após isso, apenas templates)
  - Não pode iniciar conversas proativamente

Notas:
  - Para configurar permissões: Facebook Developers > Seu App > Permissões
  - Conecte sua conta Instagram a uma Página do Facebook
  - Esta funcionalidade é limitada pela API do Instagram
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Ação a executar")

    # Subcomando: list
    parser_list = subparsers.add_parser("list", help="Listar conversas")
    parser_list.add_argument("--limit", type=int, default=25, help="Número de conversas (padrão: 25)")

    # Subcomando: read
    parser_read = subparsers.add_parser("read", help="Ler mensagens de uma conversa")
    parser_read.add_argument("conversation_id", help="ID da conversa")
    parser_read.add_argument("--limit", type=int, default=25, help="Número de mensagens (padrão: 25)")

    # Subcomando: reply
    parser_reply = subparsers.add_parser("reply", help="Responder uma mensagem")
    parser_reply.add_argument("conversation_id", help="ID da conversa")
    parser_reply.add_argument("message", help="Texto da mensagem")

    # Subcomando: mark-read
    parser_mark = subparsers.add_parser("mark-read", help="Marcar conversa como lida")
    parser_mark.add_argument("conversation_id", help="ID da conversa")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Criar manager
    manager = InstagramDMManager()

    # Executar comando
    success = False

    if args.command == "list":
        conversations = manager.list_conversations(args.limit)
        success = len(conversations) >= 0

    elif args.command == "read":
        messages = manager.read_messages(args.conversation_id, args.limit)
        success = len(messages) >= 0

    elif args.command == "reply":
        success = manager.send_message(args.conversation_id, args.message)

    elif args.command == "mark-read":
        success = manager.mark_as_read(args.conversation_id)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
