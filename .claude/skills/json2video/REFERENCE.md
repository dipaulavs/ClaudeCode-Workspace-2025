# JSON2Video - Referência Técnica Completa

## API Authentication

**Header obrigatório:**
```
x-api-key: YOUR_API_KEY
```

**Obter API key:** Dashboard em json2video.com após criar conta

## Movie Schema (Top-level)

```json
{
  "resolution": "portrait | landscape | square | vertical | custom",
  "width": 1080,
  "height": 1920,
  "quality": "high | medium | low",
  "fps": 30,
  "draft": false,
  "cache": true,
  "comment": "Project description",
  "webhook": "https://your-webhook.com/callback",
  "scenes": []
}
```

### Resolutions

| Name | Dimensions | Uso |
|------|------------|-----|
| `portrait` | 1080x1920 | Stories, Reels |
| `landscape` | 1920x1080 | YouTube horizontal |
| `square` | 1080x1080 | Posts Instagram |
| `vertical` | 1080x1350 | Posts Instagram vertical |
| `custom` | Definir width/height | Customizado |

## Scene Schema

```json
{
  "comment": "Scene description",
  "duration": 5.0,
  "background-color": "#000000",
  "background-image": "https://url.com/bg.jpg",
  "background-video": "https://url.com/bg.mp4",
  "transition": "fade | circleopen | crosswarp",
  "elements": []
}
```

### Transitions

- `fade` - Fade in/out
- `circleopen` - Círculo expandindo
- `crosswarp` - Distorção cruzada
- `doorway` - Efeito porta
- `dreamy` - Efeito sonho

## Elements Types

### 1. Text

```json
{
  "type": "text",
  "text": "Hello World",
  "style": "001",
  "x": "center",
  "y": "center",
  "xs": 0,
  "ys": 0,
  "width": "100%",
  "height": "auto",
  "color": "#ffffff",
  "background-color": "rgba(0,0,0,0.5)",
  "font-family": "Montserrat",
  "font-size": 60,
  "font-weight": "bold",
  "align": "center",
  "animation": "fade-in",
  "duration": 3.0,
  "start": 0.5
}
```

**Text Styles:** `001` a `020` (pré-definidos)

**Animations:**
- `fade-in`, `fade-out`
- `slide-left`, `slide-right`, `slide-up`, `slide-down`
- `zoom-in`, `zoom-out`
- `rotate-in`, `rotate-out`

### 2. Image

```json
{
  "type": "image",
  "src": "https://url.com/image.jpg",
  "x": "center",
  "y": "center",
  "width": "80%",
  "height": "auto",
  "fit": "cover | contain | fill",
  "animation": "ken-burns",
  "duration": 5.0,
  "start": 0
}
```

### 3. Video

```json
{
  "type": "video",
  "src": "https://url.com/video.mp4",
  "trim-start": 2.5,
  "trim-end": 10.0,
  "volume": 0.8,
  "x": 0,
  "y": 0,
  "width": "100%",
  "height": "100%"
}
```

### 4. Audio

```json
{
  "type": "audio",
  "src": "https://url.com/soundtrack.mp3",
  "volume": 0.5,
  "fade-in": 1.0,
  "fade-out": 2.0,
  "loop": true
}
```

### 5. Voice (Text-to-Speech)

```json
{
  "type": "voice",
  "text": "This is a voice-over",
  "provider": "elevenlabs",
  "voice": "Rachel",
  "model": "eleven_multilingual_v2",
  "language": "pt",
  "start": 0
}
```

**Providers:**
- `elevenlabs` - ElevenLabs (alta qualidade)
- `azure` - Azure TTS
- `google` - Google Cloud TTS

### 6. Subtitles (Auto)

```json
{
  "type": "subtitles",
  "auto": true,
  "style": "001",
  "color": "#ffffff",
  "background-color": "rgba(0,0,0,0.7)",
  "font-size": 40,
  "max-words": 5
}
```

### 7. Audiogram

```json
{
  "type": "audiogram",
  "src": "https://url.com/audio.mp3",
  "bars": 50,
  "color": "#00ff00",
  "symmetry": true,
  "x": "center",
  "y": "bottom",
  "width": "90%",
  "height": 200
}
```

## Positioning System

**X/Y valores:**
- Pixels: `100`, `500`
- Percentual: `"50%"`
- Named: `"center"`, `"left"`, `"right"`, `"top"`, `"bottom"`

**Offset (xs/ys):** Ajuste fino após posicionamento
```json
{
  "x": "center",
  "xs": 20,  // 20px para direita
  "y": "top",
  "ys": 50   // 50px para baixo
}
```

## Variables & Expressions

**Definir variáveis:**
```json
{
  "variables": {
    "name": "John",
    "score": 95
  },
  "scenes": [
    {
      "elements": [
        {
          "type": "text",
          "text": "Hello {{name}}! Score: {{score}}"
        }
      ]
    }
  ]
}
```

**Expressões:**
```json
{
  "text": "Total: {{price * quantity}}"
}
```

## Conditional Rendering

```json
{
  "type": "text",
  "text": "Winner!",
  "condition": "{{score >= 90}}"
}
```

## Duration & Timing

**Scene duration:**
- Automático: Duração do elemento mais longo
- Manual: `"duration": 5.0` (segundos)

**Element timing:**
- `start`: Delay inicial (segundos)
- `duration`: Duração do elemento
- `end`: Tempo de término (alternativa a duration)

## Cache System

```json
{
  "cache": true,  // Top-level
  "scenes": [
    {
      "cache": "scene_01",  // Cache ID
      "elements": []
    }
  ]
}
```

**Benefício:** Re-renderizações rápidas quando usar mesmo cache ID.

## Webhooks

```json
{
  "webhook": "https://your-webhook.com/callback"
}
```

**Payload enviado:**
```json
{
  "project": "abc123",
  "status": "done",
  "url": "https://assets.json2video.com/.../video.mp4",
  "duration": 30.5,
  "width": 1080,
  "height": 1920
}
```

## Export Options

**FTP/SFTP Upload:**
```json
{
  "ftp": {
    "host": "ftp.example.com",
    "username": "user",
    "password": "pass",
    "path": "/videos/"
  }
}
```

**Email notification:**
```json
{
  "email": "user@example.com"
}
```

## Quality Settings

| Quality | Bitrate | Uso |
|---------|---------|-----|
| `low` | 1 Mbps | Preview rápido |
| `medium` | 3 Mbps | Social media |
| `high` | 8 Mbps | Produção final |

## Rate Limits

- **Quota:** Baseada em tempo de renderização (não duração do vídeo)
- **Concurrent jobs:** Máximo 5 simultâneos (plano padrão)
- **Response time:** Status endpoint pode levar 30-120s dependendo da fila

## Error Codes

| Status | Significado |
|--------|-------------|
| `200` | Sucesso |
| `400` | JSON inválido ou parâmetros incorretos |
| `401` | API key inválida/ausente |
| `403` | Quota esgotada |
| `404` | Project ID não encontrado |
| `429` | Rate limit excedido |
| `500` | Erro interno do servidor |

## SDKs

- **NodeJS:** https://github.com/JSON2Video/json2video-nodejs-sdk
- **PHP:** https://github.com/JSON2Video/json2video-php-sdk
- **Python:** Em desenvolvimento (usar REST API direto)

## Links Úteis

- **Template Editor:** https://json2video.com/docs/editor/
- **API Docs:** https://json2video.com/docs/v2/
- **Dashboard:** https://json2video.com/dashboard
- **Pricing:** https://json2video.com/pricing
