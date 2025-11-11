---
name: gerar-foto-realista
description: Gera fotos ultra-realistas estilo analógico/iPhone com 3 estilos adaptativos (Flash Harsh Noturno, Candid Backseat, Editorial Luxury). SEMPRE gera 3 variações por padrão usando grok-image (6 imagens por variação = 18 imagens total). Engenheiro de prompts automático escolhe estilo adequado. Aspect ratio 2:3, salva em Downloads/{pasta}/. Auto-invoca quando usuário pedir foto/imagem.
---

# Gerar Foto Realista

Gera imagens ultra-realistas que parecem fotos reais tiradas com iPhone 11 por pessoas comuns.

## Overview

Esta skill transforma qualquer pedido simples em fotos hiper-realistas através de:
1. **Engenheiro de Prompts Automático** - Otimiza todo prompt para estilo iPhone 11 casual
2. **Geração Inteligente** - Detecta automaticamente single vs batch
3. **Organização Automática** - Nomeia pastas de forma inteligente
4. **Ultra-Realismo** - Fotos indistinguíveis de fotos reais

**Estilo obrigatório:** Foto casual espontânea, luz natural, cores vibrantes, como se alguém pegou o celular e clicou rapidamente.

---

## Quando Usar

Auto-invoca quando usuário pedir:
- "Gera foto de X"
- "Cria imagem de X"
- "Gera 5 fotos de X" (batch)
- "Faz foto de X"
- Qualquer variação com "foto" ou "imagem"

---

## Fluxo Principal

### Detecção Automática: Single vs Batch

**Lógica de decisão:**

```
Pedido contém número explícito? (ex: "5 fotos", "3 imagens", "10 fotos")
├─ SIM → Usar Geração em Lote (batch)
│   └─ Quantidade = número mencionado
│
└─ NÃO → Usar Geração Única (single)
    └─ Quantidade = 1
```

**Exemplos:**
- "Gera foto de cachorro" → **single** (1 foto)
- "Gera 5 fotos de carro" → **batch** (5 fotos)
- "Cria imagem de comida" → **single** (1 foto)
- "Gera várias fotos de paisagem" → **perguntar quantidade** → batch

---

## Geração Única (1 foto) - DEPRECADO

**ATENÇÃO:** Esta skill SEMPRE gera 3 variações por padrão!

Quando o usuário pede "1 foto" ou não especifica quantidade, automaticamente gerar **3 variações** para ele escolher a melhor.

**Fluxo simplificado:**
```
Pedido sem quantidade → Gerar 3 variações (batch mode)
```

Veja seção **"Geração em Lote"** abaixo.

---

## Geração em Lote (múltiplas fotos)

**PADRÃO:** Sempre gerar **3 variações** quando usuário não especifica quantidade!

**IMPORTANTE:** Usa `grok-image` skill (Grok Imagine API via Kie.ai) com aspect ratio 2:3

**Fluxo:**

### 1. Detectar Quantidade

**Regra de decisão:**
```
Usuário especificou número? (ex: "5 fotos", "10 imagens")
├─ SIM → quantidade = número especificado
└─ NÃO → quantidade = 3 (padrão)
```

**Exemplos:**
- "Gera foto de cachorro" → **3 variações** (padrão)
- "Gera 5 fotos de carro" → **5 variações**
- "Cria imagem de pessoa na festa" → **3 variações** (padrão)

### 2. Extrair Prompt Simples

Identificar o assunto principal:
- "Gera foto de cachorro" → `"cachorro"`
- "Cria imagem de mulher na festa à noite" → `"mulher na festa à noite"`
- "Gera foto de pessoa andando na rua" → `"pessoa andando na rua"`

### 3. Otimizar com Engenheiro de Prompts

**SEMPRE executar automaticamente:**

```bash
python3 .claude/skills/gerar-foto-realista/scripts/prompt_engineer.py "{PROMPT_SIMPLES}"
```

**O que o script faz:**
- Analisa contexto (noite/dia, indoor/outdoor, pessoa/objeto)
- Escolhe estilo adequado (Flash Harsh Noturno, Candid Backseat, Editorial Luxury)
- Retorna prompt ultra-realista com todas as características técnicas

**Exemplo:**
```
Input: "mulher na festa à noite"
Output: "Portrait of a woman at a night party, captured with harsh direct flash and visible analog film grain. just the raw photo. Same quality and lighting as a cheap point-and-shoot film camera with built-in flash. The woman faces the camera confidently, natural expression, skin slightly shiny from the flash. Use soft focus, visible grain, and cold tones with a faint yellow tint like expired film. Black lace top or oversized light green jacket. Background blurred, nightlife atmosphere. Keep the same analog bad camera aesthetic harsh flash, high contrast, imperfect texture, no retouching."
```

### 4. Mostrar Informações

```
🎨 Gerando {QUANTIDADE} variações ultra-realistas...
📝 Prompt otimizado:
"{PROMPT_ENHANCED}"

🔧 Configuração:
- API: Grok Imagine via grok-image
- Aspect ratio: 2:3 (portrait)
- Pasta: Downloads/{NOME_PASTA}/
```

### 5. Gerar Nome Base Descritivo

**IMPORTANTE:** Antes de gerar, criar nome base descritivo para os arquivos

```bash
python3 .claude/skills/gerar-foto-realista/scripts/folder_namer.py "{PROMPT_SIMPLES}" {QUANTIDADE}
```

**Exemplo:**
```
Input: "pessoa em parque de diversões" 3
Output: pessoa_parque_3_fotos
```

### 6. Gerar Imagens com grok-image

**IMPORTANTE:** Chamar a skill `grok-image` usando script batch direto com nome base

```bash
python3 .claude/skills/grok-image/scripts/batch_generate_grok.py \
    "{PROMPT_ENHANCED}" \
    "{PROMPT_ENHANCED}" \
    "{PROMPT_ENHANCED}" \
    --aspect-ratio=2:3 \
    --output-dir=~/Downloads/{NOME_PASTA} \
    --base-name={NOME_BASE_SIMPLES}
```

**O script grok-image faz automaticamente:**
1. Gera {QUANTIDADE} variações do mesmo prompt
2. Usa Grok Imagine API (xAI)
3. Aspect ratio 2:3 (portrait)
4. Cria estrutura organizada:
   ```
   Downloads/{NOME_PASTA}/
   ├── Conjunto 1/
   │   ├── {NOME_BASE}_1.jpg
   │   ├── {NOME_BASE}_2.jpg
   │   └── ... (6 imagens)
   ├── Conjunto 2/
   │   └── ... (6 imagens)
   └── Conjunto 3/
       └── ... (6 imagens)
   ```
5. Processa em lote (paralelo, max 5 workers)

### 7. Confirmar

```
✅ {QUANTIDADE} conjuntos gerados com sucesso!
📁 ~/Downloads/{NOME_PASTA}/
   ├── Conjunto 1/ (6 imagens)
   ├── Conjunto 2/ (6 imagens)
   └── Conjunto 3/ (6 imagens)

🎨 Prompt usado: "{PROMPT_ENHANCED}"
📐 Aspect ratio: 2:3
⚡ API: Grok Imagine (xAI)
```

---

## Validações

### Antes de Gerar

1. **Prompt válido:**
   - Mínimo 3 caracteres
   - Se vazio, perguntar: "Foto de quê?"

2. **Quantidade válida (batch):**
   - Entre 2-10 fotos
   - Se < 2: sugerir geração única
   - Se > 10: ajustar para 10 e avisar

3. **Scripts existem:**
   - Verificar `.claude/skills/gerar-foto-realista/scripts/prompt_engineer.py`
   - Verificar `.claude/skills/gerar-foto-realista/scripts/folder_namer.py`
   - Verificar `SCRIPTS/image-generation/generate_nanobanana.py`
   - Verificar `SCRIPTS/image-generation/batch_generate.py`

---

## Tratamento de Erros

### Erro: Engenheiro de prompts falhou
```
⚠️  Aviso: Otimização de prompt falhou, usando prompt básico melhorado
📝 Prompt: "{prompt_simples}, foto tirada com iPhone 11, luz natural, ultra-realista"
```
→ Continuar com fallback

### Erro: Script de geração falhou
```
❌ Erro ao gerar imagem: {erro}
💡 Tentar novamente ou verificar conexão
```
→ Retry 1x, depois abortar

### Erro: Timeout
```
⏱️  Geração demorou muito. Verifique conexão com a internet.
```

---

## Exemplos Completos

### Exemplo 1: Padrão (3 variações)

```
Usuário: "Gera foto de mulher na festa à noite"

Detecção: Sem quantidade → 3 variações (padrão)
↓
Extrai: prompt = "mulher na festa à noite"
↓
Otimiza: prompt_engineer.py "mulher na festa à noite"
→ "Portrait of a woman at a night party, captured with harsh direct flash and visible analog film grain. just the raw photo..."
(Escolheu ESTILO 1: Flash Harsh Noturno automaticamente)
↓
Mostra:
"🎨 Gerando 3 variações ultra-realistas...
 📝 Prompt otimizado: Portrait of a woman at a night party, captured with harsh direct flash..."
↓
Gera nome base: folder_namer.py "mulher na festa à noite" 3
→ "mulher_festa_3_fotos"
→ Nome base simples: "mulher_festa"
↓
Invoca: grok-image batch script
Comando:
python3 .claude/skills/grok-image/scripts/batch_generate_grok.py \
    "{PROMPT_ENHANCED}" "{PROMPT_ENHANCED}" "{PROMPT_ENHANCED}" \
    --aspect-ratio=2:3 \
    --output-dir=~/Downloads/mulher_festa_3_fotos \
    --base-name=mulher_festa
↓
Confirma:
"✅ 3 conjuntos gerados com sucesso!
 📁 ~/Downloads/mulher_festa_3_fotos/
    ├── Conjunto 1/ (6 imagens)
    ├── Conjunto 2/ (6 imagens)
    └── Conjunto 3/ (6 imagens)
 🎨 Prompt: Portrait of a woman at a night party...
 📐 Aspect ratio: 2:3
 ⚡ API: Grok Imagine (xAI)"
```

### Exemplo 2: Quantidade específica (5 variações)

```
Usuário: "Gera 5 fotos de pessoa andando perto de jato privado"

Detecção: Quantidade 5
↓
Extrai: prompt = "pessoa andando perto de jato privado"
↓
Otimiza: prompt_engineer.py "pessoa andando perto de jato privado"
→ "Editorial-style portrait of a single person walking near a private jet on a sunny day. just the raw photo..."
(Escolheu ESTILO 3: Editorial Luxury automaticamente)
↓
Mostra:
"🎨 Gerando 5 variações ultra-realistas...
 📝 Prompt otimizado: Editorial-style portrait of a single person walking near..."
↓
Gera nome base: folder_namer.py "pessoa andando perto de jato privado" 5
→ "pessoa_jato_5_fotos"
→ Nome base simples: "pessoa_jato"
↓
Invoca: grok-image batch script
Comando: (repetir prompt 5x)
python3 .claude/skills/grok-image/scripts/batch_generate_grok.py \
    "{PROMPT}" "{PROMPT}" "{PROMPT}" "{PROMPT}" "{PROMPT}" \
    --aspect-ratio=2:3 \
    --output-dir=~/Downloads/pessoa_jato_5_fotos \
    --base-name=pessoa_jato
↓
Confirma:
"✅ 5 conjuntos gerados com sucesso!
 📁 ~/Downloads/pessoa_jato_5_fotos/
    ├── Conjunto 1/ (6 imagens)
    ├── Conjunto 2/ (6 imagens)
    ├── Conjunto 3/ (6 imagens)
    ├── Conjunto 4/ (6 imagens)
    └── Conjunto 5/ (6 imagens)
 🎨 Prompt: Editorial-style portrait of a single person...
 📐 Aspect ratio: 2:3
 ⚡ API: Grok Imagine (xAI)"
```

### Exemplo 3: Carro à noite (Candid Backseat)

```
Usuário: "Gera foto de pessoa no banco de trás do carro à noite"

Detecção: Sem quantidade → 3 variações (padrão)
↓
Extrai: prompt = "pessoa no banco de trás do carro à noite"
↓
Otimiza: prompt_engineer.py "pessoa no banco de trás do carro à noite"
→ "Candid portrait of a person sitting in the backseat of a car, captured with harsh direct flash..."
(Escolheu ESTILO 2: Candid Backseat automaticamente)
↓
Mostra:
"🎨 Gerando 3 variações ultra-realistas...
 📝 Prompt otimizado: Candid portrait of a person sitting in the backseat..."
↓
Gera nome base: folder_namer.py "pessoa no banco de trás do carro à noite" 3
→ "pessoa_carro_noite_3_fotos"
→ Nome base simples: "pessoa_carro"
↓
Invoca: grok-image batch script
Comando:
python3 .claude/skills/grok-image/scripts/batch_generate_grok.py \
    "{PROMPT}" "{PROMPT}" "{PROMPT}" \
    --aspect-ratio=2:3 \
    --output-dir=~/Downloads/pessoa_carro_noite_3_fotos \
    --base-name=pessoa_carro
↓
Confirma:
"✅ 3 conjuntos gerados com sucesso!
 📁 ~/Downloads/pessoa_carro_noite_3_fotos/
    ├── Conjunto 1/ (6 imagens)
    ├── Conjunto 2/ (6 imagens)
    └── Conjunto 3/ (6 imagens)
 🎨 Prompt: Candid portrait of a person sitting...
 📐 Aspect ratio: 2:3
 ⚡ API: Grok Imagine (xAI)"
```

---

## Estilos Ultra-Realistas Disponíveis

O engenheiro de prompts escolhe automaticamente entre 3 estilos validados:

### 🌙 ESTILO 1: Flash Harsh Noturno
**Quando:** Festas, eventos noturnos, ambientes escuros internos

**Características técnicas:**
- Flash direto e harsh, cold tones
- Grain analógico visível (35mm film)
- High contrast, overexposed highlights
- Soft focus, imperfect texture
- Skin slightly shiny do flash
- Yellow tint (filme expirado)
- Background blurred, atmosfera nightlife
- Vignette sutil nas bordas

**Exemplo:** Pessoa em festa, balada, evento noturno

---

### 🚗 ESTILO 2: Candid Backseat
**Quando:** Pessoas em carros, momentos casuais noturnos, streetwear

**Características técnicas:**
- Flash direto cold e sharp
- Reflexos fortes no couro/vidro/óculos
- Vignette nas bordas
- Soft blur, textura imperfeita
- Streetwear/leather jacket
- Cinematic nightlife tone
- Natural smiles, relaxed posture
- 35mm analog aesthetic

**Exemplo:** Pessoa no banco traseiro do carro, selfie noturna no carro

---

### ☀️ ESTILO 3: Editorial Luxury
**Quando:** Outdoor dia, luxury lifestyle, fashion editorial, clean scenes

**Características técnicas:**
- Natural daylight, clean shadows
- Sharp details, high-end fashion campaign
- Minimalist luxury vibe
- Bright sky, concrete/clean background
- Crisp lighting, soft contrast
- Natural color tones
- Cinematic depth of field
- Elegant casual clothing

**Exemplo:** Pessoa andando, jato privado, outdoor dia, fashion

---

### ✅ Regras Universais (todos os estilos)

**Sempre incluir:**
- "just the raw photo" (aspecto não-editado)
- Imperfections: grain, soft blur, textura imperfeita
- ZERO retouching ou filtros artificiais
- Realismo total - como fotos reais de câmera comum/analógica

**Nunca incluir:**
- ❌ Termos artísticos (ilustração, desenho, pintura)
- ❌ Iluminação de estúdio (exceto flash analógico)
- ❌ Poses profissionais ensaiadas
- ❌ Cenários perfeitos demais
- ❌ Composição profissional

---

## Notas Técnicas

### Local de Salvamento
**Sempre em pasta organizada:**
```
~/Downloads/{nome_pasta}/
  ├── image_1.png
  ├── image_2.png
  └── image_3.png
```

**Exemplo:**
- "mulher na festa" → `~/Downloads/mulher-festa/image_1.png`
- "pessoa jato privado" → `~/Downloads/pessoa-jato-privado/image_1.png`

### Scripts e Skills Utilizados

**1. Prompt Engineer (bundled nesta skill):**
- Local: `.claude/skills/gerar-foto-realista/scripts/prompt_engineer.py`
- Função: Otimiza prompts para ultra-realismo com 3 estilos
- API: Claude 3.5 Haiku via OpenRouter
- Input: Prompt simples (ex: "mulher na festa")
- Output: Prompt ultra-realista adaptado ao estilo adequado

**2. grok-image skill (externa):**
- Função: Gera imagens via Grok Imagine API (xAI)
- Script: `.claude/skills/grok-image/scripts/batch_generate_grok.py`
- Parâmetros:
  - `prompts`: Prompts repetidos N vezes (1 prompt = 1 geração = 6 imagens)
  - `--aspect-ratio`: 2:3 (portrait, OBRIGATÓRIO)
  - `--output-dir`: Pasta destino em Downloads/
  - `--workers`: Max 5 parallel tasks
- Processamento: Batch paralelo (max 5 concurrent)
- Output: Cada geração = 6 imagens `grok_batch_X_taskid_Y.jpg`
- Custo: 4 créditos ($0.02) por geração = 6 imagens

### Dependências
- OpenRouter API key (prompt engineer)
- Kie.ai API key (Grok Imagine via grok-image skill)
- Skill grok-image instalada e funcional

---

## Checklist de Execução

Para TODA geração, seguir esta ordem:

- [ ] 1. Detectar quantidade (especificada? → usar valor | não? → 3 padrão)
- [ ] 2. Extrair prompt simples do pedido do usuário
- [ ] 3. Validar prompt (mín 3 caracteres)
- [ ] 4. Executar `prompt_engineer.py "{prompt_simples}"`
- [ ] 5. Capturar output (prompt ultra-realista otimizado)
- [ ] 6. Executar `folder_namer.py "{prompt_simples}" {quantidade}`
- [ ] 7. Capturar nome da pasta principal e nome base simples
- [ ] 8. Mostrar pro usuário: quantidade + prompt otimizado + config
- [ ] 9. Invocar `grok-image` batch script com:
  ```bash
  python3 .claude/skills/grok-image/scripts/batch_generate_grok.py \
      "{prompt_otimizado}" "{prompt_otimizado}" "{prompt_otimizado}" \
      --aspect-ratio=2:3 \
      --output-dir=~/Downloads/{nome_pasta_principal} \
      --base-name={nome_base_simples}
  ```
  (Repetir prompt N vezes = N gerações)
- [ ] 10. Aguardar conclusão (cada geração = 1 conjunto com 6 imagens)
- [ ] 11. Confirmar sucesso com estrutura de pastas organizada

**Regras críticas:**
- ✅ SEMPRE usar grok-image batch script direto
- ✅ SEMPRE aspect ratio 2:3 (portrait)
- ✅ SEMPRE gerar nome inteligente com folder_namer.py
- ✅ SEMPRE criar estrutura Conjunto 1/, Conjunto 2/, etc
- ✅ SEMPRE usar --base-name para nomes de arquivo descritivos
- ✅ SEMPRE gerar no mínimo 3 variações (padrão)
- ✅ Cada conjunto retorna 6 imagens JPG
