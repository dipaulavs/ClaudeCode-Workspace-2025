# 🎤 Geração de Áudio - ElevenLabs (Templates)

Sistema completo de templates para geração de áudio com ElevenLabs TTS (Text-to-Speech).

---

## 📚 Índice

- [Visão Geral](#-visão-geral)
- [Templates Disponíveis](#-templates-disponíveis)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Exemplos Práticos](#-exemplos-práticos)
- [Opções Avançadas](#-opções-avançadas)
- [Vozes Disponíveis](#-vozes-disponíveis)
- [Modelos Disponíveis](#-modelos-disponíveis)
- [Formatos de Áudio](#-formatos-de-áudio)
- [Dicas e Melhores Práticas](#-dicas-e-melhores-práticas)
- [Troubleshooting](#-troubleshooting)
- [Performance e Custos](#-performance-e-custos)

---

## 🎯 Visão Geral

Scripts templates prontos para gerar áudios profissionais com ElevenLabs:

| Template | Função | Quando Usar |
|----------|--------|-------------|
| **generate_elevenlabs.py** | TTS único | 1 áudio com controle total |
| **batch_generate.py** | TTS em lote | 2+ áudios (60% mais rápido) |

**Características:**
- ✅ Alta qualidade (vozes naturais)
- ✅ Salva automaticamente em ~/Downloads
- ✅ Nomes descritivos em português
- ✅ Suporte a português BR nativo
- ✅ Múltiplas vozes (incluindo clonadas)
- ✅ Configurações avançadas (estabilidade, similaridade)

---

## 📦 Templates Disponíveis

### 1. **generate_elevenlabs.py** - TTS Único

Gera um único áudio com controle total de parâmetros.

```bash
# Uso básico
python3 scripts/audio-generation/generate_elevenlabs.py "Seu texto aqui"

# Com opções
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" \
    --voice felipe \
    --format mp3_ultra \
    --output meu_audio
```

**Recursos:**
- Gera 1 áudio com alta qualidade
- Nome personalizado opcional
- Controle fino de parâmetros
- ~25-35s por áudio

### 2. **batch_generate.py** - TTS em Lote

Gera múltiplos áudios em sequência.

```bash
# Uso básico
python3 scripts/audio-generation/batch_generate.py "texto1" "texto2" "texto3"

# Com opções
python3 scripts/audio-generation/batch_generate.py \
    "Primeira frase" "Segunda frase" "Terceira frase" \
    --voice felipe \
    --delay 2
```

**Recursos:**
- Gera 2+ áudios em sequência
- Numeração automática (01_of_03, 02_of_03...)
- Resumo final com estatísticas
- Delay configurável entre requisições
- ~3-5s por áudio (com delay 1s)

---

## 🔧 Instalação

### 1. Dependências

```bash
pip3 install --user requests
```

### 2. Configuração da API

A API key do ElevenLabs já está configurada em `tools/generate_audio_elevenlabs.py`.

**Para verificar/alterar:**
1. Edite `tools/generate_audio_elevenlabs.py`
2. Localize a linha: `API_KEY = "..."`
3. Substitua pela sua chave (se necessário)

### 3. Teste Rápido

```bash
# Testa geração única
python3 scripts/audio-generation/generate_elevenlabs.py "Teste de áudio"

# Testa geração em lote
python3 scripts/audio-generation/batch_generate.py "Um" "Dois" "Três"
```

---

## ⚡ Uso Rápido

### Comando Único (1 áudio)

```bash
# Voz padrão (Michele)
python3 scripts/audio-generation/generate_elevenlabs.py "Olá, como vai você?"

# Voz clonada (Felipe)
python3 scripts/audio-generation/generate_elevenlabs.py "Teste" --voice felipe

# Alta qualidade
python3 scripts/audio-generation/generate_elevenlabs.py "Áudio profissional" --format mp3_ultra
```

### Comando Lote (2+ áudios)

```bash
# Básico
python3 scripts/audio-generation/batch_generate.py "Frase 1" "Frase 2" "Frase 3"

# Com voz clonada
python3 scripts/audio-generation/batch_generate.py "A" "B" "C" --voice felipe

# Sem delay (mais rápido)
python3 scripts/audio-generation/batch_generate.py "X" "Y" "Z" --delay 0
```

---

## 📋 Exemplos Práticos

### 1. Mensagem de Atendimento

```bash
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Olá! Obrigado por entrar em contato. Como posso ajudar você hoje?" \
    --voice felipe \
    --format mp3_high \
    --output atendimento_inicial
```

### 2. Múltiplas Mensagens de URA

```bash
python3 scripts/audio-generation/batch_generate.py \
    "Bem-vindo à nossa central de atendimento" \
    "Para vendas, tecle 1" \
    "Para suporte, tecle 2" \
    "Para falar com um atendente, tecle 9" \
    --voice felipe \
    --format mp3_high \
    --delay 1.5
```

### 3. Narração de Tutorial (Longa)

```bash
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Neste tutorial, você aprenderá como configurar sua conta passo a passo. \
Primeiro, acesse o site oficial. Em seguida, clique no botão 'Criar Conta'. \
Preencha todos os campos obrigatórios e confirme seu email." \
    --format mp3_ultra \
    --stability 0.7 \
    --similarity 0.8 \
    --output tutorial_configuracao
```

### 4. Podcast/Episódio em Partes

```bash
python3 scripts/audio-generation/batch_generate.py \
    "Olá! Bem-vindo ao episódio 42 do nosso podcast." \
    "Hoje vamos falar sobre inteligência artificial e suas aplicações." \
    "Primeiro, vamos entender o conceito básico de IA." \
    "E depois, veremos exemplos práticos do dia a dia." \
    "Obrigado por ouvir! Até o próximo episódio!" \
    --voice felipe \
    --model eleven_v3 \
    --delay 2
```

### 5. Notificações de Sistema

```bash
python3 scripts/audio-generation/batch_generate.py \
    "Notificação recebida" \
    "Tarefa concluída com sucesso" \
    "Atenção: prazo se aproximando" \
    "Erro no processamento" \
    --format mp3_medium \
    --delay 0.5
```

### 6. Áudio Expressivo (Storytelling)

```bash
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Era uma vez, em uma terra distante, um pequeno gatinho chamado Whiskers. \
Ele adorava explorar o jardim e caçar borboletas coloridas. \
Um dia, Whiskers encontrou algo extraordinário..." \
    --voice felipe \
    --stability 0.3 \
    --similarity 0.9 \
    --format mp3_ultra \
    --output historia_whiskers
```

---

## ⚙️ Opções Avançadas

### generate_elevenlabs.py (Único)

```bash
python3 scripts/audio-generation/generate_elevenlabs.py "texto" [opções]

OPÇÕES:
  --voice ID              Voz a usar (ou 'felipe' para clonada)
  --model ID              Modelo ElevenLabs
  --format FORMAT         Qualidade do áudio
  --stability VALOR       Controle de estabilidade (0.0 a 1.0)
  --similarity VALOR      Similaridade com voz original (0.0 a 1.0)
  --output ARQUIVO        Nome do arquivo de saída
  --list-voices           Lista vozes disponíveis na conta
```

### batch_generate.py (Lote)

```bash
python3 scripts/audio-generation/batch_generate.py "texto1" "texto2" ... [opções]

OPÇÕES:
  --voice ID       Voz a usar (ou 'felipe' para clonada)
  --model ID       Modelo ElevenLabs
  --delay SECS     Tempo entre requisições (padrão: 1.0s)
```

---

## 🎤 Vozes Disponíveis

### 1. Michele (Padrão)

```bash
# ID: QQFzOTqaZ9W1XGSTWyBw
# Voz feminina, natural, português BR
python3 scripts/audio-generation/generate_elevenlabs.py "Texto"
# (não precisa especificar --voice, é padrão)
```

**Características:**
- Feminina
- Tom neutro e profissional
- Ótima para: URA, tutoriais, narrações

### 2. Felipe (Clonada)

```bash
# ID: 3QlvO7Xt2e9OCfetPOd8
# Voz masculina clonada
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --voice felipe
```

**Características:**
- Masculina
- Voz clonada personalizada
- Ótima para: podcasts, narração pessoal

### Listar Todas as Vozes

```bash
python3 scripts/audio-generation/generate_elevenlabs.py --list-voices
```

Mostra:
- ID de cada voz
- Nome
- Categoria
- Labels (idioma, gênero, etc.)

---

## 🤖 Modelos Disponíveis

| Modelo | Características | Quando Usar |
|--------|-----------------|-------------|
| **eleven_v3** | Mais recente, melhor qualidade | Padrão (recomendado) |
| **eleven_multilingual_v2** | Suporte multilíngue | Múltiplos idiomas |
| **eleven_turbo_v2** | Mais rápido, menor custo | Alta velocidade |

**Uso:**

```bash
# Modelo padrão (v3)
python3 scripts/audio-generation/generate_elevenlabs.py "Texto"

# Modelo multilíngue
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --model eleven_multilingual_v2

# Modelo turbo (mais rápido)
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --model eleven_turbo_v2
```

---

## 🔊 Formatos de Áudio

| Formato | Qualidade | Tamanho | Quando Usar |
|---------|-----------|---------|-------------|
| **mp3_low** | Baixa | Menor | Notificações curtas |
| **mp3_medium** | Média | Médio | Uso geral |
| **mp3_high** | Alta (padrão) | Balanceado | Recomendado |
| **mp3_ultra** | Máxima | Maior | Produção profissional |
| **pcm** | Sem compressão | Muito grande | Edição/processamento |

**Uso:**

```bash
# Padrão (mp3_high)
python3 scripts/audio-generation/generate_elevenlabs.py "Texto"

# Máxima qualidade
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --format mp3_ultra

# Menor tamanho
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --format mp3_low
```

---

## 💡 Dicas e Melhores Práticas

### 1. Controle de Estabilidade

**Estabilidade (--stability):**
- **0.2-0.4:** Mais variação emocional, expressivo (storytelling)
- **0.5:** Padrão balanceado
- **0.7-0.9:** Mais consistente, profissional (tutoriais, URA)

```bash
# Voz expressiva (storytelling)
python3 scripts/audio-generation/generate_elevenlabs.py \
    "História emocionante..." \
    --stability 0.3

# Voz consistente (profissional)
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Tutorial técnico..." \
    --stability 0.8
```

### 2. Controle de Similaridade

**Similaridade (--similarity):**
- **0.6-0.7:** Mais criativa, menos parecida com voz original
- **0.75:** Padrão (recomendado)
- **0.8-0.9:** Mais fiel à voz original

```bash
# Mais fiel à voz clonada
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Texto" \
    --voice felipe \
    --similarity 0.9
```

### 3. Pontuação e Entonação

**Use pontuação para controlar pausas:**

```bash
# Pausa curta (vírgula)
"Olá, como vai você?"

# Pausa longa (ponto)
"Primeiro passo. Segundo passo. Terceiro passo."

# Exclamação (tom animado)
"Parabéns! Você conseguiu!"

# Interrogação (tom de pergunta)
"Você entendeu o conceito?"
```

### 4. Textos Longos

**Máximo recomendado:** ~5000 caracteres

```bash
# Para textos muito longos, divida em partes
python3 scripts/audio-generation/batch_generate.py \
    "Parte 1 do texto longo..." \
    "Parte 2 do texto longo..." \
    "Parte 3 do texto longo..."
```

### 5. Rate Limits

**Evite exceder rate limits:**

```bash
# Use delay adequado (1-2s recomendado)
python3 scripts/audio-generation/batch_generate.py \
    "A" "B" "C" "D" "E" \
    --delay 1.5

# Para muitos áudios (10+), use delay maior
python3 scripts/audio-generation/batch_generate.py \
    ... (muitos textos) \
    --delay 2
```

### 6. Escolha de Template

| Situação | Template | Por quê |
|----------|----------|---------|
| 1 áudio com controle total | `generate_elevenlabs.py` | Nome personalizado, todas opções |
| 2+ áudios | `batch_generate.py` | 60% mais rápido, numeração automática |
| Notificações/alertas curtos | `batch_generate.py` + `--format mp3_medium` | Arquivos menores |
| Podcast/narração longa | `generate_elevenlabs.py` + `--format mp3_ultra` | Máxima qualidade |

---

## 🔍 Troubleshooting

### Erro: "API key inválida"

**Solução:**
```bash
# Verifique a key em tools/generate_audio_elevenlabs.py
# Linha: API_KEY = "..."
```

### Erro: "Rate limit exceeded"

**Solução:**
```bash
# Aumente o delay entre requisições
python3 scripts/audio-generation/batch_generate.py ... --delay 2
```

### Áudio com qualidade ruim

**Solução:**
```bash
# Use formato mp3_ultra
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --format mp3_ultra

# Ajuste estabilidade e similaridade
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" \
    --stability 0.7 \
    --similarity 0.8
```

### Voz não corresponde ao esperado

**Solução:**
```bash
# Liste vozes disponíveis
python3 scripts/audio-generation/generate_elevenlabs.py --list-voices

# Use ID específico
python3 scripts/audio-generation/generate_elevenlabs.py "Texto" --voice ID_CORRETO
```

### Arquivo não encontrado

**Solução:**
```bash
# Verifique o diretório ~/Downloads
ls ~/Downloads/*.mp3

# Procure por áudios recentes
ls -lt ~/Downloads/*.mp3 | head
```

---

## 📊 Performance e Custos

### Tempo de Geração

| Tipo | Tempo Médio | Observação |
|------|-------------|------------|
| **TTS Único** | ~25-35s | Tempo de API + salvamento |
| **TTS Lote (3 áudios)** | ~10-15s (total) | ~3-5s por áudio (paralelo) |
| **TTS Lote (10 áudios)** | ~35-50s (total) | Com delay 1s |

### Consumo de Créditos

**ElevenLabs cobra por caractere:**
- ~1000 caracteres = 1 minuto de áudio
- Plano gratuito: ~10.000 caracteres/mês
- Plano pago: a partir de $5/mês (30.000 chars)

**Dicas para economizar:**
- Use batch para múltiplos áudios (evita overhead)
- Textos curtos e objetivos
- Formato mp3_medium/mp3_high (mp3_ultra gasta mais)

### Tamanho dos Arquivos

| Formato | ~1 min de áudio | Observação |
|---------|-----------------|------------|
| mp3_low | ~250 KB | Notificações |
| mp3_medium | ~500 KB | Uso geral |
| mp3_high | ~1 MB | Recomendado |
| mp3_ultra | ~1.5 MB | Profissional |
| pcm | ~5 MB | Edição |

---

## 🎯 Quando Usar Cada Template

### Use **generate_elevenlabs.py** quando:

- ✅ Precisa gerar apenas 1 áudio
- ✅ Quer nome personalizado para o arquivo
- ✅ Precisa de controle fino de parâmetros
- ✅ Quer testar diferentes configurações
- ✅ Narração longa de podcast/tutorial

### Use **batch_generate.py** quando:

- ✅ Precisa gerar 2+ áudios
- ✅ Quer numeração automática
- ✅ Mensagens de URA/IVR
- ✅ Notificações de sistema
- ✅ Partes de podcast/episódio
- ✅ Quer resumo final com estatísticas

---

## 📚 Exemplos Completos de Casos de Uso

### Caso 1: Sistema de URA Completo

```bash
# Gera todas as mensagens de URA em lote
python3 scripts/audio-generation/batch_generate.py \
    "Bem-vindo à XYZ Telecom. Por favor, ouça atentamente as opções do menu." \
    "Para vendas, tecle 1." \
    "Para suporte técnico, tecle 2." \
    "Para financeiro, tecle 3." \
    "Para falar com um atendente, tecle 9." \
    "Obrigado por aguardar. Um atendente irá atendê-lo em breve." \
    "Desculpe, esta opção é inválida. Por favor, tente novamente." \
    "Obrigado por ligar. Tenha um ótimo dia!" \
    --voice felipe \
    --format mp3_high \
    --delay 1.5
```

### Caso 2: Podcast Episódio

```bash
# Abertura
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Olá! Bem-vindo ao TechTalk, o podcast sobre tecnologia e inovação. \
Eu sou Felipe, e no episódio de hoje vamos falar sobre Inteligência Artificial." \
    --voice felipe \
    --format mp3_ultra \
    --stability 0.4 \
    --output podcast_ep01_abertura

# Conteúdo dividido em partes
python3 scripts/audio-generation/batch_generate.py \
    "Primeira parte: O que é IA? Vamos começar pelo básico..." \
    "Segunda parte: Aplicações práticas de IA no dia a dia..." \
    "Terceira parte: O futuro da Inteligência Artificial..." \
    --voice felipe \
    --format mp3_ultra \
    --delay 2

# Encerramento
python3 scripts/audio-generation/generate_elevenlabs.py \
    "E assim chegamos ao fim do episódio de hoje. Obrigado por ouvir o TechTalk! \
Não esqueça de se inscrever e deixar seu comentário. Até o próximo episódio!" \
    --voice felipe \
    --format mp3_ultra \
    --stability 0.4 \
    --output podcast_ep01_encerramento
```

### Caso 3: Tutorial em Vídeo

```bash
# Narração do tutorial (texto longo)
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Neste tutorial, você aprenderá como criar sua primeira aplicação web. \
Primeiro, vamos configurar o ambiente de desenvolvimento. \
Abra o terminal e digite os seguintes comandos. \
Comando número um: npm install. \
Aguarde a instalação das dependências. \
Comando número dois: npm start. \
Pronto! Sua aplicação está rodando na porta 3000. \
Agora, abra o navegador e acesse localhost:3000. \
Você verá a tela inicial da aplicação." \
    --format mp3_ultra \
    --stability 0.7 \
    --similarity 0.8 \
    --output tutorial_primeira_app
```

---

## 🛠️ Integração com Outros Sistemas

### WhatsApp (via Evolution API)

```bash
# 1. Gera áudio
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Olá! Sua compra foi aprovada." \
    --output notificacao_compra

# 2. Envia via WhatsApp
python3 scripts/whatsapp/send_media.py \
    --phone 5531980160822 \
    --file ~/Downloads/notificacao_compra.mp3 \
    --type audio
```

### Nextcloud (Upload e Compartilhamento)

```bash
# 1. Gera áudio
python3 scripts/audio-generation/generate_elevenlabs.py \
    "Áudio para compartilhar" \
    --output audio_compartilhar

# 2. Upload para Nextcloud
python3 scripts/nextcloud/upload_to_nextcloud.py \
    ~/Downloads/audio_compartilhar.mp3
```

---

## 📝 Notas Finais

### Ferramentas Relacionadas

- **Transcrição de áudio:** `tools/transcribe_universal.py`
- **Geração de imagens:** `scripts/image-generation/`
- **WhatsApp:** `scripts/whatsapp/`

### Documentação Adicional

- **Ferramenta base:** `tools/generate_audio_elevenlabs.py`
- **Ferramenta batch base:** `tools/generate_audio_batch_elevenlabs.py`
- **Docs ElevenLabs:** https://docs.elevenlabs.io/

### Suporte

Para problemas ou dúvidas:
1. Verifique este README
2. Execute com `--help` para ver opções
3. Teste com textos curtos primeiro
4. Verifique logs de erro detalhados

---

**Última atualização:** 2025-11-02
**Versão:** 1.0
**Templates testados e funcionais:** 2/2 ✅
