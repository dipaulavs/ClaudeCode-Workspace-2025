# Visual Explainer - Apresentações Interativas

Gerador de apresentações HTML dark mode interativas para gravação de vídeos educativos.

## 🎯 Propósito

Criar apresentações visuais profissionais que você usa durante a gravação de vídeos educativos sobre IA, tecnologia, tutoriais, etc.

## 🚀 Uso Rápido

```bash
# Uso básico (detecta template automaticamente)
python3 generate.py --roteiro meu_roteiro.md

# Forçar template específico
python3 generate.py --roteiro meu_roteiro.md --template notion
python3 generate.py --roteiro meu_roteiro.md --template tech-futurista
python3 generate.py --roteiro meu_roteiro.md --template mapa-mental

# Especificar arquivo de saída
python3 generate.py --roteiro meu_roteiro.md --output apresentacao_final.html

# Não abrir navegador automaticamente
python3 generate.py --roteiro meu_roteiro.md --no-open
```

## 📋 Formatos de Roteiro

### Template Notion (Explicações Estruturadas)

```markdown
# Título da Apresentação

## Slide 1: Introdução

**Conceito:** O que são Transformers em IA

Explicação simples em 2-3 linhas sobre o conceito principal.

**Analogia:** Como um tradutor que lê a frase inteira de uma vez

✓ Ponto-chave número 1
✓ Ponto-chave número 2
✓ Ponto-chave número 3

**Notas:** Mencionar o paper "Attention is All You Need" aqui

## Slide 2: Como Funciona

**Conceito:** Mecanismo de Atenção

[Continue o roteiro...]
```

### Template Tech Futurista (Lançamentos/Novidades)

```markdown
# GEMINI 2.0 - A REVOLUÇÃO

## Slide 1: O Lançamento

**Subtítulo:** Google Redefine IA Generativa

**Ícone:** 🚀

→ Lançado em Dezembro 2024
→ 2x mais rápido que GPT-4o
→ Contexto de 2 milhões de tokens

**Notas:** Enfatizar o contexto massivo - é o diferencial principal

## Slide 2: Impacto

[Continue o roteiro...]
```

### Template Mapa Mental (Arquiteturas/Sistemas)

```markdown
# Arquitetura do GPT-4o

## Nodo Central: GPT-4o

**Descrição:** Modelo multimodal da OpenAI

### Ramo 1: Arquitetura
- Transformer Decoder
- Attention Layers
- Feed Forward Networks

### Ramo 2: Capacidades
- Texto
- Visão
- Áudio

**Notas:** Explicar que é decoder-only architecture

[Continue o roteiro...]
```

## 🎨 3 Templates Disponíveis

| Template | Quando Usar | Características |
|----------|-------------|-----------------|
| **Notion** | Explicações estruturadas, tutoriais, conceitos | Minimalista, foco no conteúdo, seções expansíveis |
| **Tech Futurista** | Lançamentos, novidades, announcements | Visual impactante, animações, gradientes |
| **Mapa Mental** | Arquiteturas, sistemas, relações entre conceitos | SVG interativo, zoom, pan, conexões visuais |

## ⌨️ Atalhos Durante Apresentação

### Universais (Todos os Templates)

| Tecla | Ação |
|-------|------|
| `→` ou `Space` | Próximo slide |
| `←` | Slide anterior |
| `F` ou `F11` | Toggle fullscreen |
| `ESC` | Sair fullscreen |
| `R` | Reset (volta ao início) |
| `?` | Mostrar ajuda |

### Mapa Mental (Adicionais)

| Tecla | Ação |
|-------|------|
| `+` | Zoom in |
| `-` | Zoom out |
| `C` | Centralizar |
| Arrastar mouse | Pan (mover canvas) |
| Clique nos nós | Ver detalhes |

## 📊 Features Incluídas

### Interatividade
- ✅ **Cards clicáveis** - Expandem para mostrar detalhes + exemplos
- ✅ **Fluxos visuais** - Processos com setas numeradas
- ✅ **Quizzes interativos** - Perguntas com feedback instantâneo
- ✅ **Hover effects** - Destaque visual ao passar mouse

### Visual & Performance
- ✅ **Dark mode obrigatório** - Design profissional noturno
- ✅ **Barra de progresso** - Indicador visual (●●●○○○)
- ✅ **Performance otimizada** - SEM animações que travam
- ✅ **HTML standalone** - Funciona 100% offline
- ✅ **Responsivo** - Adapta a qualquer resolução

### Estrutura
- ✅ **Slides de conteúdo** - Conforme roteiro
- ✅ **Slide de Resumo** - Penúltimo (3 colunas visuais)
- ✅ **Slide de CTA** - Último (Like + Inscrição + Instagram)

## 🛠️ Estrutura de Arquivos

```
scripts/visual-explainer/
├── README.md                    # Este arquivo
├── generate.py                  # Script gerador principal
│
└── templates/
    ├── notion.html              # Template minimalista/profissional
    ├── mapa-mental.html         # Template SVG interativo
    └── tech-futurista.html      # Template impacto/announcements
```

## 🧠 Decisão Automática de Template

Quando você usa `--template auto` (padrão), o script analisa o roteiro:

**Escolhe Mapa Mental se encontrar:**
- "arquitetura", "componentes", "sistema", "relações", "conexões", "fluxo", "diagrama"

**Escolhe Tech Futurista se encontrar:**
- "lançamento", "novidade", "anúncio", "impacto", "revolução", "mudança"

**Senão, usa Notion (padrão)**

## 💡 Exemplos de Uso

### Exemplo 1: Vídeo sobre Transformers (Conceito)

```bash
# Criar roteiro
cat > roteiro_transformers.md << 'EOF'
# Transformers em IA

## O Que São

**Conceito:** Arquitetura de rede neural revolucionária

Explicação: É a base de modelos como GPT, BERT e Claude.

**Analogia:** Como um tradutor que lê a frase inteira

✓ Usa mecanismo de atenção
✓ Processa texto em paralelo
✓ Criado em 2017 pelo Google

**Notas:** Mencionar paper "Attention is All You Need"
EOF

# Gerar apresentação (auto-detecta template Notion)
python3 generate.py --roteiro roteiro_transformers.md
```

### Exemplo 2: Vídeo sobre Lançamento Gemini

```bash
# Criar roteiro
cat > roteiro_gemini.md << 'EOF'
# GEMINI 2.0 FLASH

## O Lançamento

**Subtítulo:** Google Redefine IA

**Ícone:** 🚀

→ Lançado em Dezembro 2024
→ 2x mais rápido que GPT-4o
→ Contexto de 2M tokens

**Notas:** Enfatizar contexto massivo
EOF

# Gerar apresentação (auto-detecta template Tech Futurista)
python3 generate.py --roteiro roteiro_gemini.md
```

## 🔗 Integração com Claude Skill

Esta ferramenta é usada pela skill `visual-explainer`:

```
Você: "Claude, cria apresentação sobre Transformers"

→ Skill ativa automaticamente
→ Analisa conteúdo
→ Escolhe template (Notion)
→ Gera HTML
→ Abre no navegador
```

Ver documentação completa em: `.claude/skills/visual-explainer/SKILL.md`

## 📝 Output Esperado

```
📊 Template detectado automaticamente: notion

✅ Apresentação criada: apresentacao_transformers.html

📊 Template: NOTION
📍 Total de slides: 5
⏱️  Estimativa: 7 minutos

🎬 Como usar:
  • Pressione F para fullscreen
  • Setas ← → para navegar
  • Notas aparecem na parte inferior
  • Timer no canto superior direito

Pronto para gravar! 🚀
```

## 🐛 Troubleshooting

Ver guia completo de erros comuns: `.claude/skills/visual-explainer/TROUBLESHOOTING.md`

**Problemas comuns:**

- **HTML não abre:** Use `open apresentacao.html` (macOS) ou `xdg-open apresentacao.html` (Linux)
- **Atalhos não funcionam:** Clique dentro da apresentação para dar foco
- **Fontes estranhas:** Templates usam fallback automático (system fonts)

## 📦 Dependências

- Python 3.8+
- Nenhuma dependência externa (100% stdlib)

## 🚧 Roadmap

- [ ] Implementar processamento completo de Mapa Mental
- [ ] Suporte para imagens/vídeos embedded
- [ ] Export para PDF
- [ ] Modo apresentador dual-screen
- [ ] Sincronização com gravação de áudio
