# 📚 Knowledge Bases - Índice Completo

**Total:** 3 KBs | **Geradas por:** `rag-novo` skill | **Viram Skills automaticamente**

Após geração com `rag-novo`, livros/documentos viram **Claude Skills consultáveis**.

---

## 📖 KBs Disponíveis

| KB | Fonte | Chunks | Tipo | Skill Path |
|----|-------|--------|------|------------|
| **100m-offers** | $100M Offers Complete (Alex Hormozi) | 25 chunks | business_book | `.claude/skills/books/100m-offers/` |
| **100m-leads** | $100M Leads (Alex Hormozi) | 24 chunks | business_book | `.claude/skills/books/100m-leads/` |
| **100m-money-models** | $100M Money Models (Alex Hormozi) | ~20 chunks | business_book | `.claude/skills/books/100m-money-models/` |

---

## 📋 Descrição das KBs

### 100m-offers

**Fonte:** $100M Offers Complete (Alex Hormozi)
**Estrutura:** 21 capítulos + front/back matter
**Inclui:** Lost Chapter (Cap. 17-21: Your First Avatar - Vista Equity methodology)

**Tópicos principais:**
- Value Equation
- Grand Slam Offer
- Pricing strategies
- Stack methodology
- Guarantees
- Scarcity & Urgency
- Bonuses

**Como usar:**
```bash
# Buscar keyword
Grep pattern="value equation" path=".claude/skills/books/100m-offers/chunks"

# Ler índice
Read file_path=".claude/skills/books/100m-offers/index.md"

# Ler chunk específico
Read file_path=".claude/skills/books/100m-offers/chunks/section_XXX.md"
```

---

### 100m-leads

**Fonte:** $100M Leads (Alex Hormozi)
**Estrutura:** 5 seções (Start Here, Get Understanding, Get Leads, Get Lead Getters, Get Started)
**Metodologias:** Core Four + Lead Getters

**Tópicos principais:**
- Core Four (Warm Outreach, Cold Outreach, Paid Ads, Content)
- Lead Getters (Customers, Employees, Agencies, Affiliates)
- Hook-Retain-Reward framework
- Headlines & Curiosidade
- Lead Magnets
- Advertising strategies

**Como usar:**
```bash
# Buscar keyword
Grep pattern="core four" path=".claude/skills/books/100m-leads/chunks"

# Ler índice
Read file_path=".claude/skills/books/100m-leads/index.md"

# Ler chunk específico
Read file_path=".claude/skills/books/100m-leads/chunks/section_XXX.md"
```

**Skill relacionada:** `hormozi-leads` (auto-invoca quando pedir hook/headline/CTA)

---

### 100m-money-models

**Fonte:** $100M Money Models (Alex Hormozi)
**Estrutura:** ~20 chunks semânticos
**Metodologias:** Modelos de negócio e monetização

**Tópicos principais:**
- SaaS models
- Info Products
- Lead Generation
- Agency models
- Recurring revenue
- Lifetime value (LTV)
- Customer acquisition cost (CAC)

**Como usar:**
```bash
# Buscar keyword
Grep pattern="saas" path=".claude/skills/books/100m-money-models/chunks"

# Ler índice
Read file_path=".claude/skills/books/100m-money-models/index.md"

# Ler chunk específico
Read file_path=".claude/skills/books/100m-money-models/chunks/section_XXX.md"
```

---

## 🎯 Como Consultar KB (via Skill)

### Método 1: Buscar keyword

```bash
Grep pattern="keyword" path=".claude/skills/books/[nome-kb]/chunks"
```

**Exemplo:**
```bash
Grep pattern="value equation" path=".claude/skills/books/100m-offers/chunks"
```

### Método 2: Ler índice completo

```bash
Read file_path=".claude/skills/books/[nome-kb]/index.md"
```

**Exemplo:**
```bash
Read file_path=".claude/skills/books/100m-leads/index.md"
```

### Método 3: Ler chunk específico

```bash
Read file_path=".claude/skills/books/[nome-kb]/chunks/section_XXX.md"
```

**Exemplo:**
```bash
Read file_path=".claude/skills/books/100m-offers/chunks/section_005.md"
```

---

## 🔧 Criar Nova KB

**Comando:**
```
Cria uma KB de [livro/documento]
```

**Processo (automático via `rag-novo` skill):**

1. **Análise semântica** (Fase 1)
   - Identifica hierarquia lógica (capítulos, seções)
   - Define chunks semânticos (<5k tokens)
   - Preserva contexto e transições

2. **Geração KB** (Fase 2)
   - Cria estrutura de arquivos
   - Gera index.md com mapa completo
   - Cria chunks numerados
   - Auto token estimation

3. **Ativação automática**
   - Symlink criado em `.claude/skills/books/[nome-kb]/`
   - KB disponível como skill imediatamente
   - Claude descobre e usa automaticamente

**Estrutura gerada:**
```
livros/kb/[nome-kb]/               # Armazenamento físico
├── index.md                       # Mapa completo da KB
├── chunks/
│   ├── section_001.md
│   ├── section_002.md
│   └── ...
└── metadata.json                  # Info técnica

.claude/skills/books/[nome-kb]/    # Symlink (auto-descoberta)
└── → livros/kb/[nome-kb]/
```

---

## 📊 Estatísticas

- **Total KBs:** 3
- **Total chunks:** ~69 chunks
- **Tokens médios por chunk:** 3500-4500
- **Tipos:** business_book (3)
- **Auto-descoberta:** ✅ (via symlink)
- **Line number precision:** ✅
- **Token estimation:** ✅ (automático)

---

## 🧠 Skills Relacionadas

| Skill | Usa KB | Descrição |
|-------|--------|-----------|
| **100m-leads** | 100m-leads | Consulta automática frameworks de geração de leads |
| **100m-offers** | 100m-offers | Consulta automática frameworks de criação de ofertas |
| **100m-money-models** | 100m-money-models | Consulta automática modelos de monetização |
| **hormozi-leads** | 100m-leads | Auto-invoca ao pedir hook/headline/CTA. Usa KB 100m-leads. |
| **rag-novo** | - | Cria novas KBs (2 fases: análise → geração) |

---

## 🎯 Quando Usar KB vs Skill

### Usar KB diretamente:
- ✅ Consulta rápida de conceito específico
- ✅ Pesquisa exploratória (Grep por keyword)
- ✅ Ler capítulo/seção completa
- ✅ Desenvolvimento de conteúdo técnico

### Usar Skill:
- ✅ Aplicar metodologia em contexto (ex: criar hook)
- ✅ Gerar conteúdo baseado em frameworks
- ✅ Workflow completo (ex: hormozi-leads)
- ✅ Consulta guiada (Skill decide o que ler)

**Exemplo:**

```
❌ Errado: "Leia o capítulo sobre Value Equation"
✅ Correto (KB): Grep pattern="value equation" + Read chunk específico

❌ Errado: "Cria um hook usando 100m-leads"
✅ Correto (Skill): Invocar hormozi-leads (skill usa KB automaticamente)
```

---

## 📁 Localização Física

```
ClaudeCode-Workspace/
├── livros/kb/                     # Armazenamento
│   ├── 100m-offers/
│   ├── 100m-leads/
│   └── 100m-money-models/
│
└── .claude/skills/books/          # Auto-descoberta (symlinks)
    ├── 100m-offers/ → livros/kb/100m-offers/
    ├── 100m-leads/ → livros/kb/100m-leads/
    └── 100m-money-models/ → livros/kb/100m-money-models/
```

**⚠️ Sempre consultar via:** `.claude/skills/books/[nome-kb]/`

---

**Última atualização:** 2025-11-05
**Versão:** 1.0 (3 KBs)
