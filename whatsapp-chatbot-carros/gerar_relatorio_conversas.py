#!/usr/bin/env python3.11
"""
📊 RELATÓRIO COMPLETO - Análise de Eficiência do Sistema Híbrido
"""

import sys
sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot-carros')

from test_conversas_reais import CONVERSAS, EstadoConversa, DecisaoIA


def analisar_conversa(conversa: dict) -> dict:
    """Analisa uma conversa e retorna métricas"""
    estado = EstadoConversa()
    decisao = DecisaoIA(estado)

    ferramentas_usadas = {"local": 0, "mcp": 0, "none": 0}
    latencia_total = 0
    decisoes = []

    for mensagem in conversa['mensagens']:
        resultado = decisao.analisar_mensagem(mensagem)
        decisoes.append({
            "mensagem": mensagem,
            "ferramenta": resultado['ferramenta'],
            "tipo": resultado['tipo'],
            "razao": resultado['razao'],
            "latencia": resultado.get('latencia', 'N/A'),
            "contexto": resultado.get('contexto', None)
        })

        ferramentas_usadas[resultado['tipo']] += 1

        if resultado['tipo'] == 'mcp':
            latencia_total += 150

    return {
        "estado_final": estado,
        "ferramentas": ferramentas_usadas,
        "latencia_total": latencia_total,
        "decisoes": decisoes
    }


def gerar_relatorio():
    """Gera relatório completo"""
    print("\n" + "="*90)
    print("📊 RELATÓRIO COMPLETO - ANÁLISE DO SISTEMA HÍBRIDO")
    print("="*90 + "\n")

    resultados = []

    for i, conversa in enumerate(CONVERSAS, 1):
        print(f"\n{'─'*90}")
        print(f"🎬 CONVERSA {i}: {conversa['titulo']}")
        print(f"{'─'*90}")
        print(f"📝 {conversa['descricao']}\n")

        analise = analisar_conversa(conversa)
        resultados.append(analise)

        # Exibe fluxo da conversa
        for j, decisao in enumerate(analise['decisoes'], 1):
            tipo_emoji = {
                'local': '⚡',
                'mcp': '🔌',
                'none': '💬'
            }
            emoji = tipo_emoji.get(decisao['tipo'], '❓')

            print(f"{j}. {emoji} \"{decisao['mensagem']}\"")
            print(f"   → {decisao['tipo'].upper()}: {decisao['ferramenta'] or 'Nenhuma'}")
            print(f"   → Razão: {decisao['razao']}")

            if decisao['contexto']:
                print(f"   → {decisao['contexto']}")
            print()

        # Métricas
        print(f"📊 MÉTRICAS:")
        print(f"   Ferramentas Locais: {analise['ferramentas']['local']}")
        print(f"   Ferramentas MCP: {analise['ferramentas']['mcp']}")
        print(f"   Conversação: {analise['ferramentas']['none']}")
        print(f"   Latência total: ~{analise['latencia_total']}ms")

        total_ferramentas = analise['ferramentas']['local'] + analise['ferramentas']['mcp']
        if total_ferramentas > 0:
            percentual_local = (analise['ferramentas']['local'] / total_ferramentas) * 100
            print(f"   Eficiência: {percentual_local:.0f}% locais")

        # Tags criadas
        if analise['estado_final'].carro_ativo:
            print(f"\n🏷️ TAG CRIADA: {analise['estado_final'].carro_ativo}")
        else:
            print(f"\n🏷️ TAG: Nenhuma")

        print()

    # Resumo global
    print("\n" + "="*90)
    print("📈 RESUMO GLOBAL")
    print("="*90 + "\n")

    total_local = sum(r['ferramentas']['local'] for r in resultados)
    total_mcp = sum(r['ferramentas']['mcp'] for r in resultados)
    total_none = sum(r['ferramentas']['none'] for r in resultados)
    latencia_global = sum(r['latencia_total'] for r in resultados)

    print(f"Total de conversas analisadas: {len(CONVERSAS)}")
    print(f"Total de mensagens: {sum(len(c['mensagens']) for c in CONVERSAS)}")
    print(f"\n🔧 FERRAMENTAS ATIVADAS:")
    print(f"   Locais (⚡ rápidas): {total_local}")
    print(f"   MCP (🔌 pesadas): {total_mcp}")
    print(f"   Conversação (💬): {total_none}")

    total_ferramentas = total_local + total_mcp
    if total_ferramentas > 0:
        percentual_local_global = (total_local / total_ferramentas) * 100
        print(f"\n✅ EFICIÊNCIA GLOBAL: {percentual_local_global:.0f}% das ferramentas foram locais")

    print(f"\n⏱️ LATÊNCIA:")
    print(f"   Total estimada: ~{latencia_global}ms")
    print(f"   Média por conversa: ~{latencia_global/len(CONVERSAS):.0f}ms")

    # Análise de uso correto
    print(f"\n🎯 ANÁLISE DE USO:")

    conversas_com_tag = sum(1 for r in resultados if r['estado_final'].carro_ativo)
    conversas_sem_tag = len(resultados) - conversas_com_tag

    print(f"   Conversas COM tag criada: {conversas_com_tag}/{len(resultados)}")
    print(f"   Conversas SEM tag: {conversas_sem_tag}/{len(resultados)}")

    # Valida uso eficiente
    print(f"\n💡 VALIDAÇÃO:")

    uso_correto = True

    # Conversa 1: Sem tag, deve usar MCP
    if resultados[0]['ferramentas']['mcp'] > 0 and not resultados[0]['estado_final'].carro_ativo:
        print(f"   ✅ Conversa 1: Usou MCP corretamente (sem tag, busca necessária)")
    else:
        print(f"   ❌ Conversa 1: Deveria usar MCP (cliente exploratório)")
        uso_correto = False

    # Conversa 2: Direto ao carro, deve usar local
    if resultados[1]['ferramentas']['local'] > resultados[1]['ferramentas']['mcp']:
        print(f"   ✅ Conversa 2: Usou LOCAL corretamente (cliente direto)")
    else:
        print(f"   ⚠️ Conversa 2: Deveria priorizar LOCAL (cliente já sabe o carro)")
        uso_correto = False

    # Conversa 3: Com tag, deve evitar MCP para consultas do carro
    if resultados[2]['estado_final'].carro_ativo:
        decisoes_com_tag = [d for d in resultados[2]['decisoes']
                            if resultados[2]['estado_final'].carro_ativo and
                            'motor' in d['mensagem'].lower() or 'consumo' in d['mensagem'].lower()]

        if any(d['tipo'] == 'local' for d in decisoes_com_tag):
            print(f"   ✅ Conversa 3: Com tag, usou LOCAL para consultas do carro")
        else:
            print(f"   ⚠️ Conversa 3: Com tag ativa, deveria usar LOCAL em vez de buscar")

    # Conversa 4: Mix apropriado
    if resultados[3]['ferramentas']['local'] > 0 and resultados[3]['ferramentas']['mcp'] > 0:
        print(f"   ✅ Conversa 4: Mix equilibrado de local + MCP")
    else:
        print(f"   ℹ️ Conversa 4: Mix de ferramentas")

    # Conversa 5: Frustração deve acionar MCP emocional
    if resultados[4]['ferramentas']['mcp'] > 0:
        print(f"   ✅ Conversa 5: Detectou frustração e usou análise de sentimento (MCP)")
    else:
        print(f"   ⚠️ Conversa 5: Deveria detectar frustração (MCP emocional)")

    print(f"\n{'='*90}")

    if uso_correto:
        print("🎉 SISTEMA HÍBRIDO FUNCIONANDO CORRETAMENTE!")
    else:
        print("⚠️ SISTEMA HÍBRIDO PRECISA DE AJUSTES")

    print(f"{'='*90}\n")


if __name__ == "__main__":
    gerar_relatorio()
