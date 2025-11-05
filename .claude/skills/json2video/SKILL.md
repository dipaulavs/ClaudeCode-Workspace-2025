# JSON2Video - Edição de Vídeo via JSON

Cria e edita vídeos programaticamente usando a API JSON2Video.

## Quando Usar

- Criar vídeos dinâmicos com texto/imagens/áudio
- Gerar legendas automáticas
- Criar audiogramas (waveform visual)
- Slideshows com transições
- Voice-over com ElevenLabs
- Adicionar watermarks/overlays
- Vídeos em lote com templates

## Workflow

```
1. JSON Definition → 2. POST /movies → 3. GET status → 4. Download URL
   (scenes/elements)   (project_id)     (polling)      (video.mp4)
```

## API Endpoints

**Base URL:** `https://api.json2video.com/v2`

**1. Criar Vídeo (POST /movies)**
```bash
curl -X POST https://api.json2video.com/v2/movies \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @video.json
```

**Response:**
```json
{
  "success": true,
  "project": "abc123",
  "timestamp": "2025-01-04T10:00:00Z"
}
```

**2. Checar Status (GET /movies?project=ID)**
```bash
curl https://api.json2video.com/v2/movies?project=abc123 \
  -H "x-api-key: YOUR_API_KEY"
```

**Response:**
```json
{
  "success": true,
  "movie": {
    "status": "done",
    "url": "https://assets.json2video.com/.../video.mp4",
    "duration": 30.5,
    "width": 1080,
    "height": 1920
  },
  "remaining_quota": {"time": 1807}
}
```

**Status:** `pending` → `running` → `done` | `error`

## Estrutura JSON Básica

```json
{
  "resolution": "portrait",
  "quality": "high",
  "scenes": [
    {
      "background-color": "#000000",
      "elements": [
        {
          "type": "text",
          "text": "Hello World",
          "style": "001"
        }
      ]
    }
  ]
}
```

## Elementos Disponíveis

| Tipo | Uso |
|------|-----|
| `text` | Textos animados |
| `image` | Imagens estáticas/animadas |
| `video` | Clips de vídeo |
| `audio` | Trilha sonora |
| `voice` | Voice-over (TTS) |
| `composition` | Sub-composições |

## Features Avançadas

- **Legendas automáticas:** `"subtitles": {"auto": true}`
- **Audiograma:** Waveform visual de áudio
- **Variáveis:** `{{variable_name}}` para templates
- **Expressões:** Cálculos dinâmicos
- **Conditional rendering:** Mostrar/ocultar elementos
- **Cache:** Otimização de renderização

## Python Template

```bash
python3 scripts/video-generation/edit_json2video.py video.json
```

Ver `EXAMPLES.md` para casos de uso completos.
Ver `REFERENCE.md` para documentação técnica detalhada.
Ver `TROUBLESHOOTING.md` para erros comuns.

## Custo

Baseado em tempo de renderização (não duração do vídeo).
Ver dashboard para quota restante.
