# 📖 Builder Orchestrator - Exemplos de Uso

## Exemplo 1: Workflow de Campanha Facebook (Imóveis)

### Input do Usuário
> "Preciso de um workflow para criar campanha de imóvel no Facebook. Quero headlines, imagens e carrossel prontos."

### Análise da Skill

**Recursos disponíveis:**
- ✅ `hormozi-leads` (gerar headlines)
- ✅ `scripts/image-generation/batch_generate.py` (gerar imagens)
- ✅ `.claude/skills/hormozi-leads/carrosseis-instagram.md` (templates carrossel)
- ✅ `scripts/instagram/publish_carousel.py` (publicar)

**Recursos faltantes:**
- ❌ Skill específica para orquestrar workflow completo de campanha imobiliária

### Plano Apresentado

```
🎯 PLANO OTIMIZADO: Workflow Campanha Imóvel Facebook

RECURSOS DISPONÍVEIS:
- hormozi-leads: Gerar 10 headlines persuasivas
- batch_generate.py: Gerar 5 imagens do imóvel
- carrosseis-instagram.md: Template base para carrossel
- publish_carousel.py: Publicar no Instagram

NOVA SKILL NECESSÁRIA:
- real-estate-campaign: Orquestrar workflow completo (delegar para skill-creator)

EXECUÇÃO PARALELA (3 subagentes simultâneos):
├─ Subagente 1: hormozi-leads gera 10 headlines (~2min)
├─ Subagente 2: batch_generate.py cria 5 imagens (~2min)
└─ Subagente 3: Adaptar template carrossel para imóveis (~2min)

EXECUÇÃO SEQUENCIAL:
1. skill-creator cria real-estate-campaign (~1min)
2. Combinar headlines + imagens + template (~1min)
3. Publicar com publish_carousel.py (~30s)

TEMPO TOTAL: ~6min (vs ~15min sequencial)
GANHO: 60% mais rápido
```

### Execução

**Passo 1:** Delegar criação de skill
```
Invocar skill-creator para criar real-estate-campaign
```

**Passo 2:** Lançar 3 subagentes paralelos
```
- Task 1: hormozi-leads "Gere 10 headlines para imóvel luxo 3 quartos"
- Task 2: batch_generate.py "Imagens realistas de apartamento moderno"
- Task 3: Adaptar template carrossel (base: "Negócios/Vendas")
```

**Passo 3:** Combinar resultados
```
- Escolher 5 melhores headlines
- Mapear imagens para slides do carrossel
- Gerar estrutura final
```

**Passo 4:** Publicar
```
python3 scripts/instagram/publish_carousel.py --images [5 imagens] --caption [headline]
```

### Resultado
✅ Campanha completa em 6min (headlines + imagens + carrossel)
✅ Nova skill `real-estate-campaign` reutilizável
✅ Workflow documentado e repetível

---

## Exemplo 2: Criar Ferramenta de Extração de Reviews

### Input do Usuário
> "Quero criar uma ferramenta que extrai reviews do Google Maps e gera relatório com análise de sentimento."

### Análise da Skill

**Recursos disponíveis:**
- ✅ `scripts/scraping/google_maps_basic.py` (extrair reviews)
- ✅ Claude API via OpenRouter (análise sentimento)
- ✅ Python (gerar relatório)

**Recursos faltantes:**
- ❌ Template específico para workflow completo
- ❌ Análise de sentimento integrada

### Plano Apresentado

```
🎯 PLANO OTIMIZADO: Ferramenta Análise Reviews Google Maps

RECURSOS DISPONÍVEIS:
- google_maps_basic.py: Extrair reviews de locais
- Claude API: Analisar sentimento
- Python: Gerar CSV/relatório

NOVA FERRAMENTA:
- scripts/scraping/analyze_reviews.py (criar template)

EXECUÇÃO SEQUENCIAL (dependências):
1. Extrair reviews com google_maps_basic.py (~2min)
2. Processar reviews em lote:
   ├─ Subagente 1: Analisar reviews 1-100 (~1min)
   ├─ Subagente 2: Analisar reviews 101-200 (~1min)
   └─ Subagente 3: Analisar reviews 201-300 (~1min)
3. Gerar relatório CSV com estatísticas (~30s)

TEMPO TOTAL: ~4.5min (vs ~8min sequencial)
GANHO: 44% mais rápido
```

### Execução

**Passo 1:** Extrair reviews
```bash
python3 scripts/scraping/google_maps_basic.py "Nome do Local"
```

**Passo 2:** Criar template analyze_reviews.py
```python
# Novo script que:
# 1. Lê reviews extraídos
# 2. Processa em lote via Claude API
# 3. Gera relatório CSV com: review, sentimento, score
```

**Passo 3:** Processar em paralelo (3 batches)
```
- Task 1: Analisar reviews[0:100]
- Task 2: Analisar reviews[100:200]
- Task 3: Analisar reviews[200:300]
```

**Passo 4:** Gerar relatório
```
Combinar resultados e criar CSV com estatísticas
```

### Resultado
✅ Ferramenta completa em 4.5min
✅ Novo template `analyze_reviews.py` em `scripts/scraping/`
✅ Processamento paralelo de reviews
✅ Documentado no CLAUDE.md

---

## Exemplo 3: Skill para Vídeos Educativos Completos

### Input do Usuário
> "Cria uma skill que pega um link do YouTube, transcreve, cria apresentação visual e gera thumbnail. Tudo automático."

### Análise da Skill

**Recursos disponíveis:**
- ✅ `scripts/extraction/transcribe_video.py` (transcrever)
- ✅ `visual-explainer` (apresentação HTML)
- ✅ `youtube-thumbnailv2` (thumbnails profissionais)
- ✅ `hormozi-leads` (headlines para thumbnail)
- ✅ `obsidian-organizer` (salvar nota)

**Recursos faltantes:**
- ❌ Skill que orquestra workflow completo

### Plano Apresentado

```
🎯 PLANO OTIMIZADO: Skill youtube-complete-workflow

RECURSOS DISPONÍVEIS:
- transcribe_video.py: Transcrever vídeo
- visual-explainer: Gerar apresentação
- youtube-thumbnailv2: Criar thumbnails
- hormozi-leads: Headlines para thumbnail
- obsidian-organizer: Salvar nota

NOVA SKILL:
- youtube-complete-workflow (delegar para skill-creator)

EXECUÇÃO SEQUENCIAL (transcrição primeiro):
1. transcribe_video.py [URL] (~3min)

EXECUÇÃO PARALELA (após transcrição):
├─ Subagente 1: visual-explainer usa transcrição (~2min)
├─ Subagente 2: hormozi-leads gera 10 headlines (~1min)
└─ Subagente 3: obsidian-organizer salva nota (~30s)

EXECUÇÃO FINAL:
- youtube-thumbnailv2 usa headlines geradas (~1.5min)

TEMPO TOTAL: ~7min (vs ~12min sequencial)
GANHO: 42% mais rápido
```

### Execução

**Passo 1:** Delegar criação de skill
```
skill-creator cria youtube-complete-workflow
```

**Passo 2:** Transcrever vídeo (dependência)
```bash
python3 scripts/extraction/transcribe_video.py "[URL]"
```

**Passo 3:** Lançar 3 subagentes paralelos
```
- Task 1: visual-explainer gera apresentação
- Task 2: hormozi-leads gera 10 headlines
- Task 3: obsidian-organizer salva nota no PKM
```

**Passo 4:** Gerar thumbnail (usa headlines)
```
youtube-thumbnailv2 usa melhores headlines
```

### Resultado
✅ Workflow completo em 7min (transcrição → apresentação → headlines → thumbnail → nota)
✅ Nova skill `youtube-complete-workflow` model-invoked
✅ 42% mais rápido que execução sequencial
✅ Tudo automático com apenas URL de input

---

## Padrões Comuns

### Quando Criar Nova Skill vs Template

**Criar Skill (model-invoked):**
- Workflow complexo com múltiplas etapas
- Reutilizável em vários contextos
- Beneficia de ativação automática

**Criar Template (script Python):**
- Ferramenta específica e direta
- Chamada explícita (não automática)
- Menos de 3 etapas

### Quando Usar Paralelização

**SEMPRE em paralelo:**
- Tarefas independentes (headlines + imagens)
- Análises de lote (reviews 1-100, 101-200)
- Gerações múltiplas (5 thumbnails diferentes)

**NUNCA em paralelo:**
- Tarefas dependentes (transcrição → análise)
- Criação de skills (skill-creator é sequencial)
- Combinação final (precisa de todos os resultados)

---

**Casos de uso adicionais:** Ver workflow real em `.claude/skills/youtube-educator/EXAMPLES.md`
