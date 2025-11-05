#!/usr/bin/env python3
"""
🔒 CONFIGURAR FILTRO DE NÚMERO
Configura quais números podem interagir com o bot
"""

import re
from pathlib import Path

def normalizar_numero(numero):
    """Remove caracteres não numéricos"""
    return re.sub(r'\D', '', numero)

def gerar_variacoes_numero(numero):
    """Gera variações do número (com e sem 9 extra)"""
    numero = normalizar_numero(numero)

    variacoes = [numero]

    # Se tem 13 dígitos (55 + DDD com 9 + número)
    if len(numero) == 13 and numero[4] == '9':
        # Adiciona versão sem o 9 extra
        numero_sem_9 = numero[:4] + numero[5:]
        variacoes.append(numero_sem_9)

    # Se tem 12 dígitos (55 + DDD sem 9 + número)
    elif len(numero) == 12:
        # Adiciona versão com o 9 extra
        numero_com_9 = numero[:4] + '9' + numero[4:]
        variacoes.append(numero_com_9)

    return list(set(variacoes))

def atualizar_middleware(numeros_permitidos):
    """Atualiza webhook_middleware com números permitidos"""

    middleware_file = Path(__file__).parent / "webhook_middleware_automaia.py"

    with open(middleware_file, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Substitui a linha de NUMEROS_PERMITIDOS
    novo_conteudo = re.sub(
        r'NUMEROS_PERMITIDOS = \[.*?\]',
        f'NUMEROS_PERMITIDOS = {numeros_permitidos}',
        conteudo,
        flags=re.DOTALL
    )

    with open(middleware_file, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)

    print(f"✅ Arquivo atualizado: {middleware_file}")

def main():
    print("=" * 70)
    print("🔒 CONFIGURAR FILTRO DE NÚMERO")
    print("=" * 70)
    print()
    print("Este script configura quais números podem interagir com o bot.")
    print("Outros números serão automaticamente ignorados.")
    print()

    numeros_finais = []

    while True:
        print("📱 Digite um número permitido (formato: 5531986549366)")
        print("   Ou deixe em branco para finalizar")
        print()
        numero = input("Número: ").strip()

        if not numero:
            if numeros_finais:
                break
            else:
                print("⚠️  Adicione pelo menos um número!")
                continue

        # Normaliza e gera variações
        variacoes = gerar_variacoes_numero(numero)

        print()
        print("✅ Variações que serão aceitas:")
        for v in variacoes:
            print(f"   • {v}")

        numeros_finais.extend(variacoes)
        print()

    # Remove duplicatas
    numeros_finais = list(set(numeros_finais))
    numeros_finais.sort()

    print()
    print("=" * 70)
    print("📋 RESUMO:")
    print("=" * 70)
    print(f"Total de números/variações permitidos: {len(numeros_finais)}")
    print()
    for num in numeros_finais:
        print(f"   ✅ {num}")
    print()

    confirma = input("Confirma configuração? (s/n): ").strip().lower()

    if confirma == 's':
        atualizar_middleware(numeros_finais)
        print()
        print("=" * 70)
        print("✅ CONFIGURAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print()
        print("⚠️  IMPORTANTE: Reinicie o bot para aplicar as mudanças:")
        print("   ./PARAR_BOT_AUTOMAIA.sh")
        print("   ./INICIAR_COM_NGROK.sh")
        print()
    else:
        print("\n❌ Configuração cancelada")

if __name__ == '__main__':
    main()
