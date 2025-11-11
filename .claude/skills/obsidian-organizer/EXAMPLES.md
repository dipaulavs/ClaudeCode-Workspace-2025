# Obsidian Organizer - Usage Examples

Real-world examples demonstrating intelligent type detection and minimalist note creation with Nextcloud media integration.

---

## Example 0: Saving Audio with Nextcloud Upload

**User Input:**
> "Salva pra mim esse áudio gerado lá no meu Obsidian, onde foi feito o resumo desse vídeo"

**Context:**
- Audio file: `~/Downloads/evolution_api_v3_resumo.mp3`
- Related note: `📺 Vídeos/Evolution API V3 - Novidades e Melhorias.md`

**Detection Logic:**
- Media detected: `.mp3` audio file
- Type: Update existing video note with audio link
- Action: Upload to Nextcloud + add link to existing note

**Workflow:**
1. Upload audio to Nextcloud:
   ```bash
   python3 SCRIPTS/nextcloud/upload_rapido.py ~/Downloads/evolution_api_v3_resumo.mp3
   ```
2. Get public link: `https://media.loop9.com.br/s/abc123/download/evolution_api_v3_resumo.mp3`
3. Update note adding audio link

**Updated Note:**
```markdown
## 🎬 Informações

**Link:** https://www.youtube.com/watch?v=xgXJP8uCq2c
**Categoria:** noticia
**Assistido em:** 08/11/2025 09:21
**🎙️ Áudio resumo:** [evolution_api_v3_resumo.mp3](https://media.loop9.com.br/s/abc123/download/evolution_api_v3_resumo.mp3)
```

**Response:**
```
✅ Áudio enviado ao Nextcloud e link adicionado!
📍 Nota: 📺 Vídeos/Evolution API V3 - Novidades e Melhorias.md
🔗 Link público: https://media.loop9.com.br/s/abc123/download/evolution_api_v3_resumo.mp3
```

---

## Example 1: Simple Task Creation

**User Input:**
> "Preciso lembrar de ligar pro cliente amanhã"

**Detection Logic:**
- Keyword: "preciso lembrar"
- Type: Task (📋 Tarefas)

**Generated File:** `📋 Tarefas/ligar-pro-cliente.md`

```markdown
---
criada: 07/11/2025 17:45
status: aberta
---

# Ligar pro cliente

## 📝 Detalhes
Ligar para o cliente amanhã para acompanhamento

## ✅ Checklist
- [ ] Preparar pontos da conversa
- [ ] Fazer a ligação
```

**Response:**
```
✅ Tarefa criada: 📋 Tarefas/ligar-pro-cliente.md
```

---

## Example 2: Quick Idea Capture

**User Input:**
> "Anota rapidamente: criar app de rastreamento de hábitos com gamificação"

**Detection Logic:**
- Keyword: "anota rapidamente"
- Type: Quick Note (💡 Anotações)

**Generated File:** `💡 Anotações/app-rastreamento-habitos-gamificacao.md`

```markdown
---
criada: 07/11/2025 18:12
tags:
  - anotacao
---

# App de rastreamento de hábitos com gamificação

Criar aplicativo para tracking de hábitos diários com elementos de gamificação (pontos, badges, streaks).
```

**Response:**
```
✅ Anotação criada: 💡 Anotações/app-rastreamento-habitos-gamificacao.md
```

---

## Example 3: YouTube Tutorial (with Visual Canvas)

**User Input:**
> "Assisti esse tutorial sobre async Python: https://youtube.com/watch?v=abc123
>
> Explica asyncio, async/await e event loops de forma clara."

**Detection Logic:**
- YouTube URL detected
- Keyword: "tutorial"
- Category: tutorial (from context)
- Type: Video (📺 Vídeos)
- **Auto-generate:** Visual Canvas diagram

**Generated Files:**
1. `📺 Vídeos/tutorial-async-python-asyncio.md` (markdown note)
2. `📺 Vídeos/tutorial-async-python-asyncio.canvas` (visual diagram)

**Markdown Note:**
```markdown
---
assistido: 07/11/2025 19:30
categoria: tutorial
link: https://youtube.com/watch?v=abc123
canvas: "[[tutorial-async-python-asyncio.canvas]]"
tags:
  - youtube
---

# Tutorial Async Python - AsyncIO e Event Loops

## 🎨 Resumo Visual

📊 **[Abrir Canvas Interativo](tutorial-async-python-asyncio.canvas)** - Explicação visual interativa

## 🎬 Informações
**Link:** https://youtube.com/watch?v=abc123
**Categoria:** tutorial
**Assistido em:** 07/11/2025 19:30

## 📝 Resumo
Tutorial completo sobre programação assíncrona em Python, cobrindo asyncio, async/await e event loops.

## 💡 Principais Aprendizados
- AsyncIO permite execução concorrente em Python
- async/await simplifica sintaxe assíncrona
- Event loops gerenciam tarefas assíncronas
- Ideal para I/O-bound operations

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Transcript would be added here if available via estudar-video skill]
```

**Canvas Visual (Automatic):**
```
    🎬 Tutorial Async Python
              ↓
         📝 RESUMO
         [Tutorial completo...]
              ↓
    ┌──────────┬──────────┐
    │ 💡 #1    │ 💡 #2    │
    │ AsyncIO  │ async/   │
    │ concor.  │ await    │
    ├──────────┼──────────┤
    │ 💡 #3    │ 💡 #4    │
    │ Event    │ I/O      │
    │ loops    │ bound    │
    └──────────┴──────────┘
```

**Response:**
```
✅ Vídeo salvo com Canvas visual: 📺 Vídeos/tutorial-async-python-asyncio.md
📊 Canvas interativo criado automaticamente
```

---

## Example 4: Video with Full Transcript

**User Input:**
> "Salva esse vídeo que assisti sobre GPT-4o:
> Link: https://youtube.com/watch?v=xyz789
> Categoria: notícia
>
> [Long transcript content provided...]"

**Detection Logic:**
- YouTube URL + explicit category
- Long transcript detected → use collapsible callout
- Type: Video (📺 Vídeos)

**Generated File:** `📺 Vídeos/gpt4o-lancamento-novidades.md`

```markdown
---
assistido: 07/11/2025 20:00
categoria: noticia
link: https://youtube.com/watch?v=xyz789
tags:
  - youtube
  - ia
---

# GPT-4o - Lançamento e Novidades

## 🎬 Informações
**Link:** https://youtube.com/watch?v=xyz789
**Categoria:** noticia
**Assistido em:** 07/11/2025 20:00

## 📝 Resumo
Lançamento do GPT-4o com novas capacidades multimodais e melhorias de performance.

## 💡 Principais Aprendizados
- Modelo multimodal nativo (texto, áudio, imagem)
- Melhor performance em raciocínio
- Latência reduzida

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Full 1000+ word transcript hidden in collapsible section]
```

**Response:**
```
✅ Vídeo com transcrição salvo: 📺 Vídeos/gpt4o-lancamento-novidades.md
```

---

## Example 5: Link/Article Reference

**User Input:**
> "Salva esse artigo interessante: https://example.com/article sobre arquitetura de microserviços"

**Detection Logic:**
- Non-YouTube URL
- Keyword: "salva", "artigo"
- Type: Quick Note (💡 Anotações)

**Generated File:** `💡 Anotações/artigo-arquitetura-microservicos.md`

```markdown
---
criada: 07/11/2025 20:15
tags:
  - anotacao
  - arquitetura
---

# Artigo - Arquitetura de Microserviços

**Link:** https://example.com/article

Artigo interessante sobre arquitetura de microserviços.
```

**Response:**
```
✅ Anotação criada: 💡 Anotações/artigo-arquitetura-microservicos.md
```

---

## Example 6: Task with Detailed Checklist

**User Input:**
> "Cria tarefa: Setup projeto novo - instalar dependências, configurar ESLint, setup Tailwind, criar estrutura de pastas"

**Detection Logic:**
- Explicit task keyword
- Multiple action items → checklist
- Type: Task (📋 Tarefas)

**Generated File:** `📋 Tarefas/setup-projeto-novo.md`

```markdown
---
criada: 07/11/2025 21:00
status: aberta
---

# Setup projeto novo

## 📝 Detalhes
Configuração inicial completa do novo projeto

## ✅ Checklist
- [ ] Instalar dependências
- [ ] Configurar ESLint
- [ ] Setup Tailwind CSS
- [ ] Criar estrutura de pastas
```

**Response:**
```
✅ Tarefa criada: 📋 Tarefas/setup-projeto-novo.md
```

---

## Example 7: Ambiguous Input Handling

**User Input:**
> "Salva: Machine Learning"

**Detection Logic:**
- Too vague → needs clarification
- Could be task or note

**Response:**
```
"Machine Learning" - é:
1. 📋 Tarefa (algo a fazer)
2. 💡 Anotação (referência/ideia)
```

**User Clarifies:**
> "Quero estudar depois"

**Result:**
- Keyword "estudar" → Task
- Generated: `📋 Tarefas/estudar-machine-learning.md`

---

## Example 8: Multiple Mixed Items

**User Input:**
> "Preciso anotar 3 coisas:
> 1. Tarefa: comprar café
> 2. Ideia: app de gestão de tempo
> 3. Vídeo que vi sobre React hooks"

**Detection Logic:**
- Multiple types detected
- Split into separate notes

**Generated Files:**
1. `📋 Tarefas/comprar-cafe.md` (task)
2. `💡 Anotações/app-gestao-tempo.md` (note)
3. Ask for React hooks video URL

**Response:**
```
✅ 3 itens criados:
- 📋 Tarefas/comprar-cafe.md
- 💡 Anotações/app-gestao-tempo.md

Precisa do link do vídeo de React hooks?
```

---

## Example 9: Minimalist Response Style

**User Input:**
> "Anota que preciso estudar DataView do Obsidian"

**❌ Wrong (too verbose):**
```
🎉 Ótimo! Vou criar uma anotação incrível para você sobre DataView!
É uma ferramenta super poderosa do Obsidian que vai revolucionar...
[Unnecessary 3 paragraphs...]
```

**✅ Correct (minimalist):**
```
✅ Anotação criada: 💡 Anotações/estudar-dataview-obsidian.md
```

---

## Pattern Recognition Summary

| User Pattern | Detected Type | Key Indicators |
|-------------|---------------|----------------|
| "Preciso fazer X" | Task | preciso, fazer, implementar |
| "Anota rapidamente X" | Quick Note | anota, ideia, salva |
| "Assisti vídeo [URL]" | Video | YouTube URL + context |
| "Salva esse link" | Quick Note | URL (non-YouTube) |
| "Organiza: X, Y, Z" | Multiple | Split by type |
| Multiple actions | Task + Checklist | List format |

---

## Edge Cases

### No content provided
**Input:** "Anota isso"
**Behavior:** Ask "O que deseja anotar?"

### Invalid YouTube URL
**Input:** "Assisti vídeo: youtube/broken"
**Behavior:** Ask "Link completo do YouTube?"

### Mixed types in single request
**Input:** "Fazer X e assisti vídeo Y"
**Behavior:** Create separate notes for each

### Empty task details
**Input:** "Cria tarefa X"
**Behavior:** Create minimal template, user adds details later

---

## Communication Guidelines

**Always:**
- Ultra-concise responses (1-2 lines max)
- Show filename + location
- Use Brazilian datetime format

**Never:**
- Repeat user's request
- Explain the obvious
- Add unnecessary emojis
- Ask too many clarifying questions (only when truly ambiguous)

**Example Good Response:**
```
✅ Tarefa criada: 📋 Tarefas/implementar-login.md
```

**Example Bad Response:**
```
🎉 Perfeito! Entendi que você quer criar uma tarefa super importante sobre implementação de login! Vou criar um arquivo lindo no Obsidian com todos os detalhes organizados...
```

---

**Related Documentation:**
- [[SKILL.md]] - Main instructions
- [[REFERENCE.md]] - Technical details
- [[TROUBLESHOOTING.md]] - Common issues
- [[references/templates.md]] - All templates
