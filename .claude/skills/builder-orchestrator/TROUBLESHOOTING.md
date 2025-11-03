# 🔧 Builder Orchestrator - Troubleshooting

## Erro 1: Paralelização Falhou (Dependências Não Respeitadas)

### Sintoma
```
Erro: Subagente 2 falhou porque esperava resultado de Subagente 1
Task tool retornou: "File not found: transcricao.txt"
```

### Causa
Tentou executar tarefas **dependentes** em paralelo.

### Exemplo do Problema
```
❌ ERRADO (paralelo quando há dependência):
- Task 1: Transcrever vídeo → transcricao.txt
- Task 2: Analisar transcricao.txt (precisa do Task 1!)

Resultado: Task 2 falha (arquivo não existe ainda)
```

### Solução
**Respeitar ordem de dependências:**
```
✅ CORRETO (sequencial quando há dependência):
1. Primeiro: Transcrever vídeo → transcricao.txt
2. Depois: Lançar tarefas paralelas que usam transcricao.txt
   ├─ Task 1: Gerar apresentação
   ├─ Task 2: Gerar headlines
   └─ Task 3: Salvar nota Obsidian
```

### Checklist de Prevenção
- [ ] Identifiquei quais tarefas precisam de resultados de outras?
- [ ] Separei em "Fase 1 (dependências)" e "Fase 2 (paralelo)"?
- [ ] Verifiquei que tarefas paralelas são realmente independentes?

---

## Erro 2: Recurso Existente Não Foi Usado (Retrabalho)

### Sintoma
```
Skill criou novo script para gerar imagens em lote
Mas já existe scripts/image-generation/batch_generate.py
```

### Causa
**Não consultou recursos existentes** antes de criar novo.

### Exemplo do Problema
```
❌ ERRADO:
Usuário: "Preciso gerar 5 imagens"
Skill: Cria novo script generate_5_images.py

Problema: Já existe batch_generate.py que faz isso!
```

### Solução
**SEMPRE consultar mapeamento de recursos primeiro:**

1. **Ler CLAUDE.md seção Mapa de Ações**
2. **Verificar se existe skill/template para a tarefa**
3. **Só criar novo se não existir equivalente**

```
✅ CORRETO:
Usuário: "Preciso gerar 5 imagens"
Skill:
  1. Consulta CLAUDE.md → Encontra batch_generate.py
  2. Apresenta plano: "Usar batch_generate.py existente"
  3. Executa: python3 scripts/image-generation/batch_generate.py ...
```

### Checklist de Prevenção
- [ ] Consultei seção `📍 MAPA DE AÇÕES` do CLAUDE.md?
- [ ] Consultei seção `🧠 CLAUDE SKILLS` do CLAUDE.md?
- [ ] Verifiquei se existe template batch para 2+ itens?
- [ ] Confirmei que NÃO existe equivalente antes de criar?

---

## Erro 3: Subagente Criou Arquivo Temporário (Violação CLAUDE.md)

### Sintoma
```
Subagente criou test_headlines.py na raiz
CLAUDE.md proíbe scripts descartáveis/temporários
```

### Causa
Subagente não seguiu **Regra 2 (Preferência por Templates)** do CLAUDE.md.

### Exemplo do Problema
```
❌ ERRADO:
Task 1: "Crie script para testar 3 headlines"
Resultado: test_headlines.py criado na raiz

Problema: Viola organização + é descartável
```

### Solução
**Instruir subagente explicitamente sobre regras:**

```
✅ CORRETO:
Task 1: "Use hormozi-leads skill para gerar 3 headlines.
         NÃO criar scripts temporários (CLAUDE.md regra 2).
         Retornar headlines diretamente no output."

Resultado: Headlines geradas sem criar arquivos
```

### Checklist de Prevenção
- [ ] Instrui subagente para usar recursos existentes?
- [ ] Deixei claro que scripts temporários são proibidos?
- [ ] Especifiquei formato de output esperado?

---

## Erro 4: Skill Criada Sem Progressive Disclosure

### Sintoma
```
skill-creator criou apenas SKILL.md (arquivo único)
Faltam: REFERENCE.md, EXAMPLES.md, TROUBLESHOOTING.md
```

### Causa
**skill-creator não foi usado** ou foi mal instruído.

### Exemplo do Problema
```
❌ ERRADO:
builder-orchestrator cria skill diretamente
Resultado: 1 arquivo gigante sem estrutura

Problema: Viola padrão Progressive Disclosure
```

### Solução
**SEMPRE delegar para skill-creator:**

```
✅ CORRETO:
builder-orchestrator identifica necessidade de nova skill
  ↓
Delega para skill-creator via Skill tool
  ↓
skill-creator cria 4 arquivos automaticamente:
  - SKILL.md (30-60 linhas)
  - REFERENCE.md (docs técnicas)
  - EXAMPLES.md (mínimo 2)
  - TROUBLESHOOTING.md (mínimo 2)
```

### Checklist de Prevenção
- [ ] Usei Skill tool para invocar skill-creator?
- [ ] Aguardei criação completa (4 arquivos)?
- [ ] Verifiquei que estrutura está completa?

---

## Erro 5: Plano Apresentado Não Mostra Ganho de Tempo

### Sintoma
```
Plano: "Executar A, depois B, depois C"
Usuário: "Mas isso é sequencial, cadê a otimização?"
```

### Causa
**Não destacou paralelização e ganho de tempo** no plano.

### Exemplo do Problema
```
❌ ERRADO:
🎯 PLANO:
1. Gerar headlines
2. Gerar imagens
3. Criar carrossel

(Sem mencionar paralelização ou tempo)
```

### Solução
**SEMPRE mostrar execução paralela + tempo estimado:**

```
✅ CORRETO:
🎯 PLANO OTIMIZADO:

EXECUÇÃO PARALELA (3 subagentes simultâneos):
├─ Subagente 1: Headlines (~2min)
├─ Subagente 2: Imagens (~2min)
└─ Subagente 3: Template (~2min)

TEMPO TOTAL: ~2min (vs ~6min sequencial)
GANHO: 67% mais rápido
```

### Checklist de Prevenção
- [ ] Identifiquei tarefas independentes para paralelizar?
- [ ] Estimei tempo de cada etapa?
- [ ] Calculei tempo total vs sequencial?
- [ ] Mostrei ganho percentual?

---

## Erro 6: Não Atualizou CLAUDE.md Após Criar Recurso

### Sintoma
```
Nova skill/template criado
CLAUDE.md não reflete novo recurso
Próxima vez, skill não usa (porque não sabe que existe)
```

### Causa
**Esqueceu Etapa 4 (Documentação)** do workflow.

### Exemplo do Problema
```
❌ ERRADO:
Criou real-estate-campaign skill
NÃO atualizou CLAUDE.md
Semana depois: Usuário pede campanha de imóvel
Skill não usa real-estate-campaign (não sabe que existe!)
```

### Solução
**SEMPRE atualizar CLAUDE.md após criar recurso:**

```
✅ CORRETO:
1. Criar skill/template
2. Atualizar CLAUDE.md:
   - Adicionar em Mapa de Ações (se template)
   - Adicionar em Skills Disponíveis (se skill)
   - Atualizar contadores
3. Fazer commit descritivo
4. Mostrar ao usuário
```

### Checklist de Prevenção
- [ ] Atualizei CLAUDE.md após criar recurso?
- [ ] Adicionei na seção correta (Mapa ou Skills)?
- [ ] Atualizei contadores (X skills → X+1)?
- [ ] Fiz commit descritivo?

---

## FAQ - Perguntas Frequentes

### P1: Quando usar batch vs múltiplas chamadas individuais?

**R:** SEMPRE usar batch para 2+ itens. É regra obrigatória do CLAUDE.md.

```
✅ CORRETO:
2+ imagens → batch_generate.py --api nanobanana
2+ vídeos → batch_generate.py
2+ áudios → batch_generate.py

❌ ERRADO:
2 imagens → chamar generate_nanobanana.py 2 vezes
```

### P2: Posso criar skill sem usar skill-creator?

**R:** NÃO. skill-creator garante Progressive Disclosure (padrão obrigatório).

### P3: Como saber se tarefa é independente ou dependente?

**R:** Pergunte: "Tarefa B precisa do resultado de Tarefa A?"
- Se SIM → Dependente (sequencial)
- Se NÃO → Independente (paralelo)

### P4: Quantos subagentes posso lançar em paralelo?

**R:** Máximo recomendado: 3-5 subagentes simultâneos.
- Mais que isso: alto custo de tokens
- Menos que isso: desperdiça oportunidade de otimização

### P5: Devo sempre priorizar velocidade?

**R:** SIM, mas nunca sacrificar qualidade:
- ✅ Paralelizar sempre que possível
- ❌ Não pular documentação
- ❌ Não criar arquivos bagunçados

---

**Outros problemas?** Consulte exemplos em [EXAMPLES.md](EXAMPLES.md) ou framework em [REFERENCE.md](REFERENCE.md).
