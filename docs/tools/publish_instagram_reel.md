# 📱 Instagram - Publicar Reel

Publica Reels (vídeos curtos até 90s) no Instagram.

## 🚀 Comando

```bash
# Arquivo local
python3 tools/publish_instagram_reel.py video.mp4 "Legenda"

# Com capa personalizada
python3 tools/publish_instagram_reel.py video.mp4 "Legenda" --cover capa.jpg

# URL pública
python3 tools/publish_instagram_reel.py "https://url-video.mp4" "Legenda"

# Apenas no feed de Reels (não no feed principal)
python3 tools/publish_instagram_reel.py video.mp4 "Legenda" --no-feed

# Com áudio personalizado
python3 tools/publish_instagram_reel.py video.mp4 "Legenda" --audio "Nome do Áudio"
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `video` | ✅ | Arquivo MP4/MOV ou URL pública |
| `legenda` | ✅ | Texto do Reel |
| `--cover` | ❌ | Imagem de capa (thumbnail) |
| `--no-feed` | ❌ | Publica apenas em Reels (não aparece no feed) |
| `--audio` | ❌ | Nome do áudio a ser usado |

## ⚙️ Recursos

- ✅ Vídeos até 90 segundos
- ✅ Formatos: MP4, MOV
- ✅ Upload automático via Catbox.moe (até 200MB)
- ✅ Capa personalizada opcional
- ✅ Controle de visibilidade (feed + Reels ou só Reels)

## 🔧 Config

`config/instagram_config.py`
