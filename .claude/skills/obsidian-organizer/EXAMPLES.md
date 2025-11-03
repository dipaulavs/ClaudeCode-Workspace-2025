# Obsidian Organizer - Exemplos Práticos

## 📋 Exemplo 1: Criar Tarefa

**Usuário diz:**
> "Preciso lembrar de ligar pro cliente amanhã"

**Skill identifica:** Tarefa (palavra-chave: "preciso")

**Ação:**
Criar arquivo em `📋 Tarefas/Ligar pro cliente.md`

```yaml
---
criada: 03/11/2025 14:30
status: aberta
---

# Ligar pro cliente

## 📝 Detalhes

Ligar para o cliente amanhã para acompanhamento.

## ✅ Checklist
- [ ] Preparar pontos da conversa
- [ ] Fazer a ligação
```

**Resposta:**
```
✅ Tarefa criada!

📋 Ligar pro cliente
📍 Salva em: 📋 Tarefas/
⏰ Criada: 03/11/2025 14:30

Ver em: [[📊 Tarefas]] ou [[📋 Tarefas/📊 Kanban|Kanban]]
```

---

## 💡 Exemplo 2: Anotação Rápida

**Usuário diz:**
> "Vi um artigo interessante sobre IA: https://exemplo.com - fala sobre modelos multimodais"

**Skill identifica:** Anotação (palavra-chave: "vi", tem link)

**Ação:**
Criar arquivo em `💡 Anotações/Artigo sobre modelos multimodais.md`

```yaml
---
criada: 03/11/2025 14:32
tags:
  - anotacao
  - ia
---

# Artigo sobre modelos multimodais

https://exemplo.com

Artigo interessante sobre IA que fala sobre modelos multimodais.
```

**Resposta:**
```
✅ Anotação salva!

💡 Artigo sobre modelos multimodais
📍 Salva em: 💡 Anotações/
⏰ 03/11/2025 14:32

Ver em: [[📝 Anotações]]
```

---

## 📺 Exemplo 3: Vídeo YouTube

**Usuário diz:**
> "Assisti um tutorial no YouTube sobre Claude Code: https://youtube.com/watch?v=abc123
>
> Ensina como usar skills customizadas. Principais pontos:
> - Skills são automáticas
> - Progressive disclosure
> - Estrutura com 4 arquivos"

**Skill identifica:** Vídeo (URL YouTube, palavra-chave: "tutorial")

**Ação:**
Criar arquivo em `📺 Vídeos/Tutorial Claude Code Skills.md`

```yaml
---
assistido: 03/11/2025 14:35
categoria: tutorial
link: https://youtube.com/watch?v=abc123
tags:
  - youtube
  - claude-code
---

# Tutorial Claude Code Skills

## 🎬 Informações

**Link:** https://youtube.com/watch?v=abc123
**Categoria:** tutorial
**Assistido em:** 03/11/2025 14:35

---

## 📝 Resumo

Tutorial completo sobre como criar e usar skills customizadas no Claude Code.

---

## 💡 Principais Aprendizados

- Skills são ativadas automaticamente (model-invoked)
- Progressive disclosure organiza informação
- Estrutura recomendada: SKILL.md + REFERENCE.md + EXAMPLES.md + TROUBLESHOOTING.md
- Skills melhoram muito a produtividade

---

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Cole aqui a transcrição quando disponível]
```

**Resposta:**
```
✅ Vídeo registrado!

📺 Tutorial Claude Code Skills
📍 Salva em: 📺 Vídeos/
⏰ Assistido: 03/11/2025 14:35
🏷️ Categoria: tutorial

Ver em: [[📺 Vídeos]]
```

---

## 📺 Exemplo 4: Vídeo com Transcrição

**Usuário diz:**
> "Salva esse vídeo que assisti sobre GPT-4o:
> Link: https://youtube.com/watch?v=xyz789
> Categoria: notícia
>
> Resumo: Lançamento do GPT-4o com novas features
>
> Transcrição:
> [transcrição longa de 1000+ palavras aqui]"

**Ação:**
```yaml
---
assistido: 03/11/2025 14:40
categoria: noticia
link: https://youtube.com/watch?v=xyz789
tags:
  - youtube
  - ia
  - gpt4
---

# GPT-4o - Novidades

## 🎬 Informações

**Link:** https://youtube.com/watch?v=xyz789
**Categoria:** noticia
**Assistido em:** 03/11/2025 14:40

---

## 📝 Resumo

Lançamento do GPT-4o com novas features multimodais.

---

## 💡 Principais Aprendizados

- [Extraídos do contexto ou perguntados ao usuário]

---

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Transcrição longa de 1000+ palavras aqui]
> [Começa oculta, expande ao clicar]
```

**Resposta:**
```
✅ Vídeo com transcrição salvo!

📺 GPT-4o - Novidades
📍 Salva em: 📺 Vídeos/
⏰ Assistido: 03/11/2025 14:40
🏷️ Categoria: notícia
📄 Transcrição: Incluída (oculta)

Ver em: [[📺 Vídeos]]
```

---

## 🔄 Exemplo 5: Múltiplos Itens

**Usuário diz:**
> "Preciso anotar 3 coisas:
> 1. Tarefa: comprar café
> 2. Ideia: app de gestão de tempo
> 3. Vídeo que vi sobre React hooks"

**Skill identifica:** 3 tipos diferentes

**Ação:** Criar 3 arquivos

1. `📋 Tarefas/Comprar café.md` (tarefa)
2. `💡 Anotações/App de gestão de tempo.md` (anotação)
3. `📺 Vídeos/React Hooks.md` (vídeo - pedir link)

**Resposta:**
```
✅ 3 itens criados!

📋 Comprar café (Tarefa)
💡 App de gestão de tempo (Anotação)
📺 React Hooks (Vídeo)

Dashboards atualizados:
- [[📊 Tarefas]]
- [[📝 Anotações]]
- [[📺 Vídeos]]
```

---

## 🎯 Exemplo 6: Ambiguidade

**Usuário diz:**
> "Salva isso: aprender Python"

**Ambíguo:** Pode ser tarefa OU anotação

**Skill pergunta:**
```
"Aprender Python" - é uma:
1. 📋 Tarefa (algo para fazer)
2. 💡 Anotação (ideia/referência)

Qual prefere?
```

**Usuário:** "Tarefa"

**Ação:** Criar como tarefa

---

## 🔄 Exemplo 7: Adicionar ao Kanban

**Usuário diz:**
> "Cria tarefa 'Revisar documentação' e já coloca no Kanban em andamento"

**Ação:**
1. Criar arquivo em `📋 Tarefas/Revisar documentação.md`
2. Adicionar ao Kanban em "🔨 Em Andamento"

**Kanban atualizado:**
```markdown
## 🔨 Em Andamento

- [ ] [[Revisar documentação]]
```

**Resposta:**
```
✅ Tarefa criada e adicionada ao Kanban!

📋 Revisar documentação
📍 Kanban: 🔨 Em Andamento
⏰ Criada: 03/11/2025 14:45

Ver: [[📋 Tarefas/📊 Kanban|Kanban Board]]
```

---

## 🎨 Exemplo 8: Estilo Minimalista

**Usuário diz:**
> "Anota que preciso estudar DataView do Obsidian"

**❌ Resposta excessiva (evitar):**
```
🎉 Ótimo! Vou criar uma anotação incrível para você sobre DataView!
É uma ferramenta super poderosa do Obsidian que vai revolucionar...
[3 parágrafos desnecessários]
```

**✅ Resposta minimalista (correto):**
```
✅ Anotação criada!

💡 Estudar DataView do Obsidian
📍 Salva em: 💡 Anotações/
⏰ 03/11/2025 14:50
```

---

## 📊 Exemplo 9: Verificar Última Criação

**Usuário diz:**
> "Qual foi a última coisa que anotei?"

**Skill verifica:** Dashboards (última criação de qualquer tipo)

**Resposta:**
```
Última anotação:

📺 Tutorial Claude Code Skills
📍 📺 Vídeos/
⏰ 03/11/2025 14:35
🏷️ tutorial

Outros recentes:
- 💡 Artigo sobre modelos multimodais (14:32)
- 📋 Ligar pro cliente (14:30)
```

---

## 🔍 Exemplo 10: Buscar por Categoria

**Usuário diz:**
> "Mostra os vídeos de tutorial que salvei"

**Skill usa:** DataView query ou lista manualmente

**Resposta:**
```
📺 Vídeos - Categoria: tutorial

1. Tutorial Claude Code Skills (03/11/2025 14:35)
2. [outros tutoriais salvos]

Ver todos em: [[📺 Vídeos]]
```

---

## 💡 Dicas de Implementação

### Tom de Comunicação
- **Conciso:** 2-3 linhas máximo
- **Direto:** Sem enrolação
- **Minimalista:** Sem emojis excessivos
- **Confirmação clara:** O que foi feito + onde está

### Erros Comuns a Evitar
1. ❌ Perguntar demais antes de criar
2. ❌ Respostas longas e cheias de explicação
3. ❌ Criar em local errado
4. ❌ Esquecer data/hora brasileira
5. ❌ Poluir com formatação excessiva
6. ❌ Vídeos sem categoria
7. ❌ Transcrição não colapsável

### Checklist Pré-Criação
- [ ] Tipo identificado corretamente?
- [ ] Local correto determinado?
- [ ] Data/hora no formato brasileiro?
- [ ] Template apropriado aplicado?
- [ ] Todos os campos obrigatórios preenchidos?
- [ ] Estilo minimalista mantido?

---

**Referências:**
- [[SKILL.md]] - Instruções principais
- [[REFERENCE.md]] - Detalhes técnicos
- [[TROUBLESHOOTING.md]] - Problemas comuns
