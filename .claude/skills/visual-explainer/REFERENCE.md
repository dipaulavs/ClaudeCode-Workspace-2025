# 📚 Visual Explainer - Referência Técnica Completa

## Especificações dos Templates

---

## 🎓 Template: Educativo (PADRÃO para YouTube) - Reveal Progressivo

### Quando Usar
- **PADRÃO para vídeos educativos do YouTube**
- Tutoriais passo a passo
- Explicações didáticas
- Aulas gravadas para screen recording
- Quando precisa controlar o ritmo da revelação (gravação de vídeo)

### Design System
Baseado em MotherDuck Style (light mode, beige + yellow + dark gray)

### Estrutura Visual

```
┌────────────────────────────────────────────────────────┐
│                             Slide 2 de 7      (2/5)    │
├────────────────────────────────────────────────────────┤
│              O QUE VOCÊ VAI APRENDER                   │
├────────────────────────────────────────────────────────┤
│                                                         │
│    ┌───────────────────────────────────────┐           │
│    │ ✅ Tópico 1                            │ ← Step 1 │
│    │ Descrição do tópico                    │           │
│    └───────────────────────────────────────┘           │
│                                                         │
│    ┌───────────────────────────────────────┐           │
│    │ ✅ Tópico 2                            │ ← Step 2 │
│    │ Descrição do tópico                    │           │
│    └───────────────────────────────────────┘           │
│                                                         │
│    (Tópicos 3-5 aparecem progressivamente)             │
│                                                         │
├────────────────────────────────────────────────────────┤
│  Clique ou → para revelar próximo item                 │
└────────────────────────────────────────────────────────┘
```

### Características Técnicas

**Cores (Light Mode - MotherDuck):**
- Background: `#F4EFEA` (beige warm)
- Acento: `#FFDE00` (yellow)
- Texto: `#383838` (dark gray)
- Borders: `2px solid #383838`
- Cards: `#fff` background

**Tipografia:**
- Font: `'SF Mono', 'Monaco', 'Cascadia Code', monospace`
- H1: 48px (títulos principais)
- H2: 38px (títulos de slides)
- H3: 24px (títulos de cards)
- Body: 19px
- Line-height: 1.4

**Animações (Reveal Progressivo):**
- Todos itens iniciam com `opacity: 0` + `transform: translateY(20px)`
- Ao clicar/→: classe `.revealed` adiciona `opacity: 1` + `transform: translateY(0)`
- Transição: `0.4s cubic-bezier(0.4, 0, 0.2, 1)`
- Cada item tem `data-step="N"` para ordem de revelação

**Estrutura de 7 Slides Fixos:**

1. **Capa** (sem reveals)
   - Título do vídeo
   - Subtítulo/frase de impacto
   - Informações básicas

2. **O Que Vai Aprender** (5 steps)
   - 5 tópicos progressivos
   - Cada tópico = 1 step
   - Formato: ✅ Título + descrição

3. **Conceito Principal** (4 steps)
   - 4 conceitos fundamentais
   - Cards com ícones (📌)
   - Explicações claras

4. **Como Funciona** (6 steps)
   - Step 1: Fluxo visual (Passo 1 → Passo 2 → Resultado)
   - Steps 2-5: Cards de etapas (1️⃣ 2️⃣ 3️⃣ 4️⃣)
   - Step 6: Dica final

5. **Exemplos Práticos** (3 steps)
   - 3 casos reais
   - Estrutura: Situação → Solução → Resultado
   - Card por exemplo

6. **Resumo** (4 steps)
   - Steps 1-3: Grid 3 colunas (O Que É | Como Funciona | Por Que Usar)
   - Step 4: Box próximo passo (amarelo)

7. **CTA** (3 steps)
   - Step 1: Grid 3x1 (👍 Like | 🔔 Inscrição | 📱 Instagram)
   - Step 2: Prompt comentário
   - Step 3: Mensagem despedida

**Navegação:**
- `→` ou `Espaço`: Revela próximo item (se houver) OU avança slide
- `←`: Slide anterior
- `F`: Fullscreen
- `ESC`: Sair fullscreen
- Clique lateral esquerdo: Slide anterior
- Clique lateral direito: Revelar próximo OU avançar slide

**Indicadores:**
- Contador no topo direito: "Slide X de 7"
- Progresso de reveals: "(3/5)" durante revelações
- Hint dinâmico: "Clique para revelar próximo item" (some quando slide completo)

**Sistema data-step:**
```html
<!-- Slide com 5 reveals -->
<div class="slide" data-total-steps="5">
    <div class="box reveal-item" data-step="1">Item 1</div>
    <div class="box reveal-item" data-step="2">Item 2</div>
    <div class="box reveal-item" data-step="3">Item 3</div>
    <div class="box reveal-item" data-step="4">Item 4</div>
    <div class="box reveal-item" data-step="5">Item 5</div>
</div>
```

**Localização:**
- Base template: `templates/video-educativo/template_video_youtube.html` (usar `Read` tool)
- Documentação: `templates/video-educativo/README.md`

**Salvamento (MCP Filesystem):**
- Usar `Write` tool (NUNCA REST API)
- Vault path: `/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/`
- Workspace path: `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/`
- Obsidian NÃO precisa estar aberto (MCP filesystem-based)

### Filosofia de Design

1. **Didático:** Informações aparecem conforme você fala (ritmo controlado)
2. **Progressivo:** Viewer não se perde lendo tudo de uma vez
3. **Clean:** Design minimalista, foco no conteúdo
4. **Interativo:** Presenter controla revelação (não automático)
5. **Warm:** Beige + yellow = acessível, não intimidante

---

## 🦆 Template: MotherDuck Style - Retro-Moderno Minimalista

### Quando Usar
- **PADRÃO para todas as apresentações** (a menos que usuário especifique outro)
- Conteúdo técnico/developer-focused
- Explicações estruturadas com estética warm/friendly
- Quando quer visual profissional mas acessível

### Design System Baseado em
Clonado de https://motherduck.com (2025-11-04)

### Estrutura Visual

```
┌────────────────────────────────────────────────────────┐
│                                     ●●●○○○  3/6        │
├────────────────────────────────────────────────────────┤
│              TÍTULO DA SEÇÃO                           │
├────────────────────────────────────────────────────────┤
│                                                         │
│    [BADGE AMARELO] CATEGORIA                            │
│                                                         │
│    | Conceito Principal                                │
│    | (barra amarela lateral)                           │
│                                                         │
│    Explicação clara em fonte Inter, texto preto,       │
│    sobre fundo beige suave. Fácil de ler.              │
│                                                         │
│    ┌───────────────────────────────────────┐           │
│    │ 💡 Analogia                           │           │
│    │ Card branco, borda preta 2px          │           │
│    │ Hover: levanta + sombra offset        │           │
│    └───────────────────────────────────────┘           │
│                                                         │
│    ┌──────────┐  →  ┌──────────┐  →  ┌──────────┐    │
│    │ Passo 1  │      │ Passo 2  │      │ Passo 3  │    │
│    └──────────┘      └──────────┘      └──────────┘    │
│                                                         │
├────────────────────────────────────────────────────────┤
│  ← →  Navegar   | Espaço Próximo  | F Fullscreen      │
└────────────────────────────────────────────────────────┘
```

### Características Técnicas

**Cores:**
- Background principal: `rgb(244, 239, 234)` - Beige warm
- Acento primário: `rgb(255, 222, 0)` - Yellow
- Texto principal: `rgb(56, 56, 56)` - Dark gray
- Texto corpo: `rgb(0, 0, 0)` - Black
- Cards/Containers: `rgb(255, 255, 255)` - White
- Borders: `rgb(56, 56, 56)` - 2px solid

**Tipografia:**
- Headings: `monospace, "Aeonik Mono", sans-serif`
- Body: `Inter, sans-serif`
- Tamanho base: 16px
- H1: 72px (letra-espaçamento 1.44px)
- H2: 32px
- H3: 18px
- Body: 15-16px
- Line-height: 1.6 (body), 1.2 (headings)

**Componentes:**
- **Badges:** Yellow bg, 2px border, uppercase, monospace
- **Cards:** White bg, 2px solid border, border-radius 0px (sharp)
- **Hover:** `translateY(-4px) + box-shadow: 8px 8px 0px solid`
- **Buttons:** Yellow bg, 2px border, hover lift + shadow
- **Inputs:** Semi-transparent white, 2px border, focus = solid white + shadow

**Bordas & Sombras:**
- Border-radius: 0-2px (maximal sharpness)
- Box-shadow ao hover: `8px 8px 0px rgb(56, 56, 56)` (offset solid, sem blur)
- Borders: SEMPRE 2px solid

**Navegação:**
- APENAS teclado (← → Espaço F R)
- APENAS cliques laterais (1/3 esquerdo = prev, 1/3 direito = next)
- SEM botões visíveis (estilo Obsidian minimalista)
- Progresso: Dots no topo direito (●●●○○○) + contador (3/6)

**Interatividade:**
- Cards clicáveis (expandem com clique)
- Quizzes com feedback visual (verde/vermelho)
- Fluxos visuais com setas
- Hover effects com lift + shadow

**Responsividade:**
- Mobile (<768px): 1 coluna, scroll vertical
- Tablet (768-1024px): 2 colunas
- Desktop (>1024px): 3 colunas
- NUNCA esconder cards (sempre visíveis com scroll)

### Filosofia de Design

1. **Warm & Technical:** Beige + monospace = friendly mas profissional
2. **High Contrast:** Dark text em light bg (máxima legibilidade)
3. **Sharp Edges:** Border-radius mínimo (retro-moderno)
4. **Offset Shadows:** Solid shadows (não blur) = distintivo
5. **Yellow Accents:** Usado com parcimônia (CTAs, badges)
6. **Minimalismo:** Zero UI poluída, apenas conteúdo

---

## 1️⃣ Template: Notion Style (Minimalista/Profissional) - FALLBACK

### Quando Usar
- Explicações estruturadas (conceitos + detalhes)
- Tutoriais passo a passo
- Conteúdo com hierarquia clara (tópicos/subtópicos)
- Conteúdo teórico com exemplos

### Estrutura Visual

```
┌────────────────────────────────────────────────────────┐
│  ← Anterior        TÍTULO DA SEÇÃO        Próximo →    │
├────────────────────────────────────────────────────────┤
│                                                         │
│    📌 Conceito Principal                                │
│    ══════════════════════                               │
│                                                         │
│    Explicação ELI5 em 2-3 linhas bem diretas.          │
│    Sem jargões técnicos desnecessários.                 │
│                                                         │
│    ┌──────────────────────────────────────┐            │
│    │  💡 Analogia do Mundo Real           │            │
│    │  Como é similar a [algo familiar]    │            │
│    └──────────────────────────────────────┘            │
│                                                         │
│    ✓ Ponto-chave número 1                              │
│    ✓ Ponto-chave número 2                              │
│    ✓ Ponto-chave número 3                              │
│                                                         │
│    ▼ Clique para ver detalhes técnicos                 │
│                                                         │
├────────────────────────────────────────────────────────┤
│  📝 Notas do Apresentador (visível só para você):      │
│  • Mencionar que X é importante aqui                   │
│  • Dar exemplo de Y antes de avançar                   │
│                                                         │
│                               ⏱️  05:32   ●●●○○○ 3/6   │
└────────────────────────────────────────────────────────┘
```

### Características Técnicas

**Layout:**
- Grid central (max-width: 1200px)
- Padding generoso (3rem)
- Font: Inter ou system-ui
- Tamanho base: 1.2rem (legível em vídeo)

**Cores (Dark Mode):**
- Background: `#0f0f0f`
- Card/Container: `#1a1a1a`
- Texto principal: `#e5e5e5`
- Texto secundário: `#a0a0a0`
- Acento: `#3b82f6` (azul profissional)
- Border: `#2a2a2a`

**Navegação:**
- Botões laterais (← →) sempre visíveis
- Setas do teclado
- Espaço avança
- Indicador de progresso no rodapé

**Seções Expansíveis:**
- Clique para expandir/colapsar
- Ícone muda: ▼ (expandir) / ▲ (colapsar)
- Animação suave (300ms)

---

## 2️⃣ Template: Mapa Mental Interativo (Exploratório)

### Quando Usar
- Arquiteturas de sistemas
- Relações entre conceitos
- Diagramas de componentes
- Fluxos de dados/processos

### Estrutura Visual

```
┌────────────────────────────────────────────────────────┐
│  [Zoom +]  [Zoom -]  [Reset]  [Centralizar]       [?]  │
├────────────────────────────────────────────────────────┤
│                                                         │
│                  ┌─────────────┐                        │
│             ┌────│  Conceito   │────┐                   │
│             │    │  Central    │    │                   │
│             │    └─────────────┘    │                   │
│             ↓                       ↓                   │
│       ┌──────────┐            ┌──────────┐             │
│       │ Ramo 1   │            │ Ramo 2   │             │
│       │  [...]   │            │  [...]   │             │
│       └────┬─────┘            └────┬─────┘             │
│            ↓                       ↓                    │
│       ┌──────────┐            ┌──────────┐             │
│       │Sub-item A│            │Sub-item B│             │
│       └──────────┘            └──────────┘             │
│                                                         │
│     [Clique nos nós para expandir detalhes]            │
│                                                         │
├────────────────────────────────────────────────────────┤
│  📝 Notas: Explicar relação entre Ramo 1 e 2           │
│                                                         │
│                               ⏱️  03:15   ●●○○○○ 2/6   │
└────────────────────────────────────────────────────────┘
```

### Características Técnicas

**Layout:**
- Canvas SVG responsivo
- Centralizado automaticamente
- Zoom: 0.5x a 2.0x
- Pan: Arrastar com mouse/touch

**Nós (Elementos):**
- Formato: Retângulos arredondados (border-radius: 12px)
- Padding: 1rem 1.5rem
- Background: `#1e293b` (nós principais), `#334155` (sub-nós)
- Border: `2px solid #475569`
- Sombra: `0 4px 12px rgba(0,0,0,0.3)`

**Conexões (Setas):**
- Stroke: `#64748b`
- Width: 2px
- Estilo: Sólido para relações diretas, tracejado para indiretas
- Arrow marker: Triângulo preenchido

**Interatividade:**
- Hover: Highlight do nó + conexões relacionadas
- Clique: Modal com detalhes (popup centralizado)
- Expandir/colapsar sub-árvores

**Cores por Tipo:**
- Conceito central: `#3b82f6` (azul)
- Categorias: `#8b5cf6` (roxo)
- Exemplos: `#10b981` (verde)
- Warnings: `#f59e0b` (laranja)

---

## 3️⃣ Template: Tech Futurista (Impact/Announcements)

### Quando Usar
- Lançamentos de tecnologia
- Novidades/breaking news
- Impacto de mudanças
- Comparações antes/depois

### Estrutura Visual

```
┌────────────────────────────────────────────────────────┐
│  ●●○○○○  Slide 2 de 6                            [⚙]  │
├────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│              🚀 GEMINI 2.0 FLASH                        │
│              A Revolução da IA                          │
│                                                         │
│                                                         │
│        ┌────────────────────────────────┐              │
│        │                                │              │
│        │     [Ícone SVG grande]         │              │
│        │     [ou imagem visual]         │              │
│        │                                │              │
│        └────────────────────────────────┘              │
│                                                         │
│                                                         │
│        → Lançado em Dezembro 2024                      │
│        → 2x mais rápido que GPT-4o                     │
│        → Contexto de 2 milhões de tokens               │
│                                                         │
│                                                         │
│                [Space para continuar]                   │
│                                                         │
├────────────────────────────────────────────────────────┤
│  📝 Notas: Enfatizar o contexto massivo aqui           │
│                                                         │
│                               ⏱️  07:45   ●●○○○○ 2/6   │
└────────────────────────────────────────────────────────┘
```

### Características Técnicas

**Layout:**
- Centralizado vertical + horizontal
- Título gigante (3-5rem)
- Muito espaço em branco (breathing room)
- Alinhamento central

**Tipografia:**
- Font: 'Space Grotesk' ou 'JetBrains Mono'
- Título: 3.5rem, weight: 800, letter-spacing: -0.02em
- Subtítulo: 1.8rem, weight: 500, opacity: 0.8
- Bullets: 1.3rem, weight: 400

**Cores (Dark Mode):**
- Background: `#0a0a0a` (quase preto puro)
- Texto principal: `#ffffff`
- Texto secundário: `#a3a3a3`
- Acento primário: `#6366f1` (indigo vibrante)
- Acento secundário: `#8b5cf6` (roxo)
- Gradiente hero: `linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)`

**Animações:**
- Entrada de slide: Fade in + slide up (500ms)
- Transição entre slides: Cross-fade (400ms)
- Bullets: Aparecem sequencialmente (delay: 100ms cada)
- Hover em elementos: Scale 1.02 + glow effect

**Elementos Visuais:**
- Ícones SVG grandes (200-300px)
- Ilustrações minimalistas (line art)
- Glassmorphism nos cards (backdrop-filter: blur)
- Sombras neon sutis em acentos

---

## Recursos Globais (Todos os Templates)

### Modo Apresentador

**Layout Split:**
```
┌─────────────────────────────┬─────────────────────┐
│                             │                     │
│   TELA PRINCIPAL            │   PAINEL CONTROLE   │
│   (aparece no vídeo)        │   (só você vê)      │
│                             │                     │
│   [Slide atual]             │   📝 Notas          │
│                             │   ⏱️  Timer         │
│                             │   ●●●○○○ Progresso │
│                             │   [Preview próximo] │
│                             │                     │
└─────────────────────────────┴─────────────────────┘
```

**Ativação:**
- Tecla `P` → Abre nova janela com painel de controle
- Ou: Modo inline (notas na parte inferior)

### Atalhos de Teclado (Universais)

| Tecla | Ação |
|-------|------|
| `→` ou `Space` | Próximo slide/seção |
| `←` | Slide/seção anterior |
| `F` ou `F11` | Toggle fullscreen |
| `ESC` | Sair fullscreen |
| `P` | Toggle modo apresentador |
| `R` | Reset (volta ao início) |
| `?` | Mostrar ajuda (overlay) |

### Timer

**Posicionamento:** Canto superior direito
**Formato:** `MM:SS` (ex: `05:32`)
**Estilo:**
```css
.timer {
  position: fixed;
  top: 2rem;
  right: 2rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.5rem;
  color: #64748b;
  opacity: 0.6;
  z-index: 1000;
}
```

**Comportamento:**
- Inicia automaticamente ao abrir
- Pode pausar/resetar (tecla `T`)
- Discreto (não distrai)

### Barra de Progresso

**Formato:** `●●●○○○ 3/6`
**Posicionamento:** Canto inferior direito (junto com timer)
**Estilo:**
- Slides passados: `●` (filled, cor acento)
- Slide atual: `●` (filled, cor acento + glow)
- Slides futuros: `○` (outline, opacidade 0.3)

### HTML Standalone

**Requisitos:**
- ✅ Sem dependências externas (CDN)
- ✅ Fonts embeddedas (base64 ou system fallback)
- ✅ CSS inline ou em `<style>` tag
- ✅ JavaScript vanilla (sem frameworks)
- ✅ Funciona offline 100%

**Tamanho target:** < 500KB (incluindo assets)

---

## Estrutura de Dados do Roteiro

**Formato JSON para injetar no template:**

```json
{
  "titulo": "Título da Apresentação",
  "tipo": "notion|mapa-mental|tech-futurista",
  "slides": [
    {
      "id": 1,
      "titulo": "Introdução",
      "conteudo": {
        "conceito": "Texto principal",
        "analogia": "Analogia do mundo real",
        "pontos": ["Ponto 1", "Ponto 2", "Ponto 3"],
        "detalhes": "Conteúdo expansível (opcional)"
      },
      "notas_apresentador": "O que você deve falar aqui",
      "duracao_estimada": 90
    }
  ],
  "metadata": {
    "total_slides": 6,
    "duracao_total": 540,
    "criado_em": "2025-01-03T10:30:00Z"
  }
}
```

---

## Fluxo MCP Filesystem (OBRIGATÓRIO)

**Skill visual-explainer é 100% MCP filesystem-based:**

1. **Ler templates:** Usar `Read` tool
   ```
   Read: templates/video-educativo/template_video_youtube.html
   ```

2. **Processar conteúdo:** Gerar HTML completo em memória

3. **Salvar apresentação:** Usar `Write` tool
   ```
   Write: /Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_[assunto].html
   ```

4. **Abrir navegador:** Usar `Bash` tool
   ```bash
   open "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_[assunto].html"
   ```

**IMPORTANTE:**
- ❌ NUNCA usar REST API do Obsidian
- ❌ NUNCA requerer que Obsidian esteja aberto
- ✅ SEMPRE usar `Write` tool (filesystem direto)
- ✅ Funciona mesmo com Obsidian fechado

---

## Script Gerador (Legado - Opcional)

**Localização:** `scripts/visual-explainer/generate.py`

**Nota:** Skill não precisa do script Python (MCP filesystem faz tudo).
Se preferir usar script standalone:

```bash
python3 scripts/visual-explainer/generate.py \
  --roteiro "caminho/roteiro.md" \
  --output "apresentacao_tema.html" \
  --template auto  # ou: notion, mapa-mental, tech-futurista
```

**Algoritmo de decisão automática:**
```python
def escolher_template(roteiro):
    # Analisa o roteiro
    if "arquitetura" in roteiro or "componentes" in roteiro:
        return "mapa-mental"
    elif "lançamento" in roteiro or "novidade" in roteiro:
        return "tech-futurista"
    else:
        return "notion"  # padrão
```

---

## Configurações Customizáveis

**Arquivo:** `config/visual-explainer.json`

```json
{
  "tema": {
    "dark_mode": true,
    "cor_acento": "#3b82f6",
    "fonte_principal": "Inter",
    "fonte_mono": "JetBrains Mono"
  },
  "apresentacao": {
    "mostrar_timer": true,
    "mostrar_progresso": true,
    "auto_fullscreen": false,
    "duracao_transicao_ms": 300
  },
  "notas_apresentador": {
    "visivel": true,
    "posicao": "inferior",
    "altura_maxima": "25vh"
  }
}
```

---

## Responsividade (OBRIGATÓRIO)

### ⚠️ REGRA ABSOLUTA: 100% DOS CARDS VISÍVEIS

**Todos os templates DEVEM garantir que NENHUM card fique cortado/escondido em QUALQUER resolução.**

### ✅ CSS CORRETO (Grid Responsivo):

```css
/* Container de cards - USA ISTO */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  grid-auto-rows: auto; /* NUNCA fixar altura */
  width: 100%;
  padding: 2rem;
}

/* Media queries para breakpoints */
@media (max-width: 768px) {
  .cards-container {
    grid-template-columns: 1fr; /* 1 coluna mobile */
    gap: 1rem;
    padding: 1rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .cards-container {
    grid-template-columns: repeat(2, 1fr); /* 2 colunas tablet */
  }
}

@media (min-width: 1025px) {
  .cards-container {
    grid-template-columns: repeat(3, 1fr); /* 3+ colunas desktop */
  }
}

/* Card individual */
.card {
  background: #1a1a1a;
  border-radius: 12px;
  padding: 1.5rem;
  min-height: 120px; /* min-height OK, height NÃO */
  height: auto; /* Altura automática sempre */
}
```

### ✅ CSS CORRETO (Flexbox Responsivo):

```css
/* Container flex - USA ISTO */
.flex-container {
  display: flex;
  flex-wrap: wrap; /* OBRIGATÓRIO para responsividade */
  gap: 1.5rem;
  width: 100%;
  padding: 2rem;
}

.flex-card {
  flex: 1 1 280px; /* Grow | Shrink | Base */
  min-width: 280px;
  max-width: 400px;
  height: auto; /* NUNCA fixar */
}

@media (max-width: 768px) {
  .flex-card {
    flex: 1 1 100%; /* 100% largura mobile */
    max-width: 100%;
  }
}
```

### ❌ CSS ERRADO (NÃO USAR):

```css
/* ❌ ERRADO - Overflow esconde conteúdo */
.bad-container {
  overflow: hidden; /* NUNCA fazer isso */
  height: 100vh; /* NUNCA fixar altura do container */
}

/* ❌ ERRADO - Cards cortados */
.bad-card {
  height: 200px; /* NUNCA fixar altura */
  white-space: nowrap; /* NUNCA impedir quebra */
  overflow: hidden; /* NUNCA esconder overflow */
}

/* ❌ ERRADO - Grid sem wrap */
.bad-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Sem auto-fit/auto-fill */
  /* Cards vão ficar minúsculos em mobile! */
}
```

### Breakpoints Padrão:

| Resolução | Layout | Colunas Cards |
|-----------|--------|---------------|
| < 768px (Mobile) | 1 coluna | 100% largura |
| 768-1024px (Tablet) | 2 colunas | 50% cada |
| 1025-1440px (Desktop) | 3 colunas | 33% cada |
| > 1440px (Ultrawide) | 4 colunas | 25% cada |

### Validação Visual (Checklist):

Antes de salvar HTML, SEMPRE verificar:
- [ ] Testado em 375px (mobile pequeno)
- [ ] Testado em 768px (tablet)
- [ ] Testado em 1920px (desktop)
- [ ] Testado em 2560px (ultrawide)
- [ ] Scroll vertical funciona (se necessário)
- [ ] Nenhum card cortado
- [ ] Nenhum texto escondido
- [ ] Sem overflow:hidden em containers de conteúdo

---

## Performance e Otimizações

### Checklist de Performance:
- ✅ CSS minificado
- ✅ JavaScript otimizado (< 50KB)
- ✅ Imagens otimizadas (WebP quando possível)
- ✅ Lazy loading de seções off-screen
- ✅ Debounce em eventos de scroll/resize
- ✅ RequestAnimationFrame para animações
- ✅ **Responsividade TOTAL (todos os cards visíveis)**

### Compatibilidade:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

---

## Extensibilidade Futura

**Possíveis adições:**
- [ ] Template Timeline/Narrativo
- [ ] Template Dashboard/Comparação
- [ ] Export para PDF (via print CSS)
- [ ] Gravação de áudio sincronizada
- [ ] Highlights/anotações ao vivo
- [ ] Integração com OBS (browser source)
