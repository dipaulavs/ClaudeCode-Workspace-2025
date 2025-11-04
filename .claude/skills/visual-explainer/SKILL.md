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
PADRÃO: MotherDuck Style (minimalista, retro-moderno, beige + yellow)
Fallback: Notion Style (se MotherDuck indisponível)
```

**Template MotherDuck:**
- Cores: Beige (#F4EFEA), Yellow (#FFDE00), Dark Gray (#383838)
- Tipografia: Monospace (Aeonik Mono fallback)
- Bordas: 2px solid, sharp edges (border-radius: 0-2px)
- Sombras: Offset solid (4px/8px sem blur) ao hover
- Estilo: Warm, technical, developer-friendly

Ver specs completas dos templates em [REFERENCE.md](REFERENCE.md).

### Etapa 3: Gerar Apresentação HTML 🎨

1. Carregar template MotherDuck (notion-motherduck.html) - PADRÃO
2. Injetar conteúdo estruturado com elementos interativos:
   - Cards clicáveis (para conceitos técnicos)
   - Fluxos visuais com setas (para processos)
   - Quizzes interativos (para fixação)
3. Adicionar slides obrigatórios:
   - Resumo Final (penúltimo slide)
   - CTA/Obrigado (último slide com like + inscrição + Instagram)
4. Configurar features:
   - ✅ Atalhos: ← → (navegar), Espaço (avançar), F (fullscreen), ESC (sair)
   - ✅ Barra de progresso (●●●○○○)
   - ❌ SEM timer (removido)
   - ❌ SEM notas do apresentador (removidas)
   - ❌ SEM animações sequenciais (performance)
   - ❌ SEM botões de navegação visíveis (NUNCA incluir)
   - ✅ Estilo minimalista Obsidian (SEMPRE)
5. **RESPONSIVIDADE (OBRIGATÓRIO):**
   - ✅ TODOS os cards devem ser SEMPRE visíveis
   - ✅ Usar CSS Grid/Flexbox com wrap automático
   - ✅ Breakpoints: mobile (<768px), tablet (768-1024px), desktop (>1024px)
   - ✅ Cards em 1 coluna (mobile), 2 colunas (tablet), 3-4 colunas (desktop)
   - ✅ Scroll vertical se necessário (NUNCA esconder cards)
   - ✅ Testar viewport: min 375px (mobile) até 2560px (ultrawide)
   - ❌ NUNCA usar overflow:hidden que esconda conteúdo
   - ❌ NUNCA fixar altura que corte cards
6. Gerar arquivo `apresentacao_[assunto].html` standalone
7. Abrir automaticamente no navegador

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

## Documentação Adicional

- **Specs técnicas dos 3 templates:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos de apresentações:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Problemas comuns:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (ativação automática)
**Output:** HTML standalone dark mode
**Versão:** 1.0
