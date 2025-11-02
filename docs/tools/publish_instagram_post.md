# 📱 Instagram - Publicar Post

Publica posts no Instagram automaticamente.

## 🚀 Comando

```bash
# Arquivo local
python3 tools/publish_instagram_post.py "imagem.jpg" "Sua legenda aqui"

# URL pública
python3 tools/publish_instagram_post.py "https://url-da-imagem.jpg" "Sua legenda aqui"
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `imagem` | ✅ | Arquivo local ou URL pública |
| `legenda` | ✅ | Texto do post |

## 💡 Exemplos

```bash
# Post simples
python3 tools/publish_instagram_post.py foto.jpg "Ótimo dia! ☀️"

# Com URL
python3 tools/publish_instagram_post.py "https://exemplo.com/foto.jpg" "Confira! 📸"
```

## ⚙️ Recursos

- ✅ Aceita arquivos locais ou URLs
- ✅ Upload automático via Catbox.moe (arquivos locais)
- ✅ Converte PNG → JPEG automaticamente
- ✅ Rate limit: 100 posts/24h

## 🔧 Config

`config/instagram_config.py`

## 📖 Docs Completa

`docs/instagram-api/INSTAGRAM_API_DOCUMENTATION.md`
