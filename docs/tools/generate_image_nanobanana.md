# 🎨 Nano Banana Image Generator

Gera imagens usando Gemini 2.5 Flash (hiper-realismo, portrait 2:3).

## 🚀 Comando

```bash
python3 tools/generate_image_nanobanana.py "prompt" [--format PNG|JPEG]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `prompt` | ✅ | Descrição da imagem |
| `--format` | ❌ | PNG ou JPEG. Padrão: PNG |

## 💡 Exemplos

```bash
# PNG (padrão)
python3 tools/generate_image_nanobanana.py "cidade futurista à noite"

# JPEG
python3 tools/generate_image_nanobanana.py "floresta tropical" --format JPEG
```

## 📦 Saída

- **Local:** `~/Downloads/`
- **Nome:** Automático em português
- **Formato:** Portrait 2:3
- **Qualidade:** Hiper-realismo, física consciente
