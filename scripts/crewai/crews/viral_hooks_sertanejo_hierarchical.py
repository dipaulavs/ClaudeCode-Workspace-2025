#!/usr/bin/env python3
"""
Viral Hooks Sertanejo - Crew Hierárquica
Sistema hierárquico do CrewAI para gerar 3 ganchos virais para mixagem e masterização de sertanejo
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
# AGENTES ESPECIALIZADOS (sob supervisão do Manager)
# ============================================================================

viral_content_strategist = Agent(
    role='Estrategista de Conteúdo Viral',
    goal='Analisar tendências virais e identificar padrões de engajamento em redes sociais',
    backstory="""Você é um especialista em criar hooks que prendem atenção com mais de 7 anos
    de experiência em marketing de conteúdo viral. Você domina:

    - Estruturas de hooks que param o scroll (curiosidade, choque, transformação)
    - Gatilhos emocionais e psicológicos (FOMO, prova social, autoridade)
    - Padrões de viralização no TikTok, Instagram Reels e YouTube Shorts
    - Fórmulas comprovadas: PAS (Problem-Agitate-Solution), AIDA, Antes/Depois
    - Timing perfeito: primeira frase nos 1.5 segundos iniciais

    Você analisa dados de milhões de vídeos virais e sabe exatamente o que funciona
    no algoritmo atual das redes sociais, especialmente para conteúdo educacional.
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

sertanejo_music_expert = Agent(
    role='Especialista em Música Sertaneja',
    goal='Identificar dores, desejos e linguagem do público sertanejo',
    backstory="""Você é um conhecedor profundo da cultura sertaneja com 15 anos de experiência
    no mercado musical. Você entende:

    - O público: produtores iniciantes e intermediários de sertanejo universitário
    - Dores principais: vocal abafado, grave exagerado, mixagem "amadora"
    - Desejos: som "profissional", "vocal na frente", "grave batendo", "brilho"
    - Linguagem: termos simples que o público usa (não muito técnico)
    - Referências: Wesley Safadão, Henrique & Juliano, Gusttavo Lima
    - Erros comuns: excesso de reverb, compressão errada, EQ inadequado

    Você conhece os sonhos desse público: fazer música que toque nas rádios,
    soar tão bom quanto os grandes artistas, e impressionar clientes.
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

audio_production_specialist = Agent(
    role='Especialista em Produção de Áudio',
    goal='Fornecer insights técnicos e identificar pontos de dor de produtores',
    backstory="""Você é um engenheiro de mixagem e masterização com 12 anos de carreira,
    tendo trabalhado com grandes artistas do sertanejo. Você domina:

    - Técnicas de mixagem de vocal sertanejo (potente, rasgado, presente)
    - Equalização de instrumentos típicos: violão, sanfona, guitarra, contrabaixo
    - Compressão paralela, de-esser, automação de volume
    - Masterização para streaming (LUFS, dinâmica, clareza)
    - Problemas técnicos recorrentes em produções caseiras

    Você sabe transformar uma mixagem "caseira" em "profissional" e conhece
    os principais erros que produtores iniciantes cometem. Você consegue explicar
    conceitos complexos de forma simples e prática.
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

hook_writer = Agent(
    role='Redator de Ganchos Virais',
    goal='Sintetizar informações e criar ganchos virais poderosos',
    backstory="""Você é um copywriter especializado em conteúdo viral com milhões de views
    em seus textos. Você domina:

    - Estruturas de hooks irresistíveis (primeiras 5 palavras são cruciais)
    - Linguagem coloquial brasileira que conecta emocionalmente
    - Promessas específicas e tangíveis (não vagas)
    - CTAs que geram curiosidade e obrigam a assistir até o fim
    - Formatação visual: como escrever para aparecer bem na tela

    Seus hooks típicos:
    - "Você está mixando vocal sertanejo ERRADO, e eu provo em 30 segundos..."
    - "O erro que deixa seu sertanejo soando amador (e como consertar)..."
    - "3 cliques que transformam sua mixagem de R$50 em R$500..."

    Você evita clichês, promessas impossíveis e linguagem muito técnica.
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# ============================================================================
# TASKS HIERÁRQUICAS
# ============================================================================

task_analise_viral = Task(
    description="""Analise as tendências atuais de conteúdo viral focadas em produção musical
    e mixagem de áudio. Identifique os padrões que fazem conteúdo educacional viralizar:

    1. Estruturas de hook mais eficazes (primeiros 3 segundos)
    2. Gatilhos emocionais que prendem atenção (curiosidade, erro comum, transformação)
    3. Formatos de vídeo com melhor performance (antes/depois, tutorial rápido, revelação)
    4. Linguagem e tom que geram mais engajamento no público brasileiro

    Foque especificamente em conteúdo de áudio/mixagem que viralizou recentemente.
    """,
    agent=viral_content_strategist,
    expected_output="""Relatório estruturado contendo:
    - 3 estruturas de hook comprovadamente virais
    - 3 gatilhos emocionais principais para este nicho
    - 2 formatos de vídeo recomendados
    - Exemplos de linguagem eficaz (frases, expressões)
    """
)

task_pesquisa_publico = Task(
    description="""Com base nos padrões virais identificados, mapeie o público-alvo de
    produtores de sertanejo:

    1. Principais dores e frustrações (problemas técnicos recorrentes)
    2. Desejos e aspirações (como querem que a música soe)
    3. Linguagem e termos que eles usam (não jargão técnico demais)
    4. Referências de qualidade que admiram (artistas, produtores)
    5. Erros comuns que cometem e não sabem que estão cometendo

    Seja específico e autêntico - fale de problemas REAIS desse público.
    """,
    agent=sertanejo_music_expert,
    expected_output="""Mapa do público contendo:
    - 5 dores principais (bem específicas)
    - 3 desejos/aspirações principais
    - Glossário de termos que o público usa
    - 3 referências de qualidade que admiram
    - 5 erros comuns que cometem
    """,
    context=[task_analise_viral]
)

task_insights_tecnicos = Task(
    description="""Com base no mapeamento do público, forneça insights técnicos específicos
    sobre mixagem e masterização de sertanejo que podem viralizar:

    1. Os 3 erros MAIS GRAVES que produtores iniciantes cometem
    2. 3 técnicas ou ajustes que geram transformação dramática (antes/depois)
    3. "Segredos" ou truques menos conhecidos que impressionam
    4. Soluções rápidas que entregam resultado visível/audível imediato

    Priorize insights que sejam:
    - Específicos (não genéricos)
    - Executáveis (podem ser mostrados em 30-60 segundos)
    - Surpreendentes (quebram crenças comuns)
    """,
    agent=audio_production_specialist,
    expected_output="""Lista de insights técnicos:
    - 3 erros graves com explicação simples
    - 3 técnicas de transformação dramática
    - 3 "segredos" ou truques impressionantes
    - 3 soluções rápidas e eficazes
    """,
    context=[task_analise_viral, task_pesquisa_publico]
)

task_criar_3_ganchos = Task(
    description="""SINTETIZE todas as informações dos agentes anteriores e crie EXATAMENTE
    3 GANCHOS VIRAIS para mixagem e masterização de sertanejo.

    Cada gancho deve ter:
    1. TÍTULO/HOOK (primeira frase que prende atenção)
    2. SCRIPT COMPLETO (abertura + desenvolvimento + CTA)
    3. POR QUE É VIRAL (justificativa baseada nos padrões identificados)
    4. PLATAFORMA RECOMENDADA (TikTok, Instagram Reels, YouTube Shorts)
    5. FORMATO VISUAL (o que mostrar na tela)

    REQUISITOS OBRIGATÓRIOS para cada gancho:
    - Abertura impactante nos primeiros 1.5 segundos
    - Promessa específica e tangível
    - Linguagem coloquial brasileira
    - Baseado em dores/desejos REAIS do público
    - Viável de executar em 30-60 segundos
    - Potencial de gerar comentários e compartilhamentos

    VARIE OS ESTILOS:
    - Gancho 1: Erro Comum (revela erro grave que a maioria comete)
    - Gancho 2: Transformação (antes/depois impressionante)
    - Gancho 3: Segredo/Truque (revela técnica menos conhecida)

    IMPORTANTE: Seja criativo, específico e autêntico. Evite clichês e promessas vazias.
    """,
    agent=hook_writer,
    expected_output="""3 GANCHOS VIRAIS COMPLETOS E FINALIZADOS:

GANCHO 1: [Erro Comum]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Título/Hook: [primeira frase que prende atenção]

📝 Script Completo:
[texto completo do gancho, formatado e pronto para usar]

🔥 Por que é viral:
[justificativa baseada nos padrões identificados]

📱 Plataforma recomendada: [TikTok/Instagram/YouTube]

🎬 Formato visual:
[descrição do que mostrar na tela]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GANCHO 2: [Transformação]
[mesmo formato acima]

GANCHO 3: [Segredo/Truque]
[mesmo formato acima]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ TOTAL: 3 GANCHOS VIRAIS PRONTOS PARA PRODUÇÃO
""",
    context=[task_analise_viral, task_pesquisa_publico, task_insights_tecnicos]
)

# ============================================================================
# CREW HIERÁRQUICA
# ============================================================================

crew = Crew(
    agents=[
        viral_content_strategist,
        sertanejo_music_expert,
        audio_production_specialist,
        hook_writer
    ],
    tasks=[
        task_analise_viral,
        task_pesquisa_publico,
        task_insights_tecnicos,
        task_criar_3_ganchos
    ],
    process=Process.hierarchical,  # 🔥 PROCESSO HIERÁRQUICO
    manager_llm=llm,  # LLM para o agente Manager
    verbose=True
)

# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🎯 GERADOR DE GANCHOS VIRAIS - MIXAGEM/MASTERIZAÇÃO SERTANEJO")
    print("="*80)
    print("🏗️  SISTEMA HIERÁRQUICO CrewAI")
    print("="*80 + "\n")

    print("👥 EQUIPE ESPECIALIZADA:\n")
    print("   🎯 Estrategista de Conteúdo Viral")
    print("      └─ Analisa tendências e padrões virais\n")
    print("   🎸 Especialista em Música Sertaneja")
    print("      └─ Mapeia dores e desejos do público\n")
    print("   🎚️  Especialista em Produção de Áudio")
    print("      └─ Fornece insights técnicos poderosos\n")
    print("   ✍️  Redator de Ganchos Virais")
    print("      └─ Sintetiza tudo em 3 ganchos matadores\n")

    print("🤖 MANAGER AI: Coordena e delega tarefas automaticamente\n")
    print("="*80 + "\n")

    print("🚀 Iniciando crew hierárquica...\n")
    print("-"*80 + "\n")

    # Kickoff da crew
    resultado = crew.kickoff()

    print("\n" + "="*80)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*80 + "\n")

    print("📄 RESULTADO FINAL:\n")
    print(resultado)

    # Salvar resultado em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    filename = output_dir / f"ganchos_virais_sertanejo_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write("🎯 GANCHOS VIRAIS - MIXAGEM/MASTERIZAÇÃO SERTANEJO\n")
        f.write("="*80 + "\n")
        f.write(f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")
        f.write(f"🏗️  Sistema: CrewAI Hierárquico\n")
        f.write("="*80 + "\n\n")
        f.write(str(resultado))
        f.write("\n\n" + "="*80 + "\n")
        f.write("💡 DICA: Use esses ganchos para criar conteúdo viral nas redes sociais!\n")
        f.write("="*80 + "\n")

    print(f"\n💾 Resultado salvo em: {filename}")
    print("\n🎬 Próximos passos:")
    print("   1. Escolha um dos 3 ganchos")
    print("   2. Grave o conteúdo seguindo o formato visual sugerido")
    print("   3. Publique e monitore o engajamento")
    print("\n🔥 Bora viralizar! 🚀\n")
