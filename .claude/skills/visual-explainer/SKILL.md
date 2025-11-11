# 🎨 Visual Explainer - Apresentações Interativas para Vídeos Educativos

## Quando Usar

**Ativa automaticamente quando usuário:**
- "Cria apresentação sobre [assunto]"
- "Quero apresentação visual para gravar vídeo de [X]"
- "Preciso slides/apresentação para explicar [Y]"
- "Cria visual interativo sobre [tema]"

**Propósito:** Criar apresentações HTML dark mode para gravação de vídeos educativos.

---

## Workflow Automático (4 Etapas)

### Etapa 1: Analisar Conteúdo 🔍

1. Receber roteiro/assunto do usuário
2. Detectar automaticamente tipo de conteúdo:
   - **Conceito técnico** (arquiteturas, sistemas) → Mapa Mental
   - **Novidade/announcement** (lançamentos, news) → Tech Futurista
   - **Explicação estruturada** (tutoriais, teoria) → Notion Style
3. Identificar elementos principais (tópicos, subtópicos, relações)

### Etapa 2: Escolher Template Automaticamente 🎯

**Lógica de decisão:**
```
PADRÃO: Educativo (reveal progressivo, 7 slides fixos, light mode)
Alternativas:
  - MotherDuck Style (apresentações gerais, retro-moderno)
  - Notion Style (fallback dark mode)
```

**Template Educativo (PADRÃO para vídeos YouTube):**
- Cores: Beige (#F4EFEA), Yellow (#FFDE00), Dark Gray (#383838)
- Tipografia: Monospace (SF Mono, Monaco)
- Animações: Reveal progressivo (clique avança, data-step)
- Estrutura: 7 slides fixos (Capa → Aprender → Conceito → Processo → Exemplos → Resumo → CTA)
- Estilo: Educativo, didático, interativo para gravação
- Localização: `templates/video-educativo/template_video_youtube.html`

**Template MotherDuck (alternativa):**
- Cores: Beige (#F4EFEA), Yellow (#FFDE00), Dark Gray (#383838)
- Tipografia: Monospace (Aeonik Mono fallback)
- Bordas: 2px solid, sharp edges (border-radius: 0-2px)
- Sombras: Offset solid (4px/8px sem blur) ao hover
- Estilo: Warm, technical, developer-friendly

Ver specs completas dos templates em [REFERENCE.md](REFERENCE.md).

### Etapa 3: Gerar Apresentação HTML 🎨

**Carregar template conforme tipo de conteúdo:**

**OPÇÃO A: Template Educativo (PADRÃO - vídeos YouTube):**
1. Ler template base: `Read` tool em `templates/video-educativo/template_video_youtube.html`
2. Estrutura fixa de 7 slides:
   - Slide 1: Capa (título do vídeo)
   - Slide 2: O Que Vai Aprender (5 tópicos progressivos)
   - Slide 3: Conceito Principal (4 cards progressivos)
   - Slide 4: Como Funciona (6 reveals: fluxo + 4 passos + dica)
   - Slide 5: Exemplos Práticos (3 casos progressivos)
   - Slide 6: Resumo (4 reveals: 3 colunas + próximo passo)
   - Slide 7: CTA (3 reveals: like/inscrição + comentário + despedida)
3. Customizar placeholders:
   - `[TÍTULO DO VÍDEO]` → Título fornecido
   - `[Tópico 1]`, `[Conceito A]`, etc → Conteúdo do roteiro
   - Manter estrutura de `data-step` intacta
4. Features incluídas:
   - ✅ Reveal progressivo (clique ou → revela próximo item)
   - ✅ Indicador de progresso "(3/5)" atualiza dinamicamente
   - ✅ Hint "Clique para revelar próximo item"
   - ✅ Navegação: ← → (slides), Clique (reveal), F (fullscreen)
   - ✅ Design MotherDuck light (beige + yellow + dark gray)

**OPÇÃO B: Template MotherDuck (apresentações gerais):**
1. Ler base MotherDuck dark mode (via `Read` tool)
2. Injetar conteúdo com:
   - Cards clicáveis (conceitos técnicos)
   - Fluxos visuais com setas (processos)
   - Quizzes interativos (fixação)
3. Adicionar slides obrigatórios:
   - Resumo Final (penúltimo)
   - CTA/Obrigado (último: like + inscrição + Instagram)

**Configurações comuns (ambos templates):**
- ✅ Atalhos: ← → Espaço F ESC
- ✅ Barra de progresso visual
- ❌ SEM timer, SEM notas visíveis, SEM animações que travam
- ❌ SEM botões de navegação visíveis
- ✅ Estilo minimalista clean
- ✅ 100% responsivo (todos cards visíveis)
- ✅ Standalone (funciona offline)

5. **Salvar HTML:** Usar `Write` tool para salvar em:
   - **Vault Obsidian:** `/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_[assunto].html`
   - **Workspace:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/apresentacao_[assunto].html`
6. Abrir automaticamente no navegador (via `Bash` tool: `open [caminho]`)

### Etapa 4: Confirmar e Orientar 📝

Mostrar ao usuário:
```
✅ Apresentação criada: apresentacao_[assunto].html

📊 Template: Notion Interativo
📍 Total de slides: [N] (incluindo Resumo + CTA)
🎮 Interatividades: Cards clicáveis, Fluxos visuais, Quizzes

🎬 Como usar:
  • Pressione F para fullscreen
  • Setas ← → para navegar
  • Progresso visual no canto superior (●●●○○○)
  • Clique nos cards para expandir detalhes
  • Responda quizzes interativos

Pronto para gravar! 🚀
```

---

## Features Incluídas

### Interatividade:
- **Cards clicáveis** → Expandem para mostrar detalhes + exemplos
- **Fluxos visuais** → Processos com setas e numeração
- **Quizzes** → Perguntas com feedback instantâneo (correto/errado)
- **Hover effects** → Destaque visual ao passar mouse

### Durante Gravação:
- **Progresso visual** → Indicador de slides (●●●○○○) no canto superior
- **Navegação minimalista** → APENAS teclado (setas, espaço, F, ESC) + cliques laterais
- **Sem distrações** → SEM timer, SEM notas visíveis, SEM animações que travam
- **SEM botões visíveis** → Nenhum botão de navegação na tela (estilo Obsidian clean)
- **SEM keyboard hints** → Sem indicações visuais de atalhos no rodapé

### Visual:
- **Dark mode only** → Design profissional noturno
- **Minimalismo Obsidian** → Interface clean, sem poluição visual, zero botões visíveis
- **Responsivo TOTAL (OBRIGATÓRIO)** → 100% dos cards visíveis em QUALQUER resolução
  - Mobile (375px+): 1 coluna
  - Tablet (768px+): 2 colunas
  - Desktop (1024px+): 3-4 colunas
  - CSS Grid com `grid-auto-rows: auto` (NUNCA altura fixa)
  - `flex-wrap: wrap` para layouts flex
  - Scroll vertical permitido (NUNCA `overflow: hidden`)
- **Performance otimizada** → Sem animações sequenciais
- **Standalone** → HTML único (funciona offline)

### Estrutura Padrão:
- **Slides de conteúdo** → Conforme roteiro fornecido
- **Slide de Resumo** → Penúltimo slide (3 colunas: O Que É | Como Funciona | Por Que Usar)
- **Slide de CTA** → Último slide (Like + Inscrição + Instagram @eusoupromptus)

---

## Regras de Ouro

### ✅ SEMPRE FAZER:
- Escolher template automaticamente (baseado no conteúdo)
- Gerar arquivo HTML standalone (funciona offline)
- Abrir apresentação no navegador após criar
- Incluir notas do apresentador
- Modo dark obrigatório
- **Estilo minimalista Obsidian (clean, sem distrações)**
- **Responsividade TOTAL: TODOS os cards SEMPRE visíveis**
- **CSS Grid/Flexbox com wrap automático (nunca altura fixa)**
- **Testar visualmente se nenhum card está cortado/escondido**

### ❌ NUNCA FAZER:
- Perguntar qual template usar (decidir automaticamente)
- Criar apresentação sem notas do apresentador
- Gerar arquivos que dependem de CDN/internet
- Usar light mode
- **NUNCA incluir botões de navegação visíveis (apenas atalhos de teclado + cliques)**
- **NUNCA criar UI poluída (minimalismo é OBRIGATÓRIO)**
- **NUNCA usar `overflow: hidden` que esconda cards**
- **NUNCA fixar altura com `height: XXpx` em containers de cards**
- **NUNCA deixar cards cortados ou fora da tela em qualquer resolução**

---

## 🔧 Ferramentas MCP (OBRIGATÓRIO)

**Skill é 100% MCP filesystem-based:**

### Read Tool
- Carregar templates: `templates/video-educativo/template_video_youtube.html`
- Nunca usar REST API ou scripts externos

### Write Tool
- Salvar HTML em: `/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/📺 Vídeos/Apresentações/`
- Backup workspace: `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/`
- **Obsidian NÃO precisa estar aberto**

### Bash Tool
- Abrir navegador: `open "[caminho-completo-html]"`
- Apenas após salvar com sucesso via Write

**IMPORTANTE:**
- ❌ NUNCA usar Obsidian REST API
- ❌ NUNCA requerer que Obsidian esteja aberto
- ❌ NUNCA usar scripts Python externos (a menos que solicitado)
- ✅ SEMPRE usar Write tool para filesystem direto
- ✅ Funciona mesmo com vault fechado

---

## Documentação Adicional

- **Specs técnicas dos 3 templates:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos de apresentações:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Problemas comuns:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (ativação automática)
**Output:** HTML standalone dark mode
**Método:** MCP filesystem-based (Write tool)
**Versão:** 2.0 (MCP)
