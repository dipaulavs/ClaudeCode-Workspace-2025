# Army of Agents - Troubleshooting

## Erro 1: Loop Infinito de Iterações

### Sintoma

```
Round 4... Round 5... Round 6...
Skill continua iterando sem aprovar resultado final
```

### Causa

- Crítico muito severo (nunca aprova)
- Critérios de aprovação não claros
- Feedback circular (A pede X, B pede contrário)

### Solução

**Prevenir:**

No prompt do Crítico, adicionar:
```
IMPORTANTE: Nota 8+ = APROVADO. Não busque perfeição absoluta.
Feedback deve ser acionável, não filosófico.
```

No Orquestrador, implementar:
```python
max_rounds = 3  # LIMITE RÍGIDO

if current_round >= max_rounds:
    # Força aprovação da melhor versão disponível
    return melhor_versao_ate_agora
```

**Diagnosticar:**

Se já aconteceu, verifique:
1. Nota do Crítico está sempre <8? → Relaxe critérios
2. Feedback contradiz round anterior? → Simplifique avaliação
3. Diretor discorda do Crítico sempre? → Alinhe critérios

---

## Erro 2: Roles Inadequados Escolhidos

### Sintoma

```
Tarefa: "Criar hook de emagrecimento"
Roles ativados: Estrategista, Designer de Conteúdo, Revisor

Resultado: Copy genérica, sem impacto Hormozi
```

### Causa

Orquestrador não identificou necessidade de **Crítico Hormozi** para tarefa de hook.

### Solução

**Prevenir:**

Mapear palavras-chave que ativam roles específicos:

| Palavra-chave | Role obrigatório |
|---------------|------------------|
| "hook", "headline", "Hormozi" | Crítico Hormozi |
| "landing page", "estrutura" | Designer de Conteúdo |
| "público-alvo", "dores" | Pesquisador |
| "estratégia", "plano" | Estrategista |

No SKILL.md, adicionar checklist:
```
Antes de definir roles, pergunte:
1. Tarefa menciona Hormozi/copy persuasiva? → Crítico Hormozi obrigatório
2. Tarefa precisa estrutura? → Designer de Conteúdo obrigatório
3. Tarefa precisa insights de mercado? → Pesquisador obrigatório
```

**Diagnosticar:**

Se output for genérico:
1. Roles incluíram Crítico Hormozi? → Se não, refaça com ele
2. Pesquisador foi consultado? → Se não, falta contexto de público
3. Só tem Copywriter? → Não suficiente para alta qualidade

---

## Erro 3: Feedback Genérico (Não Acionável)

### Sintoma

```
Crítico: "Opção 2 está boa, mas pode melhorar. Tente ser mais criativo."
Copywriter: "...?" (não sabe o que fazer)
```

### Causa

Feedback vago sem sugestão específica.

### Solução

**Prevenir:**

No prompt do Crítico, especificar formato de feedback:

```
Feedback DEVE incluir:
1. O QUE está ruim (específico)
2. POR QUÊ está ruim (critério violado)
3. COMO melhorar (sugestão acionável)

❌ Ruim: "Falta impacto"
✅ Bom: "Falta curiosity (Core Four). Adicione pergunta provocativa no início.
         Exemplo: 'E se eu te dissesse que...'"
```

**Diagnosticar:**

Se Copywriter não conseguiu melhorar após feedback:
1. Feedback tinha sugestão concreta? → Se não, refaça crítica
2. Sugestão é acionável em 1 mudança? → Se não, simplifique
3. Crítico explicou POR QUÊ? → Se não, adicione critério

---

## Erro 4: Tempo/Custo Muito Alto

### Sintoma

```
Tarefa: Hook simples
Tempo: 8 minutos
Custo: $0.20

Esperado: 2-3min, $0.03-0.05
```

### Causa

- Roles desnecessários ativados
- Execução sequencial quando poderia ser paralela
- Iterações excessivas

### Solução

**Prevenir:**

Matriz de complexidade:

| Tarefa | Roles mínimos | Execução | Tempo esperado |
|--------|---------------|----------|----------------|
| Hook/Headline | 3 (Pesquisador, Copywriter, Crítico) | Sequencial | 2-3min |
| Landing page | 5 (+ Estrategista, Designer) | Misto | 5-6min |
| Email sequence | 4 (Pesquisador, Estrategista, Copywriter, Crítico) | Sequencial | 4-5min |

**Regra de ouro:** Tarefa simples = máx 3 roles

**Diagnosticar:**

Se tempo/custo estourou:
1. Quantos roles ativados? → >5 para tarefa simples = overkill
2. Execução foi paralela quando possível? → Otimize
3. Quantas iterações? → >3 = loop (ver Erro 1)

**Otimização:**

```python
# Identificar tarefas independentes
if tarefa_simples:
    # Pesquisador e Designer podem rodar paralelo
    resultados = await asyncio.gather(
        Task(prompt_pesquisador),
        Task(prompt_designer)
    )
```

---

## Erro 5: Conflito Entre Agentes

### Sintoma

```
Crítico: "Opção 2 é melhor (nota 9/10)"
Diretor: "Discordo. Opção 1 é superior."

Resultado: Confusão, nenhuma decisão clara
```

### Causa

- Critérios de avaliação diferentes
- Roles com objetivos conflitantes
- Falta hierarquia clara

### Solução

**Prevenir:**

Estabelecer hierarquia no SKILL.md:

```
Ordem de prioridade:
1. Diretor Criativo (decisão final)
2. Crítico Hormozi (avaliação técnica)
3. Copywriter (execução)
```

No prompt do Diretor:
```
Você tem VETO FINAL. Se discordar do Crítico, justifique com base estratégica
(não só gosto pessoal). Sua decisão é definitiva.
```

**Diagnosticar:**

Se agentes discordam:
1. Ambos explicaram critérios? → Se não, peça justificativa
2. Conflito é técnico ou estratégico? → Priorize estratégia (Diretor)
3. Há consenso em algum ponto? → Use como base

**Resolução:**

Diretor deve:
1. Reconhecer pontos do Crítico
2. Explicar por que discorda
3. Tomar decisão final baseada em objetivo da tarefa

---

## Erro 6: Output Inconsistente Entre Runs

### Sintoma

```
Run 1: Hook excelente (nota 9/10)
Run 2: Hook medíocre (nota 6/10) - mesma tarefa

Inconsistência frustra usuário
```

### Causa

- Prompts dos roles não são determinísticos
- Falta contexto fixo (ex: frameworks, exemplos)
- Ordem de execução varia

### Solução

**Prevenir:**

Adicionar contexto fixo em REFERENCE.md:

```python
CONTEXT_HORMOZI = """
Core Four (Alex Hormozi):
1. Make them feel
2. Make them think
3. Make them act
4. Make them trust

Lead Getters:
- Curiosity
- Controversy
- Big Promise
- Urgency
"""

# Injetar em TODOS os prompts relevantes
prompt_critico = f"{CONTEXT_HORMOZI}\n\n{prompt_especifico}"
```

**Fixar ordem de execução:**

```python
# Sempre mesma sequência
ordem_fixa = [
    "Pesquisador",
    "Copywriter",
    "Crítico Hormozi",
    "Diretor Criativo"
]
```

**Diagnosticar:**

Se output varia muito:
1. Prompts incluem frameworks/exemplos? → Se não, adicione
2. Ordem de roles é fixa? → Se não, padronize
3. Contexto está sendo passado? → Verifique no log

---

## Erro 7: Skill Não Ativa Automaticamente

### Sintoma

```
Usuário: "Cria um hook com múltiplas perspectivas"
Claude: [Não ativa army-of-agents, responde diretamente]
```

### Causa

Frase do usuário não match com gatilhos do SKILL.md.

### Solução

**Prevenir:**

Expandir gatilhos no SKILL.md:

```
AUTO-INVOCA quando usuário pede:
- "múltiplas perspectivas"
- "vários agentes"
- "exército de agentes"
- "alta qualidade"
- "resultado diferenciado"
- "validar com múltiplos pontos de vista"
- "preciso do melhor [tarefa]"
```

**Workaround:**

Usuário pode forçar ativação:
```
"Use army-of-agents para criar [tarefa]"
```

---

## Checklist de Debug

Se algo der errado, verifique na ordem:

1. **Roles corretos?** → Ver Erro 2
2. **Tempo razoável?** → Ver Erro 4
3. **Iteração infinita?** → Ver Erro 1
4. **Feedback acionável?** → Ver Erro 3
5. **Conflito entre agentes?** → Ver Erro 5
6. **Output inconsistente?** → Ver Erro 6
7. **Skill não ativou?** → Ver Erro 7

## Logs Úteis

Para debug, orquestrador deve logar:

```python
print(f"[Army] Roles ativados: {roles}")
print(f"[Army] Round {current_round}/{max_rounds}")
print(f"[Army] Aprovado: {aprovado}")
print(f"[Army] Custo estimado: ${custo:.2f}")
```

Usuário vê resumo ao final, mas logs internos ajudam a debugar.
