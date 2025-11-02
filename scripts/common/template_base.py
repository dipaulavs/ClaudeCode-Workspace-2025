#!/usr/bin/env python3
"""
Template Base: Estrutura padrão para criar novos scripts

Este é um template genérico que pode ser copiado e adaptado para criar
novos scripts de automação rapidamente.

Uso:
    1. Copie este arquivo
    2. Renomeie para sua função (ex: minha_funcao.py)
    3. Adapte a função main() e execute_action()
    4. Adicione argumentos necessários
"""

import sys
import argparse
from pathlib import Path
from typing import Any, Dict


def execute_action(**kwargs) -> Dict[str, Any]:
    """
    Executa a ação principal do script

    Args:
        **kwargs: Argumentos variados conforme necessidade

    Returns:
        Dict com resultado da ação
    """

    # TODO: Implementar lógica aqui
    print("⚙️ Executando ação...")

    # Exemplo de processamento
    result = {
        "status": "success",
        "data": kwargs
    }

    return result


def main():
    """Função principal com parsing de argumentos"""

    parser = argparse.ArgumentParser(
        description='Descrição do script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    python3 script.py --arg1 valor1 --arg2 valor2
    python3 script.py --help
        """
    )

    # Adicione seus argumentos aqui
    parser.add_argument('--arg1', '-a', required=True, help='Descrição do argumento 1')
    parser.add_argument('--arg2', '-b', default='default', help='Descrição do argumento 2')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')

    args = parser.parse_args()

    if args.verbose:
        print(f"🔧 Modo verbose ativado")
        print(f"   Argumentos: {vars(args)}")

    print(f"🚀 Iniciando script...")

    try:
        result = execute_action(
            arg1=args.arg1,
            arg2=args.arg2
        )

        print(f"✅ Ação concluída com sucesso!")
        if args.verbose:
            print(f"   Resultado: {result}")

        return result

    except Exception as e:
        print(f"❌ Erro ao executar ação: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
