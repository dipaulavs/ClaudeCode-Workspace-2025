#!/usr/bin/env python3
"""
Workflow Interativo: Carrossel Meta Ads (Estilo Hormozi)

Fluxo completo:
1. INPUT → Coleta dados do imóvel
2. PREVIEW → Mostra copy dos 3 carrosséis
3. ESCOLHA → Usuário seleciona qual carrossel
4. GERAÇÃO → Cria imagens em paralelo

Uso:
    python3 scripts/image-generation/workflow_carrossel_interativo.py
"""

import sys
import os
import subprocess
from pathlib import Path

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')


def format_currency(value):
    """Formata valor para moeda brasileira"""
    try:
        num = float(value)
        if num >= 1000:
            return f"R$ {num/1000:.0f}k"
        return f"R$ {num:,.0f}".replace(",", ".")
    except:
        return value


def coletar_dados_imovel():
    """Coleta dados do imóvel de forma interativa"""
    limpar_tela()
    print("🏠 GERADOR DE CARROSSEL META ADS - ESTILO HORMOZI")
    print("=" * 70)
    print("📊 Metodologia: Alex Hormozi (100M Offers + 100M Leads)")
    print("🎨 Visual: Colagem artesanal feita à mão")
    print("=" * 70)
    print("\n📋 PASSO 1/4: DADOS DO IMÓVEL")
    print("-" * 70)

    dados = {}
    dados['tipo'] = input("\n🏠 Tipo do imóvel (ex: Chácara 1.000m²): ").strip()
    dados['preco'] = input("💰 Preço total (ex: 70000): ").strip()
    dados['entrada'] = input("💵 Entrada (ex: 10000): ").strip()
    dados['parcela'] = input("💳 Valor da parcela mensal (ex: 1000): ").strip()
    dados['parcelas'] = input("📅 Número de parcelas (ex: 60): ").strip()
    dados['localizacao'] = input("📍 Localização (ex: Itatiaiuçu, 15min do centro): ").strip()

    print("\n📷 IMAGEM (OPCIONAL)")
    print("💡 Dica: A imagem aparece apenas no primeiro slide do carrossel")
    dados['image_url'] = input("🔗 URL da imagem (deixe em branco para pular): ").strip()
    if not dados['image_url']:
        dados['image_url'] = None

    print("\n🎨 VARIANTES")
    print("💡 Cada slide gera múltiplas versões (4-10). Mais variantes = mais opções, mas maior custo/tempo")
    while True:
        variants = input("🔢 Quantas variantes por slide? (4-10, padrão: 4): ").strip()
        if not variants:
            dados['variants'] = 4
            break
        try:
            v = int(variants)
            if 4 <= v <= 10:
                dados['variants'] = v
                break
            else:
                print("❌ Digite um número entre 4 e 10")
        except ValueError:
            print("❌ Digite um número válido")

    return dados


def mostrar_resumo_dados(dados):
    """Mostra resumo dos dados coletados"""
    print("\n✅ DADOS COLETADOS:")
    print(f"   • Tipo: {dados['tipo']}")
    print(f"   • Preço: {format_currency(dados['preco'])}")
    print(f"   • Entrada: {format_currency(dados['entrada'])}")
    print(f"   • Parcela: {format_currency(dados['parcela'])} x {dados['parcelas']}x")
    print(f"   • Localização: {dados['localizacao']}")
    if dados['image_url']:
        print(f"   • Imagem: Sim ({dados['image_url'][:40]}...)")
    else:
        print(f"   • Imagem: Não")
    print(f"   • Variantes por slide: {dados['variants']}")


def gerar_preview_carrossel1(dados):
    """Gera preview do Carrossel 1: Matemática Brutal (primeiros 5 slides)"""
    entrada = format_currency(dados['entrada'])
    parcela = format_currency(dados['parcela'])
    total_investido = float(dados['entrada']) + (float(dados['parcela']) * int(dados['parcelas']))

    preview = f"""
╔══════════════════════════════════════════════════════════════════╗
║  CARROSSEL 1: MATEMÁTICA BRUTAL (10 slides)                      ║
╚══════════════════════════════════════════════════════════════════╝

📊 ESTRUTURA: Comparação direta aluguel vs imóvel
🎯 MELHOR PARA: Público geral, primeira campanha
🔥 FORÇA: Matemática brutal e comparação lado a lado

─────────────────────────────────────────────────────────────────

📄 SLIDE 1 - HOOK
   "VOCÊ VAI PAGAR {parcela}/MÊS PELOS PRÓXIMOS {int(dados['parcelas'])//12} ANOS
    DE QUALQUER JEITO."

   "A pergunta é: pra quem?"
   "Aluguel ou patrimônio? Você decide."

─────────────────────────────────────────────────────────────────

📄 SLIDE 2 - CREDIBILIDADE
   "Levei 23 famílias de 'pagando aluguel' para 'dona de terra'"
   "Nos últimos 6 meses."

   ✅ Nome comprometido
   ✅ Banco negou
   ✅ Sem entrada grande

─────────────────────────────────────────────────────────────────

📄 SLIDE 3 - OPÇÃO 1: ALUGUEL (com perdas)
   Parcela: {parcela}/mês
   Total pago: {format_currency(float(dados['parcela']) * int(dados['parcelas']))}

   RESULTADO:
   ❌ Zero patrimônio
   ❌ Continua pagando
   ❌ Nada pra deixar pros filhos

─────────────────────────────────────────────────────────────────

📄 SLIDE 4 - OPÇÃO 2: {dados['tipo'].upper()} (com ganhos)
   Entrada: {entrada}
   Parcela: {parcela}/mês
   Total: {format_currency(total_investido)}

   RESULTADO:
   ✅ {dados['tipo']} SEU
   ✅ Valendo {format_currency(float(dados['preco']) * 1.5)}+
   ✅ Patrimônio pros filhos

─────────────────────────────────────────────────────────────────

📄 SLIDE 5 - COMPARAÇÃO LADO A LADO
   MESMA DOR MENSAL | RESULTADOS OPOSTOS

   ALUGUEL: {parcela}/mês → R$ 0 em {int(dados['parcelas'])//12} anos
   {dados['tipo'].upper()}: {parcela}/mês → {format_currency(float(dados['preco']) * 1.5)} em {int(dados['parcelas'])//12} anos

   "É matemática. Não opinião."

─────────────────────────────────────────────────────────────────

📄 SLIDES 6-10: Sem Banco | Sem Juros | Value Stack | Recap | CTA
"""
    return preview


def gerar_preview_carrossel2(dados):
    """Gera preview do Carrossel 2: Objeção Nome Sujo (primeiros 5 slides)"""
    entrada = format_currency(dados['entrada'])
    parcela = format_currency(dados['parcela'])

    preview = f"""
╔══════════════════════════════════════════════════════════════════╗
║  CARROSSEL 2: OBJEÇÃO "NOME SUJO" (8 slides)                     ║
╚══════════════════════════════════════════════════════════════════╝

📊 ESTRUTURA: Destrói objeção principal (nome sujo)
🎯 MELHOR PARA: Pessoas com restrição de crédito
🔥 FORÇA: Empatia + Casos reais + Dignidade

─────────────────────────────────────────────────────────────────

📄 SLIDE 1 - HOOK
   "NÃO CONSIGO COMPRAR, MEU NOME TÁ SUJO"

   "Escuto isso 10 vezes por dia."
   "E minha resposta é sempre a mesma:"

─────────────────────────────────────────────────────────────────

📄 SLIDE 2 - REFRAME
   "ERRADO."

   "Você não consegue comprar NO BANCO."
   "Mas aqui? Não tem banco."

   ❌ Score alto obrigatório
   ❌ Juros de 12-18% ao ano
   ❌ Demora 60 dias pra negar

─────────────────────────────────────────────────────────────────

📄 SLIDE 3 - CASOS REAIS
   "ONTEM FECHEI 3 UNIDADES EM 47 MINUTOS"

   João, 34 anos: SPC há 2 anos → ✅ Comprou
   Maria, 41 anos: Serasa vermelho → ✅ Comprou
   Carlos, 29 anos: Score 195 → ✅ Comprou

─────────────────────────────────────────────────────────────────

📄 SLIDE 4 - O QUE ELES TINHAM
   ✅ {entrada} guardados
   ✅ Capacidade de pagar {parcela}/mês
   ✅ Cansados de pagar aluguel

   O QUE NÃO PRECISARAM:
   ❌ Score alto
   ❌ Aprovação bancária
   ❌ Fiador

─────────────────────────────────────────────────────────────────

📄 SLIDE 5 - MATEMÁTICA
   "Você JÁ paga {parcela}/mês de aluguel, certo?"

   ALUGUEL: {format_currency(float(dados['parcela']) * int(dados['parcelas']))} → ZERO patrimônio
   {dados['tipo'].upper()}: {format_currency(float(dados['parcela']) * int(dados['parcelas']))} → Imóvel valendo {format_currency(float(dados['preco']) * 1.5)}+

   "MESMA DOR. Só muda o resultado."

─────────────────────────────────────────────────────────────────

📄 SLIDES 6-8: Sem Barreiras | Dignidade | CTA Qualificado
"""
    return preview


def gerar_preview_carrossel3(dados):
    """Gera preview do Carrossel 3: Custo de Não Agir (primeiros 5 slides)"""
    parcela = format_currency(dados['parcela'])

    preview = f"""
╔══════════════════════════════════════════════════════════════════╗
║  CARROSSEL 3: CUSTO DE NÃO AGIR (7 slides)                       ║
╚══════════════════════════════════════════════════════════════════╝

📊 ESTRUTURA: Foca na dor da perda acumulada
🎯 MELHOR PARA: Indecisos, procrastinadores
🔥 FORÇA: Dor > Ganho (move mais que promessa)

─────────────────────────────────────────────────────────────────

📄 SLIDE 1 - HOOK
   "CADA MÊS QUE VOCÊ NÃO COMPRA IMÓVEL"

   "VOCÊ PERDE R$ 3.000"

   "Deixa eu te mostrar como isso acontece:"

─────────────────────────────────────────────────────────────────

📄 SLIDE 2 - PERDA #1: ALUGUEL
   Você paga: {parcela}
   Todo mês. Todo ano.

   Em 12 meses: {format_currency(float(dados['parcela']) * 12)}

   "Esse dinheiro vai pro bolso do dono do imóvel."
   "Ele tá comprando outro imóvel com SEU dinheiro."

─────────────────────────────────────────────────────────────────

📄 SLIDE 3 - PERDA #2: VALORIZAÇÃO
   Imóvel valoriza 2-3% ao mês nessa região.

   Se vale {format_currency(dados['preco'])} hoje...
   Em 1 ano: {format_currency(float(dados['preco']) * 1.26)}

   "Você perdeu R$ 26k de valorização
    que poderia ser SUA."

─────────────────────────────────────────────────────────────────

📄 SLIDE 4 - PERDA #3: INFLAÇÃO
   Seus R$ 10k guardados na poupança...
   Perdem 4-5% ao ano pro governo.

   Em 5 anos: R$ 10.000 viram R$ 7.800 de poder de compra.

   "Enquanto isso... imóvel que valia {format_currency(dados['preco'])}
    agora vale {format_currency(float(dados['preco']) * 1.8)}."

─────────────────────────────────────────────────────────────────

📄 SLIDE 5 - TOTAL PERDIDO
   Perda #1 (Aluguel): {format_currency(float(dados['parcela']) * 12)}
   Perda #2 (Valorização): R$ 26.000
   Perda #3 (Inflação): R$ 500

   TOTAL EM 1 ANO: R$ 38.500 PERDIDOS

   "Por ficar parado. Por esperar 'o momento certo'."

─────────────────────────────────────────────────────────────────

📄 SLIDES 6-7: A Alternativa | CTA Urgência Máxima

⚠️  NOTA: Carrossel 3 ainda não está implementado na geração de imagens.
    Será adicionado em breve!
"""
    return preview


def mostrar_previews(dados):
    """Mostra preview dos 3 carrosséis e retorna escolha do usuário"""
    limpar_tela()
    print("📋 PASSO 2/4: PREVIEW DOS CARROSSÉIS")
    print("=" * 70)
    print("\n📊 Analisando dados e gerando previews dos 3 carrosséis...\n")

    input("⏎ Pressione ENTER para ver o Carrossel 1...")
    limpar_tela()
    print(gerar_preview_carrossel1(dados))
    input("\n⏎ Pressione ENTER para ver o Carrossel 2...")

    limpar_tela()
    print(gerar_preview_carrossel2(dados))
    input("\n⏎ Pressione ENTER para ver o Carrossel 3...")

    limpar_tela()
    print(gerar_preview_carrossel3(dados))

    print("\n" + "=" * 70)
    print("📋 PASSO 3/4: ESCOLHA O CARROSSEL")
    print("=" * 70)

    while True:
        escolha = input("\n🎯 Qual carrossel você quer gerar? (1, 2 ou 3): ").strip()

        if escolha == '1':
            print("\n✅ Carrossel 1 selecionado: MATEMÁTICA BRUTAL (10 slides)")
            return 1
        elif escolha == '2':
            print("\n✅ Carrossel 2 selecionado: OBJEÇÃO NOME SUJO (8 slides)")
            return 2
        elif escolha == '3':
            print("\n⚠️  AVISO: Carrossel 3 ainda não está implementado!")
            continuar = input("Deseja escolher outro? (s/n): ").strip().lower()
            if continuar not in ['s', 'sim', 'y', 'yes']:
                return None
        else:
            print("❌ Escolha inválida. Digite 1, 2 ou 3.")


def gerar_imagens(dados, tipo_carrossel):
    """Executa o script de geração de imagens"""
    limpar_tela()
    print("=" * 70)
    print("📋 PASSO 4/4: GERAÇÃO DAS IMAGENS")
    print("=" * 70)

    # Monta comando
    script_path = Path(__file__).parent / "batch_carrossel_gpt4o.py"

    cmd = [
        "python3",
        str(script_path),
        "--tipo", dados['tipo'],
        "--preco", dados['preco'],
        "--entrada", dados['entrada'],
        "--parcela", dados['parcela'],
        "--parcelas", dados['parcelas'],
        "--localizacao", dados['localizacao'],
        "--carrossel", str(tipo_carrossel),
        "--variants", str(dados['variants'])
    ]

    if dados['image_url']:
        cmd.extend(["--image-url", dados['image_url']])

    num_slides = 10 if tipo_carrossel == 1 else 8
    total_imagens = num_slides * dados['variants']

    print("\n🚀 Iniciando geração de imagens em paralelo...")
    print(f"📊 Carrossel {tipo_carrossel} ({num_slides} slides)")
    print(f"🖼️  Total de imagens: {num_slides} slides × {dados['variants']} variantes = {total_imagens} imagens")
    print()

    # Executa
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar geração: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        return False


def main():
    """Função principal - Workflow completo"""
    try:
        # Passo 1: Coletar dados
        dados = coletar_dados_imovel()

        # Mostrar resumo
        mostrar_resumo_dados(dados)
        input("\n⏎ Pressione ENTER para continuar...")

        # Passo 2 e 3: Mostrar previews e escolher
        tipo_carrossel = mostrar_previews(dados)

        if tipo_carrossel is None:
            print("\n❌ Operação cancelada")
            return 1

        # Confirmação final
        num_slides = 10 if tipo_carrossel == 1 else 8
        total_imagens = num_slides * dados['variants']
        # Custo base: $0.01/imagem aproximadamente
        custo_estimado = total_imagens * 0.01

        print("\n" + "-" * 70)
        print("🎨 PRONTO PARA GERAR!")
        print("-" * 70)
        print(f"\n📊 Carrossel: {tipo_carrossel} ({'Matemática Brutal' if tipo_carrossel == 1 else 'Objeção Nome Sujo'})")
        print(f"🖼️  Imagens: {num_slides} slides × {dados['variants']} variantes = {total_imagens} imagens")
        print(f"⏱️  Tempo estimado: ~{total_imagens//8}-{total_imagens//6} minutos")
        print(f"💰 Custo estimado: ~${custo_estimado:.2f} USD")

        confirma = input("\n🚀 Iniciar geração? (s/n): ").strip().lower()

        if confirma not in ['s', 'sim', 'y', 'yes']:
            print("\n❌ Operação cancelada")
            return 0

        # Passo 4: Gerar imagens
        sucesso = gerar_imagens(dados, tipo_carrossel)

        if sucesso:
            print("\n" + "=" * 70)
            print("✅ WORKFLOW CONCLUÍDO COM SUCESSO!")
            print("=" * 70)
            print("\n📂 Imagens salvas em: ~/Downloads")
            print(f"📝 Padrão de nome: carrossel_slide_01_v1.png até carrossel_slide_01_v{dados['variants']}.png")
            print("\n🎯 Próximos passos:")
            print(f"   1. Revisar as {dados['variants']} variantes de cada slide")
            print("   2. Escolher a melhor variante por slide")
            print("   3. Fazer upload para Meta Ads")
            print("   4. Criar campanha no Facebook Ads Manager")
            return 0
        else:
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        return 1
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
