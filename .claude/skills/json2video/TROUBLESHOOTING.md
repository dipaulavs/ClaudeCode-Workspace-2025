# JSON2Video - Troubleshooting

## Erro 1: "401 Unauthorized"

**Sintoma:**
```json
{
  "success": false,
  "error": "Unauthorized"
}
```

**Causas:**
- API key ausente no header
- API key incorreta
- API key expirada

**Solução:**
```bash
# Verificar se header está correto
curl -X POST https://api.json2video.com/v2/movies \
  -H "x-api-key: SUA_API_KEY_AQUI" \
  -H "Content-Type: application/json" \
  -d @video.json

# Obter nova API key:
# 1. Login em json2video.com
# 2. Dashboard → API Keys → Generate New Key
```

---

## Erro 2: "403 Quota Exceeded"

**Sintoma:**
```json
{
  "success": false,
  "error": "Quota exceeded"
}
```

**Causa:** Tempo de renderização esgotado no plano atual

**Solução:**
```bash
# Checar quota restante
curl https://api.json2video.com/v2/movies?project=SEU_PROJECT_ID \
  -H "x-api-key: SUA_API_KEY"

# Response mostra:
{
  "remaining_quota": {"time": 0}  # Esgotado!
}

# Opções:
# 1. Aguardar reset mensal
# 2. Upgrade de plano em json2video.com/pricing
# 3. Usar "draft": true para previews (gasta menos quota)
```

---

## Erro 3: "400 Invalid JSON"

**Sintoma:**
```json
{
  "success": false,
  "error": "Invalid movie schema",
  "details": "scenes is required"
}
```

**Causas:**
- JSON malformado (sintaxe errada)
- Campos obrigatórios ausentes
- Tipos de dados incorretos

**Solução:**
```bash
# Validar JSON antes de enviar
python3 -m json.tool video.json  # Se falhar, JSON inválido

# Estrutura mínima obrigatória:
{
  "scenes": [
    {
      "elements": [
        {
          "type": "text",
          "text": "Hello"
        }
      ]
    }
  ]
}

# Campos obrigatórios:
# - scenes[] (array não vazio)
# - elements[] dentro de cada scene
# - type em cada element
```

---

## Erro 4: "Status stuck em 'pending'"

**Sintoma:**
Após 5+ minutos, status ainda é `pending`

**Causas:**
- Fila de renderização cheia (horários de pico)
- Vídeo muito complexo
- Problema temporário no servidor

**Solução:**
```python
import time
import requests

def wait_for_video(project_id, max_wait=600):
    """Aguarda até 10 minutos"""
    start_time = time.time()

    while time.time() - start_time < max_wait:
        response = requests.get(
            f"https://api.json2video.com/v2/movies?project={project_id}",
            headers={"x-api-key": "YOUR_API_KEY"}
        )

        data = response.json()
        status = data["movie"]["status"]

        print(f"Status: {status} ({int(time.time() - start_time)}s)")

        if status == "done":
            return data["movie"]["url"]
        elif status == "error":
            raise Exception(data["movie"]["message"])

        time.sleep(10)  # Checar a cada 10s

    raise TimeoutError("Video rendering timeout")

# Uso:
video_url = wait_for_video("abc123")
```

---

## Erro 5: "Element not showing in video"

**Sintoma:**
Vídeo renderiza mas elemento específico não aparece

**Causas comuns:**

**1. Start time maior que scene duration**
```json
{
  "duration": 5.0,  // Scene dura 5s
  "elements": [
    {
      "type": "text",
      "text": "Hello",
      "start": 6.0  // ❌ Começa após fim da scene!
    }
  ]
}

// Solução: start < duration
{
  "start": 2.0  // ✅ Aparece aos 2s
}
```

**2. Elemento fora da tela**
```json
{
  "type": "text",
  "text": "Hello",
  "x": 5000,  // ❌ Muito longe da tela (1080px)
  "y": -500   // ❌ Acima da tela
}

// Solução: usar valores válidos
{
  "x": "center",  // ✅ ou 0-1080 para portrait
  "y": "center"
}
```

**3. Elemento sob outro elemento**
```json
{
  "elements": [
    {
      "type": "image",
      "src": "bg.jpg",
      "width": "100%",
      "height": "100%",
      "z-index": 10  // Cobre tudo
    },
    {
      "type": "text",
      "text": "Hello",
      "z-index": 1  // ❌ Atrás da imagem!
    }
  ]
}

// Solução: ajustar z-index
{
  "z-index": 20  // ✅ Na frente
}
```

---

## Erro 6: "Audio/Video source not accessible"

**Sintoma:**
```json
{
  "status": "error",
  "message": "Unable to fetch https://example.com/video.mp4"
}
```

**Causas:**
- URL inválida ou inacessível
- Arquivo privado (requer autenticação)
- CORS bloqueando
- URL expirada (signed URLs)

**Solução:**
```bash
# 1. Testar URL manualmente
curl -I https://example.com/video.mp4
# Deve retornar 200 OK

# 2. URLs devem ser públicas
# ❌ Não funciona: Dropbox private links
# ❌ Não funciona: Google Drive shared links
# ✅ Funciona: Nextcloud public links
# ✅ Funciona: S3 pre-signed URLs (antes expirar)
# ✅ Funciona: URLs diretas públicas

# 3. Upload para Nextcloud:
python3 scripts/nextcloud/upload_rapido.py --from-local
# Retorna URL pública permanente
```

---

## Erro 7: "Voice rendering failed"

**Sintoma:**
Voice-over não gera ou vídeo falha

**Causas:**
- Texto muito longo (limite: ~5000 caracteres)
- Idioma não suportado
- Voz não existe
- API key ElevenLabs inválida (se provider=elevenlabs)

**Solução:**
```json
// ❌ Texto muito longo
{
  "type": "voice",
  "text": "Lorem ipsum..." // 10000 caracteres
}

// ✅ Quebrar em múltiplas scenes
{
  "scenes": [
    {
      "elements": [
        {
          "type": "voice",
          "text": "Parte 1 do texto..."  // ~1000 chars
        }
      ]
    },
    {
      "elements": [
        {
          "type": "voice",
          "text": "Parte 2 do texto..."  // ~1000 chars
        }
      ]
    }
  ]
}

// Vozes válidas ElevenLabs:
// Rachel, Clyde, Domi, Dave, Fin, Sarah, Antoni, Thomas, Charlie, Emily, Elli, Josh, Arnold, Adam, Sam
```

---

## Erro 8: "Subtitles not appearing"

**Sintoma:**
`"auto": true` mas legendas não aparecem

**Causas:**
- Vídeo/áudio sem fala detectável
- Idioma errado
- Audio muito baixo

**Solução:**
```json
// Especificar idioma explicitamente
{
  "type": "subtitles",
  "auto": true,
  "language": "pt",  // Português
  "style": "001",
  "max-words": 4
}

// Aumentar volume se necessário
{
  "type": "video",
  "src": "video.mp4",
  "volume": 1.5  // 150% do original
}

// Verificar se há fala no vídeo
// Transcrever manualmente primeiro:
python3 scripts/extraction/transcribe_video.py "video_url"
// Se transcrição vazia → sem fala detectada
```

---

## Erro 9: "Video quality is low"

**Sintoma:**
Vídeo final pixelado ou com artefatos

**Causas:**
- `quality: "low"` ou `"medium"`
- Source images/videos de baixa resolução
- `draft: true` ativado

**Solução:**
```json
// Usar quality: "high"
{
  "quality": "high",  // ✅ Máxima qualidade
  "draft": false,     // ✅ Renderização final
  "fps": 30           // ✅ Smooth
}

// Source files devem ter boa resolução:
// - Imagens: Mínimo 1080px na menor dimensão
// - Vídeos: 1080p ou superior
// - Evitar upscaling (usar tamanho original)
```

---

## Erro 10: "Webhook not receiving callback"

**Sintoma:**
Vídeo renderiza mas webhook nunca é chamado

**Causas:**
- URL inválida
- Servidor webhook offline
- Firewall bloqueando
- Timeout no webhook (>30s)

**Solução:**
```json
// 1. Testar webhook URL
// Usar webhook.site para debug:
{
  "webhook": "https://webhook.site/seu-unique-id"
}

// 2. Webhook deve responder <30s
// Processar assíncrono:
# webhook_receiver.py
@app.post("/webhook")
async def receive(data: dict):
    # ✅ Retornar imediatamente
    asyncio.create_task(process_video(data))
    return {"success": true}

# ❌ Não fazer:
@app.post("/webhook")
def receive(data: dict):
    download_video(data["url"])  # Demora 2 minutos!
    return {"success": true}
```

---

## Dicas de Performance

**1. Usar cache para elementos repetidos:**
```json
{
  "cache": true,
  "scenes": [
    {"cache": "intro", "elements": [...]},  // Renderiza
    {"cache": "intro", "elements": [...]}   // Reusa cache (rápido!)
  ]
}
```

**2. Draft mode para testes:**
```json
{
  "draft": true,  // 50% mais rápido, qualidade reduzida
  "quality": "low"
}
```

**3. Polling inteligente:**
```python
# Não ficar fazendo request a cada 1s
# Usar backoff exponencial:
delays = [5, 10, 15, 20, 30]  # segundos
for delay in delays:
    time.sleep(delay)
    status = check_status(project_id)
    if status != "running":
        break
```

---

## Links Úteis para Debug

- **Status page:** https://status.json2video.com
- **Support:** support@json2video.com
- **Community:** https://json2video.com/community
- **API Changelog:** https://json2video.com/docs/v2/changelog
