# 🤖 Claude Code - Workspace Configuration

**Auto-load:** Este arquivo é carregado automaticamente e SOBRESCREVE comportamentos padrão do Claude Code.

---

## 📝 REGRAS DE EDIÇÃO DESTE ARQUIVO (OBRIGATÓRIO)

### ⚠️ ANTES DE ADICIONAR/EDITAR CONTEÚDO NO CLAUDE.md

**PRINCÍPIO:** CLAUDE.md é um **índice navegável**, NÃO uma documentação completa.

### ✅ O QUE INCLUIR (permitido):

1. **Regras de comportamento** → Instruções críticas de como Claude Code deve agir
2. **Links para índices** → 1 linha por recurso (Skills, Templates, Ferramentas, KBs)
3. **Quick Actions** → Comandos essenciais (formato resumido)
4. **Estrutura workspace** → Visão geral compacta
5. **APIs configuradas** → Lista simples

### ❌ O QUE NÃO INCLUIR (proibido):

1. ❌ **Tabelas inline detalhadas** → Vai para índices em docs/
2. ❌ **Documentação de skills** → Vai para `.claude/skills/INDEX.md`
3. ❌ **Mapa de ações completo** → Vai para `docs/MAPA_ACOES.md`
4. ❌ **Regras de decisão** → Vai para `docs/REGRAS_DECISAO.md`
5. ❌ **Knowledge Bases detalhadas** → Vai para `docs/KNOWLEDGE_BASES.md`

### 📏 LIMITES RÍGIDOS:

- **Regras comportamento:** Máx 15 linhas por regra
- **Arquivo total:** Máx 400 linhas
- **Índices:** 1 linha de link por recurso

### 🔍 CHECKLIST antes de salvar edições:

- [ ] Removi tabelas inline?
- [ ] Usei links para índices?
- [ ] Mantive só regras críticas?
- [ ] Total < 400 linhas?

---

## 🚨 REGRAS DE COMPORTAMENTO (PRIORIDADE MÁXIMA)

### 0️⃣ Modo Conciso (Comunicação)

**⚠️ PREFERÊNCIA DO USUÁRIO:** Respostas ULTRA-CURTAS. Zero fluff. Zero repetição.

**Estrutura:**
1. O que vou fazer (1 linha)
2. Executo
3. Resultado (1-2 linhas)

**Proibido:**
- ❌ Repetir o que usuário pediu
- ❌ Explicações longas desnecessárias
- ❌ Contexto óbvio

**Exceções:**
- ✅ Erros críticos (explicar o problema)
- ✅ Usuário pede detalhes explicitamente
- ✅ Decisões complexas que precisam clarificação

---

### 1️⃣ Confirmação Obrigatória

**SEMPRE que usuário pedir qualquer ação que crie/modifique arquivos:**

**Passo 1 - PLANEJAR:**
- Apresentar plano objetivo (3-5 itens)
- Mostrar quais arquivos serão criados/modificados
- Indicar comandos que serão executados

**Passo 2 - AGUARDAR:**
- Não executar até usuário confirmar
- Aceitar ajustes no plano

**Passo 3 - EXECUTAR:**
- Só após confirmação explícita

**Exceções** (executar direto sem plano):
- Leitura de arquivos (Read, Grep, Glob)
- Busca/pesquisa
- Comandos informativos (ls, git status)
- Templates únicos e diretos (ex: enviar mensagem WhatsApp)
- Estudo de vídeos YouTube (workflow automático)

---

### 2️⃣ Preferência por Templates

**SEMPRE verificar se existe template antes de criar código novo.**

**Ver índice completo:** `docs/MAPA_ACOES.md` (71+ templates)

**NUNCA:**
- ❌ Criar scripts descartáveis/temporários
- ❌ Criar arquivos `test_*.py` quando existe template
- ❌ Usar ferramentas de `tools/` diretamente (usar templates de `scripts/`)

---

### 3️⃣ Organização de Arquivos

**Ao criar QUALQUER novo recurso:**

1. ✅ **Nunca criar arquivos soltos na raiz**
2. ✅ **Usar estrutura existente:**
   - Scripts Python → `tools/` (ferramenta low-level) ou `scripts/` (template)
   - Documentação → `docs/` (na subpasta apropriada)
   - Configs → `config/` (com nome descritivo)
   - Projetos completos → Pasta própria na raiz

---

### 4️⃣ Auto-Documentação de Novos Recursos (OBRIGATÓRIO)

**Após criar o recurso, SEMPRE executar:**

1. ✅ Documentar no README da categoria
2. ✅ Registrar no índice apropriado (`docs/MAPA_ACOES.md`, `.claude/skills/INDEX.md`, etc)
3. ✅ Manter organização consistente
4. ✅ Resumo final ao usuário

---

### 5️⃣ TodoWrite Obrigatório

**Usar quando:**
- Tarefa com 3+ etapas
- Múltiplos arquivos envolvidos
- Usuário lista múltiplas ações

**Não usar quando:**
- Ação única trivial
- Leitura simples
- Template direto

---

### 6️⃣ Workflow Automático: Estudar Vídeo YouTube

**GATILHO:** Usuário diz "Estuda esse vídeo: [URL]" ou fornece URL YouTube

**MÉTODO:** Claude Code Skill `estudar-video` (model-invoked, totalmente automática)

**WORKFLOW:** Transcrever (Whisper) → Analisar (Claude) → Salvar em `📺 Vídeos/` (obsidian-organizer)

**Custo:** ~$0.006/vídeo | **Tempo:** ~3min | **Regras:** ❌ Sem confirmação

---

### 7️⃣ WhatsApp Mídia: SEMPRE URL Pública

**REGRA ABSOLUTA:** Evolution API aceita APENAS URLs públicas.

**SEMPRE:**
- ✅ Usar `--url` com link público (http:// ou https://)
- ✅ URLs vêm nas respostas das APIs (Nano Banana, GPT-4o, Sora)

**NUNCA:**
- ❌ `--file` foi REMOVIDO do script (não existe mais)
- ❌ Arquivos locais não funcionam
- ❌ Base64 não funciona

---

### 8️⃣ Auto-Correção de Scripts (OBRIGATÓRIO)

**GATILHO:** Script executado retorna erro → Corrijo o erro → Script funciona

**SEMPRE após corrigir erro:**
1. ✅ Atualizar o script para prevenir o erro no futuro
2. ✅ Melhorar validação (adicionar checks, avisos)
3. ✅ Remover informações confusas (código obsoleto, docs enganosas)
4. ✅ Atualizar documentação (README, docstrings, comentários)

**Objetivo:** Erro só acontece UMA vez. Scripts melhoram continuamente.

---

### 9️⃣ Priorização de Skills (OBRIGATÓRIO)

**GATILHO:** Usuário menciona ideia/dúvida/implementação de forma genérica

**SEMPRE ativar `adaptive-mentor` PRIMEIRO quando usuário disser:**
- "To com uma ideia..." (qualquer contexto)
- "Quero criar/fazer/implementar..." (sem PRD/validação explícita)
- "Preciso de um plano para..." (contexto técnico/estratégico)
- "Como fazer..." ou "Me ajuda com..." (genérico)
- "Não sei como..." ou "Qual a melhor forma..."

**Exceções** (usar outras skills):
- Usuário menciona explicitamente: "valida essa ideia" → `idea-validator`
- Usuário menciona explicitamente: "cria PRD" ou "MVP" → `launch-planner`
- Usuário pede: "design de UI" ou "tela de login" → `product-designer`
- Usuário pede: "copy de marketing" ou "landing page" → `marketing-writer`

---

### 🔟 Verificação Obrigatória Antes de Responder

**GATILHO:** Qualquer solicitação do usuário (início de conversa ou durante)

**ANTES de responder, executar checklist:**
1. ✅ Existe Claude Skill? → Ver `.claude/skills/INDEX.md`
2. ✅ Existe template/script? → Ver `docs/MAPA_ACOES.md`
3. ✅ Existe regra de decisão? → Ver `docs/REGRAS_DECISAO.md`
4. ✅ Só então responder com base no que existe

**Exceções:** Perguntas conceituais, leitura de arquivos, comandos informativos.

---

### 1️⃣1️⃣ Links YouTube: SEMPRE Transcrever

**GATILHO:** Usuário envia link do YouTube (qualquer contexto)

**SEMPRE executar:**
```bash
python3 scripts/extraction/transcribe_video.py "URL_DO_YOUTUBE"
```

**NUNCA:**
- ❌ Tentar WebFetch em links YouTube (não funciona)
- ❌ Pedir ao usuário para descrever o conteúdo
- ❌ Ignorar o link

---

### 1️⃣2️⃣ Obsidian: SEMPRE Usar obsidian-organizer

**GATILHO:** Usuário pede para anotar, salvar, registrar algo no Obsidian

**REGRA ABSOLUTA:** NUNCA criar arquivos diretamente no Obsidian. SEMPRE usar skill `obsidian-organizer`.

**SEMPRE:**
- ✅ Invocar skill `obsidian-organizer` (automática)
- ✅ Skill decide local e formato correto
- ✅ Sistema minimalista: `📺 Vídeos/`, `💡 Anotações/`, `📋 Tarefas/`

**NUNCA:**
- ❌ Usar scripts Python antigos (quick_note.py, capture_idea.py, etc) - OBSOLETOS
- ❌ Criar arquivos diretamente com Write tool sem invocar skill
- ❌ Usar estrutura antiga "00 - Inbox", "09 - YouTube Knowledge"

---

### 1️⃣3️⃣ Orquestração Inteligente: builder-orchestrator

**GATILHO:** Usuário diz "criar ferramenta/skill/workflow/implementar..."

**SEMPRE ativar `builder-orchestrator` PRIMEIRO quando usuário disser:**
- "Quero criar uma ferramenta..."
- "Preciso de um workflow..."
- "Cria uma skill..."
- "Implementar [funcionalidade]..."
- "Fazer uma campanha de..."

**Comportamento:** Analisa recursos → Identifica paralelização → Apresenta plano → Delega subagentes → Cria skills se necessário

---

### 1️⃣4️⃣ Upload Rápido de Imagens

**GATILHO:** Usuário diz "suba as imagens" / "upload rápido" / "faça upload"

**REGRA ABSOLUTA:** SEMPRE usar `upload_rapido.py --from-local`

**SEMPRE:**
- ✅ Executar `python3 scripts/nextcloud/upload_rapido.py --from-local`
- ✅ Pasta local: `~/Pictures/upload/`
- ✅ Links permanentes (sem expiração)
- ✅ Auto-delete dos arquivos locais após upload

**NUNCA:**
- ❌ Pedir caminho do arquivo
- ❌ Usar upload_to_nextcloud.py ou upload_from_downloads.py
- ❌ Perguntar "qual arquivo?"

---

### 1️⃣5️⃣ Visualização de Processos (OBRIGATÓRIO)

**GATILHO:** Usuário pede explicação/resumo/ideia com múltiplas etapas

**SEMPRE incluir visualização ASCII antes da explicação:**

```
Etapa 1 → Etapa 2 → Etapa 3 → Resultado
   ↓          ↓          ↓
[breve]   [breve]   [breve]
```

**Exemplo:**
```
📺 URL YouTube → 🎤 Whisper → 🤖 Claude → 📝 Obsidian
                 (transcrição)  (análise)   (📺 Vídeos/)
```

---

### 1️⃣6️⃣ Chatbot WhatsApp: Adicionar Imóvel/Criar Novo Bot

**GATILHO:** Usuário diz "adiciona imóvel" ou "cria chatbot para [empresa]"

**WORKFLOW ADICIONAR IMÓVEL:**
1. Usuário fornece: descrição, preço, FAQ, detalhes
2. Usuário coloca fotos em `~/Pictures/upload/`
3. Claude executa: upload Nextcloud → cria estrutura (base.txt, faq.txt, etc) → links.json
4. Bot reconhece automaticamente (reiniciar ou `/reload`)

**CRIAR NOVO CHATBOT (3 opções):**
- **Opção A:** Mesma conta Chatwoot, nova inbox (2-3 clientes)
- **Opção B:** Conta Chatwoot separada (4-10 clientes)
- **Opção C:** Multi-tenant framework (10+ clientes)

**Docs:** `whatsapp-chatbot/FRAMEWORK_COMPLETO_README.md` | `whatsapp-chatbot/INTEGRACAO_FRAMEWORK.md`

---

### 1️⃣7️⃣ Chatbot Automaia (Carros Seminovos)

**EMPRESA:** Automaia - Agência de Carros Seminovos
**LOCALIZAÇÃO:** `whatsapp-chatbot-carros/`

**INICIAR/PARAR:**
```bash
cd whatsapp-chatbot-carros
./INICIAR_COM_NGROK.sh              # Iniciar (ngrok + webhooks automáticos) ✅
./PARAR_BOT_AUTOMAIA.sh && pkill -f ngrok  # Parar
```

**⚠️ SEMPRE usar `INICIAR_COM_NGROK.sh`** - Configura webhooks automaticamente

**PORTAS:** Bot: 5003 | Middleware: 5004
**DOCS:** `whatsapp-chatbot-carros/README.md`

---

## 📚 RECURSOS DISPONÍVEIS (Índices)

**⚠️ SEMPRE consultar índices antes de criar código novo:**

| Recurso | Índice | Total |
|---------|--------|-------|
| **Skills** | `.claude/skills/INDEX.md` | 26 skills |
| **Templates & Workflows** | `docs/MAPA_ACOES.md` | 71+ templates |
| **Ferramentas** | `docs/tools/INDEX.md` | 65+ ferramentas |
| **Knowledge Bases** | `docs/KNOWLEDGE_BASES.md` | 3 KBs |
| **Regras de Decisão** | `docs/REGRAS_DECISAO.md` | 10+ fluxogramas |

---

## ⚡ Quick Actions

### Chatbot WhatsApp (Imóveis)
```bash
bot         # Iniciar Bot V4 + Framework Híbrido
botstop     # Parar
# Logs: whatsapp-chatbot/logs/chatbot_v4.log
```

### Chatbot Automaia (Carros)
```bash
cd whatsapp-chatbot-carros
./INICIAR_COM_NGROK.sh      # Iniciar (ngrok + portas 5003/5004) ✅
./PARAR_BOT_AUTOMAIA.sh && pkill -f ngrok  # Parar
```

### Backup Git
```bash
/bk         # Backup automático (add + commit + push)
/cbk        # Listar e restaurar backups
```
**Repo:** https://github.com/dipaulavs/ClaudeCode-Workspace-2025 (PRIVADO)

### Geração de Conteúdo
```bash
# 1 imagem (Nano Banana)
python3 scripts/image-generation/generate_nanobanana.py "prompt"

# 2+ imagens (BATCH obrigatório)
python3 scripts/image-generation/batch_generate.py --api nanobanana "prompt1" "prompt2"

# 1 vídeo (Sora portrait)
python3 scripts/video-generation/generate_sora.py "prompt"

# 1 áudio (ElevenLabs voz Michele)
python3 scripts/audio-generation/generate_elevenlabs.py "texto"
```

### WhatsApp/Instagram
```bash
# WhatsApp
python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Olá!"

# Instagram
python3 scripts/instagram/publish_post.py --image "foto.jpg" --caption "Legenda"
```

---

## 📁 ESTRUTURA DO WORKSPACE

```
ClaudeCode-Workspace/
├── 📄 CLAUDE.md                 # Config auto-load (este arquivo)
├── 📄 README.md                 # Índice geral
│
├── 📁 .claude/
│   ├── commands/                # /bk, /cbk
│   └── skills/                  # 26 Claude Skills + INDEX.md
│
├── 📁 scripts/                  # 71+ Templates prontos
│   ├── whatsapp/                # 22 templates
│   ├── instagram/               # 6 templates
│   ├── image-generation/        # 6 templates
│   ├── video-generation/        # 2 templates
│   ├── audio-generation/        # 2 templates
│   └── [outras categorias]/
│
├── 📁 tools/                    # 40+ Ferramentas low-level
├── 📁 config/                   # Configurações APIs
├── 📁 docs/                     # Documentação organizada
│   ├── MAPA_ACOES.md            # Índice completo de templates
│   ├── REGRAS_DECISAO.md        # Fluxogramas de decisão
│   ├── KNOWLEDGE_BASES.md       # Índice de KBs
│   └── tools/INDEX.md           # Índice de ferramentas
│
├── 📁 whatsapp-chatbot/         # Bot V4 + Framework Híbrido
├── 📁 whatsapp-chatbot-carros/  # Bot Automaia (Carros)
├── 📁 scheduling-system/        # Agendamento WhatsApp
└── [outros projetos]/
```

---

## 💡 DICAS IMPORTANTES

### Geração de Múltiplos Itens
🚨 **REGRA CRÍTICA:** 2+ itens = SEMPRE usar batch
- Imagens: `batch_generate.py --api nanobanana`
- Vídeos: `batch_generate.py`
- Áudios: `batch_generate.py`

**Ver:** `docs/REGRAS_DECISAO.md`

### Modelos Padrão
- **Imagens:** Nano Banana (Gemini 2.5 Flash)
- **Vídeos:** Sora 2 portrait (Stories/Reels)
- **Áudio:** ElevenLabs voz Michele

### Outros
- **Busca xAI:** Requer Python 3.11+ (usar `python3.11`)
- **WhatsApp:** Formato DDI+DDD+Número (ex: 5531980160822)
- **Instagram Scraping:** Usar `--limit` ($2.30/1000 itens)
- **Obsidian:** Datas em formato brasileiro DD/MM/YYYY

---

## 📖 DOCUMENTAÇÕES COMPLETAS

| Recurso | Localização |
|---------|-------------|
| **README Principal** | `README.md` |
| **Skills (26)** | `.claude/skills/INDEX.md` |
| **Templates (71+)** | `docs/MAPA_ACOES.md` |
| **Ferramentas (65+)** | `docs/tools/INDEX.md` |
| **Knowledge Bases (3)** | `docs/KNOWLEDGE_BASES.md` |
| **Regras Decisão** | `docs/REGRAS_DECISAO.md` |
| **Obsidian** | `docs/tools/obsidian_integration.md` |
| **Chatbot WhatsApp** | `whatsapp-chatbot/README.md` |
| **Meta Ads API** | `docs/meta-ads-api/META_ADS_API_DOCUMENTATION.md` |
| **Instagram API** | `docs/instagram-api/INSTAGRAM_API_DOCUMENTATION.md` |

---

## ⚙️ APIs CONFIGURADAS

- ✅ OpenRouter (Claude Haiku/Sonnet 4.5)
- ✅ OpenAI (GPT-4o, Whisper)
- ✅ Gemini 2.5 Flash (Nano Banana)
- ✅ Instagram API (v24.0)
- ✅ Meta Ads API (v24.0)
- ✅ Evolution API (WhatsApp - instância lfimoveis)
- ✅ xAI (Grok)
- ✅ ElevenLabs (TTS)
- ✅ Kie.ai (GPT-4o Image, Sora)
- ✅ Apify (Scraping)
- ✅ RapidAPI (Transcrição)
- ✅ Nextcloud (Upload)
- ✅ Upstash Redis (Memória chatbot)

---

**Última atualização:** 2025-11-05
**Versão:** 6.0 (26 Skills | 71+ templates | 17 regras | 2 chatbots | Modular)
