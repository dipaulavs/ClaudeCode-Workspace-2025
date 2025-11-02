#!/usr/bin/env python3
"""
Template: Gerenciar comentários do Instagram

Uso:
    # Listar comentários de um post
    python3 scripts/instagram/manage_comments.py --list MEDIA_ID --limit 50

    # Responder comentário
    python3 scripts/instagram/manage_comments.py --reply COMMENT_ID --text "Obrigado!"

    # Deletar comentário
    python3 scripts/instagram/manage_comments.py --delete COMMENT_ID

    # Ocultar comentário
    python3 scripts/instagram/manage_comments.py --hide COMMENT_ID

    # Revelar comentário
    python3 scripts/instagram/manage_comments.py --unhide COMMENT_ID

    # Obter detalhes de comentário
    python3 scripts/instagram/manage_comments.py --get COMMENT_ID
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.manage_instagram_comments import InstagramCommentManager


def manage_comments(action: str, item_id: str, text: str = None, limit: int = 50):
    """
    Gerencia comentários do Instagram

    Args:
        action: Ação a executar ('list', 'reply', 'delete', 'hide', 'unhide', 'get')
        item_id: ID do post (list) ou ID do comentário (outras ações)
        text: Texto da resposta (necessário se action='reply')
        limit: Quantidade de comentários a listar (padrão: 50)

    Returns:
        dict/list: Resultado da operação
    """

    # Inicializa manager
    manager = InstagramCommentManager()

    # Executa ação
    if action == 'list':
        return manager.list_comments(item_id, limit)
    elif action == 'reply':
        if not text:
            raise ValueError("--reply requer --text")
        return manager.reply_comment(item_id, text)
    elif action == 'delete':
        return manager.delete_comment(item_id)
    elif action == 'hide':
        return manager.hide_comment(item_id)
    elif action == 'unhide':
        return manager.unhide_comment(item_id)
    elif action == 'get':
        return manager.get_comment(item_id)
    else:
        raise ValueError(f"Ação inválida: {action}")


def main():
    parser = argparse.ArgumentParser(description='Gerenciar comentários do Instagram')

    # Ações mutuamente exclusivas
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--list', metavar='MEDIA_ID', help='Listar comentários de um post')
    action_group.add_argument('--reply', metavar='COMMENT_ID', help='Responder comentário')
    action_group.add_argument('--delete', metavar='COMMENT_ID', help='Deletar comentário')
    action_group.add_argument('--hide', metavar='COMMENT_ID', help='Ocultar comentário')
    action_group.add_argument('--unhide', metavar='COMMENT_ID', help='Revelar comentário')
    action_group.add_argument('--get', metavar='COMMENT_ID', help='Obter detalhes de comentário')

    parser.add_argument('--text', '-t', help='Texto da resposta (necessário para --reply)')
    parser.add_argument('--limit', '-l', type=int, default=50, help='Quantidade de comentários (padrão: 50)')

    args = parser.parse_args()

    # Determina ação e ID
    if args.list:
        action = 'list'
        item_id = args.list
    elif args.reply:
        action = 'reply'
        item_id = args.reply
    elif args.delete:
        action = 'delete'
        item_id = args.delete
    elif args.hide:
        action = 'hide'
        item_id = args.hide
    elif args.unhide:
        action = 'unhide'
        item_id = args.unhide
    else:  # args.get
        action = 'get'
        item_id = args.get

    print(f"💬 Gerenciando comentários do Instagram...")

    try:
        result = manage_comments(action, item_id, args.text, args.limit)

        # Exibe resultado
        if action == 'list':
            print(f"✅ {len(result)} comentários listados")
            for comment in result[:5]:  # Mostra primeiros 5
                username = comment.get('username', 'N/A')
                text = comment.get('text', '')[:50]
                print(f"   @{username}: {text}...")
            if len(result) > 5:
                print(f"   ... e mais {len(result) - 5} comentários")
        elif action == 'reply':
            print(f"✅ Resposta enviada com sucesso!")
        elif action == 'delete':
            print(f"✅ Comentário deletado com sucesso!")
        elif action == 'hide':
            print(f"✅ Comentário ocultado com sucesso!")
        elif action == 'unhide':
            print(f"✅ Comentário revelado com sucesso!")
        else:  # get
            username = result.get('username', 'N/A')
            text = result.get('text', 'N/A')
            print(f"✅ Comentário de @{username}:")
            print(f"   {text}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
