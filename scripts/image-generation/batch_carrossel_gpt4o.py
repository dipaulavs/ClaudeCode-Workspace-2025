#!/usr/bin/env python3
"""
Template: Gerar Carrossel Meta Ads (Estilo Hormozi - Colagem Artesanal)

Workflow completo para criar carrosséis de 7-10 slides para Meta Ads no nicho de imóveis.
Usa metodologia Hormozi com visual de colagem artesanal feita à mão.
Geração 100% paralela usando ThreadPoolExecutor.

Uso:
    # Modo interativo (recomendado)
    python3 scripts/image-generation/batch_carrossel_gpt4o.py

    # Modo teste (apenas 3 slides)
    python3 scripts/image-generation/batch_carrossel_gpt4o.py --limit 3

    # Carrossel 1 completo (10 slides - Matemática Brutal)
    python3 scripts/image-generation/batch_carrossel_gpt4o.py \
        --tipo "Chácara 1.000m²" \
        --preco "70000" \
        --entrada "10000" \
        --parcela "1000" \
        --parcelas "60" \
        --localizacao "Itatiaiuçu, 15min do centro" \
        --carrossel 1 \
        --image-url "https://exemplo.com/foto.jpg"

Tipos de Carrossel:
    1 = Matemática Brutal (10 slides)
    2 = Objeção Nome Sujo (8 slides)
    3 = Custo de Não Agir (7 slides - em breve)
"""

import sys
import argparse
import time
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from generate_image_batch_gpt import create_task, check_task_status, download_image

DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Template base do prompt visual (colagem artesanal)
PROMPT_BASE = """Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre vendas de terrenos.

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

{CONTEUDO_ESPECIFICO}

Adicione ícones desenhados à mão: {ICONES}

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica."""


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
    print("🏠 DADOS DO IMÓVEL")
    print("=" * 60)

    dados = {}
    dados['tipo'] = input("Tipo do imóvel (ex: Chácara 1.000m²): ").strip()
    dados['preco'] = input("Preço total (ex: 70000): ").strip()
    dados['entrada'] = input("Entrada (ex: 10000): ").strip()
    dados['parcela'] = input("Valor da parcela (ex: 1000): ").strip()
    dados['parcelas'] = input("Número de parcelas (ex: 60): ").strip()
    dados['localizacao'] = input("Localização (ex: Itatiaiuçu, 15min do centro): ").strip()

    print("\n📷 IMAGEM (OPCIONAL)")
    dados['image_url'] = input("URL da imagem do imóvel (deixe em branco para pular): ").strip()
    if not dados['image_url']:
        dados['image_url'] = None

    return dados


def escolher_carrossel():
    """Apresenta opções de carrossel e retorna escolha do usuário"""
    print("\n🎯 ESCOLHA O TIPO DE CARROSSEL")
    print("=" * 60)
    print("\n1️⃣  MATEMÁTICA BRUTAL (10 slides)")
    print("   → Comparação direta: aluguel vs imóvel")
    print("   → Melhor para: público geral, primeira campanha\n")

    print("2️⃣  OBJEÇÃO 'NOME SUJO' (8 slides)")
    print("   → Destrói objeção principal")
    print("   → Melhor para: pessoas com restrição de crédito\n")

    print("3️⃣  CUSTO DE NÃO AGIR (7 slides)")
    print("   → Foca na dor da perda")
    print("   → Melhor para: indecisos, procrastinadores\n")

    while True:
        escolha = input("Digite o número do carrossel (1, 2 ou 3): ").strip()
        if escolha in ['1', '2', '3']:
            return int(escolha)
        print("❌ Escolha inválida. Digite 1, 2 ou 3.")


def gerar_slide1_template2(dados):
    """Gera Slide 1 usando Template 2: Colagem Vertical (textos em cima + foto embaixo)"""
    parcela = format_currency(dados['parcela'])
    entrada = format_currency(dados['entrada'])

    slide = {
        "conteudo": f"""Colagem artesanal completa em fundo de madeira clara:

PARTE SUPERIOR (60% da imagem):
Papéis coloridos colados em estilo artesanal com escrita à mão em canetinha:

"VOCÊ VAI PAGAR {parcela}/MÊS PELOS PRÓXIMOS {int(dados['parcelas'])//12} ANOS DE QUALQUER JEITO."

"A pergunta é: pra quem?"

"Aluguel ou patrimônio? Você decide."

PARTE INFERIOR (40% da imagem):
Foto do imóvel fornecido como referência, limpa e sem texto sobre ela (ou apenas com texto pequeno: "{entrada} DE ENTRADA").

RODAPÉ (centralizado):
Desenhe uma setinha para a direita (→) com texto pequeno:
"Deslize para continuar ➜" """,
        "icones": "interrogação, casinha, cifrão (desenhados à mão na parte superior)"
    }

    return slide


def gerar_slides_carrossel1(dados):
    """Gera slides do Carrossel 1: Matemática Brutal (10 slides)"""
    preco_total = format_currency(dados['preco'])
    entrada = format_currency(dados['entrada'])
    parcela = format_currency(dados['parcela'])

    # Cálculos
    total_investido = float(dados['entrada']) + (float(dados['parcela']) * int(dados['parcelas']))
    total_aluguel = float(dados['parcela']) * int(dados['parcelas'])
    economia_juros = float(dados['preco'])

    slides = [
        # Slide 1 - HOOK (LAYOUT DIVIDIDO: foto + textos)
        {
            "conteudo": f"""Layout dividido vertical em duas metades iguais:

Lado esquerdo: A foto do imóvel fornecida, limpa e sem texto sobre ela.

Lado direito: Colagem artesanal em fundo de madeira clara com papéis coloridos escritos à mão em canetinha:

"VOCÊ VAI PAGAR {parcela}/MÊS PELOS PRÓXIMOS {int(dados['parcelas'])//12} ANOS DE QUALQUER JEITO."

"A pergunta é: pra quem?"

"Aluguel ou patrimônio? Você decide."

NA PARTE DE BAIXO (centralizado):
Desenhe uma setinha para a direita (→) ou emoji de dedo apontando, com texto pequeno:
"Deslize para continuar ➜" """,
            "icones": "interrogação, casinha, cifrão (desenhados à mão no lado direito)"
        },

        # Slide 2 - CREDIBILIDADE
        {
            "conteudo": """No topo: "Levei 23 famílias de 'pagando aluguel' para 'dona de terra'"

Abaixo: "Nos últimos 6 meses."

Liste com checks verdes:
✅ Nome comprometido
✅ Banco negou
✅ Sem entrada grande

Em destaque: "Aqui está a matemática:"
""",
            "icones": "grid com 23 casinhas pequenas, check verde grande"
        },

        # Slide 3 - OPÇÃO 1: ALUGUEL
        {
            "conteudo": f"""No topo em papel vermelho: "OPÇÃO 1: ALUGUEL"

Parcela: {parcela}/mês
Duração: {dados['parcelas']} meses
Total pago: {format_currency(total_aluguel)}

RESULTADO FINAL:
❌ Zero patrimônio
❌ Continua pagando
❌ Nada pra deixar pros filhos
❌ Senhorio compra Porsche
""",
            "icones": "X's vermelhos, dinheiro voando, tristeza"
        },

        # Slide 4 - OPÇÃO 2: IMÓVEL
        {
            "conteudo": f"""No topo em papel verde: "OPÇÃO 2: {dados['tipo'].upper()}"

Entrada: {entrada}
Parcela: {parcela}/mês
Duração: {dados['parcelas']} meses
Total investido: {format_currency(total_investido)}

RESULTADO FINAL:
✅ {dados['tipo']} SEU
✅ Valendo {format_currency(float(dados['preco']) * 1.5)}+
✅ Patrimônio pros filhos
✅ Você compra o Porsche
""",
            "icones": "checks verdes dourados, casa crescendo, felicidade"
        },

        # Slide 5 - COMPARAÇÃO LADO A LADO
        {
            "conteudo": f"""No topo: "MESMA DOR MENSAL | RESULTADOS OPOSTOS"

Divida ao meio com linha vertical:

ALUGUEL (vermelho):
{parcela}/mês
↓
{int(dados['parcelas'])//12} anos depois:
R$ 0

{dados['tipo'].upper()} (verde):
{parcela}/mês
↓
{int(dados['parcelas'])//12} anos depois:
{format_currency(float(dados['preco']) * 1.5)}

Em destaque: "Diferença: {format_currency(float(dados['preco']) * 1.5)}"

Abaixo: "É matemática. Não opinião."
""",
            "icones": "balança comparando, seta pra baixo (vermelho), seta pra cima (verde)"
        },

        # Slide 6 - SEM BANCO
        {
            "conteudo": f"""No topo entre aspas grandes vermelhas: "MAS MEU NOME TÁ SUJO"

Abaixo: "Você não consegue comprar NO BANCO."

Em destaque: "Aqui não tem banco."

Liste com X's vermelhos:
❌ Sem consulta SPC
❌ Sem consulta Serasa
❌ Sem aprovação de crédito
❌ Sem comitê decidindo por você

E checks verdes:
✅ Você tem {entrada}?
✅ Você paga {parcela}/mês?

Em papel amarelo: "Pronto. É sua."
""",
            "icones": "banco riscado com X vermelho, pessoa feliz com check verde"
        },

        # Slide 7 - SEM JUROS
        {
            "conteudo": f"""No topo: "BANCO vs DIRETO"

Em papel branco:
🏦 COMPRANDO PELO BANCO:
Imóvel: {format_currency(dados['preco'])}
Juros (5 anos): {format_currency(economia_juros)}
TOTAL: {format_currency(float(dados['preco']) * 2)}

Em papel verde:
🤝 COMPRANDO DIRETO:
Imóvel: {format_currency(dados['preco'])}
Juros: R$ 0
TOTAL: {format_currency(dados['preco'])}

Em papel pardo gigante:
"ECONOMIA: {format_currency(economia_juros)}"

Abaixo: "Metade do preço. Mesmo imóvel."
""",
            "icones": "calculadora, nota de dinheiro cortada ao meio"
        },

        # Slide 8 - O QUE VOCÊ RECEBE
        {
            "conteudo": f"""No topo: "{dados['tipo'].upper()}"

Liste com checks verdes:
✅ {dados['tipo']}
✅ {dados['localizacao']}
✅ Posse imediata

Em destaque:
{entrada} entrada
+ {dados['parcelas']}x {parcela} FIXAS

= SEM juros | SEM reajuste
""",
            "icones": "checklist completo, casinha, localização pin"
        },

        # Slide 9 - RECAP
        {
            "conteudo": f"""No topo: "RECAPITULANDO:"

"Você VAI pagar {parcela}/mês."

No aluguel:
→ {format_currency(total_aluguel)} gastos = Zero patrimônio

No {dados['tipo']}:
→ {format_currency(total_investido)} investidos = {format_currency(float(dados['preco']) * 1.5)} patrimônio

Diferença: {format_currency(float(dados['preco']) * 1.5)}

Em destaque:
"Sem banco. Sem juros. Sem SPC."

Abaixo:
"A cada mês que passa, fica mais caro NÃO ter."
""",
            "icones": "resumo, check verde, relógio"
        },

        # Slide 10 - CTA
        {
            "conteudo": """No topo: "ÚLTIMA COISA:"

Segunda-feira: 17 unidades
Hoje: 9 unidades

Em papel amarelo:
"Preço sobe semana que vem."

"Não é pressão. É realidade."

Você decide:
→ Continuar pagando aluguel
→ ou ter patrimônio

Em papel verde gigante:
👉 CHAMA NO WHATSAPP AGORA

Manda: "TENHO A ENTRADA"
""",
            "icones": "relógio urgente, WhatsApp logo desenhado, seta pra CTA"
        }
    ]

    return slides


def gerar_slides_carrossel2(dados):
    """Gera slides do Carrossel 2: Objeção Nome Sujo (8 slides)"""
    entrada = format_currency(dados['entrada'])
    parcela = format_currency(dados['parcela'])
    total_investido = float(dados['entrada']) + (float(dados['parcela']) * int(dados['parcelas']))

    slides = [
        # Slide 1 - HOOK
        {
            "conteudo": """No topo, entre aspas gigantes vermelhas: "NÃO CONSIGO COMPRAR MEU NOME TÁ SUJO"

Abaixo: "Escuto isso 10 vezes por dia."

E em destaque: "E minha resposta é sempre a mesma:"
""",
            "icones": "aspas grandes, pessoa preocupada, interrogação"
        },

        # Slide 2 - REFRAME
        {
            "conteudo": """No topo em letras vermelhas gigantes: "ERRADO."

Abaixo: "Você não consegue comprar NO BANCO."

Liste:
Banco = Score alto obrigatório
Banco = Juros de 12-18% ao ano
Banco = Demora 60 dias pra negar

Em papel verde:
"Mas aqui? Não tem banco."
""",
            "icones": "ERRADO riscado, banco com X, check verde"
        },

        # Slide 3 - CASOS REAIS
        {
            "conteudo": """No topo: "ONTEM FECHEI 3 UNIDADES EM 47 MINUTOS"

Desenhe 3 cards:

João, 34 anos:
❌ Nome no SPC há 2 anos
❌ Score 280
❌ Banco negou 3x
✅ Comprou

Maria, 41 anos:
❌ Serasa vermelho
❌ Score 195
❌ Sem conta bancária
✅ Comprou

Carlos, 29 anos:
❌ Negativado
❌ MEI sem faturamento fixo
❌ Banco riu da cara dele
✅ Comprou
""",
            "icones": "3 pessoas felizes, checks verdes, relógio"
        },

        # Slide 4 - O QUE ELES TINHAM
        {
            "conteudo": f"""No topo: "O QUE OS 3 TINHAM EM COMUM?"

Liste com checks verdes:
✅ {entrada} guardados
✅ Capacidade de pagar {parcela}/mês
✅ Cansados de pagar aluguel
✅ Queriam patrimônio

"O QUE OS 3 NÃO PRECISARAM?"

Liste com X's vermelhos:
❌ Score alto
❌ Aprovação bancária
❌ Comprovante de renda
❌ Fiador
❌ Pilha de documentos

Em destaque: "Só precisaram: RG + CPF + {entrada}"
""",
            "icones": "pessoas diferentes, documento simples, check"
        },

        # Slide 5 - MATEMÁTICA
        {
            "conteudo": f"""No topo: "VAMOS FAZER A CONTA:"

"Você JÁ paga {parcela}/mês de aluguel, certo?"

Divida ao meio:

ALUGUEL (vermelho):
{parcela} × {dados['parcelas']} meses = {format_currency(float(dados['parcela']) * int(dados['parcelas']))}
Resultado: ZERO patrimônio

{dados['tipo'].upper()} (verde):
{parcela} × {dados['parcelas']} meses = {format_currency(float(dados['parcela']) * int(dados['parcelas']))}
(+ {entrada} entrada = {format_currency(total_investido)} total)
Resultado: {dados['tipo']} valendo {format_currency(float(dados['preco']) * 1.5)}+

Em destaque: "MESMA DOR. Só muda o resultado final."

Abaixo: "Nome sujo não muda isso."
""",
            "icones": "calculadora, balança equilibrada"
        },

        # Slide 6 - SEM BANCO = SEM BARREIRAS
        {
            "conteudo": f"""No topo: "AQUI NÃO TEM:"

Liste com X's vermelhos:
❌ Consulta ao SPC
❌ Consulta ao Serasa
❌ Análise de crédito
❌ Comitê de aprovação
❌ Gerente de banco
❌ Score mínimo
❌ Juros
❌ Reajuste
❌ Fiador

Em papel verde grande:
"AQUI SÓ TEM:"

"Você + {entrada} + {parcela}/mês = Imóvel seu"

Abaixo: "Simples assim."
""",
            "icones": "barreiras derrubadas, caminho livre, check"
        },

        # Slide 7 - DIGNIDADE
        {
            "conteudo": """No topo: "OLHA..."

"Eu sei como é humilhante entrar no banco com esperança..."

"E sair com vergonha."

Liste:
→ Gerente olhando seu score
→ Fazendo aquela cara
→ Dizendo 'infelizmente...'

Em papel azul claro:
"Aqui você não passa por isso."

"Ninguém julga seu passado.
Ninguém olha seu score.
Ninguém faz você se sentir menos."

Em destaque:
"Tem dinheiro? Tem imóvel. Ponto final."
""",
            "icones": "coração, pessoa digna, respeito"
        },

        # Slide 8 - CTA
        {
            "conteudo": f"""No topo: "NÃO É PRA TODO MUNDO."

"Se você NÃO tem {entrada}: Não chama."
"Se você NÃO pode pagar {parcela}/mês: Não chama."

"MAS SE VOCÊ:"

Liste com checks:
✅ Tem {entrada} guardados
✅ Paga aluguel (e tá cansado)
✅ Nome sujo mas quer patrimônio
✅ Quer imóvel SEM depender de banco

Em papel verde gigante:
👉 CHAMA NO WHATSAPP AGORA

Em papel amarelo:
"PS: Eram 17. Restam 9. Semana que vem não sei quantos sobram."
""",
            "icones": "WhatsApp logo, urgência, check verde"
        }
    ]

    return slides


def monitor_and_download_slide(task_info, slide_num, template_suffix=""):
    """
    Monitora uma tarefa de slide até conclusão e baixa a imagem
    (Adaptado de generate_image_batch_gpt.py)

    Args:
        task_info: Informações da tarefa
        slide_num: Número do slide
        template_suffix: Sufixo do template (ex: "_template1", "_template2", "")
    """
    task_id = task_info["task_id"]
    prompt = task_info["prompt"]

    max_wait = 300
    check_interval = 3
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)

        if result["status"] == "success":
            image_urls = result["image_urls"]
            if not image_urls:
                return {"success": False, "slide": slide_num, "template": template_suffix, "error": "No image URL"}

            # Baixa todas as variantes
            downloaded_paths = []
            for i, url in enumerate(image_urls, 1):
                filename = f"carrossel_slide_{slide_num:02d}{template_suffix}_v{i}.png"
                output_path = os.path.join(DOWNLOADS_PATH, filename)

                downloaded = download_image(url, output_path)
                if downloaded:
                    downloaded_paths.append(downloaded)

            if downloaded_paths:
                return {
                    "success": True,
                    "slide": slide_num,
                    "template": template_suffix,
                    "paths": downloaded_paths,
                    "urls": image_urls,
                    "variants": len(downloaded_paths)
                }
            else:
                return {"success": False, "slide": slide_num, "template": template_suffix, "error": "Download failed"}

        elif result["status"] == "failed":
            return {"success": False, "slide": slide_num, "template": template_suffix, "error": "Generation failed"}

        time.sleep(check_interval)

    return {"success": False, "slide": slide_num, "template": template_suffix, "error": "Timeout"}


def gerar_carrossel_paralelo(slides, image_url=None, n_variants=4, dual_cover=False, dados=None):
    """
    Gera todos os slides do carrossel em paralelo (baseado em generate_image_batch_gpt.py)

    Args:
        slides: Lista de slides a gerar
        image_url: URL da imagem do imóvel (para slide 1)
        n_variants: Número de variantes por slide
        dual_cover: Se True, gera Slide 1 com 2 templates
        dados: Dados do imóvel (necessário se dual_cover=True)
    """
    total_slides = len(slides) + (1 if dual_cover else 0)  # +1 se dual cover (slide 1 template 2)
    print(f"\n🚀 Gerando {total_slides} slides em paralelo...")
    print(f"🎨 Variantes por slide: {n_variants}")
    if dual_cover:
        print("🎭 Modo Dual Cover: Slide 1 será gerado com 2 templates")
    print("=" * 60)

    # Fase 1: Criar todas as tarefas
    print("🚀 Fase 1: Criando todas as tarefas...")
    tasks = []

    for i, slide in enumerate(slides, 1):
        # Monta prompt completo
        conteudo = slide['conteudo']
        icones = slide['icones']
        prompt = PROMPT_BASE.replace("{CONTEUDO_ESPECIFICO}", conteudo)
        prompt = prompt.replace("{ICONES}", icones)

        # Primeiro slide usa imagem de referência, demais só prompt
        files_url = [image_url] if (i == 1 and image_url) else None

        # Template 1 (ou único se não dual cover)
        template_suffix = "_template1" if (i == 1 and dual_cover) else ""

        if files_url:
            label = "Slide 1 Template 1" if dual_cover else "Slide 1"
            print(f"   [{len(tasks)+1}/{total_slides}] {label} (com imagem de referência)...")
        else:
            print(f"   [{len(tasks)+1}/{total_slides}] Slide {i}...")

        task = create_task(prompt, n_variants=n_variants, enhance=False, files_url=files_url)

        if task:
            task['slide_num'] = i
            task['template_suffix'] = template_suffix
            task['has_image'] = (i == 1 and image_url)
            tasks.append(task)
            print(f"   ✅ Task ID: {task['task_id']}")
        else:
            print(f"   ❌ Falha ao criar tarefa")

        # Se dual cover e for slide 1, criar também Template 2
        if dual_cover and i == 1 and dados:
            slide_t2 = gerar_slide1_template2(dados)
            conteudo_t2 = slide_t2['conteudo']
            icones_t2 = slide_t2['icones']
            prompt_t2 = PROMPT_BASE.replace("{CONTEUDO_ESPECIFICO}", conteudo_t2)
            prompt_t2 = prompt_t2.replace("{ICONES}", icones_t2)

            print(f"   [{len(tasks)+1}/{total_slides}] Slide 1 Template 2 (com imagem de referência)...")

            task_t2 = create_task(prompt_t2, n_variants=n_variants, enhance=False, files_url=files_url)

            if task_t2:
                task_t2['slide_num'] = 1
                task_t2['template_suffix'] = "_template2"
                task_t2['has_image'] = True
                tasks.append(task_t2)
                print(f"   ✅ Task ID: {task_t2['task_id']}")
            else:
                print(f"   ❌ Falha ao criar tarefa Template 2")

    if not tasks:
        print("\n❌ Nenhuma tarefa foi criada com sucesso")
        return []

    print(f"\n✅ {len(tasks)} tarefa(s) criada(s) com sucesso!")
    print(f"\n⏳ Fase 2: Monitorando e baixando ({len(tasks)} em paralelo)...")

    # Fase 2: Monitorar todas as tarefas em paralelo
    results = []
    completed = 0

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_task = {
            executor.submit(monitor_and_download_slide, task, task['slide_num'], task.get('template_suffix', '')): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            completed += 1
            result = future.result()
            results.append(result)

            if result["success"]:
                variants_count = result.get('variants', 0)
                template_label = result.get('template', '')
                slide_label = f"Slide {result['slide']}{template_label}"
                print(f"   ✅ [{completed}/{len(tasks)}] {slide_label}: {variants_count} variantes")
                for path in result.get('paths', []):
                    print(f"      💾 {os.path.basename(path)}")
            else:
                template_label = result.get('template', '')
                slide_label = f"Slide {result['slide']}{template_label}"
                print(f"   ❌ [{completed}/{len(tasks)}] {slide_label}: {result.get('error', 'Unknown')}")

    # Ordena resultados por número do slide e template
    results.sort(key=lambda x: (x["slide"], x.get("template", "")))
    return results


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Gerar Carrossel Meta Ads (Estilo Hormozi - Colagem Artesanal)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

1. Modo interativo (recomendado):
   python3 scripts/image-generation/batch_carrossel_gpt4o.py

2. Modo teste (3 slides):
   python3 scripts/image-generation/batch_carrossel_gpt4o.py --limit 3

3. Carrossel 1 completo (10 slides):
   python3 scripts/image-generation/batch_carrossel_gpt4o.py \\
       --tipo "Chácara 1.000m²" \\
       --preco "70000" \\
       --entrada "10000" \\
       --parcela "1000" \\
       --parcelas "60" \\
       --localizacao "Itatiaiuçu, 15min do centro" \\
       --carrossel 1 \\
       --image-url "https://exemplo.com/foto.jpg"

Tipos de carrossel:
   - Carrossel 1: Matemática Brutal (10 slides)
   - Carrossel 2: Objeção Nome Sujo (8 slides)
   - Carrossel 3: Custo de Não Agir (7 slides - em breve)

Características:
   - Visual: colagem artesanal feita à mão
   - Geração 100% paralela (máxima velocidade)
   - 4-10 variantes por slide (personalizável com --variants)
   - Salvamento automático em ~/Downloads
        """
    )

    parser.add_argument('--tipo', help='Tipo do imóvel')
    parser.add_argument('--preco', help='Preço total')
    parser.add_argument('--entrada', help='Valor da entrada')
    parser.add_argument('--parcela', help='Valor da parcela')
    parser.add_argument('--parcelas', help='Número de parcelas')
    parser.add_argument('--localizacao', help='Localização do imóvel')
    parser.add_argument('--carrossel', type=int, choices=[1, 2, 3], default=1,
                        help='Tipo de carrossel (1=Matemática 10 slides, 2=Objeção 8 slides, 3=Custo 7 slides). Padrão: 1')
    parser.add_argument('--image-url', help='URL da imagem do imóvel (slide 1)')
    parser.add_argument('--variants', type=int, choices=range(4, 11), default=4,
                        help='Número de variantes por slide (4-10). Padrão: 4')
    parser.add_argument('--limit', type=int,
                        help='Limitar número de slides (para teste). Ex: --limit 3')
    parser.add_argument('--prompts-file', help='Arquivo JSON com prompts dinâmicos (skill carrossel-meta-ads)')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Pular confirmação e executar automaticamente')
    parser.add_argument('--dual-cover', action='store_true',
                        help='Gerar Slide 1 com 2 templates (Template 1 + Template 2)')

    args = parser.parse_args()

    print("\n🏠 GERADOR DE CARROSSEL META ADS - ESTILO HORMOZI")
    print("=" * 60)
    print("📊 Metodologia: Alex Hormozi (100M Offers + 100M Leads)")
    print("🎨 Visual: Colagem artesanal feita à mão")
    print("⚡ Modo: Paralelo (máxima velocidade)")
    print("=" * 60)

    # MODO DINÂMICO: Se forneceu --prompts-file, usa JSON
    if args.prompts_file:
        print("\n📄 Modo dinâmico: Carregando prompts de arquivo JSON")
        try:
            with open(args.prompts_file, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)

            # Converte JSON para formato de slides
            slides = []
            for item in prompts_data:
                slides.append({
                    "conteudo": item["conteudo"],
                    "icones": item["icones"]
                })

            print(f"✅ {len(slides)} slides carregados do JSON")

            # Aplica limite se especificado
            if args.limit:
                slides = slides[:args.limit]
                print(f"⚠️  MODO TESTE: Gerando apenas {len(slides)} slides")

            # Confirmação antes de gerar
            total_imagens = len(slides) * args.variants
            print(f"\n🎨 Pronto para gerar {len(slides)} slides × {args.variants} variantes = {total_imagens} imagens")

            if not args.yes:
                confirma = input("Deseja continuar? (s/n): ").strip().lower()
                if confirma not in ['s', 'sim', 'y', 'yes']:
                    print("❌ Operação cancelada")
                    return 0
            else:
                print("✅ Confirmação automática (--yes)")


            # Gera imagens em paralelo
            inicio = time.time()
            resultados = gerar_carrossel_paralelo(slides, args.image_url, args.variants)
            duracao = time.time() - inicio

        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {args.prompts_file}")
            return 1
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao ler JSON: {e}")
            return 1
        except KeyError as e:
            print(f"❌ JSON mal formatado. Falta campo: {e}")
            print("Formato esperado: [{'conteudo': '...', 'icones': '...'}, ...]")
            return 1

    # MODO CLÁSSICO: Coleta dados e usa carrosséis hardcoded
    else:
        if args.tipo and args.preco and args.entrada and args.parcela and args.parcelas and args.localizacao:
            dados = {
                'tipo': args.tipo,
                'preco': args.preco,
                'entrada': args.entrada,
                'parcela': args.parcela,
                'parcelas': args.parcelas,
                'localizacao': args.localizacao,
                'image_url': args.image_url
            }
            print("\n✅ Dados do imóvel carregados via argumentos")
        else:
            dados = coletar_dados_imovel()

        # Resumo dos dados
        print("\n📋 RESUMO DO IMÓVEL:")
        print(f"   Tipo: {dados['tipo']}")
        print(f"   Preço: {format_currency(dados['preco'])}")
        print(f"   Entrada: {format_currency(dados['entrada'])}")
        print(f"   Parcela: {format_currency(dados['parcela'])} x {dados['parcelas']}x")
        print(f"   Localização: {dados['localizacao']}")
        if dados['image_url']:
            print(f"   Imagem: {dados['image_url'][:50]}...")

        # Escolhe carrossel
        tipo_carrossel = args.carrossel

        if tipo_carrossel == 1:
            nome_carrossel = "Matemática Brutal"
        elif tipo_carrossel == 2:
            nome_carrossel = "Objeção Nome Sujo"
        else:
            nome_carrossel = "Custo de Não Agir"

        print(f"\n✅ Carrossel {tipo_carrossel} selecionado ({nome_carrossel})")

        # Gera slides
        print(f"\n📝 Gerando copy dos slides...")

        if tipo_carrossel == 1:
            slides = gerar_slides_carrossel1(dados)
        elif tipo_carrossel == 2:
            slides = gerar_slides_carrossel2(dados)
        else:
            print("❌ Carrossel 3 ainda não implementado")
            return 1

        # Aplica limite se especificado
        if args.limit:
            slides = slides[:args.limit]
            print(f"⚠️  MODO TESTE: Gerando apenas {len(slides)} slides")

        print(f"✅ {len(slides)} slides gerados")

        # Confirmação antes de gerar
        total_imagens = len(slides) * args.variants
        print(f"\n🎨 Pronto para gerar {len(slides)} slides × {args.variants} variantes = {total_imagens} imagens em paralelo")

        if not args.yes:
            confirma = input("Deseja continuar? (s/n): ").strip().lower()
            if confirma not in ['s', 'sim', 'y', 'yes']:
                print("❌ Operação cancelada")
                return 0
        else:
            print("✅ Confirmação automática (--yes)")

        # Gera imagens em paralelo
        inicio = time.time()
        resultados = gerar_carrossel_paralelo(
            slides,
            image_url=dados['image_url'],
            n_variants=args.variants,
            dual_cover=args.dual_cover,
            dados=dados
        )
        duracao = time.time() - inicio

    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DA GERAÇÃO")
    print("=" * 60)

    sucesso = sum(1 for r in resultados if r["success"])
    falhas = len(resultados) - sucesso
    total_imagens = sum(r.get('variants', 0) for r in resultados if r["success"])

    print(f"✅ Slides gerados com sucesso: {sucesso}/{len(resultados)}")
    print(f"🖼️  Total de imagens geradas: {total_imagens} ({sucesso} slides × {args.variants} variantes)")
    print(f"❌ Falhas: {falhas}/{len(resultados)}")
    print(f"⏱️  Tempo total: {duracao:.1f}s ({duracao/len(slides):.1f}s por slide)")

    if sucesso > 0:
        print(f"\n📂 Imagens salvas em: ~/Downloads")
        print(f"📝 Padrão de nome: carrossel_slide_01_v1.png, carrossel_slide_01_v2.png, ..., carrossel_slide_01_v{args.variants}.png")
        print(f"\n🎯 Próximo passo: Escolher melhor variante de cada slide e fazer upload para Meta Ads")

    if falhas > 0:
        print("\n⚠️  Slides com falha:")
        for r in resultados:
            if not r["success"]:
                print(f"   Slide {r['slide']}: {r.get('error', 'Unknown')}")

    return 0 if falhas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
