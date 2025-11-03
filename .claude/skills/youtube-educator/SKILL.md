# 🎬 YouTube Educator - Produção Completa de Vídeos Educativos

## Quando Usar (Model-Invoked)

**Ativa automaticamente quando usuário pedir:**
- "Cria vídeo sobre [assunto]"
- "Quero fazer vídeo do YouTube de [tema]"
- "Prepara apresentação para gravar vídeo sobre [X]"

**Propósito:** Automatizar produção de vídeos educativos (roteiro → gravação → metadados → thumbnails).

---

## Workflow Automático (3 Etapas - 100% Paralelo)

### 1. Extração de Conteúdo 🔍
**Se URL YouTube fornecida:**
- Executa `python3 scripts/extraction/transcribe_video.py "URL"`
- Obtém transcrição completa do vídeo

**Se tema genérico:**
- Busca em: xAI Search + YouTube + Twitter/X
- Consolida contexto rico sobre tema

**Output:** Transcrição/contexto completo (input para todos os agents)

---

### 2. Processamento em 2 FASES 🚀

**FASE 1 - Processamento SUPER PARALELO (4 agents simultâneos):**

#### Agent 1: Apresentação HTML (Estilo Notion)
- **Subagent:** general-purpose
- **Input:** Transcrição completa
- **Tarefa:** Criar roteiro único (6-8 slides) + chamar skill `visual-explainer` (template Notion)
- **Salvamento duplo:**
  - `~/Downloads/apresentacao_[tema].html` (backup rápido)
  - `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_[tema].html` (permanente)
- **Output:** Caminho do HTML gerado em Obsidian (pasta `📺 Vídeos/Apresentações/`)

#### Agent 2: Headlines Hormozi
- **Subagent:** general-purpose
- **Input:** Transcrição completa
- **Tarefa:**
  - Ler `.claude/skills/hormozi-leads/hooks-biblioteca.md`
  - Ler `.claude/skills/hormozi-leads/headlines-frameworks.md`
  - Gerar 7 headlines (frameworks diferentes + MAIÚSCULAS + 2-3 hooks)
  - **IDENTIFICAR a headline MAIS IMPACTANTE** (escolher 1 das 7)
- **Output:** 7 headlines formatadas + **headline escolhida para thumbnail**

#### Agent 3: Descrição YouTube
- **Subagent:** general-purpose
- **Input:** Transcrição completa
- **Tarefa:** Criar arquivo `descricao_youtube_[tema].md` com:
  - Título otimizado SEO
  - Descrição com emojis
  - Timestamps detalhados
  - 3 CTAs (Soft, Médio, Alto)
  - Hashtags estratégicas
- **Output:** Caminho do arquivo criado

#### Agent 4: Nota Obsidian
- **Subagent:** general-purpose
- **Input:** Transcrição completa
- **Tarefa:** Chamar skill `obsidian-organizer` para criar nota de vídeo YouTube
  - Local automático: `📺 Vídeos/`
  - Formato: Template de Vídeo YouTube (da skill obsidian-organizer)
  - Conteúdo: Link (se houver) + Resumo + Aprendizados + Checklist de produção
  - **Assets incluir:** Link para apresentação HTML salva em `📺 Vídeos/Apresentações/`
- **Output:** Caminho da nota no Obsidian

**⏱️ Tempo Fase 1:** ~2 minutos (tudo em SUPER PARALELO)

---

**FASE 2 - Thumbnails (após Agent 2):**

#### Agent 5: Thumbnails YouTube
- **Subagent:** general-purpose
- **Input:** **Headline mais impactante** (selecionada pelo Agent 2)
- **Tarefa:** Chamar skill `youtube-thumbnailv2` com headline escolhida
- **Output:** 5 URLs de thumbnails + paths locais

**⏱️ Tempo Fase 2:** ~1 minuto
**⏱️ Tempo total:** ~3 minutos
**🚀 Ganho:** Thumbnails otimizadas com melhor headline

---

### 3. Apresentação Final 📦

**Mostrar ao usuário:**
- ✅ 1 Apresentação HTML estilo Notion (salva em `📺 Vídeos/Apresentações/` + Downloads)
- ✅ 7 Headlines Hormozi + headline escolhida (mais impactante)
- ✅ 5 Thumbnails profissionais (criadas com headline escolhida)
- ✅ Descrição YouTube completa
- ✅ Nota Obsidian com "cola" do vídeo (inclui link para apresentação)

**Próximo passo:** Gravar vídeo usando apresentação + cola do Obsidian

---

## Output Final

✅ **Apresentação HTML** → 1 apresentação estilo Notion (salva em `📺 Vídeos/Apresentações/` + `~/Downloads/`)
✅ **Headlines Hormozi** → 7 opções profissionais + 1 escolhida como MAIS IMPACTANTE
✅ **Thumbnails** → 5 variações profissionais (dourado/azul-ciano) geradas com headline escolhida
✅ **Descrição YouTube** → Completa (Título + Timestamps + CTA + Hashtags)
✅ **Nota Obsidian** → Criada via skill `obsidian-organizer` (formato minimalista + link para apresentação)

**⚡ Processamento:** Fase 1 (4 agents SUPER PARALELO) → Fase 2 (thumbnails com headline)
**⏱️ Tempo total:** ~3 minutos

**Pronto para gravação e upload!**

---

## Setup Inicial

**✅ Tudo já está configurado!**
- Foto base: URL permanente configurada
- Skill youtube-thumbnailv2: Pronta para usar
- Template profissional: Estilo dourado/azul-ciano definido

---

## Documentação Completa

- **Specs técnicas + Integração:** [REFERENCE.md](REFERENCE.md)
- **Casos de uso (4 exemplos):** [EXAMPLES.md](EXAMPLES.md)
- **Erros comuns (8 problemas):** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (auto-ativa)
**FASE:** 1 (Pré-gravação + Metadados)
**Versão:** 5.0 (Workflow otimizado: 1 apresentação Notion | 4 agents SUPER PARALELO | Obsidian via skill obsidian-organizer | Fase 2 thumbnails independente)
