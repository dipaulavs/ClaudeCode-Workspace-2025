# 🚀 Início Rápido - CrewAI

## ⚡ 3 Passos para Começar

### 1️⃣ Configure sua API Key (30 segundos)

```bash
# Edite o arquivo .env
nano crewai/.env

# Substitua esta linha:
OPENROUTER_API_KEY=sua_chave_openrouter_aqui

# Por sua chave real da OpenRouter:
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
```

**Obtenha sua chave gratuita em:** https://openrouter.ai/keys

---

### 2️⃣ Teste o Exemplo Pronto (2-3 minutos)

```bash
cd ~/Desktop/ClaudeCode-Workspace/crewai

# Execute a crew de copywriting
python3 crews/copywriter_crew.py
```

**O que vai acontecer:**

```
🚀 Iniciando Crew de Copywriting...
📋 Input: {'nicho': 'Emagrecimento', 'tema': '...', 'objetivo': '...'}

⚙️  Executando crew...

🤖 Copywriter: Criando gancho viral...
📊 Analista: Avaliando qualidade (critérios 1-7)...
🔄 Manager: Solicitando revisão (nota < 60)...
🤖 Copywriter: Corrigindo com feedback...
📊 Analista: Reavaliando... ✅ Aprovado!
👔 Diretor: Aprovação final...

✅ RESULTADO FINAL
---
[Gancho viral aprovado e validado]
```

---

### 3️⃣ Crie Sua Própria Crew

#### Opção A: Use seus agentes .md existentes

```python
# Copie e adapte: crews/copywriter_crew.py
from md_loader import MDLoader

loader = MDLoader()

# Carrega instruções do seu agente
instructions = loader.load_agent_instructions("ganchos-hormozi", "SKILL.md")

# Usa no agent
agent = Agent(
    role="Seu Role",
    goal="Seu Goal",
    backstory=instructions  # 🔥 Instruções completas do .md
)
```

#### Opção B: Crie novo agente .md

```bash
# 1. Crie pasta para novo agente
mkdir -p agentes/meu-agente

# 2. Crie arquivo de instruções
nano agentes/meu-agente/SKILL.md
```

```markdown
# Meu Agente Especializado

Você é um [ESPECIALISTA] que [FAZ O QUE].

## Expertise
- [Habilidade 1]
- [Habilidade 2]

## Como Trabalhar
[Passo a passo detalhado]

## Exemplos
[Exemplos práticos]

## Regras
✅ FAZER:
- [Regra 1]

❌ NÃO FAZER:
- [Proibição 1]
```

```python
# 3. Use no seu script
instructions = loader.load_agent_instructions("meu-agente", "SKILL.md")
```

---

## 📚 Comandos Úteis

### Listar Agentes Disponíveis
```bash
cd ~/Desktop/ClaudeCode-Workspace/crewai
python3 utils/md_loader.py
```

### Testar Conexão OpenRouter
```bash
cd ~/Desktop/ClaudeCode-Workspace/crewai

# Crie teste.py:
cat > teste.py << 'EOF'
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")
if api_key and api_key != "sua_chave_openrouter_aqui":
    print("✅ API Key configurada!")
    print(f"Chave: {api_key[:20]}...")
else:
    print("❌ API Key não configurada. Edite o .env")
EOF

python3 teste.py
```

### Ver Estrutura Completa
```bash
tree crewai/
# ou
find crewai -type f
```

---

## 🎯 Casos de Uso Práticos

### 1. Criar Copy com Revisão Automática
✅ **Já está pronto!** Execute: `python3 crews/copywriter_crew.py`

### 2. Gerar Headlines + Analisar + Aprovar
```python
# Adapte copywriter_crew.py:
# - Agent 1: Gera 5 headlines
# - Agent 2: Avalia cada uma (0-10)
# - Agent 3: Escolhe a melhor
```

### 3. Pesquisa → Escrita → Fact-checking
```python
# Crie research_crew.py:
# - Agent 1: Pesquisa tema (usa tool de busca)
# - Agent 2: Escreve artigo baseado na pesquisa
# - Agent 3: Fact-checks e valida fontes
```

### 4. Brainstorm → Refinamento → Priorização
```python
# Crie ideation_crew.py:
# - Agent 1: Gera 20 ideias criativas
# - Agent 2: Refina as 5 melhores
# - Agent 3: Prioriza por viabilidade
```

---

## ⚙️ Configurações Comuns

### Mudar para Claude Sonnet (mais poderoso)
```bash
# No .env, mude para:
OPENAI_MODEL_NAME=anthropic/claude-3-5-sonnet-20250131
```

### Mudar para Modelo Grátis
```bash
# No .env, mude para:
OPENAI_MODEL_NAME=meta-llama/llama-3.3-70b-instruct:free
```

### Desabilitar Verbose (menos logs)
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=False  # Silencioso
)
```

### Processo Sequencial (sem feedback loops)
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential  # Linear A→B→C
)
```

---

## 🐛 Problemas Comuns

### "No module named 'crewai'"
```bash
pip3 install --user crewai
```

### "OPENROUTER_API_KEY not found"
Edite `crewai/.env` e configure sua chave.

### Crew não respeita instruções?
1. Use modelo mais poderoso (Claude Sonnet)
2. Torne as instruções mais específicas
3. Adicione exemplos práticos no .md

### Muito lento?
1. Use Claude Haiku 4.5 (padrão)
2. Use `Process.sequential`
3. Reduza número de agentes

---

## 📖 Documentação Completa

Leia: `crewai/README.md`

---

## ✅ Checklist de Sucesso

- [ ] API Key configurada no `.env`
- [ ] Testei `python3 utils/md_loader.py` (lista agentes)
- [ ] Executei `python3 crews/copywriter_crew.py` (exemplo)
- [ ] Li `crewai/README.md` (documentação completa)
- [ ] Criei minha primeira crew personalizada

**Pronto! Você está usando CrewAI com seus agentes .md! 🎉**
