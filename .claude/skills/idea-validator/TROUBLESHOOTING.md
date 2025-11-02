# Idea Validator - Solução de Problemas

## Problema 1: Pesquisa superficial / Faltam dados

### Sintoma
A análise de validação parece genérica, sem dados específicos ou competidores nomeados.

### Causa
- WebSearch não foi usada adequadamente
- Queries muito vagas
- Tempo insuficiente de research

### Solução

**Use queries específicas e múltiplas:**

```bash
# Em vez de:
"note taking app competitors"  # Muito vago

# Use múltiplas queries específicas:
1. "[idea] app alternative"
2. "[idea] software pricing"
3. "[idea] vs [competitor name]"
4. "best [category] tools 2025"
5. "[idea] market size"
```

**Exemplos práticos:**

**Para "Markdown to Twitter converter":**
```
1. "markdown twitter thread converter"
2. "typefully alternative"
3. "developer twitter tools pricing"
4. "repurpose blog content twitter"
5. "twitter automation tools"
```

**Fontes confiáveis para pesquisar:**
- Product Hunt (lançamentos recentes + reviews)
- AlternativeTo (comparação de competidores)
- IndieHackers (revenue de produtos indie)
- G2/Capterra (reviews B2B)
- Reddit r/SaaS (feedback honesto)

**Template de research:**

```markdown
## Competitors Research Checklist:

[ ] Buscou 5+ queries diferentes no Google
[ ] Encontrou 3-5 competidores diretos
[ ] Verificou pricing de cada um (WebFetch landing pages)
[ ] Leu reviews (positivas E negativas)
[ ] Checou Product Hunt para launches similares
[ ] Buscou no Reddit/Twitter reclamações sobre o problema
[ ] Verificou Google Trends (demanda crescendo ou caindo?)
```

**Tempo mínimo:**
- 10-15 minutos de research focused
- Não menos que isso ou análise fica superficial

---

## Problema 2: Muito otimista / Não sendo brutalmente honesto

### Sintoma
A avaliação sempre conclui "BUILD IT" ou ignora red flags óbvios.

### Causa
- Viés para encorajar o usuário
- Não aplicando framework crítico
- Ignorando evidências negativas

### Solução

**Lembrar da missão da skill:**
> "Prevent builders from wasting weeks on bad ideas"

**É MELHOR:**
- ❌ Matar ideia ruim em 15 minutos
- ✅ Do que deixar builder gastar 4 semanas

**Red flags que DEVEM resultar em "SKIP IT":**

1. **Market saturation EXTREME:**
   - 10+ competidores estabelecidos
   - Gigantes tech (Google, Meta) dominam
   - Commoditização completa

2. **Zero diferenciação:**
   - "É como X mas com UI bonita" (não é suficiente)
   - Competidor pode copiar em 1 sprint
   - Nenhuma vantagem defensável

3. **Demanda imaginária:**
   - Zero evidência de pessoas buscando isso
   - "Achismo" sem dados
   - Problema que "deveria existir" mas não existe

4. **Unrealistic para solo builder:**
   - 6+ meses de desenvolvimento
   - Requer infra complexa (real-time, ML custom)
   - Tech stack completamente nova

5. **Monetização impossível:**
   - Precisa de milhões de users para viabilizar
   - Ninguém pagaria por isso
   - Modelo não existe

**Framework de honestidade:**

Antes de dar o veredicto, pergunte:
1. "Eu investiria meu próprio tempo nisso?"
2. "Se um amigo me contasse essa ideia, o que eu diria?"
3. "Quais são os 3 maiores riscos? Eles são mitigáveis?"

**Template de veredicto honesto:**

```markdown
🎯 QUICK VERDICT: SKIP IT

**Por que:**
[Seja específico sobre os red flags encontrados]

**O que fazer em vez disso:**
[Sugira um pivot concreto OU uma ideia relacionada mais viável]
```

**Exemplo de honestidade brutal:**

```
User: "Valide: rede social para developers"

Response:
🎯 QUICK VERDICT: SKIP IT

**Por que:**
1. Market absurdamente saturado: GitHub, Twitter, LinkedIn, Dev.to, Hashnode
2. Network effects são impossíveis de competir (todos já estão lá)
3. Monetização difícil (devs odeiam ads, não pagam por social)
4. Build time: 6+ meses para algo minimamente comparável
5. Zero diferenciação clara (seria "mais uma" rede)

**O que fazer em vez disso:**
Não construa OUTRA rede social. Construa uma FEATURE que falta em redes existentes:

- "Code snippet sharing with live preview" (integra com Twitter/LinkedIn)
- "Portfolio builder que auto-sync do GitHub" (complementa, não compete)
- "Dev event discovery tool" (usa APIs das redes existentes)
```

---

## Problema 3: Avaliação muito genérica (não personalizada)

### Sintoma
A análise parece template copy-paste, sem considerar contexto específico do usuário.

### Causa
- Não fazendo perguntas de clarificação
- Assumindo contexto sem verificar
- Não adaptando framework à situação

### Solução

**Faça perguntas antes de validar (se necessário):**

```markdown
Para validar melhor, preciso entender:

1. **Experiência:**
   - Já construiu produtos antes?
   - Familiaridade com tech stack necessário?

2. **Recursos:**
   - Solo builder ou tem time?
   - Orçamento para APIs/infra? ($0, $100/mês, $1K/mês?)

3. **Timeline:**
   - Quanto tempo pode dedicar? (noites/fins de semana, full-time?)
   - Deadline? (quer lançar em 1 mês, 6 meses?)

4. **Objetivo:**
   - Side project ou full-time business?
   - Expectativa de revenue? ($500/mês, $5K/mês, $50K/mês?)
```

**Adapte a análise ao contexto:**

**Exemplo A: Iniciante + $0 budget + side project**
```
⚙️ BUILD FEASIBILITY

Para iniciante com $0 budget:
- ✅ Usa stack que já conhece (não aprenda React+Node+PostgreSQL ao mesmo tempo)
- ✅ Managed services free tier (Vercel, Supabase, Railway)
- ❌ Evite: Payments (Stripe compliance), Auth custom (use Clerk/Auth0)
- Timeline: 6-8 semanas (está aprendendo)
```

**Exemplo B: Experiente + $500/mês budget + full-time**
```
⚙️ BUILD FEASIBILITY

Para builder experiente full-time:
- ✅ Pode usar tech nova (tempo para aprender)
- ✅ Budget permite paid APIs (OpenAI, Stripe, etc)
- ✅ Pode construir features complexas
- Timeline: 3-4 semanas (foco total)
```

**Personalize recomendações:**

```markdown
🚀 RECOMENDAÇÕES (para seu perfil):

**Como iniciante:**
1. Comece com boilerplate (Next.js + Supabase starter)
2. Use componentes prontos (shadcn/ui)
3. Evite features complexas no MVP

**Como experiente:**
1. Foque na diferenciação técnica (seu diferencial)
2. Invista em UX polish (users notam)
3. Setup analytics desde dia 1
```

---

## Problema 4: Ignora contexto de mercado atual (trends)

### Sintoma
A validação não considera trends atuais que afetam a ideia (AI boom, mudanças de plataforma, etc).

### Causa
- Não usar WebSearch para trends recentes
- Não considerar timing de mercado
- Análise estática (ignora momento)

### Solução

**Sempre considere timing:**

```markdown
## Timing de Mercado

**Perguntas:**
1. Esta ideia é mais viável hoje do que 1 ano atrás? Por quê?
2. Há alguma mudança recente que cria oportunidade?
3. Há alguma mudança que pode matar a ideia?
```

**Exemplos de timing impactando validação:**

**Ideia: "AI writing assistant for blogs"**

**2023:** ✅ BUILD IT (GPT-3 novo, pouca competição)
**2025:** ❌ SKIP IT (saturado - Jasper, Copy.ai, 100+ tools)

**Ideia: "Twitter analytics for creators"**

**2022:** ✅ BUILD IT (mercado crescendo)
**2024:** ⚠️ CUIDADO (Twitter/X API mudou, pricing subiu, incerteza de plataforma)

**Use WebSearch para trends:**

```bash
# Queries para timing:
1. "[ideia] 2025" (ver lançamentos recentes)
2. "[categoria] market trends 2025"
3. "[competidor principal] news" (se tá morrendo ou crescendo)
4. "alternative to [competidor]" (se pessoas estão migrando)
```

**Adicione seção de timing no output:**

```markdown
⏰ MARKET TIMING

**Momento atual:** [GOOD | NEUTRAL | BAD]

**Por que agora:**
- [Mudanças que criam oportunidade]
- [Tecnologias que se tornaram acessíveis]
- [Gaps que surgiram recentemente]

**Riscos de timing:**
- [Mudanças que podem afetar negativamente]
- [Competição que está surgindo]
```

---

## Problema 5: Não sugere pivots concretos quando ideia é fraca

### Sintoma
Quando ideia é ruim, a análise apenas diz "SKIP IT" sem ajudar o usuário a salvar a direção.

### Causa
- Foco só em validar, não em melhorar
- Não explorando "núcleo bom" da ideia
- Não sugerindo alternativas

### Solução

**Toda ideia ruim tem um "núcleo aproveitável":**

**Processo de pivot:**

1. **Identifique o núcleo:**
   - O que há de interessante na ideia original?
   - Qual problema real está tentando resolver?
   - Qual parte da solução é única?

2. **Reduza o escopo:**
   - Se é muito genérico, especialize em nicho
   - Se é muito complexo, simplifique para MVP
   - Se competição é alta, foque em sub-mercado

3. **Sugira 2-3 pivots concretos:**
   - Específicos (não vagos)
   - Com reasoning claro
   - Viáveis em 2-4 semanas

**Template de pivot:**

```markdown
🚫 NÃO CONSTRUA ISSO. MAS AQUI ESTÃO PIVOTS VIÁVEIS:

### Núcleo aproveitável da ideia original:
[O que é interessante apesar dos problemas]

### Pivot 1: [Nome específico]
**Conceito:** [1-2 linhas]
**Por que é melhor:**
- Nicho específico: [tamanho]
- Resolve dor real: [qual]
- Sem competitor direto
- Timeline: [X semanas]
- Monetização: [modelo + estimativa]

### Pivot 2: [Nome específico]
[Mesma estrutura]

### Pivot 3: [Nome específico]
[Mesma estrutura]

**Recomendação:** [Qual dos 3 começar e por quê]
```

**Exemplo prático:**

**Ideia original (ruim):** "Alternativa ao Notion com AI"

**Pivots concretos:**
1. **"Notion AI Workflows Marketplace"** - Complementa em vez de competir
2. **"Notion to Obsidian Migrator"** - Serve quem já decidiu trocar
3. **"Notion API Monitor"** - Tool para devs usando Notion API

Todos são:
- ✅ Relacionados à ideia original
- ✅ Muito mais viáveis
- ✅ Sem competição direta
- ✅ Construíveis em semanas

---

## Recursos para Melhor Validação

### Ferramentas de Research

1. **WebSearch queries efetivas:**
   - `"[idea] pricing 2025"`
   - `"[idea] market size"`
   - `"best [category] tools"`
   - `"[idea] vs [competitor]"`
   - `"[problem] solution reddit"`

2. **Fontes confiáveis:**
   - IndieHackers.com (revenue real de indies)
   - MicroConf.com (talks sobre validation)
   - Hacker News "Show HN" (feedback honesto)
   - Reddit r/SaaS, r/startups

3. **Data sources:**
   - Google Trends (demanda ao longo do tempo)
   - Product Hunt (lançamentos recentes)
   - BuiltWith (tech stacks de competidores)
   - SimilarWeb (traffic estimates)

### Templates

**Quick validation checklist:**
```
[ ] Found 3-5 competitors
[ ] Checked their pricing
[ ] Read their reviews (positive + negative)
[ ] Searched Reddit for problem discussions
[ ] Checked Google Trends (growing or declining?)
[ ] Estimated build timeline realistically
[ ] Defined monetization model clearly
[ ] Calculated break-even customer count
```

**One-liner validator:**
Preencha e veja se faz sentido:

```
"[Target customer] will pay $[amount] for [value delivered]
because [existing alternative] doesn't [specific gap]."

Exemplo BOM:
"Tech bloggers will pay $12/month for markdown-to-Twitter converter
because Typefully doesn't support markdown import."

Exemplo RUIM:
"Everyone will pay $5/month for better note-taking
because Notion is expensive."
→ "Everyone" não é target, $5 é barato demais, "better" é vago
```
