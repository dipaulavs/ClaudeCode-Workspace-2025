# 🔧 Adaptive Mentor - Troubleshooting

## Problema 1: Explicação Muito Técnica (Usuário Não Entendeu)

### Sintoma
```
Usuário: "Não entendi o que você quis dizer com 'serialização de objetos'"
```

### Causa Raiz
- Skill assumiu conhecimento prévio incorretamente
- Usou jargão técnico sem traduzir para analogia primeiro
- Pulou etapa de explicação ELI5

### Como Identificar
- Usuário responde: "Não entendi", "Explica melhor", "Mas o que é X?"
- Usuário pede para "simplificar"
- Usuário não confirma o plano (silêncio)

### Solução

**Imediata:**
```markdown
"Deixa eu explicar de um jeito mais simples!

[Conceito Técnico] é como [Analogia do Cotidiano].

Por exemplo: [Exemplo concreto e visual]

Faz sentido agora? Quer que eu explique alguma parte específica?"
```

**Preventiva (para próximas vezes):**
1. **Sempre** começar com analogia antes de termos técnicos
2. **Perguntar nível** de conhecimento se ambíguo
3. **Validar entendimento** após cada conceito complexo
4. **Usar hierarquia**: Analogia → Diagrama → Termo Técnico

### Exemplo Corrigido

❌ **Ruim:**
```
"Vou implementar serialização JSON dos objetos ORM com lazy loading."
```

✅ **Bom:**
```
"Vou fazer seu app 'traduzir' os dados do banco para um formato que
qualquer sistema consiga ler (JSON).

É como pegar um livro em português e criar uma versão em inglês -
o conteúdo é o mesmo, só muda o formato.

No código, isso significa que quando você buscar um usuário do banco,
eu vou transformar ele em algo assim:

{
  "nome": "João",
  "email": "joao@example.com"
}

Ficou claro?"
```

---

## Problema 2: Plano Muito Vago (Não Executável)

### Sintoma
```
Usuário: "Ok, mas... como exatamente você vai fazer isso?"
```

### Causa Raiz
- Plano técnico faltando detalhes
- Não especificou arquivos/comandos concretos
- Usuário não consegue visualizar a execução

### Como Identificar
- Usuário pede mais detalhes
- Usuário não confirma execução (hesita)
- Perguntas sobre "qual arquivo", "que comando"

### Solução

**Sempre incluir no plano técnico:**

```markdown
## 🛠️ Plano Técnico de Execução

### Ferramentas que vou usar:
- [Ferramenta 1]: [Propósito específico]
- [Ferramenta 2]: [Propósito específico]

### Arquivos que vou criar:
- `path/to/new_file.py` - [O que faz]

### Arquivos que vou modificar:
- `path/to/existing.py:123` - [O que vou mudar]

### Comandos que vou executar:
```bash
comando1 aqui
comando2 aqui
```

### Resultado esperado:
[Descrever estado final]
```

### Checklist de Plano Completo

Antes de apresentar, validar:
- [ ] Especifiquei **caminhos completos** dos arquivos?
- [ ] Listei **comandos exatos** a executar?
- [ ] Mostrei **resultado esperado** de cada etapa?
- [ ] Indiquei **tempo estimado**?
- [ ] Mencionei **dependências** (se houver)?

### Exemplo Corrigido

❌ **Vago:**
```
"Vou adicionar autenticação no seu app."
```

✅ **Específico:**
```
## 🛠️ Plano de Implementação - Autenticação

### O que vou fazer:

1. **Instalar biblioteca de autenticação**
   ```bash
   pip install flask-login
   ```

2. **Criar modelo de usuário**
   - Arquivo: `models/user.py` (novo)
   - Conteúdo: Classe User com email/senha/hash

3. **Adicionar rotas de login/logout**
   - Arquivo: `routes/auth.py` (novo)
   - Rotas: `/login`, `/logout`, `/register`

4. **Proteger rotas existentes**
   - Arquivo: `routes/dashboard.py:5` (modificar)
   - Adicionar decorator `@login_required`

5. **Criar templates HTML**
   - `templates/login.html` (novo)
   - `templates/register.html` (novo)

### Resultado final:
- Usuários poderão criar conta
- Login com email/senha
- Dashboard só acessível após login
- Sessão persiste 7 dias

⏱️ Tempo: 15-20 minutos

**Posso executar?**
```

---

## Problema 3: Usuário Quer Pular Explicação (Já Conhece o Conceito)

### Sintoma
```
Usuário: "Já sei o que é API, só implementa logo"
```

### Causa Raiz
- Usuário é avançado e skill assumiu iniciante
- Explicação detalhada desnecessária para este caso

### Como Identificar
- Usuário usa jargões técnicos corretos
- Pede para "ir direto ao ponto"
- Menciona que "já tentou X" (indica conhecimento)

### Solução

**Ajustar tom imediatamente:**
```markdown
"Entendido! Vou direto à implementação.

[Plano técnico conciso, sem ELI5]

Confirma?"
```

**Adaptar nível de detalhe:**
- **Iniciante:** Analogias + diagramas + explicações
- **Intermediário:** Conceitos técnicos + justificativas
- **Avançado:** Direto ao ponto + trade-offs

### Exemplo Corrigido

❌ **Muito didático para avançado:**
```
"Cache é como um caderninho de anotações...
[5 parágrafos de analogias]"
```

✅ **Direto para avançado:**
```
"Vou implementar Redis como cache layer:

- LRU eviction policy
- TTL de 1h para dados de usuário
- Cache-aside pattern
- Invalidação por evento

Dependências:
- redis-py
- celery (invalidação async)

Confirma?"
```

---

## Problema 4: Executou Sem Mostrar Plano Primeiro

### Sintoma
```
[Skill cria arquivos imediatamente sem aguardar confirmação]
Usuário: "Espera, não era isso que eu queria..."
```

### Causa Raiz
- Violação da regra: **SEMPRE** apresentar plano antes de executar
- Skill interpretou mal o contexto
- Pulou etapa de confirmação

### Como Identificar
- Ferramentas Write/Edit/Bash usadas sem output de plano primeiro
- Usuário corrige/desfaz ações

### Solução

**NUNCA executar sem antes:**
1. Apresentar plano dual (simples + técnico)
2. Aguardar confirmação explícita do usuário
3. Só então executar

**Template obrigatório:**
```markdown
[Explicação do que vou fazer]

## 🎯 Plano

### Visão Geral: [...]
### Plano Técnico: [...]

**Posso executar?** / **Confirma?** / **Quer que eu implemente isso?**

[AGUARDAR RESPOSTA DO USUÁRIO]
```

### Exceções (pode executar direto)
- Comandos informativos (Read, Grep, ls, git status)
- Usuário pediu explicitamente: "Executa", "Faz", "Implementa já"

---

## Problema 5: Analogia Não Fez Sentido (Contexto Cultural)

### Sintoma
```
Usuário: "Não entendi a analogia do basebol, não conheço esse esporte"
```

### Causa Raiz
- Analogia usou referência cultural não universal
- Assumiu conhecimento de contextos específicos

### Solução

**Usar analogias universais:**
✅ Cotidiano doméstico (cozinha, casa, supermercado)
✅ Transporte (carro, ônibus, avião)
✅ Relacionamentos (amigos, família)
✅ Natureza (plantas, animais, clima)

❌ Evitar:
- Esportes específicos (baseball, cricket)
- Referências pop culture nicho
- Contextos profissionais específicos (finanças complexas)

**Quando analogia falhar:**
```markdown
"Deixa eu tentar outra analogia mais clara:

[Nova analogia + universal]

Ou prefere que eu mostre direto com um exemplo de código?"
```

---

## Problema 6: Plano Muito Longo (Usuário Desistiu de Ler)

### Sintoma
```
[Skill apresenta 20 etapas detalhadas]
Usuário: "Muito complexo, simplifica"
```

### Causa Raiz
- Quebrou task complexo em micro-etapas
- Plano ficou intimidador
- Falta de agrupamento lógico

### Solução

**Agrupar em fases digestíveis (máx 5-7):**

❌ **Muito granular:**
```
1. Criar pasta models
2. Criar arquivo __init__.py
3. Criar arquivo user.py
4. Importar SQLAlchemy
5. Definir classe User
[... 15 etapas mais]
```

✅ **Agrupado:**
```
1. **Setup inicial** (estrutura + dependências)
2. **Criar modelos** (User + Auth)
3. **Implementar rotas** (login/logout)
4. **Testar** (validação)

Cada fase tem sub-etapas, mas vou executar uma por vez mostrando progresso.
```

**Para tarefas grandes:**
```markdown
## 🎯 Visão Geral (Fases)

1. Fase 1 - [Nome] (5 min)
2. Fase 2 - [Nome] (10 min)
3. Fase 3 - [Nome] (5 min)

Total: ~20 min

**Quer que eu detalhe alguma fase específica ou posso começar?**
```

---

## Problema 7: Skill Não Ativou Quando Deveria

### Sintoma
```
Usuário pediu explicação simples, mas skill adaptive-mentor não ativou
```

### Causa Raiz
- Trigger phrase não matchou os patterns definidos
- Outro comportamento padrão tomou prioridade

### Triggers Esperados
- "explica [X] de forma simples"
- "como fazer [Y]"
- "preciso de ajuda com [Z]"
- "me ajuda a criar/implementar [W]"
- "quero entender [conceito]"

### Solução para Usuários

Se skill não ativar, **mencionar explicitamente**:
```
"Usa a skill adaptive-mentor para me explicar [conceito]"
```

### Solução para Claude Code

Se identifiquei que deveria ter ativado:
```markdown
"Vou usar a skill adaptive-mentor para te ajudar com isso.

[Segue workflow normal da skill]"
```

---

## Checklist de Qualidade (Auto-Validação)

Antes de enviar resposta, verificar:

- [ ] Comecei com analogia/ELI5?
- [ ] Criei diagrama visual?
- [ ] Dei exemplo prático concreto?
- [ ] Plano dual (simples + técnico)?
- [ ] Pedi confirmação antes de executar?
- [ ] Linguagem acessível (sem jargões não explicados)?
- [ ] Plano tem máx 5-7 etapas principais?
- [ ] Especifiquei arquivos/comandos exatos?

---

## Quando Pedir Ajuda/Clarificação

Perguntar ao usuário se:
- Nível de conhecimento ambíguo
- Múltiplas abordagens válidas (pedir preferência)
- Contexto técnico faltando (arquitetura atual)
- Requisitos não claros

**Template:**
```markdown
"Antes de continuar, preciso entender melhor:

1. [Pergunta específica]
2. [Outra pergunta]

Isso me ajuda a criar o plano perfeito para você!"
```

---

## Recursos Adicionais

- **SKILL.md**: Workflow principal
- **REFERENCE.md**: Técnicas detalhadas + templates
- **EXAMPLES.md**: 5 casos de uso reais
