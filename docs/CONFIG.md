# ⚙️ Configurações e Detalhes Técnicos

## 📡 APIs Configuradas

### Principais
- **OpenRouter:** Claude Haiku/Sonnet 4.5
- **OpenAI:** GPT-4o, Whisper, DALL-E 3
- **Gemini:** 2.5 Flash (via Nano Banana)
- **xAI:** Grok (requer Python 3.11+)
- **ElevenLabs:** TTS voz Michele
- **Kie.ai:** GPT-4o Image, Sora 2

### Integrações
- **Instagram API:** v24.0 (posts, stories, reels)
- **Meta Ads API:** v24.0 (campanhas, públicos)
- **Evolution API:** WhatsApp instância lfimoveis
- **Apify:** Web scraping ($2.30/1000 itens)
- **RapidAPI:** Transcrição YouTube
- **Nextcloud:** Upload permanente
- **Upstash Redis:** Memória chatbot
- **Chatwoot:** Atendimento integrado

---

## 🔧 Configurações Técnicas

### Modelos Padrão
- **Imagens:** Nano Banana (Gemini 2.5 Flash)
- **Vídeos:** Sora 2 portrait (Stories/Reels)
- **Áudio:** ElevenLabs voz Michele
- **Transcrição:** Whisper API

### Portas e Serviços
| Serviço | Porta | Localização |
|---------|-------|-------------|
| Bot Imóveis | 5001 | whatsapp-chatbot/ |
| Middleware Imóveis | 5002 | whatsapp-chatbot/ |
| Bot Automaia | 5003 | whatsapp-chatbot-carros/ |
| Middleware Automaia | 5004 | whatsapp-chatbot-carros/ |
| Ngrok | Auto | Configurado no script |

### Custos Aproximados
- **Vídeo YouTube:** ~$0.006/vídeo
- **Imagem Nano Banana:** ~$0.001/imagem
- **Vídeo Sora:** ~$0.05/vídeo
- **Instagram Scraping:** $2.30/1000 itens
- **WhatsApp Evolution:** Grátis (self-hosted)

---

## 📝 Detalhes de Implementação

### Upload Rápido
- **Pasta local:** `~/Pictures/upload/`
- **Auto-delete:** Após upload bem-sucedido
- **Links:** Permanentes (sem expiração)
- **Comando:** `upload_rapido.py --from-local`

### WhatsApp Mídia
- **Regra absoluta:** Apenas URLs públicas
- **Formato:** `--url https://...`
- **Proibido:** --file (removido), base64, arquivos locais

### Batch Generation
- **Obrigatório para:** 2+ itens
- **APIs suportadas:** Nano Banana, GPT-4o, Sora
- **Comando:** `batch_generate.py --api [api] "p1" "p2"`

### Obsidian Integration
- **Skill obrigatória:** obsidian-organizer
- **Estrutura:** `📺 Vídeos/`, `💡 Anotações/`, `📋 Tarefas/`
- **Formato datas:** DD/MM/YYYY (brasileiro)

---

## 🛠️ Troubleshooting Comum

### Python Versions
- **Padrão:** Python 3.x
- **xAI (Grok):** Requer Python 3.11+
- **Comando:** `python3.11` para xAI

### Git Backup
- **Repo:** github.com/dipaulavs/ClaudeCode-Workspace-2025
- **Visibilidade:** PRIVADO
- **Backup:** `/bk` (add + commit + push)
- **Restore:** `/cbk` (listar e restaurar)

### Formatos WhatsApp
- **Telefone:** DDI+DDD+Número (ex: 5531980160822)
- **Mídia:** Sempre URL pública
- **Mensagens:** Markdown suportado

### Rate Limits
- **Instagram API:** 200/hora
- **Meta Ads:** 200/hora
- **Evolution:** Sem limite
- **Nano Banana:** 1000/dia

---

## 📊 Workflows Detalhados

### Adicionar Imóvel (Bot WhatsApp)
1. Usuário fornece descrição, preço, FAQ
2. Colocar fotos em `~/Pictures/upload/`
3. Executar upload Nextcloud
4. Criar estrutura (base.txt, faq.txt)
5. Atualizar links.json
6. Bot reconhece após `/reload`

### Criar Novo Chatbot
**Opção A:** Mesma conta Chatwoot (2-3 clientes)
**Opção B:** Conta separada (4-10 clientes)
**Opção C:** Multi-tenant framework (10+ clientes)

### Estudar Vídeo YouTube
1. Skill `estudar-video` (automática)
2. Transcrever com Whisper
3. Analisar com Claude
4. Salvar em `📺 Vídeos/` no Obsidian
5. Custo: ~$0.006 | Tempo: ~3min

---

## 🔑 Variáveis de Ambiente

```bash
# APIs Principais
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
ELEVENLABS_API_KEY=...

# Meta/Instagram
META_APP_ID=...
META_APP_SECRET=...
META_ACCESS_TOKEN=...
INSTAGRAM_ACCOUNT_ID=...

# WhatsApp
EVOLUTION_API_URL=https://...
EVOLUTION_API_KEY=...
EVOLUTION_INSTANCE=lfimoveis

# Outros
NEXTCLOUD_URL=...
NEXTCLOUD_USER=...
NEXTCLOUD_PASS=...
UPSTASH_REDIS_URL=...
CHATWOOT_URL=...
```

---

**Última atualização:** 2025-11-05
**Documento auxiliar do CLAUDE.md v7.0**