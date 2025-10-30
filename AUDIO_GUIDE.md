# 🎙️ Guia Rápido - Geração de Áudio ElevenLabs

## Configuração
✅ API Key já configurada nos scripts
✅ Áudios salvos automaticamente em `~/Downloads`

## Comandos Rápidos

### Áudio Simples
```bash
python3 tools/generate_audio_elevenlabs.py "Seu texto aqui"
```

### Listar Vozes Disponíveis
```bash
python3 tools/generate_audio_elevenlabs.py --list-voices
```

### Alta Qualidade
```bash
python3 tools/generate_audio_elevenlabs.py "Texto" --format mp3_ultra
```

### Múltiplos Áudios (Batch)
```bash
python3 tools/generate_audio_batch_elevenlabs.py "Texto 1" "Texto 2" "Texto 3"
```

## Formatos Disponíveis

| Formato | Qualidade | Tamanho | Uso Recomendado |
|---------|-----------|---------|-----------------|
| `mp3_low` | 22kHz, 32kbps | Menor | Testes rápidos |
| `mp3_medium` | 44kHz, 64kbps | Médio | Uso geral |
| `mp3_high` | 44kHz, 128kbps | Bom | **Padrão** |
| `mp3_ultra` | 44kHz, 192kbps | Maior | Produção profissional |
| `pcm` | 44kHz, sem compressão | Muito grande | Edição de áudio |

## Modelos Disponíveis

- `eleven_multilingual_v2` - **Recomendado para português** (padrão)
- `eleven_monolingual_v1` - Inglês apenas
- `eleven_turbo_v2` - Mais rápido

## Parâmetros de Voz

### Stability (0.0 - 1.0)
- **0.0-0.3**: Voz mais variada e expressiva
- **0.4-0.6**: Balanceado (padrão: 0.5)
- **0.7-1.0**: Voz mais consistente e estável

### Similarity (0.0 - 1.0)
- **0.0-0.5**: Mais criativo, menos fiel à voz original
- **0.6-0.8**: Balanceado (padrão: 0.75)
- **0.8-1.0**: Muito fiel à voz original

## Exemplos Práticos

### Narração para YouTube
```bash
python3 tools/generate_audio_elevenlabs.py \
  "Olá pessoal, bem-vindos ao meu canal! Hoje vamos falar sobre inteligência artificial." \
  --format mp3_high \
  --stability 0.6 \
  --similarity 0.8
```

### Tutorial em Partes
```bash
python3 tools/generate_audio_batch_elevenlabs.py \
  "Parte 1: Introdução ao Python" \
  "Parte 2: Variáveis e Tipos de Dados" \
  "Parte 3: Estruturas de Controle" \
  "Parte 4: Funções e Módulos" \
  --delay 2
```

### Podcast Intro/Outro
```bash
python3 tools/generate_audio_batch_elevenlabs.py \
  "Bem-vindo ao Podcast Tech. Eu sou seu host e hoje vamos falar sobre IA." \
  "Obrigado por ouvir. Não esqueça de se inscrever!" \
  --format mp3_ultra
```

### Audiobook
```bash
python3 tools/generate_audio_batch_elevenlabs.py \
  "Capítulo Um. Era uma vez, em uma terra distante..." \
  "Capítulo Dois. O herói partiu em sua jornada..." \
  "Capítulo Três. Ele enfrentou muitos desafios..." \
  --stability 0.7 \
  --delay 3
```

### Voiceover Profissional
```bash
python3 tools/generate_audio_elevenlabs.py \
  "Este produto revolucionário vai mudar sua vida. Disponível agora." \
  --format mp3_ultra \
  --stability 0.8 \
  --similarity 0.9 \
  --output comercial_produto.mp3
```

## Dicas de Texto

### ✅ BOM
```
"Olá! Bem-vindo ao nosso tutorial. Hoje, vamos aprender sobre Python."
```

### ❌ EVITE
```
"ola bem vindo ao nosso tutorial hoje vamos aprender sobre python"
```

### Pontuação é Importante
- **.** = Pausa curta
- **,** = Pausa muito curta
- **!** = Ênfase e pausa
- **?** = Entonação de pergunta

### Números
- ✅ "vinte e três"
- ❌ "23"

### Siglas
- ✅ "I A" (para IA)
- ✅ "C P F" (para CPF)

## Uso em Batch

### Vantagens
- Automatiza criação de múltiplas narrações
- Mantém consistência de voz
- Numeração sequencial automática
- Perfeito para tutoriais divididos

### Exemplo Completo
```bash
python3 tools/generate_audio_batch_elevenlabs.py \
  "Olá, bem-vindo ao curso de Python" \
  "Nesta aula, vamos aprender sobre variáveis" \
  "Variáveis são espaços na memória do computador" \
  "Você pode armazenar números, textos e mais" \
  "Vamos praticar criando algumas variáveis" \
  "Parabéns! Você completou a primeira aula" \
  --format mp3_high \
  --delay 2
```

## Onde Encontrar os Arquivos

Todos os áudios são salvos em:
```
~/Downloads/
```

### Nomes dos Arquivos
- Individual: `generated_audio_AAAAMMDD_HHMMSS.mp3`
- Batch: `audio_batch_AAAAMMDD_HHMMSS_01_of_03.mp3`
- Personalizado: `seu_nome.mp3` (com --output)

## Solução de Problemas

### Erro de autenticação
Verifique se a API key está correta no script:
```bash
grep "API_KEY" tools/generate_audio_elevenlabs.py
```

### Áudio não gerado
- Verifique sua conexão com internet
- Confirme que tem créditos na conta ElevenLabs
- Tente um texto mais curto

### Qualidade ruim
- Use `--format mp3_ultra`
- Ajuste `--stability 0.7 --similarity 0.8`
- Melhore a pontuação do texto

## Limites e Custos

- Cada requisição consome créditos da sua conta ElevenLabs
- Textos maiores = mais caracteres = mais créditos
- Use `--list-voices` para verificar vozes disponíveis na sua conta
- Modo batch usa 1 requisição por texto (não economiza créditos)

## Recursos Adicionais

- Documentação ElevenLabs: https://elevenlabs.io/docs
- Ver vozes disponíveis: https://elevenlabs.io/voice-library
- Gerenciar conta: https://elevenlabs.io/app

---

**Criado com Claude Code** - Workspace inteligente para desenvolvimento com IA
