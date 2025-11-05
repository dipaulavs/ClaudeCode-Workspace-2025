# YouTube Educator - Referência Técnica Completa

## Arquitetura do Sistema

### Fluxo de Dados
```
INPUT: "Cria vídeo sobre [tema]" ou URL YouTube
    ↓
┌─────────────────────────────────────────────────────┐
│ ETAPA 1: Extração de Conteúdo                      │
│ - Transcrição YouTube (se URL fornecida)           │
│ - OU xAI Search (se tema genérico)                 │
└────────────┬────────────────────────────────────────┘
             ↓ [Transcrição/contexto completo]
┌─────────────────────────────────────────────────────┐
│ FASE 1: Processamento PARALELO (4 agents)          │
│                                                     │
│ Agent 1: Apresentação HTML (visual-explainer)      │
│ • Input: Transcrição completa                      │
│ • Output: apresentacao_[tema].html (Notion style)  │
│ • Salvamento duplo: Downloads + Obsidian           │
│                                                     │
│ Agent 2: Headlines Hormozi                         │
│ • Input: Transcrição completa                      │
│ • Output: 7 headlines + 1 MAIS IMPACTANTE         │
│                                                     │
│ Agent 3: Descrição YouTube                         │
│ • Input: Transcrição completa                      │
│ • Output: descricao_youtube_[tema].md              │
│                                                     │
│ Agent 4: Nota Obsidian (MCP Filesystem)           │
│ • Input: Transcrição completa                      │
│ • Output: Nota em 📺 Vídeos/ (obsidian-organizer) │
│ • Método: Write tool direto (sem REST API)        │
└────────────┬────────────────────────────────────────┘
             ↓ [FASE 1 completa em ~2min]
┌─────────────────────────────────────────────────────┐
│ FASE 2: Thumbnails (após headline escolhida)       │
│                                                     │
│ Agent 5: Thumbnails YouTube (youtube-thumbnailv2)  │
│ • Input: Headline MAIS IMPACTANTE (Agent 2)        │
│ • Output: 5 thumbnails profissionais               │
└────────────┬────────────────────────────────────────┘
             ↓ [Tudo pronto em ~3min]
┌─────────────────────────────────────────────────────┐
│ OUTPUT FINAL: Pronto para Gravação 🎥             │
│ • 1 Apresentação HTML (estilo Notion)              │
│ • 7 Headlines (+ 1 escolhida)                      │
│ • 5 Thumbnails profissionais                       │
│ • Descrição YouTube completa                       │
│ • Nota Obsidian com "cola" de gravação             │
└─────────────────────────────────────────────────────┘
```

---

## Apresentação HTML (visual-explainer)

### Características da Apresentação

**Template:** Notion-style (dark mode)
**Estrutura:** 6-8 slides educativos
**Formato:** HTML standalone (funciona offline)

**Elementos visuais:**
- Cards clicáveis para conceitos
- Transições suaves
- Layout limpo e profissional
- Focado em didática

**Salvamento duplo:**
1. `~/Downloads/apresentacao_[tema].html` (backup rápido)
2. `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_[tema].html` (permanente)

**Uso:** Abrir em navegador → Fullscreen (F) → Gravar tela + áudio

---

## Extração de Conteúdo (ETAPA 1)

### 1. xAI Search (Grok)

**Script:** `scripts/search/xai_web.py`
**Python:** 3.11+ obrigatório

```bash
python3.11 scripts/search/xai_web.py "[tema do vídeo]"
```

**Output:**
- Artigos relevantes
- Documentação oficial
- Insights técnicos atualizados

**Uso:** Contexto geral + definições + estado da arte

---

### 2. YouTube Transcription (Whisper)

**Script:** `scripts/extraction/transcribe_video.py`

```bash
python3 scripts/extraction/transcribe_video.py "[URL do vídeo]"
```

**Output:**
- Transcrição completa
- Timestamps
- Conteúdo estruturado

**Uso:** Aprender de especialistas, pegar explicações claras

---

### 3. Twitter/X Scraping (Apify)

**Script:** `scripts/twitter/search_twitter.py`

```bash
python3 scripts/twitter/search_twitter.py "[hashtag ou keyword]"
```

**Output:**
- Threads relevantes
- Discussões técnicas
- Insights da comunidade

**Uso:** Perspectivas variadas, casos de uso reais

---

## Headlines + Metadados (ETAPA 2) - Metodologia Hormozi Completa

### Integração com hormozi-leads Skill

**Objetivo:** Gerar 15-20 headlines irresistíveis testando TODOS os frameworks do livro "$100M Leads" de Alex Hormozi.

**Skill chamada:** `.claude/skills/hormozi-leads/`

### Processo Obrigatório

#### 1. Coletar Contexto do Vídeo
- **Produto/Oferta:** O que o vídeo ensina (ex: SyncThing - sincronização gratuita)
- **Avatar:** Quem vai assistir (ex: Usuários de iCloud/Drive/Dropbox)
- **Problema:** Dor que resolve (ex: Custos mensais altos, falta de controle)
- **Resultado:** Transformação prometida (ex: Sincronização grátis e autônoma)
- **Plataforma:** YouTube (vídeo educativo)

#### 2. Aplicar 7 Elementos de Hook (Combinar 2-3 por headline)

**Elementos disponíveis** (ver `.claude/skills/hormozi-leads/hooks-biblioteca.md`):

1. **RECENCY** - "Ontem descobri...", "Acabei de testar..."
2. **RELEVANCY** - "Se você [persona específica]...", "Para quem..."
3. **CELEBRITY** - "Como [autoridade] conseguiu...", "Roubei isso de..."
4. **PROXIMITY** - "No seu negócio...", "Na sua cidade..."
5. **CONFLICT** - "Por que [crença] está errada", "[A] vs [B]"
6. **UNUSUAL** - "Eu não faço [ação esperada]...", "Parece loucura mas..."
7. **ONGOING** - "Estou testando agora...", "Dia 7 de 30..."

**Combinações de alto impacto:**
- Recency + Unusual + Relevancy
- Conflict + Celebrity
- Ongoing + Proximity

#### 3. Testar Múltiplos dos 30 Frameworks de Headlines

**Mínimo:** 10 frameworks diferentes
**Recomendado:** 15-20 headlines variadas

**Frameworks principais** (ver `.claude/skills/hormozi-leads/headlines-frameworks.md`):

**Categoria 1: Transformação**
- Framework 1: Antes → Depois
- Framework 2: Número + Resultado
- Framework 3: Tempo Específico

**Categoria 2: Revelação/Segredo**
- Framework 4: Segredo Escondido
- Framework 5: Insight Contrário
- Framework 6: Roubo Autorizado

**Categoria 3: Erros/Avisos**
- Framework 7: Erro Custoso
- Framework 8: Múltiplos Erros
- Framework 9: Alerta Urgente

**Categoria 4: Método/Sistema**
- Framework 10: Sistema Nomeado
- Framework 11: Passo a Passo
- Framework 12: Blueprint

*+ 18 frameworks adicionais em 9 categorias*

#### 4. Fórmula Master para Cada Headline

```
[Número] [Forma/Método] para [Avatar Específico] conseguir
[Resultado Desejado] em [Prazo] sem [Dor/Esforço]
```

**Elementos obrigatórios:**
- ✅ Número específico (dá credibilidade)
- ✅ Promessa clara (o que vai conseguir)
- ✅ Prazo definido (quando vai conseguir)
- ✅ Qualificação (quem é isso para)
- ✅ Remove dor principal (sem [esforço])

#### 5. Output Completo da ETAPA 2

**Headlines:**
- 15-20 opções testando frameworks variados
- Cada uma com 2-3 elementos de hook
- Seguindo estrutura Hook → Retain → Reward

**Descrição YouTube:**
```
[Headline escolhida]

[Resumo do vídeo - 2-3 linhas]

⏱️ TIMESTAMPS:
00:00 - Introdução
02:15 - [Tópico 1]
05:30 - [Tópico 2]
[...]

🔗 LINKS ÚTEIS:
- [Recurso mencionado 1]
- [Recurso mencionado 2]

📢 [CTA - Call to Action]

#Hashtag1 #Hashtag2 #Hashtag3
```

**CTAs em 3 níveis:**
- **Soft:** "Salve para não esquecer" / "Compartilhe com quem precisa"
- **Médio:** "Comente 'QUERO' se quer tutorial detalhado" / "Inscreva-se"
- **Alto:** "Link na descrição - implemente hoje" / "Baixe o guia grátis"

**Hashtags estratégicas:**
- 3-5 hashtags relevantes ao tema
- Mix de volume alto (#YouTube) e específicas (#SyncThing)

#### 6. Checklist de Qualidade (Cada headline deve ter)

✅ Número específico?
✅ Promessa clara e mensurável?
✅ Prazo definido?
✅ Avatar qualificado?
✅ Remove dor principal?
✅ Gera curiosidade?
✅ Eu clicaria?

**7/7 = Headline aprovada**

### Recursos Adicionais da Skill hormozi-leads

Para aprofundar cada elemento:
- **Hooks:** `.claude/skills/hormozi-leads/hooks-biblioteca.md` (50+ hooks validados)
- **Headlines:** `.claude/skills/hormozi-leads/headlines-frameworks.md` (30 frameworks)
- **Retenção:** `.claude/skills/hormozi-leads/retain-formulas.md` (Listas/Steps/Stories)
- **CTAs:** `.claude/skills/hormozi-leads/ctas-persuasivos.md` (30 templates em 5 níveis)
- **Valor:** `.claude/skills/hormozi-leads/equacao-valor.md` (4 elementos de valor)

---

## Nota Obsidian (Agent 4)

### Estrutura via obsidian-organizer

**Criada automaticamente pela skill:** `obsidian-organizer`

**Pasta:** `📺 Vídeos/`
**Nome:** `Vídeo YouTube - [Tema] - [DATA].md`

**Conteúdo:**
```markdown
# Vídeo YouTube - [Tema]

**Data:** DD/MM/YYYY HH:MM
**Link:** [URL original se houver]

## 📊 Status
- [ ] Pendente
- [ ] Em Gravação
- [ ] Gravado
- [ ] Em Edição
- [ ] Finalizado

## 🎬 Assets

**Apresentação:**
- `📺 Vídeos/Apresentações/apresentacao_[tema].html`

**Headlines (7 opções):**
1. [Headline 1]
2. [Headline 2]
...
7. [Headline 7]

**✅ Headline escolhida:** [Headline mais impactante]

**Thumbnails:**
- `~/Downloads/thumbnail_[tema]_var1.png`
- `~/Downloads/thumbnail_[tema]_var2.png`
- `~/Downloads/thumbnail_[tema]_var3.png`
- `~/Downloads/thumbnail_[tema]_var4.png`
- `~/Downloads/thumbnail_[tema]_var5.png`

## 📝 "Cola" de Gravação

[Pontos-chave para narração durante gravação]
[Estrutura didática do conteúdo]
[Conceitos principais + Analogias]

## ✅ Checklist de Produção

- [x] Apresentação criada
- [x] Headlines geradas
- [x] Thumbnails geradas
- [ ] Vídeo gravado
- [ ] Vídeo editado
- [ ] Upload YouTube
- [ ] Publicado

## 📈 Performance (Após Publicação)

**YouTube Analytics:**
- Views: [Adicionar após 48h]
- CTR: [%]
- AVD: [%]
```

---

## Skills Integradas

### 1. visual-explainer (Agent 1)

**Quando:** FASE 1 - Apresentação HTML

**Input:** Transcrição completa do vídeo

**Output:** `apresentacao_[tema].html` (Notion-style)

**Características:**
- Template 1: Notion (dark mode)
- 6-8 slides educativos
- Layout limpo e profissional
- Didático e visual

**Salvamento:**
- `~/Downloads/apresentacao_[tema].html`
- `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_[tema].html`

**Doc:** `.claude/skills/visual-explainer/SKILL.md`

---

### 2. hormozi-leads (Agent 2)

**Quando:** FASE 1 - Headlines + Descrição

**Input:** Transcrição completa do vídeo

**Output:**
- 7 Headlines (frameworks variados)
- 1 Headline MAIS IMPACTANTE (escolhida automaticamente)
- Descrição YouTube completa

**Metodologia:**
- Lê `.claude/skills/hormozi-leads/hooks-biblioteca.md`
- Lê `.claude/skills/hormozi-leads/headlines-frameworks.md`
- Aplica frameworks diferentes em cada headline
- Combina 2-3 elementos de hook por headline

**Doc:** `.claude/skills/hormozi-leads/SKILL.md`

---

### 3. obsidian-organizer (Agent 4)

**Quando:** FASE 1 - Nota de rastreamento

**Input:** Transcrição + Assets gerados

**Output:** Nota em `📺 Vídeos/`

**Método:** MCP filesystem direto (Write tool)
- **Sem REST API:** Obsidian não precisa estar aberto
- **Vault path:** `/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios`
- **Write direto:** Cria arquivo `.md` diretamente no vault

**Estrutura:**
- Status da produção
- Links para apresentação
- Headlines geradas
- "Cola" de gravação
- Checklist de produção

**Doc:** `.claude/skills/obsidian-organizer/SKILL.md`

---

### 4. youtube-thumbnailv2 (Agent 5)

**Quando:** FASE 2 - Thumbnails

**Input:** Headline MAIS IMPACTANTE (do Agent 2)

**Output:** 5 thumbnails profissionais (PNG 1024x576)

**Características:**
- Estilo único: Dourado + Azul-ciano
- Layout fixo: Texto (esquerda) + Foto (direita)
- Split lighting
- 5 variações de texto

**Tempo:** ~90s
**Custo:** ~$0.15

**Doc:** `.claude/skills/youtube-thumbnailv2/SKILL.md`

---

## Performance e Custos

### Workflow Completo

| Etapa | Ferramenta | Custo | Tempo |
|-------|------------|-------|-------|
| Transcrição (YouTube) | Whisper API | ~$0.06 | 2min |
| Agent 1 (Apresentação) | visual-explainer | Grátis | 30s |
| Agent 2 (Headlines) | hormozi-leads | Grátis | 30s |
| Agent 3 (Descrição YT) | Claude Code | Grátis | 30s |
| Agent 4 (Nota Obsidian) | obsidian-organizer | Grátis | 30s |
| Agent 5 (Thumbnails) | youtube-thumbnailv2 | ~$0.15 | 90s |

**Total:** ~$0.21 por vídeo
**Tempo:** ~3 minutos (PARALELO: FASE 1 + FASE 2)

---

## Arquivos e Pastas

```
ClaudeCode-Workspace/
│
├── .claude/skills/youtube-educator/
│   ├── SKILL.md
│   ├── REFERENCE.md
│   ├── EXAMPLES.md
│   └── TROUBLESHOOTING.md
│
├── descricao_youtube_[tema].md  # Descrição YouTube (Agent 3)
│
├── ~/Downloads/
│   ├── apresentacao_[tema].html      # Apresentação (backup rápido)
│   ├── thumbnail_[tema]_var1.png    # Thumbnails (Agent 5)
│   ├── thumbnail_[tema]_var2.png
│   ├── thumbnail_[tema]_var3.png
│   ├── thumbnail_[tema]_var4.png
│   └── thumbnail_[tema]_var5.png
│
└── ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/
    │
    ├── 📺 Vídeos/
    │   ├── Vídeo YouTube - [Tema] - [DATA].md  # Nota (Agent 4 via MCP)
    │   │
    │   └── Apresentações/
    │       └── apresentacao_[tema].html         # Apresentação (permanente)
```

---

## Decisões de Arquitetura

### Por que MCP Filesystem (não REST API)?

**Razão:** Confiabilidade, simplicidade e independência do Obsidian.

**MCP Filesystem (atual):**
- ✅ Write tool cria arquivos `.md` diretamente no vault
- ✅ Obsidian não precisa estar aberto
- ✅ Funciona offline
- ✅ Sem dependências de servidor local
- ✅ Sincronização automática via iCloud
- ✅ Mais confiável (menos pontos de falha)

**REST API Local (antigo - NÃO usado):**
- ❌ Obsidian precisa estar aberto
- ❌ Servidor local precisa estar rodando
- ❌ Plugin REST API precisa estar habilitado
- ❌ Mais pontos de falha
- ❌ Dependência de configuração externa

**Resultado:** MCP filesystem é mais simples, confiável e eficiente.

---

### Por que Agents autônomos (não script único)?

**Razão:** Processamento paralelo e especialização.

Cada agent é especialista em sua tarefa:
- **Agent 1:** visual-explainer entende didática e design
- **Agent 2:** hormozi-leads domina copywriting persuasivo
- **Agent 3:** Claude Code gera metadados SEO-otimizados
- **Agent 4:** obsidian-organizer organiza formato minimalista
- **Agent 5:** youtube-thumbnailv2 cria thumbnails profissionais

**Benefícios:**
- FASE 1 roda em paralelo (~2min total)
- Cada skill evolui independentemente
- Especialização profunda por área

---

### Por que salvamento duplo da apresentação?

**Downloads:** Backup rápido e fácil acesso
**Obsidian:** Organização permanente + versionamento Git

**Resultado:** Segurança + organização PKM.

---

### Por que Obsidian para rastreamento?

- Sistema PKM existente
- Linking entre notas
- Versionamento (git)
- Markdown nativo
- Busca poderosa
- Offline-first
- Skill obsidian-organizer garante formato consistente

---

**Última atualização:** 2025-11-05
**Versão:** 5.1 (1 apresentação HTML | 4 agents FASE 1 MCP filesystem | Thumbnails FASE 2)
