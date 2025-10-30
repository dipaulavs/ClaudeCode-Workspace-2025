# 🤖 Claude Code Workspace

Workspace com ferramentas de IA pré-configuradas.

## 📁 Estrutura

```
ClaudeCode-Workspace/
├── agentes/            # Agentes especializados
│   ├── especificidade33/       # Conteúdos virais Instagram
│   └── openrouter/             # Agentes via OpenRouter API
├── tools/              # Scripts Python de IA
├── config/             # Configurações
├── logs/               # Logs
├── requirements.txt    # Dependências (requests já instalado)
├── setup.sh           # Instalação
└── iniciar.sh         # Boas-vindas
```

## 🤖 Sistema de Agentes

Agentes especializados com frameworks específicos em arquivos `.md`.

### Uso:
```
"Ative o agente [nome] para [tarefa]"
```

### Agentes Disponíveis:
- **especificidade33** (`agentes/especificidade33/`) - Conteúdos virais Instagram com 33 formatos

### Criar Novo Agente:
1. `mkdir agentes/meu-agente`
2. Adicione arquivos `.md` com instruções/frameworks
3. Ative: "Ative o agente meu-agente para [tarefa]"

---

## 🔌 Agentes via OpenRouter

Subagentes especializados que economizam tokens do Claude Code. Instruções ficam armazenadas localmente e são enviadas apenas para a API da OpenRouter.

**Uso:**
```bash
python3 tools/agent_openrouter.py <agente> "seu input" [--model MODEL] [--temp 0-1]
```

**Agentes:**
- `copywriter-vendas` - Copy persuasivo e textos de vendas
- `analista-negocios` - Análise estratégica e business intelligence

**Modelos disponíveis:** Claude Haiku/Sonnet 4.5 (padrão), GPT-4o/5, Gemini 2.5 Pro, Grok 4, DeepSeek, GLM 4.6

**Exemplos:**
```bash
# Usa Claude Haiku 4.5 (padrão)
python3 tools/agent_openrouter.py copywriter-vendas "Crie headline para curso de Python"

# Escolher modelo específico
python3 tools/agent_openrouter.py analista-negocios "Analise viabilidade" --model openai/gpt-4o

# Listar agentes
python3 tools/agent_openrouter.py --list
```

**Docs completa:** `agentes/openrouter/README.md`

---

## 🔄 Workflows

Automações completas que executam múltiplas etapas sequencialmente, combinando agentes e ferramentas.

**Uso:**
```
Ative o workflow [nome] para [input]
```

**Workflows disponíveis:**
- `headline-to-image` - Gera imagens com headlines virais automaticamente (nicho → headlines → imagens)

**Criar workflow:**
1. Crie arquivo `.md` em `workflows/`
2. Defina: objetivo, inputs, etapas (ferramenta, ação, output)
3. Ative: "Ative o workflow nome para [input]"

**Docs completa:** `workflows/README.md`

---

## 🚀 Setup Inicial

```bash
bash setup.sh  # Apenas primeira vez
```

## 🛠️ Ferramentas (tools/)

Todas salvam em `~/Downloads` com timestamp automático.

### Geração de Imagens

**GPT-4o Image** (Kie.ai):
```bash
python3 tools/generate_image.py "prompt" [--variants 1|2|4] [--enhance]
python3 tools/generate_image_batch_gpt.py "p1" "p2" [--variants N] [--enhance]
```
- Portrait 2:3, variações, refinamento de prompt
- Batch: processamento paralelo

**Nano Banana** (Gemini 2.5 Flash):
```bash
python3 tools/generate_image_nanobanana.py "prompt" [--format PNG|JPEG]
python3 tools/generate_image_batch.py "p1" "p2" [--format PNG|JPEG]
```
- Portrait 2:3, hiper-realismo, física consciente
- Batch: processamento paralelo

**Editor Nano Banana**:
```bash
python3 tools/edit_image_nanobanana.py --url "URL" "edit prompt" [--format PNG|JPEG] [--size RATIO] [--expire-days N]
python3 tools/edit_image_nanobanana.py arquivo.jpg "edit prompt"  # Upload automático Nextcloud
```
- Proporções: 1:1, 9:16, 16:9, 3:4, 4:3, 3:2, 2:3, 5:4, 4:5, 21:9, auto
- Arquivo local: upload automático para Nextcloud com link temporário

### Geração de Áudio

**ElevenLabs TTS**:
```bash
python3 tools/generate_audio_elevenlabs.py "texto" [--voice ID|felipe] [--model ID] [--format mp3_low|medium|high|ultra|pcm] [--stability 0-1] [--similarity 0-1] [--output arquivo.mp3] [--list-voices]
python3 tools/generate_audio_batch_elevenlabs.py "t1" "t2" [--voice ID] [--model ID] [--delay SECS]
```
- Vozes padrão: Michele (QQFzOTqaZ9W1XGSTWyBw), felipe (3QlvO7Xt2e9OCfetPOd8)
- Modelos: eleven_v3 (padrão, 70+ idiomas), eleven_turbo_v2_5, eleven_multilingual_v2, eleven_flash_v2_5
- Batch: processamento sequencial com numeração automática

### Geração de Vídeos

**Sora 2** (OpenAI via Kie.ai):
```bash
python3 tools/generate_video_sora.py "prompt" [--aspect portrait|landscape|square] [--watermark]
python3 tools/generate_video_batch_sora.py "v1" "v2" [--aspect RATIO] [--watermark]
```
- ~15s, portrait padrão, marca d'água removida por padrão
- Batch: processamento paralelo (2-5min para todos)
- Tempo individual: 2-5min/vídeo

### Extração de Conteúdo

**Transcrição Universal** (via RapidAPI):
```bash
python3 tools/transcribe_universal.py "URL" [--lang IDIOMA] [--task transcribe|translate]
```
- Transcreve vídeos de YouTube, TikTok, Instagram, LinkedIn, X/Twitter, Vimeo
- Suporta URLs diretas de áudio/vídeo
- Idiomas: pt (português), en (inglês), es (espanhol), etc.
- Salva transcrição em TXT e JSON, exibe no terminal

**Como usar:**

*Para vídeos online (YouTube, TikTok, etc.):*
```bash
# Cole a URL diretamente
python3 tools/transcribe_universal.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang pt
```

*Para arquivos de áudio/vídeo locais (sempre em ~/Downloads):*
```bash
# 1. Upload para Nextcloud (gera URL pública)
python3 tools/upload_to_nextcloud.py "~/Downloads/seu_audio.m4a" --days 7

# 2. Transcrever usando a URL gerada
python3 tools/transcribe_universal.py "URL_DO_NEXTCLOUD" --lang pt
```

**Atalho para YouTube:** Cole o link do vídeo para transcrever e resumir automaticamente

**Instagram - Posts/Carrosséis** (via Apify):
```bash
python3 tools/extract_instagram.py "URL" [--limit N]
```
- Extrai imagens e legendas de posts/carrosséis
- Suporta URLs de posts ou perfis
- Salva imagens, legendas, metadados (likes, comentários)
- Cria pasta com timestamp em ~/Downloads

**Instagram - Reels Transcrição** (via Apify + OpenAI):
```bash
python3 tools/transcribe_instagram_reels.py "URL_REELS" [--model MODEL]
```
- Transcreve automaticamente áudio de Reels
- Modelos: gpt-4o-mini-transcribe (padrão), gpt-4o-transcribe
- Salva transcrição em TXT e JSON completo
- Exibe transcrição no terminal

**TikTok - Transcrição** (via Apify + OpenAI):
```bash
python3 tools/transcribe_tiktok.py "URL_TIKTOK" [--model MODEL]
```
- Transcreve automaticamente áudio de vídeos do TikTok
- Modelos: whisper-1 (padrão), gpt-4o-mini-transcribe
- Salva transcrição em TXT e JSON completo
- Exibe transcrição no terminal

### Upload de Imagens

**Nextcloud** (media.loop9.com.br):
```bash
python3 tools/upload_to_nextcloud.py imagem.jpg [--days N] [--permanent] [--folder PASTA]
```
- Gera links públicos diretos (terminam em .jpg)
- Expiração padrão: 24 horas
- Servidor: media.loop9.com.br, usuário: dipaula, pasta: claude-code

---

## 🎨 Dicas Rápidas

**Imagens**: Seja específico (detalhes, estilo, iluminação, cores). Use `--enhance` para complexidade.
- Arquivos são nomeados automaticamente em **português** com base no prompt
- Formato: `descricao_do_conteudo_xyz1.png` (código aleatório de 4 chars)
- Exemplo: `mulher_cyberpunk_oculos_a7f2.png`, `por_do_sol_montanhas_k9x3.png`

**Áudio**: Use pontuação para pausas, escreva números por extenso, mp3_ultra para máxima qualidade.

**Vídeos**: Descreva movimento, câmera, atmosfera e iluminação.

---

## 🔧 Manutenção

**Adicionar script**: Coloque em `tools/`, adicione dependências em `requirements.txt`, rode `bash setup.sh`.

**Troubleshooting**:
- Module not found: `pip3 install --user requests`
- Script não executa: `chmod +x tools/*.py *.sh`

---

**Docs**: [Kie.ai](https://docs.kie.ai) | [Claude Code](https://claude.com/claude-code)
