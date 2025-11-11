"""
Exemplo de Crew com 3 agentes usando arquivos .md como instruções:
- Copywriter (Peão): Cria ganchos virais usando técnica Hormozi
- Analista (Middle): Avalia qualidade e sugere melhorias
- Diretor (Senior): Aprova versão final

Processo: Hierarchical (com Manager automático para feedback loops)
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adiciona o caminho do utils ao PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

from crewai import Agent, Task, Crew, Process
from md_loader import MDLoader

# Carrega variáveis de ambiente (.env)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Inicializa o loader de arquivos .md
loader = MDLoader()


def create_copywriter_agent() -> Agent:
    """
    Copywriter Especialista (Peão)
    Carrega instruções do arquivo ganchos-hormozi/SKILL.md
    """
    # Carrega instruções completas do arquivo .md
    instructions = loader.load_agent_instructions("ganchos-hormozi", "SKILL.md")

    return Agent(
        role="Copywriter Especialista em Ganchos Virais",
        goal="Criar ganchos emocionais de alto engajamento usando técnica Hormozi",
        backstory=instructions,
        verbose=True,
        allow_delegation=False  # Peão não delega
    )


def create_analyst_agent() -> Agent:
    """
    Analista de Qualidade (Middle)
    Avalia ganchos usando critérios específicos
    """
    backstory = """
Você é um Analista de Qualidade sênior especializado em copy viral.

## Sua Missão
Avaliar ganchos criados pelo copywriter usando critérios objetivos e sugerir melhorias concretas.

## Critérios de Avaliação (Checklist)

✅ **Especificidade Numérica** (0-10)
- Tem números concretos? (datas, valores, quantidades)
- Os números são hiper-específicos? (não arredondados)

✅ **Contradição Clara** (0-10)
- Existe paradoxo/contradição? (fez X, resultado oposto Y)
- A contradição é imediatamente identificável?

✅ **Testemunhas/Validação** (0-10)
- Menciona pessoas que viram/julgaram?
- Tem prova social específica?

✅ **Timeline Concreta** (0-10)
- Períodos de tempo específicos?
- Sequência de eventos clara?

✅ **Momento de Virada** (0-10)
- Termina com "até descobrir" ou similar?
- Gera curiosidade sem revelar?

✅ **Linguagem Emocional** (0-10)
- Tom confessional e íntimo?
- Evita jargões técnicos?

✅ **Impacto Visual** (0-10)
- Seria impactante visualmente em feed?
- Para o scroll?

## Formato de Avaliação

Ao avaliar um gancho, você DEVE retornar:

**NOTAS:**
- Especificidade: X/10
- Contradição: X/10
- Testemunhas: X/10
- Timeline: X/10
- Virada: X/10
- Emoção: X/10
- Impacto: X/10

**NOTA FINAL:** XX/70

**STATUS:** ✅ APROVADO (60+) ou ❌ REPROVAR (<60)

**FEEDBACK:** (se reprovar)
- Problema 1: [descrição] → Sugestão: [correção específica]
- Problema 2: [descrição] → Sugestão: [correção específica]

## Tom de Voz
- Direto e objetivo
- Crítico construtivo
- Específico (nunca vago)
- Sempre sugere melhorias concretas, não apenas aponta problemas
"""

    return Agent(
        role="Analista de Qualidade de Copy",
        goal="Avaliar ganchos usando critérios objetivos e sugerir melhorias específicas",
        backstory=backstory,
        verbose=True,
        allow_delegation=True  # Pode pedir revisões ao copywriter
    )


def create_director_agent() -> Agent:
    """
    Diretor Criativo (Senior)
    Aprova versão final ou solicita ajustes estratégicos
    """
    # Carrega instruções do copywriter para entender o contexto
    copywriter_instructions = loader.load_agent_instructions("openrouter", "copywriter-vendas.md")

    backstory = f"""
Você é o Diretor Criativo responsável pela aprovação final de copy.

## Seu Papel
Você recebe ganchos que já foram revisados pelo Analista. Sua função é:
1. Validar se atende aos objetivos de negócio
2. Verificar alinhamento com voz da marca
3. Aprovar ou solicitar ajustes estratégicos finais

## Contexto do Copywriter
{copywriter_instructions}

## Critérios de Aprovação

✅ **Aprovação Imediata** quando:
- Nota do Analista ≥ 60/70
- Alinhado com técnica Hormozi
- Linguagem adequada para público-alvo
- Potencial viral claro

❌ **Solicitar Revisão** quando:
- Desalinhamento estratégico com marca
- Tom inadequado para público
- Falta clareza no gancho
- Potencial de interpretação negativa

⚠️ **Feedback Estratégico** (não técnico):
- Você não corrige gramática ou números
- Você avalia visão macro e estratégia
- Foca em impacto de negócio

## Formato de Resposta

**DECISÃO:** ✅ APROVADO ou ❌ REVISAR

**JUSTIFICATIVA:** [breve explicação da decisão]

**AJUSTES ESTRATÉGICOS** (se reprovar):
- [ajuste de posicionamento/tom/mensagem]

**VERSÃO FINAL** (se aprovar):
[o gancho aprovado, sem modificações]
"""

    return Agent(
        role="Diretor Criativo",
        goal="Aprovar versão final de ganchos garantindo alinhamento estratégico",
        backstory=backstory,
        verbose=True,
        allow_delegation=True  # Pode pedir revisões aos outros
    )


def create_tasks(agents: dict, input_data: dict) -> list[Task]:
    """
    Cria as tasks para o fluxo de trabalho

    Args:
        agents: Dict com os agentes {copywriter, analyst, director}
        input_data: Dict com inputs do usuário {nicho, tema, objetivo}
    """

    task_criar = Task(
        description=f"""
Crie um gancho viral para:

**Nicho:** {input_data.get('nicho', 'não especificado')}
**Tema:** {input_data.get('tema', 'não especificado')}
**Objetivo:** {input_data.get('objetivo', 'engajamento máximo')}

Use a Técnica Hormozi de especificidade brutal.

Entregue no formato:
GANCHO VIRAL:
[o gancho]

TÉCNICA APLICADA:
- Números específicos: [...]
- Contradição: [...]
- Testemunhas: [...]
- Timeline: [...]
- Virada: [...]
""",
        expected_output="Gancho viral formatado com técnicas aplicadas explícitas",
        agent=agents['copywriter']
    )

    task_avaliar = Task(
        description=f"""
Avalie o gancho criado pelo copywriter usando o checklist de 7 critérios.

IMPORTANTE: Você receberá o gancho completo criado na task anterior no contexto.
Avalie EXATAMENTE o gancho que foi produzido, não invente outro texto.

Se a nota for inferior a 60/70, REPROVE e forneça feedback específico.
Se for 60+, APROVE e passe para o diretor.

Seja rigoroso e específico nas sugestões de melhoria.
""",
        expected_output="Avaliação completa com notas, status e feedback detalhado",
        agent=agents['analyst'],
        context=[task_criar]  # 🔥 Injeta o output da task anterior automaticamente
    )

    task_aprovar = Task(
        description=f"""
Revise a avaliação do analista e o gancho final.

IMPORTANTE: Você receberá tanto o gancho original quanto a avaliação do analista no contexto.

Se tudo estiver alinhado estrategicamente, APROVE e apresente a versão final.
Se houver desalinhamento estratégico, solicite ajustes.

Lembre-se: você avalia estratégia e impacto de negócio, não detalhes técnicos.
""",
        expected_output="Decisão final com justificativa e versão aprovada do gancho",
        agent=agents['director'],
        context=[task_criar, task_avaliar]  # 🔥 Injeta AMBOS os outputs anteriores
    )

    return [task_criar, task_avaliar, task_aprovar]


def run_copywriter_crew(input_data: dict) -> str:
    """
    Executa a crew de copywriting completa

    Args:
        input_data: Dict com {nicho, tema, objetivo}

    Returns:
        Resultado final da crew (gancho aprovado)
    """
    print("🚀 Iniciando Crew de Copywriting...")
    print(f"📋 Input: {input_data}\n")

    # Cria agentes
    agents = {
        'copywriter': create_copywriter_agent(),
        'analyst': create_analyst_agent(),
        'director': create_director_agent()
    }

    # Cria tasks
    tasks = create_tasks(agents, input_data)

    # Cria crew com processo HIERARCHICAL
    # Isso adiciona automaticamente um Manager que coordena e cria feedback loops
    # No CrewAI 1.2+, precisamos configurar o manager_llm explicitamente
    from crewai import LLM

    manager_llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.hierarchical,  # 🔥 Ativa feedback loops automáticos
        manager_llm=manager_llm,       # 🔥 LLM do Manager (CrewAI 1.2+)
        verbose=True
    )

    # Executa crew
    print("\n⚙️  Executando crew (isso pode levar alguns minutos)...\n")
    result = crew.kickoff()

    return result


# Exemplo de uso direto
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 CREWAI - COPYWRITER CREW")
    print("=" * 60)
    print()

    # Exemplo de input
    input_example = {
        'nicho': 'Emagrecimento',
        'tema': 'Exercícios abdominais não funcionam sozinhos',
        'objetivo': 'Gerar 100k+ visualizações no Instagram'
    }

    # Executa crew
    resultado = run_copywriter_crew(input_example)

    print("\n" + "=" * 60)
    print("✅ RESULTADO FINAL")
    print("=" * 60)
    print(resultado)
