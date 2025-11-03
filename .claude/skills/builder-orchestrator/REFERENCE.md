# 📚 Builder Orchestrator - Documentação Técnica

## Visão Geral

**Propósito:** Orquestrar criação de ferramentas/skills/workflows de forma otimizada, usando paralelização máxima e recursos existentes.

**Diferencial:** Conhecimento completo do workspace + delegação inteligente + execução paralela.

---

## Mapeamento de Recursos do Workspace

### 1. Claude Skills (14 disponíveis)

| Skill | Uso |
|-------|-----|
| `idea-validator` | Validar viabilidade de ideias |
| `launch-planner` | Criar PRDs e MVPs |
| `product-designer` | Design UI/UX profissional |
| `marketing-writer` | Copy e conteúdo marketing |
| `hormozi-leads` | Headlines, hooks, CTAs (Hormozi) |
| `roadmap-builder` | Priorizar features |
| `adaptive-mentor` | Mentoria adaptável |
| `estudar-video` | Transcrever e analisar vídeos YouTube |
| `visual-explainer` | Apresentações HTML interativas |
| `youtube-educator` | Workflow vídeos educativos |
| `youtube-thumbnailv2` | Thumbnails profissionais |
| `orshot-design` | Designs via Orshot API |
| `obsidian-organizer` | Organização PKM |
| `skill-creator` | Criar novas skills (Progressive Disclosure) |

### 2. Templates Scripts (67+ disponíveis)

| Categoria | Path | Principais Templates |
|-----------|------|---------------------|
| WhatsApp | `scripts/whatsapp/` | 22 templates (mensagens, mídia, grupos) |
| Instagram | `scripts/instagram/` | 6 templates (post, carousel, reel, story) |
| Imagens | `scripts/image-generation/` | 5 templates (Nano Banana, GPT-4o, batch) |
| Vídeos | `scripts/video-generation/` | 2 templates (Sora, batch) |
| Áudio | `scripts/audio-generation/` | 2 templates (ElevenLabs, batch) |
| Meta Ads | `scripts/meta-ads/` | 4 templates (campanhas, ads) |
| Scraping | `scripts/instagram-scraper/`, `scripts/twitter/`, `scripts/tiktok/` | 15+ scrapers |
| Busca | `scripts/search/` | 3 templates xAI (web, Twitter, news) |
| Extração | `scripts/extraction/` | 4 templates (transcrição, scraping) |

### 3. Ferramentas Low-Level (40+ em tools/)

Raramente usadas diretamente (templates em `scripts/` são preferidos).

### 4. Capacidades Claude Code

- **Subagentes paralelos:** Task tool (general-purpose, Explore, Plan)
- **Delegação de skills:** Skill tool
- **MCP:** Canva (OAuth, design automation)
- **Bash:** Comandos sistema, git, Python

---

## Framework de Paralelização

### Análise de Dependências

**Independentes (rodar em paralelo):**
- Tarefa A não precisa de B
- Tarefa B não precisa de A
- → Executar A + B simultaneamente (2 subagentes)

**Dependentes (rodar sequencial):**
- Tarefa C precisa do resultado de A
- → Executar A primeiro, depois C

### Uso de Subagentes (Task Tool)

**Quando usar:**
- 3+ tarefas independentes
- Tarefas longas (transcrição, geração batch)
- Exploração de codebase

**Exemplo conceitual:**
Criar 3 subagentes paralelos para: (1) gerar headlines com hormozi-leads, (2) gerar imagens com batch_generate.py, (3) criar estrutura de carrossel.

### Delegação para skill-creator

**REGRA OBRIGATÓRIA:** Se precisar criar nova skill durante workflow:

1. **Identificar necessidade:** "Falta skill específica para X"
2. **Delegar:** Usar Skill tool com `skill-creator`
3. **Aguardar:** skill-creator cria estrutura Progressive Disclosure
4. **Integrar:** Usar skill criada no workflow final

---

## Processo de Orquestração (Detalhado)

### Fase 1: Análise (Checklist)

```
✅ Que skills existem que resolvem partes da tarefa?
✅ Que templates/scripts já fazem isso?
✅ O que precisa ser criado do zero?
✅ Quais tarefas são independentes?
✅ Quais dependem de outras?
```

### Fase 2: Planejamento

**Estrutura do plano:**
```
🎯 PLANO OTIMIZADO

RECURSOS DISPONÍVEIS:
- Skill X: [propósito]
- Template Y: [propósito]
- Ferramenta Z: [propósito]

TAREFAS A CRIAR:
- [Nova skill/script necessário]

EXECUÇÃO PARALELA:
├─ Subagente 1: [tarefa independente] (tempo estimado)
├─ Subagente 2: [tarefa independente] (tempo estimado)
└─ Subagente 3: [tarefa independente] (tempo estimado)

EXECUÇÃO SEQUENCIAL:
1. [Tarefa que depende de resultados anteriores]
2. [Combinação final]

TEMPO TOTAL: Xmin paralelo (vs Ymin sequencial)
GANHO: Z% mais rápido
```

### Fase 3: Execução

**Ordem de execução:**
1. Criar recursos faltantes (skills via skill-creator)
2. Lançar tarefas paralelas (Task tool)
3. Aguardar resultados
4. Executar tarefas dependentes
5. Combinar resultados finais

### Fase 4: Documentação

**Após criar novo recurso:**
1. Atualizar CLAUDE.md (Mapa de Ações ou Skills)
2. Criar/atualizar README da categoria
3. Fazer commit descritivo
4. Mostrar ao usuário onde ficou

---

## Regras de Otimização

### Princípio de Velocidade

**SEMPRE preferir:**
- ✅ Paralelização vs sequencial
- ✅ Recursos existentes vs criar novo
- ✅ Batch vs múltiplas chamadas individuais
- ✅ Subagentes vs execução direta

### Princípio de Qualidade

**Nunca sacrificar:**
- ❌ Estrutura Progressive Disclosure (skills)
- ❌ Documentação adequada
- ❌ Organização de arquivos (CLAUDE.md regras)
- ❌ Commits descritivos

### Princípio de Praticidade

**Reutilização:**
- Templates batch são obrigatórios para 2+ itens
- Skills existentes sempre têm prioridade
- Ferramentas low-level são último recurso
- Scripts descartáveis são proibidos

---

## Integração com CLAUDE.md

### Recursos a Consultar

**Antes de qualquer orquestração, ler:**
- Seção `📍 MAPA DE AÇÕES` (templates disponíveis)
- Seção `🧠 CLAUDE SKILLS` (skills disponíveis)
- Seção `🔍 REGRAS DE DECISÃO` (quando usar batch, etc)
- Seção `🚨 REGRAS DE COMPORTAMENTO` (obrigações)

### Recursos a Atualizar

**Após criar novo recurso:**
- Adicionar em `📍 MAPA DE AÇÕES` (se for template)
- Adicionar em `🧠 CLAUDE SKILLS` (se for skill)
- Atualizar contadores (X templates → X+1 templates)
- Manter formato consistente

---

## Performance e Custos

### Tempo Típico de Tarefas

| Tarefa | Sequencial | Paralelo | Ganho |
|--------|-----------|----------|-------|
| 3 headlines + 3 imagens + template | ~8min | ~3min | 62% |
| Transcrição + análise + nota Obsidian | ~5min | ~2min | 60% |
| 10 headlines + 10 imagens + carrossel | ~20min | ~6min | 70% |

### Custos de Paralelização

**Vantagens:**
- ⚡ Redução drástica de tempo
- 🎯 Melhor experiência do usuário
- 🔄 Aproveitamento de APIs assíncronas

**Desvantagens:**
- 💰 Uso de múltiplos tokens Claude (subagentes)
- 🧠 Contexto duplicado entre agentes

**Trade-off:** Velocidade vale o custo extra em quase todos os casos.

---

## Versão e Manutenção

**Versão atual:** 1.0
**Última atualização:** 2025-11-03
**Compatibilidade:** Claude Code, skills v2.0 (Progressive Disclosure)
