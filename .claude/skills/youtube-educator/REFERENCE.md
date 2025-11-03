# YouTube Educator - Referência Técnica Completa

## Arquitetura do Sistema

### Fluxo de Dados
```
INPUT: "Cria vídeo sobre [tema]"
    ↓
┌─────────────────────────────────────┐
│ ETAPA 1: Extração de Conteúdo      │
│ - xAI Search (web atual)            │
│ - YouTube (transcrições)            │
│ - Twitter/X (threads)               │
└────────────┬────────────────────────┘
             ↓ [Texto consolidado]
┌─────────────────────────────────────┐
│ ETAPA 2: Roteiro Didático           │
│ Claude Code LLM analisa e estrutura │
│ Formato: visual-explainer compatible│
└────────────┬────────────────────────┘
             ↓ [roteiro_tema.md]
┌─────────────────────────────────────┐
│ ETAPA 3: Apresentação HTML          │
│ Chama: visual-explainer skill       │
│ Output: apresentacao_tema.html      │
└────────────┬────────────────────────┘
             ↓ [Usuário grava]
┌─────────────────────────────────────┐
│ ETAPA 5: Metadados (Hormozi)        │
│ Chama: hormozi-leads skill          │
│ Output: 6-8 headlines + descrição   │
└────────────┬────────────────────────┘
             ↓ [Usuário escolhe headline]
┌─────────────────────────────────────┐
│ ETAPA 6: Thumbnails                 │
│ Chama: thumbnail-creator            │
│ Output: 4 thumbnails (estilos)      │
└────────────┬────────────────────────┘
             ↓ [Usuário escolhe thumbnail]
┌─────────────────────────────────────┐
│ ETAPA 7: Nota Obsidian              │
│ Rastreamento completo da produção   │
└─────────────────────────────────────┘
```

---

## Formato do Roteiro Didático

### Estrutura Markdown (Compatible com visual-explainer)

```markdown
# [Título do Vídeo]

## Slide 1: [Título do Slide]

**Conceito:** [Definição em 1-2 linhas]

**Analogia:** [Comparação do dia a dia]

**Como funciona na prática:**
- Ponto 1
- Ponto 2
- Ponto 3

**Exemplo:** [Caso concreto]

**Notas:** [Dicas para o apresentador durante gravação]

## Slide 2: [Título do Slide]
[... mesmo formato ...]
```

### Princípios de Design do Roteiro

**1. Linguagem Clara**
- Profissional mas acessível
- Analogias do cotidiano
- Sem jargão desnecessário

**2. Estrutura Progressiva**
- Conceito → Analogia → Prática → Exemplo
- Cada slide construi no anterior
- Transições naturais

**3. Conteúdo Interativo**
- Cards clicáveis para conceitos técnicos
- Fluxos visuais para processos
- Quizzes para fixação

**4. Slides Obrigatórios**
- 6-8 slides de conteúdo
- Slide de Resumo (penúltimo)
- Slide de CTA (último)

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

## Nota Obsidian (ETAPA 7)

### Estrutura Completa

**Pasta:** `09 - YouTube Production/`
**Nome:** `[YYYY-MM-DD] - [Título do Vídeo].md`

```markdown
---
tipo: video-producao
status: roteiro-criado
data: 2025-11-03
titulo: "[Título do Vídeo]"
headline: "[Headline escolhida]"
thumbnail: "[thumbnail_tema_estilo.jpg]"
---

# [Título do Vídeo]

## 📊 Metadados

**Status:** Roteiro criado ⏳
**Data:** 2025-11-03
**Duração estimada:** X minutos
**Avatar:** [Público-alvo]

**Arquivos:**
- Roteiro: `roteiro_[tema].md`
- Apresentação: `apresentacao_[tema].html`
- Thumbnail: `output/thumbnails/thumbnail_[tema]_[estilo].jpg`

## 📝 Fontes de Conteúdo

**xAI Search:**
- [URLs pesquisadas]

**YouTube:**
- [Vídeos transcritos]

**Twitter/X:**
- [Threads analisadas]

## 🎯 Headlines Geradas (Hormozi)

1. [Headline 1 - Curiosidade]
2. [Headline 2 - Urgência]
3. [Headline 3 - Prova Social]
4. [Headline 4 - Transformação]
5. [Headline 5 - Contrarian]
6. [Headline 6 - Clareza]
7. [Headline 7 - Impacto]
8. [Headline 8 - Prático]

**✅ Escolhida:** [Headline X]

## 🎨 Thumbnails Geradas

- ✅ thumbnail_[tema]_mr-beast.jpg
- ✅ thumbnail_[tema]_tech-minimal.jpg
- ✅ thumbnail_[tema]_high-contrast.jpg
- ✅ thumbnail_[tema]_split-screen.jpg

**✅ Escolhida:** [Estilo X]

## 📝 Roteiro Completo

[Roteiro estruturado copiado aqui]

## ✅ Checklist de Produção

- [x] Extração de conteúdo
- [x] Roteiro criado
- [x] Apresentação gerada
- [ ] Vídeo gravado
- [ ] Vídeo editado
- [x] Headlines geradas
- [x] Thumbnails criadas
- [ ] Metadados finalizados
- [ ] Upload YouTube
- [ ] Publicado

## 📈 Performance (Pós-Publicação)

**YouTube Analytics:**
- Views: [Adicionar após 48h]
- CTR: [%]
- AVD: [%]
- Comentários: [Número]

## 🔗 Links

- **YouTube:** [URL após upload]
- **Instagram Teaser:** [URL]
- **Twitter Thread:** [URL]
```

---

## Skills Integradas

### 1. visual-explainer

**Quando:** ETAPA 3 (Apresentação HTML)

**Input:** `roteiro_[tema].md`

**Output:** `apresentacao_[tema].html`

**Características:**
- Template notion-interativo.html
- Dark mode
- Cards clicáveis
- Fluxos visuais
- Quizzes
- Resumo (3 colunas)
- CTA (@eusoupromptus)

**Doc:** `.claude/skills/visual-explainer/SKILL.md`

---

### 2. hormozi-leads

**Quando:** ETAPA 5 (Metadados)

**Input:**
- Assunto do vídeo
- Avatar (público-alvo)
- Objetivo/transformação

**Output:**
- 6-8 Headlines virais
- Descrição YouTube completa
- Timestamps sugeridos
- CTAs persuasivos

**Frameworks aplicados:**
- Curiosidade
- Urgência
- Prova social
- Transformação
- Contrarian
- Clareza/Simplicidade
- Impacto
- Prático

**Doc:** `.claude/skills/hormozi-leads/SKILL.md`

---

### 3. thumbnail-creator

**Quando:** ETAPA 6 (Thumbnails)

**Input:** Headline escolhida

**Output:** 4 thumbnails (JPEG 16:9)

**Estilos:**
1. **MrBeast Style**
   - Fundo vermelho/amarelo vibrante
   - Expressão surpresa
   - Setas e círculos
   - Energia máxima

2. **Tech Minimal**
   - Gradiente azul/roxo escuro
   - Visual profissional
   - Ícones tech sutis
   - Futurista clean

3. **High Contrast**
   - Fundo preto sólido
   - Texto neon (amarelo/verde)
   - Efeito glitch
   - Cyberpunk

4. **Split Screen**
   - Dividido verticalmente
   - Você + visual relacionado
   - Texto centralizado
   - Dinâmico balanceado

**Doc:** `scripts/thumbnail-creation/README.md`

---

## Performance e Custos

### FASE 1 (Pré-Gravação)

| Etapa | Ferramenta | Custo | Tempo |
|-------|------------|-------|-------|
| Extração (xAI) | Grok | ~$0.10 | 30s |
| Extração (YouTube) | Whisper | ~$0.06 | 2min |
| Extração (Twitter) | Apify | ~$0.15 | 1min |
| Roteiro | Claude Code | Grátis | 2min |
| Apresentação | visual-explainer | Grátis | 30s |
| Headlines | hormozi-leads | Grátis | 1min |
| Thumbnails (4) | Nano Banana Edit | ~$0.20 | 3min |
| Nota Obsidian | Python script | Grátis | 5s |

**Total:** ~$0.51 por vídeo
**Tempo:** ~10 minutos (automático)

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
├── scripts/youtube-workflow/
│   ├── extract_content.py       # Orquestrador de extração
│   ├── generate_obsidian_note.py # Cria nota rastreamento
│   └── README.md
│
├── roteiro_[tema].md            # Roteiros gerados
├── apresentacao_[tema].html     # Apresentações geradas
│
└── output/thumbnails/           # Thumbnails gerados
    ├── thumbnail_[tema]_mr-beast.jpg
    ├── thumbnail_[tema]_tech-minimal.jpg
    ├── thumbnail_[tema]_high-contrast.jpg
    └── thumbnail_[tema]_split-screen.jpg
```

---

## Decisões de Arquitetura

### Por que Claude Code LLM gera roteiro (não script)?

**Razão:** Análise contextual e estruturação criativa.

Claude Code:
- Entende nuances do conteúdo extraído
- Cria analogias relevantes
- Estrutura didaticamente
- Adapta tom e complexidade
- Mantém coerência narrativa

**Impossível** fazer isso com script Python simples.

---

### Por que 3 fontes de extração?

**xAI Search:** Contexto atual + documentação oficial
**YouTube:** Explicações de especialistas (visual/verbal)
**Twitter/X:** Discussões práticas + casos de uso

**Resultado:** Conteúdo rico e multifacetado.

---

### Por que Obsidian para rastreamento?

- Sistema PKM existente
- Linking entre notas
- Versionamento (git)
- Markdown nativo
- Busca poderosa
- Offline-first

---

**Última atualização:** 2025-11-03
**Versão:** 1.0 (FASE 1)
