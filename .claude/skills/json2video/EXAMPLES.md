# JSON2Video - Exemplos Práticos

## Exemplo 1: Slideshow de Imagens

**Caso de uso:** Criar vídeo com 3 imagens + música de fundo

```json
{
  "resolution": "portrait",
  "quality": "high",
  "scenes": [
    {
      "comment": "Imagem 1",
      "duration": 3.0,
      "background-color": "#000000",
      "transition": "fade",
      "elements": [
        {
          "type": "image",
          "src": "https://example.com/image1.jpg",
          "x": "center",
          "y": "center",
          "width": "100%",
          "height": "100%",
          "fit": "cover",
          "animation": "ken-burns"
        },
        {
          "type": "text",
          "text": "Momento 1",
          "style": "001",
          "x": "center",
          "y": "bottom",
          "ys": -100,
          "animation": "fade-in"
        }
      ]
    },
    {
      "comment": "Imagem 2",
      "duration": 3.0,
      "transition": "circleopen",
      "elements": [
        {
          "type": "image",
          "src": "https://example.com/image2.jpg",
          "x": "center",
          "y": "center",
          "width": "100%",
          "height": "100%",
          "fit": "cover",
          "animation": "zoom-in"
        },
        {
          "type": "text",
          "text": "Momento 2",
          "style": "001",
          "x": "center",
          "y": "bottom",
          "ys": -100,
          "animation": "slide-up"
        }
      ]
    },
    {
      "comment": "Imagem 3",
      "duration": 3.0,
      "transition": "crosswarp",
      "elements": [
        {
          "type": "image",
          "src": "https://example.com/image3.jpg",
          "x": "center",
          "y": "center",
          "width": "100%",
          "height": "100%",
          "fit": "cover"
        },
        {
          "type": "text",
          "text": "Momento 3",
          "style": "001",
          "x": "center",
          "y": "bottom",
          "ys": -100,
          "animation": "fade-in"
        }
      ]
    }
  ],
  "soundtrack": {
    "type": "audio",
    "src": "https://example.com/music.mp3",
    "volume": 0.3,
    "fade-in": 1.0,
    "fade-out": 2.0
  }
}
```

**Resultado:** Vídeo de 9s com 3 imagens animadas + texto + música de fundo

---

## Exemplo 2: Vídeo com Legendas Automáticas

**Caso de uso:** Vídeo falado com legendas auto-geradas

```json
{
  "resolution": "portrait",
  "quality": "high",
  "scenes": [
    {
      "background-color": "#1a1a1a",
      "elements": [
        {
          "type": "video",
          "src": "https://example.com/video.mp4",
          "x": "center",
          "y": "center",
          "width": "100%",
          "height": "100%"
        },
        {
          "type": "subtitles",
          "auto": true,
          "style": "001",
          "color": "#ffffff",
          "background-color": "rgba(0,0,0,0.8)",
          "font-size": 50,
          "font-weight": "bold",
          "max-words": 4,
          "y": "bottom",
          "ys": -150
        }
      ]
    }
  ]
}
```

**Resultado:** Vídeo com legendas automáticas estilo TikTok/Reels

---

## Exemplo 3: Audiograma (Podcast Visual)

**Caso de uso:** Transformar áudio de podcast em vídeo visual

```json
{
  "resolution": "square",
  "quality": "high",
  "scenes": [
    {
      "background-color": "#0a0a0a",
      "elements": [
        {
          "type": "image",
          "src": "https://example.com/podcast-cover.jpg",
          "x": "center",
          "y": "center",
          "ys": -200,
          "width": 300,
          "height": 300,
          "border-radius": 150
        },
        {
          "type": "text",
          "text": "Episódio #42",
          "font-family": "Montserrat",
          "font-size": 40,
          "font-weight": "bold",
          "color": "#ffffff",
          "x": "center",
          "y": "center",
          "ys": 150
        },
        {
          "type": "text",
          "text": "Como Crescer no Instagram",
          "font-family": "Montserrat",
          "font-size": 28,
          "color": "#cccccc",
          "x": "center",
          "y": "center",
          "ys": 200
        },
        {
          "type": "audiogram",
          "src": "https://example.com/podcast-ep42.mp3",
          "bars": 60,
          "color": "#00ff88",
          "symmetry": true,
          "x": "center",
          "y": "bottom",
          "ys": -100,
          "width": "90%",
          "height": 150
        },
        {
          "type": "audio",
          "src": "https://example.com/podcast-ep42.mp3",
          "volume": 1.0
        }
      ]
    }
  ]
}
```

**Resultado:** Vídeo quadrado com cover + waveform animado + áudio

---

## Exemplo 4: Voice-Over com ElevenLabs

**Caso de uso:** Criar narração automática para vídeo explicativo

```json
{
  "resolution": "landscape",
  "quality": "high",
  "scenes": [
    {
      "background-color": "#ffffff",
      "duration": 8.0,
      "elements": [
        {
          "type": "text",
          "text": "Como Funciona?",
          "style": "003",
          "x": "center",
          "y": "center",
          "ys": -200,
          "color": "#000000",
          "font-size": 80,
          "animation": "fade-in"
        },
        {
          "type": "image",
          "src": "https://example.com/diagram.png",
          "x": "center",
          "y": "center",
          "ys": 100,
          "width": "70%",
          "animation": "zoom-in",
          "start": 1.0
        },
        {
          "type": "voice",
          "text": "Nosso sistema funciona em três etapas simples: primeiro você envia os dados, depois processamos automaticamente, e por fim você recebe os resultados em tempo real.",
          "provider": "elevenlabs",
          "voice": "Rachel",
          "model": "eleven_multilingual_v2",
          "language": "pt"
        }
      ]
    }
  ]
}
```

**Resultado:** Vídeo com narração profissional em português + animações

---

## Exemplo 5: Template com Variáveis

**Caso de uso:** Criar múltiplos vídeos personalizados

**Template JSON:**
```json
{
  "resolution": "portrait",
  "quality": "high",
  "variables": {
    "name": "João",
    "score": 95,
    "rank": "1º"
  },
  "scenes": [
    {
      "background-color": "#1e3a8a",
      "elements": [
        {
          "type": "text",
          "text": "Parabéns {{name}}!",
          "style": "001",
          "x": "center",
          "y": "center",
          "ys": -200,
          "color": "#fbbf24",
          "font-size": 70,
          "animation": "zoom-in"
        },
        {
          "type": "text",
          "text": "Sua pontuação: {{score}}",
          "font-family": "Montserrat",
          "font-size": 50,
          "color": "#ffffff",
          "x": "center",
          "y": "center",
          "animation": "slide-up",
          "start": 1.0
        },
        {
          "type": "text",
          "text": "Você ficou em {{rank}} lugar!",
          "font-family": "Montserrat",
          "font-size": 40,
          "color": "#10b981",
          "x": "center",
          "y": "center",
          "ys": 150,
          "animation": "fade-in",
          "start": 2.0
        },
        {
          "type": "image",
          "src": "https://example.com/trophy.png",
          "x": "center",
          "y": "bottom",
          "ys": -150,
          "width": 200,
          "animation": "zoom-in",
          "start": 2.5
        }
      ]
    }
  ]
}
```

**Uso em lote (Python):**
```python
users = [
    {"name": "João", "score": 95, "rank": "1º"},
    {"name": "Maria", "score": 92, "rank": "2º"},
    {"name": "Pedro", "score": 88, "rank": "3º"}
]

for user in users:
    video_json["variables"] = user
    # Renderizar vídeo personalizado
```

**Resultado:** 3 vídeos personalizados com nomes/scores diferentes

---

## Exemplo 6: Vídeo Promocional com Múltiplas Scenes

**Caso de uso:** Anúncio de produto com 3 seções

```json
{
  "resolution": "portrait",
  "quality": "high",
  "scenes": [
    {
      "comment": "Intro - Problema",
      "duration": 4.0,
      "background-color": "#dc2626",
      "transition": "fade",
      "elements": [
        {
          "type": "text",
          "text": "Cansado de perder tempo?",
          "style": "001",
          "x": "center",
          "y": "center",
          "color": "#ffffff",
          "font-size": 60,
          "animation": "zoom-in"
        }
      ]
    },
    {
      "comment": "Solução",
      "duration": 5.0,
      "background-color": "#0891b2",
      "transition": "circleopen",
      "elements": [
        {
          "type": "text",
          "text": "Conheça nossa solução!",
          "style": "002",
          "x": "center",
          "y": "center",
          "ys": -250,
          "color": "#ffffff",
          "font-size": 50
        },
        {
          "type": "image",
          "src": "https://example.com/product.png",
          "x": "center",
          "y": "center",
          "width": "80%",
          "animation": "slide-up",
          "start": 0.5
        }
      ]
    },
    {
      "comment": "CTA",
      "duration": 4.0,
      "background-color": "#16a34a",
      "transition": "crosswarp",
      "elements": [
        {
          "type": "text",
          "text": "Acesse Agora!",
          "style": "001",
          "x": "center",
          "y": "center",
          "ys": -100,
          "color": "#ffffff",
          "font-size": 70,
          "animation": "zoom-in"
        },
        {
          "type": "text",
          "text": "www.exemplo.com.br",
          "font-family": "Montserrat",
          "font-size": 40,
          "color": "#ffffff",
          "x": "center",
          "y": "center",
          "ys": 100,
          "animation": "fade-in",
          "start": 1.0
        }
      ]
    }
  ]
}
```

**Resultado:** Vídeo promocional de 13s (Problema → Solução → CTA)

---

## Exemplo 7: Watermark Persistente

**Caso de uso:** Logo em todas as cenas

```json
{
  "resolution": "portrait",
  "quality": "high",
  "watermark": {
    "type": "image",
    "src": "https://example.com/logo.png",
    "x": "right",
    "xs": -20,
    "y": "top",
    "ys": 20,
    "width": 120,
    "opacity": 0.8
  },
  "scenes": [
    {
      "elements": [
        {
          "type": "video",
          "src": "https://example.com/content.mp4"
        }
      ]
    }
  ]
}
```

**Resultado:** Logo aparece em todas as scenes do vídeo
