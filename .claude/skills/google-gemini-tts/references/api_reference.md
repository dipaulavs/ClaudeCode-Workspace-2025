# Google Gemini TTS - Referência Completa

## Vozes Disponíveis (30 total)

### Vozes Masculinas (16)

| Nome | Personalidade | Uso Recomendado |
|------|--------------|-----------------|
| **Puck** | Upbeat | ✅ **Conversacional casual** - Tom animado mas natural |
| **Zubenelgenubi** | Casual | ✅ **Conversacional casual** - Muito relaxado |
| **Achird** | Friendly | ✅ **Conversacional casual** - Amigável e próximo |
| **Umbriel** | Easy-going | ✅ **Conversacional casual** - Descontraído |
| Charon | Informative | Narração educacional |
| Fenrir | Excitable | Apresentação energética |
| Orus | Firm | Autoridade/seriedade |
| Algenib | Gravelly | Voz rouca/madura |
| Algieba | Smooth | Voz suave profissional |
| Alnilam | Firm | Tom autoritário |
| Enceladus | Breathy | Intimista/sussurrado |
| Iapetus | Clear | Clareza profissional |
| Rasalgethi | Informative | Explicativo/didático |
| Sadachbia | Lively | Vivaz/animado |
| Sadaltager | Knowledgeable | Especialista/professor |
| Schedar | Even | Tom equilibrado neutro |

### Vozes Femininas (14)

| Nome | Personalidade | Uso Recomendado |
|------|--------------|-----------------|
| **Callirrhoe** | Easy-going | ✅ **Conversacional casual** - Relaxada e natural |
| **Aoede** | Breezy | ✅ **Conversacional casual** - Leve e descontraída |
| **Vindemiatrix** | Gentle | ✅ **Conversacional casual** - Suave e amigável |
| **Zephyr** | Bright | ✅ **Conversacional casual** - Alegre sem exagero |
| Kore | Firm | Assertiva/profissional |
| Leda | Youthful | Jovem/energética |
| Autonoe | Bright | Brilhante/clara |
| Despina | Smooth | Suave profissional |
| Erinome | Clear | Clareza profissional |
| Achernar | Soft | Suave/delicada |
| Gacrux | Mature | Madura/experiente |
| Laomedeia | Upbeat | Animada/positiva |
| Pulcherrima | Forward | Direta/assertiva |
| Sulafat | Warm | Calorosa/acolhedora |

## Bracket Tags (Marcadores de Emoção)

### Efeitos Vocais

```
[laughing]          - Riso natural
[sighing]           - Suspiro
[clears throat]     - Limpar garganta
[uhm]               - Hesitação pensativa
```

### Tons Emocionais

```
[angry]             - Raiva
[excited]           - Empolgado
[sarcastic]         - Sarcástico
[empathetic]        - Empático
[scornful]          - Desdenhoso
```

### Estilos de Fala

```
[whispering]        - Sussurrando
[shouting]          - Gritando
[speaking slowly]   - Falando devagar
[extremely fast]    - Muito rápido
[robotic]           - Tom robótico
```

### Pausas

```
[short pause]       - Pausa curta (~0.5s)
[medium pause]      - Pausa média (~1s)
[long pause]        - Pausa longa (~2s)
[PAUSE=2s]          - Pausa customizada
```

## SSML Tags Suportadas

### Pausas

```xml
<break time="2s"/>              - Pausa de 2 segundos
<break time="500ms"/>           - Pausa de 500 milissegundos
```

### Controle de Voz

```xml
<prosody rate="slow">texto</prosody>              - Velocidade lenta
<prosody rate="fast">texto</prosody>              - Velocidade rápida
<prosody pitch="low">texto</prosody>              - Tom grave
<prosody pitch="high">texto</prosody>             - Tom agudo
<prosody volume="loud">texto</prosody>            - Volume alto
<prosody volume="soft">texto</prosody>            - Volume baixo
```

### Ênfase

```xml
<emphasis level="strong">palavra</emphasis>       - Ênfase forte
<emphasis level="moderate">palavra</emphasis>     - Ênfase moderada
<emphasis level="reduced">palavra</emphasis>      - Ênfase reduzida
```

### Pronúncia

```xml
<say-as interpret-as="date" format="mdy">12/25/2024</say-as>
<say-as interpret-as="characters">ABC</say-as>
<sub alias="International Business Machines">IBM</sub>
<phoneme alphabet="ipa" ph="təˈmeɪtoʊ">tomato</phoneme>
```

### Mudança de Idioma

```xml
<lang xml:lang="pt-BR">Olá mundo</lang>
<lang xml:lang="en-US">Hello world</lang>
<lang xml:lang="es-ES">Hola mundo</lang>
```

## Limitações Técnicas

| Parâmetro | Limite |
|-----------|--------|
| Texto máximo | 4.000 bytes |
| Prompt máximo | 4.000 bytes |
| Total combinado | 8.000 bytes |
| Duração output | ~655 segundos |
| Rate limit (free) | 10 req/min |
| Tokens/min (free) | 250k |
| Requests/dia (free) | 250 |

## Formatos de Áudio

| Formato | Qualidade | Tamanho | Uso |
|---------|-----------|---------|-----|
| **PCM** | Máxima | Grande | Processamento |
| **LINEAR16** | Máxima | Grande | Sem compressão |
| **WAV** | Alta | Médio | Padrão (24kHz, 16-bit, mono) |
| **MP3** | Boa | Pequeno | Distribuição web |
| **OGG_OPUS** | Muito boa | Muito pequeno | Melhor custo-benefício |

## Modelos Disponíveis

### gemini-2.5-flash-preview-tts

- ⚡ **Velocidade:** Mais rápido
- 💰 **Custo:** ~$0.005-0.01 por request
- 🎯 **Uso:** Aplicações em tempo real, alta demanda

### gemini-2.5-pro-preview-tts

- 🎨 **Qualidade:** Melhor controle emocional
- 💰 **Custo:** ~$0.01-0.02 por request
- 🎯 **Uso:** Conteúdo premium, emoções complexas

## Idiomas Suportados (23 GA + 50+ Preview)

### Disponibilidade Geral (GA)

- 🇺🇸 English (US/India)
- 🇧🇷 Português (Brasil)
- 🇪🇸 Español (España)
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇮🇹 Italiano
- 🇯🇵 日本語
- 🇰🇷 한국어
- 🇮🇳 हिन्दी / मराठी / தமிழ் / తెలుగు
- 🇸🇦 العربية (مصر)
- E mais 10 idiomas

### Preview (50+ idiomas)

Inclui variantes regionais: pt-PT, es-US, es-MX, fr-CA, zh-CN, zh-TW, etc.

## Best Practices para Voz Conversacional Casual

### ✅ Fazer

1. **Pausas naturais**: Adicionar `[short pause]` em vírgulas/pontos
2. **Respirações ocasionais**: `[short pause]` a cada 2-3 frases
3. **Prompt casual**: Mencionar "conversa entre amigos" ou "telefone casual"
4. **Vozes recomendadas**: Usar Puck, Zubenelgenubi, Achird (male) ou Callirrhoe, Aoede (female)
5. **Combinar técnicas**: Bracket tags + prompt natural + pausas

### ❌ Evitar

1. **Energia exagerada**: Não usar vozes "Excited" ou "Lively" para casual
2. **Tom robótico**: Evitar frases muito curtas sem pausas
3. **Tags ambientais**: `[crowd laughing]` não funciona (só efeitos individuais)
4. **Textos longos sem chunks**: Quebrar textos >500 palavras
5. **Múltiplas tags seguidas**: Podem ser lidas literalmente

## Exemplos de Prompts Casuais

### Podcast Informal

```
"Fale como em um podcast descontraído entre amigos. Tom casual,
pausas naturais, sem energia de apresentador. Conversa relaxada
e próxima. [short pause] Texto: {seu_texto}"
```

### Conversa Telefônica

```
"Fale como em uma ligação telefônica casual com um amigo próximo.
Tom natural, respiração normal, sem pressa. Como quem está
conversando descontraído. [short pause] Texto: {seu_texto}"
```

### Storytelling Casual

```
"Conte de forma super natural, como quem está contando uma história
para amigos. Pausas naturais [short pause], respirações ocasionais,
tom próximo e autêntico. Texto: {seu_texto}"
```

## Autenticação

### Via Environment Variable (Recomendado)

```bash
export GEMINI_API_KEY="AIzaSy..."
```

### Via Código Python

```python
from google import genai
client = genai.Client(api_key="AIzaSy...")
```

## Conversão de Formatos

### WAV → MP3 (pydub)

```python
from pydub import AudioSegment
audio = AudioSegment.from_wav("input.wav")
audio.export("output.mp3", format="mp3", bitrate="128k")
```

### WAV → MP3 (ffmpeg)

```bash
ffmpeg -i input.wav -codec:a libmp3lame -b:a 128k output.mp3
```

### WAV → OGG_OPUS (ffmpeg)

```bash
ffmpeg -i input.wav -codec:a libopus -b:a 64k output.ogg
```

## Troubleshooting

### Erro: "API key not valid"

- Verificar se a chave começa com `AIza`
- Confirmar que tem ~39 caracteres
- Validar no Google AI Studio

### Erro: "Rate limit exceeded"

- Aguardar 60 segundos
- Considerar upgrade para paid tier
- Usar batching para múltiplas requisições

### Áudio soa robótico/artificial

- Adicionar mais pausas `[short pause]`
- Usar prompt mais conversacional
- Testar voz diferente (Zubenelgenubi, Callirrhoe)
- Adicionar `[short pause]` entre frases

### Tags sendo lidas literalmente

- Quebrar texto em chunks menores
- Reduzir número de tags por frase
- Usar SSML alternativo (`<break time="1s"/>`)
