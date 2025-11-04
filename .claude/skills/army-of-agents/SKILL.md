# Army of Agents

**Tipo:** Model-invoked (ativa automaticamente)
**Custo:** Variável (~$0.03-0.15 por tarefa, dependendo de roles e iterações)
**Tempo:** 2-8 minutos

## Quando Usar

AUTO-INVOCA quando usuário pede:
- "Criar [conteúdo] com múltiplas perspectivas"
- "Quero um resultado de alta qualidade em [tarefa criativa]"
- "Use vários agentes para [tarefa]"
- "Exército de agentes para [tarefa]"

Ideal para:
- Copy crítica (hooks, headlines, CTAs)
- Landing pages
- Email sequences
- Roteiros de vídeo
- Propostas comerciais

## Como Funciona

### Fase 1: Análise + Definição de Roles (30s)

1. Analisa tarefa do usuário
2. Define 3-5 roles necessários (ver REFERENCE.md)
3. Monta ordem de execução (paralelo quando possível)

Roles comuns:
- **Pesquisador:** Analisa público, dores, desejos
- **Copywriter:** Cria conteúdo inicial
- **Crítico Hormozi:** Avalia com metodologia Core Four + Lead Getters
- **Diretor Criativo:** Decisões finais, ajustes estratégicos
- **Revisor:** Gramática, clareza, tom

### Fase 2: Execução Multi-Agente (1-3min)

1. Lança subagentes com Task tool (paralelo quando possível)
2. Cada subagente trabalha em sua função específica
3. Output de um alimenta próximo (sequencial quando necessário)

### Fase 3: Feedback Mútuo + Iteração (1-4min)

1. **Round 1:** Crítico avalia output do Copywriter (nota 1-10 + feedback brutal)
2. **Round 2:** Copywriter refina com base no feedback
3. **Round 3:** Diretor escolhe melhor versão + ajuste final (se necessário)
4. **Aprovação:** Retorna resultado validado por múltiplas perspectivas

**Limite:** Máximo 3 rounds de iteração (previne loops infinitos)

## Output

Mostra SEMPRE ao usuário:
1. **Roles ativados:** Quais agentes trabalharam
2. **Processo:** Resumo do que cada agente fez
3. **Iterações:** Feedback dado e mudanças aplicadas
4. **Resultado final:** Conteúdo aprovado

## Progressive Disclosure

- **Dúvidas técnicas?** → `REFERENCE.md`
- **Ver exemplos completos?** → `EXAMPLES.md`
- **Erros?** → `TROUBLESHOOTING.md`
