# 🏗️ Builder Orchestrator - Orquestração Inteligente de Projetos

## Quando Usar

Automaticamente quando usuário mencionar:
- "Quero criar uma ferramenta..."
- "Preciso de um workflow..."
- "Cria uma skill..."
- "Implementar [funcionalidade]..."
- "Fazer uma campanha de..."

**Objetivo:** Criar ferramentas/skills/workflows otimizados usando **paralelização máxima** e **recursos existentes**.

---

## Workflow Automático (4 Etapas)

### Etapa 1: Análise Completa do Contexto 🔍

Mapear recursos disponíveis:
1. **Skills existentes** → `.claude/skills/` (14 skills)
2. **Templates prontos** → `scripts/` (67+ templates)
3. **Ferramentas low-level** → `tools/` (40+ ferramentas)
4. **Capacidades Claude Code** → Subagentes paralelos (Task tool), MCP, etc.

### Etapa 2: Identificação de Paralelização ⚡

Analisar a tarefa:
1. **Quebrar em sub-processos independentes**
2. **Identificar o que pode rodar em paralelo**
3. **Mapear dependências** (o que precisa esperar o quê)
4. **Planejar delegação** para subagentes via Task tool

### Etapa 3: Plano Estruturado 📋

Apresentar ao usuário:
```
🎯 Plano Otimizado:

Recursos Disponíveis:
- Skill X (para headlines)
- Template Y (para imagens)
- Ferramenta Z (para publicação)

Execução Paralela:
├─ Subagente 1: [tarefa independente]
├─ Subagente 2: [tarefa independente]
└─ Subagente 3: [tarefa independente]

Combinação Final: [integração dos resultados]

Tempo estimado: Xmin (vs Ymin sequencial)
```

### Etapa 4: Delegação e Execução 🚀

**REGRA CRÍTICA:** Se precisar criar NOVA skill:
- ✅ **SEMPRE** delegar para `skill-creator`
- ✅ Aguardar criação (Progressive Disclosure)
- ✅ Integrar no workflow final

Executar usando subagentes paralelos quando possível.

---

## Princípios Fundamentais

- ⚡ **Agilidade:** Maximizar velocidade (paralelização)
- 🔧 **Praticidade:** Usar recursos existentes (zero retrabalho)
- ⏱️ **Tempo:** Otimizar duração total
- 🧠 **Inteligência:** Conhecimento completo do workspace
- 🏗️ **Padronização:** Skills via `skill-creator` (Progressive Disclosure)

---

## Docs Adicionais

- **Framework completo:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos de uso:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Troubleshooting:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (ativação automática)
**Versão:** 1.0
