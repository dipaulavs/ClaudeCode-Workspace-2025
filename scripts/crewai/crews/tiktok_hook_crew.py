#!/usr/bin/env python3
"""
TikTok Hook Viral Generator Crew
Especializado em criar hooks virais para o nicho de mixagem e masterização de áudio no sertanejo
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from datetime import datetime

# Carrega variáveis de ambiente
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Configura LLM para todos os agentes
llm = LLM(
    model=os.getenv("OPENAI_MODEL_NAME"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# ============================================================================
# AGENTES
# ============================================================================

pesquisador_trends = Agent(
    role='Analista de Tendências TikTok',
    goal='Identificar padrões e estruturas de conteúdo viral no TikTok focado em produção musical',
    backstory="""Você é um especialista em viralização de conteúdo no TikTok com mais de 5 anos
    de experiência analisando trends. Você entende profundamente:

    - Estruturas de hooks que prendem atenção nos primeiros 3 segundos
    - Gatilhos emocionais que fazem pessoas pararem o scroll
    - Padrões de conteúdo educacional viral (antes/depois, erros comuns, segredos)
    - Tendências do nicho de produção musical no Brasil
    - Horários e formatos que maximizam engajamento

    Você sabe que no TikTok, conteúdo de mixagem/masterização viraliza quando:
    - Mostra transformação visual/sonora dramática
    - Revela "erros que todo mundo comete"
    - Promete resultado rápido e profissional
    - Usa linguagem direta e provocativa
    - Cria curiosidade ou polêmica controlada
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

especialista_audio = Agent(
    role='Especialista em Mixagem e Masterização de Sertanejo',
    goal='Fornecer insights técnicos autênticos sobre produção de áudio sertanejo',
    backstory="""Você é um produtor musical especializado em sertanejo com 10 anos de carreira.
    Você conhece profundamente:

    - Características sonoras do sertanejo universitário vs raiz
    - Técnicas de mixagem para vocais rasgados e potentes
    - Equalização específica para violão, sanfona e guitarra sertaneja
    - Compressão e masterização para plataformas de streaming
    - Problemas comuns: vocal abafado, grave exagerado, falta de brilho
    - Termos técnicos que o público entende: "grave batendo", "vocal na frente", "som limpo"

    Você sabe que produtores iniciantes de sertanejo costumam errar em:
    - Excesso de reverb no vocal
    - Equalização errada que deixa o vocal "enterrado"
    - Falta de compressão que deixa o vocal inconsistente
    - Master muito limitado que perde dinâmica
    - Não ajustar frequências para competir com a batida eletrônica
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

copywriter_viral = Agent(
    role='Copywriter Especializado em Conteúdo Viral',
    goal='Criar hooks irresistíveis que fazem pessoas pararem de scrollar',
    backstory="""Você é um copywriter especializado em conteúdo viral para TikTok.
    Você domina técnicas de persuasão e escrita viral:

    - Fórmulas de hooks: Curiosidade, Polêmica, Transformação, Erro Comum
    - Estrutura PAS (Problem-Agitate-Solution)
    - Gatilhos mentais: escassez, autoridade, prova social
    - Linguagem direta e coloquial que conecta com o público brasileiro
    - CTA (call-to-action) que gera engajamento

    Você sabe criar aberturas como:
    - "Você está mixando sertanejo ERRADO e eu vou te provar..."
    - "Produtores odeiam esse truque de masterização..."
    - "3 segundos para transformar seu vocal de amador para profissional"
    - "Por que seu sertanejo não soa como os das rádios? Vou te mostrar..."

    Você evita:
    - Aberturas genéricas ou chatas
    - Promessas impossíveis
    - Linguagem muito técnica que afasta iniciantes
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

estrategista_conteudo = Agent(
    role='Estrategista de Conteúdo para TikTok',
    goal='Validar e otimizar hooks para máximo potencial viral',
    backstory="""Você é um estrategista de conteúdo com cases de vídeos virais.
    Você avalia cada hook considerando:

    - Força da abertura (prende atenção em 1 segundo?)
    - Clareza da promessa (fica claro o valor?)
    - Viabilidade de execução (é possível gravar isso?)
    - Potencial de engajamento (gera comentários/compartilhamentos?)
    - Adequação ao algoritmo do TikTok

    Você adiciona:
    - CTA estratégico (comenta, salva, compartilha)
    - Hashtags relevantes e não saturadas
    - Sugestões de formato visual
    - Timing ideal do vídeo

    Você rejeita hooks que:
    - São muito longos ou confusos
    - Não têm diferencial claro
    - São clickbait sem entregar valor
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# ============================================================================
# TASKS
# ============================================================================

task_analisar_trends = Task(
    description="""Analise as tendências atuais de conteúdo viral no TikTok focado em
    produção musical e mixagem de áudio.

    Com base no seu conhecimento, identifique:
    1. As 5 estruturas de hook mais eficazes para conteúdo educacional de áudio
    2. Gatilhos emocionais que funcionam no nicho de produção musical
    3. Formatos de vídeo que estão performando bem (antes/depois, tutoriais rápidos, etc)
    4. Padrões de linguagem que geram mais engajamento

    Foque especificamente no contexto brasileiro e no público de produtores de sertanejo
    (desde iniciantes até intermediários).
    """,
    agent=pesquisador_trends,
    expected_output="""Relatório estruturado com:
    - 5 estruturas de hook comprovadas
    - 3 gatilhos emocionais principais
    - 3 formatos de vídeo recomendados
    - Exemplos de linguagem eficaz
    """
)

task_insights_tecnicos = Task(
    description="""Com base nos padrões identificados pelo analista de trends, forneça
    insights técnicos específicos sobre mixagem e masterização de sertanejo que podem
    ser transformados em conteúdo viral.

    Identifique:
    1. Os 5 erros mais comuns que produtores iniciantes cometem
    2. 3 técnicas "secretas" ou menos conhecidas que geram resultados dramáticos
    3. Transformações antes/depois que são visualmente/sonoramente impactantes
    4. Termos técnicos que o público-alvo entende e busca

    Priorize dores reais que você conhece do dia a dia de produtores de sertanejo.
    """,
    agent=especialista_audio,
    expected_output="""Lista estruturada com:
    - 5 erros comuns com explicação simples
    - 3 técnicas diferenciadas
    - 3 ideias de transformação antes/depois
    - Glossário de termos técnicos populares
    """,
    context=[task_analisar_trends]
)

task_criar_hooks = Task(
    description="""Com base nas tendências identificadas e nos insights técnicos,
    crie 10 hooks virais para TikTok focados em mixagem/masterização de sertanejo.

    Para cada hook, crie:
    1. Abertura impactante (primeiros 3 segundos que prendem atenção)
    2. Corpo do script (15-20 segundos de conteúdo valioso)
    3. CTA inicial (o que vai acontecer no vídeo)

    Use as fórmulas:
    - Curiosidade: "O segredo que [autoridade] não conta sobre [problema]..."
    - Erro Comum: "Você está fazendo [ação] errado, e eu vou te provar..."
    - Transformação: "X segundos para transformar [estado atual] em [estado desejado]"
    - Polêmica: "Por que [crença comum] está te sabotando..."

    Varie os estilos mas mantenha foco no nicho de sertanejo.
    """,
    agent=copywriter_viral,
    expected_output="""10 hooks completos, cada um contendo:
    - Título/Gancho (primeira linha que aparece no vídeo)
    - Script completo (abertura + corpo + CTA)
    - Ângulo usado (curiosidade, erro comum, etc)
    """,
    context=[task_analisar_trends, task_insights_tecnicos]
)

task_validar_otimizar = Task(
    description="""Analise os 10 hooks criados e selecione os 5 melhores para serem
    produzidos. Para cada hook selecionado, otimize e adicione:

    1. Score de potencial viral (1-10) com justificativa
    2. Hashtags estratégicas (mix de populares e nicho)
    3. Sugestão de formato visual (o que mostrar na tela)
    4. CTA final otimizado (comentário, salvamento, seguir)
    5. Melhorias no texto se necessário

    Priorize hooks que:
    - Têm abertura forte e clara
    - Prometem valor entregável em 30-60 segundos
    - Têm potencial de gerar comentários/discussão
    - São viáveis de produzir com equipamento básico

    Rejeite ou melhore hooks vagos, muito técnicos ou sem diferencial claro.
    """,
    agent=estrategista_conteudo,
    expected_output="""5 hooks finalizados e otimizados, cada um com:
    - Hook completo revisado
    - Score de potencial viral (1-10) + justificativa
    - 5-8 hashtags estratégicas
    - Descrição do formato visual
    - CTA otimizado
    - Sugestão de duração do vídeo
    """,
    context=[task_criar_hooks]
)

# ============================================================================
# CREW
# ============================================================================

crew = Crew(
    agents=[
        pesquisador_trends,
        especialista_audio,
        copywriter_viral,
        estrategista_conteudo
    ],
    tasks=[
        task_analisar_trends,
        task_insights_tecnicos,
        task_criar_hooks,
        task_validar_otimizar
    ],
    process=Process.sequential,
    verbose=True
)

# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎬 TIKTOK HOOK VIRAL GENERATOR - MIXAGEM/MASTERIZAÇÃO SERTANEJO")
    print("="*80 + "\n")

    print("🚀 Iniciando crew com 4 agentes especializados...\n")
    print("📋 Pipeline:")
    print("   1. Analista de Trends → Identifica padrões virais")
    print("   2. Especialista em Áudio → Fornece insights técnicos")
    print("   3. Copywriter Viral → Cria 10 hooks impactantes")
    print("   4. Estrategista → Valida e otimiza os 5 melhores\n")

    print("-"*80 + "\n")

    # Kickoff da crew
    resultado = crew.kickoff()

    print("\n" + "="*80)
    print("✅ PROCESSO CONCLUÍDO!")
    print("="*80 + "\n")

    print("📄 RESULTADO FINAL:\n")
    print(resultado)

    # Salvar resultado em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tiktok_hooks_sertanejo_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("TIKTOK HOOKS VIRAIS - MIXAGEM/MASTERIZAÇÃO SERTANEJO\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        f.write(str(resultado))

    print(f"\n💾 Resultado salvo em: {filename}")
    print("\n🎯 Use esses hooks para criar conteúdo viral no TikTok!")
