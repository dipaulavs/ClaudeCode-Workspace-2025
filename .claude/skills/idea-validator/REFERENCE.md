# Idea Validator - Documentação Técnica

## Framework de Avaliação Completo

### 1. Market Saturation (Saturação de Mercado)

**Objetivo:** Determinar se o mercado está saturado demais para entrar.

**Processo de pesquisa:**

1. **Buscar competidores diretos:**
   ```
   Use WebSearch para:
   - "[ideia] app"
   - "[ideia] software"
   - "[ideia] tool"
   - "[ideia] alternative"
   ```

2. **Analisar cada competidor:**
   - Nome e URL
   - Tamanho (usuários, funding, tempo no mercado)
   - Forças principais
   - Barreiras de entrada que criam

3. **Classificar saturação:**
   - **LOW:** 0-2 competidores, nicho inexplorado
   - **MEDIUM:** 3-5 competidores, espaço para diferenciação
   - **HIGH:** 6+ competidores estabelecidos, difícil competir

**Sinais de saturação problemática:**
- Múltiplos players com funding milionário
- Gigantes tech (Google, Meta, Microsoft) no espaço
- Commoditização completa (preço único fator)

### 2. Differentiation (Diferenciação)

**Objetivo:** Identificar o que torna a ideia única (ou admitir que não é).

**Perguntas-chave:**
- O que esta solução faz que outras não fazem?
- Qual problema ela resolve melhor?
- Por que usuários trocariam de solução atual?

**Tipos de diferenciação válida:**
- **Funcional:** Recurso único que resolve problema real
- **Experiência:** UX drasticamente melhor
- **Nicho:** Foco em segmento ignorado pelos competidores
- **Preço:** Significativamente mais barato (com modelo sustentável)
- **Integração:** Funciona nativamente com tools populares

**Diferenciação fraca (red flags):**
- "É como X mas com Y" (Y sendo feature trivial)
- "Mesma coisa mas design bonito"
- "Versão mais simples" (sem razão clara)

**Seja honesto:**
Se não há diferenciação real, diga claramente. Melhor saber agora.

### 3. Real Demand (Demanda Real)

**Objetivo:** Separar problemas reais de "nice to have" imaginários.

**Sinais de demanda REAL (positivos):**

1. **Pessoas pagam por soluções similares:**
   - Busque preços de competidores
   - Procure reviews mencionando preço ("worth it")
   - Planos pagos visíveis e ativos

2. **Buscas ativas pelo problema:**
   - Use Google Trends
   - Veja volume de "how to [problema]"
   - Fóruns/Reddit com threads ativas

3. **Dor expressa publicamente:**
   - Tweets reclamando
   - Issues em GitHub de projetos existentes
   - Reviews negativas de competidores citando falhas

4. **Workarounds complexos:**
   - Tutoriais longos de "como fazer X"
   - Uso de múltiplas ferramentas combinadas
   - Scripts/plugins criados pela comunidade

**Red flags (demanda fraca):**

1. **"Wouldn't it be cool if...":**
   - Ideia legal mas ninguém pagaria
   - Não resolve dor urgente

2. **Problema que "deveria" existir:**
   - Lógica faz sentido mas mercado não confirma
   - Zero evidência de pessoas buscando solução

3. **Feature, não produto:**
   - Resolve problema muito pequeno
   - Competidores poderiam adicionar em 1 sprint

4. **Solução buscando problema:**
   - Tecnologia legal sem uso claro
   - "X mas com blockchain/AI" sem motivo

**Pesquisa estruturada:**
```
1. Google Trends: "[problema]" últimos 5 anos
2. Reddit: buscar "[problema]" em r/productivity, r/business
3. Twitter/X: "[problema] solution" últimos 30 dias
4. Product Hunt: competitors + reviews
5. Alternativeto.com: buscar categoria
```

### 4. Solo Builder Feasibility (Viabilidade para Builder Solo)

**Objetivo:** Estimar se 1 pessoa pode construir em 2-4 semanas.

**Fatores de complexidade:**

**Baixa complexidade (2-3 semanas):**
- CRUD simples + autenticação
- 1-2 integrações API bem documentadas
- UI com componentes prontos (shadcn, Tailwind)
- Deploy em plataforma managed (Vercel, Supabase)

**Média complexidade (3-5 semanas):**
- Lógica de negócio moderada
- 3-5 integrações API
- Processamento de dados em background
- Webhooks simples

**Alta complexidade (6+ semanas - UNREALISTIC):**
- Real-time collaboration
- Machine learning/AI customizado
- Processamento de mídia pesado (vídeo, áudio)
- Infraestrutura complexa (WebRTC, WebSockets em escala)
- Múltiplas plataformas (web + mobile + desktop)

**Perguntas-chave:**
1. Qual é o MVP mínimo viável? (ignore 80% das features)
2. As APIs necessárias têm docs boas?
3. Já existe boilerplate para tech stack escolhido?
4. Precisa de infra complexa ou pode usar managed services?

**Timeline realista:**
- Semana 1: Setup + autenticação + UI base
- Semana 2: Feature principal funcionando
- Semana 3: Integrações + polish
- Semana 4: Testes + deploy + beta

**Red flags de unrealistic:**
- "E também vai ter..." (lista de 10+ features)
- Tecnologia que nunca usou antes
- "Só precisa de um modelo de ML treinado"
- "Real-time com milhares de usuários simultâneos"

### 5. Monetization Potential (Potencial de Monetização)

**Objetivo:** Definir como a ideia gerará receita sustentável.

**Modelos de receita comuns:**

**1. SaaS Subscription**
- **Melhor para:** Tools de produtividade, automação, analytics
- **Preço típico:** $10-50/mês (indie) | $50-500/mês (B2B)
- **Viabilidade:** Precisa de valor recorrente claro

**2. One-time purchase**
- **Melhor para:** Plugins, templates, boilerplates
- **Preço típico:** $29-199 (único)
- **Viabilidade:** Precisa de marketing constante (sem MRR)

**3. Freemium**
- **Melhor para:** High volume, product-led growth
- **Conversão típica:** 2-5% free → paid
- **Viabilidade:** Precisa escalar MUITO

**4. Usage-based**
- **Melhor para:** APIs, processing, storage
- **Preço típico:** Pay per use com tiers
- **Viabilidade:** Custos variáveis bem definidos

**5. Marketplace commission**
- **Melhor para:** Conectar compradores e vendedores
- **Taxa típica:** 10-30% de transação
- **Viabilidade:** Precisa resolver chicken-egg problem

**Análise de viabilidade:**

**Calcular break-even:**
```
Custos mensais:
- Infra/APIs: $X
- Marketing: $Y
- Tempo (oportunidade): $Z
Total: $T/mês

Break-even = $T / (preço × conversão)
Exemplo: $500 / ($20 × 50%) = 50 usuários pagos
```

**Perguntas críticas:**
1. Quem é o target customer?
   - B2B ou B2C?
   - Empresa (qual tamanho?) ou indivíduo?
   - Qual orçamento disponível?

2. Qual o valor entregue?
   - Economiza tempo: quanto tempo? Qual valor/hora?
   - Gera receita: quanto? Qual % pode cobrar?
   - Evita dor: quão crítico é o problema?

3. Por que pagariam?
   - "Nice to have" = difícil vender
   - "Need to have" = disposto a pagar
   - "Mission critical" = pagam premium

**Red flags de monetização:**
- "Vou descobrir depois"
- Depender de ads (precisa milhões de usuários)
- "Freemium with viral growth" (raramente funciona)
- Preço muito baixo (<$5/mês) para B2C

## Estratégia de Pesquisa

### Ferramentas a usar:

1. **WebSearch:**
   - Competitors research
   - Market size estimates
   - Pricing data
   - User complaints

2. **WebFetch:**
   - Landing pages de competidores
   - Pricing pages detalhadas
   - Documentation de APIs necessárias

3. **Fontes confiáveis:**
   - Product Hunt (lançamentos recentes)
   - Hacker News (discussões de builders)
   - IndieHackers (revenue numbers reais)
   - Reddit r/SaaS, r/startups (feedback honesto)

### Tempo de pesquisa:
- 10-15 minutos de research focused
- Priorize qualidade sobre quantidade
- 3-5 competidores são suficientes

## Filosofia da Skill

### Por que "brutalmente honesto"?

Developers têm tempo limitado. Melhor:
- Matar ideia ruim em 15 minutos
- Do que desperdiçar 4 semanas construindo algo que ninguém quer

### O que NÃO é esta skill:

❌ **NÃO é cheerleader:**
- Não vai dizer "great idea!" automaticamente
- Não vai encorajar se a pesquisa mostra problemas

❌ **NÃO é advisor genérico:**
- Foco específico: solo builders, MVPs rápidos
- Ignora conselhos de "scale to millions"

❌ **NÃO é anti-risk:**
- Risk calculado OK
- Red flags sérios = avisar claramente

### O que É esta skill:

✅ **Research-backed honesty:**
- Usa dados reais do mercado
- Cita competidores específicos

✅ **Actionable feedback:**
- Se ideia é fraca, sugere pivot concreto
- Se é boa, dá próximos passos específicos

✅ **Time-conscious:**
- Foca em MVPs de 2-4 semanas
- Ignora features "phase 2"

## Triggers de Ativação

User diz qualquer variação de:
- "Validate this idea: [X]"
- "Is [X] worth building?"
- "Should I build [X]?"
- "What do you think about [X]?"
- "Help me evaluate [X]"
- "Is there a market for [X]?"

Automaticamente ativa skill e roda framework completo.
