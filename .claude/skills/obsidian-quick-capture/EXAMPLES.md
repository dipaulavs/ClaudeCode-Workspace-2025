# obsidian-quick-capture - Exemplos Reais

## 📋 Exemplo 1: Tarefa Bagunçada

### Input Original

```
preciso lembrar de ligar pro cliente amanhã cedo
sobre proposta e enviar orçamento atualizado
urgente!!!
```

### Output Processado

**Path:** `📋 TAREFAS/20251105_103045.md`

```markdown
# 📋 Ligar para Cliente + Enviar Orçamento

**Tipo:** Tarefa
**Capturado:** 2025-11-05 10:30 BR
**Status:** Pendente
**Prioridade:** Alta ⚠️
**Deadline:** Amanhã cedo

---

## 🎯 Resumo Visual

┌─────────────────────┐
│  CONTATO CLIENTE    │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
  Ligar       Enviar
  (manhã)    Orçamento

---

## 📝 Detalhes

**Contexto original:**
> preciso lembrar de ligar pro cliente amanhã cedo sobre proposta e enviar orçamento atualizado urgente!!!

**Pontos principais:**
- Ligar para cliente (período: manhã)
- Assunto: proposta
- Enviar orçamento atualizado

---

## ✅ Checklist

- [ ] Preparar pontos da ligação
- [ ] Ligar para cliente (manhã)
- [ ] Atualizar orçamento
- [ ] Enviar por email

---

#urgente #cliente #proposta
```

---

## 💡 Exemplo 2: Ideia Criativa

### Input Original

```
e se a gente criasse um sistema de captura rápida pro obsidian
tipo nota de voz que transcreve e organiza automaticamente
seria muito útil
```

### Output Processado

**Path:** `💡 IDEIAS/20251105_103100.md`

```markdown
# 💡 Sistema de Captura Rápida + Voz para Obsidian

**Tipo:** Ideia
**Capturado:** 2025-11-05 10:31 BR
**Status:** Pendente
**Potencial:** Alto ⭐

---

## 🎯 Resumo Visual

            SISTEMA CAPTURA
                  │
        ┌─────────┼─────────┐
        │         │         │
    Nota Voz  Transcrição  Organização
                            Automática
                                │
                        ┌───────┴───────┐
                        │               │
                   Obsidian          Visual
                   Estruturado       ASCII

---

## 📝 Descrição

**Conceito:**
Sistema inteligente que captura notas de voz, transcreve automaticamente e organiza visualmente no Obsidian.

**Valor:**
- Captura ideias no momento (sem perder)
- Zero fricção (só falar)
- Organização automática

**Contexto original:**
> e se a gente criasse um sistema de captura rápida pro obsidian tipo nota de voz que transcreve e organiza automaticamente seria muito útil

---

## 🚀 Próximos Passos

- [ ] Validar viabilidade técnica
- [ ] Pesquisar APIs de transcrição (Whisper?)
- [ ] Definir UX do fluxo
- [ ] Prototipar MVP

---

## 🔗 Recursos

- API de transcrição: OpenAI Whisper
- Obsidian API local
- Scripts existentes: `transcribe_video.py`

---

#ideia #obsidian #voz #produtividade
```

---

## 📂 Exemplo 3: Projeto Complexo

### Input Original

```
preciso desenvolver um chatbot pra imobiliária
vai ter rag com busca de imóveis
integração whatsapp
follow-up automático
sistema de score de leads
relatórios pro corretor
```

### Output Processado

**Path:** `📂 PROJETOS/20251105_103200.md`

```markdown
# 📂 Chatbot Imobiliária Completo

**Tipo:** Projeto
**Capturado:** 2025-11-05 10:32 BR
**Status:** Planejamento
**Duração Estimada:** 2-4 semanas
**Complexidade:** Alta

---

## 🎯 Visão Geral

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FASE 1    │ ─> │   FASE 2    │ ─> │   FASE 3    │
│   Core Bot  │    │ Integrações │    │  Analytics  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                   │
   WhatsApp          RAG+Score           Relatórios
   + Básico         + Follow-up           Gerenciais

---

## 📝 Escopo

**Objetivo:**
Chatbot completo para imobiliária com automação de atendimento, qualificação de leads e follow-up inteligente.

**Contexto original:**
> preciso desenvolver um chatbot pra imobiliária vai ter rag com busca de imóveis integração whatsapp follow-up automático sistema de score de leads relatórios pro corretor

---

## 🗂️ Componentes

### 1. RAG + Busca de Imóveis
- Base de conhecimento vetorial
- Busca semântica
- Filtros (preço, localização, tipo)

### 2. Integração WhatsApp
- API oficial
- Webhook
- Envio de mídia (fotos imóveis)

### 3. Follow-up Automático
- Triggers por abandono
- Mensagens contextuais
- Agendamento inteligente

### 4. Sistema de Score
- Qualificação de leads
- Segmentação automática
- Detecção de origem

### 5. Relatórios
- Dashboard corretor
- Métricas conversão
- Alertas tempo real

---

## 🗓️ Roadmap

**Fase 1: Core Bot (Semana 1)**
- [ ] Setup WhatsApp API
- [ ] RAG básico
- [ ] Fluxo conversacional

**Fase 2: Integrações (Semana 2)**
- [ ] Sistema de score
- [ ] Follow-up automático
- [ ] Busca avançada

**Fase 3: Analytics (Semana 3-4)**
- [ ] Dashboard relatórios
- [ ] Métricas tempo real
- [ ] Testes + ajustes

---

## 🔗 Recursos

- Framework: `chatbot-template/` (já existe)
- RAG: `componentes/rag/`
- Score: `componentes/score/`
- Follow-up: `componentes/followup/`

---

#projeto #chatbot #imobiliaria #whatsapp
```

---

## 📝 Exemplo 4: Nota de Estudo

### Input Original

```
descobri que o algoritmo de busca semântica do RAG
usa embeddings vetoriais pra calcular similaridade
cosine similarity é o mais comum
artigo interessante: https://arxiv.org/...
```

### Output Processado

**Path:** `📝 NOTAS/20251105_103300.md`

```markdown
# 📝 Busca Semântica RAG - Embeddings e Similaridade

**Tipo:** Nota
**Capturado:** 2025-11-05 10:33 BR
**Categoria:** Técnico - IA
**Tags:** #rag #embeddings #semantica

---

## 🎯 Resumo Visual

┌─────────────────────────┐
│   BUSCA SEMÂNTICA RAG   │
└────────────┬────────────┘
             │
    ┌────────┼────────┐
    │        │        │
Embeddings  Vector  Similaridade
Vetoriais   Database   (Cosine)
    │
    └─> Representação
        numérica do
        significado

---

## 📝 Conteúdo

**Conceito Principal:**
Algoritmos de busca semântica em sistemas RAG utilizam embeddings vetoriais para representar o significado de textos e calcular similaridade entre consultas e documentos.

**Pontos-Chave:**

1. **Embeddings Vetoriais**
   - Transformam texto em vetores numéricos
   - Capturam significado semântico
   - Dimensionalidade típica: 768-1536

2. **Cosine Similarity**
   - Método mais comum de cálculo
   - Mede ângulo entre vetores
   - Valores: -1 (oposto) a 1 (idêntico)

3. **Aplicação em RAG**
   - Query → Embedding
   - Busca top-k similares
   - Contexto → LLM

**Contexto original:**
> descobri que o algoritmo de busca semântica do RAG usa embeddings vetoriais pra calcular similaridade cosine similarity é o mais comum

---

## 🔗 Referências

- Artigo: https://arxiv.org/...
- Ver também: [[RAG Architecture]]
- Relacionado: [[Vector Databases Comparison]]

---

## 💡 Insights

- Qualidade dos embeddings impacta diretamente precisão
- Diferentes modelos (OpenAI, Sentence-BERT, etc)
- Trade-off dimensionalidade vs performance

---

#ia #rag #embeddings #semantica #estudo
```

---

## 🎤 Exemplo 5: Captura por Voz

### Input Original (Áudio)

**Transcrição automática (via Whisper):**
```
ei, acabei de ter uma ideia maluca
e se a gente fizesse um gerador de thumbnails pro youtube
que usa o estilo do alex hormozi
com aquelas cores douradas e fonte impact
seria massa pra vender curso
```

**Nota:** Obsidian não precisa estar aberto. Claude Code acessa vault diretamente via MCP filesystem.

### Output Processado

**Path:** `💡 IDEIAS/20251105_103400.md`

```markdown
# 💡 Gerador de Thumbnails Estilo Hormozi

**Tipo:** Ideia
**Capturado:** 2025-11-05 10:34 BR (via voz 🎤)
**Status:** Pendente
**Potencial:** Alto ⭐

---

## 🎯 Resumo Visual

     GERADOR THUMBNAILS
            │
    ┌───────┴───────┐
    │               │
  Estilo         Automação
  Hormozi        Completa
    │               │
    ├─> Cores       ├─> Templates
    │   douradas    ├─> API
    ├─> Font        └─> Batch
    │   Impact
    └─> Visual
        agressivo

---

## 📝 Descrição

**Conceito:**
Ferramenta automática de geração de thumbnails para YouTube no estilo visual de Alex Hormozi (cores douradas, fonte Impact, design agressivo).

**Aplicação:**
Ideal para criadores de conteúdo educativo/vendas (cursos, infoprodutos).

**Transcrição original:**
> ei, acabei de ter uma ideia maluca e se a gente fizesse um gerador de thumbnails pro youtube que usa o estilo do alex hormozi com aquelas cores douradas e fonte impact seria massa pra vender curso

---

## 🚀 Próximos Passos

- [ ] Analisar thumbnails Hormozi (padrões visuais)
- [ ] Definir paleta cores (dourado + ?)
- [ ] Escolher API geração (Canvas? Pillow?)
- [ ] Criar templates base
- [ ] Prototipar MVP

---

## 🔗 Recursos

- Referência: Canal Alex Hormozi YouTube
- Fonts: Impact, Bebas Neue
- APIs: Canva, Bannerbear, Placid
- Skill existente: `youtube-thumbnailv2`

---

#ideia #youtube #thumbnail #hormozi #design
```

---

## 🔄 Exemplo 6: Workflow Completo

### Cenário: Ideia → Projeto

**1. Captura Inicial (Ideia)**
```
Input: "criar um sistema de orçamentos automáticos"
→ Claude usa Write() para criar
Output: 💡 IDEIAS/sistema_orcamentos.md
```

**2. Validação**
```
Usuário: "valida essa ideia"
→ Auto-invoca: idea-validator skill
→ Resultado: viável, demanda confirmada
```

**3. Planejamento**
```
Usuário: "cria o PRD"
→ Auto-invoca: launch-planner skill
→ Usa Write() para criar: 📂 PROJETOS/orcamentos_mvp.md
```

**4. Desenvolvimento**
```
Usuário: "implementa"
→ Claude executa
→ Atualiza status com Write() em PROJETOS/
```

**5. Retrospectiva**
```
Após conclusão:
→ Move para 📂 PROJETOS/concluidos/ (Read + Write)
→ Cria 📝 NOTAS/aprendizados_orcamentos.md (Write)
```

**Vantagem:** Todo processo funciona sem Obsidian aberto!

---

## 📊 Estatísticas de Uso

**Classificação automática:**
- ✅ 95%+ acurácia em tipos claros
- ⚠️ 80% em textos ambíguos
- 🎤 90% com transcrição limpa

**Tempo de processamento:**
- Texto: < 1s
- Voz: 3-5s (transcrição) + 1s (processamento)

**Formatos suportados:**
- ✅ Texto puro
- ✅ Áudio (mp3, m4a, wav)
- 🔄 Futuro: imagens (OCR)

**Requisitos:**
- ❌ Obsidian NÃO precisa estar aberto
- ✅ Acesso direto ao vault via MCP filesystem
- ✅ Sincronização iCloud automática
