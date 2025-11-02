#!/usr/bin/env python3
"""
Orshot - Listar Templates Disponíveis

Lista todos templates disponíveis (pré-prontos + Studio customizados).

Uso:
    python3 scripts/orshot/list_templates.py
    python3 scripts/orshot/list_templates.py --search "certificate"
    python3 scripts/orshot/list_templates.py --studio-only
"""

import sys
import argparse
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent.parent))


def list_predefined_templates(search: str = None):
    """
    Lista templates pré-prontos do Orshot

    Args:
        search: Filtrar por termo de busca
    """

    # Templates pré-prontos conhecidos
    templates = [
        {
            'id': 'open-graph-image-1',
            'name': 'Open Graph Image',
            'description': 'OG image para blogs/sites (1200x630)',
            'params': ['title', 'description', 'image']
        },
        {
            'id': 'tweet-image-1',
            'name': 'Tweet/X Post',
            'description': 'Post estilo Twitter/X',
            'params': ['title', 'author', 'date']
        },
        {
            'id': 'instagram-post-1',
            'name': 'Instagram Post',
            'description': 'Post quadrado Instagram (1080x1080)',
            'params': ['title', 'description', 'image']
        },
        {
            'id': 'certificate-1',
            'name': 'Certificado',
            'description': 'Certificado genérico',
            'params': ['name', 'course', 'date']
        },
        {
            'id': 'website-screenshot',
            'name': 'Website Screenshot',
            'description': 'Captura de tela de website',
            'params': ['websiteUrl', 'fullCapture', 'delay', 'width', 'height']
        },
    ]

    # Filtra por busca
    if search:
        search_lower = search.lower()
        templates = [
            t for t in templates
            if search_lower in t['name'].lower()
            or search_lower in t['description'].lower()
            or search_lower in t['id'].lower()
        ]

    return templates


def list_studio_templates():
    """
    Lista templates customizados do Studio

    Nota: Requer API call real ao Orshot para listar templates do usuário.
    Por enquanto retorna placeholder.
    """

    # TODO: Implementar chamada API real
    # GET https://api.orshot.com/v1/templates

    print("ℹ️ Templates Studio:")
    print("   Para ver seus templates customizados do Studio:")
    print("   1. Acesse: https://orshot.com/studio")
    print("   2. Veja o ID de cada template criado")
    print("   3. Use o ID diretamente nos scripts")
    print()


def main():
    """Função principal"""

    parser = argparse.ArgumentParser(
        description='Lista templates disponíveis no Orshot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    # Listar todos
    python3 scripts/orshot/list_templates.py

    # Buscar templates de certificado
    python3 scripts/orshot/list_templates.py --search certificate

    # Buscar posts sociais
    python3 scripts/orshot/list_templates.py --search post

    # Ver apenas templates Studio
    python3 scripts/orshot/list_templates.py --studio-only
        """
    )

    parser.add_argument(
        '--search', '-s',
        help='Buscar templates por termo'
    )

    parser.add_argument(
        '--studio-only',
        action='store_true',
        help='Mostrar apenas templates Studio customizados'
    )

    args = parser.parse_args()

    print("📋 Templates Orshot\n")

    # Templates Studio
    if args.studio_only or not args.search:
        list_studio_templates()

    # Templates pré-prontos
    if not args.studio_only:
        templates = list_predefined_templates(args.search)

        if not templates:
            print(f"❌ Nenhum template encontrado para: {args.search}")
            sys.exit(1)

        print(f"✨ Templates Pré-Prontos ({len(templates)}):\n")

        for t in templates:
            print(f"  🎨 {t['name']}")
            print(f"     ID: {t['id']}")
            print(f"     Descrição: {t['description']}")
            print(f"     Parâmetros: {', '.join(t['params'])}")
            print(f"     Exemplo:")
            print(f"       python3 scripts/orshot/generate_image.py \\")
            print(f"         --template {t['id']} \\")
            print(f"         --data '{{\"title\":\"Teste\"}}'")
            print()

    print("💡 Dica: Use generate_image.py ou batch_generate.py para gerar imagens")


if __name__ == "__main__":
    main()
