#!/usr/bin/env python3
"""
Script para gerenciar comentários no Instagram via Instagram Graph API

Funcionalidades:
- ✅ Listar comentários de um post/reel
- ✅ Responder comentários
- ✅ Deletar comentários
- ✅ Ocultar/revelar comentários
- ✅ Obter detalhes de um comentário específico

Uso:
    # Listar comentários de um post
    python3 manage_instagram_comments.py list MEDIA_ID

    # Responder um comentário
    python3 manage_instagram_comments.py reply COMMENT_ID "Sua resposta aqui"

    # Deletar um comentário
    python3 manage_instagram_comments.py delete COMMENT_ID

    # Ocultar um comentário
    python3 manage_instagram_comments.py hide COMMENT_ID

    # Revelar um comentário
    python3 manage_instagram_comments.py unhide COMMENT_ID

    # Ver detalhes de um comentário
    python3 manage_instagram_comments.py get COMMENT_ID
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


class InstagramCommentManager:
    """Classe para gerenciar comentários no Instagram"""

    def __init__(self):
        self.user_id = config.INSTAGRAM_USER_ID
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.endpoints = config.ENDPOINTS

    def list_comments(self, media_id, limit=50):
        """Lista comentários de um post"""
        print(f"📝 Listando comentários do post {media_id}...")
        print("=" * 60)

        try:
            response = requests.get(
                f"{self.endpoints['get_media']}/{media_id}/comments",
                params={
                    "fields": "id,text,username,timestamp,like_count,replies_count,hidden",
                    "limit": limit,
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            comments = data.get("data", [])

            if not comments:
                print("📭 Nenhum comentário encontrado neste post")
                return []

            print(f"✅ Encontrados {len(comments)} comentários:\n")

            for i, comment in enumerate(comments, 1):
                username = comment.get("username", "Unknown")
                text = comment.get("text", "")
                comment_id = comment.get("id")
                timestamp = comment.get("timestamp", "")
                like_count = comment.get("like_count", 0)
                replies_count = comment.get("replies_count", 0)
                hidden = comment.get("hidden", False)

                # Formatar timestamp
                if timestamp:
                    try:
                        # Tentar formato padrão primeiro
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        # Formato alternativo do Instagram: 2025-10-31T21:52:50+0000
                        from datetime import datetime as dt_module
                        dt = dt_module.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
                        timestamp_str = dt.strftime("%d/%m/%Y %H:%M")
                else:
                    timestamp_str = "N/A"

                status = "🚫 OCULTO" if hidden else "👁️  VISÍVEL"

                print(f"[{i}] {status}")
                print(f"    👤 @{username}")
                print(f"    💬 {text}")
                print(f"    🆔 ID: {comment_id}")
                print(f"    📅 {timestamp_str}")
                print(f"    ❤️  {like_count} curtidas | 💭 {replies_count} respostas")
                print()

            return comments

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao listar comentários: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return []
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    def get_comment(self, comment_id):
        """Obtém detalhes de um comentário específico"""
        print(f"🔍 Buscando comentário {comment_id}...")
        print("=" * 60)

        try:
            response = requests.get(
                f"{self.endpoints['get_media']}/{comment_id}",
                params={
                    "fields": "id,text,username,timestamp,like_count,replies_count,hidden,media",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            comment = response.json()

            username = comment.get("username", "Unknown")
            text = comment.get("text", "")
            timestamp = comment.get("timestamp", "")
            like_count = comment.get("like_count", 0)
            replies_count = comment.get("replies_count", 0)
            hidden = comment.get("hidden", False)
            media_id = comment.get("media", {}).get("id", "N/A")

            # Formatar timestamp
            if timestamp:
                try:
                    # Tentar formato padrão primeiro
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp_str = dt.strftime("%d/%m/%Y %H:%M:%S")
                except:
                    # Formato alternativo do Instagram: 2025-10-31T21:52:50+0000
                    from datetime import datetime as dt_module
                    dt = dt_module.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
                    timestamp_str = dt.strftime("%d/%m/%Y %H:%M:%S")
            else:
                timestamp_str = "N/A"

            status = "🚫 OCULTO" if hidden else "👁️  VISÍVEL"

            print(f"✅ Comentário encontrado:\n")
            print(f"Status: {status}")
            print(f"👤 Autor: @{username}")
            print(f"💬 Texto: {text}")
            print(f"🆔 Comment ID: {comment_id}")
            print(f"📝 Post ID: {media_id}")
            print(f"📅 Data: {timestamp_str}")
            print(f"❤️  Curtidas: {like_count}")
            print(f"💭 Respostas: {replies_count}")

            return comment

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao buscar comentário: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None

    def reply_comment(self, comment_id, message):
        """Responde um comentário"""
        print(f"💬 Respondendo comentário {comment_id}...")
        print("=" * 60)

        if len(message) > config.MEDIA_CONFIG["max_caption_length"]:
            print(f"❌ Resposta muito longa. Máximo: {config.MEDIA_CONFIG['max_caption_length']} caracteres")
            return False

        try:
            response = requests.post(
                f"{self.endpoints['get_media']}/{comment_id}/replies",
                params={
                    "message": message,
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            reply_id = data.get("id")

            if not reply_id:
                print("❌ Falha ao criar resposta")
                print(f"Resposta da API: {data}")
                return False

            print("✅ Resposta publicada com sucesso!")
            print(f"🆔 Reply ID: {reply_id}")
            print(f"💬 Mensagem: {message}")

            return True

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao responder comentário: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def delete_comment(self, comment_id):
        """Deleta um comentário"""
        print(f"🗑️  Deletando comentário {comment_id}...")
        print("=" * 60)

        try:
            response = requests.delete(
                f"{self.endpoints['get_media']}/{comment_id}",
                params={"access_token": self.access_token}
            )
            response.raise_for_status()

            data = response.json()
            success = data.get("success", False)

            if success:
                print("✅ Comentário deletado com sucesso!")
                return True
            else:
                print("❌ Falha ao deletar comentário")
                print(f"Resposta da API: {data}")
                return False

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao deletar comentário: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def hide_comment(self, comment_id):
        """Oculta um comentário"""
        print(f"🚫 Ocultando comentário {comment_id}...")
        print("=" * 60)

        try:
            response = requests.post(
                f"{self.endpoints['get_media']}/{comment_id}",
                params={
                    "hide": "true",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            success = data.get("success", False)

            if success:
                print("✅ Comentário ocultado com sucesso!")
                print("ℹ️  O comentário continua existindo, mas não aparece publicamente")
                return True
            else:
                print("❌ Falha ao ocultar comentário")
                print(f"Resposta da API: {data}")
                return False

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao ocultar comentário: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def unhide_comment(self, comment_id):
        """Revela um comentário oculto"""
        print(f"👁️  Revelando comentário {comment_id}...")
        print("=" * 60)

        try:
            response = requests.post(
                f"{self.endpoints['get_media']}/{comment_id}",
                params={
                    "hide": "false",
                    "access_token": self.access_token
                }
            )
            response.raise_for_status()

            data = response.json()
            success = data.get("success", False)

            if success:
                print("✅ Comentário revelado com sucesso!")
                print("ℹ️  O comentário voltou a aparecer publicamente")
                return True
            else:
                print("❌ Falha ao revelar comentário")
                print(f"Resposta da API: {data}")
                return False

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro ao revelar comentário: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Gerenciar comentários no Instagram via API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Listar comentários de um post
  python3 manage_instagram_comments.py list 18083282260953214

  # Listar mais comentários (até 100)
  python3 manage_instagram_comments.py list 18083282260953214 --limit 100

  # Ver detalhes de um comentário
  python3 manage_instagram_comments.py get 17890123456789012

  # Responder um comentário
  python3 manage_instagram_comments.py reply 17890123456789012 "Obrigado pelo comentário!"

  # Ocultar um comentário
  python3 manage_instagram_comments.py hide 17890123456789012

  # Revelar um comentário oculto
  python3 manage_instagram_comments.py unhide 17890123456789012

  # Deletar um comentário
  python3 manage_instagram_comments.py delete 17890123456789012

Notas:
  - Para listar comentários, use o MEDIA_ID (ID do post/reel)
  - Para outras ações, use o COMMENT_ID (ID do comentário)
  - Comentários ocultos não aparecem publicamente, mas não são deletados
  - Apenas o dono da conta pode moderar comentários
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Ação a executar")

    # Subcomando: list
    parser_list = subparsers.add_parser("list", help="Listar comentários de um post")
    parser_list.add_argument("media_id", help="ID do post/reel")
    parser_list.add_argument("--limit", type=int, default=50, help="Número máximo de comentários (padrão: 50)")

    # Subcomando: get
    parser_get = subparsers.add_parser("get", help="Obter detalhes de um comentário")
    parser_get.add_argument("comment_id", help="ID do comentário")

    # Subcomando: reply
    parser_reply = subparsers.add_parser("reply", help="Responder um comentário")
    parser_reply.add_argument("comment_id", help="ID do comentário")
    parser_reply.add_argument("message", help="Texto da resposta")

    # Subcomando: delete
    parser_delete = subparsers.add_parser("delete", help="Deletar um comentário")
    parser_delete.add_argument("comment_id", help="ID do comentário")

    # Subcomando: hide
    parser_hide = subparsers.add_parser("hide", help="Ocultar um comentário")
    parser_hide.add_argument("comment_id", help="ID do comentário")

    # Subcomando: unhide
    parser_unhide = subparsers.add_parser("unhide", help="Revelar um comentário")
    parser_unhide.add_argument("comment_id", help="ID do comentário")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Criar manager
    manager = InstagramCommentManager()

    # Executar comando
    success = False

    if args.command == "list":
        comments = manager.list_comments(args.media_id, args.limit)
        success = len(comments) >= 0

    elif args.command == "get":
        comment = manager.get_comment(args.comment_id)
        success = comment is not None

    elif args.command == "reply":
        success = manager.reply_comment(args.comment_id, args.message)

    elif args.command == "delete":
        success = manager.delete_comment(args.comment_id)

    elif args.command == "hide":
        success = manager.hide_comment(args.comment_id)

    elif args.command == "unhide":
        success = manager.unhide_comment(args.comment_id)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
