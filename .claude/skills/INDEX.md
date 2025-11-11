# 🧠 Claude Skills - Índice Completo

**Total:** 34 Skills | **Localização:** `.claude/skills/` | **Doc oficial:** https://docs.claude.com/en/docs/claude-code/skills.md

Skills são capacidades modulares model-invoked (Claude decide quando usar automaticamente).

**⚠️ PRIORIDADE:** `adaptive-mentor` é skill de **primeiro contato** para frases genéricas.

---

## 📋 Skills por Categoria

### 🎯 Mentoria & Planejamento

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **adaptive-mentor** | Qualquer ideia/dúvida/implementação | Mentor que ativa PRIMEIRO e se adapta depois. Pergunta detalhes se necessário. Explica ELI5 + analogias + diagramas. Cria plano executável. |
| **idea-validator** | Validar ideias antes de construir | Analisa saturação de mercado, viabilidade, demanda real, monetização. Dá feedback brutalmente honesto. |
| **launch-planner** | Planejar lançamento de MVP | Transforma ideias validadas em PRDs completos com roadmap, schema de DB, e escopo MVP (2-4 semanas). |
| **roadmap-builder** | Priorizar features | Atua como PM: decide o que construir (e o que NÃO construir). Previne feature creep. |

### 🎨 Design & UI/UX

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **product-designer** | Design de UI/UX | Elimina o "visual de IA" (gradientes azul/roxo). Cria interfaces profissionais com Tailwind + shadcn/ui. |
| **website-cloner** | Clonar design de qualquer site | Extração automática CSS via Playwright + co-criação → 100% fidelidade (não 60-70%). Gera style guide detalhado reutilizável. |
| **orshot-design** | Gerar designs/imagens | Automação de designs profissionais usando Orshot API. Posts sociais, certificados, OG images. $0.01/render. |

### 📝 Marketing & Copy

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **marketing-writer** | Criar conteúdo de marketing | Escreve landing pages, tweets, Product Hunt, emails de lançamento. Tom claro e focado em benefícios. |
| **ads-titulo-curto** | Criar copy completa Meta Ads (4 campos) | Gera Texto Principal, Título Curto, Descrição e CTA para anúncios Meta usando metodologia Hormozi. Suporta imagem estática, carrossel, reels. CTA adaptável (comentário, WhatsApp, DM). AUTO-INVOCA: "copy Meta Ads", "Facebook/Instagram ad". |
| **hormozi-leads** | Criar hooks/headlines/copy + gerar leads | AUTO-INVOCA quando pedir: hook, headline, CTA, ângulo, body, legenda IG/YT, descrição. Metodologia Hormozi: Core Four + Lead Getters. |
| **hormozi-copywriter** | Escrever copy Hormozi-style | Clone de Alex Hormozi. Escreve headlines, hooks, body copy, scripts de vídeo, email sequences, ads. Frameworks $100M Leads/Offers/Money Models. |
| **exercito-hormozi-ads** | Top 3 copys Meta Ads milhão de dólares | Orquestra 3-6 subagentes hormozi-copywriter em hierarquia (Comandante, Especialistas, Revisor). Suporta carrossel, anúncio único, reels. AUTO-INVOCA: "copy Meta Ads", "army of Hormozi". |
| **hormozi-exercito-viral** | Carrosséis educativos ultra-virais | Orquestra 3-6 subagentes Hormozi para criar conteúdo educativo de alto valor projetado para máximo engajamento via comentários com palavra-chave. Combina educação + Hormozi + estratégia viral. AUTO-INVOCA: "carrossel viral", "conteúdo educativo". |
| **cria-carrossel** | Criar carrosséis/reels completos | Automatiza criação de carrosséis virais e reels: copy Hormozi → imagens batch → legenda + hashtags. Templates validados (Colagem Artesanal, ABSM, Adesivo, Antes/Depois). AUTO-INVOCA: "cria carrossel", "post Instagram", "reels". |
| **carrossel-meta-ads** | Criar carrosséis Meta Ads (imóveis) | Workflow completo: coleta dados → subagente gera copy (3 opções) → subagente gera prompts → imagens paralelas. Copy Hormozi + visual artesanal. |
| **pega-carrossel** | Download automático carrosséis Instagram | Baixa todos os slides do carrossel, organiza com nomes descritivos (Hook, Tipo1, CTA), e gera prompts IA detalhados (versão original + template adaptável para qualquer nicho). AUTO-INVOCA: "pega/baixa esse carrossel". |
| **analitic-ads** | Análise completa Meta Ads | Busca métricas de campanhas ativas, analisa com framework Hormozi, e gera dashboard HTML visual (estilo MotherDuck) salvo em Downloads com nome do produto + data BR. AUTO-INVOCA: "puxar/analisar métricas", "dashboard de anúncios". |

### 🎥 Conteúdo YouTube

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **youtube-educator** | Criar vídeos educativos YouTube | Workflow completo: extrai conteúdo → roteiro → apresentação → headlines (hormozi) → thumbnails → nota Obsidian. FASE 1 (Pré-gravação). |
| **youtube-thumbnailv2** | Gerar thumbnails YouTube profissionais | Gera 5 variações de thumbnails (estilo único: dourado/azul-ciano). Layout fixo, split lighting, ~90s. Integra com hormozi-leads para headlines. |
| **visual-explainer** | Criar apresentações para vídeos | Gera apresentações HTML dark mode interativas (3 templates: Notion, Mapa Mental, Tech Futurista). Para gravação de vídeos educativos. |
| **estudar-video** | Estudar vídeos do YouTube | Workflow automático: transcreve (Whisper) → analisa com IA → salva em `📺 Vídeos/` (formato minimalista obsidian-organizer). |

### 📚 Knowledge Base & Consulta

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **100m-leads** | Consultar metodologias $100M Leads | Busca frameworks de geração de leads (Core Four, Lead Getters, Hook-Retain-Reward, Headlines, Curiosidade). Consulta KB do livro Alex Hormozi. |
| **100m-offers** | Consultar metodologias $100M Offers | Busca frameworks de criação de ofertas (Value Equation, Grand Slam Offer, Pricing, Stack). Consulta KB completo + Lost Chapter (Vista Equity). |
| **100m-money-models** | Consultar modelos de monetização | Busca frameworks de modelos de negócio (SaaS, Info Products, Lead Gen, Agency). Baseado em metodologia Alex Hormozi. |
| **rag-novo** | Criar knowledge bases de documentos grandes | Gera KB skills semanticamente estruturadas de PDFs/Markdown/TXT. Processo 2 fases (análise semântica → geração). Quebra em chunks <5k tokens preservando hierarquia lógica. |

### 🔧 Desenvolvimento & Automação

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **login-google** | Implementar login com Google OAuth 2.0 | Workflow completo: Google Console (OAuth Client) → Authlib → rotas Flask → proteção de páginas → UI login. Previne redirect_uri_mismatch. AUTO-INVOCA quando pedir "login com Google" ou OAuth. |
| **builder-orchestrator** | Criar ferramentas/skills/workflows | Orquestra criação otimizada usando paralelização máxima e recursos existentes. Conhece todo workspace. Delega para skill-creator quando necessário. |
| **skill-creator** | Criar novas Skills | Meta-skill que cria outras Skills automaticamente. Gera estrutura multi-arquivo Progressive Disclosure. |
| **vibecode-premium-builder** | Criar apps iOS premium via VibeCode | Gera prompts VibeCode (Large Headers, Liquid Glass, Haptics, Context Menus, Bottom Sheets) + plano backend. Cenário A: criar do zero. Cenário B: replicar app (4 métodos). |
| **json2video** | Criar/editar vídeos via JSON | Gera vídeos programaticamente (JSON2Video API). Suporta: texto/imagem/vídeo/áudio, legendas automáticas, audiogramas, voice-over (ElevenLabs), variáveis, templates. |

### 🤖 Multi-Agente & Orquestração

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **army-of-agents** | Criar conteúdo de alta qualidade com múltiplas perspectivas | Sistema multi-agente: Orquestrador define roles (Pesquisador, Copywriter, Crítico Hormozi, Diretor) → execução paralela/sequencial → feedback mútuo → iteração até aprovação. |
| **orcamento-profissional** | Criar orçamentos/propostas para clientes | Analisa recursos disponíveis (scripts/skills), calcula preço baseado em VALOR (não tempo), gera apresentação HTML profissional, aplica ancoragem realista (Hormozi), mostra ROI matemático (3 cenários). |

### 🗂️ Organização & Produtividade

| Skill | Quando Usar | Descrição |
|-------|-------------|-----------|
| **obsidian-quick-capture** | Capturar ideias bagunçadas rapidamente | Captura nota solta (texto/voz) → identifica tipo (tarefa/ideia/projeto/nota) → formata visual ASCII → organiza no local correto. Sistema INBOX → processamento automático. |
| **obsidian-organizer** | Anotar/salvar/organizar no Obsidian | Entende sistema minimalista (Tarefas/Anotações/Vídeos). Cria automaticamente no formato e local corretos. Data/hora BR. Transcrição colapsável. |
| **prompt-templates** | Pesquisar templates de prompt engineering | Consulta biblioteca aitmpl.com (100+ templates). Busca por categoria (Agents, Commands, Skills, MCPs, Hooks, Settings). WebFetch sob demanda. |

---

## 📊 Estatísticas

- **Total Skills:** 33
- **Model-Invoked:** Todas (Claude decide automaticamente)
- **Skills com KB:** 3 (100m-leads, 100m-offers, 100m-money-models)
- **Skills multi-agente:** 6 (army-of-agents, exercito-hormozi-ads, hormozi-exercito-viral, carrossel-meta-ads, youtube-educator, builder-orchestrator)
- **Skills de automação:** 5 (json2video, orshot-design, visual-explainer, estudar-video, orcamento-profissional)
- **Skills de produtividade:** 2 (obsidian-quick-capture, obsidian-organizer)

---

## 🎯 Estrutura de uma Skill (Progressive Disclosure)

```
.claude/skills/nome-da-skill/
├── SKILL.md               # Instruções principais (30-60 linhas, máx 80)
├── REFERENCE.md           # Documentação técnica detalhada
├── EXAMPLES.md            # Casos de uso reais (mínimo 2)
└── TROUBLESHOOTING.md     # Guia de erros comuns (mínimo 2)
```

**Criar nova Skill:**
- Via comando: `python3 scripts/claude-skills/create_skill.py nome-da-skill`
- Via skill: Dizer "Crie uma skill para [propósito]" → `skill-creator` ativa automaticamente

**Doc completa:** `scripts/claude-skills/README.md`
**Exemplos reais:** Ver `.claude/skills/*/EXAMPLES.md`

---

**Última atualização:** 2025-11-10
