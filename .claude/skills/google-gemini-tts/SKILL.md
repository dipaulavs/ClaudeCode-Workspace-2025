---
name: google-gemini-tts
description: Generate realistic conversational voices with Google Gemini TTS. Use when user asks to create voice audio, generate speech, convert text to speech, or wants casual/natural-sounding narration (podcast style, phone conversation, friendly chat). Auto-invokes when user requests voice generation or TTS with natural/casual tone.
---

# Google Gemini TTS - Geração de Voz Conversacional Realista

## Overview

Generate ultra-realistic voice audio with Google Gemini 2.5 TTS that sounds like natural conversation between friends, casual phone calls, or informal podcasts. NOT the robotic "excited announcer" voice - this creates authentic, relaxed, conversational audio with natural pauses and breathing.

## When to Use This Skill

Auto-invoke when user asks for:
- "Gera voz/áudio para..."
- "Converte esse texto em voz"
- "Quero uma narração natural/casual"
- "Tom de podcast informal/conversa entre amigos"
- "Voz realista sem aquele tom de locutor"
- Any TTS request emphasizing natural/casual/conversational tone

## IMPORTANTE: Ajuste Automático de Gênero

**O script ajusta AUTOMATICAMENTE o texto para perspectiva de gênero:**
- Voz feminina (`-g female`): "nervoso" → "nervosa", "empolgado" → "empolgada"
- Sempre use perspectiva correta no texto original
- Exemplos ajustados: cansado/a, preocupado/a, animado/a, estressado/a

## Quick Start

### Basic Usage

```bash
# Gerar voz conversacional casual (masculina, MP3 por padrão)
python3 SCRIPTS/audio-generation/generate_voice.py "Olá, como você está hoje? Espero que esteja tudo bem por aí."

# Voz feminina
python3 SCRIPTS/audio-generation/generate_voice.py "Seu texto aqui" -g female

# Voz NEUTRA/SÉRIA (sem empolgação, como áudio de celular)
python3 SCRIPTS/audio-generation/generate_voice.py "Texto" -g female -t neutral

# Escolher voz específica
python3 SCRIPTS/audio-generation/generate_voice.py "Texto" -v Puck

# Arquivo de saída customizado
python3 SCRIPTS/audio-generation/generate_voice.py "Texto" -o ~/Downloads/audio.mp3

# Formato WAV (ao invés de MP3)
python3 SCRIPTS/audio-generation/generate_voice.py "Texto" -f wav -o ~/Downloads/audio.wav

# Sem adicionar pausas automáticas (modo raw)
python3 SCRIPTS/audio-generation/generate_voice.py "Texto" --no-style
```

### Listar Vozes Casuais

```bash
python3 SCRIPTS/audio-generation/generate_voice.py --list-voices
```

## Core Workflow

### Step 1: Identify Voice Type

**For casual conversation (default - use `-t casual`):**
- 👨 Male: `Puck` (upbeat), `Zubenelgenubi` (casual), `Achird` (friendly)
- 👩 Female: `Callirrhoe` (easy-going), `Aoede` (breezy), `Vindemiatrix` (gentle)

**For neutral/serious tone (use `-t neutral`):**
- 👨 Male: `Charon`, `Kore`
- 👩 Female: `Kore`, `Charon` (tom sério, sem empolgação, como áudio de celular)

**For other styles** (see `references/api_reference.md`):
- Energetic: `Fenrir`, `Leda`
- Soft/Intimate: `Enceladus`, `Achernar`

### Step 2: Process Text

Script automatically adds:
- ✅ `[short pause]` after commas/periods
- ✅ `[short pause]` every 2-3 sentences (breathing)
- ✅ Conversational prompt styling

**To disable auto-styling:**
```bash
python3 SCRIPTS/audio-generation/generate_voice.py "texto" --no-style
```

### Step 3: Generate Audio

```python
# Direct Python usage
import sys
sys.path.append('SCRIPTS/audio-generation')
from generate_voice import generate_casual_voice

generate_casual_voice(
    text="Seu texto aqui",
    output_file="audio.mp3",  # MP3 por padrão
    gender="male",  # or "female"
    tone="casual",  # "casual" (empolgado) ou "neutral" (sério)
    output_format="mp3",  # ou "wav"
    api_key="AIzaSy..."  # or use env GEMINI_API_KEY
)
```

## Advanced Features

### Custom Voice & Model

```bash
# Use Pro model (better emotion control)
python3 SCRIPTS/audio-generation/generate_voice.py "texto" \
    --model gemini-2.5-pro-preview-tts \
    -v Puck

# Flash model (faster, default)
python3 SCRIPTS/audio-generation/generate_voice.py "texto" \
    --model gemini-2.5-flash-preview-tts
```

### Manual Bracket Tags

Add emotion/effects manually in text:

```bash
python3 SCRIPTS/audio-generation/generate_voice.py \
    "Olá! [laughing] Como você está? [short pause] Tudo bem por aí?" \
    --no-style
```

**Available tags** (see `references/api_reference.md` for complete list):
- Vocal: `[laughing]`, `[sighing]`, `[clears throat]`
- Emotion: `[excited]`, `[sarcastic]`, `[empathetic]`
- Style: `[whispering]`, `[speaking slowly]`
- Pause: `[short pause]`, `[PAUSE=2s]`

### Environment Setup

```bash
# Set API key permanently
export GEMINI_API_KEY="AIzaSyAz2Jbiir_0-D3RvQGPk-e5Mb4HzvlerXA"

# Or use .env file
echo 'GEMINI_API_KEY=AIzaSy...' >> .env
```

### Install Dependencies

```bash
pip install google-genai
```

## Output Details

**Audio format (MP3 por padrão):**
- Sample rate: 24kHz
- Bit depth: 16-bit (WAV) / 128kbps (MP3)
- Channels: Mono
- Format: MP3 (default) ou WAV

**File size:**
- MP3: ~300-500 KB per minute
- WAV: ~2-5 MB per minute

**Conversão automática:**
Script converte automaticamente WAV→MP3 usando ffmpeg (se disponível).
Use `-f wav` para manter formato WAV original.

**Custo (pricing):**
- Flash model (default): ~$0.005 USD por áudio (~R$ 0.03)
- Pro model: ~$0.015 USD por áudio (~R$ 0.09)
- Custo é exibido automaticamente ao gerar

## Best Practices

### ✅ Do

1. **Use casual voices**: Puck, Zubenelgenubi, Callirrhoe, Aoede
2. **Let auto-styling work**: Default `[short pause]` injection creates natural flow
3. **Keep texts <500 words**: Break longer content into chunks
4. **Test voices**: Use `--list-voices` to explore options
5. **Combine techniques**: Bracket tags + auto-styling + conversational prompt

### ❌ Don't

1. **Avoid "excited" voices** for casual tone (Fenrir, Leda)
2. **Don't skip pauses**: Remove auto-style only if you manually add pauses
3. **Don't use environmental tags**: `[crowd laughing]` doesn't work (only individual effects)
4. **Don't over-tag**: Too many `[tags]` may be read literally
5. **Don't use robotic voices**: Avoid very short sentences without pauses

## Troubleshooting

### Audio sounds robotic

**Fix:**
- Add more `[short pause]` manually
- Use different voice (try Zubenelgenubi or Callirrhoe)
- Enable auto-styling (remove `--no-style`)

### Tags read literally ("laughing" spoken instead of laugh sound)

**Fix:**
- Break text into smaller chunks
- Reduce tags per sentence
- Use SSML alternative: `<break time="1s"/>`

### API errors

**"API key not valid":**
- Check key starts with `AIza`
- Verify ~39 characters length
- Set `GEMINI_API_KEY` environment variable

**"Rate limit exceeded":**
- Wait 60 seconds (free tier: 10 req/min)
- Space out requests

## Resources

### SCRIPTS/audio-generation/generate_voice.py

Main generation script with:
- Automatic conversational styling (pausas/respirações)
- Gender-based voice selection
- Casual tone prompt engineering
- MP3 output (default) com conversão automática
- Fallback para WAV se ffmpeg não disponível

**Key function:**
```python
generate_casual_voice(
    text: str,
    output_file: str = "output.mp3",
    voice: str = None,  # Auto-select voice based on tone
    gender: str = 'male',
    tone: str = 'casual',  # 'casual' ou 'neutral'
    api_key: str = None,
    model: str = 'gemini-2.5-flash-preview-tts',
    add_style: bool = True,  # Auto-add pauses
    output_format: str = 'mp3'  # 'mp3' ou 'wav'
)
```

### references/api_reference.md

Complete technical reference:
- All 30 voices with personalities
- Bracket tags catalog (emotions/effects/pauses)
- SSML tags supported
- Technical limits & pricing
- Format conversion examples
- Best practices deep dive
- Troubleshooting guide

**Load when:**
- User needs specific voice characteristics
- Wants advanced SSML control
- Needs format conversion help
- Troubleshooting complex issues

### Example Workflows

**Podcast narration:**
```bash
python3 SCRIPTS/audio-generation/generate_voice.py \
    "E aí pessoal, tudo bem? Hoje vamos falar sobre um assunto super interessante..." \
    -g male -v Puck -o podcast_intro.mp3
```

**Friendly conversation:**
```bash
python3 SCRIPTS/audio-generation/generate_voice.py \
    "Oi! Como foi seu dia? [short pause] Conta pra mim, to curioso!" \
    -g female -v Aoede -o conversa.mp3
```

**Áudio neutro (como mensagem de celular):**
```bash
python3 SCRIPTS/audio-generation/generate_voice.py \
    "Oi, acabei de sair da reunião. Vou chegar aí por volta das 18h, tá bom?" \
    -g female -t neutral -o mensagem.mp3
```

**Casual explanation:**
```bash
python3 SCRIPTS/audio-generation/generate_voice.py \
    "Então, basicamente funciona assim... [short pause] Você pega o arquivo, [uhm] processa os dados, e pronto!" \
    -v Zubenelgenubi -o explicacao.mp3
```

## API Key Configuration

**Default API key (pre-configured):**
```
AIzaSyAz2Jbiir_0-D3RvQGPk-e5Mb4HzvlerXA
```

Script will use `GEMINI_API_KEY` env var if set, or accept `--api-key` flag.

## Auto-Correction System

This skill includes an automatic error correction system that learns from mistakes and prevents them from happening again.

### How It Works

When a script or command in this skill fails:

1. **Detect the error** - The system identifies what went wrong
2. **Fix automatically** - Updates the skill's code/instructions
3. **Log the learning** - Records the fix in LEARNINGS.md
4. **Prevent recurrence** - Same error won't happen again

### Using Auto-Correction

**Scripts available:**

```bash
# Fix a problem in this skill's SKILL.md
python3 scripts/update_skill.py <old_text> <new_text>

# Log what was learned
python3 scripts/log_learning.py <error_description> <fix_description> [line]
```

**Example workflow when error occurs:**

```bash
# 1. Fix the error in SKILL.md
python3 scripts/update_skill.py \
    "old incorrect text" \
    "new corrected text"

# 2. Log the learning
python3 scripts/log_learning.py \
    "Error description" \
    "How it was fixed" \
    "SKILL.md:line_number"
```

### LEARNINGS.md

All fixes are automatically recorded in `LEARNINGS.md`:

```markdown
### 2025-01-07 - Error description

**Problema:** What went wrong
**Correção:** How it was fixed
**Linha afetada:** SKILL.md:97
**Status:** ✅ Corrigido
```

This creates a history of improvements and ensures mistakes don't repeat.
