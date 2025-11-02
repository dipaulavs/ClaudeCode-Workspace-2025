# ⚡ Quick Start - Claude Skills

Guia rápido para começar a usar as 5 Skills instaladas.

---

## 🎯 Teste Rápido (5 Minutos)

### 1️⃣ Validar uma Ideia
```
Valide esta ideia: app de receitas geradas por IA personalizado para ingredientes que você tem em casa
```

**Esperado:** Claude usa `idea-validator` automaticamente e retorna análise de mercado, concorrentes, viabilidade.

---

### 2️⃣ Criar Roadmap
```
Ajude-me a planejar o MVP de um app de to-do list com IA que sugere prioridades
```

**Esperado:** Claude usa `launch-planner` e entrega PRD completo, schema de DB, roadmap de 2 semanas.

---

### 3️⃣ Melhorar Design
```
Crie uma landing page moderna para um SaaS de analytics
```

**Esperado:** Claude usa `product-designer` e cria componentes React com Tailwind, paleta de cores profissional.

---

### 4️⃣ Escrever Marketing
```
Escreva um tweet de lançamento para este projeto
```

**Esperado:** Claude usa `marketing-writer`, analisa o código atual, e cria tweet focado em benefícios.

---

### 5️⃣ Priorizar Features
```
Quais features devo adicionar a seguir no meu projeto?
```

**Esperado:** Claude usa `roadmap-builder`, lê o código, e sugere features com matriz impacto/esforço.

---

## 🔍 Como Saber Se Está Funcionando?

### Indicadores de Sucesso:

✅ **Claude menciona a Skill** - "Vou usar a skill [nome]..."
✅ **Análise contextual** - Claude lê arquivos do projeto automaticamente
✅ **Output estruturado** - Respostas seguem formato definido na Skill
✅ **Ferramentas limitadas** - Claude usa apenas tools permitidas na Skill

### Se Não Funcionar:

❌ Skill não é mencionada
❌ Resposta genérica
❌ Não analisa o código

**Solução:**
1. Mencione a Skill explicitamente: `"Use a skill [nome] para..."`
2. Verifique se o arquivo está em `.claude/skills/[nome]/SKILL.md`
3. Recarregue a janela do Claude Code

---

## 📋 Cheat Sheet - Frases de Ativação

### idea-validator
```
"Valide esta ideia: [descrição]"
"Isso vale a pena construir?"
"Deve gastar tempo com isso?"
"Analise esta ideia de app"
```

### launch-planner
```
"Planeje o lançamento de [app]"
"Crie um PRD para [ideia]"
"Como estruturo este MVP?"
"Preciso de um roadmap de 2 semanas"
```

### product-designer
```
"Crie uma landing page moderna"
"Melhore o design deste componente"
"Faça isso parecer profissional"
"Design de dashboard clean"
```

### marketing-writer
```
"Escreva uma landing page"
"Crie um tweet de lançamento"
"Copy para Product Hunt"
"Email de anúncio do produto"
```

### roadmap-builder
```
"Quais features adicionar?"
"Preciso de um roadmap"
"O que construir a seguir?"
"Priorize estas funcionalidades"
```

---

## 🚀 Workflow Completo - Exemplo Real

### Cenário: Lançar um SaaS em 2 Semanas

**Dia 1 - Validação:**
```
Valide esta ideia: SaaS que automatiza posts no LinkedIn usando IA
```
→ `idea-validator` analisa mercado, dá feedback honesto

---

**Dia 1 - Planejamento:**
```
Planeje o MVP deste SaaS de automação LinkedIn em 2 semanas
```
→ `launch-planner` cria PRD, schema, roadmap

---

**Dias 2-10 - Desenvolvimento:**
```
Crie a landing page seguindo as melhores práticas de design
```
→ `product-designer` cria UI profissional

---

**Dia 11 - Marketing:**
```
Escreva materiais de lançamento para este projeto
```
→ `marketing-writer` cria landing page, tweet, Product Hunt description

---

**Dia 14 - Pós-Lançamento:**
```
Quais features devo adicionar com base no feedback inicial?
```
→ `roadmap-builder` prioriza próximos passos

---

## 💡 Dicas Pro

### 1. Combine Skills
```
1. "Valide esta ideia: [descrição]"
2. [Se aprovada] "Planeje o MVP desta ideia"
3. "Crie o design da landing page"
4. "Escreva o conteúdo de marketing"
```

### 2. Contexto Automático
Skills **leem seu código automaticamente**. Não precisa explicar o projeto:

❌ Ruim:
```
"Escreva um tweet para meu app que é um SaaS de analytics com Next.js..."
```

✅ Bom:
```
"Escreva um tweet de lançamento"
```
→ Skill lê README.md, package.json, e entende sozinha

### 3. Iteração Rápida
```
"Melhore este design" → Skill analisa código atual
"Adicione dark mode" → Skill mantém contexto
"Otimize para mobile" → Skill itera sobre versão anterior
```

---

## 🎓 Próximos Passos

1. ✅ Teste as 5 Skills com prompts acima
2. ✅ Use em projeto real
3. ✅ Crie sua própria Skill customizada (veja `README.md`)
4. ✅ Compartilhe com time via git

---

## 📚 Documentação Completa

- **README Completo:** `.claude/skills/README.md`
- **Documentação CLAUDE.md:** Seção "🧠 CLAUDE SKILLS"
- **Docs Oficiais:** https://docs.claude.com/en/docs/claude-code/skills.md

---

**Tempo para dominar:** ~30 minutos testando cada Skill
**Produtividade ganho:** 10x (segundo o vídeo original)
**Investimento:** 0 (Skills já instaladas e prontas)

🚀 **Comece agora! Teste o primeiro comando acima.**
