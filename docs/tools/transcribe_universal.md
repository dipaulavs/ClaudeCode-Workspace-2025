# 🎤 Transcrição Universal

Transcreve vídeos e áudios de múltiplas plataformas.

## 🚀 Comando

```bash
python3 tools/transcribe_universal.py "URL" [--lang IDIOMA] [--task transcribe|translate]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `URL` | ✅ | URL do vídeo/áudio ou arquivo local via Nextcloud |
| `--lang` | ❌ | Idioma (pt, en, es). Padrão: pt |
| `--task` | ❌ | transcribe ou translate. Padrão: transcribe |

## 🌐 Plataformas Suportadas

- YouTube
- TikTok
- Instagram
- LinkedIn
- X/Twitter
- Vimeo
- URLs diretas de áudio/vídeo

## 💡 Exemplos

```bash
# YouTube
python3 tools/transcribe_universal.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang pt

# TikTok
python3 tools/transcribe_universal.py "https://www.tiktok.com/@user/video/123" --lang pt

# Arquivo local (via Nextcloud)
python3 tools/upload_to_nextcloud.py ~/Downloads/audio.m4a --days 7
python3 tools/transcribe_universal.py "URL_NEXTCLOUD_GERADA" --lang pt

# Traduzir para inglês
python3 tools/transcribe_universal.py "URL" --task translate
```

## 📦 Saída

- **Arquivos:** `transcricao_TIMESTAMP.txt` e `.json`
- **Local:** `~/Downloads/`
- **Exibe:** No terminal automaticamente

## 🔧 Config

Via RapidAPI (configurado no script)
