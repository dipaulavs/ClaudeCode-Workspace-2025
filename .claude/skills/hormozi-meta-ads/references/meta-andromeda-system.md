# Meta Andromeda System (2025 Algorithm)

Documentação completa do sistema Andromeda do Meta Ads, extraída de transcrições de especialistas e artigos oficiais da Meta.

---

## O Que É Andromeda?

**Andromeda** é o nome do sistema de Machine Learning do Meta Ads lançado em dezembro de 2024, que mudou completamente a forma como o algoritmo otimiza campanhas.

### Mudança Fundamental:

```
ANTES (2023):
Meta buscava: "1 criativo campeão" que performava bem
Estratégia: Encontrar THE WINNER e escalar ele

DEPOIS (2025 - Andromeda):
Meta busca: "Múltiplos criativos" atingindo diferentes segmentos
Estratégia: Creative Diversity (diversidade de criativos)
```

---

## Por Que a Mudança?

### Problema Anterior:

O algoritmo antigo não conseguia processar eficientemente grandes volumes de criativos diferentes. Quando anunciantes subiam muitos criativos, o algoritmo se confundia e performava mal.

### Solução Andromeda:

Andromeda foi desenvolvido especificamente para:

1. **Processar mais criativos simultaneamente** (50+ por campanha)
2. **Identificar qual criativo funciona para qual segmento** da audiência
3. **Otimizar entrega** mostrando criativo certo → pessoa certa

---

## Creative Diversity (Princípio Central)

### O Que É:

**Creative Diversity** = Ter múltiplos criativos MUITO DIFERENTES entre si, cada um atingindo um segmento/ângulo específico da audiência.

### Exemplo Prático - True Classic (Camisetas):

```
Criativo 1: "Meu marido de 38 anos se veste como universitário"
├── Segmento: Mulheres 35-45 anos
├── Comprando: Para marido/namorado
└── Ângulo: Upgrade de estilo

Criativo 2: "A melhor camiseta para caras grandes"
├── Segmento: Homens acima do peso
├── Comprando: Para si mesmo
└── Ângulo: Conforto + fit

Criativo 3: "Camiseta nº1 para quem malha"
├── Segmento: Homens fitness 25-35 anos
├── Comprando: Para si mesmo
└── Ângulo: Performance + fit muscular

Criativo 4: "Quero agradecer o algoritmo por mostrar isso pro meu marido"
├── Segmento: Mulheres 30-50 anos
├── Comprando: Presente para marido
└── Ângulo: Descoberta algoritmo
```

### Resultado:

Cada criativo atinge **DIFERENTES** partes da audiência broad.

True Classic não precisa segmentar manualmente (idade, gênero, interesse) porque **os criativos fazem a segmentação**.

---

## Targeting: BROAD é o Novo Padrão

### Configuração Recomendada:

```
Targeting: BROAD (sem segmentação detalhada)
Idade: 18-65+
Gênero: Todos
Interesses: Nenhum
Locais: País inteiro (ou múltiplos países)

ÚNICA exclusão: Clientes existentes
```

### Por Quê Broad?

O algoritmo Andromeda **precisa de volume** de dados para identificar padrões.

Quando você restringe muito (ex: Mulheres 25-34, Interesse: Yoga, São Paulo), você:
- ❌ Limita o aprendizado do algoritmo
- ❌ Aumenta CPM (competição maior)
- ❌ Perde segmentos inesperados que convertem

Com Broad + Creative Diversity:
- ✅ Algoritmo testa todos os segmentos
- ✅ Identifica qual criativo → qual segmento
- ✅ Otimiza entrega automaticamente
- ✅ CPM menor (menos competição)

---

## Estrutura de Campanha Andromeda-Optimized

### 2 Campanhas Principais:

```
┌─────────────────────────────────────┐
│  TESTING CAMPAIGN (CBO)             │
│  Budget: 20-40% do total            │
│  Objetivo: Encontrar winners        │
├─────────────────────────────────────┤
│  Ad Set 1: Batch 1 (Ângulo A)       │
│    ├── Criativo 1                   │
│    ├── Criativo 2                   │
│    ├── Criativo 3                   │
│    ├── Criativo 4                   │
│    ├── Criativo 5                   │
│    └── Criativo 6                   │
│                                      │
│  Ad Set 2: Batch 2 (Ângulo B)       │
│    ├── Criativo 1                   │
│    ├── Criativo 2                   │
│    ├── ...                          │
│                                      │
│  Ad Set 3: Batch 3 (Ângulo C)       │
│    └── ...                          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  SCALING CAMPAIGN (Advantage+)      │
│  Budget: 60-80% do total            │
│  Objetivo: Escalar winners          │
├─────────────────────────────────────┤
│  Ad Set: Winners                    │
│    ├── Winner 1 (Batch 1)           │
│    ├── Winner 2 (Batch 2)           │
│    ├── Winner 3 (Batch 1 v2)        │
│    ├── Winner 4 (Batch 3)           │
│    ├── ...                          │
│    └── Winner 50 (máx)              │
└─────────────────────────────────────┘
```

### Detalhes da Testing Campaign:

**Tipo:** CBO (Campaign Budget Optimization)
- Budget no nível da campanha (não ad set)
- Meta distribui budget automaticamente
- Prioriza ad sets com melhor performance

**Bid Strategy:** Highest Volume
- Meta busca máximo de conversões
- Não limitar bid manualmente

**Targeting:** BROAD (excluir apenas clientes)

**Duração de Teste:** 2-3 dias mínimo
- Dia 1: Aprendizado inicial (não julgar)
- Dia 2-3: Dados suficientes para decisão
- Gastar mínimo 5x AOV antes de decidir

**Batches:**
- 1 batch = 4-6 criativos do MESMO ângulo
- Lançar 1-2 batches por semana
- Cada batch = 1 ad set

### Detalhes da Scaling Campaign:

**Tipo:** Advantage+ Sales Campaign
- Tipo de campanha mais otimizado do Meta
- Usa todos os dados disponíveis
- Maximiza conversões

**Budget:** Daily (diário)
- Mais estável que lifetime
- Fácil controlar gasto diário

**Ad Set:** 1 único ad set com TODOS os winners
- Não criar múltiplos ad sets
- Até 50 criativos ativos por ad set
- Meta distribui spend automaticamente

**Targeting:** BROAD (excluir apenas clientes)

**Duplicar AD ID:** SEMPRE preservar engajamento social
- Likes, comments, shares = Social proof
- Aumenta performance do criativo
- Método: Copiar POST ID → duplicar com "Use Existing Post"

---

## Workflow Semanal (Operacional)

### Segunda-feira: Lançar Novo Batch

```
1. Definir ângulo do batch (ex: Prova Social)
2. Criar 4-6 criativos neste ângulo:
   - 2-3 big swings (totalmente novo)
   - 2-3 iterations (variação de winners)
3. Criar Ad Set no Testing Campaign
4. Lançar batch
5. Aguardar 2-3 dias
```

### Terça-Quarta: Monitorar Testing

```
1. Revisar batches ativos (2-3 dias rodando)
2. Identificar early winners:
   ├── CPA ≤ Target CPA
   ├── ROAS ≥ Target ROAS (2.5x+)
   ├── Volume: 10+ conversões
   └── Spend: 5x AOV mínimo
3. Pausar clear losers:
   ├── Spend > 3x AOV, zero vendas
   └── CPA > 2x Target CPA
4. Deixar demais rodando (aguardar mais 1-2 dias)
```

### Quinta-Sexta: Promover Winners

```
1. Identificar winners validados (critérios acima)
2. Para cada winner:
   a. Ir no ad → "View Facebook Post with Comments"
   b. Copiar POST ID da URL
   c. Ir no Scaling Campaign → Ad Set Winners
   d. Criar ad → "Use Existing Post"
   e. Colar POST ID → salvar
3. Limpar Scaling Campaign:
   - Pausar criativos sem spend (última semana)
   - Manter top 30-40 ativos
4. MANTER criativo ativo no Testing também
```

### Sábado-Domingo: Análise & Planejamento

```
1. Revisar métricas gerais:
   ├── ROAS geral da conta
   ├── CPA médio
   ├── LTV por cohort
   └── Spend total vs receita

2. Identificar padrões:
   ├── Quais ângulos funcionam melhor?
   ├── Quais segmentos convertem mais?
   ├── Quais formatos (vídeo/imagem/carrossel)?
   └── Quais hooks geram mais engajamento?

3. Planejar batches da próxima semana:
   ├── 50% big swings (ângulos novos)
   └── 50% iterations (variações de winners)

4. Criar/encomendar criativos para próxima semana
```

---

## Critérios de Decisão (Data-Driven)

### Winner = Promover para Scaling

```
Conversões: ≥ 10 (double digits)
Spend: ≥ 5x AOV
CPA: ≤ Target CPA
ROAS: ≥ Target ROAS (geralmente 2.5x+)
Duração: 2-3 dias consecutivos
Tendência: Estável ou melhorando
```

**Exemplo:**
```
AOV: R$500
Target CPA: R$100
Target ROAS: 2.5x

Criativo X:
├── Conversões: 15 ✅
├── Spend: R$2.800 (5.6x AOV) ✅
├── CPA: R$93 ≤ R$100 ✅
├── ROAS: 2.9x ≥ 2.5x ✅
├── Duração: 3 dias ✅
└── STATUS: WINNER → Promover
```

### Loser = Pausar

```
Spend: > 3-4x AOV
Conversões: 0-2 (muito baixo)
CPA: > 2x Target CPA
ROAS: < 1.0x (prejuízo)
Duração: 3+ dias sem melhora
```

**Exemplo:**
```
AOV: R$500
Target CPA: R$100

Criativo Y:
├── Conversões: 1 ❌
├── Spend: R$1.800 (3.6x AOV) ❌
├── CPA: R$1.800 (18x target!) ❌
├── ROAS: 0.3x ❌
└── STATUS: LOSER → Pausar
```

### Maybe = Aguardar Mais

```
Spend: < 5x AOV (dados insuficientes)
ou
Performance: Entre winner e loser
ou
Tendência: Melhorando gradualmente
```

**Ação:** Aguardar mais 1-2 dias, reavaliar.

---

## Ad Fatigue (Fadiga de Criativo)

### O Que É:

Com o tempo, mesmo criativos winners perdem performance porque a audiência já viu ele muitas vezes.

### Sinais de Ad Fatigue:

```
Performance cai 50%+ (comparado com pico)
Duração: 5+ dias consecutivos de queda
Frequency: > 3.0-4.0 (mesma pessoa viu 3-4x)
CTR: Cai significativamente
CPM: Sobe significativamente
```

### O Que Fazer:

```
1. Pausar criativo fatigado
2. Criar iteration (variação):
   - Trocar hook (primeiros 3s)
   - Trocar thumbnail
   - Trocar copy/headline
   - Manter corpo/mensagem similar
3. Lançar iteration no Testing
4. Se validar → mover para Scaling
```

**Nota:** Iterations funcionam bem porque audiência já conhece mensagem, só precisa de "refresh" visual.

---

## Métricas Essenciais (KPIs)

### Nível de Campanha:

| Métrica | Definição | Target |
|---------|-----------|--------|
| ROAS | Return on Ad Spend (receita/gasto) | 2.5x+ |
| CPA | Cost Per Acquisition (custo/cliente) | ≤ 10% do LTV |
| Spend | Gasto total diário | Conforme budget |
| Revenue | Receita gerada | Spend × ROAS |

### Nível de Criativo:

| Métrica | Definição | Target |
|---------|-----------|--------|
| CTR | Click-Through Rate (cliques/impressões) | 1.5%+ |
| Hook Rate | % que assiste 3+ segundos | 30%+ |
| Retention | % que assiste vídeo completo | 15%+ |
| CPM | Cost Per 1000 Impressions | Quanto menor melhor |
| CPC | Cost Per Click | R$1-5 (varia por nicho) |
| Conversions | Número de vendas | 10+ (para validar) |

### Nível de Negócio:

| Métrica | Definição | Target |
|---------|-----------|--------|
| LTV | Lifetime Value (receita por cliente) | 5-10x CPA |
| CAC | Customer Acquisition Cost | = CPA |
| Payback Period | Tempo para recuperar CAC | ≤ 30 dias |
| MRR | Monthly Recurring Revenue (se subscription) | Crescendo |

---

## Budget Management (Gestão de Budget)

### Budget Split por Estágio:

**Iniciante (testando produto/oferta):**
```
Total: R$500-1000/dia
├── Testing: R$400 (80%)
├── Scaling: R$100 (20%)
└── Remarketing: R$0 (audiência pequena ainda)
```

**Intermediário (winners validados):**
```
Total: R$1000-5000/dia
├── Testing: R$300 (30%)
├── Scaling: R$600 (60%)
└── Remarketing: R$100 (10%)
```

**Avançado (escalando):**
```
Total: R$5000-20000/dia
├── Testing: R$1000 (20%)
├── Scaling: R$3500 (70%)
└── Remarketing: R$500 (10%)
```

### Budget por AOV (Ticket):

```
AOV < R$100:
├── Testing batch: R$100-200/dia por batch
├── Scaling: R$500-2000/dia
└── CPA máx: R$20-30

AOV R$100-300:
├── Testing batch: R$300-500/dia por batch
├── Scaling: R$2000-5000/dia
└── CPA máx: R$50-100

AOV > R$300:
├── Testing batch: R$500-1000/dia por batch
├── Scaling: R$5000-20000/dia
└── CPA máx: R$100-500
```

---

## Case Study Real (Ecommerce - Produto Físico)

**Contexto:**
- Produto: Óculos especiais
- AOV: R$200
- LTV: R$300 (incluindo upsells)
- Target CPA: R$60 (20% do LTV)
- Target ROAS: 2.5x

**Estratégia:**

```
Batch 1: Ângulo "Problema de Visão" (idosos)
├── Criativo 1: "Cansado de não enxergar bem?"
├── Criativo 2: "Ler se tornou difícil?"
├── Criativo 3: "Dor de cabeça ao ler?"
├── Criativo 4: "Vista embaçada?"
└── Targeting: BROAD (sem segmentar idade)

Resultado (3 dias):
├── Criativo 2 → WINNER
│   ├── Conversões: 18
│   ├── CPA: R$55 ✅
│   ├── ROAS: 3.1x ✅
│   └── Segmento: 55-64 e 65+ (descoberto pelo algoritmo!)
│
└── Demais → LOSERS (pausar)
```

```
Batch 2: Ângulo "Benefício" (público geral)
├── Criativo 1: "Enxergue melhor sem óculos de grau"
├── Criativo 2: "Óculos que se ajustam sozinhos"
├── Criativo 3: "Veja de perto e de longe (mesmo óculos)"
└── Criativo 4: "Liberdade sem trocar óculos"

Resultado (3 dias):
├── Criativo 3 → WINNER
│   ├── Conversões: 22
│   ├── CPA: R$58 ✅
│   ├── ROAS: 2.8x ✅
│   └── Segmento: 45-54 (descoberto!)
│
├── Criativo 1 → MAYBE (aguardar)
└── Demais → LOSERS
```

**Scaling Campaign (após 2 semanas):**
```
Winners ativos: 8 criativos
Budget: R$2000/dia (70% do total)
ROAS: 2.9x (média)
CPA: R$57 (média)
Receita: R$5.800/dia
```

**Learning:** Algoritmo Andromeda identificou **demografias específicas** (55-64, 65+, 45-54) através dos criativos, SEM segmentação manual.

---

## Erros Comuns (Evitar)

### 1. Segmentar Demais

❌ **Erro:**
```
Targeting: Mulheres, 25-34, São Paulo
Interesses: Yoga, Meditação, Vida Saudável
```

✅ **Correto:**
```
Targeting: BROAD (todos)
Exclusão: Apenas clientes
Creative Diversity: Criativos fazem segmentação
```

### 2. Pausar Criativos Cedo Demais

❌ **Erro:** Pausar após 1 dia ou R$200 gastos

✅ **Correto:** Aguardar 2-3 dias + 5x AOV gastos

### 3. Buscar "1 Criativo Campeão"

❌ **Erro:** Testar 50 iterações do mesmo criativo

✅ **Correto:** Testar ângulos DIFERENTES (creative diversity)

### 4. Não Duplicar AD ID ao Escalar

❌ **Erro:** Criar ad novo (perde engajamento social)

✅ **Correto:** Duplicar POST ID (mantém likes/comments)

### 5. Budget Muito Baixo

❌ **Erro:** R$50/dia para produto de R$500

✅ **Correto:** Mínimo R$500/dia (1x AOV)

### 6. Não Ter Creative Diversity

❌ **Erro:** 10 criativos similares (mesmo ângulo)

✅ **Correto:** 3+ ângulos diferentes × 4-6 criativos cada

### 7. Mexer Demais nas Campanhas

❌ **Erro:** Mudar budget, pausar/despausar todo dia

✅ **Correto:** Deixar algoritmo aprender (48-72h)

---

## Conclusão: Regras de Ouro Andromeda

1. **BROAD Targeting** (sem segmentação manual)
2. **Creative Diversity** (múltiplos ângulos diferentes)
3. **Paciência** (aguardar 2-3 dias + 5x AOV)
4. **Workflow Semanal** (lançar batches regularmente)
5. **Data-Driven** (decisões baseadas em métricas, não feeling)
6. **Duplicar AD ID** (preservar engajamento social)
7. **50/50 Rule** (50% big swings + 50% iterations)
8. **Scaling Gradual** (não aumentar budget 100%+ de uma vez)
9. **Kill Losers Fast** (não insistir em criativo ruim)
10. **Feed Winners** (continuar criando variações de winners)

---

**Última Atualização:** Janeiro 2025 (baseado em transcrições de especialistas Meta Ads + documentação oficial Meta Engineering)
