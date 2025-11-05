# Estudar Vídeo - Documentação de Referência

## Arquitetura do Sistema

### Fluxo Completo (3 Etapas - MCP Filesystem)

```
┌─────────────────────────────────────────────────────────┐
│                    1. TRANSCRIÇÃO                       │
│  Bash tool → transcribe_video.py → Whisper API         │
│  Output: transcription.txt no ~/Downloads/              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    2. ANÁLISE IA                        │
│  Read tool → lê transcrição → Claude analisa           │
│  Classifica tipo → Extrai insights → Gera resumo       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                3. SALVAR OBSIDIAN (MCP)                 │
│  Write tool → Cria arquivo markdown direto no vault    │
│  Caminho: vault/📺 Vídeos/[TITULO].md                  │
│  Não requer Obsidian aberto                             │
└─────────────────────────────────────────────────────────┘
```

### Componentes Técnicos

#### 1. Extração de Áudio
**Ferramenta:** yt-dlp (open source)
**Formatos suportados:** YouTube, Vimeo, TikTok, 50+ sites
**Saída:** Arquivo .mp3 temporário

```bash
# Comando usado internamente
yt-dlp -x --audio-format mp3 \
  --output "/tmp/video_%(id)s.%(ext)s" \
  "URL_DO_VIDEO"
```

#### 2. Transcrição com Whisper
**API:** OpenAI Whisper
**Modelo:** whisper-1 (multilíngue)
**Custo:** $0.006/minuto (~$0.36 para vídeo de 1h)
**Idiomas:** Automático (PT, EN, ES, FR, etc.)
**Precisão:** 95%+ para áudio claro

**Saída:**
```
/Users/felipemdepaula/Downloads/transcription_youtube_[TIMESTAMP]/
├── transcription.txt      # Transcrição completa
├── metadata.json          # Título, canal, duração, URL
└── video_[ID].mp3        # Áudio temporário
```

#### 3. Análise com Claude
**Modelo:** Definido no OpenRouter (Sonnet 4.5 recomendado)
**Context window:** 200k tokens (~150k palavras)
**Capacidade:** Analisa vídeos de até 8 horas
**Tempo:** ~20-30 segundos para análise completa

**Análise inclui:**
- Classificação de tipo (6 categorias)
- Resumo executivo (2-3 parágrafos)
- Key takeaways (5-7 pontos)
- Análise específica por tipo
- Recursos mencionados
- Aplicações práticas
- Insights profundos

#### 4. Integração com Obsidian (MCP Filesystem)
**Método:** Write tool (MCP filesystem nativo do Claude Code)
**API:** Nenhuma REST API - acesso direto ao filesystem
**Formato:** Markdown com frontmatter YAML
**Localização:** iCloud Drive (sincroniza iOS)
**Requisito:** Obsidian NÃO precisa estar aberto
**Estrutura:** Tags, links internos, templates

## Sistema de Classificação de Vídeos

### 6 Tipos de Conteúdo

#### 1. Tutorial
**Definição:** Instruções passo a passo para executar uma tarefa
**Exemplos:**
- "How to build X in Y"
- "Step-by-step guide to Z"
- "Learn X in 20 minutes"

**Análise específica:**
```markdown
## Passo a Passo

### 1. [Primeira etapa]
- Comandos/código específicos
- Parâmetros importantes
- Erros comuns

### 2. [Segunda etapa]
[...]

## Pré-requisitos
- Ferramentas necessárias
- Conhecimento prévio
- Setup inicial

## Resultado Final
- O que você terá ao fim
- Como validar que funcionou
```

#### 2. Metodologia
**Definição:** Frameworks, processos, sistemas de trabalho
**Exemplos:**
- "The MASTER Framework"
- "How I prioritize features"
- "My content creation process"

**Análise específica:**
```markdown
## Framework Detalhado

### Componentes do Sistema
- [Nome do componente]: função/propósito
- [Nome do componente]: função/propósito

### Como Aplicar
1. Situação/contexto ideal
2. Passo a passo de aplicação
3. Resultados esperados

### Comparação com Alternativas
- Framework A vs Este: diferenças
- Quando usar qual
```

#### 3. Aula
**Definição:** Conteúdo educacional teórico
**Exemplos:**
- "Introduction to Machine Learning"
- "Understanding React Hooks"
- "Design Patterns Explained"

**Análise específica:**
```markdown
## Conceitos Principais

### Conceito 1: [Nome]
**Definição:** [Explicação clara]
**Por que importa:** [Relevância prática]
**Exemplo:** [Caso concreto]

### Conceito 2: [Nome]
[...]

## Conexões
- Como conceitos se relacionam
- Pré-requisitos de conhecimento
- Próximos passos de aprendizado
```

#### 4. Notícia
**Definição:** Novidades, lançamentos, updates de tecnologia
**Exemplos:**
- "Claude 4.5 Released"
- "GitHub Copilot Updates"
- "New JavaScript Features"

**Análise específica:**
```markdown
## Novidade Principal
[O que foi lançado/anunciado]

## Impacto
- Quem é afetado
- Mudanças necessárias
- Oportunidades criadas

## Timeline
- Disponibilidade
- Deprecações (se aplicável)
- Migração recomendada

## Recursos
- Docs oficiais
- Guias de migração
- Exemplos de código
```

#### 5. Review
**Definição:** Análise crítica de ferramenta/produto
**Exemplos:**
- "Cursor IDE Review"
- "Supabase vs Firebase"
- "Best AI Tools for 2024"

**Análise específica:**
```markdown
## Prós
- Vantagem 1 (com exemplo concreto)
- Vantagem 2
- [...]

## Contras
- Limitação 1 (com impacto)
- Limitação 2
- [...]

## Comparação
| Critério | Ferramenta Analisada | Alternativa |
|----------|---------------------|-------------|
| Preço | $X/mês | $Y/mês |
| Feature A | ✅ | ❌ |

## Recomendação
- Use se: [contexto específico]
- Evite se: [contexto específico]
- Alternativas: [quando considerar]
```

#### 6. Outros
**Definição:** Conteúdo que não se encaixa nas categorias acima
**Exemplos:**
- Entrevistas
- Palestras motivacionais
- Debates/discussões
- Vlogs de desenvolvimento

**Análise específica:**
```markdown
## Natureza do Conteúdo
[Formato e objetivo]

## Principais Pontos
- [Insight relevante 1]
- [Insight relevante 2]

## Aplicação
[Como usar essas informações]
```

## Prompt de Análise (Interno)

### Template Usado por Claude

```markdown
Analise esta transcrição de vídeo do YouTube e forneça:

1. CLASSIFICAÇÃO
Tipo: [Tutorial | Metodologia | Aula | Notícia | Review | Outros]
Justificativa: [Por que esse tipo?]

2. RESUMO EXECUTIVO (2-3 parágrafos)
[Síntese clara do conteúdo principal]

3. KEY TAKEAWAYS (5-7 pontos)
- [Insight 1 - específico e acionável]
- [Insight 2]
[...]

4. ANÁLISE DETALHADA
[Conteúdo específico baseado no tipo classificado]

5. RECURSOS MENCIONADOS
- [Ferramenta/link/código mencionado]
- [Outro recurso]

6. APLICAÇÕES PRÁTICAS
- [Como aplicar no dia a dia]
- [Projetos onde isso é útil]

7. INSIGHTS PROFUNDOS
[Conexões não óbvias, implicações, padrões identificados]

DIRETRIZES:
- Seja específico (números, exemplos concretos)
- Foque no valor prático
- Identifique ações aplicáveis
- Organize de forma escaneável
- Use markdown para estrutura clara
```

## Estrutura das Notas no Obsidian

### Frontmatter YAML

```yaml
---
tipo: tutorial | metodologia | aula | noticia | review | outros
titulo: "[Título exato do vídeo]"
canal: "[Nome do canal]"
url: "https://youtube.com/watch?v=..."
duracao: "XXmin"
data_assistido: YYYY-MM-DD
rating: 5
categoria: [IA & Automação, Programação, Marketing, ...]
tags:
  - youtube
  - [tag relevante 1]
  - [tag relevante 2]
status: estudado
---
```

### Corpo da Nota

```markdown
# 🎬 [Título do Vídeo]

**Canal:** [[Nome do Canal]]
**Duração:** XXmin
**Assistido em:** DD/MM/YYYY
**Rating:** ⭐⭐⭐⭐⭐
**Tipo:** #tutorial #metodologia (etc)

---

## 📝 Resumo Executivo

[2-3 parágrafos síntese]

---

## 🎯 Key Takeaways

- **[Takeaway 1]:** Explicação detalhada
- **[Takeaway 2]:** Explicação detalhada
[...]

---

## 📚 [Seção Específica por Tipo]

[Conteúdo da análise detalhada]

---

## 🔗 Recursos Mencionados

- [Ferramenta 1](link)
- [Ferramenta 2](link)

---

## 💡 Aplicações Práticas

- **Projeto X:** Como aplicar esse conhecimento
- **Situação Y:** Quando usar essa abordagem

---

## 🧠 Insights Profundos

[Conexões não óbvias, padrões, implicações]

---

## 🔗 Links Relacionados

- [[Outro Vídeo Relacionado]]
- [[Projeto que usa isso]]
- [[Conceito mencionado]]

---

## 📄 Transcrição Completa

> Transcrição disponível em: `09 - YouTube Knowledge/Transcricoes/[VIDEO_ID].txt`

[Link para arquivo de transcrição]
```

## Dashboard Automático

### Atualização Dinâmica

Cada vídeo adicionado atualiza automaticamente:

```markdown
# 📊 YouTube Knowledge Dashboard

**Total de vídeos:** [[Videos]]
**Última atualização:** DD/MM/YYYY

## 📂 Por Tipo

- **Tutoriais:** [[Videos/Tutoriais]] (X vídeos)
- **Metodologias:** [[Videos/Metodologias]] (X vídeos)
- **Aulas:** [[Videos/Aulas]] (X vídeos)
- **Notícias:** [[Videos/Noticias]] (X vídeos)
- **Reviews:** [[Videos/Reviews]] (X vídeos)
- **Outros:** [[Videos/Outros]] (X vídeos)

## 🏷️ Por Categoria

- **IA & Automação:** X vídeos
- **Programação:** X vídeos
- **Marketing:** X vídeos
[...]

## ⏰ Recentes (Últimos 10)

```dataview
TABLE tipo, canal, duracao, rating
FROM "09 - YouTube Knowledge/Videos"
SORT data_assistido DESC
LIMIT 10
```

## ⭐ Top Rated

```dataview
TABLE tipo, canal, duracao
FROM "09 - YouTube Knowledge/Videos"
WHERE rating = 5
SORT data_assistido DESC
```
```

## Configuração Técnica (MCP-Based)

### Variáveis de Ambiente

```bash
# .env
OPENAI_API_KEY=sk-...           # Para Whisper (transcrição apenas)
# Não requer OPENROUTER_API_KEY - Claude já está integrado
# Não requer OBSIDIAN_VAULT_PATH - MCP filesystem acessa direto
```

### Caminhos do Sistema (Hardcoded - MCP Write Tool)

```bash
# Caminho absoluto do vault (usado no Write tool)
VAULT_PATH="/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/"

# Pasta destino dos vídeos
VIDEOS_PATH="${VAULT_PATH}/📺 Vídeos/"

# Transcrições temporárias (fora do vault)
TRANSCRIPTIONS_PATH="/Users/felipemdepaula/Downloads/transcription_youtube_[TIMESTAMP]/"
```

### Dependências Python (Mínimas)

```
# requirements.txt (parcial)
yt-dlp>=2023.3.4          # Download de vídeos do YouTube
openai>=1.0.0             # Whisper API (transcrição apenas)
python-dotenv>=1.0.0      # Variáveis de ambiente (.env)

# NÃO requer:
# - requests (não usa REST API customizada)
# - obsidian-api (MCP filesystem direto)
```

## Performance & Custos

### Tempo de Processamento

```
Vídeo 10 min:
├─ Download: ~30s
├─ Transcrição: ~20s (Whisper)
├─ Análise: ~15s (Claude)
└─ Total: ~65s (~1 min)

Vídeo 60 min:
├─ Download: ~2min
├─ Transcrição: ~2min (Whisper)
├─ Análise: ~30s (Claude)
└─ Total: ~4.5min
```

### Custos por Vídeo

```
Transcrição (Whisper):
├─ $0.006/minuto
└─ Vídeo 60min = $0.36

Análise (Claude Sonnet 4.5):
├─ Input: ~$3/1M tokens
├─ Output: ~$15/1M tokens
├─ Vídeo 60min = ~20k tokens input + 2k output
└─ Custo = ~$0.09

TOTAL: ~$0.45 por vídeo de 1 hora
```

### Limites Técnicos

**Tamanho do vídeo:**
- Whisper: Até 25MB de áudio (~3h de vídeo)
- Claude: Até 200k tokens (~8h de transcrição)

**Idiomas suportados:**
- Whisper: 99 idiomas (automático)
- Claude: Análise em PT, EN, ES, FR

## Troubleshooting Técnico (MCP)

### Erro: "Write tool: Permission denied"
```bash
# Verificar caminho absoluto do vault
ls "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/"

# Verificar pasta destino existe
ls "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/"

# MCP Write tool não requer configuração adicional
# Obsidian NÃO precisa estar aberto
```

### Erro: "yt-dlp failed"
```bash
# Atualizar yt-dlp
pip install --upgrade yt-dlp

# Testar manualmente
yt-dlp "URL_DO_VIDEO"
```

### Erro: "Whisper API limit"
```bash
# Verificar cota da API
# OpenAI Dashboard > Usage > Whisper

# Aguardar reset (1 minuto) ou trocar chave
```

---

**Related:** See `EXAMPLES.md` for analysis examples and `TROUBLESHOOTING.md` for common issues.
