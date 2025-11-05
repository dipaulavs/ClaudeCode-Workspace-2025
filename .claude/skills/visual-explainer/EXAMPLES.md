# 📖 Visual Explainer - Exemplos de Uso

## Exemplo 1: Template Notion Style (Explicação Conceitual)

### Contexto
Usuário quer criar vídeo explicando "O que são Transformers" (arquitetura de IA).

### Input do Usuário
```
"Claude, cria apresentação sobre Transformers em IA,
preciso explicar o conceito de forma didática"
```

### Processamento da Skill

1. **Análise:** Detecta que é explicação conceitual estruturada
2. **Decisão:** Escolhe template **Notion Style**
3. **Estrutura gerada:**

```markdown
# Transformers em IA

## Slide 1: O Que São Transformers?
**Conceito:** Arquitetura de rede neural revolucionária criada em 2017

**Analogia:** É como ter um tradutor que consegue ler a frase inteira
de uma vez, em vez de palavra por palavra

**Pontos-chave:**
✓ Usa mecanismo de "atenção" para focar no importante
✓ Processa texto em paralelo (muito rápido)
✓ Base do GPT, BERT, e outros modelos modernos

**Notas apresentador:**
- Mencionar paper "Attention is All You Need"
- Dar exemplo de tradução de frases
- Transição: "Mas como isso funciona na prática?"

## Slide 2: Mecanismo de Atenção
[...]
```

### Output Gerado (MCP Filesystem)
```
✅ Apresentação criada e salva em:
   📂 Vault: /Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_transformers.html
   📂 Workspace: /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/apresentacao_transformers.html

📊 Template: Notion Style
📍 Total de slides: 5
⏱️  Estimativa: 8 minutos

🎬 Como usar:
  • Pressione F para fullscreen
  • Setas ← → para navegar
  • Notas aparecem na parte inferior
  • Timer no canto superior direito

🚀 Abrindo no navegador...
Pronto para gravar!
```

**Ferramentas MCP usadas:**
1. `Read` - Carregar template base
2. `Write` - Salvar HTML no vault + workspace
3. `Bash` - Abrir no navegador (`open [caminho]`)

### HTML Gerado (Snippet)
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Transformers em IA</title>
  <style>
    body {
      background: #0f0f0f;
      color: #e5e5e5;
      font-family: Inter, system-ui;
    }
    .slide {
      max-width: 1200px;
      margin: 0 auto;
      padding: 3rem;
    }
    .conceito { font-size: 2rem; font-weight: 700; }
    .analogia {
      background: #1a1a1a;
      border-left: 4px solid #3b82f6;
      padding: 1.5rem;
      margin: 2rem 0;
    }
    /* ... mais estilos ... */
  </style>
</head>
<body>
  <div class="slide active" data-slide="1">
    <div class="nav-header">
      <button class="nav-btn prev">← Anterior</button>
      <h1>O Que São Transformers?</h1>
      <button class="nav-btn next">Próximo →</button>
    </div>

    <p class="conceito">📌 Arquitetura de rede neural revolucionária</p>

    <div class="analogia">
      💡 <strong>Analogia:</strong> Como um tradutor que lê a frase inteira...
    </div>

    <ul class="pontos">
      <li>✓ Usa mecanismo de "atenção" para focar no importante</li>
      <li>✓ Processa texto em paralelo (muito rápido)</li>
      <li>✓ Base do GPT, BERT, e outros modelos</li>
    </ul>
  </div>

  <div class="apresentador-notas">
    📝 Notas: Mencionar paper "Attention is All You Need"...
  </div>

  <div class="controls">
    <div class="timer">00:00</div>
    <div class="progresso">●○○○○ 1/5</div>
  </div>

  <script>
    // Navegação, timer, atalhos...
  </script>
</body>
</html>
```

---

## Exemplo 2: Template Mapa Mental (Arquitetura de Sistema)

### Contexto
Usuário quer explicar arquitetura do GPT-4o (componentes e relações).

### Input do Usuário
```
"Preciso de apresentação visual mostrando como o GPT-4o
funciona internamente, os componentes principais"
```

### Processamento da Skill

1. **Análise:** Detecta palavras-chave "componentes", "funciona internamente"
2. **Decisão:** Escolhe template **Mapa Mental**
3. **Estrutura gerada:**

```json
{
  "tipo": "mapa-mental",
  "nodo_central": {
    "titulo": "GPT-4o",
    "descricao": "Modelo multimodal da OpenAI"
  },
  "ramos": [
    {
      "titulo": "Arquitetura",
      "cor": "#3b82f6",
      "subnodos": [
        "Transformer Decoder",
        "Attention Layers",
        "Feed Forward Networks"
      ]
    },
    {
      "titulo": "Capacidades",
      "cor": "#8b5cf6",
      "subnodos": [
        "Texto",
        "Visão",
        "Áudio"
      ]
    },
    {
      "titulo": "Treinamento",
      "cor": "#10b981",
      "subnodos": [
        "Pre-training",
        "Fine-tuning",
        "RLHF"
      ]
    }
  ]
}
```

### Output Visual (SVG Gerado)

```
                    ┌──────────────┐
               ┌────│   GPT-4o     │────┐
               │    │  Multimodal  │    │
               │    └──────────────┘    │
               ↓                        ↓
         ┌──────────┐            ┌──────────┐
         │Arquitetura│           │Capacidades│
         └─────┬────┘            └────┬─────┘
         ┌─────┼─────┐           ┌────┼────┐
         ↓     ↓     ↓           ↓    ↓    ↓
    Transform Atten Feed     Texto Visão Áudio
     Decoder  Layers Forward
```

### HTML Gerado (Snippet SVG)
```html
<svg viewBox="0 0 1200 800" class="mapa-mental">
  <!-- Nodo central -->
  <g class="nodo central" data-nodo="gpt4o">
    <rect x="500" y="350" width="200" height="100"
          rx="12" fill="#1e293b" stroke="#3b82f6" stroke-width="3"/>
    <text x="600" y="400" text-anchor="middle" fill="#fff">
      GPT-4o
    </text>
    <text x="600" y="420" text-anchor="middle" fill="#a0a0a0">
      Multimodal
    </text>
  </g>

  <!-- Conexões -->
  <line x1="600" y1="450" x2="300" y2="600"
        stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Ramo: Arquitetura -->
  <g class="nodo ramo" data-nodo="arquitetura">
    <rect x="200" y="550" width="200" height="80"
          rx="12" fill="#334155" stroke="#3b82f6" stroke-width="2"/>
    <text x="300" y="595" text-anchor="middle" fill="#fff">
      Arquitetura
    </text>
  </g>

  <!-- Clique para expandir -->
  <script>
    document.querySelectorAll('.nodo').forEach(nodo => {
      nodo.addEventListener('click', (e) => {
        mostrarDetalhes(e.target.dataset.nodo);
      });
    });
  </script>
</svg>
```

---

## Exemplo 3: Template Tech Futurista (Lançamento/Novidade)

### Contexto
Usuário quer criar vídeo anunciando lançamento do Gemini 2.0.

### Input do Usuário
```
"Claude, vou fazer vídeo sobre o lançamento do Gemini 2.0,
preciso de apresentação impactante para anunciar"
```

### Processamento da Skill

1. **Análise:** Detecta "lançamento", "anunciar" → é novidade
2. **Decisão:** Escolhe template **Tech Futurista**
3. **Estrutura gerada:**

```markdown
# GEMINI 2.0 - A REVOLUÇÃO

## Slide 1: Hero
[Ícone grande do Gemini com gradiente]
**Título:** GEMINI 2.0 FLASH
**Subtítulo:** Google redefine IA generativa

## Slide 2: O Que Mudou
→ 2x mais rápido que GPT-4o
→ Contexto de 2 milhões de tokens
→ Multimodal nativo (texto, imagem, áudio, vídeo)

## Slide 3: Impacto
**Antes:** Modelos lentos, contexto limitado
**Agora:** Velocidade + capacidade massiva

## Slide 4: Casos de Uso
[Animação de ícones]
• Análise de documentos gigantes
• Code review de repositórios inteiros
• Conversas longas sem perder contexto
```

### Output Visual (ASCII)

```
┌────────────────────────────────────────────┐
│          ●●○○○○  Slide 2 de 6              │
├────────────────────────────────────────────┤
│                                            │
│                                            │
│          🚀 GEMINI 2.0 FLASH               │
│          Google Redefine IA                │
│                                            │
│                                            │
│       ┌──────────────────────┐            │
│       │                      │            │
│       │   [Gemini Logo SVG]  │            │
│       │   com gradiente      │            │
│       │                      │            │
│       └──────────────────────┘            │
│                                            │
│                                            │
│    → Lançado em Dezembro 2024             │
│    → 2x mais rápido que GPT-4o            │
│    → Contexto de 2M tokens                │
│                                            │
│                                            │
│          [Space para continuar]            │
│                                            │
└────────────────────────────────────────────┘
```

### HTML Gerado (Snippet)
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <style>
    body {
      background: #0a0a0a;
      color: #fff;
      font-family: 'Space Grotesk', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }

    .slide {
      text-align: center;
      animation: fadeInUp 500ms ease-out;
    }

    .hero-title {
      font-size: 4rem;
      font-weight: 800;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -0.02em;
      margin-bottom: 1rem;
    }

    .hero-subtitle {
      font-size: 1.8rem;
      color: #a3a3a3;
      font-weight: 500;
      margin-bottom: 3rem;
    }

    .visual-hero {
      width: 400px;
      height: 400px;
      margin: 2rem auto;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      border-radius: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
    }

    .bullets {
      text-align: left;
      font-size: 1.5rem;
      line-height: 2.5;
      margin: 3rem auto;
      max-width: 800px;
    }

    .bullet {
      opacity: 0;
      animation: fadeIn 400ms ease-out forwards;
    }

    .bullet:nth-child(1) { animation-delay: 200ms; }
    .bullet:nth-child(2) { animation-delay: 400ms; }
    .bullet:nth-child(3) { animation-delay: 600ms; }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes fadeIn {
      to { opacity: 1; }
    }
  </style>
</head>
<body>
  <div class="slide active">
    <h1 class="hero-title">GEMINI 2.0 FLASH</h1>
    <p class="hero-subtitle">Google Redefine IA Generativa</p>

    <div class="visual-hero">
      <svg width="200" height="200" viewBox="0 0 200 200">
        <!-- Ícone do Gemini aqui -->
      </svg>
    </div>

    <div class="bullets">
      <div class="bullet">→ Lançado em Dezembro 2024</div>
      <div class="bullet">→ 2x mais rápido que GPT-4o</div>
      <div class="bullet">→ Contexto de 2 milhões de tokens</div>
    </div>
  </div>

  <div class="apresentador-notas">
    📝 Enfatizar o contexto massivo - game changer para uso real
  </div>

  <div class="timer">00:00</div>
  <div class="progresso">●●○○○○ 2/6</div>
</body>
</html>
```

---

## Resumo de Quando Usar Cada Template

| Seu Vídeo É Sobre... | Template Escolhido | Por Quê |
|----------------------|-------------------|---------|
| Explicar conceitos (teoria + exemplos) | **Notion Style** | Estrutura clara, fácil seguir |
| Mostrar arquitetura/sistema | **Mapa Mental** | Visualiza relações entre partes |
| Anunciar novidade/lançamento | **Tech Futurista** | Visual impactante, gera hype |
| Tutorial passo a passo | **Notion Style** | Sequencial e didático |
| Comparação antes/depois | **Tech Futurista** | Destaca mudanças/impacto |
| Fluxo de dados/processos | **Mapa Mental** | Mostra como tudo se conecta |

---

## Dica Final

**Você não precisa escolher!** A skill decide automaticamente baseado no seu conteúdo.

Se discordar da escolha, você pode forçar manualmente:
```
"Claude, cria apresentação MAPA MENTAL sobre [assunto]"
```
