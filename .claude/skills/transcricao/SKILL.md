---
name: transcricao
description: Atualiza scripts de transcrição de vídeo para usar o título do vídeo como nome da pasta e arquivo. Auto-invoca quando usuário pedir para atualizar/modificar o comportamento de nomenclatura dos arquivos de transcrição.
---

# Transcrição

## Overview

Esta skill atualiza o sistema de transcrição de vídeos para usar automaticamente o título do vídeo como nome da pasta e arquivo de saída, substituindo o formato antigo baseado em timestamp.

## Quando Usar

Esta skill deve ser invocada quando:
- Usuário solicitar atualização no sistema de transcrição
- Usuário pedir para usar títulos de vídeo como nome de arquivo
- Necessário modificar comportamento de nomenclatura de transcrições

## Como Funciona

### Arquitetura da Solução

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  URL do Vídeo   │ →  │  get_video_title │ →  │ Título Sanitizado   │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                           ↓
┌─────────────────────────────────────────────────────────┘
│
↓
┌──────────────────────────────────────────────────────────┐
│  transcribe_universal.py                                 │
│  ├─ Usa título como nome da pasta                        │
│  ├─ Usa título como nome do arquivo .txt                 │
│  └─ Fallback para timestamp se título não disponível     │
└──────────────────────────────────────────────────────────┘
```

### Workflow de Atualização

Executar o script de atualização para modificar o `transcribe_universal.py`:

```bash
python3 scripts/update_transcribe.py
```

**O que este script faz:**

1. Adiciona função `get_video_title()` que:
   - Usa `yt-dlp` para extrair título do vídeo
   - Sanitiza título removendo caracteres inválidos
   - Limita tamanho a 100 caracteres
   - Retorna None em caso de erro (fallback)

2. Atualiza função `save_transcription()` para:
   - Tentar obter título do vídeo primeiro
   - Usar título como nome da pasta: `~/Downloads/{titulo}/`
   - Usar título como nome do arquivo: `{titulo}.txt`
   - Fallback para timestamp se título não disponível

### Exemplo de Uso

**Antes da atualização:**
```
~/Downloads/transcription_youtube_20251110_203100/
├── transcription.txt
└── transcription_full.json
```

**Depois da atualização:**
```
~/Downloads/The best way to advertise with Facebook ads in 2025/
├── The best way to advertise with Facebook ads in 2025.txt
└── transcription_full.json
```

## Scripts Disponíveis

### scripts/update_transcribe.py

Atualiza o arquivo `TOOLS/transcribe_universal.py` com a nova lógica de nomenclatura.

**Uso:**
```bash
python3 .claude/skills/transcricao/scripts/update_transcribe.py
```

**Funcionalidade:**
- Adiciona import `subprocess`
- Adiciona função `get_video_title(url)` completa
- Modifica `save_transcription()` para usar título
- Mantém fallback para timestamp em caso de erro
- Preserva toda funcionalidade existente

### scripts/get_video_title.py

Script auxiliar standalone para extrair título de vídeos (principalmente para debugging).

**Uso:**
```bash
python3 .claude/skills/transcricao/scripts/get_video_title.py "https://youtube.com/watch?v=..."
```

**Retorna:** Título sanitizado do vídeo ou código de erro

## Dependências

**Requerido:**
- `yt-dlp` (para extrair metadados do vídeo)

**Instalação:**
```bash
brew install yt-dlp
```

## Sanitização de Nomes

A função `sanitize_filename()` remove automaticamente:
- Caracteres inválidos: `< > : " / \ | ? *`
- Espaços extras
- Limita comprimento a 100 caracteres

## Fallback Automático

Se `get_video_title()` falhar por qualquer motivo:
- Timeout na extração
- yt-dlp não instalado
- Erro de rede
- Vídeo privado/indisponível

O sistema automaticamente usa o formato antigo:
```
transcription_{platform}_{timestamp}/
└── transcription.txt
```

## Auto-Correction System

Esta skill inclui sistema automático de correção de erros.

### Scripts disponíveis:

```bash
# Corrigir erro em SKILL.md
python3 scripts/update_skill.py <texto_antigo> <texto_novo>

# Registrar aprendizado
python3 scripts/log_learning.py <erro> <correção> [linha]
```

### Exemplo de uso:

```bash
# 1. Corrigir erro
python3 scripts/update_skill.py \
    "python3 script.py --flag" \
    "python3 script.py"

# 2. Registrar
python3 scripts/log_learning.py \
    "Flag não reconhecida" \
    "Removido --flag, usando argumento posicional" \
    "SKILL.md:42"
```

Todos os aprendizados são registrados em `LEARNINGS.md` para prevenir recorrência.
