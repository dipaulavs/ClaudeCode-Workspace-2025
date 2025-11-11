# 🎯 Casos de Uso - Workstation Completa

**Última atualização:** 2025-11-05

---

## 📊 ÍNDICE

- [Skills IA (27 skills)](#skills-ia)
- [Geração de Conteúdo](#geracao-conteudo)
- [Social Media & Ads](#social-media)
- [Workflows Completos (10 workflows)](#workflows-completos)

---

<a name="skills-ia"></a>
## 🧠 SKILLS IA

### adaptive-mentor

#### Caso de Uso 1: Desenvolvedor Junior com Ideia Confusa
**Contexto:** Dev junior diz "quero fazer um app tipo Uber mas pra entregadores de comida, mas não sei por onde começar"
**Solução:** Skill ativa PRIMEIRO, faz perguntas estratégicas (público? tech stack? prazo?), explica conceitos com analogias ELI5, desenha diagrama ASCII do fluxo, cria plano executável em etapas
**Resultado:** Em vez de "me dê mais detalhes", entrega plano concreto de 4 semanas com arquitetura visual e próximos passos claros

#### Caso de Uso 2: Empreendedor Não-Técnico com Problema de Negócio
**Contexto:** Cliente diz "minha equipe perde muito tempo respondendo mesmas perguntas no WhatsApp, tem como automatizar?"
**Solução:** Skill detecta gap técnico, explica chatbot com analogia (recepcionista 24/7), desenha fluxo usuário→bot→humano, propõe implementação realista (framework já existente)
**Resultado:** Cliente entende viabilidade, custo e timeline sem jargão técnico, decisão informada em 10 minutos

#### Caso de Uso 3: Estudante Travado em Bug Complexo
**Contexto:** "Meu código tá dando erro mas não entendo por quê" (código assíncrono React)
**Solução:** Skill identifica nivel (intermediário), explica event loop com analogia de restaurante, diagrama ASCII do fluxo de execução, mostra onde promise falha
**Resultado:** Além de corrigir o bug, estudante entende conceito fundamental de async/await permanentemente

---

### idea-validator

#### Caso de Uso 1: Indie Hacker com Ideia de SaaS
**Contexto:** Dev quer criar "Notion para médicos" e acha que vai funcionar porque médicos usam muito papel
**Solução:** Skill analisa mercado (10+ concorrentes especializados), questiona demanda real vs stated interest, calcula viabilidade solo (8-12 semanas = inviável), expõe fricção de compliance (HIPAA)
**Resultado:** Evita 3 meses de desenvolvimento perdido, pivota para nicho menor (clínicas veterinárias) com validação real

#### Caso de Uso 2: Fundador com Ideia Saturada
**Contexto:** "Vou fazer app de delivery porque iFood cobra muito caro dos restaurantes"
**Solução:** Skill mostra dados brutais: 15 competidores locais falidos, efeito de rede do iFood = impossível competir, custo de aquisição >R$50/usuário, break-even em 5+ anos
**Resultado:** Feedback honesto em 5min evita queimar economia pessoal, redireciona para vertical específica (delivery de marmitas fit)

#### Caso de Uso 3: Desenvolvedora com Solução em Busca de Problema
**Contexto:** "Criei ferramenta AI que resume PDFs, vou vender para estudantes"
**Solução:** Skill identifica: 20+ ferramentas grátis fazem isso, estudantes não pagam por software, monetização impossível, mas descobre uso real em nicho B2B (advogados analisando contratos)
**Resultado:** Pivota de B2C fracassado para B2B viável, valida com 3 escritórios antes de construir MVP

---

### launch-planner

#### Caso de Uso 1: Startup Validada Pronta pra MVP
**Contexto:** Validou ideia (waitlist com 200 emails), precisa criar MVP em 4 semanas para pitch de investidor
**Solução:** Skill transforma conceito em PRD completo: user stories priorizadas, schema Supabase com RLS, roadmap Next.js 14, escopo cirúrgico (só features que demonstram valor core)
**Resultado:** Entrega MVP funcional em Vercel em 3.5 semanas, pitch com produto real funcionando, levanta seed round

#### Caso de Uso 2: Agência Recebendo Projeto Mal Definido
**Contexto:** Cliente quer "plataforma de cursos" mas brief tem 3 linhas
**Solução:** Skill extrai requisitos via perguntas estruturadas, cria PRD profissional (10 páginas), define MVP vs V2 vs Nice-to-Have, gera schema DB normalizado, estima timeline realista (8 semanas)
**Resultado:** Proposta técnica impressiona cliente, evita scope creep, projeto entregue no prazo com margem de 15%

---

### roadmap-builder

#### Caso de Uso 1: Fundador Sobrecarregado com Feature Requests
**Contexto:** 200 usuários pedindo 50 features diferentes via support tickets, dev perdido sem saber priorizar
**Solução:** Skill analisa codebase atual, categoriza requests por impacto/esforço, identifica 3 features que 80% dos usuários pedem, cria roadmap trimestral com justificativa matemática (retenção +30%)
**Resultado:** Ignora 90% dos pedidos com confiança, foca em 3 features high-impact, churn cai de 15% para 5% em 2 meses

#### Caso de Uso 2: SaaS em Fase de Growth
**Contexto:** Produto funciona, 1000 usuários ativos, mas não sabe se investe em: (a) automações (b) integrações (c) analytics
**Solução:** Skill analisa métricas (NPS, churn, ticket médio), descobre que 70% do churn é por falta de integrações, calcula ROI de cada opção, prioriza 2 integrações críticas (Zapier + Slack)
**Resultado:** Implementa integrações em 3 semanas, churn cai 40%, LTV sobe de $300 para $500

---

### product-designer

#### Caso de Uso 1: Developer Frustrado com "Cara de Projeto de Faculdade"
**Contexto:** App funciona perfeitamente mas usuários reclamam que "parece amador", gradientes azul/roxo padrão, espaçamento inconsistente
**Solução:** Skill aplica sistema de design profissional: tipografia hierárquica (Inter + escala modular), cores neutras + 1 accent, espaçamento Tailwind (4/8/16), componentes shadcn/ui
**Resultado:** Redesign completo em 1 dia, conversão de trial→pago sobe de 8% para 18%

#### Caso de Uso 2: Startup B2B Precisando Parecer Enterprise
**Contexto:** Produto vendido para CFOs de empresas grandes, UI atual parece "startup de garage", perde deals por "falta de profissionalismo"
**Solução:** Skill cria design system corporativo: palette cinza/azul sóbrio, tabelas densas de dados, dark mode opcional, microinterações sutis, zero gradientes/glassmorphism
**Resultado:** Redesign fecha 3 contratos enterprise pausados ($120k ARR), CFO diz "agora sim parece ferramenta séria"

---

### marketing-writer

#### Caso de Uso 1: Indie Hacker Lançando no Product Hunt
**Contexto:** Produto pronto mas zero habilidade de copywriting, landing page atual diz "ferramenta para gerenciar tarefas" (genérico)
**Solução:** Skill analisa codebase, identifica diferencial único (AI que prioriza tarefas por impacto), escreve headline focada em benefício ("Stop doing busywork. AI finds your highest-impact tasks"), copy clara sem jargão
**Resultado:** Launch PH atinge #2 do dia, 800 signups, copy clara converte 22% de visitantes (vs 5% anterior)

#### Caso de Uso 2: SaaS B2B Escrevendo Cold Emails
**Contexto:** 500 leads qualificados mas taxa de resposta 1% em cold emails genéricos ("solução inovadora para seu negócio")
**Solução:** Skill escreve emails personalizados por segmento, abre com problema específico (não pitch), CTA clara e de baixo commitment ("responda com SIM se quiser ver demo de 5min")
**Resultado:** Taxa de resposta sobe para 12%, 60 demos agendados, 8 contratos fechados ($40k ARR)

---

### hormozi-leads

#### Caso de Uso 1: Coach Online com Anúncio Genérico
**Contexto:** Anuncia "curso de emagrecimento" no Meta Ads, CPL de R$80 (inviável), copy genérico sem gancho
**Solução:** Skill aplica Hook-Retain-Reward: "Emagreça 5kg em 30 dias sem dieta maluca (método validado com 200 clientes)" → gera 5 variações de hook testáveis, CTA de baixo commitment (ebook grátis)
**Resultado:** Testa 5 hooks, melhor atinge CPL de R$12, volume de leads 10x maior, ROI positivo pela primeira vez

#### Caso de Uso 2: E-commerce de Moda com Legenda de IG Fraca
**Contexto:** Post bonito mas legenda só descreve produto ("vestido floral em viscose"), engajamento 1%
**Solução:** Skill gera legenda Hormozi: abre com curiosidade ("Por que essa peça esgotou 3x em 2 meses?"), conta história emocional (cliente usou em pedido de casamento), CTA suave (link na bio)
**Resultado:** Engajamento sobe para 8%, vendas diretas do post aumentam 40%

---

### carrossel-meta-ads

#### Caso de Uso 1: Corretor de Imóveis com Meta Ads Travado
**Contexto:** Anuncia apartamento de R$800k no Meta Ads, anúncio genérico ("Apto 3 quartos no centro"), CPL R$150, zero conversões em 30 dias
**Solução:** Skill roda workflow completo: extrai dados do imóvel → subagente gera 3 opções de copy Hormozi ("Pare de Pagar Aluguel: Apto que se Paga em 7 Anos") → subagente gera prompts visuais artesanais → gera 10 imagens paralelas
**Resultado:** Carrossel com copy emocional + visuais únicos, CPL cai para R$35, 12 visitas agendadas, 1 venda fechada (comissão R$24k)

#### Caso de Uso 2: Imobiliária Lançando Empreendimento
**Contexto:** Lançamento de condomínio com 80 unidades, precisa vender 30 em pré-lançamento, ads atuais convertem 0.5%
**Solução:** Skill gera 5 carrosséis diferentes testando ângulos (localização, ROI, lifestyle, escassez, prova social), cada um com copy Hormozi + 10 imagens únicas
**Resultado:** Testa 5 campanhas paralelas, melhor carrossel atinge 3.2% conversão, 42 unidades vendidas em pré-lançamento

---

### youtube-educator

#### Caso de Uso 1: Developer Criando Canal Técnico
**Contexto:** Quer ensinar React no YouTube mas trava ao escrever roteiro, vídeos desorganizados, 50 views/vídeo
**Solução:** Skill roda workflow FASE 1: extrai conceito (hooks) → gera roteiro estruturado (problema→solução→prática) → cria apresentação HTML dark mode → gera 5 headlines Hormozi → 5 thumbnails automáticos
**Resultado:** Vídeos organizados profissionalmente, headlines chamativas ("React Hooks Explained (finally makes sense)"), views sobem para 2k/vídeo

#### Caso de Uso 2: Coach Transformando Conteúdo Escrito em Vídeo
**Contexto:** Tem 50 artigos de blog sobre produtividade, quer replicar no YouTube mas não sabe adaptar formato
**Solução:** Skill pega artigo → identifica story arc → gera roteiro para vídeo de 8-12min → cria slides visuais (Mapa Mental template) → headlines testáveis
**Resultado:** Converte 10 artigos em vídeos em 1 semana, canal cresce de 0 para 500 inscritos no primeiro mês

---

### estudar-video

#### Caso de Uso 1: Desenvolvedor Assistindo Conference Talks
**Contexto:** Assiste 10 talks/mês do YouTube (Next.js Conf, React Summit), quer revisar conceitos depois mas não lembra detalhes
**Solução:** Skill pega URL → transcreve com Whisper → analisa com IA → extrai insights principais → salva nota minimalista no Obsidian (`📺 Vídeos/`)
**Resultado:** Biblioteca de 100+ talks indexadas e pesquisáveis, revisa conceitos em 2min vs reassistir vídeo de 40min

#### Caso de Uso 2: Estudante de Marketing Digital
**Contexto:** Curso de Alex Hormozi (50 vídeos), assiste mas esquece 80% em 1 semana
**Solução:** Skill processa todos os vídeos do curso → gera notas estruturadas com timestamps → identifica frameworks principais → organiza por tema
**Resultado:** Revisa curso inteiro em 30min antes de prova, aprovação com nota 9.5, economiza 10h de reassistir vídeos

---

### 100m-leads

#### Caso de Uso 1: Agência com CAC Insustentável
**Contexto:** Gasta R$5k/mês em Meta Ads, gera 50 leads mas só fecha 2 clientes (CAC R$2500, LTV R$3000 = margem inexistente)
**Solução:** Skill consulta KB → ensina Core Four (Warm Outbound + Cold Outbound + Free Content + Paid Ads), sugere adicionar Cold Outbound (LinkedIn + email), calcula novo CAC projetado
**Resultado:** Diversifica canais, CAC cai para R$800, fecha 15 clientes/mês, negócio finalmente lucrativo

#### Caso de Uso 2: Coach com Anúncios que Não Convertem
**Contexto:** Meta Ads gerando leads mas ninguém compra (conversão lead→cliente 1%), problema não é preço
**Solução:** Skill busca framework Hook-Retain-Reward → identifica hook fraco (genérico), ensina reescrever com curiosidade + especificidade, gera 5 exemplos testáveis
**Resultado:** Testa novos hooks, conversão lead→cliente sobe para 8%, ROI de ads finalmente positivo

---

### 100m-offers

#### Caso de Uso 1: Freelancer com Proposta Rejeitada
**Contexto:** Propõe "site institucional por R$5k", cliente acha caro e contrata concorrente por R$2k
**Solução:** Skill consulta Value Equation → ensina reposicionar como "Sistema de Captação de Leads" (inclui site + SEO + formulários + integração CRM), stack de valor vs preço isolado
**Resultado:** Reprecia para R$8k com stack completo, cliente paga feliz porque vê ROI claro (100 leads/mês = R$20k em vendas)

#### Caso de Uso 2: SaaS com Churn Alto (10%/mês)
**Contexto:** Produto bom mas clientes cancelam após 3 meses, não entendem valor completo
**Solução:** Skill busca Grand Slam Offer → identifica que falta clarity of value, sugere rename de features para benefícios ("AI Assistant" → "Save 10 hours/week"), adiciona onboarding estruturado
**Resultado:** Churn cai de 10% para 4%, LTV dobra de $300 para $600

---

### orcamento-profissional

#### Caso de Uso 1: Freelancer Perdendo Proposta por "Estar Caro"
**Contexto:** Propõe chatbot WhatsApp por R$8k, cliente diz "muito caro" e some
**Solução:** Skill analisa recursos (scripts prontos), calcula preço por VALOR (chatbot economiza 40h/mês de atendimento = R$4k/mês economizados), gera apresentação HTML com ROI em 3 cenários (conservador/realista/otimista), aplica ancoragem (mostra versão enterprise de R$25k primeiro)
**Resultado:** Cliente vê ROI claro (payback em 2 meses), aceita proposta de R$12k (vs R$8k original), paga feliz porque entende valor

#### Caso de Uso 2: Agência Competindo com Freelancer Barato
**Contexto:** Concorrente propõe site por R$2k, agência quer cobrar R$15k mas precisa justificar diferença
**Solução:** Skill gera orçamento profissional: mostra stack de valor (site + SEO + conversões + analytics + suporte 3 meses), calcula ROI matemático (100 leads/mês × 5% conversão × R$1k ticket = R$5k/mês), apresentação HTML impecável vs PDF genérico do concorrente
**Resultado:** Cliente escolhe agência mesmo 7x mais cara, entende que está comprando SISTEMA DE VENDAS (não só site bonito)

---

<a name="geracao-conteudo"></a>
## 🎨 GERAÇÃO DE CONTEÚDO

### Imagens - Catálogo de Produtos E-commerce
**Ferramenta:** Nano Banana Batch
**Cenário:** Loja online precisa gerar 50 imagens de produtos com fundo profissional
**Execução:**
```bash
python3 scripts/image-generation/batch_generate.py --api nanobanana \
  "relógio dourado luxuoso fundo branco" \
  "tênis esportivo preto vista lateral" \
  "bolsa de couro marrom fundo neutro"
```
**Resultado:** 50 imagens hiper-realistas em portrait 2:3, salvas em ~/Downloads/, prontas para upload no site

---

### Imagens - Variações de Logo/Identidade Visual
**Ferramenta:** GPT-4o com variants
**Cenário:** Designer precisa apresentar 4 opções de logo para cliente aprovar
**Execução:**
```bash
python3 tools/generate_image.py "logo minimalista letra M com folhas verdes" --variants 4
```
**Resultado:** 4 variações do mesmo conceito (2:3), cliente escolhe a preferida

---

### Vídeos - Anúncios Imobiliários Automatizados
**Ferramenta:** Sora 2 Batch
**Cenário:** Imobiliária anuncia 8 imóveis por semana, precisa de vídeos promocionais
**Execução:**
```bash
python3 scripts/video-generation/batch_generate.py --aspect landscape \
  "tour virtual apartamento moderno sacada vista mar" \
  "sobrado 3 quartos jardim quintal piscina"
```
**Resultado:** 8 vídeos ~15s em landscape, gerados em paralelo (2-5min total), prontos para Instagram/WhatsApp

---

### Áudio - Narração de Vídeos Explicativos
**Ferramenta:** ElevenLabs (single)
**Cenário:** YouTuber precisa narrar roteiro de 2min com voz profissional
**Execução:**
```bash
python3 scripts/audio-generation/generate_elevenlabs.py "Bem-vindo ao tutorial de Python..." --voice felipe --format mp3_high
```
**Resultado:** Áudio MP3 alta qualidade, voz clonada natural, pronto para edição de vídeo

---

### Áudio - Sistema de URA/Atendimento Automático
**Ferramenta:** ElevenLabs Batch
**Cenário:** Empresa implementando URA, precisa gravar 15 mensagens
**Execução:**
```bash
python3 scripts/audio-generation/batch_generate.py \
  "Bem-vindo à empresa X" \
  "Digite 1 para vendas, 2 para suporte" \
  "Aguarde, transferindo..."
```
**Resultado:** 15 áudios sequenciais (70+ idiomas), voz consistente Michele, prontos para sistema telefônico

---

<a name="social-media"></a>
## 📱 SOCIAL MEDIA & ADS

### Instagram - Análise de Concorrentes com Publicação Automática
**Objetivo:** Monitorar concorrentes e criar conteúdo baseado em tendências
**Workflow:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Scrape    │ → │  Analisa IA │ → │  Gera Post  │ → │  Publica IG │
│ Concorrente │    │  Tendências │    │ (imagem/AI) │    │  Agendado   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```
**Ferramentas:** `scrape_profile.py` → `scrape_hashtag.py` → `generate_nanobanana.py` → `publish_post.py` → `schedule_whatsapp.py`
**ROI Esperado:** Redução 80% tempo pesquisa + engajamento 40% maior (posts data-driven)

---

### WhatsApp - Chatbot de Qualificação 24/7
**Objetivo:** Qualificar leads e agendar visitas automaticamente
**Workflow:**
```
Lead manda msg ──> Chatbot IA ──> Qualifica? ──YES──> Agenda visita + notifica vendedor
                                      │
                                      NO
                                      └──> FAQ automático
```
**Ferramentas:** `criar_chatbot_cliente.py` (framework universal) + `agendar_visita.py`
**ROI Esperado:** 70% redução tempo atendimento + vendedores focam em leads quentes + disponibilidade 24/7

---

### Meta Ads - Campanhas Dinâmicas de Imóveis/Carros
**Objetivo:** Criar 50+ anúncios personalizados automaticamente
**Workflow:**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Catálogo    │ → │  Carrosséis │ → │  Campanha + │ → │   Anúncios  │
│ (JSON/BD)   │    │    batch    │    │   Ad Sets   │    │   ativos    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```
**Ferramentas:** SKILL `carrossel-meta-ads` → `create_campaign.py` → `create_adset.py` → `create_ad.py`
**ROI Esperado:** Criação 50 anúncios em 10min (antes: 8h manual) + CPC 30% menor (segmentação precisa)

---

### TikTok - Análise de Tendências para Criação de Conteúdo
**Objetivo:** Identificar trends virais e criar conteúdo similar
**Workflow:**
```
Scrape trending ──> Analisa IA (padrões) ──> Gera roteiro ──> Cria vídeo (Sora) ──> Publicação manual
```
**Ferramentas:** `scrape_trending.py` → Claude (análise) → `generate_sora.py`
**ROI Esperado:** 3-5x mais views (conteúdo trend-based) + redução 70% tempo pesquisa

---

### Twitter/X - Monitoramento de Marca e Resposta Automática
**Objetivo:** Detectar menções e responder em <5min
**Workflow:**
```
Scrape "@marca" ──> Filtro IA (urgência?) ──YES──> Notificação + rascunho resposta
                            │
                            NO
                            └──> Log para análise
```
**Ferramentas:** `search_twitter.py` + Claude (classificação) + notificação Obsidian
**ROI Esperado:** Tempo resposta 95% menor + crise evitada (detecção precoce)

---

<a name="workflows-completos"></a>
## 🚀 WORKFLOWS COMPLETOS

### Workflow 1: E-commerce Turbo Launch

**Problema:** Lançar produto físico/digital e começar a gerar leads/vendas em <24h
**Stack:** Idea Validator + Launch Planner + Meta Ads + WhatsApp + Instagram + Obsidian

#### Fluxo:
```
Ideia inicial → Validação → PRD/MVP → Criativos → Campanha → Automação → Monitoramento
     ↓             ↓           ↓          ↓          ↓           ↓            ↓
  Usuário    idea-validator  launch-   carrossel-  meta-ads   whatsapp-   obsidian-
                              planner   meta-ads    scripts    chatbot     organizer
```

1. **Validação brutal** (`idea-validator`) → Análise de mercado, concorrência, viabilidade financeira
2. **Planejamento executável** (`launch-planner`) → PRD + Schema DB + Stack tech + Timeline 2-4 semanas
3. **Copy Hormozi** (`carrossel-meta-ads` ou `marketing-writer`) → Headlines/CTAs/Ofertas irresistíveis
4. **Criativos visuais** (`scripts/image-generation/batch_generate.py --api nanobanana`) → 5-10 variações paralelas
5. **Campanha raio** (`scripts/meta-ads/meta_ads_regional_campaign.py`) → Targeting geográfico preciso
6. **Chatbot de vendas** (`criar_chatbot_cliente.py`) → Framework universal WhatsApp (5min setup)
7. **Instagram amplificação** (`scripts/instagram/publish_carousel.py`) → Carrossel organico + Story
8. **Tracking centralizado** (`obsidian-organizer`) → Registro automático métricas/insights

**Tempo Total:** 8-12h (distribuído em 2 dias)
**ROI:** Validação previne 80% dos fracassos / Primeiras vendas em <48h / Automação reduz 90% follow-up manual

---

### Workflow 2: Geração de Leads Hiper-Segmentados (B2B)

**Problema:** Encontrar leads qualificados com dados de contato validados para cold outreach
**Stack:** Google Maps Scraper + Instagram Scraper + WhatsApp + xAI Search + Obsidian

#### Fluxo:
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Scrape GMaps │ →  │ Enriquecer   │ →  │ Validar      │ →  │ Outreach     │
│ (empresas)   │    │ com IG/xAI   │    │ qualidade    │    │ automatizado │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

1. **Extração massiva** (`scripts/scraping/google_maps_batch.py`) → 2000+ empresas (nome, tel, endereço, site, rating)
2. **Enriquecimento Instagram** (`scripts/instagram-scraper/scrape_user_profile.py`) → Bio, engajamento, followers
3. **Validação contextual** (`scripts/search/xai_web.py`) → Notícias recentes, expansões, contratações
4. **Análise competitiva** (`100m-offers` skill) → Identificar dores/ofertas irresistíveis baseado em Value Equation
5. **Copy personalizado** (`hormozi-leads` skill) → Hook-Retain-Reward customizado por lead
6. **Outreach batch** (`scripts/whatsapp/send_message.py` em loop) → Mensagens hiperpersonalizadas
7. **CRM minimalista** (`obsidian-organizer`) → Tracking de respostas/follow-ups

**Tempo Total:** 3-5h (setup inicial) + 30min/dia (follow-up)
**ROI:** Lead qualificado custa $0.50-2 (vs $15-50 em ads) / Taxa conversão 8-15% (vs 1-3% cold ads)

---

### Workflow 3: Criador de Conteúdo Educativo (YouTube → Multi-Plataforma)

**Problema:** Criar conteúdo educativo de alta qualidade e distribuir em 5+ plataformas simultaneamente
**Stack:** YouTube Educator + Visual Explainer + Thumbnails + ElevenLabs + Instagram + TikTok + Obsidian

#### Fluxo:
```
Tópico → Roteiro → Apresentação → Gravação → Thumbnails → Publicação → Repurposing
   ↓        ↓          ↓            ↓           ↓            ↓             ↓
youtube- visual-   youtube-      (manual)   youtube-      YouTube    Cortes para
educator explainer thumbnailv2              thumbnailv2              IG/TikTok
```

1. **Pesquisa + Roteiro** (`youtube-educator`) → Extrai conteúdo + estrutura FASE 1 (pré-gravação)
2. **Apresentação interativa** (`visual-explainer`) → 3 templates (Notion/Mapa Mental/Tech) dark mode
3. **Thumbnails profissionais** (`youtube-thumbnailv2`) → 5 variações (dourado/azul-ciano) + headlines Hormozi
4. **Voice-over AI** (`scripts/audio-generation/batch_generate.py`) → Narração em 70+ idiomas
5. **Publicação YouTube** (manual) → Upload vídeo + thumbnail + descrição SEO
6. **Cortes virais** (`json2video` skill) → 3-5 clips <60s com legendas automáticas
7. **Distribuição massiva**:
   - Instagram Reels (`scripts/instagram/publish_reel.py`)
   - TikTok (upload manual)
   - Carrossel educativo (`scripts/instagram/publish_carousel.py`)
8. **Knowledge Base** (`estudar-video` + `obsidian-organizer`) → Salva transcrição + insights em Obsidian

**Tempo Total:** 6-10h/vídeo (incluindo gravação)
**ROI:** 1 vídeo → 8-12 pieces de conteúdo / Crescimento orgânico 3-5x mais rápido / Autoridade no nicho

---

### Workflow 4: Funil de Vendas Imobiliário Automatizado

**Problema:** Captar leads qualificados para imóveis e converter em visitas agendadas
**Stack:** Chatbot Framework + Meta Ads + Instagram + WhatsApp + RAG + Obsidian

#### Fluxo:
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Captação   │→ │  Qualific.  │→ │   Nutrição  │→ │   Conversão │
│  (Ads/IG)   │   │  (Chatbot)  │   │  (WhatsApp) │   │   (Visita)  │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

1. **Setup chatbot** (`criar_chatbot_cliente.py`) → Framework universal WhatsApp (5min)
2. **Upload imóveis** (workflow automático) → Fotos + dados → `links.json` + Redis RAG
3. **Carrosséis Meta Ads** (`carrossel-meta-ads`) → Copy Hormozi + imagens hiper-realistas + targeting raio
4. **Instagram orgânico** (`scripts/instagram/publish_carousel.py`) → 1 imóvel/dia com CTA WhatsApp
5. **Chatbot inteligente** (RAG busca híbrida) → Responde dúvidas, filtra preferências, sugere imóveis
6. **Agendamento automático** (`ferramentas/agendar_visita.py`) → Integração Google Calendar
7. **Follow-up programado** (`scheduling-system/schedule_whatsapp.py`) → Mensagens 24h/48h/72h
8. **CRM Obsidian** (`obsidian-organizer`) → Tracking leads/visitas/conversões

**Tempo Total:** 2h (setup inicial) + 15min/dia (novos imóveis)
**ROI:** 70% redução tempo atendimento / 40% aumento taxa conversão / Atendimento 24/7

---

### Workflow 5: Lançamento Produto Digital (Infoproduto/SaaS)

**Problema:** Validar, construir e lançar produto digital em <30 dias com tração inicial
**Stack:** Idea Validator + Launch Planner + Marketing Writer + Visual Explainer + Orshot + Meta Ads + Obsidian

#### Fluxo:
```
Validação → PRD/MVP → Landing Page → Criativos → Pré-lançamento → Lançamento → Scale
    ↓          ↓           ↓             ↓            ↓               ↓           ↓
  idea-    launch-     marketing-     orshot     hormozi-leads    Product     meta-ads
validator  planner     writer                                     Hunt        regional
```

1. **Validação brutal** (`idea-validator`) → Saturação mercado, viabilidade solo builder, demanda real
2. **PRD executável** (`launch-planner`) → Roadmap 4 semanas + DB schema + Tech stack (Next.js/Supabase)
3. **Landing page copy** (`marketing-writer`) → Headlines/Features/Pricing/CTAs focados em benefícios
4. **Design landing** (`product-designer` + `scripts/orshot/generate_image.py`) → Mockups profissionais + OG images
5. **Apresentação demo** (`visual-explainer`) → HTML interativo mostrando produto (para vídeo explicativo)
6. **Copy lançamento** (`hormozi-leads`) → Product Hunt / Emails / Twitter threads
7. **Thumbnails YouTube** (`youtube-thumbnailv2`) → 5 variações para vídeo demo
8. **Campanha pré-launch** (`scripts/meta-ads/create_campaign.py`) → Waitlist + early access
9. **Product Hunt launch** (manual + `marketing-writer`) → Copy otimizado + imagens Orshot
10. **Retargeting** (`scripts/meta-ads/create_adset.py`) → Nurture leads que visitaram mas não converteram
11. **Knowledge Base** (`obsidian-organizer`) → Tracking feedback/features/bugs

**Tempo Total:** 25-30 dias (incluindo dev)
**ROI:** Validação economiza 80h dev / Primeiros $1k MRR em 14 dias / Product Hunt top 5 aumenta 300% tráfego

---

### Workflow 6: Reaproveitamento Conteúdo (Content Repurposing Machine)

**Problema:** Maximizar ROI de cada piece de conteúdo distribuindo em 10+ formatos/plataformas
**Stack:** Estudar Video + JSON2Video + Batch Generate + Instagram + TikTok + WhatsApp + Obsidian

#### Fluxo:
```
Vídeo original → Transcrição → Decomposição → Geração Massiva → Distribuição → Tracking
       ↓             ↓             ↓                ↓                 ↓            ↓
   YouTube     estudar-video  army-of-agents  batch_generate    scripts/*   obsidian-
                                                                             organizer
```

1. **Input original** (vídeo YouTube/podcast de 30-60min)
2. **Transcrição + Análise** (`estudar-video`) → Texto completo + insights + classificação
3. **Decomposição estratégica** (`army-of-agents`):
   - Pesquisador → Identifica 10-15 soundbites virais
   - Copywriter → Hooks para cada formato
   - Diretor → Sequência publicação otimizada
4. **Geração paralela massiva**:
   - 10 imagens quote (`scripts/image-generation/batch_generate.py`)
   - 5 vídeos curtos (`json2video`) → Legendas automáticas + audiogramas
   - 3 carrosséis educativos (Canva via MCP)
   - 1 thread Twitter (manual com copy `marketing-writer`)
5. **Distribuição automática**:
   - Instagram: 10 posts (`scripts/instagram/publish_post.py`)
   - Reels: 5 vídeos (`scripts/instagram/publish_reel.py`)
   - Stories: 15 frames (`scripts/instagram/publish_story.py`)
   - WhatsApp Status: broadcast 3 melhores
6. **Agendamento inteligente** (`scheduling-system/schedule_whatsapp.py`) → 1 piece/dia por 30 dias
7. **Tracking performance** (`obsidian-organizer`) → Qual formato/plataforma performou melhor

**Tempo Total:** 2-3h (de 1 vídeo para 30+ pieces)
**ROI:** 1 vídeo → 30 dias de conteúdo / Custo por piece cai 90% / Alcance 5-8x maior

---

### Workflow 7: Orçamento Profissional High-Ticket (Vendas Complexas)

**Problema:** Fechar vendas B2B/high-ticket com propostas que justificam valor absurdo
**Stack:** Orcamento Profissional + 100M Offers + Orshot + Visual Explainer + WhatsApp + Obsidian

#### Fluxo:
```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Discovery   │→ │  Cálculo ROI │→ │  Apresentação│→ │   Follow-up  │
│   (Manual)   │   │  Automático  │   │  Interativa  │   │  Programado  │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

1. **Análise recursos** (`orcamento-profissional`) → Escaneia scripts/skills disponíveis
2. **Cálculo valor** (`100m-offers` framework) → Preço baseado em VALOR não tempo (Value Equation)
3. **Cenários ROI** (skill gera 3 cenários) → Conservador/Realista/Otimista com matemática real
4. **Ancoragem Hormozi** (skill aplica) → Preço alto primeiro → desconto estratégico
5. **Mockups profissionais** (`scripts/orshot/generate_image.py`) → Visualização resultado final
6. **Apresentação HTML** (skill gera) → Interativa, responsiva, profissional (sem slides PDF chatos)
7. **Envio WhatsApp** (`scripts/whatsapp/send_media.py`) → Link apresentação + mensagem contextual
8. **Follow-up sequencial** (`scheduling-system/schedule_whatsapp.py`) → Dia 3/7/14 (não antes)
9. **Objeções database** (`obsidian-organizer`) → Registra objeções comuns + respostas efetivas

**Tempo Total:** 30-45min/proposta (vs 3-5h manual)
**ROI:** 60-80% aumento taxa fechamento / Preços 2-3x maiores aceitos / Posicionamento premium

---

### Workflow 8: Sistema Referrals Automatizado (Growth Loop)

**Problema:** Transformar clientes em promotores ativos gerando referrals qualificados continuamente
**Stack:** WhatsApp + Hormozi Leads + Batch Generate + Instagram + Obsidian + Orshot

#### Fluxo:
```
Cliente feliz → Incentivo → Materiais → Compartilhamento → Tracking → Recompensa
      ↓            ↓           ↓              ↓              ↓            ↓
  Pós-venda  hormozi-leads  batch_gen    whatsapp-helper  obsidian   whatsapp
                                                          -organizer
```

1. **Trigger automático** (7 dias pós-compra) → WhatsApp mensagem personalizada
2. **Copy irresistível** (`hormozi-leads`) → Lead Getter: "Indique 3 amigos → ganhe X"
3. **Kit referral visual**:
   - 5 imagens share (`scripts/image-generation/batch_generate.py`)
   - 3 templates Stories (`scripts/orshot/batch_generate.py`)
   - 1 vídeo depoimento (manual + `json2video` para legendas)
4. **Envio automatizado** (`scripts/whatsapp/send_media.py`) → Kit completo + link tracking
5. **Landing page referral** (manual) → UTM personalizado por cliente
6. **Instagram amplificação** (`scripts/instagram/publish_carousel.py`) → Repost melhores depoimentos
7. **Tracking granular** (`obsidian-organizer`) → Dashboard:
   - Quem indicou quem
   - Taxa conversão por indicador
   - Lifetime value de referrals
8. **Gamificação** (manual logic) → Leaderboard mensal + prêmios escalonados
9. **Recompensas automáticas** (`scripts/whatsapp/send_message.py`) → Confirmação instantânea quando referral converte

**Tempo Total:** 3h setup inicial + automação perpétua
**ROI:** CAC de referrals 70-90% menor / LTV 2-3x maior / Crescimento exponencial orgânico (cada cliente traz 1.5-3 novos)

---

### Workflow 9: Extração Competitiva Inteligente (Market Research)

**Problema:** Entender profundamente concorrentes e identificar oportunidades não-óbvias
**Stack:** Instagram Scraper + TikTok API + Twitter Scraper + xAI Search + 100M Offers + Army of Agents + Obsidian

#### Fluxo:
```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Extração   │→ │   Análise    │→ │   Insights   │→ │  Ação Plan   │
│ Multi-Canal  │   │ Multi-Agente │   │  Estratég.   │   │  Executável  │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

1. **Scraping massivo paralelo**:
   - Instagram (`scripts/instagram-scraper/scrape_user_posts.py`) → 200+ posts top concorrentes
   - TikTok (`scripts/tiktok/get_user_info.py`) → Vídeos virais + hashtags
   - Twitter (`scripts/twitter/scrape_profile.py`) → Narrativa/posicionamento
2. **Monitoramento notícias** (`scripts/search/xai_news.py`) → Movimentações recentes (funding, features, partnerships)
3. **Análise multi-perspectiva** (`army-of-agents`):
   - Pesquisador → Padrões de conteúdo/frequência
   - Copywriter → Tom de voz/hooks/CTAs
   - Crítico Hormozi → Ofertas (Value Equation)
   - Diretor → Gaps estratégicos
4. **Framework ofertas** (`100m-offers`) → Comparar Grand Slam Offer vs concorrentes
5. **Síntese executável** (Army orchestrator) → 3-5 oportunidades high-impact
6. **Knowledge Base** (`obsidian-organizer`) → Dashboard competitivo atualizado

**Tempo Total:** 3-4h (análise completa)
**ROI:** Identificação de gaps que concorrentes levaram meses para perceber / Posicionamento único data-driven

---

### Workflow 10: Campanha de Influência Local (Small Business)

**Problema:** Pequeno negócio quer viralizar localmente e captar clientes próximos
**Stack:** Google Maps + Instagram Scraper + Hormozi Leads + WhatsApp + Meta Ads + TikTok

#### Fluxo:
```
Mapeamento → Análise → Copy → Criação → Campanha → Outreach → Monitoramento
     ↓          ↓        ↓        ↓          ↓          ↓            ↓
  GMaps     IG Scraper hormozi  batch_     meta-ads  whatsapp    obsidian-
                       -leads  generate               helper     organizer
```

1. **Mapeamento concorrência** (`scripts/scraping/google_maps_batch.py`) → 50-100 negócios similares (raio 5km)
2. **Análise social** (`scripts/instagram-scraper/scrape_user_profile.py`) → Perfis IG concorrentes (engajamento, posts, tom)
3. **Identificação gaps** (manual) → O que concorrentes NÃO estão fazendo
4. **Copy irresistível** (`hormozi-leads`) → Hooks locais + Lead Getters (descontos, eventos, workshops)
5. **Criativos visuais** (`scripts/image-generation/batch_generate.py`) → 10 variações com local landmarks
6. **Campanha raio** (`scripts/meta-ads/meta_ads_regional_campaign.py`) → Raio 3-10km + lookalike
7. **Conteúdo TikTok** (manual + `json2video`) → 3-5 vídeos virais/semana (behind-the-scenes, clientes felizes)
8. **Outreach influenciadores micro** (`scripts/whatsapp/send_message.py`) → Parcerias locais (500-5k followers)
9. **Promoções relâmpago** (`scripts/instagram/publish_story.py`) → Stories urgentes (24h)
10. **Tracking geográfico** (`obsidian-organizer`) → Mapa mental leads por bairro

**Tempo Total:** 4-6h/semana
**ROI:** 5-10x ROAS em campanha local / 200-500% crescimento IG em 90 dias / Viralizações locais orgânicas

---

## 📊 RESUMO DE IMPACTO

| Workflow | Setup | ROI Médio | Aplicação |
|----------|-------|-----------|-----------|
| 1. E-commerce Turbo | 8-12h | Primeiras vendas <48h | Lançamentos rápidos |
| 2. Leads B2B | 3-5h | Lead $0.50 vs $15-50 | Prospecção massiva |
| 3. YouTube Multi | 6-10h/vídeo | 1 vídeo → 30 pieces | Criadores conteúdo |
| 4. Imobiliário | 2h + 15min/dia | 70% redução tempo | Imobiliárias/Corretores |
| 5. Produto Digital | 25-30 dias | $1k MRR em 14d | Infoprodutos/SaaS |
| 6. Repurposing | 2-3h | 30 dias conteúdo | Criadores/Agências |
| 7. High-Ticket | 30-45min | 60-80% fechamento | Vendas complexas B2B |
| 8. Referrals | 3h setup | CAC -70-90% | Qualquer com clientes |
| 9. Market Research | 3-4h | Gaps estratégicos | Qualquer negócio |
| 10. Influência Local | 4-6h/sem | 5-10x ROAS | Small business físico |

---

**v1.0** | **2025-11-05** | **Gerado por Army of Agents**
