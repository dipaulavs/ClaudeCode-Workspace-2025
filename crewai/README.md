# 🤖 CrewAI - Sistema de Agentes Colaborativos

Sistema de múltiplos agentes usando CrewAI com instruções carregadas dos seus arquivos `.md` existentes.

## 🎯 O Que É Isso?

CrewAI permite criar **equipes de agentes especializados** que trabalham juntos de forma colaborativa, com **feedback loops automáticos** para refinamento iterativo.

### Conceitos Principais

- **Agents (Agentes)**: Especialistas com roles, goals e instruções detalhadas
- **Tasks (Tarefas)**: Trabalho que cada agente deve executar
- **Crew (Equipe)**: Coordenação entre agentes
- **Process (Processo)**:
  - `Sequential`: Linear (A → B → C)
  - `Hierarchical`: Manager automático coordena e cria feedback loops

## 📁 Estrutura

```
crewai/
├── .env                        # Configuração OpenRouter
├── README.md                   # Esta documentação
├── utils/
│   └── md_loader.py           # Carrega arquivos .md como instruções
└── crews/
    └── copywriter_crew.py     # Exemplo: Copywriter → Analista → Diretor
```

## ⚙️ Configuração

### 1. Configurar API Key da OpenRouter

Edite o arquivo `.env`:

```bash
# Substitua por sua chave real
OPENROUTER_API_KEY=sk-or-v1-SUA_CHAVE_AQUI
```

**Obtenha sua chave em:** https://openrouter.ai/keys

### 2. Escolher Modelo LLM

O padrão é **Claude Haiku 4.5** (rápido e econômico). Para mudar:

```bash
# Edite .env e descomente a linha do modelo desejado:

# Claude Sonnet 4.5 (mais poderoso):
OPENAI_MODEL_NAME=anthropic/claude-3-5-sonnet-20250131

# GPT-4o:
OPENAI_MODEL_NAME=openai/gpt-4o

# Gemini 2.5 Pro:
OPENAI_MODEL_NAME=google/gemini-2.0-flash-exp:free

# Llama 3.3 70B (grátis):
OPENAI_MODEL_NAME=meta-llama/llama-3.3-70b-instruct:free
```

## 🚀 Como Usar

### Exemplo 1: Crew de Copywriting (Pronto para Usar)

Executa um fluxo completo de criação de copy com **revisão iterativa automática**:

**Copywriter (Peão)** → **Analista (Middle)** → **Diretor (Senior)**

```bash
cd ~/Desktop/ClaudeCode-Workspace/crewai

# Execute a crew de exemplo
python3 crews/copywriter_crew.py
```

**O que acontece:**
1. 🤖 Copywriter cria gancho viral usando técnica Hormozi
2. 📊 Analista avalia (0-70 pontos) e reprova se < 60
3. 🔄 Se reprovado, Manager automático coordena revisão
4. 👔 Diretor aprova versão final
5. ✅ Resultado: Gancho aprovado e validado

### Exemplo 2: Uso Programático

```python
from crews.copywriter_crew import run_copywriter_crew

# Configure o input
input_data = {
    'nicho': 'Emagrecimento',
    'tema': 'Dietas restritivas não funcionam',
    'objetivo': '100k+ visualizações no Instagram'
}

# Execute a crew
resultado = run_copywriter_crew(input_data)

print(resultado)
```

### Exemplo 3: Testar MDLoader

Verifica quais agentes `.md` estão disponíveis:

```bash
cd ~/Desktop/ClaudeCode-Workspace/crewai

# Lista todos os agentes disponíveis
python3 utils/md_loader.py
```

**Saída esperada:**
```
🤖 Agentes disponíveis:
   - ganchos-hormozi
      └─ SKILL.md
      └─ diretrizes.md
      └─ exemplos-hormozi.md
      └─ checklist-execucao.md
   - imagem-colada
      └─ SKILL.md
   - openrouter
      └─ copywriter-vendas.md
      └─ analista-negocios.md
      └─ README.md
```

## 🏗️ Como Funciona

### 1. Carregamento de Instruções via .md

```python
from md_loader import MDLoader

loader = MDLoader()

# Carrega instruções de um agente
instructions = loader.load_agent_instructions("ganchos-hormozi", "SKILL.md")

# Usa como backstory do agente
agent = Agent(
    role="Copywriter Especialista",
    goal="Criar ganchos virais",
    backstory=instructions  # 🔥 Instruções completas do .md
)
```

### 2. Processo Hierarchical (Feedback Loops Automáticos)

Quando você usa `Process.hierarchical`:

```python
crew = Crew(
    agents=[copywriter, analista, diretor],
    tasks=[criar, avaliar, aprovar],
    process=Process.hierarchical  # 🔥 Ativa Manager automático
)
```

**O CrewAI automaticamente:**
1. Cria um **Manager Agent** invisível
2. Manager coordena o fluxo de trabalho
3. Se o Analista reprovar (< 60 pontos):
   - Manager delega revisão ao Copywriter
   - Copywriter corrige com feedback específico
   - Analista reavalia
   - Loop até aprovação (ou limite de tentativas)

### 3. Agentes com Delegação

```python
agent = Agent(
    role="Analista",
    goal="Avaliar qualidade",
    backstory="...",
    allow_delegation=True  # 🔥 Pode pedir ajuda a outros agentes
)
```

## 📝 Criar Sua Própria Crew

### Passo 1: Organize Suas Instruções em .md

Crie um arquivo `.md` em `agentes/seu-agente/`:

```markdown
# Seu Agente Expert

Você é um [ROLE] especializado em [EXPERTISE].

## Sua Missão
[Descrição detalhada do objetivo]

## Como Você Trabalha
[Metodologia passo a passo]

## Exemplos
[Exemplos práticos]

## Regras
[O que fazer e não fazer]
```

### Passo 2: Crie Seu Script Python

```python
# crews/minha_crew.py
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from md_loader import MDLoader

load_dotenv(Path(__file__).parent.parent / ".env")
loader = MDLoader()

# Crie seus agentes
agent1 = Agent(
    role="Especialista 1",
    goal="Fazer X",
    backstory=loader.load_agent_instructions("seu-agente", "SKILL.md"),
    allow_delegation=False
)

agent2 = Agent(
    role="Revisor",
    goal="Validar X",
    backstory="Instruções do revisor...",
    allow_delegation=True
)

# Crie as tasks
task1 = Task(
    description="Crie X para o tema: {tema}",
    expected_output="X formatado e completo",
    agent=agent1
)

task2 = Task(
    description="Revise X e aprove ou sugira melhorias",
    expected_output="Decisão com justificativa",
    agent=agent2
)

# Crie a crew
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.hierarchical,  # Feedback loops automáticos
    verbose=True
)

# Execute
resultado = crew.kickoff(inputs={'tema': 'Seu tema aqui'})
print(resultado)
```

### Passo 3: Execute

```bash
python3 crews/minha_crew.py
```

## 🔧 Dicas e Boas Práticas

### 1. Instruções Longas (Sem Limites)

✅ **Seus arquivos .md podem ter quantos caracteres quiser**
- O `backstory` do agente aceita textos gigantes
- CrewAI suporta instruções de 10k+ caracteres sem problema
- Quanto mais específico, melhor o agente performa

### 2. Modelos Recomendados por Caso

| Tarefa | Modelo | Motivo |
|--------|--------|--------|
| Copywriting criativo | Claude Sonnet 4.5 | Melhor criatividade e tom |
| Análise/Avaliação | Claude Haiku 4.5 | Rápido e objetivo |
| Código | GPT-4o | Melhor para programação |
| Brainstorm | Gemini 2.5 Pro | Grátis e bom |
| Produção em massa | Llama 3.3 70B | Grátis e rápido |

### 3. Hierárquico vs Sequencial

Use **Hierarchical** quando:
- ✅ Precisa de feedback loops (revisões iterativas)
- ✅ Qualidade é mais importante que velocidade
- ✅ Tem agentes com allow_delegation=True

Use **Sequential** quando:
- ✅ Fluxo linear simples (A → B → C, sem volta)
- ✅ Velocidade é prioridade
- ✅ Não precisa de revisões

### 4. Verbose Mode

Deixe `verbose=True` durante desenvolvimento:

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=True  # Veja todo o processo
)
```

Você verá:
- 🤔 Pensamento de cada agente
- 💬 Comunicação entre agentes
- 🔄 Feedback loops acontecendo
- ✅ Decisões tomadas

### 5. Custos OpenRouter

**Claude Haiku 4.5** (padrão):
- ~$0.50 por 1M tokens de entrada
- ~$1.00 por 1M tokens de saída
- Crew completa: ~$0.05 - $0.15 por execução

**Modelos Grátis:**
- Gemini 2.5 Pro (via OpenRouter)
- Llama 3.3 70B (via OpenRouter)

## 📚 Recursos

### Documentação Oficial
- **CrewAI Docs**: https://docs.crewai.com
- **OpenRouter**: https://openrouter.ai/docs
- **LiteLLM**: https://docs.litellm.ai

### Seus Agentes Existentes
- `agentes/ganchos-hormozi/` - Técnica Hormozi completa
- `agentes/openrouter/` - Copywriter e Analista de Negócios
- `agentes/imagem-colada/` - Agente de imagens

### Arquivos Deste Sistema
- `utils/md_loader.py` - Carregador de instruções .md
- `crews/copywriter_crew.py` - Exemplo funcional completo
- `.env` - Configuração da API

## 🐛 Troubleshooting

### Erro: "No module named 'crewai'"
```bash
pip3 install --user crewai
```

### Erro: "OPENROUTER_API_KEY not found"
```bash
# Edite crewai/.env e adicione sua chave
OPENROUTER_API_KEY=sk-or-v1-SUA_CHAVE_AQUI
```

### Erro: "Rate limit exceeded"
Aguarde alguns segundos ou mude para modelo grátis:
```bash
# No .env:
OPENAI_MODEL_NAME=meta-llama/llama-3.3-70b-instruct:free
```

### Agentes não seguem instruções?
1. Verifique se o .md foi carregado: `python3 utils/md_loader.py`
2. Use modelo mais poderoso (Claude Sonnet 4.5)
3. Torne as instruções ainda mais específicas

### Crew muito lenta?
1. Use Claude Haiku 4.5 (padrão) ou Llama 3.3 70B
2. Mude para `Process.sequential` (sem feedback loops)
3. Reduza número de agentes/tasks

## 🎉 Próximos Passos

1. ✅ Configure sua chave OpenRouter no `.env`
2. ✅ Teste o exemplo: `python3 crews/copywriter_crew.py`
3. ✅ Liste seus agentes: `python3 utils/md_loader.py`
4. ✅ Crie sua própria crew usando seus arquivos `.md`

**Divirta-se criando equipes de agentes inteligentes! 🚀**
