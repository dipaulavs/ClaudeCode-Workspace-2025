#!/usr/bin/env python3
"""
Calculadora de Precificação - Calcula preço baseado em valor e ROI

Usa metodologia da skill orcamento-profissional para:
1. Calcular valor gerado para o cliente
2. Sugerir preço justo (2-10% do valor)
3. Aplicar valores quebrados (terminam em 7 ou 9)
4. Criar ancoragem com descontos nomeados
5. Calcular ROI, payback e comparações
"""

import sys
from typing import Dict, Tuple


def calcular_valor_gerado(
    receita_nova_mes: float = 0,
    economia_custos_mes: float = 0,
    horas_economizadas_mes: float = 0,
    valor_hora_cliente: float = 0,
    custo_oportunidade_mes: float = 0
) -> float:
    """
    Calcula valor total gerado para o cliente no ano 1

    Args:
        receita_nova_mes: Nova receita mensal gerada
        economia_custos_mes: Economia mensal de custos
        horas_economizadas_mes: Horas economizadas por mês
        valor_hora_cliente: Valor/hora do tempo do cliente
        custo_oportunidade_mes: Custo de oportunidade mensal

    Returns:
        Valor total anual gerado
    """
    valor_tempo_mes = horas_economizadas_mes * valor_hora_cliente

    valor_total_mes = (
        receita_nova_mes +
        economia_custos_mes +
        valor_tempo_mes +
        custo_oportunidade_mes
    )

    return valor_total_mes * 12  # Anualizar


def calcular_preco_base(valor_gerado_ano: float, percentual: float = 5.0) -> float:
    """
    Calcula preço base (2-10% do valor gerado)

    Args:
        valor_gerado_ano: Valor gerado no primeiro ano
        percentual: Percentual do valor (2-10%)

    Returns:
        Preço base calculado
    """
    return valor_gerado_ano * (percentual / 100)


def aplicar_valor_quebrado(preco: float) -> int:
    """
    Ajusta preço para terminar em 7 ou 9 (psicologia de preços)

    Args:
        preco: Preço original

    Returns:
        Preço ajustado terminando em 7 ou 9
    """
    preco_int = int(preco)
    ultimo_digito = preco_int % 10

    # Se já termina em 7 ou 9, manter
    if ultimo_digito in [7, 9]:
        return preco_int

    # Preferir 7 (mais natural que 9 para valores médios/altos)
    return (preco_int // 10) * 10 + 7


def criar_ancoragem(preco_base: int) -> Dict[str, int]:
    """
    Cria ancoragem alta (+37%) com descontos nomeados

    Args:
        preco_base: Preço base desejado

    Returns:
        Dict com ancoragem, descontos e preço final
    """
    # Ancoragem 37% maior
    ancoragem = int(preco_base * 1.37)
    ancoragem = aplicar_valor_quebrado(ancoragem)

    # Descontos nomeados (soma = diferença entre ancoragem e base)
    desconto_total = ancoragem - preco_base

    # Dividir em 2 descontos
    desconto_1 = int(desconto_total * 0.6)  # 60% do desconto
    desconto_2 = desconto_total - desconto_1  # 40% restante

    # Ajustar desconto_2 para número "bonito"
    desconto_2 = (desconto_2 // 10) * 10 + (4 if desconto_2 % 10 >= 5 else 4)

    # Recalcular preço final com descontos
    preco_final = ancoragem - desconto_1 - desconto_2

    return {
        "tabela": ancoragem,
        "desconto_parceria": desconto_1,
        "desconto_combo": desconto_2,
        "investimento_final": preco_final,
        "economia_total": desconto_1 + desconto_2
    }


def calcular_roi(investimento: float, retorno_anual: float) -> Dict[str, float]:
    """
    Calcula métricas de ROI

    Args:
        investimento: Investimento inicial
        retorno_anual: Retorno esperado no ano 1

    Returns:
        Dict com ROI, payback e lucro
    """
    lucro = retorno_anual - investimento
    roi_multiplo = retorno_anual / investimento if investimento > 0 else 0
    roi_percentual = ((retorno_anual - investimento) / investimento * 100) if investimento > 0 else 0
    payback_meses = (investimento / (retorno_anual / 12)) if retorno_anual > 0 else 0
    payback_dias = payback_meses * 30

    return {
        "lucro": lucro,
        "roi_multiplo": roi_multiplo,
        "roi_percentual": roi_percentual,
        "payback_meses": payback_meses,
        "payback_dias": payback_dias
    }


def formatar_moeda(valor: float) -> str:
    """Formata valor como moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", ".")


def main():
    """CLI para cálculo de precificação"""

    print("=" * 60)
    print("CALCULADORA DE PRECIFICAÇÃO - Skill orcamento-profissional")
    print("=" * 60)
    print()

    # Coletar dados
    print("📊 COLETA DE DADOS (valores mensais, pressione Enter para 0)")
    print()

    try:
        receita_nova = float(input("Receita nova/mês (R$): ") or 0)
        economia_custos = float(input("Economia custos/mês (R$): ") or 0)
        horas_economizadas = float(input("Horas economizadas/mês: ") or 0)
        valor_hora = float(input("Valor/hora cliente (R$): ") or 0)
        custo_oportunidade = float(input("Custo oportunidade/mês (R$): ") or 0)

        percentual_valor = float(input("\n% do valor a cobrar (2-10%, padrão 5): ") or 5)

    except ValueError:
        print("❌ Erro: Digite apenas números")
        sys.exit(1)

    # Calcular valor gerado
    valor_gerado = calcular_valor_gerado(
        receita_nova,
        economia_custos,
        horas_economizadas,
        valor_hora,
        custo_oportunidade
    )

    # Calcular preço base
    preco_base = calcular_preco_base(valor_gerado, percentual_valor)
    preco_base_quebrado = aplicar_valor_quebrado(preco_base)

    # Criar ancoragem
    ancoragem = criar_ancoragem(preco_base_quebrado)

    # Calcular ROI
    roi = calcular_roi(preco_base_quebrado, valor_gerado)

    # RESULTADOS
    print("\n" + "=" * 60)
    print("💰 RESULTADO DA PRECIFICAÇÃO")
    print("=" * 60)

    print(f"\n1️⃣ VALOR GERADO PARA O CLIENTE (ANO 1)")
    print(f"   Receita nova: {formatar_moeda(receita_nova * 12)}")
    print(f"   Economia custos: {formatar_moeda(economia_custos * 12)}")
    print(f"   Valor do tempo: {formatar_moeda(horas_economizadas * valor_hora * 12)}")
    print(f"   Custo oportunidade: {formatar_moeda(custo_oportunidade * 12)}")
    print(f"   {'─' * 55}")
    print(f"   TOTAL ANUAL: {formatar_moeda(valor_gerado)}")

    print(f"\n2️⃣ PRECIFICAÇÃO SUGERIDA")
    print(f"   Preço base ({percentual_valor}%): {formatar_moeda(preco_base)}")
    print(f"   Valor quebrado: {formatar_moeda(preco_base_quebrado)}")

    print(f"\n3️⃣ ANCORAGEM COM DESCONTOS")
    print(f"   TABELA EMPRESAS: {formatar_moeda(ancoragem['tabela'])}")
    print(f"   ├─ Desconto parceria: -{formatar_moeda(ancoragem['desconto_parceria'])}")
    print(f"   ├─ Desconto combo: -{formatar_moeda(ancoragem['desconto_combo'])}")
    print(f"   └─ INVESTIMENTO FINAL: {formatar_moeda(ancoragem['investimento_final'])} ⭐")
    print(f"")
    print(f"   Economia: {formatar_moeda(ancoragem['economia_total'])} ({ancoragem['economia_total']/ancoragem['tabela']*100:.0f}%)")

    print(f"\n4️⃣ ROI E PAYBACK")
    print(f"   Investimento: {formatar_moeda(preco_base_quebrado)}")
    print(f"   Retorno ano 1: {formatar_moeda(valor_gerado)}")
    print(f"   Lucro: {formatar_moeda(roi['lucro'])}")
    print(f"   ROI: {roi['roi_multiplo']:.1f}x ({roi['roi_percentual']:.0f}%)")
    print(f"   Payback: {roi['payback_dias']:.0f} dias ({roi['payback_meses']:.1f} meses)")

    print(f"\n5️⃣ COMPARAÇÕES (para slide de ancoragem)")
    print(f"   Vs Contratar CLT: {formatar_moeda(preco_base_quebrado)} << R$ {(3500*1.8*12):,.0f}/ano")
    print(f"   Vs Fazer manual: Libera {horas_economizadas*12:.0f}h/ano")
    print(f"   Vs Não fazer: Deixa de ganhar {formatar_moeda(valor_gerado)}/ano")

    print("\n" + "=" * 60)
    print("✅ Cálculo concluído!")
    print("=" * 60)


if __name__ == "__main__":
    main()
